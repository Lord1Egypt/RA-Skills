#!/usr/bin/env python3
"""YAML frontmatter validator for KG notes.

Usage:
    python yaml-validator.py <file.md>

Exit codes:
    0 - valid (prints YAML_VALID)
    1 - invalid (prints YAML_ERRORS + details)

Checks:
    - Opening/closing ---
    - tags field present
    - abstract field required for 概念/某物/skill
    - name+version required for skill
    关系 notes: no abstract, single line only
    type field forbidden (use tags)
    [[ links in frontmatter forbidden
    Non-empty body
    Agent memory: forbid type/[[links/related_fragments, require summary
"""
import re, sys, os


def normalize_path(p: str) -> str:
    """Handle Git Bash /d/ style paths on Windows."""
    p = p.strip()
    m = re.match(r'^/([a-zA-Z])/(.*)', p)
    if m and os.name == 'nt':
        p = f"{m.group(1).upper()}:/{m.group(2)}"
    return os.path.abspath(p)


def validate(filepath: str) -> list[str]:
    errors = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            raw = f.read()
    except FileNotFoundError:
        errors.append(f"NOT_FOUND: {filepath}")
        return errors
    except Exception as e:
        errors.append(f"READ_ERROR: {e}")
        return errors

    if not raw.startswith('---'):
        errors.append(f"MISSING_OPEN: file does not start with '---'")
        return errors

    # Find closing --- in raw directly (avoids lstrip offset bug)
    close_idx = raw.find('\n---', 3)  # skip first --- at pos 0-2
    if close_idx == -1:
        errors.append(f"MISSING_CLOSE: frontmatter has no closing '---'")
        return errors

    yaml_block = raw[3:close_idx].strip()
    if not yaml_block:
        errors.append(f"EMPTY: frontmatter is empty")
        return errors

    # Parse YAML lines into dict
    fields = {}
    for line in yaml_block.split('\n'):
        m = re.match(r'^(\w[\w_-]*)\s*:\s*(.*)', line)
        if m:
            fields[m.group(1)] = m.group(2).strip()

    # Detect note type from tags
    note_type = None
    raw_tags = fields.get('tags', '')
    tag_match = re.match(r'\[?\s*(\S+?)\s*\]?', raw_tags)
    if tag_match:
        note_type = tag_match.group(1)

    # Check agent memory fragments
    is_agent_memory = filepath.replace('\\', '/').find('/agent memory/') != -1
    if is_agent_memory:
        if 'type' in fields:
            errors.append(f"AGENT_MEM_FORBIDDEN_type: agent memory has 'type:' (use 'tags:' instead)")
        if '[[' in yaml_block:
            errors.append(f"AGENT_MEM_FORBIDDEN_links: agent memory frontmatter has '[[ ]]' (use plain text)")
        if 'related_fragments' in fields:
            errors.append(f"AGENT_MEM_FORBIDDEN_related_fragments: agent memory has 'related_fragments' (use 'project:' grouping)")
        if 'summary' not in fields:
            errors.append(f"AGENT_MEM_MISSING_summary: agent memory needs 'summary:' field")

    # General checks
    if 'tag' in fields and 'tags' not in fields:
        errors.append(f"TAG_VS_TAGS: frontmatter has 'tag:' — did you mean 'tags:'? (common typo: missing 's')")
    if not fields.get('tags'):
        if not any('TAG_VS_TAGS' in e for e in errors):
            errors.append(f"MISSING_TAGS: no 'tags:' field")

    if 'type' in fields and not is_agent_memory:
        errors.append(f"FORBIDDEN_TYPE: has 'type:' (use 'tags:' instead)")

    if '[[' in yaml_block:
        errors.append(f"FORBIDDEN_LINKS_IN_FM: frontmatter has '[[ ]]' in YAML")

    # Type-specific checks
    if note_type in ('概念', '某物', 'skill') and not fields.get('abstract'):
        errors.append(f"MISSING_ABSTRACT: {note_type} note needs 'abstract:' field")

    if note_type == 'skill':
        if not fields.get('name'):
            errors.append(f"MISSING_NAME: skill note needs 'name:' field")
        if not fields.get('version'):
            errors.append(f"MISSING_VERSION: skill note needs 'version:' field")

    if note_type == '关系':
        if fields.get('abstract'):
            errors.append(f"FORBIDDEN_ABSTRACT: relation note should not have 'abstract:'")
        if len(fields) > 1:
            errors.append(f"EXTRA_FIELDS: relation note should only have 'tags: [关系]'")

    # Body check: use raw position directly, no offset accumulation
    body_start = close_idx + 5  # skip \n---\n
    body_raw = raw[body_start:]
    body = body_raw.strip()
    if not body:
        errors.append(f"EMPTY_BODY: no content after frontmatter")
    else:
        # Check for stray trailing --- (extra frontmatter delimiter)
        if any(line.strip() == '---' for line in body_raw.split('\n')):
            errors.append(f"STRAY_FM_CLOSE: body contains '---' (stray frontmatter delimiter in content area)")

    return errors


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("USAGE: python yaml-validator.py <file.md>", file=sys.stderr)
        sys.exit(1)

    path = normalize_path(sys.argv[1])
    errors = validate(path)
    if errors:
        basename = os.path.basename(path)
        print("YAML_ERRORS")
        for e in errors:
            print(f"  [{basename}] {e}")
        sys.exit(1)
    else:
        print("YAML_VALID")
        sys.exit(0)
