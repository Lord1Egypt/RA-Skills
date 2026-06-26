#!/usr/bin/env python3
"""
Step 6: AutoDock Vina Molecular Docking
Main script for running molecular docking.

Prerequisites:
    1. receptor.pdbqt - Convert from PDB using obabel
    2. ligand.pdbqt - Convert from SDF using obabel
    3. Grid Box coordinates from step5_pae_analysis.py

Usage:
    python step6_vina_docking.py \
        --receptor_pdb receptor.pdb \
        --ligand_sdf ligand.sdf \
        --center_x 0.0 --center_y 0.0 --center_z 0.0 \
        --size 22 \
        --output_dir ./docking_results \
        --vina_path ./vina

Output:
    - ligand_out.pdbqt        # All docking poses
    - vina_maps.*.map         # Affinity maps
    - docking_summary.json    # Results summary
"""
import argparse
import subprocess
import json
import numpy as np
import os
import re


def prepare_receptor(pdb_file, output_path):
    """Convert PDB to PDBQT using OpenBabel."""
    cmd = [
        'obabel', '-ipdb', pdb_file,
        '-opdbqt', '-O', output_path, '-xr'
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"obabel failed: {result.stderr}")
    print(f"  Receptor prepared: {output_path}")
    return output_path


def prepare_ligand(sdf_file, output_path):
    """Convert SDF to PDBQT using OpenBabel."""
    cmd = [
        'obabel', '-isdf', sdf_file,
        '-opdbqt', '-O', output_path
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"obabel ligand failed: {result.stderr}")
    print(f"  Ligand prepared: {output_path}")
    return output_path


def run_vina(receptor, ligand, center, size, vina_path='./vina',
              output_dir='.', exhaustiveness=16, num_modes=20):
    """Run AutoDock Vina docking."""
    os.makedirs(output_dir, exist_ok=True)
    maps_prefix = os.path.join(output_dir, 'vina_maps')

    cmd = [
        vina_path,
        '--receptor', receptor,
        '--ligand', ligand,
        '--center_x', str(center['x']),
        '--center_y', str(center['y']),
        '--center_z', str(center['z']),
        '--size_x', str(size),
        '--size_y', str(size),
        '--size_z', str(size),
        '--scoring', 'vina',
        '--write_maps', maps_prefix,
        '--force_even_voxels',
        '--exhaustiveness', str(exhaustiveness),
        '--num_modes', str(num_modes),
    ]

    print(f"\nRunning Vina...")
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=output_dir)
    output = result.stdout + result.stderr
    print(output[-2000:])

    if result.returncode != 0:
        raise RuntimeError(f"Vina failed: {result.stderr[-500:]}")

    return output


def parse_vina_output(output_text):
    """Parse Vina output to extract binding affinities."""
    modes = []
    for line in output_text.split('\n'):
        if re.match(r'\s*\d+\s+[-−]', line):
            parts = line.split()
            if len(parts) >= 4:
                try:
                    mode = {
                        'mode': int(parts[0]),
                        'affinity': float(parts[1]),
                        'rmsd_lb': float(parts[2]),
                        'rmsd_ub': float(parts[3]),
                    }
                    modes.append(mode)
                except ValueError:
                    pass
    return modes


def analyze_binding_pose(ligand_out_pdbqt, receptor_pdb, grid_center):
    """Analyze spatial position of best binding pose."""
    ca_a_coords = {}
    ca_b_coords = {}
    for line in open(receptor_pdb):
        if line.startswith('ATOM') and line[12:16].strip() == 'CA':
            ch = line[21]
            res = int(line[22:26])
            coords = np.array([float(line[30:38]), float(line[38:46]), float(line[46:54])])
            if ch == 'A':
                ca_a_coords[res] = coords
            else:
                ca_b_coords[res] = coords

    lig_coords = []
    in_m1 = False
    for line in open(ligand_out_pdbqt):
        if line.startswith('MODEL 1'):
            in_m1 = True
            continue
        if line.startswith('MODEL 2'):
            break
        if in_m1 and line.startswith('ATOM'):
            lig_coords.append(np.array([
                float(line[30:38]),
                float(line[38:46]),
                float(line[46:54])
            ]))

    if not lig_coords:
        return None

    lig_center = np.mean(lig_coords, axis=0)
    dists_a = [np.linalg.norm(lig_center - c) for c in ca_a_coords.values()]
    dists_b = [np.linalg.norm(lig_center - c) for c in ca_b_coords.values()]
    grid_center_arr = np.array([grid_center['x'], grid_center['y'], grid_center['z']])

    return {
        'ligand_center': {
            'x': round(float(lig_center[0]), 1),
            'y': round(float(lig_center[1]), 1),
            'z': round(float(lig_center[2]), 1),
        },
        'shift_from_grid_center': round(float(np.linalg.norm(lig_center - grid_center_arr)), 1),
        'min_dist_chain_a': round(float(min(dists_a)), 1),
        'min_dist_chain_b': round(float(min(dists_b)), 1),
        'contacts_4A_chain_a': sum(1 for d in dists_a if d < 4.0),
        'contacts_4A_chain_b': sum(1 for d in dists_b if d < 4.0),
        'hydrogen_bond_range': sum(1 for d in dists_a if d < 3.5) + sum(1 for d in dists_b if d < 3.5),
    }


def main():
    parser = argparse.ArgumentParser(description='AutoDock Vina molecular docking')
    parser.add_argument('--receptor_pdb', required=True, help='Receptor PDB file')
    parser.add_argument('--ligand_sdf', required=True, help='Ligand SDF file')
    parser.add_argument('--center_x', type=float, required=True, help='Grid center X')
    parser.add_argument('--center_y', type=float, required=True, help='Grid center Y')
    parser.add_argument('--center_z', type=float, required=True, help='Grid center Z')
    parser.add_argument('--size', type=int, default=22, help='Grid box size (Angstrom)')
    parser.add_argument('--vina_path', default='./vina', help='Path to vina executable')
    parser.add_argument('--output_dir', default='./docking_results', help='Output directory')
    parser.add_argument('--receptor_pdbqt', default=None, help='Pre-made receptor PDBQT (skip prep)')
    parser.add_argument('--ligand_pdbqt', default=None, help='Pre-made ligand PDBQT (skip prep)')
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)
    center = {'x': args.center_x, 'y': args.center_y, 'z': args.center_z}

    if args.receptor_pdbqt and os.path.exists(args.receptor_pdbqt):
        receptor_pdbqt = args.receptor_pdbqt
        print(f"Using existing receptor: {receptor_pdbqt}")
    else:
        receptor_pdbqt = os.path.join(args.output_dir, 'receptor.pdbqt')
        prepare_receptor(args.receptor_pdb, receptor_pdbqt)

    if args.ligand_pdbqt and os.path.exists(args.ligand_pdbqt):
        ligand_pdbqt = args.ligand_pdbqt
        print(f"Using existing ligand: {ligand_pdbqt}")
    else:
        ligand_pdbqt = os.path.join(args.output_dir, 'ligand.pdbqt')
        prepare_ligand(args.ligand_sdf, ligand_pdbqt)

    output = run_vina(
        receptor=receptor_pdbqt,
        ligand=ligand_pdbqt,
        center=center,
        size=args.size,
        vina_path=args.vina_path,
        output_dir=args.output_dir,
    )

    modes = parse_vina_output(output)
    print(f"\n=== Docking Results ===")
    print(f"{'Mode':<6} {'Affinity (kcal/mol)':<20} {'RMSD l.b.':<12} {'RMSD u.b.'}")
    for m in modes:
        print(f"  {m['mode']:<4} {m['affinity']:<20.3f} {m['rmsd_lb']:<12.3f} {m['rmsd_ub']:.3f}")

    ligand_out = os.path.join(args.output_dir, 'ligand_out.pdbqt')
    if os.path.exists(ligand_out):
        pose = analyze_binding_pose(ligand_out, args.receptor_pdb, center)
        print(f"\n=== Binding Pose Analysis ===")
        print(f"  Ligand center: ({pose['ligand_center']['x']}, {pose['ligand_center']['y']}, {pose['ligand_center']['z']})")
        print(f"  Shift from grid center: {pose['shift_from_grid_center']} A")
        print(f"  Min dist to Chain A: {pose['min_dist_chain_a']} A")
        print(f"  Min dist to Chain B: {pose['min_dist_chain_b']} A")
        print(f"  Contacts <4A: A={pose['contacts_4A_chain_a']}, B={pose['contacts_4A_chain_b']}")
    else:
        pose = None
        print("Warning: ligand_out.pdbqt not found")

    summary = {
        'grid_center': center,
        'grid_size': args.size,
        'modes': modes,
        'best_mode': modes[0] if modes else None,
        'pose_analysis': pose,
    }
    out_path = os.path.join(args.output_dir, 'docking_summary.json')
    with open(out_path, 'w') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    print(f"\nSummary saved: {out_path}")

    if modes:
        best_affinity = modes[0]['affinity']
        if best_affinity < -9:
            verdict = "STRONG binding (comparable to reference)"
        elif best_affinity < -7:
            verdict = "MODERATE binding (may be significant)"
        else:
            verdict = "WEAK/NO binding"
        print(f"\n=== Verdict ===")
        print(f"  Best affinity: {best_affinity:.3f} kcal/mol")
        print(f"  {verdict}")


if __name__ == '__main__':
    main()
