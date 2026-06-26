#!/usr/bin/env python3
"""
Memory Gardener v2 — Improved entity extraction + consolidation.

Improvements over v1:
1. Deduplication: merges events into existing entity files instead of duplicating
2. Better entity types: "Greptile" is a tool, not a person
3. Facts section: persistent facts separated from timeline
4. Cross-references: bidirectional wikilinks
5. Consolidation: MEMORY.md auto-update from high-surprise items
6. Multi-agent support: reads from configurable workspace path

Usage:
    python3 gardener-improved.py                    # Process today
    python3 gardener-improved.py --all              # Process all daily files
    python3 gardener-improved.py --date 2026-02-16  # Specific date
    python3 gardener-improved.py --surprise         # Surprise scoring
    python3 gardener-improved.py --consolidate      # Update MEMORY.md from entities
"""

import json
import os
import sys
import glob
import re
import urllib.request
from datetime import datetime, date
from pathlib import Path

from .filelock import file_lock, safe_write, safe_append
from .conflicts import detect_conflict, log_conflict, resolve_conflict, Conflict

# Configuration — each agent sets its own workspace
WORKSPACE = Path(os.environ.get("GARDENER_WORKSPACE", "/root/clawd"))
MEMORY_DIR = WORKSPACE / "memory"
ENTITIES_DIR = MEMORY_DIR / "entities"
GRAPH_FILE = MEMORY_DIR / "graph.jsonl"
MEMORY_FILE = WORKSPACE / "MEMORY.md"
SURPRISE_FILE = MEMORY_DIR / "surprise-scores.jsonl"

ENTITIES_DIR.mkdir(parents=True, exist_ok=True)

API_KEY = os.environ.get("GEMINI_API_KEY", "")
API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

EXTRACT_PROMPT = """Extract structured knowledge from this daily log. Output ONLY valid JSON.

{
  "entities": [
    {
      "name": "canonical name",
      "type": "person|company|project|tool|concept|role",
      "facts": ["permanent fact 1", "permanent fact 2"],
      "summary": "one-line description"
    }
  ],
  "triplets": [
    {"subject": "Entity1", "predicate": "verb_phrase", "object": "Entity2", "detail": "context", "confidence": 0.9}
  ],
  "events": [
    {"description": "what happened", "entities": ["Entity1"], "significance": "low|medium|high"}
  ]
}

Rules:
- Canonical names: "Marcus" (not "Marcus Widing"), "OpenClaw" (not "openclaw/openclaw")
- Types: tools like Greptile/GitHub are "tool", not "person"
- Facts = permanent truths ("CTO of Sana Labs", "195k stars"). Events = temporal ("submitted PR on Feb 16")
- Predicates: active verbs ("submitted_pr", "applied_to", "contacted", "works_at", "merged")
- Skip low-significance routine items (heartbeats, status checks)
- Only medium/high significance events

DAILY LOG ({date}):
{content}
"""

SURPRISE_PROMPT = """Compare what an agent's long-term memory says vs what actually happened today.
Rate surprise 0.0-1.0 (0 = totally expected, 1 = completely unexpected).

Output JSON:
{{
  "surprises": [
    {{"event": "description", "surprise_score": 0.0-1.0, "reason": "why unexpected"}}
  ]
}}

Only include events with surprise_score > 0.3.

MEMORY (world model):
{memory}

TODAY'S LOG:
{today}
"""

CONSOLIDATE_PROMPT = """Review these entity files and identify the most important facts and events
that should be in long-term memory (MEMORY.md).

Output a markdown section to APPEND to MEMORY.md. Format:
## Entity Updates ({date})
- **EntityName**: key fact or event
- **EntityName**: key fact or event

Only include genuinely important, long-term-relevant information.
Skip routine events.

ENTITY FILES:
{entities}
"""


def call_gemini(prompt: str) -> dict | None:
    """Call Gemini Flash API and parse JSON response."""
    if not API_KEY:
        print("No GEMINI_API_KEY set", file=sys.stderr)
        return None
    
    url = f"{API_URL}?key={API_KEY}"
    payload = json.dumps({
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.1, "responseMimeType": "application/json"}
    })
    
    try:
        req = urllib.request.Request(url, data=payload.encode(),
                                    headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=120) as resp:
            data = json.loads(resp.read())
            text = data["candidates"][0]["content"]["parts"][0]["text"]
            return json.loads(text)
    except Exception as e:
        print(f"API call failed: {e}", file=sys.stderr)
        # Try to extract JSON from text if mime type didn't work
        try:
            text = data["candidates"][0]["content"]["parts"][0]["text"]
            return extract_json_from_text(text)
        except:
            return None


def extract_json_from_text(text: str) -> dict | None:
    """Extract JSON from text that might have markdown fences."""
    text = text.strip()
    # Remove markdown code fences
    if text.startswith("```"):
        text = re.sub(r'^```(?:json)?\s*\n?', '', text)
        text = re.sub(r'\n?```\s*$', '', text)
    try:
        return json.loads(text)
    except:
        # Try to find JSON object in text
        match = re.search(r'\{[\s\S]*\}', text)
        if match:
            try:
                return json.loads(match.group())
            except:
                pass
    return None


def read_daily_file(date_str: str) -> str:
    """Read a daily memory file."""
    path = MEMORY_DIR / f"{date_str}.md"
    if path.exists():
        return path.read_text()
    return ""


def sanitize_filename(name: str) -> str:
    """Convert entity name to safe filename."""
    return re.sub(r'[^\w\s-]', '', name).strip().replace(' ', '-')


def read_entity_file(name: str) -> str:
    """Read existing entity file if it exists."""
    path = ENTITIES_DIR / f"{sanitize_filename(name)}.md"
    if path.exists():
        return path.read_text()
    return ""


def update_entity_file(name: str, entity_type: str, facts: list, 
                       date_str: str, events: list, triplets: list):
    """Create or update an entity wiki page with deduplication."""
    filename = sanitize_filename(name)
    filepath = ENTITIES_DIR / f"{filename}.md"
    existing = filepath.read_text() if filepath.exists() else ""
    
    # Check if this date already processed (dedup)
    if f"### [[{date_str}]]" in existing:
        return  # Already processed this date
    
    if existing:
        # Append new timeline entry
        lines = existing.rstrip().split('\n')
        
        # Add new facts if not already present
        for fact in facts:
            if fact not in existing:
                # Find Facts section and append
                for i, line in enumerate(lines):
                    if line.startswith('## Facts'):
                        # Find next section or end
                        insert_at = i + 1
                        while insert_at < len(lines) and not lines[insert_at].startswith('## '):
                            insert_at += 1
                        lines.insert(insert_at, f"- {fact}")
                        break
        
        # Add timeline entry
        timeline_entry = f"\n### [[{date_str}]]"
        for event in events:
            if any(name.lower() in e.lower() for e in event.get("entities", [])):
                timeline_entry += f"\n- {event['description']}"
        
        for triplet in triplets:
            if triplet["subject"] == name:
                timeline_entry += f"\n- {triplet['predicate']} → [[{triplet['object']}]]: {triplet['detail']}"
            elif triplet["object"] == name:
                timeline_entry += f"\n- [[{triplet['subject']}]] {triplet['predicate']} → this: {triplet['detail']}"
        
        if timeline_entry.count('\n') > 1:  # Has content beyond header
            content = '\n'.join(lines) + timeline_entry + '\n'
            safe_write(filepath, content)
            print(f"  Updated: {filename}.md")
    else:
        # Create new entity file
        content = f"# {name}\n**Type:** {entity_type}\n\n"
        
        if facts:
            content += "## Facts\n"
            for fact in facts:
                content += f"- {fact}\n"
            content += "\n"
        
        content += "## Timeline\n"
        content += f"\n### [[{date_str}]]\n"
        
        for event in events:
            if any(name.lower() in e.lower() for e in event.get("entities", [])):
                content += f"- {event['description']}\n"
        
        for triplet in triplets:
            if triplet["subject"] == name:
                content += f"- {triplet['predicate']} → [[{triplet['object']}]]: {triplet['detail']}\n"
            elif triplet["object"] == name:
                content += f"- [[{triplet['subject']}]] {triplet['predicate']} → this: {triplet['detail']}\n"
        
        content += "\n## Relations\n"
        related = set()
        for triplet in triplets:
            if triplet["subject"] == name:
                related.add(triplet["object"])
            elif triplet["object"] == name:
                related.add(triplet["subject"])
        for r in sorted(related):
            content += f"- [[{r}]]\n"
        
        safe_write(filepath, content)
        print(f"  Created: {filename}.md")


def append_to_graph(
    triplets: list, 
    date_str: str, 
    provenance: dict = None,
    conflict_strategy: str = "latest_wins",
    conflicts_file: Path = None,
):
    """Append triplets to graph.jsonl with dedup, provenance, and conflict detection.
    
    Args:
        triplets: List of triplet dicts with subject, predicate, object, detail
        date_str: Date string (YYYY-MM-DD)
        provenance: Optional dict with source, agent, confidence fields
        conflict_strategy: How to resolve conflicts (latest_wins, confidence_wins, keep_both)
        conflicts_file: Path to conflicts.md (default: memory/conflicts.md)
    """
    if conflicts_file is None:
        conflicts_file = MEMORY_DIR / "conflicts.md"
    
    existing = set()
    if GRAPH_FILE.exists():
        for line in GRAPH_FILE.read_text().strip().split('\n'):
            if line:
                try:
                    t = json.loads(line)
                    existing.add((t.get("date"), t.get("subject"), t.get("predicate"), t.get("object")))
                except:
                    pass
    
    # Build default provenance if not provided
    if provenance is None:
        provenance = {}
    default_provenance = {
        "source": provenance.get("source", f"file:memory/{date_str}.md"),
        "agent": provenance.get("agent", os.environ.get("AGENT_ID", "unknown")),
        "confidence": provenance.get("confidence", 0.8),
        "timestamp": datetime.now().isoformat(),
    }
    
    new_count = 0
    conflict_count = 0
    
    with file_lock(GRAPH_FILE):
        with open(GRAPH_FILE, "a") as f:
            for t in triplets:
                key = (date_str, t["subject"], t["predicate"], t["object"])
                if key not in existing:
                    triplet_provenance = {
                        **default_provenance,
                        "confidence": t.pop("confidence", default_provenance["confidence"]),
                    }
                    
                    # Check for conflicts with existing facts
                    conflict = detect_conflict(GRAPH_FILE, t, triplet_provenance)
                    if conflict:
                        conflict_count += 1
                        print(f"  ⚠️ Conflict detected: {conflict.subject} {conflict.predicate}")
                        print(f"     Old: {conflict.old_value}")
                        print(f"     New: {conflict.new_value}")
                        
                        # Log conflict for human review
                        log_conflict(conflicts_file, conflict)
                        
                        # Resolve based on strategy
                        resolved = resolve_conflict(conflict, conflict_strategy)
                        if resolved.get("conflicted"):
                            t["conflicted"] = True
                            t["alternative"] = resolved.get("alternative")
                    
                    t["date"] = date_str
                    t["provenance"] = triplet_provenance
                    f.write(json.dumps(t) + "\n")
                    new_count += 1
    
    if new_count:
        msg = f"  Added {new_count} new triplets to graph.jsonl"
        if conflict_count:
            msg += f" ({conflict_count} conflicts detected, logged to conflicts.md)"
        msg += f" (provenance: {default_provenance['source']})"
        print(msg)


MAX_CHUNK_SIZE = int(os.environ.get("ENGRAM_MAX_CHUNK", "6000"))


def chunk_content(content: str, max_size: int = MAX_CHUNK_SIZE) -> list[str]:
    """Split large content into chunks, breaking at section boundaries."""
    if len(content) <= max_size:
        return [content]
    
    chunks = []
    # Try to split at ## headers first
    sections = re.split(r'(?=^## )', content, flags=re.MULTILINE)
    
    current = ""
    for section in sections:
        if len(current) + len(section) > max_size and current:
            chunks.append(current.strip())
            current = section
        else:
            current += section
    if current.strip():
        chunks.append(current.strip())
    
    # If any chunk is still too big, split at paragraphs
    final_chunks = []
    for chunk in chunks:
        if len(chunk) <= max_size:
            final_chunks.append(chunk)
        else:
            paragraphs = chunk.split("\n\n")
            sub = ""
            for para in paragraphs:
                if len(sub) + len(para) > max_size and sub:
                    final_chunks.append(sub.strip())
                    sub = para
                else:
                    sub += "\n\n" + para
            if sub.strip():
                final_chunks.append(sub.strip())
    
    return final_chunks if final_chunks else [content[:max_size]]


def pre_filter(content: str) -> str:
    """Remove low-signal sections (raw logs, code blocks, repeated output)."""
    lines = content.split("\n")
    filtered = []
    in_code_block = False
    code_block_lines = 0
    
    for line in lines:
        if line.startswith("```"):
            in_code_block = not in_code_block
            code_block_lines = 0
            if not in_code_block and code_block_lines > 20:
                filtered.append("```\n[... code block truncated ...]\n```")
            continue
        
        if in_code_block:
            code_block_lines += 1
            if code_block_lines <= 5:  # Keep first 5 lines of code
                filtered.append(line)
            continue
        
        # Skip repetitive log lines
        if re.match(r'^\s*(HEARTBEAT_OK|NO_REPLY|\d{2}:\d{2}:\d{2}.*DEBUG)', line):
            continue
        
        filtered.append(line)
    
    return "\n".join(filtered)


def merge_extraction_results(results: list[dict]) -> dict:
    """Merge multiple chunk extraction results, deduplicating entities."""
    all_entities = {}
    all_triplets = []
    all_events = []
    seen_triplets = set()
    
    for result in results:
        for entity in result.get("entities", []):
            name = entity["name"]
            if name in all_entities:
                # Merge facts
                existing_facts = set(all_entities[name].get("facts", []))
                new_facts = entity.get("facts", [])
                all_entities[name]["facts"] = list(existing_facts | set(new_facts))
            else:
                all_entities[name] = entity
        
        for triplet in result.get("triplets", []):
            key = (triplet["subject"], triplet["predicate"], triplet["object"])
            if key not in seen_triplets:
                seen_triplets.add(key)
                all_triplets.append(triplet)
        
        all_events.extend(result.get("events", []))
    
    return {
        "entities": list(all_entities.values()),
        "triplets": all_triplets,
        "events": all_events,
    }


def process_date(date_str: str):
    """Process a daily file: extract entities, triplets, events.
    
    Handles large files by chunking and merging results.
    """
    print(f"\nProcessing {date_str}...")
    content = read_daily_file(date_str)
    if not content:
        print(f"  No daily file for {date_str}")
        return
    
    # Pre-filter to remove noise
    content = pre_filter(content)
    
    # Chunk if needed
    chunks = chunk_content(content)
    if len(chunks) > 1:
        print(f"  Large file: splitting into {len(chunks)} chunks")
    
    # Extract from each chunk
    results = []
    for i, chunk in enumerate(chunks):
        if len(chunks) > 1:
            print(f"  Processing chunk {i+1}/{len(chunks)}...")
        prompt = EXTRACT_PROMPT.replace("{date}", date_str).replace("{content}", chunk)
        result = call_gemini(prompt)
        if result:
            results.append(result)
    
    if not results:
        print(f"  Failed to get LLM response")
        return
    
    # Merge results from all chunks
    merged = merge_extraction_results(results) if len(results) > 1 else results[0]
    
    entities = merged.get("entities", [])
    triplets = merged.get("triplets", [])
    events = merged.get("events", [])
    
    print(f"  Extracted: {len(entities)} entities, {len(triplets)} triplets, {len(events)} events")
    
    for entity in entities:
        update_entity_file(
            entity["name"],
            entity.get("type", "unknown"),
            entity.get("facts", []),
            date_str, events, triplets
        )
    
    if triplets:
        # Add provenance metadata
        provenance = {
            "source": f"file:memory/{date_str}.md",
            "agent": os.environ.get("AGENT_ID", "unknown"),
            "confidence": 0.8,  # Default confidence for LLM extraction
        }
        append_to_graph(triplets, date_str, provenance=provenance)


def run_surprise(date_str: str):
    """Run surprise scoring."""
    memory = MEMORY_FILE.read_text()[:3000] if MEMORY_FILE.exists() else ""
    today = read_daily_file(date_str)
    if not today:
        print(f"No daily file for {date_str}")
        return
    
    prompt = SURPRISE_PROMPT.replace("{memory}", memory).replace("{today}", today)
    result = call_gemini(prompt)
    
    if result and result.get("surprises"):
        print(f"\n🎯 Surprise scoring for {date_str}:")
        for s in result["surprises"]:
            score = s.get("surprise_score", 0)
            emoji = "🔴" if score > 0.7 else "🟡" if score > 0.5 else "🟢"
            print(f"  {emoji} [{score:.1f}] {s['event']}")
            print(f"       {s['reason']}")
        
        with file_lock(SURPRISE_FILE):
            with open(SURPRISE_FILE, "a") as f:
                for s in result["surprises"]:
                    s["date"] = date_str
                    s["timestamp"] = datetime.now().isoformat()
                    f.write(json.dumps(s) + "\n")
    else:
        print(f"No surprises for {date_str}")


def run_consolidate():
    """Auto-update MEMORY.md from entity files."""
    entity_content = ""
    for f in sorted(ENTITIES_DIR.glob("*.md")):
        entity_content += f.read_text() + "\n---\n"
    
    if not entity_content:
        print("No entity files to consolidate")
        return
    
    today = date.today().isoformat()
    prompt = CONSOLIDATE_PROMPT.replace("{date}", today).replace("{entities}", entity_content[:8000])
    result = call_gemini(prompt)
    
    if result:
        # Result might be raw text, not JSON
        update_text = result if isinstance(result, str) else json.dumps(result, indent=2)
        with file_lock(MEMORY_FILE):
            with open(MEMORY_FILE, "a") as f:
                f.write(f"\n\n{update_text}\n")
        print(f"MEMORY.md updated with consolidation from {today}")


def main():
    args = sys.argv[1:]
    
    if "--surprise" in args:
        date_str = date.today().isoformat()
        if "--date" in args:
            idx = args.index("--date")
            date_str = args[idx + 1]
        run_surprise(date_str)
    elif "--consolidate" in args:
        run_consolidate()
    elif "--all" in args:
        files = sorted(glob.glob(str(MEMORY_DIR / "2026-*.md")))
        for f in files:
            date_str = Path(f).stem
            if re.match(r'^\d{4}-\d{2}-\d{2}$', date_str):
                process_date(date_str)
    elif "--date" in args:
        idx = args.index("--date")
        process_date(args[idx + 1])
    else:
        process_date(date.today().isoformat())


if __name__ == "__main__":
    main()
