#!/bin/bash
# Run Sunday scan: stock scanner + FIRE pipeline
# Runs at 9:50 AM CDT Sunday (before catalyst-edge-weekly at 10 AM)
# Output: fresh scan → last_scan.json → fire_pipeline.py → Discord #retirement-edge

cd /workspace/skills/catalyst-edge/stock_scanner
python3 scan_once.py --quiet 2>&1 | tail -3

cd /workspace/skills/catalyst-edge
python3 fire_pipeline.py --dry-run 2>&1 | tail -5

echo "Sunday scan complete at $(date)"
