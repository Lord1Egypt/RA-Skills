#!/usr/bin/env bash
# OpenClaw Memory Stack — A-MEM Self-Organizing Memory
# Zettelkasten-inspired agent-driven memory reorganization.
# Sourced by wrappers; not run standalone.
set -euo pipefail

SELF_ORG_LIB_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_ROOT="${OPENCLAW_INSTALL_ROOT:-$HOME/.openclaw/memory-stack}"
source "$INSTALL_ROOT/lib/contracts.sh"

AMEM_MODEL="${AMEM_MODEL:-qwen2.5:7b}"
AMEM_ENDPOINT="${AMEM_ENDPOINT:-http://localhost:11434}"
AMEM_STATE_DIR="$HOME/.openclaw/state"

# ============================================================
# Stage 1-4: Organize a new memory
# ============================================================
organize_new_memory() {
  local content="$1"
  local model="${AMEM_MODEL}"
  local endpoint="${AMEM_ENDPOINT}"

  if [ -z "$content" ]; then
    echo '{"status": "error", "message": "content is required"}' >&2
    return 1
  fi

  if ! has_command python3; then
    echo '{"status": "error", "message": "python3 required"}' >&2
    return 1
  fi

  mkdir -p "$AMEM_STATE_DIR"

  python3 -c "
import json, sys, os, urllib.request, subprocess
from datetime import datetime, timezone

content = sys.stdin.read().strip()
model = '$model'
endpoint = '$endpoint'
state_dir = '$AMEM_STATE_DIR'

def llm_call(prompt, model=model):
    \"\"\"Call local LLM via Ollama API.\"\"\"
    payload = json.dumps({
        'model': model,
        'prompt': prompt,
        'stream': False,
        'options': {'temperature': 0.3, 'num_predict': 500}
    }).encode()
    req = urllib.request.Request(
        f'{endpoint}/api/generate',
        data=payload,
        headers={'Content-Type': 'application/json'}
    )
    try:
        resp = urllib.request.urlopen(req, timeout=30)
        data = json.loads(resp.read().decode())
        return data.get('response', '').strip()
    except Exception as e:
        return ''

def qmd_vsearch(query, limit=5):
    \"\"\"Search existing memories for connections.\"\"\"
    try:
        result = subprocess.run(
            ['qmd', 'vsearch', query, '--json'],
            capture_output=True, text=True, timeout=10
        )
        if result.returncode == 0 and result.stdout.strip():
            data = json.loads(result.stdout)
            if isinstance(data, list):
                return data[:limit]
            elif isinstance(data, dict) and 'results' in data:
                return data['results'][:limit]
        return []
    except Exception:
        return []

# ── Stage 1: Note generation — structure into note with tags ──
stage1_prompt = f'''Analyze this memory content and generate a structured note.
Return valid JSON only, no other text.

Content: {content[:1000]}

Return JSON with:
- \"title\": short descriptive title (max 60 chars)
- \"summary\": one-sentence summary
- \"tags\": list of 3-7 lowercase tags
- \"category\": one of [\"decision\", \"architecture\", \"bug\", \"learning\", \"preference\", \"workflow\", \"reference\"]
- \"key_entities\": list of named entities (tools, libraries, concepts)
'''

note_raw = llm_call(stage1_prompt)
try:
    # Try to extract JSON from LLM response
    start = note_raw.find('{')
    end = note_raw.rfind('}') + 1
    if start >= 0 and end > start:
        note = json.loads(note_raw[start:end])
    else:
        raise ValueError('No JSON found')
except (json.JSONDecodeError, ValueError):
    # Fallback: basic structuring without LLM
    words = content.lower().split()
    note = {
        'title': ' '.join(words[:8]),
        'summary': content[:150],
        'tags': list(set(w for w in words if len(w) > 4))[:5],
        'category': 'reference',
        'key_entities': []
    }

# ── Stage 2: Historical analysis — find connections ──
related = qmd_vsearch(content[:200])
related_keys = []
for item in related:
    key = item.get('path', item.get('source', item.get('content', '')))[:200]
    score = float(item.get('score', item.get('relevance', item.get('similarity', 0))))
    if key and score > 0.1:
        related_keys.append({'key': key, 'score': round(score, 4)})

# ── Stage 3: Link establishment — create links to related memories ──
links = []
if related_keys:
    for rk in related_keys[:5]:
        links.append({
            'target': rk['key'],
            'similarity': rk['score'],
            'type': 'related'
        })

# ── Stage 4: Tag propagation — inherit cluster tags ──
if related and note.get('tags'):
    # Collect tags from related memories via LLM analysis
    related_context = ' | '.join([
        str(item.get('content', item.get('text', '')))[:100]
        for item in related[:3]
    ])
    if related_context.strip():
        propagation_prompt = f'''Given these related memories:
{related_context}

And a new memory with tags: {json.dumps(note.get('tags', []))}

Suggest 0-3 additional tags that should be inherited from the related memories.
Return valid JSON array of strings only, e.g. [\"tag1\", \"tag2\"]. If none, return [].
'''
        prop_raw = llm_call(propagation_prompt)
        try:
            start = prop_raw.find('[')
            end = prop_raw.rfind(']') + 1
            if start >= 0 and end > start:
                extra_tags = json.loads(prop_raw[start:end])
                if isinstance(extra_tags, list):
                    existing = set(note.get('tags', []))
                    for t in extra_tags:
                        if isinstance(t, str) and t.lower() not in existing:
                            note.setdefault('tags', []).append(t.lower())
                            existing.add(t.lower())
        except (json.JSONDecodeError, ValueError):
            pass

# Build final organized note
timestamp = datetime.now(timezone.utc).isoformat()
organized = {
    'status': 'success',
    'note': note,
    'links': links,
    'linked_to': [l['target'] for l in links],
    'related_count': len(related),
    'timestamp': timestamp,
    'model': model,
    'stages_completed': ['note_generation', 'historical_analysis', 'link_establishment', 'tag_propagation']
}

# Log the organization for audit
log_path = os.path.join(state_dir, 'amem-audit.log')
try:
    with open(log_path, 'a') as f:
        f.write(json.dumps({'timestamp': timestamp, 'action': 'organize', 'title': note.get('title', ''), 'links': len(links)}) + '\n')
except:
    pass

print(json.dumps(organized, indent=2))
" <<< "$content"
}

# ============================================================
# Periodic reorganization of existing memories
# ============================================================
reorganize_memories() {
  local collection="${1:-}"
  local model="${AMEM_MODEL}"
  local endpoint="${AMEM_ENDPOINT}"
  local dry_run="${AMEM_DRY_RUN:-false}"

  if ! has_command python3; then
    echo '{"status": "error", "message": "python3 required"}' >&2
    return 1
  fi

  if ! has_command qmd; then
    echo '{"status": "error", "message": "qmd CLI required for reorganization"}' >&2
    return 1
  fi

  mkdir -p "$AMEM_STATE_DIR"

  python3 -c "
import json, sys, os, subprocess, urllib.request
from datetime import datetime, timezone

model = '$model'
endpoint = '$endpoint'
collection = '$collection'
dry_run = '$dry_run' == 'true'
state_dir = '$AMEM_STATE_DIR'

def llm_call(prompt, model=model):
    payload = json.dumps({
        'model': model,
        'prompt': prompt,
        'stream': False,
        'options': {'temperature': 0.3, 'num_predict': 800}
    }).encode()
    req = urllib.request.Request(
        f'{endpoint}/api/generate',
        data=payload,
        headers={'Content-Type': 'application/json'}
    )
    try:
        resp = urllib.request.urlopen(req, timeout=30)
        data = json.loads(resp.read().decode())
        return data.get('response', '').strip()
    except:
        return ''

def qmd_vsearch(query, limit=5):
    try:
        cmd = ['qmd', 'vsearch', query, '--json']
        if collection:
            cmd.extend(['-c', collection])
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        if result.returncode == 0 and result.stdout.strip():
            data = json.loads(result.stdout)
            if isinstance(data, list):
                return data[:limit]
            elif isinstance(data, dict):
                return data.get('results', [])[:limit]
        return []
    except:
        return []

def qmd_ls(collection_name=''):
    try:
        cmd = ['qmd', 'ls']
        if collection_name:
            cmd.append(collection_name)
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            return [line.strip() for line in result.stdout.strip().split('\n') if line.strip()]
        return []
    except:
        return []

# 1. Load all memories
files = qmd_ls(collection)
if not files:
    print(json.dumps({'status': 'empty', 'message': 'No memories found', 'changes': []}))
    sys.exit(0)

# 2. For each memory, find connections
suggestions = []
analyzed = 0
max_analyze = 50  # Cap to avoid timeout

for file_path in files[:max_analyze]:
    analyzed += 1
    # Get the file content snippet
    try:
        cmd = ['qmd', 'get', file_path]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        if result.returncode != 0 or not result.stdout.strip():
            continue
        content = result.stdout.strip()[:500]
    except:
        continue

    # Find related memories
    related = qmd_vsearch(content[:200])
    if not related:
        continue

    related_summaries = []
    for r in related[:3]:
        r_content = r.get('content', r.get('text', str(r)))[:150]
        r_path = r.get('path', r.get('source', ''))
        related_summaries.append(f'- {r_path}: {r_content}')

    if not related_summaries:
        continue

    # 3. Ask LLM for reorganization suggestions
    prompt = f'''Analyze these connected memories and suggest actions.

Current memory ({file_path}):
{content[:300]}

Related memories:
{chr(10).join(related_summaries)}

For each suggestion return valid JSON with:
- \"action\": one of [\"merge\", \"split\", \"retag\", \"link\", \"none\"]
- \"target\": file path of related memory (if applicable)
- \"reason\": brief explanation

Return a JSON array of suggestions. If no action needed, return [].
'''
    raw = llm_call(prompt)
    try:
        start = raw.find('[')
        end = raw.rfind(']') + 1
        if start >= 0 and end > start:
            file_suggestions = json.loads(raw[start:end])
            if isinstance(file_suggestions, list):
                for s in file_suggestions:
                    if isinstance(s, dict) and s.get('action', 'none') != 'none':
                        s['source'] = file_path
                        suggestions.append(s)
    except (json.JSONDecodeError, ValueError):
        pass

# 4. Log all changes for audit
timestamp = datetime.now(timezone.utc).isoformat()
log_entry = {
    'timestamp': timestamp,
    'action': 'reorganize',
    'analyzed': analyzed,
    'suggestions': len(suggestions),
    'dry_run': dry_run
}

log_path = os.path.join(state_dir, 'amem-audit.log')
try:
    with open(log_path, 'a') as f:
        f.write(json.dumps(log_entry) + '\n')
except:
    pass

result = {
    'status': 'success',
    'analyzed': analyzed,
    'total_files': len(files),
    'suggestions': suggestions,
    'suggestion_count': len(suggestions),
    'dry_run': dry_run,
    'model': model,
    'timestamp': timestamp
}

if dry_run:
    result['note'] = 'Dry run — no changes applied. Set AMEM_DRY_RUN=false to apply.'

print(json.dumps(result, indent=2))
" 2>/dev/null
}
