#!/usr/bin/env python3
"""
Save ModelShow results to both MD and JSON formats with full model names.
Version: 1.0.1
"""

import sys
import json
import os
from pathlib import Path
from datetime import datetime

def load_model_aliases():
    """Load model alias mapping from openclaw.json"""
    config_path = Path.home() / '.openclaw' / 'openclaw.json'
    if not config_path.exists():
        return {}
    
    try:
        with open(config_path, 'r') as f:
            data = json.load(f)
        
        models = data.get('agents', {}).get('defaults', {}).get('models', {})
        alias_map = {}
        
        # Build alias -> full name mapping
        for full_name, config in models.items():
            alias = config.get('alias')
            if alias:
                alias_map[alias] = full_name
        
        # Also add short names (e.g., "claude-opus-4-6" -> full path)
        for full_name in models.keys():
            short = full_name.split('/')[-1]
            if short not in alias_map:
                alias_map[short] = full_name
        
        return alias_map
    except Exception as e:
        print(f"Warning: Could not load alias map: {e}", file=sys.stderr)
        return {}

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
    """Convert text to slug: first N words, lowercased, hyphenated."""
    words = text.strip().split()[:max_words]
    return '-'.join(w.lower().replace("'", "").replace('"', '') for w in words)

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
    
    import re
    for pattern in patterns:
        match = re.search(pattern, judge_output, re.IGNORECASE | re.DOTALL)
        if match:
            section = match.group(1).strip()
            if len(section) > 50:  # sanity check — must be substantive
                return section
    
    # Fallback: return full output
    return judge_output


def save_json(data, output_path, slug=None, timestamp_str=None):
    """Save structured JSON for local use, custom dashboards, or web display with full model names."""
    # Compute table_view fields
    top_result = sorted(data['ranked_results'], key=lambda x: x['rank'])[0]
    total_duration_s = round(data.get('metadata', {}).get('total_duration_ms', 0) / 1000, 1)
    
    # Generate slug and timestamp if not provided
    if not slug:
        slug = slugify(data['prompt'])
    if not timestamp_str:
        timestamp_str = format_timestamp(data['timestamp'])
    
    # Extract holistic overall assessment for prominent display
    full_judge_output = data.get('deanonymized_judge_output', '')
    overall_assessment = extract_overall_assessment(full_judge_output)
    
    json_data = {
        "meta": {
            "timestamp": data['timestamp'],
            "prompt": data['prompt'],
            "models_queried": [resolve_model_name(m) for m in data['models']],
            "judge_model": resolve_model_name(data['judge_model']),
            "judging_mode": "blind"
        },
        "results": [
            {
                "rank": r['rank'],
                "model": resolve_model_name(r['model']),
                "model_alias": r['model'],  # Keep alias for reference
                "score": r['score'],
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
            "id": f"{slug}-{timestamp_str}",
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

def main():
    try:
        # Read JSON from stdin
        input_data = sys.stdin.read()
        data = json.loads(input_data)
        
        # Validate required fields
        required = ['prompt', 'timestamp', 'models', 'judge_model', 'ranked_results']
        missing = [f for f in required if f not in data]
        if missing:
            print(json.dumps({
                "success": False,
                "error": f"Missing required fields: {', '.join(missing)}"
            }))
            sys.exit(1)
        
        # Expand output directory (handle ~). Default from config; common: modelshow-results or modelshow-private.
        output_dir = Path(data.get('output_dir', '~/.openclaw/workspace/modelshow-results')).expanduser()
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate filename
        slug = slugify(data['prompt'])
        timestamp_str = format_timestamp(data['timestamp'])
        base_name = f"{slug}-{timestamp_str}"
        
        md_path = output_dir / f"{base_name}.md"
        json_path = output_dir / f"{base_name}.json"
        
        # Save both formats
        saved_md = save_markdown(data, md_path)
        saved_json = save_json(data, json_path, slug, timestamp_str)
        
        # Return success with paths
        result = {
            "success": True,
            "md_path": str(saved_md),
            "json_path": str(saved_json),
            "slug": slug
        }
        print(json.dumps(result, indent=2))
        
    except json.JSONDecodeError as e:
        print(json.dumps({
            "success": False,
            "error": f"Invalid JSON input: {str(e)}"
        }))
        sys.exit(1)
    except Exception as e:
        print(json.dumps({
            "success": False,
            "error": f"Unexpected error: {str(e)}"
        }))
        sys.exit(1)

if __name__ == '__main__':
    main()
