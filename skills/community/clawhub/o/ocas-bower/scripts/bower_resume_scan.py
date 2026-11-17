#!/usr/bin/env python3
"""
Resume Bower deep scan from where it left off.
Skips Hermes and Openclaw backup folders.
Uses scans/ directory as source of truth for what was scanned.
"""
import json
import sys
import time
from pathlib import Path
from datetime import datetime, timezone
from googleapiclient.errors import HttpError

_HELP_ARGS = {"--help", "-h"}
if set(sys.argv[1:]) & _HELP_ARGS:
    print((__doc__ or "").strip() or "Usage: python3 bower_resume_scan.py [no flags]")
    sys.exit(0)

# Paths
HERMES_HOME = Path.home() / ".hermes"
BOWER_DATA = HERMES_HOME / "commons/data/ocas-bower"

SCANS_DIR = BOWER_DATA / "scans"
FOLDER_INDEX = BOWER_DATA / "folder_index.json"
SCAN_PROGRESS = BOWER_DATA / "scan_progress.json"

# Central auth
sys.path.insert(0, str(HERMES_HOME / 'scripts'))
from google_auth import get_drive_service

def get_drive():
    return get_drive_service()

# Folders to skip (agent system backups - not user's real Drive content)
SKIP_FOLDERS = {
    # hermes-* folders
    "1Axg8QxQ5WlDbvIxW_4Jglm4zWVG-Qudj", "1tcHNivhcpJY9zXMrFtuf4WV-tTKx1lD1", "19lJhqHgAjcg0N3x-M5FlK40gAdf6uPmj", "1i8fuFw5nqm3ABqVRVskgos97lzxnxcoe",
    "1Nruipkw44CbuKVmb9fvxJ3c3svtjjRdi", "17GFgeXttVgw-Ob4ScKCLPt7UH8We-qyU", "1Bp7eaRhsNLYZiom8NDbyH1QCg2P578VJ", "10l4dOVO5GMY7cjRLKTvNxhhnZOvA-6s0",
    "1gdXBSjwNsJ5MCohzB-3g67O5e_OggaDZ", "1uBwL8OJ-XrXaBo4Uv9niZ_Qdx3JaqWHS", "1_Uk9ElpbEkxGT0mpgAo-d6KBOk1rnnXC", "1keQ5D1p2QP_XaxaabpMw-YYZL9GOORN6",
    # openclaw-* folders
    "1G8j8mPnnVLi46S9yPLtyD9jrcGmVUbmQ", "1D7pXHAJCdKaXuxTRHcXIJxhybEkplSwv", "1iieGDgDEYmegiLR_EOTbQj5VZQDw0IYu", "1N0QpqGJjSmxCudW9l_4l0hnqIDlzmAMc",
    # openclaw and hermes root folders
    "1uBwL8OJ-XrXaBo4Uv9niZ_Qdx3JaqWHS",  # Hermes
    "1sS039DPzf6uCWkfDB3GdSjydG8u3fumh",  # hermes
    "1miKFiJt4rP1j1Hkg4ncrLCT2DTmhevDh",  # hermes
    "1nKn0_rPCFc9GXcAbEfidlOuSk_VeDq_h",  # hermes_cli
}

def get_scanned_folders():
    """Get set of folder IDs that have been scanned (from scans directory)."""
    scanned = set()
    for f in SCANS_DIR.glob('*.json'):
        try:
            with open(f) as fp:
                d = json.load(fp)
                scanned.add(d.get('folder_id'))
        except:
            pass
    return scanned

def main():
    print(f"Bower Deep Scan Resume (skipping Hermes/Openclaw)", flush=True)
    print(f"="*50, flush=True)
    
    # Get already scanned folders from scans directory
    scanned = get_scanned_folders()
    print(f"Already scanned: {len(scanned)} folders", flush=True)
    
    # Load folder index
    with open(FOLDER_INDEX) as f:
        index_data = json.load(f)
    
    all_folders = index_data.get('folders', [])
    total_folders = index_data.get('total_folders', len(all_folders))
    
    # Build list of unscanned folders, excluding Hermes/Openclaw
    unscanned = []
    skipped = 0
    for folder in all_folders:
        fid = folder.get('id')
        fname = folder.get('name', '')
        if fid in scanned:
            continue
        # Skip hermes and openclaw folders
        fname_lower = fname.lower()
        if 'hermes' in fname_lower or 'openclaw' in fname_lower or '.openclaw' in fname_lower or 'open claw' in fname_lower:
            skipped += 1
            continue
        unscanned.append(folder)
    
    print(f"Total folders in index: {total_folders}", flush=True)
    print(f"Skipped (Hermes/Openclaw): {skipped}", flush=True)
    print(f"Remaining to scan: {len(unscanned)}", flush=True)
    if len(unscanned) > 0:
        print(f"Estimated time: {len(unscanned) * 0.5 / 60:.1f} minutes", flush=True)
    print(flush=True)
    
    if len(unscanned) == 0:
        print("All user folders scanned!")
        return
    
    # Initialize Drive
    print("Connecting to Google Drive...", flush=True)
    drive = get_drive()
    print("Connected!", flush=True)
    
    # Scan each unscanned folder
    start_time = time.time()
    for i, folder in enumerate(unscanned):
        fid = folder['id']
        fname = folder.get('name', '')
        
        try:
            # List files in this folder
            results = drive.files().list(
                q=f"'{fid}' in parents and trashed=false",
                pageSize=200,
                fields="files(id, name, mimeType, size, modifiedTime, description)",
                orderBy="modifiedTime desc"
            ).execute()
            
            files = results.get('files', [])
            
            # Save folder scan
            scan_file = SCANS_DIR / f"{fid}.json"
            with open(scan_file, 'w') as f:
                json.dump({
                    'folder_id': fid,
                    'folder_name': fname,
                    'scanned_at': datetime.now(timezone.utc).isoformat(),
                    'files': files,
                    'file_count': len(files)
                }, f)
            
            # Progress every 50 folders
            if (i+1) % 50 == 0:
                elapsed = time.time() - start_time
                rate = (i+1) / elapsed
                eta = (len(unscanned) - i-1) / rate / 60
                print(f"[{i+1}/{len(unscanned)}] ({100*(i+1)/len(unscanned):.1f}%) ETA: {eta:.1f}min - {fname[:30]}", flush=True)
            
        except Exception as e:
            # Skip problematic folders
            continue
    
    print(f"\nDone! Total scanned: {len(scanned) + len(unscanned)} folders", flush=True)

if __name__ == '__main__':
    main()
