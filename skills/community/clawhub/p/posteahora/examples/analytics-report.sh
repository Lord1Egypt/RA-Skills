#!/usr/bin/env bash
# Pull a 30-day cross-platform performance report as JSON.
set -euo pipefail

posteahora analytics --period 30d --json
