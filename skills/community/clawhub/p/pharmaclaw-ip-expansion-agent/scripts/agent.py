#!/usr/bin/env python3
# Main IP Expansion Agent class. Compatible w/ OpenClaw exec. Standalone or importable.

import json
import sys
import argparse
import sqlite3
import os
import logging
from datetime import datetime
from typing import List, Dict, Any, Optional
# Cheminformatics
from rdkit import Chem
from rdkit.Chem import Descriptors, Draw, rdMolDescriptors
from rdkit.Chem.Draw import rdMolDraw2D
from rdkit import DataStructs
# NLP (assume scispacy or spacy)
try:
    import spacy
    from scispacy.umls_linking import UmlsEntityLinker
except ImportError:
    print("Install: pip install scispacy[scispacy_models] https://s3-us-west-2.amazonaws.com/ai2-s2-scispacy/releases/v0.5.1/en_core_sci_sm-0.5.1.tar.gz")
    sys.exit(1)
# APIs
import requests
import pandas as pd

logging.basicConfig(filename='logs/ip_expansion.log', level=logging.INFO)

class IPExpansionAgent:
    def __init__(self, db_path: str = 'ip_portfolio.db'):
        self.db_path = db_path
        self.db = sqlite3.connect(db_path)
        self._init_db()
        self.nlp = spacy.load("en_core_sci_sm")
        self.linker = UmlsEntityLinker(resolve_abbreviations=True)
        self.nlp.add_pipe(self.linker)

    def _init_db(self):
        """Init portfolio table."""
        schema = """
        CREATE TABLE IF NOT EXISTS portfolio (
            id INTEGER PRIMARY KEY,
            patent_num TEXT UNIQUE,
            title TEXT,
            filing_date TEXT,
            expiration_date TEXT,
            claims TEXT,
            smiles TEXT,
            therapeutic TEXT,
            status TEXT DEFAULT 'active',
            added_date TEXT DEFAULT CURRENT_TIMESTAMP
        );
        """
        self.db.executescript(schema)
        self.db.commit()

    def add_asset(self, patent_data: Dict[str, Any]):
        """Add to portfolio."""
        cur = self.db.cursor()
        cur.execute('''
            INSERT OR REPLACE INTO portfolio (patent_num, title, filing_date, expiration_date, claims, smiles, therapeutic)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (patent_data['num'], patent_data['title'], patent_data['filing'], patent_data['exp'], 
              json.dumps(patent_data['claims']), patent_data.get('smiles'), patent_data.get('therapeutic')))
        self.db.commit()
        logging.info(f"Added {patent_data['num']}")

    def track_portfolio(self) -> List[Dict]:
        """Monitor expirations (next 12mo)."""
        today = datetime.now()
        cutoff = (today.replace(year=today.year+1)).isoformat()
        cur = self.db.cursor()
        cur.execute('SELECT * FROM portfolio WHERE expiration_date < ? AND status="active"', (cutoff,))
        return [dict(row) for row in cur.fetchall()]

    def infringement_analysis(self, query_smiles: List[str], portfolio_smiles: Optional[List[str]] = None, threshold: float = 0.85) -> Dict:
        """Morgan FP Tanimoto vs patents/portfolio."""
        query_fps = [rdMolDescriptors.GetMorganFingerprintAsBitVect(Chem.MolFromSmiles(s), 2, 2048) for s in query_smiles if s]
        risks = []
        # Vs portfolio
        if portfolio_smiles:
            port_fps = [rdMolDescriptors.GetMorganFingerprintAsBitVect(Chem.MolFromSmiles(s), 2, 2048) for s in portfolio_smiles]
            for i, qfp in enumerate(query_fps):
                sims = [DataStructs.TanimotoSimilarity(qfp, pfp) for pfp in port_fps]
                max_sim = max(sims)
                if max_sim > threshold:
                    risks.append({'query_idx': i, 'max_sim': max_sim, 'risk': 'high'})
        # Vs PubChem recent (mock; extend w/ patent SMILES)
        return {'risks': risks, 'threshold': threshold}

    def fto_assess(self, therapeutic: str, keywords: List[str]) -> Dict:
        """FTO: Search USPTO/PubChem for blocking."""
        # USPTO PatentsView
        url = 'https://api.patentsview.org/patents/query'
        q = {'q': {'_and': [{'text': {'_any': keywords}}, {'text': therapeutic}]}, 'f': ['patent_number', 'patent_title', 'filing_date']}
        resp = requests.post(url, json=q).json()
        patents = resp.get('patents', [])
        blockers = [p for p in patents if self._is_blocking(p)]
        # PubChem similar actives
        pubchem_url = f'https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/fastsimilarity_2d/{therapeutic}/cids/JSON?Threshold=80'
        pc_resp = requests.get(pubchem_url).json()
        return {'blockers': len(blockers), 'patents': patents[:5], 'pubchem_hits': pc_resp}

    def _is_blocking(self, patent: Dict) -> bool:
        """Simple heuristic: recent, broad claims."""
        return 'method of use' in patent.get('patent_title', '').lower()  # Enhance w/ NLP

    def prior_art_mining(self, query: str) -> Dict:
        """NLP extract chemicals/claims from fetched patents/lit."""
        doc = self.nlp(query)
        entities = [(ent.text, ent._.kb_ents) for ent in doc.ents if ent.label_ == 'CHEMICAL']
        nov_sugs = self.suggest_novel(entities[0][0] if entities else query)  # First chem
        return {'entities': entities, 'novel_suggestions': nov_sugs}

    def suggest_novel(self, smiles: str) -> List[str]:
        """RDKit bioisosteres/derivatives."""
        mol = Chem.MolFromSmiles(smiles)
        # Simple: replace halogens, add methyls (extend w/ BRICS)
        replacements = {'Cl': 'F', 'Br': 'Cl', 'F': 'Me'}  # Bioisostere map
        news = []
        for atom in mol.GetAtoms():
            if atom.GetSymbol() in replacements:
                newmol = Chem.RWMol(mol)
                newmol.GetAtomWithIdx(atom.GetIdx()).SetAtomicNum(Chem.AtomFromSmiles(replacements[atom.GetSymbol()]).GetAtomicNum())
                news.append(Chem.MolToSmiles(newmol.GetMol()))
        return news[:3]

    def strategic_expansion(self, data: Dict) -> Dict:
        """Recommend claims based on FTO/novelty."""
        recs = {'continuations': True if data.get('white_space') else False,
                'method_use': 'Prioritize if efficacy data from Tox',
                'repurpose': 'Check ChEMBL for new indications'}
        return recs

    def generate_report(self, analysis: Dict, output_dir: str = '.') -> str:
        """MD + PNG viz."""
        mols = [Chem.MolFromSmiles(s) for s in analysis.get('smiles', [])]
        img = Draw.MolsToGridImage(mols, molsPerRow=4, subImgSize=(200,200))
        viz_path = os.path.join(output_dir, 'ip_viz.png')
        img.save(viz_path)
        report = f"""
# IP Expansion Report {datetime.now()}

Risks: {json.dumps(analysis['risks'], indent=2)}
Suggestions: {analysis['suggestions']}
Viz: {viz_path}
"""
        md_path = os.path.join(output_dir, 'ip_report.md')
        with open(md_path, 'w') as f:
            f.write(report)
        return md_path

    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Main entry: Process input from other agents."""
        mode = input_data.get('mode', 'analysis')
        smiles = input_data.get('smiles', [])
        therapeutic = input_data.get('therapeutic', '')
        # Chain logic
        if smiles:
            inf = self.infringement_analysis(smiles)
            fto = self.fto_assess(therapeutic, input_data.get('keywords', []))
            prior = self.prior_art_mining(input_data.get('query', ''))
            strat = self.strategic_expansion({'fto': fto})
            report = self.generate_report({'risks': inf['risks'], 'suggestions': prior['novel_suggestions'], 'smiles': smiles})
            output = {'infringement': inf, 'fto': fto, 'novelty': prior, 'strategy': strat, 'report': report}
        else:
            output = {'portfolio': self.track_portfolio()}
        # Log
        logging.info(json.dumps(output))
        return output

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', default='analysis')
    parser.add_argument('--input', required=True, help='JSON input str')
    args = parser.parse_args()
    data = json.loads(args.input)
    agent = IPExpansionAgent()
    result = agent.run(data)
    print(json.dumps(result, indent=2))
