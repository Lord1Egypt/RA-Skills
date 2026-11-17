#!/usr/bin/env python3
# Usage: bower_analyze.py [--help] [--scan-data PATH]
# argparse-based CLI for Bower analysis
"""
Bower Analysis Script
Implements bower.analyze: loads scan data, builds preference profile,
detects domains, generates organization proposals.
"""

import json
import os
import re
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict, Counter
import hashlib

import sys as _sys
if set(_sys.argv[1:]) & {"--help", "-h"}:
    print((__doc__ or "Usage: bower_analyze.py [--scan-data PATH]").strip())
    _sys.exit(0)

# Configuration
AGENT_ROOT = Path(os.environ.get("HERMES_HOME") or os.environ.get("OCAS_AGENT_ROOT") or Path.home() / ".hermes")
BOWER_DATA = AGENT_ROOT / "commons/data/ocas-bower"
SCANS_DIR = BOWER_DATA / "scans"
CONTENT_SUMMARIES_PATH = BOWER_DATA / "content_summaries.jsonl"
FOLDER_INDEX_PATH = BOWER_DATA / "folder_index.json"
DRIVE_DIGEST_PATH = BOWER_DATA / "drive_digest.json"
PREFERENCE_PROFILE_PATH = BOWER_DATA / "preference_profile.json"
PROPOSALS_PATH = BOWER_DATA / "proposals.jsonl"
FEEDBACK_LOG_PATH = BOWER_DATA / "feedback_log.jsonl"
ANALYSIS_EVENTS_PATH = BOWER_DATA / "analysis_events.jsonl"
CONFIG_PATH = BOWER_DATA / "config.json"

# Domain detection vocabulary
DOMAIN_VOCABULARY = {
    "taxes": ["tax", "taxes", "irs", "tax return", "w2", "w-2", "1099", "schedule k", "hmrc", "vat"],
    "projects": ["projects", "project", "clients", "client work", "engagements", "work"],
    "home": ["home", "house", "apartment", "property", "household", "real estate"],
    "finance": ["finance", "financial", "banking", "bank", "investments", "brokerage", "accounts", "statements"],
    "legal": ["legal", "contracts", "agreements", "law", "attorney", "nda", "lease", "deed"],
    "medical": ["medical", "health", "insurance", "eob", "explanation of benefits", "records", "rx", "prescription", "lab", "doctor", "hospital"],
    "archive": ["archive", "archived", "reference", "old", "historical", "backup"],
    "education": ["school", "university", "college", "course", "class", "lecture", "education", "study", "degree", "certificate"]
}

# Forbidden move/rename categories
FORBIDDEN_MOVE_TYPES = [
    "application/vnd.google-apps.folder",
    "application/vnd.google-apps.shortcut"
]

def load_config():
    """Load configuration"""
    if CONFIG_PATH.exists():
        with open(CONFIG_PATH) as f:
            return json.load(f)
    return {}

def load_folder_index():
    """Load folder index"""
    with open(FOLDER_INDEX_PATH) as f:
        return json.load(f)

def load_drive_digest():
    """Load drive digest"""
    if DRIVE_DIGEST_PATH.exists():
        with open(DRIVE_DIGEST_PATH) as f:
            return json.load(f)
    return {}

def load_content_summaries():
    """Load content summaries into a dict keyed by file ID"""
    summaries = {}
    if CONTENT_SUMMARIES_PATH.exists():
        with open(CONTENT_SUMMARIES_PATH) as f:
            for line in f:
                try:
                    entry = json.loads(line)
                    file_id = entry.get('id')
                    if file_id:
                        summaries[file_id] = entry
                except json.JSONDecodeError:
                    continue
    return summaries

def load_feedback_suppressions():
    """Load feedback suppressions from feedback log"""
    suppressions = defaultdict(int)
    if FEEDBACK_LOG_PATH.exists():
        with open(FEEDBACK_LOG_PATH) as f:
            for line in f:
                try:
                    entry = json.loads(line)
                    pattern_key = entry.get('pattern_key')
                    if pattern_key:
                        suppressions[pattern_key] += 1
                except json.JSONDecodeError:
                    continue
    return suppressions

def load_existing_proposals():
    """Load existing proposals to avoid duplicates"""
    existing = {}
    if PROPOSALS_PATH.exists():
        with open(PROPOSALS_PATH) as f:
            for line in f:
                try:
                    proposal = json.loads(line)
                    source_id = proposal.get('source_id')
                    status = proposal.get('status')
                    if source_id and status in ('pending', 'approved'):
                        existing[source_id] = proposal
                except json.JSONDecodeError:
                    continue
    return existing

def build_folder_hierarchy(folder_index):
    """Build folder hierarchy from folder index"""
    folders = folder_index.get('folders', [])
    
    # Build lookup by ID
    folder_by_id = {f['id']: f for f in folders}
    
    # Build path lookup
    folder_paths = {}
    
    def get_folder_path(folder_id, visited=None):
        if visited is None:
            visited = set()
        if folder_id in visited:
            return f"/{folder_id}"  # Circular reference protection
        visited.add(folder_id)
        
        if folder_id in folder_paths:
            return folder_paths[folder_id]
        
        folder = folder_by_id.get(folder_id)
        if not folder:
            return f"/{folder_id}"
        
        parents = folder.get('parents', [])
        if not parents or parents[0] == folder_id:
            # Root folder
            path = f"/{folder.get('name', folder_id)}"
        else:
            parent_path = get_folder_path(parents[0], visited)
            path = f"{parent_path}/{folder.get('name', folder_id)}"
        
        folder_paths[folder_id] = path
        return path
    
    # Build paths for all folders
    for folder_id in folder_by_id:
        get_folder_path(folder_id)
    
    return folder_by_id, folder_paths

def scan_all_files():
    """Scan all files from scan files"""
    all_files = []
    folder_file_counts = defaultdict(int)
    
    for scan_file in SCANS_DIR.glob("*.json"):
        try:
            with open(scan_file) as f:
                data = json.load(f)
            
            folder_id = data.get('folder_id')
            folder_name = data.get('folder_name', '')
            files = data.get('children', data.get('files', []))
            
            for file in files:
                file['_folder_id'] = folder_id
                file['_folder_name'] = folder_name
                all_files.append(file)
                folder_file_counts[folder_id] += 1
        except (json.JSONDecodeError, KeyError):
            continue
    
    return all_files, folder_file_counts

def detect_domain_for_folder(folder_path, folder_name, files):
    """Detect domain for a folder based on name and file content"""
    folder_text = f"{folder_path} {folder_name}".lower()
    
    # Skip if folder name is too generic or system-like
    generic_names = ['documents', 'files', 'data', 'stuff', 'misc', 'temp', 'untitled']
    if folder_name.lower() in generic_names:
        return None, None
    
    # Check folder name/path against vocabulary
    domain_scores = defaultdict(int)
    for domain, keywords in DOMAIN_VOCABULARY.items():
        for keyword in keywords:
            if keyword in folder_text:
                # Stronger signal for exact folder name match
                if keyword in folder_name.lower():
                    domain_scores[domain] += 5  # Folder name match is very strong signal
                else:
                    domain_scores[domain] += 2  # Path match is weaker
    
    # Check file names and content
    for file in files[:20]:  # Sample first 20 files
        file_text = f"{file.get('name', '')} {file.get('description', '')}".lower()
        for domain, keywords in DOMAIN_VOCABULARY.items():
            for keyword in keywords:
                if keyword in file_text:
                    domain_scores[domain] += 1
    
    if not domain_scores:
        return None, None
    
    # Get top domain
    top_domain = max(domain_scores.items(), key=lambda x: x[1])
    domain, score = top_domain
    
    # Require stronger evidence for domain assignment
    if score >= 8:  # Increased threshold
        confidence = "high"
    elif score >= 5:
        confidence = "med"
    else:
        confidence = "low"
    
    # Only assign domain if we have medium or high confidence
    if confidence == "low":
        return None, None
    
    # Determine mode (prescriptive vs descriptive)
    # Prescriptive if folder has clear domain structure (5+ files or 2+ subfolders)
    subfolder_count = sum(1 for f in files if f.get('mimeType') == 'application/vnd.google-apps.folder')
    if len(files) >= 5 or subfolder_count >= 2:
        mode = "prescriptive"
    else:
        mode = "descriptive"
    
    return domain, {"confidence": confidence, "mode": mode}

def is_system_folder(folder_path, folder_name):
    """Check if a folder is a system/backup folder that should be excluded from domain detection"""
    folder_path_lower = folder_path.lower()
    folder_name_lower = folder_name.lower()
    
    # Skip folders with these patterns in path or name
    exclude_patterns = [
        'node_modules', '.git', '__pycache__', '.venv', 'venv',
        'backup', 'backups', 'archive', 'archived',
        'temp', 'tmp', 'cache', '.cache',
        'logs', 'log', '.log',
        'test', 'tests', 'testing',
        'build', 'dist', 'out', 'output',
        '.github', '.vscode', '.idea',
        'vendor', 'packages', 'dependencies',
        'site-packages', 'lib/python',
        'data-download', 'flickr import',
        '2026-', '2025-', '2024-', '2023-', '2022-',  # Timestamped folders
        '.clawhub', 'references', 'classifications',  # System folders
    ]
    
    # Check for timestamp patterns (like 2026-04-09_06-00-01)
    import re
    timestamp_pattern = r'\d{4}-\d{2}-\d{2}[_\-\s]\d{2}-\d{2}-\d{2}'
    if re.search(timestamp_pattern, folder_path_lower):
        return True
    
    # Check for backup folder patterns
    backup_patterns = ['backup', 'backups', 'archive', 'archived']
    if any(pattern in folder_path_lower for pattern in backup_patterns):
        return True
    
    # Check for exclude patterns
    if any(pattern in folder_path_lower or pattern in folder_name_lower for pattern in exclude_patterns):
        return True
    
    # Check for very long folder IDs (likely system-generated)
    if len(folder_name) > 30 and all(c in '0123456789abcdef-' for c in folder_name):
        return True
    
    # Check for folders with no meaningful name (just IDs)
    if len(folder_name) > 20 and not any(c.isalpha() for c in folder_name):
        return True
    
    # Check for folders that start with long hex IDs (like 1U6KEOL3IHvu-jwxSWsEzCq1RJcRveYDj)
    if len(folder_name) > 20 and re.match(r'^[A-Za-z0-9_-]{20,}$', folder_name):
        return True
    
    return False

def build_preference_profile(all_files, folder_by_id, folder_paths, folder_file_counts):
    """Build preference profile from scan data"""
    profile = {
        "naming_conventions": analyze_naming_conventions(all_files),
        "depth_preference": analyze_depth_preference(folder_paths),
        "folder_density": analyze_folder_density(folder_file_counts),
        "date_handling": analyze_date_handling(all_files),
        "sacred_folders": identify_sacred_folders(all_files, folder_by_id),
        "domains": {},
        "auto_approved_patterns": [],
        "class_precision": {},
        "last_updated": datetime.now().isoformat()
    }
    
    # Detect domains
    domain_folders = defaultdict(list)
    for scan_file in SCANS_DIR.glob("*.json"):
        try:
            with open(scan_file) as f:
                data = json.load(f)
            
            folder_id = data.get('folder_id')
            folder_name = data.get('folder_name', '')
            files = data.get('children', data.get('files', []))
            folder_path = folder_paths.get(folder_id, f"/{folder_name}")
            
            # Skip backup/system folders for domain detection
            if is_system_folder(folder_path, folder_name):
                continue
            
            domain, domain_info = detect_domain_for_folder(folder_path, folder_name, files)
            if domain:
                domain_folders[domain].append({
                    "folder_id": folder_id,
                    "folder_path": folder_path,
                    "folder_name": folder_name,
                    "file_count": len(files),
                    "info": domain_info
                })
        except (json.JSONDecodeError, KeyError):
            continue
    
    # Consolidate domains - prefer top-level user folders
    for domain, folders in domain_folders.items():
        if folders:
            # Score folders based on: top-level status, file count, name match
            def folder_score(f):
                score = 0
                # Prefer top-level folders (fewer path separators)
                path_depth = f['folder_path'].count('/')
                score += max(0, 10 - path_depth) * 100
                
                # Prefer folders with more files
                score += min(f['file_count'], 100)
                
                # Prefer folders with exact domain name match
                if domain in f['folder_name'].lower():
                    score += 50
                
                # Prefer folders without system-like names
                if not any(sys in f['folder_name'].lower() for sys in ['node_modules', 'backup', 'cache']):
                    score += 25
                
                return score
            
            root_folder = max(folders, key=folder_score)
            profile["domains"][domain] = {
                "root_path": root_folder['folder_path'],
                "mode": root_folder['info']['mode'],
                "confidence": root_folder['info']['confidence'],
                "folders": [f['folder_path'] for f in folders]
            }
    
    return profile

def analyze_naming_conventions(all_files):
    """Analyze naming conventions from files"""
    conventions = {
        "date_prefix": 0,
        "title_case": 0,
        "lowercase": 0,
        "uppercase": 0,
        "underscores": 0,
        "hyphens": 0,
        "spaces": 0,
        "version_suffixes": 0
    }
    
    for file in all_files[:1000]:  # Sample first 1000 files
        name = file.get('name', '')
        if not name:
            continue
        
        # Date prefix detection
        if re.match(r'^\d{4}[-_]\d{2}[-_]\d{2}', name):
            conventions["date_prefix"] += 1
        elif re.match(r'^\d{4}-Q[1-4]', name):
            conventions["date_prefix"] += 1
        
        # Case detection
        if name == name.upper() and len(name) > 3:
            conventions["uppercase"] += 1
        elif name == name.lower():
            conventions["lowercase"] += 1
        elif re.match(r'^[A-Z][a-z]', name):
            conventions["title_case"] += 1
        
        # Separator detection
        if '_' in name and ' ' not in name:
            conventions["underscores"] += 1
        elif '-' in name and ' ' not in name:
            conventions["hyphens"] += 1
        elif ' ' in name:
            conventions["spaces"] += 1
        
        # Version suffix detection
        if re.search(r'[_-]v\d+', name, re.IGNORECASE) or re.search(r'[_-]final', name, re.IGNORECASE):
            conventions["version_suffixes"] += 1
    
    # Determine dominant convention
    if conventions:
        dominant = max(conventions.items(), key=lambda x: x[1])
        return {
            "dominant": dominant[0],
            "distribution": conventions,
            "locked": False
        }
    return {"dominant": "mixed", "distribution": conventions, "locked": False}

def analyze_depth_preference(folder_paths):
    """Analyze depth preference from folder paths"""
    depths = []
    for path in folder_paths.values():
        depth = len([p for p in path.split('/') if p])
        depths.append(depth)
    
    if not depths:
        return {"median_depth": 2, "prefer_fine_grained": True, "locked": False}
    
    depths.sort()
    median_depth = depths[len(depths) // 2]
    
    return {
        "median_depth": median_depth,
        "prefer_fine_grained": median_depth > 2,
        "locked": False
    }

def analyze_folder_density(folder_file_counts):
    """Analyze folder density (files per folder)"""
    if not folder_file_counts:
        return {"average": 0, "preference": "unknown", "locked": False}
    
    counts = list(folder_file_counts.values())
    average = sum(counts) / len(counts)
    
    if average < 10:
        preference = "fine_grained"
    elif average > 50:
        preference = "coarse"
    else:
        preference = "balanced"
    
    return {
        "average": round(average, 1),
        "preference": preference,
        "locked": False
    }

def analyze_date_handling(all_files):
    """Analyze date handling patterns"""
    date_patterns = {
        "in_filename": 0,
        "in_folder": 0,
        "prefix": 0,
        "suffix": 0,
        "none": 0
    }
    
    for file in all_files[:1000]:  # Sample
        name = file.get('name', '')
        folder_name = file.get('_folder_name', '')
        
        # Check for dates in filename
        if re.search(r'\b(19|20)\d{2}\b', name):
            date_patterns["in_filename"] += 1
        
        # Check for dates in folder name
        if re.search(r'\b(19|20)\d{2}\b', folder_name):
            date_patterns["in_folder"] += 1
        
        # Check position
        if re.match(r'^(19|20)\d{2}', name):
            date_patterns["prefix"] += 1
        elif re.search(r'(19|20)\d{2}$', name):
            date_patterns["suffix"] += 1
    
    # Determine dominant pattern
    if date_patterns:
        dominant = max(date_patterns.items(), key=lambda x: x[1])
        return {
            "dominant": dominant[0],
            "distribution": date_patterns,
            "locked": False
        }
    return {"dominant": "none", "distribution": date_patterns, "locked": False}

def identify_sacred_folders(all_files, folder_by_id):
    """Identify sacred folders (unchanged 90+ days with 20+ files)"""
    sacred = []
    
    # Group files by folder
    folder_files = defaultdict(list)
    for file in all_files:
        folder_id = file.get('_folder_id')
        if folder_id:
            folder_files[folder_id].append(file)
    
    # Check each folder
    for folder_id, files in folder_files.items():
        if len(files) < 20:
            continue
        
        # Check if any file modified recently
        recent_mod = False
        for file in files:
            modified = file.get('modifiedTime')
            if modified:
                try:
                    mod_date = datetime.fromisoformat(modified.replace('Z', '+00:00'))
                    if datetime.now().astimezone() - mod_date < timedelta(days=90):
                        recent_mod = True
                        break
                except ValueError:
                    continue
        
        if not recent_mod:
            folder = folder_by_id.get(folder_id, {})
            sacred.append({
                "folder_id": folder_id,
                "folder_name": folder.get('name', 'Unknown'),
                "file_count": len(files)
            })
    
    return sacred

def classify_file_outlier(file, folder_path, folder_files, preference_profile, content_summaries):
    """Classify a file as an outlier and determine proposal type"""
    file_id = file.get('id')
    file_name = file.get('name', '')
    mime_type = file.get('mimeType', '')
    modified = file.get('modifiedTime', '')
    
    # Skip folders and shortcuts
    if mime_type in FORBIDDEN_MOVE_TYPES:
        return None
    
    # Skip recently modified files (within 24 hours)
    if modified:
        try:
            mod_date = datetime.fromisoformat(modified.replace('Z', '+00:00'))
            if datetime.now().astimezone() - mod_date < timedelta(hours=24):
                return None
        except ValueError:
            pass
    
    # Skip starred files unless high confidence
    if file.get('starred') and not file.get('_high_confidence'):
        return None
    
    outlier_classes = []
    proposals = []
    
    # 1. Check for depth outlier (file at root level)
    if folder_path == "/" or folder_path.count('/') <= 1:
        outlier_classes.append("depth_outlier")
    
    # 2. Check for location outlier (file in wrong folder based on name/content)
    content_summary = content_summaries.get(file_id, {}).get('summary_text', '')
    
    # Check if file belongs to a domain
    file_text = f"{file_name} {content_summary}".lower()
    for domain, keywords in DOMAIN_VOCABULARY.items():
        for keyword in keywords:
            if keyword in file_text:
                # Check if file is in wrong domain folder
                if domain in preference_profile.get('domains', {}):
                    domain_root = preference_profile['domains'][domain]['root_path']
                    if not folder_path.startswith(domain_root):
                        outlier_classes.append("location_outlier")
                        # Generate move proposal
                        proposals.append({
                            "type": "move",
                            "domain": domain,
                            "destination": domain_root,
                            "confidence": "high" if preference_profile['domains'][domain]['mode'] == 'prescriptive' else "med"
                        })
                break
    
    # 3. Check for name inconsistency
    if folder_files:
        sibling_names = [f.get('name', '') for f in folder_files if f.get('id') != file_id]
        if sibling_names and len(sibling_names) >= 3:
            # Check if name follows sibling convention
            # Simple check: if siblings use underscores and this file uses spaces
            sibling_convention = "spaces" if any(' ' in name for name in sibling_names[:5]) else "underscores"
            file_convention = "spaces" if ' ' in file_name else "underscores"
            
            if sibling_convention != file_convention:
                outlier_classes.append("name_inconsistency")
    
    # 4. Check for stale staging
    staging_folders = ["inbox", "unsorted", "staging", "to sort", "temp", "tmp"]
    folder_name_lower = folder_path.lower().split('/')[-1] if folder_path else ""
    if any(staging in folder_name_lower for staging in staging_folders):
        if modified:
            try:
                mod_date = datetime.fromisoformat(modified.replace('Z', '+00:00'))
                if datetime.now().astimezone() - mod_date > timedelta(days=30):
                    outlier_classes.append("stale_staging")
            except ValueError:
                pass
    
    # 5. Check for description auto-write opportunity
    if not file.get('description') and content_summary:
        proposals.append({
            "type": "describe_auto",
            "confidence": "high"
        })
    
    # Generate proposals based on outlier classes
    if outlier_classes:
        # For now, just return the classification
        return {
            "file_id": file_id,
            "file_name": file_name,
            "outlier_classes": outlier_classes,
            "proposals": proposals,
            "folder_path": folder_path
        }
    
    return None

def generate_proposals(all_files, folder_by_id, folder_paths, preference_profile, content_summaries, suppressions):
    """Generate organization proposals"""
    proposals = []
    existing_proposals = load_existing_proposals()
    
    # Group files by folder
    folder_files = defaultdict(list)
    for file in all_files:
        folder_id = file.get('_folder_id')
        if folder_id:
            folder_files[folder_id].append(file)
    
    # Analyze each file
    for file in all_files:
        file_id = file.get('id')
        
        # Skip if already has pending/approved proposal
        if file_id in existing_proposals:
            continue
        
        folder_id = file.get('_folder_id')
        folder_path = folder_paths.get(folder_id, f"/{file.get('_folder_name', 'Unknown')}")
        folder_file_list = folder_files.get(folder_id, [])
        
        classification = classify_file_outlier(
            file, folder_path, folder_file_list, 
            preference_profile, content_summaries
        )
        
        if classification:
            # Apply feedback suppressions
            for proposal in classification['proposals']:
                pattern_key = f"{proposal.get('type')}:{folder_path}:{proposal.get('destination', '')}"
                
                # Check suppression level
                suppression_count = suppressions.get(pattern_key, 0)
                if suppression_count >= 3:
                    continue  # Fully suppressed
                elif suppression_count == 2:
                    if proposal.get('confidence') in ['low', 'med']:
                        continue  # Suppress low/med
                elif suppression_count == 1:
                    # Downgrade confidence
                    if proposal.get('confidence') == 'high':
                        proposal['confidence'] = 'med'
                    elif proposal.get('confidence') == 'med':
                        proposal['confidence'] = 'low'
                
                # Create proposal record
                proposal_type = proposal.get('type')
                hash_input = f"{file_id}_{proposal_type}"
                proposal_id = f"p_{hashlib.md5(hash_input.encode()).hexdigest()[:8]}"
                
                proposal_record = {
                    "proposal_id": proposal_id,
                    "source_id": file_id,
                    "source_name": file.get('name', ''),
                    "source_path": folder_path,
                    "proposal_type": proposal.get('type'),
                    "confidence_tier": proposal.get('confidence', 'med'),
                    "outlier_classes": classification['outlier_classes'],
                    "domain": proposal.get('domain'),
                    "destination_path": proposal.get('destination'),
                    "status": "pending",
                    "created_at": datetime.now().isoformat(),
                    "expires_at": (datetime.now() + timedelta(days=14)).isoformat(),
                    "reasoning": f"File classified as {', '.join(classification['outlier_classes'])}",
                    "auto_approved": False
                }
                
                proposals.append(proposal_record)
    
    return proposals

def expire_old_proposals():
    """Expire old pending proposals"""
    if not PROPOSALS_PATH.exists():
        return 0
    
    expired_count = 0
    proposals = []
    
    with open(PROPOSALS_PATH) as f:
        for line in f:
            try:
                proposal = json.loads(line)
                if proposal.get('status') == 'pending':
                    expires_at = proposal.get('expires_at')
                    if expires_at:
                        try:
                            expiry_date = datetime.fromisoformat(expires_at)
                            # Make both timezone-aware or both naive
                            if expiry_date.tzinfo is not None:
                                # expiry_date is timezone-aware
                                current_time = datetime.now().astimezone()
                            else:
                                # expiry_date is naive
                                current_time = datetime.now()
                            
                            if current_time > expiry_date:
                                proposal['status'] = 'expired'
                                expired_count += 1
                        except ValueError:
                            pass
                proposals.append(proposal)
            except json.JSONDecodeError:
                continue
    
    # Write back
    with open(PROPOSALS_PATH, 'w') as f:
        for proposal in proposals:
            f.write(json.dumps(proposal) + '\n')
    
    return expired_count

def write_analysis_event(stats):
    """Write analysis event to log"""
    event = {
        "event_type": "analysis",
        "timestamp": datetime.now().isoformat(),
        "stats": stats
    }
    
    with open(ANALYSIS_EVENTS_PATH, 'a') as f:
        f.write(json.dumps(event) + '\n')

def main():
    """Main analysis function"""
    print("Starting Bower analysis...")
    
    # Load data
    print("Loading folder index...")
    folder_index = load_folder_index()
    folder_by_id, folder_paths = build_folder_hierarchy(folder_index)
    
    print("Loading content summaries...")
    content_summaries = load_content_summaries()
    
    print("Loading feedback suppressions...")
    suppressions = load_feedback_suppressions()
    
    print("Scanning all files...")
    all_files, folder_file_counts = scan_all_files()
    print(f"Found {len(all_files)} files across {len(folder_file_counts)} folders")
    
    # Build preference profile
    print("Building preference profile...")
    preference_profile = build_preference_profile(all_files, folder_by_id, folder_paths, folder_file_counts)
    
    # Save preference profile
    with open(PREFERENCE_PROFILE_PATH, 'w') as f:
        json.dump(preference_profile, f, indent=2)
    print(f"Preference profile saved with {len(preference_profile.get('domains', {}))} domains")
    
    # Expire old proposals
    print("Expiring old proposals...")
    expired_count = expire_old_proposals()
    print(f"Expired {expired_count} old proposals")
    
    # Generate new proposals
    print("Generating proposals...")
    new_proposals = generate_proposals(
        all_files, folder_by_id, folder_paths, 
        preference_profile, content_summaries, suppressions
    )
    print(f"Generated {len(new_proposals)} new proposals")
    
    # Append new proposals to proposals.jsonl
    if new_proposals:
        with open(PROPOSALS_PATH, 'a') as f:
            for proposal in new_proposals:
                f.write(json.dumps(proposal) + '\n')
    
    # Write analysis event
    stats = {
        "files_analyzed": len(all_files),
        "folders_analyzed": len(folder_file_counts),
        "domains_detected": len(preference_profile.get('domains', {})),
        "proposals_generated": len(new_proposals),
        "proposals_expired": expired_count,
        "content_summaries_loaded": len(content_summaries)
    }
    write_analysis_event(stats)
    
    print("\nAnalysis complete!")
    print(f"Domains detected: {list(preference_profile.get('domains', {}).keys())}")
    print(f"New proposals: {len(new_proposals)}")
    print(f"Expired proposals: {expired_count}")
    
    # Print proposal summary
    if new_proposals:
        print("\nProposal summary:")
        by_type = defaultdict(int)
        by_confidence = defaultdict(int)
        for p in new_proposals:
            by_type[p.get('proposal_type', 'unknown')] += 1
            by_confidence[p.get('confidence_tier', 'unknown')] += 1
        
        print(f"  By type: {dict(by_type)}")
        print(f"  By confidence: {dict(by_confidence)}")

if __name__ == "__main__":
    main()