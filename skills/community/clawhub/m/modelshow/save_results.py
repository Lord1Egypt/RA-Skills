#!/usr/bin/env python3
"""
Save ModelShow results to both MD and JSON formats with full model names.
Version: 1.2.0

Security notes:
  - Uses only the Python standard library; makes no network calls.
  - The payload is parsed strictly as JSON data — nothing in it is executed.
  - Filenames are built from a sanitized slug ([a-z0-9-] only) so a crafted
    prompt can never inject path separators or traversal sequences.
  - Writes are confined to the resolved output_dir (defense-in-depth check).
  - ~/.openclaw/openclaw.json is read ONLY to map model aliases to full model
    names; no other keys are read, and nothing from it is logged or emitted
    beyond the resolved model names.
"""

import sys
import json
import os
import re
from pathlib import Path
from datetime import datetime

# Hard cap on payload size — a runaway payload should fail loudly, not OOM.
MAX_PAYLOAD_BYTES = 64 * 1024 * 1024

_alias_cache = None


def load_model_aliases():
    """Load model alias mapping from openclaw.json (cached per process)."""
    global _alias_cache
    if _alias_cache is not None:
        return _alias_cache

    config_path = Path.home() / '.openclaw' / 'openclaw.json'
    if not config_path.exists():
        _alias_cache = {}
        return _alias_cache

    try:
        with open(config_path, 'r') as f:
            data = json.load(f)

        models = data.get('agents', {}).get('defaults', {}).get('models', {})
        alias_map = {}

        # Build alias -> full name mapping
        for full_name, config in models.items():
            if not isinstance(config, dict):
                continue
            alias = config.get('alias')
            if alias:
                alias_map[alias] = full_name

        # Also add short names (e.g., "claude-opus-4-6" -> full path)
        for full_name in models.keys():
            short = full_name.split('/')[-1]
            if short not in alias_map:
                alias_map[short] = full_name

        _alias_cache = alias_map
    except Exception as e:
        # Never fail (or leak config content) over the alias map — it is cosmetic.
        print(f"Warning: Could not load alias map: {e}", file=sys.stderr)
        _alias_cache = {}
    return _alias_cache

def resolve_model_name(alias):
    """Convert alias to full model name, with fuzzy matching"""
    alias_map = load_model_aliases()

    # Direct match
    if alias in alias_map:
        return alias_map[alias]

    # Check if it's already a full name
    if '/' in alias:
        return alias

    # Fuzzy match: find model ending with this alias
    for full_name in alias_map.values():
        if full_name.endswith(f"/{alias}") or full_name.endswith(f"-{alias}"):
            return full_name
        # Also check if short name matches (e.g., "opus" matches "claude-opus-4-6")
        short = full_name.split('/')[-1]
        if alias in short or short.startswith(alias):
            return full_name

    # No match found, return alias as-is
    return alias

def slugify(text, max_words=5):
    """Convert text to a filesystem-safe slug: first N words, lowercased, hyphenated.

    Strips everything except [a-z0-9-] so a crafted prompt can never inject path
    separators (``/``, ``\\``) or traversal sequences (``..``) into the filename.
    """
    words = text.strip().split()[:max_words]
    raw = '-'.join(words).lower()
    slug = re.sub(r'[^a-z0-9]+', '-', raw).strip('-')
    return slug or 'result'

def format_timestamp(iso_string):
    """Convert ISO timestamp to YYYY-MM-DD-HHMM format."""
    dt = datetime.fromisoformat(iso_string.replace('Z', '+00:00'))
    return dt.strftime('%Y-%m-%d-%H%M')

def get_medal(rank):
    """Return medal emoji for rank."""
    medals = {1: '🏆', 2: '🥈', 3: '🥉'}
    return medals.get(rank, '')

def save_markdown(data, output_path):
    """Generate and save markdown report with full model names."""
    md = []
    md.append("# ModelShow Results")
    md.append(f"**Date:** {data['timestamp']}")
    md.append(f"**Prompt:** {data['prompt']}")

    # Convert model aliases to full names
    full_model_names = [resolve_model_name(m) for m in data['models']]
    md.append(f"**Models:** {', '.join(full_model_names)}")
    md.append(f"**Judge:** {resolve_model_name(data['judge_model'])}")
    md.append(f"**Judging Mode:** Blind (model identities hidden from judge)")
    md.append("")
    md.append("---")
    md.append("")

    # Rankings section
    md.append("## Rankings")
    md.append("")

    for result in sorted(data['ranked_results'], key=lambda x: x['rank']):
        medal = get_medal(result['rank'])
        full_name = resolve_model_name(result['model'])
        md.append(f"### {medal} **{full_name}** — {result['score']}/10")
        md.append("")
        criteria_scores = result.get('criteria_scores') or {}
        if criteria_scores:
            parts = ', '.join(f"{k}: {v}" for k, v in criteria_scores.items())
            md.append(f"**Criteria:** {parts}")
            md.append("")
        md.append("**Judge's Assessment:**")
        md.append(result.get('judge_notes', '(No notes available)'))
        md.append("")
        md.append("**Full Response:**")
        md.append(result.get('response_text', '(No response text available)'))
        md.append("")
        md.append("---")
        md.append("")

    # Full judge analysis (with full names substituted)
    md.append("## Judge's Overall Assessment")
    md.append("")
    judge_output = data.get('deanonymized_judge_output', '(No analysis available)')
    # Replace aliases with full names in judge output
    for alias in data['models']:
        full_name = resolve_model_name(alias)
        if full_name != alias:
            judge_output = judge_output.replace(f"**{alias}**", f"**{full_name}**")
    md.append(judge_output)
    md.append("")
    md.append("---")
    md.append("")

    # Anonymization key (audit trail) - show both alias and full name
    md.append("## Blind Judging Key (Audit)")
    md.append("")
    for placeholder, alias in data.get('anonymization_map', {}).items():
        full_name = resolve_model_name(alias)
        md.append(f"- {placeholder} → {full_name}")
    md.append("")
    md.append("---")
    md.append("")

    # Metadata
    meta = data.get('metadata', {})
    md.append("## Metadata")
    md.append("")
    md.append(f"- **Total Duration:** {meta.get('total_duration_ms', 0) / 1000:.1f}s")
    md.append(f"- **Successful Models:** {meta.get('successful_models', len(data['ranked_results']))}")
    md.append(f"- **Failed Models:** {meta.get('failed_models', 0)}")
    if meta.get('timed_out_models'):
        md.append(f"- **Timed Out:** {', '.join(meta['timed_out_models'])}")
    md.append("")

    # Write file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(md))

    return output_path

def extract_overall_assessment(judge_output: str) -> str:
    """Extract only the 'Overall Assessment' section from the full judge output.

    The judge is instructed to write a holistic 'Overall Assessment' section
    that goes beyond per-result summaries. This extracts just that section
    for prominent display.

    Falls back to the full judge output if the section cannot be found.
    """
    if not judge_output:
        return ''

    # Look for the Overall Assessment / Overall Summary section
    patterns = [
        r'(?:###?\s*)?Overall\s+Assessment\s*\n+(.*?)(?=\n###|\n##|\Z)',
        r'(?:###?\s*)?Overall\s+Summary\s*\n+(.*?)(?=\n###|\n##|\Z)',
        r'(?:###?\s*)?Holistic\s+Analysis\s*\n+(.*?)(?=\n###|\n##|\Z)',
        r'(?:###?\s*)?Summary\s+&\s+Takeaways\s*\n+(.*?)(?=\n###|\n##|\Z)',
    ]

    for pattern in patterns:
        match = re.search(pattern, judge_output, re.IGNORECASE | re.DOTALL)
        if match:
            section = match.group(1).strip()
            if len(section) > 50:  # sanity check — must be substantive
                return section

    # Fallback: return full output
    return judge_output


def save_json(data, output_path, slug=None, timestamp_str=None, file_id=None):
    """Save structured JSON for local use, custom dashboards, or web display with full model names."""
    # Compute table_view fields
    top_result = sorted(data['ranked_results'], key=lambda x: x['rank'])[0]
    total_duration_s = round(data.get('metadata', {}).get('total_duration_ms', 0) / 1000, 1)

    # Generate slug and timestamp if not provided
    if not slug:
        slug = slugify(data['prompt'])
    if not timestamp_str:
        timestamp_str = format_timestamp(data['timestamp'])
    if not file_id:
        file_id = f"{slug}-{timestamp_str}"

    # Extract holistic overall assessment for prominent display
    full_judge_output = data.get('deanonymized_judge_output', '')
    overall_assessment = extract_overall_assessment(full_judge_output)

    json_data = {
        "meta": {
            "timestamp": data['timestamp'],
            "prompt": data['prompt'],
            "models_queried": [resolve_model_name(m) for m in data['models']],
            "judge_model": resolve_model_name(data['judge_model']),
            "judging_mode": "blind",
            "judge_criteria": data.get('judge_criteria', [])
        },
        "results": [
            {
                "rank": r['rank'],
                "model": resolve_model_name(r['model']),
                "model_alias": r['model'],  # Keep alias for reference
                "score": r['score'],
                # Optional per-criterion subscores, e.g. {"accuracy": 9, "clarity": 8}
                "criteria_scores": r.get('criteria_scores', {}),
                "response": r.get('response_text', ''),
                "assessment": r.get('judge_notes', '')
            }
            for r in sorted(data['ranked_results'], key=lambda x: x['rank'])
        ],
        "judge_analysis": overall_assessment,   # Holistic overall assessment for display
        "judge_analysis_full": full_judge_output,  # Full output including per-result rankings
        "anonymization_map": {
            k: resolve_model_name(v) for k, v in data.get('anonymization_map', {}).items()
        },
        "table_view": {
            "id": file_id,
            "timestamp": data['timestamp'],
            "prompt_preview": data['prompt'][:50] + ("..." if len(data['prompt']) > 50 else ""),
            "models_count": len(data['models']),
            "top_model": resolve_model_name(top_result['model']),
            "top_score": top_result['score'],
            "total_duration_seconds": total_duration_s,
            "judge_model": resolve_model_name(data['judge_model'])
        },
        "metadata": data.get('metadata', {})
    }

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, indent=2, ensure_ascii=False)

    return output_path

def read_payload():
    """Read the JSON payload from `--file PATH` if given, else from stdin.

    Reading from a file/stdin (instead of an inline shell `echo '...'`) keeps
    untrusted model/judge text off the command line — avoiding quote breakage
    and shell-injection risk.
    """
    argv = sys.argv[1:]
    if "--file" in argv:
        idx = argv.index("--file")
        if idx + 1 >= len(argv):
            raise ValueError("--file requires a path argument")
        path = argv[idx + 1]
        if not os.path.isfile(path):
            raise ValueError(f"--file path is not a regular file: {path}")
        if os.path.getsize(path) > MAX_PAYLOAD_BYTES:
            raise ValueError(f"payload exceeds size limit ({MAX_PAYLOAD_BYTES} bytes)")
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    text = sys.stdin.read(MAX_PAYLOAD_BYTES + 1)
    if len(text) > MAX_PAYLOAD_BYTES:
        raise ValueError(f"payload exceeds size limit ({MAX_PAYLOAD_BYTES} bytes)")
    return text

def fail(message):
    """Emit a machine-parseable failure and exit non-zero."""
    print(json.dumps({"success": False, "error": message}))
    sys.exit(1)

def validate_payload(data):
    """Check required fields and shapes, failing with an actionable message."""
    if not isinstance(data, dict):
        fail("Payload must be a JSON object")

    required = ['prompt', 'timestamp', 'models', 'judge_model', 'ranked_results']
    missing = [f for f in required if f not in data]
    if missing:
        fail(f"Missing required fields: {', '.join(missing)}")

    if not isinstance(data['prompt'], str) or not data['prompt'].strip():
        fail("'prompt' must be a non-empty string")

    if not isinstance(data['models'], list) or not all(isinstance(m, str) for m in data['models']):
        fail("'models' must be a list of model alias strings")

    ranked = data['ranked_results']
    if not isinstance(ranked, list) or not ranked:
        fail("'ranked_results' must be a non-empty list")
    for i, entry in enumerate(ranked):
        if not isinstance(entry, dict):
            fail(f"ranked_results[{i}] must be an object")
        needed = [k for k in ('rank', 'model', 'score') if k not in entry]
        if needed:
            fail(f"ranked_results[{i}] is missing: {', '.join(needed)}")

def main():
    try:
        input_data = read_payload()
        data = json.loads(input_data)

        validate_payload(data)

        try:
            timestamp_str = format_timestamp(data['timestamp'])
        except (ValueError, AttributeError, TypeError):
            fail("Invalid 'timestamp' — must be ISO 8601, e.g. 2026-07-10T12:00:00Z")

        # Expand + resolve output directory (handle ~ and relative paths).
        # Default from config; common: modelshow-results or modelshow-private.
        output_dir = Path(data.get('output_dir', '~/.openclaw/workspace/modelshow-results')).expanduser().resolve()
        output_dir.mkdir(parents=True, exist_ok=True)

        # Generate filename (slug is sanitized to [a-z0-9-] — no path traversal)
        slug = slugify(data['prompt'])
        base_name = f"{slug}-{timestamp_str}"

        md_path = output_dir / f"{base_name}.md"
        json_path = output_dir / f"{base_name}.json"

        # Never silently overwrite an earlier run from the same minute —
        # uniquify with a numeric suffix instead.
        counter = 2
        while md_path.exists() or json_path.exists():
            base_name = f"{slug}-{timestamp_str}-{counter}"
            md_path = output_dir / f"{base_name}.md"
            json_path = output_dir / f"{base_name}.json"
            counter += 1

        # Defense in depth: ensure the resolved paths stay inside output_dir
        for p in (md_path, json_path):
            if output_dir not in p.resolve().parents:
                fail("Refusing to write outside output_dir (path traversal blocked)")

        # Save both formats
        saved_md = save_markdown(data, md_path)
        saved_json = save_json(data, json_path, slug, timestamp_str, file_id=base_name)

        # Return success with paths
        result = {
            "success": True,
            "md_path": str(saved_md),
            "json_path": str(saved_json),
            "slug": slug
        }
        print(json.dumps(result, indent=2))

    except SystemExit:
        raise
    except json.JSONDecodeError as e:
        fail(f"Invalid JSON input: {str(e)}")
    except Exception as e:
        fail(f"Unexpected error: {str(e)}")

if __name__ == '__main__':
    main()
