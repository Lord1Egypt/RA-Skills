#!/usr/bin/env python3
"""
Step 5: AlphaFold Model Quality Assessment (pLDDT + PAE)
Analyzes AlphaFold model confidence and outputs interface coordinates for Vina docking.

Usage:
    python step5_pae_analysis.py \
        --pdb AF_complex_rank_001.pdb \
        --pae_json predicted_aligned_error_v1.json \
        --chain_a A --chain_b B \
        --chain_a_len 200 --chain_b_len 300 \
        --output_dir ./analysis

Output:
    - pLDDT statistics per chain
    - PAE matrix analysis (interface confidence)
    - Vina Grid Box coordinates
"""
import argparse
import json
import numpy as np
import os


def parse_pdb_plddt(pdb_path):
    """Extract pLDDT scores per chain from PDB file."""
    plddt_by_chain = {}
    ca_by_chain = {}
    for line in open(pdb_path):
        if not line.startswith('ATOM'):
            continue
        if line[12:16].strip() != 'CA':
            continue
        chain = line[21]
        res = int(line[22:26])
        plddt = float(line[60:66])
        if chain not in plddt_by_chain:
            plddt_by_chain[chain] = []
            ca_by_chain[chain] = {}
        plddt_by_chain[chain].append(plddt)
        ca_by_chain[chain][res] = np.array([
            float(line[30:38]),
            float(line[38:46]),
            float(line[46:54])
        ])
    return plddt_by_chain, ca_by_chain


def analyze_pae(pae_json_path, chain_a_len, chain_b_len):
    """Analyze PAE matrix for interface confidence."""
    with open(pae_json_path) as f:
        raw = json.load(f)
    pae = np.array(raw['predicted_aligned_error'])

    n = pae.shape[0]
    mid = min(chain_a_len, n // 2)

    pae_aa = pae[:mid, :mid]
    pae_bb = pae[mid:, mid:]
    pae_ab = pae[:mid, mid:]
    pae_ba = pae[mid:, :mid]

    return {
        'chain_a_self_pae': float(pae_aa.mean()),
        'chain_b_self_pae': float(pae_bb.mean()),
        'interface_pae': float((pae_ab.mean() + pae_ba.mean()) / 2),
        'pae_matrix_shape': list(pae.shape),
        'max_pae': float(raw.get('max_predicted_aligned_error', 0)),
    }


def calc_interface_and_gridbox(ca_by_chain, chain_a, chain_b, cutoff=8.0):
    """Calculate interface residues and Grid Box center."""
    ca_a = ca_by_chain[chain_a]
    ca_b = ca_by_chain[chain_b]

    interface_a = {}
    for r1, p1 in ca_a.items():
        for r2, p2 in ca_b.items():
            dist = np.linalg.norm(p1 - p2)
            if dist < cutoff:
                if r1 not in interface_a:
                    interface_a[r1] = []
                interface_a[r1].append((r2, round(dist, 2)))

    chain_a_res = list(interface_a.keys())
    chain_b_res = set()
    for partners in interface_a.values():
        for r2, d in partners:
            chain_b_res.add(r2)

    if_ca = np.array([ca_a[r] for r in chain_a_res] + [ca_b[r] for r in chain_b_res])
    center = if_ca.mean(axis=0)

    return {
        'chain_a_interface_count': len(chain_a_res),
        'chain_b_interface_count': len(chain_b_res),
        'grid_center': {
            'x': round(float(center[0]), 1),
            'y': round(float(center[1]), 1),
            'z': round(float(center[2]), 1),
        },
        'grid_size': 22,
        'interface_residues_chain_a': chain_a_res[:10],
    }


def main():
    parser = argparse.ArgumentParser(description='AlphaFold model quality + Vina Grid Box')
    parser.add_argument('--pdb', required=True, help='AlphaFold PDB file (rank_001)')
    parser.add_argument('--pae_json', required=True, help='PAE JSON file')
    parser.add_argument('--chain_a', default='A', help='Chain A name')
    parser.add_argument('--chain_b', default='B', help='Chain B name')
    parser.add_argument('--chain_a_len', type=int, default=200, help='Chain A length (CA count)')
    parser.add_argument('--chain_b_len', type=int, default=300, help='Chain B length (CA count)')
    parser.add_argument('--output_dir', default='./analysis')
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)

    plddt_by_chain, ca_by_chain = parse_pdb_plddt(args.pdb)
    print("=== pLDDT Analysis ===")
    for chain, vals in plddt_by_chain.items():
        mean_plddt = np.mean(vals)
        high_conf = sum(1 for v in vals if v > 70)
        print(f"  Chain {chain}: pLDDT mean={mean_plddt:.1f}, >70: {high_conf}/{len(vals)} residues")

    pae_result = analyze_pae(args.pae_json, args.chain_a_len, args.chain_b_len)
    print("\n=== PAE Analysis (Interface Confidence) ===")
    print(f"  Chain A self PAE:    {pae_result['chain_a_self_pae']:.2f} A")
    print(f"  Chain B self PAE:    {pae_result['chain_b_self_pae']:.2f} A")
    print(f"  A-B Interface PAE:  {pae_result['interface_pae']:.2f} A")

    if pae_result['interface_pae'] < 10:
        verdict = "RELIABLE (proceed with docking)"
    elif pae_result['interface_pae'] < 15:
        verdict = "MODERATE (cautious interpretation)"
    else:
        verdict = "LOW confidence (docking may not be meaningful)"
    print(f"  Verdict: {verdict}")

    grid = calc_interface_and_gridbox(ca_by_chain, args.chain_a, args.chain_b)
    print("\n=== Vina Grid Box Parameters ===")
    print(f"  center_x = {grid['grid_center']['x']}")
    print(f"  center_y = {grid['grid_center']['y']}")
    print(f"  center_z = {grid['grid_center']['z']}")
    print(f"  size_x = size_y = size_z = {grid['grid_size']}")

    result = {
        'plddt': {ch: {'mean': float(np.mean(v)), 'high_conf': sum(1 for x in v if x > 70), 'total': len(v)}
                  for ch, v in plddt_by_chain.items()},
        'pae': pae_result,
        'grid_box': grid,
    }
    out_path = f"{args.output_dir}/model_quality_results.json"
    with open(out_path, 'w') as f:
        json.dump(result, f, indent=2)
    print(f"\nResults saved: {out_path}")
    return result


if __name__ == '__main__':
    main()
