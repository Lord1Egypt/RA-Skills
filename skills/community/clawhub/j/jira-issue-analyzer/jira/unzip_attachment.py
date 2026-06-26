"""Unzip the Jira attachment."""

import zipfile
import os

zip_file = "c52056b2-b788-47a9-9390-bc94045457b4_app_log.zip"
extract_dir = "app_log"

if not os.path.exists(zip_file):
    print(f"Error: {zip_file} not found")
    exit(1)

print(f"Extracting {zip_file}...")

with zipfile.ZipFile(zip_file, 'r') as zf:
    # Create extract directory
    os.makedirs(extract_dir, exist_ok=True)

    # Extract all files
    zf.extractall(extract_dir)

    # List extracted files
    print(f"\nExtracted to: {extract_dir}/")
    print("Files:")
    for name in zf.namelist():
        filepath = os.path.join(extract_dir, name)
        if os.path.isfile(filepath):
            size = os.path.getsize(filepath)
            print(f"  - {name} ({size:,} bytes)")

print("\nDone!")
