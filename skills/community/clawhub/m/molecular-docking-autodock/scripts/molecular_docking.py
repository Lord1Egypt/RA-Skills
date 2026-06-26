#!/usr/bin/env python3
import os
import sys
import argparse
import tempfile
import subprocess
import re
from rdkit import Chem
from rdkit.Chem import AllChem
from meeko import MoleculePreparation
from Bio.PDB import PDBParser, PDBIO, Select
import openbabel as ob

class ProteinPreparer:
    def __init__(self, input_pdb, output_dir):
        self.input_pdb = input_pdb
        self.output_dir = output_dir
        self.prepared_pdbqt = os.path.join(output_dir, "protein_prepared.pdbqt")
    
    def prepare(self):
        # Step 1: Remove water and non-standard residues
        parser = PDBParser(QUIET=True)
        structure = parser.get_structure("protein", self.input_pdb)
        
        class NonWaterAndStandardSelect(Select):
            def accept_residue(self, residue):
                if residue.get_id()[0] == 'W': # Skip water
                    return False
                if residue.get_resname() not in ['ALA', 'ARG', 'ASN', 'ASP', 'CYS', 'GLN', 'GLU', 'GLY', 'HIS', 'ILE', 'LEU', 'LYS', 'MET', 'PHE', 'PRO', 'SER', 'THR', 'TRP', 'TYR', 'VAL']:
                    return False
                return True
        
        io = PDBIO()
        io.set_structure(structure)
        temp_pdb = os.path.join(self.output_dir, "protein_no_water.pdb")
        io.save(temp_pdb, NonWaterAndStandardSelect())
        
        # Step 2: Convert to PDBQT with AutoDock Tools script or obabel
        cmd = f"obabel {temp_pdb} -O {self.prepared_pdbqt} -xr -h --partialcharge gasteiger"
        subprocess.run(cmd, shell=True, check=True, capture_output=True)
        os.remove(temp_pdb)
        return self.prepared_pdbqt

class LigandPreparer:
    def __init__(self, smiles, output_dir):
        self.smiles = smiles
        self.output_dir = output_dir
        self.prepared_pdbqt = os.path.join(output_dir, "ligand_prepared.pdbqt")
    
    def prepare(self):
        # Generate 3D conformer from SMILES
        mol = Chem.MolFromSmiles(self.smiles)
        if not mol:
            raise ValueError("Invalid SMILES string")
        mol = Chem.AddHs(mol)
        AllChem.EmbedMolecule(mol, randomSeed=42)
        AllChem.UFFOptimizeMolecule(mol)
        
        # Convert to PDBQT with meeko
        preparator = MoleculePreparation()
        preparator.prepare(mol)
        preparator.write_pdbqt_file(self.prepared_pdbqt)
        return self.prepared_pdbqt

class PocketParser:
    def __init__(self, pocket_desc, protein_pdb, output_dir):
        self.pocket_desc = pocket_desc
        self.protein_pdb = protein_pdb
        self.output_dir = output_dir
    
    def parse(self):
        # Check if pocket is coordinate format
        coord_pattern = r"center_x\s*=\s*([\d\.-]+)\s*center_y\s*=\s*([\d\.-]+)\s*center_z\s*=\s*([\d\.-]+)\s*size_x\s*=\s*([\d\.]+)\s*size_y\s*=\s*([\d\.]+)\s*size_z\s*=\s*([\d\.]+)"
        match = re.search(coord_pattern, self.pocket_desc, re.IGNORECASE)
        if match:
            return {
                "center_x": float(match.group(1)),
                "center_y": float(match.group(2)),
                "center_z": float(match.group(3)),
                "size_x": float(match.group(4)),
                "size_y": float(match.group(5)),
                "size_z": float(match.group(6))
            }
        
        # If text description, use p2rank to predict pockets
        print("Detected text pocket description, running p2rank pocket prediction...")
        p2rank_output = os.path.join(self.output_dir, "p2rank_output")
        os.makedirs(p2rank_output, exist_ok=True)
        cmd = f"prank predict -f {self.protein_pdb} -o {p2rank_output}"
        subprocess.run(cmd, shell=True, check=True, capture_output=True)
        
        # Read top pocket result
        predict_file = os.path.join(p2rank_output, os.path.basename(self.protein_pdb).replace(".pdb", "_predictions.csv"))
        with open(predict_file, "r") as f:
            lines = f.readlines()
            if len(lines) < 2:
                raise ValueError("No pockets detected, please provide explicit coordinates")
            top_pocket = lines[1].split(",")
            center_x = float(top_pocket[5])
            center_y = float(top_pocket[6])
            center_z = float(top_pocket[7])
            return {
                "center_x": center_x,
                "center_y": center_y,
                "center_z": center_z,
                "size_x": 20.0,
                "size_y": 20.0,
                "size_z": 20.0
            }

class DockingRunner:
    def __init__(self, protein_pdbqt, ligand_pdbqt, pocket_config, output_dir, num_modes=1, exhaustiveness=8):
        self.protein_pdbqt = protein_pdbqt
        self.ligand_pdbqt = ligand_pdbqt
        self.pocket_config = pocket_config
        self.output_dir = output_dir
        self.num_modes = num_modes
        self.exhaustiveness = exhaustiveness
        self.output_pdbqt = os.path.join(output_dir, "docking_results.pdbqt")
    
    def run(self):
        # Write VINA config file
        config_file = os.path.join(self.output_dir, "vina_config.txt")
        with open(config_file, "w") as f:
            f.write(f"receptor = {self.protein_pdbqt}\n")
            f.write(f"ligand = {self.ligand_pdbqt}\n")
            f.write(f"center_x = {self.pocket_config['center_x']}\n")
            f.write(f"center_y = {self.pocket_config['center_y']}\n")
            f.write(f"center_z = {self.pocket_config['center_z']}\n")
            f.write(f"size_x = {self.pocket_config['size_x']}\n")
            f.write(f"size_y = {self.pocket_config['size_y']}\n")
            f.write(f"size_z = {self.pocket_config['size_z']}\n")
            f.write(f"num_modes = {self.num_modes}\n")
            f.write(f"exhaustiveness = {self.exhaustiveness}\n")
            f.write(f"out = {self.output_pdbqt}\n")
        
        # Run VINA
        cmd = f"vina --config {config_file}"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(f"VINA docking failed: {result.stderr}")
        
        # Save docking log
        with open(os.path.join(self.output_dir, "docking_log.txt"), "w") as f:
            f.write(result.stdout)
        
        return self.output_pdbqt

class ResultExporter:
    def __init__(self, protein_pdb, docking_pdbqt, output_dir, num_modes=1):
        self.protein_pdb = protein_pdb
        self.docking_pdbqt = docking_pdbqt
        self.output_dir = output_dir
        self.num_modes = num_modes
    
    def export(self):
        # Convert ligand PDBQT to PDB
        ligand_pdbs = []
        for i in range(self.num_modes):
            ligand_pdb = os.path.join(self.output_dir, f"ligand_mode_{i+1}.pdb")
            cmd = f"obabel {self.docking_pdbqt} -O {ligand_pdb} -m -f {i+1} -l {i+1}"
            subprocess.run(cmd, shell=True, check=True, capture_output=True)
            ligand_pdbs.append(ligand_pdb)
        
        # Combine protein and top ligand into complex PDB
        complex_pdb = os.path.join(self.output_dir, "docked_complex_top1.pdb")
        with open(self.protein_pdb, "r") as f_prot, open(ligand_pdbs[0], "r") as f_lig, open(complex_pdb, "w") as f_out:
            for line in f_prot:
                if not line.startswith("END"):
                    f_out.write(line)
            f_out.write("TER\n")
            for line in f_lig:
                if line.startswith("ATOM") or line.startswith("HETATM"):
                    f_out.write(line)
            f_out.write("END\n")
        
        # Extract docking scores
        scores = []
        with open(os.path.join(self.output_dir, "docking_log.txt"), "r") as f:
            for line in f:
                if line.strip().startswith(str(len(scores)+1)) and len(line.strip().split()) ==4:
                    parts = line.strip().split()
                    scores.append({
                        "mode": int(parts[0]),
                        "affinity_kcal_mol": float(parts[1]),
                        "rmsd_lb": float(parts[2]),
                        "rmsd_ub": float(parts[3])
                    })
        
        # Save scores
        with open(os.path.join(self.output_dir, "docking_scores.txt"), "w") as f:
            f.write("Mode\tAffinity (kcal/mol)\tRMSD lower bound\tRMSD upper bound\n")
            for score in scores:
                f.write(f"{score['mode']}\t{score['affinity_kcal_mol']}\t{score['rmsd_lb']}\t{score['rmsd_ub']}\n")
        
        print(f"Docking completed successfully!")
        print(f"Top 1 affinity: {scores[0]['affinity_kcal_mol']} kcal/mol")
        print(f"Complex structure saved to: {complex_pdb}")
        print(f"All scores saved to: {os.path.join(self.output_dir, 'docking_scores.txt')}")
        return complex_pdb, scores

def main():
    parser = argparse.ArgumentParser(description="AutoDock VINA molecular docking full workflow")
    parser.add_argument("--protein", required=True, help="Input protein PDB file path")
    parser.add_argument("--smiles", required=True, help="Small molecule SMILES string")
    parser.add_argument("--pocket", required=True, help="Pocket description: coordinate format (center_x=xx center_y=xx center_z=xx size_x=xx size_y=xx size_z=xx) or text description")
    parser.add_argument("--output_dir", default="./docking_results", help="Output directory, default ./docking_results")
    parser.add_argument("--num_modes", type=int, default=1, help="Number of docking modes to output, default 1")
    parser.add_argument("--exhaustiveness", type=int, default=8, help="VINA exhaustiveness parameter, default 8")
    args = parser.parse_args()
    
    os.makedirs(args.output_dir, exist_ok=True)
    
    try:
        # Step 1: Prepare protein
        print("Step 1/5: Preparing protein...")
        protein_preparer = ProteinPreparer(args.protein, args.output_dir)
        protein_pdbqt = protein_preparer.prepare()
        
        # Step 2: Prepare ligand
        print("Step 2/5: Preparing ligand from SMILES...")
        ligand_preparer = LigandPreparer(args.smiles, args.output_dir)
        ligand_pdbqt = ligand_preparer.prepare()
        
        # Step 3: Parse pocket
        print("Step 3/5: Parsing pocket configuration...")
        pocket_parser = PocketParser(args.pocket, args.protein, args.output_dir)
        pocket_config = pocket_parser.parse()
        print(f"Pocket configuration: {pocket_config}")
        
        # Step 4: Run docking
        print("Step 4/5: Running AutoDock VINA docking...")
        docking_runner = DockingRunner(protein_pdbqt, ligand_pdbqt, pocket_config, args.output_dir, args.num_modes, args.exhaustiveness)
        docking_result_pdbqt = docking_runner.run()
        
        # Step 5: Export results
        print("Step 5/5: Exporting docking results...")
        result_exporter = ResultExporter(args.protein, docking_result_pdbqt, args.output_dir, args.num_modes)
        complex_pdb, scores = result_exporter.export()
        
    except Exception as e:
        print(f"Error during docking: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
