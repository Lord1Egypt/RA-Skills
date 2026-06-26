#!/usr/bin/env python3
"""
Memory Indexer - Creates searchable index from memory markdown files
"""

import os
import json
import re
from pathlib import Path
from datetime import datetime
from collections import defaultdict


def _env_path(name: str, fallback: str) -> Path:
    value = os.getenv(name, fallback)
    return Path(os.path.expandvars(value)).expanduser()


MEMORY_DIR = _env_path("MEMORY_PRO_DATA_DIR", os.path.join(os.getenv("OPENCLAW_WORKSPACE", ""), "memory"))
INDEX_FILE = _env_path(
    "MEMORY_PRO_LEGACY_INDEX_PATH",
    os.path.join(os.getenv("OPENCLAW_WORKSPACE", ""), "skills", "memory-pro", "data", "INDEX.json"),
)
STATE_FILE = _env_path(
    "MEMORY_PRO_LEGACY_STATE_PATH",
    os.path.join(os.getenv("OPENCLAW_WORKSPACE", ""), "skills", "memory-pro", "data", "state.json"),
)

def extract_keywords(text):
    """Extract keywords from text (Chinese and English)"""
    # Remove markdown syntax
    text = re.sub(r'[#*`\[\]()]', ' ', text)
    
    # Split into words (handle Chinese and English)
    words = []
    
    # English words (3+ chars)
    english_words = re.findall(r'\b[a-zA-Z]{3,}\b', text)
    words.extend([w.lower() for w in english_words])
    
    # Chinese phrases (2+ chars) and single characters
    chinese_phrases = re.findall(r'[\u4e00-\u9fff]{1,}', text)  # Changed to 1+ chars
    words.extend(chinese_phrases)
    
    # Technical terms (camelCase, kebab-case, etc.)
    tech_terms = re.findall(r'[A-Z][a-z]+(?:[A-Z][a-z]+)+|[\w]+-[\w]+', text)
    words.extend([t.lower() for t in tech_terms])
    
    # Filter common words
    stopwords = {'the', 'and', 'for', 'with', 'this', 'that', 'from', 'have', 'has', '的', '了', '是', '在', '我', '你', '他'}
    words = [w for w in words if w not in stopwords and len(w) > 0]  # Allow single chars
    
    return list(set(words))

def get_file_mtime(filepath):
    """Get file modification time"""
    return os.path.getmtime(filepath)

def load_state():
    """Load processing state"""
    if STATE_FILE.exists():
        with open(STATE_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_state(state):
    """Save processing state"""
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(STATE_FILE, 'w', encoding='utf-8') as f:
        json.dump(state, f, ensure_ascii=False, indent=2)

def load_index():
    """Load existing index"""
    if INDEX_FILE.exists():
        with open(INDEX_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_index(index):
    """Save index to file"""
    INDEX_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(INDEX_FILE, 'w', encoding='utf-8') as f:
        json.dump(index, f, ensure_ascii=False, indent=2)

def process_file(filepath, incremental=False, state=None):
    """Process a single markdown file"""
    if state is None:
        state = load_state()
    
    file_key = str(filepath)
    current_mtime = get_file_mtime(filepath)
    
    # Skip if not modified (incremental mode)
    if incremental and file_key in state:
        if state[file_key] == current_mtime:
            return None
    
    print(f"Processing: {filepath.name}")
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"⚠️ Error reading {filepath.name}: {e}")
        return None
    
    # Extract date from filename (YYYY-MM-DD.md)
    date_match = re.match(r'(\d{4}-\d{2}-\d{2})', filepath.name)
    date = date_match.group(1) if date_match else 'unknown'
    
    # Extract keywords
    keywords = extract_keywords(content)
    
    # Get context (first 200 chars of paragraph containing keyword)
    paragraphs = content.split('\n\n')
    keyword_contexts = defaultdict(list)
    
    for keyword in keywords:
        for para in paragraphs:
            if keyword.lower() in para.lower():
                context = para.strip()[:200]
                if context:
                    keyword_contexts[keyword].append({
                        'date': date,
                        'file': filepath.name,
                        'context': context
                    })
                    break  # One context per keyword per file
    
    # Update state (but don't save yet - save once at end)
    state[file_key] = current_mtime
    
    return keyword_contexts, state

def build_index(incremental=False):
    """Build or update the index"""
    print(f"🔍 Memory Indexer - {'Incremental' if incremental else 'Full'} Mode")
    print(f"📂 Scanning: {MEMORY_DIR}")
    
    if not MEMORY_DIR.exists():
        print(f"❌ Memory directory not found: {MEMORY_DIR}")
        return
    
    # Load state and index
    state = load_state()
    index = load_index() if incremental else {}
    
    # Process all .md files
    md_files = sorted(MEMORY_DIR.glob("*.md"))
    processed = 0
    skipped = 0
    
    for filepath in md_files:
        result = process_file(filepath, incremental, state)
        
        if result is None:
            skipped += 1
            continue
        
        keyword_contexts, state = result
        
        # Merge into index
        for keyword, contexts in keyword_contexts.items():
            if keyword not in index:
                index[keyword] = []
            index[keyword].extend(contexts)
        
        processed += 1
    
    # Save state and index (ONCE at the end)
    save_state(state)
    save_index(index)
    
    print(f"\n✅ Index updated!")
    print(f"📊 Files processed: {processed}")
    print(f"⏭️  Files skipped: {skipped}")
    print(f"🔤 Total keywords: {len(index)}")
    print(f"💾 Index saved: {INDEX_FILE}")

if __name__ == "__main__":
    import sys
    
    incremental = '--incremental' in sys.argv
    build_index(incremental=incremental)
