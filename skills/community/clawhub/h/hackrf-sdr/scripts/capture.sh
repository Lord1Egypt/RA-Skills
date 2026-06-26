#!/usr/bin/env bash
# hackrf-sdr capture - Record IQ samples
# Usage: capture.sh <freq_hz> [options]
#   Options:
#     -s <Hz>      Sample rate (default: 10000000)
#     -l <dB>      LNA gain (default: 40)
#     -g <dB>      VGA gain (default: 40)
#     -t <sec>     Duration in seconds (default: 5)
#     -o <file>    Output file (default: /tmp/iq_capture.raw)
#     -a <antenna>  Antenna port: enable or disable (default: enable)

set -euo pipefail

FREQ=${1:?Usage: capture.sh <freq_hz> [options]}
RATE=10000000; LNA=40; VGA=40; DURATION=5; OUTFILE="/tmp/iq_capture.raw"; ANT="enable"

while getopts "s:l:g:t:o:a:" opt; do
  case $opt in
    s) RATE=$OPTARG ;;
    l) LNA=$OPTARG ;;
    g) VGA=$OPTARG ;;
    t) DURATION=$OPTARG ;;
    o) OUTFILE=$OPTARG ;;
    a) ANT=$OPTARG ;;
    *) echo "Unknown option"; exit 1 ;;
  esac
done

NUM_SAMPLES=$(( RATE * DURATION ))

echo "Capturing IQ: ${FREQ} Hz, ${RATE} SPS, ${DURATION}s (${NUM_SAMPLES} samples)"
echo "Output: ${OUTFILE}"

hackrf_transfer -f "${FREQ}" -s "${RATE}" -l "${LNA}" -g "${VGA}" -n "${NUM_SAMPLES}" -r "${OUTFILE}" -a "${ANT}"

FILESIZE=$(stat -c%s "${OUTFILE}" 2>/dev/null || echo "?")
echo "Capture complete: ${FILESIZE} bytes"