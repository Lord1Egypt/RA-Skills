#!/usr/bin/env python3
"""
Polymarket Brain - FIXED VERSION
AI-Powered Full Workflow
"""

import subprocess
import sys
import os
from pathlib import Path

def run_phase_1():
    """Run CNBC Geopolitics Fetcher"""
    print("\n" + "="*60)
    print("PHASE 1: CNBC Geopolitics News Fetch")
    print("="*60)
    
    script_path = r"C:\Users\Legion 5i Pro\.browseros\skills\cnbc-geopolitics-fetcher\scripts\fetch_cnbc_geopolitics.py"
    
    result = subprocess.run(
        [
            "python", script_path,
            "--count", "5",
            "--json-output", r"C:\Users\Legion 5i Pro\.browseros\skills\polymarket-brain\output\latest_articles.json",
            "--config", r"C:\Users\Legion 5i Pro\.browseros\skills\cnbc-geopolitics-fetcher\config\config.json"
        ],
        capture_output=True,
        text=True
    )
    
    print(result.stdout)
    if result.stderr:
        print(f"Errors: {result.stderr}")
    
    return result.returncode == 0

def run_phase_2_3():
    """Run AI Analysis (Phases 2 & 3)"""
    print("\n" + "="*60)
    print("PHASE 2-3: AI Expert Analysis + Market Matching")
    print("="*60)
    
    script_path = r"C:\Users\Legion 5i Pro\.browseros\skills\polymarket-brain\ai_analyzer.py"
    
    result = subprocess.run(
        ["python", script_path],
        capture_output=True,
        text=True
    )
    
    print(result.stdout)
    if result.stderr:
        print(f"Errors: {result.stderr}")
    
    return result.returncode == 0

def run_phase_4():
    """Send to Discord"""
    print("\n" + "="*60)
    print("PHASE 4: Discord Dispatch")
    print("="*60)
    
    script_path = r"C:\Users\Legion 5i Pro\.browseros\skills\polymarket-brain\send_discord.py"
    
    result = subprocess.run(
        ["python", script_path],
        capture_output=True,
        text=True
    )
    
    print(result.stdout)
    if result.stderr:
        print(f"Errors: {result.stderr}")
    
    return result.returncode == 0

def main():
    """Run full orchestrated workflow"""
    print("\n" + "="*60)
    print("POLYMARKET BRAIN - AI-POWERED WORKFLOW")
    print("="*60)
    
    success = True
    
    # Phase 1: CNBC Fetch
    if not run_phase_1():
        print("\n[X] Phase 1 FAILED")
        success = False
    else:
        print("\n[OK] Phase 1 COMPLETE")
    
    # Phase 2-3: AI Analysis
    if not run_phase_2_3():
        print("\n[X] Phase 2-3 FAILED")
        success = False
    else:
        print("\n[OK] Phase 2-3 COMPLETE")
    
    # Phase 4: Discord
    if not run_phase_4():
        print("\n[X] Phase 4 FAILED")
        success = False
    else:
        print("\n[OK] Phase 4 COMPLETE")
    
    print("\n" + "="*60)
    if success:
        print("ALL PHASES COMPLETE")
    else:
        print("WORKFLOW COMPLETED WITH ERRORS")
    print("="*60)
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
