#!/usr/bin/env python3
"""
Run TargetScan miRNA target prediction.
Usage: python targetscan_predict.py --input mirna_list.txt --output results.txt --database path/to/targetscan_db

Security/reliability notes:
  * the external tool is invoked with an argv list (never a shell)
  * the binary is resolved via PATH and reported clearly when missing
  * parsing skips malformed lines instead of crashing, and pandas is imported
    lazily so the prediction step works without it
"""

import argparse
import os
import shutil
import subprocess
import sys


def run_targetscan(input_file, output_file, database_path, species='human'):
    """Run TargetScan prediction."""
    exe = shutil.which('targetscan')
    if not exe:
        print("Error: 'targetscan' was not found on PATH.")
        print("Install TargetScan or run the prediction with predict_targets_genome.py instead.")
        return False

    # Build command - TargetScan is typically run with Perl scripts
    cmd = [
        exe,
        '--mirna', input_file,
        '--output', output_file,
        '--species', species
    ]
    if database_path:
        cmd.extend(['--db', database_path])

    out_dir = os.path.dirname(os.path.abspath(output_file))
    os.makedirs(out_dir, exist_ok=True)

    print("Running TargetScan with command: %s" % ' '.join(cmd))
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print("Error running TargetScan:\n%s" % result.stderr)
            return False
        print("TargetScan complete. Results written to %s" % output_file)
        return True
    except OSError as exc:
        print("Exception running TargetScan: %s" % exc)
        return False


def parse_results(input_file, output_file):
    """Parse TargetScan results into a cleaner format."""
    import pandas as pd

    results, skipped = [], 0
    with open(input_file, 'r', errors='replace') as f:
        for line in f:
            if line.startswith('#') or not line.strip():
                continue
            fields = line.strip().split()
            if len(fields) < 5:
                skipped += 1
                continue
            try:
                results.append({
                    'mirna': fields[0],
                    'target_gene': fields[1],
                    'context_score': float(fields[2]),
                    'conservation': float(fields[3]),
                    'site_type': fields[4],
                })
            except ValueError:
                skipped += 1

    if skipped:
        print("Skipped %d malformed line(s)." % skipped)
    df = pd.DataFrame(results, columns=['mirna', 'target_gene', 'context_score',
                                        'conservation', 'site_type'])
    df.to_csv(output_file, sep='\t', index=False)
    print("Parsed results saved to %s" % output_file)
    return df


def main():
    parser = argparse.ArgumentParser(description='Run TargetScan miRNA target prediction')
    parser.add_argument('--input', required=True, help='Input miRNA list or FASTA file')
    parser.add_argument('--output', required=True, help='Output file for results')
    parser.add_argument('--database', help='Path to TargetScan database directory')
    parser.add_argument('--species', default='human', help='Species (default: human)')
    parser.add_argument('--parse', action='store_true', help='Parse output to TSV format')
    args = parser.parse_args()

    if not os.path.isfile(args.input):
        print("Input file %s not found!" % args.input)
        sys.exit(1)

    success = run_targetscan(args.input, args.output, args.database, args.species)
    if not success:
        sys.exit(1)

    if args.parse:
        parse_results(args.output, args.output + '.tsv')

    print("Done!")


if __name__ == '__main__':
    main()
