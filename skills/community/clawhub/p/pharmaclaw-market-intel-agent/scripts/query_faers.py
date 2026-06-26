#!/usr/bin/env python3
import requests
import pandas as pd
import matplotlib.pyplot as plt
import argparse
import json
import os
import re
import sys

def get_drug_name_from_smiles(smiles):
    """Resolve SMILES to primary drug name via PubChem API."""
    try:
        # Get CID from SMILES (strict canonical)
        cid_url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/smiles/{smiles}/cids/JSON"
        cid_resp = requests.get(cid_url, timeout=10)
        if cid_resp.status_code != 200:
            return None
        cids = cid_resp.json().get('IdentifierList', {}).get('CID', [])
        if not cids:
            return None
        cid = cids[0]
        
        # Get synonyms
        syn_url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{cid}/synonyms/JSON"
        syn_resp = requests.get(syn_url, timeout=10)
        if syn_resp.status_code != 200:
            return None
        info = syn_resp.json().get('InformationList', {}).get('Information', [{}])[0]
        synonyms = info.get('Synonym', [])
        if synonyms:
            # Prefer non-IUPAC name if available
            for syn in synonyms:
                if not syn.startswith('InChI=') and len(syn) < 50:
                    return syn
            return synonyms[0]
    except:
        pass
    return None

def query_faers(drug_query, count_field=None, limit=100):
    """Query openFDA FAERS API."""
    base_url = "https://api.fda.gov/drug/event.json"
    params = {
        'search': f'patient.drug.medicinalproduct:"{drug_query}"',
        'limit': limit
    }
    if count_field:
        params['count'] = count_field
        params['limit'] = 0  # No results for count
    resp = requests.get(base_url, params=params, timeout=30)
    resp.raise_for_status()
    return resp.json()

def parse_year(date_str):
    if date_str and len(date_str) >= 4:
        return int(date_str[:4])
    return None

def main():
    parser = argparse.ArgumentParser(description='Query FAERS for drug adverse events, generate trends and plots.')
    parser.add_argument('--drug', required=True, help='Drug name or SMILES string')
    parser.add_argument('--output', default='./faers_output', help='Output directory')
    parser.add_argument('--limit-events', type=int, default=20, help='Max events to list')
    args = parser.parse_args()

    os.makedirs(args.output, exist_ok=True)
    drug_name = args.drug.strip()

    # Resolve SMILES if looks like one
    if re.search(r'^[A-Za-z0-9#\(\)=\[\]@+\-%/.]+$', drug_name) and len(drug_name) > 3 and not drug_name.isalpha():
        print(f"Resolving SMILES '{drug_name}' to drug name...", file=sys.stderr)
        resolved = get_drug_name_from_smiles(drug_name)
        if resolved:
            drug_name = resolved
            print(f"Resolved to: {drug_name}", file=sys.stderr)
        else:
            print(f"Failed to resolve SMILES '{args.drug}', using as-is.", file=sys.stderr)

    print(f"Querying FAERS for drug: {drug_name}", file=sys.stderr)

    results = {}

    # 1. Yearly trends
    try:
        yearly_data = query_faers(drug_name, count_field='receivedate', limit=100)
        if 'results' in yearly_data:
            df_year = pd.DataFrame(yearly_data['results'])
            df_year['year'] = df_year['term'].apply(parse_year)
            yearly_counts = df_year.dropna(subset=['year']).groupby('year')['count'].sum().reset_index()
            yearly_counts.to_json(os.path.join(args.output, f'{drug_name}_yearly_trends.json'), orient='records', indent=2)
            results['yearly_trends'] = yearly_counts.to_dict('records')

            plt.figure(figsize=(10, 6))
            plt.bar(yearly_counts['year'], yearly_counts['count'])
            plt.title(f'FAERS Yearly Report Counts: {drug_name}')
            plt.xlabel('Year')
            plt.ylabel('Number of Reports')
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.savefig(os.path.join(args.output, f'{drug_name}_yearly_trends.png'), dpi=150, bbox_inches='tight')
            plt.close()
    except Exception as e:
        print(f"Error generating yearly trends: {e}", file=sys.stderr)

    # 2. Top reactions
    try:
        reactions_data = query_faers(drug_name, count_field='patient.reaction.reactionmeddrapt', limit=25)
        if 'results' in reactions_data:
            df_react = pd.DataFrame(reactions_data['results'].head(10))
            df_react.to_json(os.path.join(args.output, f'{drug_name}_top_reactions.json'), orient='records', indent=2)
            results['top_reactions'] = df_react.to_dict('records')

            plt.figure(figsize=(10, 8))
            plt.barh(range(len(df_react)), df_react['count'])
            plt.yticks(range(len(df_react)), df_react['term'])
            plt.title(f'Top 10 Reactions: {drug_name}')
            plt.xlabel('Number of Reports')
            plt.tight_layout()
            plt.savefig(os.path.join(args.output, f'{drug_name}_top_reactions.png'), dpi=150, bbox_inches='tight')
            plt.close()
    except Exception as e:
        print(f"Error generating top reactions: {e}", file=sys.stderr)

    # 3. Top outcomes
    try:
        outcomes_data = query_faers(drug_name, count_field='patient.outcome.result', limit=25)
        if 'results' in outcomes_data:
            df_out = pd.DataFrame(outcomes_data['results'].head(10))
            df_out.to_json(os.path.join(args.output, f'{drug_name}_top_outcomes.json'), orient='records', indent=2)
            results['top_outcomes'] = df_out.to_dict('records')

            plt.figure(figsize=(10, 8))
            plt.barh(range(len(df_out)), df_out['count'])
            plt.yticks(range(len(df_out)), df_out['term'])
            plt.title(f'Top 10 Outcomes: {drug_name}')
            plt.xlabel('Number of Reports')
            plt.tight_layout()
            plt.savefig(os.path.join(args.output, f'{drug_name}_top_outcomes.png'), dpi=150, bbox_inches='tight')
            plt.close()
    except Exception as e:
        print(f"Error generating top outcomes: {e}", file=sys.stderr)

    # 4. Recent events list (limited)
    try:
        events_data = query_faers(drug_name, limit=args.limit_events)
        events_path = os.path.join(args.output, f'{drug_name}_recent_events.json')
        with open(events_path, 'w') as f:
            json.dump(events_data, f, indent=2)
        results['recent_events_count'] = len(events_data.get('results', []))
    except Exception as e:
        print(f"Error fetching events list: {e}", file=sys.stderr)

    # Summary JSON
    summary_path = os.path.join(args.output, f'{drug_name}_summary.json')
    with open(summary_path, 'w') as f:
        json.dump(results, f, indent=2)

    print(f"Analysis complete. Files saved to: {args.output}/", file=sys.stdout)
    print(f"Summary: {summary_path}", file=sys.stdout)

if __name__ == '__main__':
    main()
