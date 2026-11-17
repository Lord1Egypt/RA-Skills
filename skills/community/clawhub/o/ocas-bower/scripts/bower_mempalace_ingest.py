#!/usr/bin/env python3
"""
Bower to MemPalace ingestion pipeline.
Runs the ingestion script for Bower data.
"""
import subprocess
import sys
import os

_HELP_ARGS = {"--help", "-h"}
if set(sys.argv[1:]) & _HELP_ARGS:
    print((__doc__ or "").strip() or "Usage: python3 bower_mempalace_ingest.py [no flags]")
    sys.exit(0)

def main():
    # Run the Bower to MemPalace ingestion
    ingest_script = os.path.expanduser("~/.hermes/commons/data/ocas-bower/bower_full_scan.py")
    
    if not os.path.exists(ingest_script):
        print(f"ERROR: Ingest script not found: {ingest_script}")
        return False
    
    result = subprocess.run(
        ["python3", ingest_script],
        capture_output=True, text=True,
        cwd=os.path.expanduser("~/.hermes/commons/data/ocas-bower")
    )
    
    if result.returncode == 0:
        print("Bower-MemPalace ingestion completed successfully")
        if result.stdout.strip():
            print(result.stdout.strip())
        return True
    else:
        print(f"ERROR: Ingestion failed")
        if result.stderr.strip():
            print(result.stderr.strip())
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
