#!/usr/bin/env python3
"""
bower.scan.deep -- Founding scan in batches.

Scans Google Drive in small batches, writes structural model incrementally,
and produces the foundation preference profile.

Usage: python3 bower_scan_deep.py [--batch-size N] [--dry-run]
"""

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import json
import os
import sys
import time
import hashlib
from pathlib import Path
from datetime import datetime, timezone

_HELP_ARGS = {"--help", "-h"}
if set(sys.argv[1:]) & _HELP_ARGS:
    print((__doc__ or "").strip() or "Usage: python3 bower_full_scan.py [no flags]")
    sys.exit(0)

# Google OAuth credentials — use the central google_auth helper or direct API access
CREDS_DIR = Path.home() / '.hermes' / 'credentials'
TOKEN_PATH = CREDS_DIR / 'google-workspace-user.json'
BOWER_DATA = Path.home() / ".hermes" / "commons/data" / "ocas-bower"
JOURNALS_DIR = Path.home() / ".hermes" / "commons/journals" / "ocas-bower"

# Ensure directories
BOWER_DATA.mkdir(parents=True, exist_ok=True)
(BOWER_DATA / "reports").mkdir(exist_ok=True)
(BOWER_DATA / "staging").mkdir(exist_ok=True)
JOURNALS_DIR.mkdir(parents=True, exist_ok=True)

CONFIG_PATH = BOWER_DATA / "config.json"
STRUCTURAL_MODEL_PATH = BOWER_DATA / "structural_model.json"
PREFERENCE_PROFILE_PATH = BOWER_DATA / "preference_profile.json"
SCAN_EVENTS_PATH = BOWER_DATA / "scan_events.jsonl"
CHECKPOINT_PATH = BOWER_DATA / "staging" / "scan_checkpoint.json"

# Batch size - can be overridden via CLI
BATCH_SIZE = 50

# Max file size to read content (5MB)
CONTENT_READ_MAX_BYTES = 5 * 1024 * 1024

# Google Doc mime types we can export
GOOGLE_DOC_TYPES = {
    'application/vnd.google-apps.document',
    'application/vnd.google-apps.spreadsheet',
    'application/vnd.google-apps.presentation',
}

# Content types we can attempt to read
READABLE_MIME_TYPES = set(GOOGLE_DOC_TYPES) | {
    'text/plain', 'text/html', 'text/csv', 'text/x-python',
    'text/x-sh', 'text/x-script.python', 'text/x-markdown',
    'application/pdf', 'application/json', 'application/xml',
}


def get_drive_service():
    creds = Credentials.from_authorized_user_file(str(TOKEN_PATH))
    return build('drive', 'v3', credentials=creds)


def list_all_file_ids(drive, batch_size=50):
    """Paginate through ALL files, return list of (id, name, mimeType, parents, ...) dicts."""
    all_files = []
    page_token = None
    fields = "nextPageToken, files(id, name, mimeType, parents, modifiedTime, starred, size, description, trashed)"

    while True:
        try:
            results = drive.files().list(
                pageSize=batch_size,
                orderBy='folder, modifiedTime',  # folders first
                fields=fields,
                pageToken=page_token,
                q="trashed=false"
            ).execute()
        except HttpError as e:
            print(f"  ERROR listing files: {e}")
            break

        files = results.get('files', [])
        all_files.extend(files)
        page_token = results.get('nextPageToken')

        if page_token:
            sys.stdout.write(f"\r  Fetching file list... {len(all_files)} files retrieved")
            sys.stdout.flush()
        else:
            sys.stdout.write(f"\r  Fetching file list... {len(all_files)} files retrieved - DONE\n")
            sys.stdout.flush()
            break

    return all_files


def build_parent_map(all_files):
    """Build a map of folder_id -> folder info for path reconstruction."""
    folders = {}
    for f in all_files:
        if 'folder' in f.get('mimeType', ''):
            folders[f['id']] = {
                'name': f['name'],
                'id': f['id'],
                'parents': f.get('parents', []),
            }
    return folders


def resolve_path(file, folder_map):
    """Resolve full path for a file given folder map."""
    parents = file.get('parents', [])
    if not parents:
        return file['name'], 1

    parts = [file['name']]
    current = parents[0] if parents else None
    depth = 1

    while current and current in folder_map:
        folder = folder_map[current]
        parts.append(folder['name'])
        depth += 1
        current = folder['parents'][0] if folder.get('parents') else None

    path = '/'.join(reversed(parts))
    return path, depth


def read_content_summary(drive, file_info):
    """Get a brief content summary for a file."""
    mime = file_info.get('mimeType', '')
    name = file_info.get('name', '')
    file_id = file_info.get('id', '')
    size = file_info.get('size', '0')

    # Skip large files
    try:
        if int(size) > CONTENT_READ_MAX_BYTES:
            return None, False
    except (ValueError, TypeError):
        pass

    # Skip non-readable types
    if not any(rt in mime for rt in READABLE_MIME_TYPES) and not any(rt in mime for rt in GOOGLE_DOC_TYPES):
        return None, False

    try:
        if mime == 'application/vnd.google-apps.document':
            content = drive.files().export(
                fileId=file_id, mimeType='text/plain'
            ).execute()
        elif mime == 'application/vnd.google-apps.spreadsheet':
            content = drive.files().export(
                fileId=file_id, mimeType='text/csv'
            ).execute()
        elif mime == 'application/vnd.google-apps.presentation':
            content = drive.files().export(
                fileId=file_id, mimeType='text/plain'
            ).execute()
        else:
            # For PDFs and other files, try download
            content = drive.files().get_media(fileId=file_id).execute()
            if isinstance(content, bytes):
                # Try to decode, skip binary
                try:
                    content = content.decode('utf-8', errors='ignore')[:10000]
                except Exception:
                    return None, False

        if isinstance(content, (bytes, bytearray)):
            content = content.decode('utf-8', errors='ignore')[:10000]

        if not content:
            return None, True

        # First 2000 chars as summary
        summary = content[:2000]
        return summary, True

    except HttpError:
        return None, True  # tried but failed
    except Exception:
        return None, True


def detect_content_type(name, content_summary):
    """Heuristic content classification."""
    name_lower = name.lower() if name else ''
    content_lower = (content_summary or '').lower()[:1000]
    combined = f"{name_lower} {content_lower}"

    types_found = []

    # Tax documents
    if any(k in combined for k in ['w2', 'w-2', '1099', 'tax return', 'irs', 'schedule k', '1040', 'tax form']):
        types_found.append('tax')

    # Financial
    if any(k in combined for k in ['statement', 'balance', 'account', 'bank', 'brokerage', 'transaction', 'deposit']):
        types_found.append('finance')

    # Legal
    if any(k in combined for k in ['contract', 'agreement', 'nda', 'lease', 'deed', 'terms of service']):
        types_found.append('legal')

    # Medical
    if any(k in combined for k in ['eob', 'explanation of benefits', 'lab result', 'prescription', 'medical', 'doctor', 'hospital']):
        types_found.append('medical')

    # Home
    if any(k in combined for k in ['mortgage', 'home insurance', 'warranty', 'appliance', 'hvac', 'plumbing', 'roofing']):
        types_found.append('home')

    # Education
    if any(k in combined for k in ['lecture', 'course', 'assignment', 'syllabus', 'exam', 'grade']):
        types_found.append('education')

    # Project
    if any(k in combined for k in ['deliverable', 'specification', 'requirements', 'milestone', 'sprint', 'standup']):
        types_found.append('project')

    return types_found


def generate_description(name, content_summary, types_found, path):
    """Generate a 50-120 word description for a file."""
    if not content_summary:
        return None

    # Simple description: file type + topic + key terms
    name_ext = Path(name).suffix.replace('.', '') if name else ''
    first_lines = content_summary.split('\n')[:5]
    text = ' '.join(first_lines)[:500]

    # Try to identify what kind of document this is
    doc_type = 'Document'
    if 'spreadsheet' in name.lower() or 'csv' in name.lower() or 'sheet' in name.lower():
        doc_type = 'Spreadsheet'
    elif 'presentation' in name.lower() or 'slide' in name.lower() or 'deck' in name.lower():
        doc_type = 'Presentation'
    elif any(ext in name.lower() for ext in ['pdf', 'doc', 'docx']):
        doc_type = 'Document'

    description = f"{doc_type}"
    if types_found:
        description += f" related to {', '.join(types_found)}"
    description += f". Contains: {text[:200]}"
    return description.strip()[:500]


def is_folder(file):
    return 'folder' in file.get('mimeType', '')


def main():
    global BATCH_SIZE

    # Parse CLI
    dry_run = False
    for arg in sys.argv[1:]:
        if arg.startswith('--batch-size='):
            BATCH_SIZE = int(arg.split('=')[1])
        elif arg == '--batch-size':
            idx = sys.argv.index('--batch-size')
            if idx + 1 < len(sys.argv):
                BATCH_SIZE = int(sys.argv[idx + 1])
        elif arg == '--dry-run':
            dry_run = True
        elif arg == '--founding':
            pass  # handled

    print(f"Bower founding scan (batch_size={BATCH_SIZE}, dry_run={dry_run})")

    # Initialize config if not exists
    if not CONFIG_PATH.exists():
        config = {
            "skill_id": "hermes-bower",
            "skill_version": "1.0.0",
            "config_version": "2",
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat(),
            "drive_root": "root",
            "scan_schedule_light": "0 2 * * *",
            "scan_schedule_deep": "0 1 * * 0",
            "timezone": "America/Los_Angeles",
            "auto_approve_tiers": [],
            "forbidden_parent_ids": [],
            "proposal_expiry_days": 14,
            "apply_cap": 25,
            "describe_auto_cap": 50,
            "drift_abort_threshold": 0.15,
            "content_read_max_mb": 5,
            "quiet_mode": False,
            "founding_run_complete": False,
            "arrival_detection_enabled": True,
            "health_score_history_weeks": 8,
            "retention": {"days": 365, "max_records": 10000}
        }
        CONFIG_PATH.write_text(json.dumps(config, indent=2))
        print("  Created default config.json")

    # Connect to Drive
    print("  Connecting to Google Drive...")
    drive = get_drive_service()

    # Step 1: Get all file listings
    print("  Step 1: Enumerating all files and folders...")
    all_files = list_all_file_ids(drive, batch_size=BATCH_SIZE)

    if not all_files:
        print("  No files found. Aborting.")
        sys.exit(1)

    print(f"  Total: {len(all_files)} files/folders")

    # Step 2: Build parent map and folder info
    print("  Step 2: Building folder index...")
    folder_map = build_parent_map(all_files)
    print(f"  {len(folder_map)} folders found")

    # Step 3: Process files with content reading in small batches
    print(f"  Step 3: Processing files with content reading (batch_size={BATCH_SIZE})...")

    files_data = []
    scan_id = f"scan_{hashlib.md5(str(time.time()).encode()).hexdigest()[:12]}"
    started_at = datetime.now(timezone.utc).isoformat()
    content_read_count = 0
    content_skip_count = 0
    description_proposed_count = 0

    for i, file_info in enumerate(all_files):
        fid = file_info.get('id', '')
        fname = file_info.get('name', '')
        mime = file_info.get('mimeType', '')

        file_path, depth = resolve_path(file_info, folder_map)

        read_content_summary_val = None
        content_read = False

        # Only read content for Google Docs and text files (skip PDFs in batch for speed)
        if mime in GOOGLE_DOC_TYPES:
            read_content_summary_val, content_read = read_content_summary(drive, file_info)
            if content_read:
                content_read_count += 1
            else:
                content_skip_count += 1
        else:
            content_skip_count += 1

        types_found = detect_content_type(fname, read_content_summary_val)
        desc = generate_description(fname, read_content_summary_val, types_found, file_path)
        if desc:
            description_proposed_count += 1

        record = {
            "id": fid,
            "name": fname,
            "mimeType": mime,
            "parent_id": file_info.get('parents', [''])[0] if file_info.get('parents') else None,
            "parent_path": '/'.join(file_path.split('/')[:-1]) if '/' in file_path else '',
            "depth": depth,
            "modifiedTime": file_info.get('modifiedTime', ''),
            "starred": file_info.get('starred', False),
            "size": file_info.get('size'),
            "is_folder": is_folder(file_info),
            "content_summary": (read_content_summary_val or '')[:3000] if read_content_summary_val else None,
            "content_read": content_read,
            "existing_description": file_info.get('description') or None,
            "proposed_description": desc,
        }

        files_data.append(record)

        if (i + 1) % BATCH_SIZE == 0:
            # Save intermediate checkpoint
            model = {
                "scan_id": scan_id,
                "scan_type": "deep",
                "scanned_at": started_at,
                "file_count": len([f for f in files_data if not f['is_folder']]),
                "folder_count": len([f for f in files_data if f['is_folder']]),
                "root_folders": [],
                "taxonomy": {"labels": [], "depth_distribution": {}},
                "folder_index": {},
                "files": files_data
            }
            STRUCTURAL_MODEL_PATH.write_text(json.dumps(model, indent=2))
            sys.stdout.write(f"  Processed {i + 1}/{len(all_files)} - written to structural_model.json\r")
            sys.stdout.flush()

    print(f"  Processed {len(files_data)}/{len(all_files)} files - DONE")

    # Step 4: Build folder_index and root_folders
    print("  Step 4: Building folder index...")
    folder_index = {}
    root_folders = []

    for f in files_data:
        if f['is_folder']:
            folder_index[f['id']] = {
                "name": f['name'],
                "path": f['parent_path'],
                "depth": f['depth'],
                "effective_permissions": [],  # Would need separate API calls - skip for now
            }
            if f['depth'] == 1:
                root_folders.append(f['id'])

    # Depth distribution
    depth_dist = {"1": 0, "2": 0, "3": 0, "4+": 0}
    for f in files_data:
        d = f['depth']
        if d <= 3:
            depth_dist[str(d)] += 1
        else:
            depth_dist["4+"] += 1

    # Taxonomy - infer from folder names
    folder_names = [f['name'] for f in files_data if f['is_folder']]
    taxonomy_labels = list(set(folder_names))[:50]  # top 50 unique folder names

    # Step 5: Build the final structural model
    print("  Step 5: Writing final structural model...")
    non_folder_count = len([f for f in files_data if not f['is_folder']])
    folder_count = len([f for f in files_data if f['is_folder']])

    model = {
        "scan_id": scan_id,
        "scan_type": "deep",
        "scanned_at": started_at,
        "file_count": non_folder_count,
        "folder_count": folder_count,
        "root_folders": root_folders,
        "taxonomy": {
            "labels": taxonomy_labels,
            "depth_distribution": depth_dist
        },
        "folder_index": folder_index,
        "files": files_data,
    }

    if not dry_run:
        STRUCTURAL_MODEL_PATH.write_text(json.dumps(model, indent=2))
        print(f"  Written structural_model.json ({STRUCTURAL_MODEL_PATH.stat().st_size / 1024 / 1024:.1f} MB)")

    # Step 6: Build preference profile
    print("  Step 6: Building preference profile...")

    # Detect domains by checking root folder names
    domain_vocab = {
        'taxes': ['tax', 'taxes', 'irs', 'w2', 'w-2', '1099'],
        'projects': ['projects', 'project', 'clients', 'client work', 'engagements'],
        'home': ['home', 'house', 'apartment', 'property', 'household'],
        'finance': ['finance', 'financial', 'banking', 'bank', 'investments', 'brokerage'],
        'legal': ['legal', 'contracts', 'agreements', 'law', 'attorney'],
        'medical': ['medical', 'health', 'eob', 'records', 'hospital'],
        'archive': ['archive', 'archived', 'reference', 'old'],
        'education': ['school', 'university', 'college', 'course', 'class', 'education'],
    }

    root_folder_names = [f['name'].lower() for f in files_data if f['is_folder'] and f['depth'] == 1]
    domains_detected = []

    for domain, keywords in domain_vocab.items():
        for rname in root_folder_names:
            if any(kw in rname for kw in keywords):
                # Find the folder
                for f in files_data:
                    if f['is_folder'] and f['depth'] == 1 and f['name'].lower() == rname:
                        # Count children
                        children = [ff for ff in files_data if ff.get('parent_id') == f['id']]
                        child_folders = [c for c in children if c['is_folder']]
                        child_files = [c for c in children if not c['is_folder']]

                        # Prescriptive if 5+ files or 2+ subfolders
                        mode = 'prescriptive' if len(child_files) >= 5 or len(child_folders) >= 2 else 'descriptive'

                        domains_detected.append({
                            "domain": domain,
                            "root_folder_id": f['id'],
                            "root_folder_path": f['name'],
                            "mode": mode,
                            "locked": False,
                        })
                        break
                break

    # Naming analysis
    naming_date_format = None
    naming_capitalization = None
    date_prefix_count = 0
    date_suffix_count = 0
    title_count = 0
    lower_count = 0

    import re
    for f in files_data:
        if f['is_folder']:
            continue
        name = f['name']

        # Date patterns
        if re.match(r'^\d{4}-\d{2}-\d{2}', name) or re.match(r'^\d{4}-Q\d', name):
            naming_date_format = 'YYYY-MM-DD'
            date_prefix_count += 1
        elif re.match(r'^\d{2}-\d{2}-\d{4}', name):
            naming_date_format = 'MM-DD-YYYY'
            date_prefix_count += 1
        elif re.search(r'\d{4}-\d{2}-\d{2}', name):
            date_suffix_count += 1

        # Capitalization
        if name and name != name.lower() and not name.isupper():
            title_count += 1
        elif name and name == name.lower():
            lower_count += 1

    if date_prefix_count > date_suffix_count:
        naming_date_position = 'prefix'
    elif date_suffix_count > date_prefix_count:
        naming_date_position = 'suffix'
    else:
        naming_date_position = 'none'

    if title_count > lower_count:
        naming_capitalization = 'title'
    else:
        naming_capitalization = 'lower' if lower_count > 0 else 'mixed'

    # Depth preference
    depths = [f['depth'] for f in files_data if not f['is_folder']]
    median_depth = sorted(depths)[len(depths) // 2] if depths else 1
    avg_files_per_folder = non_folder_count / max(folder_count, 1)

    preference_profile = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "scan_id": scan_id,
        "naming": {
            "date_format": naming_date_format,
            "date_position": naming_date_position,
            "capitalization": naming_capitalization,
            "separator": None,
            "locked": False,
        },
        "depth_preference": {
            "median_depth": median_depth,
            "prefer_fine_grained": avg_files_per_folder < 10,
            "locked": False,
        },
        "sacred_folders": [],
        "domains_detected": domains_detected,
        "auto_approved_patterns": [],
        "class_precision": {
            "location": 0.5,
            "content_mismatch": 0.5,
            "depth": 0.5,
            "name_inconsistency": 0.5,
            "stale_staging": 0.5,
            "duplicate_candidate": 0.5,
            "poor_name": 0.5,
            "domain_prescriptive": 0.5,
            "domain_descriptive": 0.5,
        },
        "suppressed_classes": [],
    }

    if not dry_run:
        PREFERENCE_PROFILE_PATH.write_text(json.dumps(preference_profile, indent=2))
        print(f"  Written preference_profile.json")

    # Step 7: Generate initial proposals based on content analysis
    print("  Step 7: Generating initial proposals...")

    proposals = []
    proposals_path = BOWER_DATA / "proposals.jsonl"

    # Analyze each non-root, non-folder file for potential proposals
    domain_roots = {}
    for d in domains_detected:
        if d['mode'] == 'prescriptive':
            domain_roots[d['domain']] = d['root_folder_id']

    # Detect orphaned tax/legal/finance files at root level
    root_level_files = [f for f in files_data if not f['is_folder'] and f['depth'] == 1]
    orphaned = [f for f in root_level_files if f['content_summary'] or detect_content_type(f['name'], None)]

    for f in orphaned[:20]:  # Limit to 20 for review
        types_found = detect_content_type(f['name'], f.get('content_summary'))
        if not types_found:
            continue

        dest_domain = types_found[0]
        if dest_domain in domain_roots:
            # This file might belong in a domain folder
            pass  # Only create proposals with high confidence

    # Poor name detection
    poor_name_patterns = ['copy of', 'copy ', 'final', 'v2', 'v3', 'untitled', 'new document', 'draft']
    poor_name_files = [f for f in files_data
                       if not f['is_folder']
                       and any(p in f['name'].lower() for p in poor_name_patterns)]

    for f in poor_name_files[:10]:
        proposal = {
            "proposal_id": f"p_{hashlib.md5(('rename_' + f['id']).encode()).hexdigest()[:12]}",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "scan_id": scan_id,
            "proposal_type": "rename",
            "source_id": f['id'],
            "source_path": f['parent_path'],
            "source_name": f['name'],
            "destination_id": None,
            "destination_path": f['parent_path'],
            "new_name": None,
            "previous_value": None,
            "proposed_description": None,
            "outlier_class": "poor_name",
            "domain": None,
            "confidence_tier": "med",
            "content_signal": False,
            "auto_approved": False,
            "pattern_key": None,
            "reasoning": f"Filename suggests an informal or duplicated naming pattern. Current name: {f['name']}",
            "status": "pending",
            "skip_reason": None,
            "approved_at": None,
            "executed_at": None,
            "expires_at": "2026-04-20T00:00:00+00:00",
            "error": None
        }
        proposals.append(proposal)

    if not dry_run:
        with open(proposals_path, 'w') as fh:
            for p in proposals:
                fh.write(json.dumps(p) + '\n')
        print(f"  Written {len(proposals)} proposals to proposals.jsonl")

    # Step 8: Write scan event
    print("  Step 8: Writing scan event...")
    completed_at = datetime.now(timezone.utc).isoformat()

    scan_event = {
        "event_id": f"evt_{hashlib.md5(scan_id.encode()).hexdigest()[:12]}",
        "scan_id": scan_id,
        "scan_type": "deep",
        "started_at": started_at,
        "completed_at": completed_at,
        "file_count": non_folder_count,
        "folder_count": folder_count,
        "content_read_count": content_read_count,
        "content_skip_count": content_skip_count,
        "description_proposed_count": description_proposed_count,
        "checkpoint_id": None,
        "drift_rate": None,
        "abort_reason": None,
        "error": None
    }

    if not dry_run:
        with open(SCAN_EVENTS_PATH, 'a') as fh:
            fh.write(json.dumps(scan_event) + '\n')

    # Step 9: Summary
    print("\n" + "=" * 60)
    print(f"Bower Founding Scan Complete")
    print(f"  Scan ID: {scan_id}")
    print(f"  Files scanned: {non_folder_count}")
    print(f"  Folders scanned: {folder_count}")
    print(f"  Content read: {content_read_count}")
    print(f"  Content skipped: {content_skip_count}")
    print(f"  Descriptions proposed: {description_proposed_count}")
    print(f"  Domains detected: {len(domains_detected)}")
    for d in domains_detected:
        print(f"    - {d['domain']} ({d['mode']})")
    print(f"  Proposals generated: {len(proposals)}")
    print(f"  Structural model: {STRUCTURAL_MODEL_PATH}")
    print(f"  Preference profile: {PREFERENCE_PROFILE_PATH}")
    print("=" * 60)

    return 0


if __name__ == '__main__':
    sys.exit(main())
