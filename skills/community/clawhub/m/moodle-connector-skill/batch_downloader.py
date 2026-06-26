#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generic batch downloader for Moodle Connector.
Reads file lists from downloads.json and downloads them organized by module.

Usage:
    python batch_downloader.py                    # Uses downloads.json
    python batch_downloader.py --config my.json   # Custom config file
    python batch_downloader.py --output /path/to  # Custom output directory
"""

import sys
import io
import json
import argparse
from pathlib import Path

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

from moodle_connector import MoodleConnector


def load_config(config_path: Path) -> dict:
    """Load and validate downloads.json"""
    if not config_path.exists():
        raise FileNotFoundError(
            f"Config file not found: {config_path}\n"
            f"Copy downloads.example.json to downloads.json and customize it."
        )
    
    with config_path.open(encoding='utf-8') as f:
        return json.load(f)


def download_files(connector: MoodleConnector, config: dict, output_dir: Path):
    """Download files from config"""
    output_dir.mkdir(parents=True, exist_ok=True)
    
    total = 0
    downloaded = 0
    failed = 0
    
    for module in config.get('downloads', []):
        module_name = module.get('module', 'Unknown')
        module_dir = output_dir / module_name.replace(' ', '_')
        module_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"\n[Module] {module_name}")
        print("-" * 80)
        
        for file_info in module.get('files', []):
            total += 1
            filename = file_info.get('name', 'file')
            url = file_info.get('url')
            
            if not url:
                print(f"  ⚠️  Skipped: {filename} (no URL)")
                continue
            
            try:
                target_path = module_dir / filename
                print(f"  Downloading: {filename}...", end=' ')
                sys.stdout.flush()
                
                connector.api.download_file(url, target_path)
                size_mb = target_path.stat().st_size / (1024 * 1024)
                print(f"✅ ({size_mb:.1f} MB)")
                downloaded += 1
            except Exception as e:
                print(f"❌ Failed: {e}")
                failed += 1
    
    return total, downloaded, failed


def main():
    parser = argparse.ArgumentParser(
        description="Batch download files from Moodle using downloads.json"
    )
    parser.add_argument(
        '--config',
        type=Path,
        default=Path('downloads.json'),
        help='Path to downloads.json config (default: ./downloads.json)'
    )
    parser.add_argument(
        '--output',
        type=Path,
        default=Path('downloads'),
        help='Output directory (default: ./downloads)'
    )
    parser.add_argument(
        '--password',
        default='test-pass',
        help='Encryption password for credentials (default: test-pass)'
    )
    
    args = parser.parse_args()
    
    print("=" * 80)
    print("MOODLE CONNECTOR — Batch Downloader")
    print("=" * 80)
    
    try:
        # Load config
        config = load_config(args.config)
        print(f"\n✅ Loaded config: {args.config}")
        print(f"📁 Output directory: {args.output.resolve()}")
        
        # Get password from env var or args
        password = args.password or os.getenv('MOODLE_CRED_PASSWORD')
        if not password:
            # Prompt interactively if not provided
            import getpass
            password = getpass.getpass("Enter encryption password: ")
        
        # Initialize connector
        connector = MoodleConnector(
            config_path=Path('config.json'),
            password=password
        )
        print("✅ Connector initialized")
        
        # Download
        total, downloaded, failed = download_files(connector, config, args.output)
        
        print("\n" + "=" * 80)
        print(f"SUMMARY: {downloaded}/{total} files downloaded")
        if failed:
            print(f"⚠️  {failed} files failed")
        print(f"📁 Saved to: {args.output.resolve()}")
        print("=" * 80)
        
    except FileNotFoundError as e:
        print(f"ERROR: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
