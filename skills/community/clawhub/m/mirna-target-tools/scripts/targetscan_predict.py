#!/usr/bin/env python3
"""
Run TargetScan miRNA target prediction.
Usage: python targetscan_predict.py --input mirna_list.txt --output results.txt --database path/to/targetscan_db
"""

import argparse
import subprocess
import sys
import os

def run_targetscan(input_file, output_file, database_path, species='human'):
    """Run TargetScan prediction"""
    
    # Build command - TargetScan is typically run with Perl scripts
    # This assumes targetscan is properly installed and in PATH
    cmd = [
        'targetscan',
        '--mirna', input_file,
        '--output', output_file,
        '--species', species
    ]
    
    if database_path:
        cmd.extend(['--db', database_path])
    
    print(f"Running TargetScan with command: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Error running TargetScan:\n{result.stderr}")
            return False
        
        print(f"TargetScan complete. Results written to {output_file}")
        return True
    except Exception as e:
        print(f"Exception running TargetScan: {e}")
        return False

def parse_results(input_file, output_file):
    """Parse TargetScan results into a cleaner format"""
    # Implementation depends on TargetScan output format
    # This is a placeholder for the standard parsing
    import pandas as pd
    
    results = []
    with open(input_file, 'r') as f:
        for line in f:
            if line.startswith('#') or line.strip() == '':
                continue
            fields = line.strip().split()
            if len(fields) >= 5:
                results.append({
                    'mirna': fields[0],
                    'target_gene': fields[1],
                    'context_score': float(fields[2]),
                    'conservation': float(fields[3]),
                    'site_type': fields[4]
                })
    
    df = pd.DataFrame(results)
    df.to_csv(output_file, sep='\t', index=False)
    print(f"Parsed results saved to {output_file}")
    return df

def main():
    parser = argparse.ArgumentParser(description='Run TargetScan miRNA target prediction')
    parser.add_argument('--input', required=True, help='Input miRNA list or FASTA file')
    parser.add_argument('--output', required=True, help='Output file for results')
    parser.add_argument('--database', help='Path to TargetScan database directory')
    parser.add_argument('--species', default='human', help='Species (default: human)')
    parser.add_argument('--parse', action='store_true', help='Parse output to TSV format')
    
    args = parser.parse_args()
    
    # Check input exists
    if not os.path.exists(args.input):
        print(f"Input file {args.input} not found!")
        sys.exit(1)
    
    # Run TargetScan
    success = run_targetscan(args.input, args.output, args.database, args.species)
    if not success:
        sys.exit(1)
    
    # Parse if requested
    if args.parse and args.output != args.output + '.tsv':
        parse_results(args.output, args.output + '.tsv')
    
    print("Done!")

if __name__ == '__main__':
    main()
