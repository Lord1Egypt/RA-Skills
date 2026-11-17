#!/usr/bin/env python3
# get_swatch_time.py
# Single-file example that prints the current Swatch Internet Time to stdout
# Canonical definition: Biel = UTC+1 (fixed), no DST. One beat = 86.4 seconds.

from datetime import datetime, timezone, timedelta
import sys

def get_swatch_time(dt=None):
    # Use provided datetime or current UTC time
    if dt is None:
        now = datetime.now(timezone.utc)
    else:
        # Accept naive or aware datetimes; normalize to UTC
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        now = dt.astimezone(timezone.utc)

    utc_seconds = now.hour * 3600 + now.minute * 60 + now.second
    biel_seconds = (utc_seconds + 3600) % 86400
    beat = int(biel_seconds // 86.4) % 1000
    return f"@{beat:03d}"

# Centibeat helper (safe rounding + wrap):
# raw = biel_seconds / 86.4
# rounded = round(raw * 100) / 100
# if rounded >= 1000:
#     rounded -= 1000
# display = f"{rounded:.2f}"

if __name__ == '__main__':
    # Optional: allow passing an ISO timestamp as first arg
    if len(sys.argv) > 1:
        t = datetime.fromisoformat(sys.argv[1].replace('Z', '+00:00'))
        print(get_swatch_time(t))
    else:
        print(get_swatch_time())

# Examples:
# python3 get_swatch_time.py                 # prints current beat
# python3 get_swatch_time.py 2025-01-01T00:00:00Z  # -> @041