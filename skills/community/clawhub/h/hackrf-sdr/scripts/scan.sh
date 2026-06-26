#!/usr/bin/env bash
# hackrf-sdr scan - Frequency sweep and signal detection
# Usage: scan.sh <start_mhz> <end_mhz> [options]
#   Options:
#     -l <dB>   LNA gain (default: 40)
#     -g <dB>   VGA gain (default: 40)
#     -w <Hz>   Bin width (default: 1000000)
#     -n <num>  Number of sweeps (default: 10)
#     -o <file> Output file (default: stdout)

set -euo pipefail

START=${1:?Usage: scan.sh <start_mhz> <end_mhz> [options]}
END=${2:?Missing end frequency}

LNA=40; VGA=40; BINW=1000000; NSWEEPS=10; OUTFILE=""

while getopts "l:g:w:n:o:" opt; do
  case $opt in
    l) LNA=$OPTARG ;;
    g) VGA=$OPTARG ;;
    w) BINW=$OPTARG ;;
    n) NSWEEPS=$OPTARG ;;
    o) OUTFILE=$OPTARG ;;
    *) echo "Unknown option"; exit 1 ;;
  esac
done

CMD="hackrf_sweep -f ${START}:${END} -l ${LNA} -g ${VGA} -w ${BINW} -N ${NSWEEPS}"

if [ -n "$OUTFILE" ]; then
  $CMD > "$OUTFILE"
else
  $CMD
fi