#!/usr/bin/env python3
# Pharma Tox Agent: ADMET/safety for SMILES.

from rdkit import Chem
from rdkit.Chem import Descriptors, Crippen, rdMolDescriptors
from rdkit.Chem.rdMolDescriptors import CalcNumRings, CalcNumAromaticRings
import json
from typing import Dict

class ToxAgent:
    def __init__(self):
        pass

    def analyze(self, smiles: str) -> Dict:
        mol = Chem.MolFromSmiles(smiles)
        if not mol:
            return {'error': 'Invalid SMILES'}
        Chem.SanitizeMol(mol)

        # Lipinski
        mw = Descriptors.MolWt(mol)
        logp = Crippen.MolLogP(mol)
        hbd = Descriptors.NumHDonors(mol)
        hba = Descriptors.NumHAcceptors(mol)
        rotb = Descriptors.NumRotatableBonds(mol)
        lipinski_viol = sum([mw > 500, logp > 5, hbd > 5, hba > 10])

        # Veber
        tpsa = Descriptors.TPSA(mol)
        veber_viol = sum([tpsa > 140, rotb > 10])

        # QED
        try:
            from rdkit.Chem import QED as QEDModule
            qed = QEDModule.qed(mol)
        except Exception:
            qed = 0.0

        # PAINS mock (simple substruct)
        pains_subs = ['c1ncnc2c1ncn2', 'cc1ccc2nsnc2c1']
        pains_count = sum(1 for sub in pains_subs if mol.HasSubstructMatch(Chem.MolFromSmarts(sub)))

        # Rings
        rings = CalcNumRings(mol)
        arom = CalcNumAromaticRings(mol)

        report = {
            'lipinski_viol': lipinski_viol,
            'veber_viol': veber_viol,
            'qed': round(qed, 3),
            'pains': pains_count,
            'risk': 'Low' if lipinski_viol == 0 and pains_count == 0 else 'Medium/High',
            'props': {'mw': round(mw,1), 'logp': round(logp,2), 'tpsa': round(tpsa,1), 'hbd': hbd, 'hba': hba, 'rotb': rotb, 'rings': rings, 'arom': arom}
        }
        return report

if __name__ == '__main__':
    import sys
    smiles = sys.argv[1] if len(sys.argv) > 1 else 'CCO'
    agent = ToxAgent()
    print(json.dumps(agent.analyze(smiles), indent=2))
