#!/usr/bin/env python3
"""
Ontology to ExpertPack Converter

Converts OpenClaw ontology graph.jsonl + schema.yaml into a standards-compliant ExpertPack.
"""
import sys
import json
import yaml
import argparse
from collections import defaultdict
from pathlib import Path
from datetime import datetime
import re

def parse_graph(graph_path):
    """Replay append-only ops to build final entity and relation state."""
    entities = {}
    relations = []
    seen_ids = set()
    if not Path(graph_path).exists():
        print(f"Warning: Graph file {graph_path} not found. Creating empty pack.")
        return entities, relations

    with open(graph_path, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            try:
                op = json.loads(line)
                op_type = op.get('op')
                if op_type == 'create' or op_type == 'update':
                    entity = op.get('entity', {})
                    eid = entity.get('id')
                    if eid:
                        if eid in entities and op_type == 'update':
                            entities[eid]['properties'].update(entity.get('properties', {}))
                            if 'type' in entity:
                                entities[eid]['type'] = entity['type']
                        else:
                            entities[eid] = entity.copy()
                            entities[eid]['properties'] = entities[eid].get('properties', {})
                            seen_ids.add(eid)
                elif op_type == 'relate':
                    rel = {
                        'from': op.get('from'),
                        'rel': op.get('rel'),
                        'to': op.get('to')
                    }
                    relations.append(rel)
                elif op_type == 'delete':
                    did = op.get('entity', {}).get('id') or op.get('id')
                    if did and did in entities:
                        del entities[did]
            except json.JSONDecodeError:
                print(f"Warning: Malformed JSONL at line {line_num}: {line[:100]}")
                continue
    return entities, relations

def load_schema(schema_path):
    if not Path(schema_path).exists():
        return {}, {}
    with open(schema_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f) or {}

def sanitize_properties(props):
    """Strip sensitive credential-like properties."""
    sensitive = {'password', 'secret', 'token', 'key', 'credential', 'api_key', 'private_key'}
    cleaned = {}
    for k, v in props.items():
        if any(s in k.lower() for s in sensitive):
            continue
        cleaned[k] = v
    return cleaned

def detect_pack_type(entities):
    """Auto-detect pack type from entity distribution."""
    type_counts = defaultdict(int)
    for e in entities.values():
        t = e.get('type', 'Unknown')
        type_counts[t] += 1

    person_org = type_counts['Person'] + type_counts['Organization']
    project_task = type_counts['Project'] + type_counts['Task'] + type_counts['Goal']
    total = len(entities)

    if person_org > total * 0.6:
        return 'person'
    if project_task > total * 0.5:
        return 'process'
    if total > 0 and (project_task + type_counts['Document'] + type_counts['Note']) > total * 0.5:
        return 'product'
    return 'composite'

def map_to_directory(entity_type):
    """Map ontology type to ExpertPack directory."""
    mapping = {
        'Person': 'relationships',
        'Organization': 'relationships',
        'Project': 'workflows',
        'Task': 'workflows',
        'Goal': 'workflows',
        'Event': 'facts',
        'Location': 'facts',
        'Document': 'concepts',
        'Note': 'concepts',
        'Message': 'concepts',
        'Thread': 'concepts',
        'Account': 'operational',
        'Device': 'operational',
        'Credential': 'operational',
        'Action': 'governance',
        'Policy': 'governance',
    }
    return mapping.get(entity_type, 'concepts')

def to_kebab(name):
    if not name:
        return 'entity'
    s = re.sub(r'[^a-zA-Z0-9]+', '-', str(name)).strip('-').lower()
    return s or 'entity'

def build_pack(output_dir, entities, relations, schema, pack_name, pack_type):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    content_dirs = {}
    for e in entities.values():
        etype = e.get('type', 'unknown')
        dname = map_to_directory(etype)
        if dname not in content_dirs:
            content_dirs[dname] = []
        content_dirs[dname].append(e)

    # Generate content files
    entity_map = {}  # id -> (label, file_path)
    stats = defaultdict(int)

    for dirname, elist in content_dirs.items():
        dir_path = output_dir / dirname
        dir_path.mkdir(exist_ok=True)

        index_lines = [f"# {dirname.capitalize()}\n", f"Entities of type related to {dirname}.\n\n"]

        for entity in elist:
            eid = entity.get('id', 'unknown')
            etype = entity.get('type', 'Unknown')
            props = sanitize_properties(entity.get('properties', {}))
            label = props.get('name') or props.get('title') or eid
            stats[etype] += 1

            filename = to_kebab(label) + '.md'
            file_path = dir_path / filename
            rel_path = f"{dirname}/{filename}"

            entity_map[eid] = (label, rel_path)

            md = [f"# {label}\n"]
            md.append(f"> **Lead summary:** {etype} record from ontology graph.")

            md.append(f"\n**Type:** {etype}")
            for k, v in props.items():
                md.append(f"- **{k}:** {v}")

            # Add relations for this entity
            outgoing = [r for r in relations if r.get('from') == eid]
            if outgoing:
                md.append("\n**Relations:**")
                for r in outgoing:
                    to_id = r.get('to')
                    to_label = entity_map.get(to_id, (to_id, ''))[0] if to_id in entity_map else to_id
                    md.append(f"- {r.get('rel', 'relates_to')} → [{to_label}](../{entity_map.get(to_id, ('', ''))[1]})" if to_id in entity_map else f"- {r.get('rel', 'relates_to')} → {to_label}")

            md_content = '\n'.join(md)
            file_path.write_text(md_content, encoding='utf-8')
            index_lines.append(f"- [{label}]({filename}) — {etype}\n")

        # Write _index.md
        (dir_path / '_index.md').write_text(''.join(index_lines), encoding='utf-8')

    # Generate relations.yaml
    rel_yaml = {
        'entities': [],
        'relations': []
    }
    for eid, (label, fpath) in entity_map.items():
        e = next((e for e in entities.values() if e.get('id') == eid), {})
        etype = e.get('type', 'concept').lower()
        rel_yaml['entities'].append({
            'id': eid,
            'type': etype,
            'label': label,
            'file': fpath
        })

    for r in relations:
        if r['from'] in entity_map and r['to'] in entity_map:
            rel_yaml['relations'].append({
                'from': r['from'],
                'rel': r.get('rel', 'related_to'),
                'to': r['to']
            })

    with open(output_dir / 'relations.yaml', 'w', encoding='utf-8') as f:
        yaml.dump(rel_yaml, f, sort_keys=False)

    # manifest.yaml
    manifest = {
        'name': pack_name,
        'slug': to_kebab(pack_name),
        'type': pack_type,
        'version': '1.0.0',
        'description': f'ExpertPack generated from Ontology graph. {len(entities)} entities, {len(relations)} relations.',
        'entry_point': 'overview.md',
        'created': datetime.now().strftime('%Y-%m-%d'),
        'context': {
            'always': ['overview.md'],
            'searchable': ['relationships/', 'workflows/', 'facts/', 'concepts/'],
        },
        'schema_version': '2.3'
    }
    with open(output_dir / 'manifest.yaml', 'w', encoding='utf-8') as f:
        yaml.dump(manifest, f, sort_keys=False)

    # overview.md
    overview = f"""# {pack_name}

Overview of the migrated ontology knowledge graph.

**Statistics:**
- Entities: {len(entities)}
- Relations: {len(relations)}
- Entity types: {len(stats)}

Generated on {datetime.now().strftime('%Y-%m-%d')} by ontology-to-expertpack skill.

See `relations.yaml` for the entity graph and individual content files for details.
"""
    (output_dir / 'overview.md').write_text(overview, encoding='utf-8')

    # glossary.md (basic)
    glossary = "# Glossary\n\n"
    for t in sorted(stats.keys()):
        glossary += f"**{t}** — Entities of type {t} from the original ontology.\n\n"
    (output_dir / 'glossary.md').write_text(glossary, encoding='utf-8')

    return stats, len(relations)

def main():
    parser = argparse.ArgumentParser(description='Ontology to ExpertPack Converter')
    parser.add_argument('--graph', required=True, help='Path to graph.jsonl')
    parser.add_argument('--output', required=True, help='Output directory for ExpertPack')
    parser.add_argument('--schema', default='', help='Optional schema.yaml')
    parser.add_argument('--name', default='Ontology Export', help='Pack name')
    parser.add_argument('--type', default='auto', choices=['auto', 'person', 'product', 'process', 'composite'])
    args = parser.parse_args()

    entities, relations = parse_graph(args.graph)
    schema = load_schema(args.schema) if args.schema else {}

    pack_type = args.type if args.type != 'auto' else detect_pack_type(entities)

    print(f"Converting {len(entities)} entities and {len(relations)} relations...")
    print(f"Detected pack type: {pack_type}")

    stats, rel_count = build_pack(args.output, entities, relations, schema, args.name, pack_type)

    print("\n=== Conversion Complete ===")
    print(f"Pack type: {pack_type}")
    print("Entity counts by type:")
    for t, c in sorted(stats.items()):
        print(f"  {t}: {c}")
    print(f"Relations: {rel_count}")
    print(f"Output written to: {args.output}")
    print("\nNext steps:")
    print(f"  cd {args.output}")
    print("  # Run chunker and EK evaluator from expertpack skill")

if __name__ == "__main__":
    main()
