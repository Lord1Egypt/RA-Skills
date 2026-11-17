#!/usr/bin/env python3
"""
Run miRanda miRNA target prediction.
Usage: python miranda_predict.py --mirna mirna.fa --mrna 3utr_sequence.fa --output results.txt
"""

import argparse
import subprocess
import sys
import os
import pandas as pd

def run_miranda(mirna_file, mrna_file, output_file, energy_cutoff=-10, score_cutoff=50):
    """Run miRanda target prediction"""
    
    # miRanda command: miranda <mirna> <mrna> [options]
    cmd = [
        'miranda',
        mirna_file,
        mrna_file,
        '-en', str(energy_cutoff),
        '-score', str(score_cutoff),
        '-out', output_file
    ]
    
    print(f"Running miRanda with command: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Error running miRanda:\n{result.stderr}")
            return False
        
        print(f"miRanda complete. Results written to {output_file}")
        return True
    except Exception as e:
        print(f"Exception running miRanda: {e}")
        return False

def parse_miranda_output(input_file, output_file):
    """Parse miRanda text output into TSV format"""
    results = []
    current = {}
    
    with open(input_file, 'r') as f:
        for line in f:
            line = line.strip()
            if line.startswith('>>'):
                # New interaction
                if current and 'mirna' in current and 'target' in current:
                    results.append(current.copy())
                parts = line.split()
                current = {
                    'mirna': parts[1],
                    'target': parts[3]
                }
            elif line.startswith('Energy:'):
                energy = float(line.split(':')[1].split()[0])
                current['energy'] = energy
            elif line.startswith('Score:'):
                score = float(line.split(':')[1])
                current['score'] = score
    
    # Add last entry
    if current and 'mirna' in current and 'target' in current:
        results.append(current)
    
    df = pd.DataFrame(results)
    df.to_csv(output_file, sep='\t', index=False)
    print(f"Parsed {len(results)} interactions saved to {output_file}")
    return df

def main():
    parser = argparse.ArgumentParser(description='Run miRanda miRNA target prediction')
    parser.add_argument('--mirna', required=True, help='FASTA file with miRNA sequences')
    parser.add_argument('--mrna', required=True, help='FASTA file with 3\'UTR sequences')
    parser.add_argument('--output', required=True, help='Output file for results')
    parser.add_argument('--energy-cutoff', type=float, default=-10, 
                        help='Minimum free energy cutoff (default: -10 kcal/mol)')
    parser.add_argument('--score-cutoff', type=float, default=50,
                        help='Minimum score cutoff (default: 50)')
    parser.add_argument('--parse', action='store_true', help='Parse output to TSV format')
    
    args = parser.parse_args()
    
    # Check inputs
    for f in [args.mirna, args.mrna]:
        if not os.path.exists(f):
            print(f"Input file {f} not found!")
            sys.exit(1)
    
    # Run miRanda
    success = run_miranda(args.mirna, args.mrna, args.output, args.energy_cutoff, args.score_cutoff)
    if not success:
        sys.exit(1)
    
    # Parse if requested
    if args.parse:
        parsed_output = args.output + '.tsv'
        parse_miranda_output(args.output, parsed_output)
    
    print("Done!")

if __name__ == '__main__':
    main()
