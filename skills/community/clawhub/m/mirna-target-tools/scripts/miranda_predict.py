#!/usr/bin/env python3
"""
Run miRanda miRNA target prediction.
Usage: python miranda_predict.py --mirna mirna.fa --mrna 3utr_sequence.fa --output results.txt

Security/reliability notes:
  * miRanda is invoked with an argv list (never a shell)
  * the score flag is -sc (the old -score flag is not understood by miRanda)
  * pandas is imported lazily, so only --parse needs it
  * malformed output lines are skipped instead of crashing
"""

import argparse
import os
import shutil
import subprocess
import sys


def find_miranda():
    """PATH first, then common conda prefixes (base env may be inactive)."""
    found = shutil.which('miranda')
    if found:
        return found
    prefixes = []
    if os.environ.get('CONDA_PREFIX'):
        prefixes.append(os.environ['CONDA_PREFIX'])
    home = os.path.expanduser('~')
    prefixes.extend([os.path.join(home, p) for p in
                     ('anaconda3', 'miniconda3', 'mambaforge', 'micromamba')])
    prefixes.extend(['/opt/conda', '/opt/miniconda3'])
    for prefix in prefixes:
        candidate = os.path.join(prefix, 'bin', 'miranda')
        if os.path.isfile(candidate) and os.access(candidate, os.X_OK):
            return candidate
    return None


def run_miranda(mirna_file, mrna_file, output_file, energy_cutoff=-10, score_cutoff=50):
    """Run miRanda target prediction."""
    exe = find_miranda()
    if not exe:
        print("Error: 'miranda' was not found on PATH.")
        print("Install it (conda install -c bioconda miranda) or use predict_targets_genome.py.")
        return False

    cmd = [
        exe,
        mirna_file,
        mrna_file,
        '-en', str(energy_cutoff),
        '-sc', str(score_cutoff),
        '-out', output_file,
    ]

    out_dir = os.path.dirname(os.path.abspath(output_file))
    os.makedirs(out_dir, exist_ok=True)
    print("Running miRanda with command: %s" % ' '.join(cmd))
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print("Error running miRanda:\n%s" % result.stderr)
            return False
        print("miRanda complete. Results written to %s" % output_file)
        return True
    except OSError as exc:
        print("Exception running miRanda: %s" % exc)
        return False


def parse_miranda_output(input_file, output_file):
    """Parse miRanda text output into TSV format."""
    import pandas as pd

    results, current = [], {}
    with open(input_file, 'r', errors='replace') as f:
        for line in f:
            line = line.strip()
            if line.startswith('>') and not line.startswith('>>'):
                if current.get('mirna') and current.get('target'):
                    results.append(current)
                parts = line.lstrip('>').split()
                # miRanda header: query  target  score  energy  [coordinates]
                if len(parts) >= 4:
                    current = {'mirna': parts[0], 'target': parts[1],
                               'score': parts[2], 'energy': parts[3]}
                else:
                    current = {}
            elif line.startswith('Energy:') and current:
                try:
                    current['energy'] = float(line.split(':', 1)[1].split()[0])
                except (IndexError, ValueError):
                    pass
            elif line.startswith('Score:') and current:
                try:
                    current['score'] = float(line.split(':', 1)[1].split()[0])
                except (IndexError, ValueError):
                    pass

    if current.get('mirna') and current.get('target'):
        results.append(current)

    df = pd.DataFrame(results)
    df.to_csv(output_file, sep='\t', index=False)
    print("Parsed %d interactions saved to %s" % (len(results), output_file))
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

    for path in (args.mirna, args.mrna):
        if not os.path.isfile(path):
            print("Input file %s not found!" % path)
            sys.exit(1)

    if args.energy_cutoff > 0:
        parser.error('--energy-cutoff must be <= 0 kcal/mol')
    if args.score_cutoff < 0:
        parser.error('--score-cutoff must be >= 0')

    success = run_miranda(args.mirna, args.mrna, args.output,
                          args.energy_cutoff, args.score_cutoff)
    if not success:
        sys.exit(1)

    if args.parse:
        parse_miranda_output(args.output, args.output + '.tsv')

    print("Done!")


if __name__ == '__main__':
    main()
