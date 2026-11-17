#!/bin/sh
# PhD Research Companion - installation verification (thin wrapper)
#
# The real verifier is self_score.py, which is cross-platform. This shell
# wrapper exists only for convenience on POSIX systems; on Windows run:
#
#     python run.py score
#
set -e
DIR="$(cd "$(dirname "$0")" && pwd)"

if command -v python3 >/dev/null 2>&1; then
    PY=python3
else
    PY=python
fi

echo "phd-research-companion 2.3.0 - verification"
"$PY" "$DIR/run.py" score
