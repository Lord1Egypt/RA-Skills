#!/usr/bin/env python3
"""
Step 1: Collect IRED (Imine Reductase) sequences from UniProt
"""

import requests
import json
import time
import sys
from pathlib import Path

PROJECT_DIR = Path("/root/autodl-tmp/ou_a1d19d5984eecd78f231c50f774eddb0/IRED_phylogeny")
SEQ_DIR = PROJECT_DIR / "sequences"

def search_uniprot(query, size=500):
    """Search UniProt REST API"""
    base_url = "https://rest.uniprot.org/uniprotkb/search"
    params = {
        "query": query,
        "format": "json",
        "size": size,
    }
    try:
        resp = requests.get(base_url, params=params, timeout=120)
        resp.raise_for_status()
        data = resp.json()
        return data.get("results", [])
    except Exception as e:
        print(f"  Search error: {e}")
        return []

def main():
    print("=" * 60)
    print("IRED Sequence Collection from UniProt")
    print("=" * 60)
    
    # Multiple search queries to get diverse IRED set
    queries = [
        '"imine reductase"',
        '"imine reductase activity"',
        'gene:"imine reductase"',
    ]
    
    all_entries = {}  # dedup by accession
    
    for i, query in enumerate(queries):
        print(f"\n[{i+1}] Searching: {query}")
        results = search_uniprot(query, size=500)
        print(f"  Raw results: {len(results)}")
        for r in results:
            acc = r.get("primaryAccession", "")
            if acc and acc not in all_entries:
                all_entries[acc] = r
    
    print(f"\nTotal unique sequences: {len(all_entries)}")
    
    # Filter and process
    valid_entries = []
    for acc, entry in all_entries.items():
        seq = entry.get("sequence", {}).get("value", "")
        length = len(seq)
        if 150 <= length <= 600:  # typical IRED range
            pd = entry.get("proteinDescription", {})
            name = pd.get("recommendedName", {}).get("fullName", {}).get("value", "Unknown")
            org = entry.get("organism", {}).get("scientificName", "Unknown")
            tax = entry.get("organism", {}).get("taxonId", 0)
            valid_entries.append({
                "accession": acc,
                "entry_name": entry.get("uniProtkbId", acc),
                "protein_name": name,
                "organism": org,
                "taxon_id": tax,
                "sequence": seq,
                "length": length,
            })
    
    print(f"After length filter (150-600 aa): {len(valid_entries)}")
    
    if not valid_entries:
        print("No valid sequences found!")
        sys.exit(1)
    
    # Save metadata
    meta_file = SEQ_DIR / "ired_metadata.json"
    with open(meta_file, "w") as f:
        json.dump(valid_entries, f, indent=2, ensure_ascii=False)
    print(f"\nMetadata saved: {meta_file}")
    
    # Save FASTA
    fasta_file = SEQ_DIR / "ired_sequences.fasta"
    with open(fasta_file, "w") as f:
        for e in valid_entries:
            f.write(f">{e['accession']}|{e['organism']}|{e['protein_name']}\n")
            # Wrap sequence at 80 chars
            seq = e["sequence"]
            for i in range(0, len(seq), 80):
                f.write(seq[i:i+80] + "\n")
    
    print(f"FASTA saved: {fasta_file}")
    
    # Summary stats
    organisms = set(e["organism"] for e in valid_entries)
    lengths = [e["length"] for e in valid_entries]
    print(f"\n=== Summary ===")
    print(f"Total sequences: {len(valid_entries)}")
    print(f"Unique organisms: {len(organisms)}")
    print(f"Length range: {min(lengths)} - {max(lengths)} aa")
    print(f"Average length: {sum(lengths)/len(lengths):.0f} aa")
    
    # Top 10 organisms
    from collections import Counter
    org_counts = Counter(e["organism"] for e in valid_entries)
    print(f"\nTop organisms:")
    for org, cnt in org_counts.most_common(10):
        print(f"  {org}: {cnt}")

if __name__ == "__main__":
    main()
