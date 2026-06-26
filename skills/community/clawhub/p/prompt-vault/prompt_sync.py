#!/usr/bin/env python3
"""
PromptVault Sync - Export/Import for team sharing
Share prompt libraries between teams safely

Author: Shadow Rose
License: MIT
"""

import sys
import json
import argparse
from pathlib import Path
from datetime import datetime

import os as _os, types as _types
def _load_config():
    _defaults = {"VAULT_PATH": "./prompt_vault.json"}
    for _p in ("config.json", "config_example.json"):
        if _os.path.exists(_p):
            try:
                import json as _j
                with open(_p, "r", encoding="utf-8") as _f:
                    _defaults.update(_j.load(_f))
                    return _types.SimpleNamespace(**_defaults)
            except Exception:
                pass
    return _types.SimpleNamespace(**_defaults)
config = _load_config()


def export_vault(vault_path, output_path, categories=None, min_rating=None, include_private=False):
    """
    Export vault to shareable format
    
    Args:
        vault_path: Source vault file
        output_path: Export destination
        categories: List of categories to include (None = all)
        min_rating: Minimum rating to include
        include_private: Include notes/changelog (default: exclude for sharing)
    """
    
    with open(vault_path, 'r', encoding='utf-8') as f:
        vault = json.load(f)
    
    exported_prompts = []
    
    for prompt in vault.get('prompts', []):
        # Category filter
        if categories and prompt.get('category') not in categories:
            continue
        
        # Rating filter
        if min_rating and (prompt.get('rating') or 0) < min_rating:
            continue
        
        # Create export copy
        exported = {
            'id': prompt['id'],
            'name': prompt['name'],
            'text': prompt['text'],
            'category': prompt['category'],
            'tags': prompt.get('tags', []),
            'author': prompt.get('author', ''),
            'model_compat': prompt.get('model_compat', ''),
            'rating': prompt.get('rating'),
            'usage_count': prompt.get('usage_count', 0),
            'created': prompt.get('created', ''),
        }
        
        # Include private data if requested
        if include_private:
            exported['notes'] = prompt.get('notes', '')
            exported['changelog'] = prompt.get('changelog', [])
        
        exported_prompts.append(exported)
    
    export_data = {
        'version': '1.0',
        'export_date': datetime.now().isoformat(),
        'source': str(vault_path),
        'prompt_count': len(exported_prompts),
        'prompts': exported_prompts
    }
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(export_data, f, indent=2, ensure_ascii=False)
    
    return len(exported_prompts)


def import_vault(vault_path, import_path, merge_strategy='skip', update_existing=False):
    """
    Import prompts from export file
    
    Args:
        vault_path: Destination vault file
        import_path: Import source file
        merge_strategy: 'skip', 'replace', or 'merge' for duplicate IDs
        update_existing: Update existing prompts with newer data
    
    Returns:
        Dict with import statistics
    """
    
    # Load existing vault
    if Path(vault_path).exists():
        with open(vault_path, 'r', encoding='utf-8') as f:
            vault = json.load(f)
    else:
        vault = {
            'version': '1.0',
            'created': datetime.now().isoformat(),
            'prompts': []
        }
    
    # Load import data
    with open(import_path, 'r', encoding='utf-8') as f:
        import_data = json.load(f)
    
    existing_ids = {p['id']: i for i, p in enumerate(vault['prompts'])}
    
    stats = {
        'total': len(import_data.get('prompts', [])),
        'added': 0,
        'skipped': 0,
        'replaced': 0,
        'errors': []
    }
    
    for prompt in import_data.get('prompts', []):
        prompt_id = prompt.get('id')
        
        if not prompt_id:
            stats['errors'].append("Prompt missing ID")
            continue
        
        if prompt_id in existing_ids:
            # Handle duplicate
            if merge_strategy == 'skip':
                stats['skipped'] += 1
                continue
            elif merge_strategy == 'replace':
                vault['prompts'][existing_ids[prompt_id]] = prompt
                stats['replaced'] += 1
            elif merge_strategy == 'merge':
                # Merge: keep existing metadata, update content if newer
                existing = vault['prompts'][existing_ids[prompt_id]]
                
                # Update text if import is newer or has higher rating
                import_rating = prompt.get('rating', 0)
                existing_rating = existing.get('rating', 0)
                
                if import_rating > existing_rating or update_existing:
                    existing['text'] = prompt['text']
                    existing['modified'] = datetime.now().isoformat()
                    existing['rating'] = max(import_rating, existing_rating)
                
                # Merge tags (union)
                existing_tags = set(existing.get('tags', []))
                import_tags = set(prompt.get('tags', []))
                existing['tags'] = sorted(existing_tags | import_tags)
                
                stats['replaced'] += 1
        else:
            # New prompt - add it
            # Ensure required fields
            prompt.setdefault('usage_count', 0)
            prompt.setdefault('created', datetime.now().isoformat())
            prompt.setdefault('modified', datetime.now().isoformat())
            prompt.setdefault('changelog', [])
            
            vault['prompts'].append(prompt)
            stats['added'] += 1
    
    # Save updated vault
    Path(vault_path).parent.mkdir(parents=True, exist_ok=True)
    
    # Backup existing vault
    if Path(vault_path).exists():
        backup_path = Path(vault_path).with_suffix('.json.bak')
        Path(vault_path).replace(backup_path)
    
    with open(vault_path, 'w', encoding='utf-8') as f:
        json.dump(vault, f, indent=2, ensure_ascii=False)
    
    return stats


def diff_vaults(vault1_path, vault2_path):
    """
    Show differences between two vaults
    
    Returns:
        Dict with difference statistics
    """
    
    with open(vault1_path, 'r', encoding='utf-8') as f:
        vault1 = json.load(f)
    
    with open(vault2_path, 'r', encoding='utf-8') as f:
        vault2 = json.load(f)
    
    ids1 = {p['id']: p for p in vault1.get('prompts', [])}
    ids2 = {p['id']: p for p in vault2.get('prompts', [])}
    
    only_in_1 = set(ids1.keys()) - set(ids2.keys())
    only_in_2 = set(ids2.keys()) - set(ids1.keys())
    common = set(ids1.keys()) & set(ids2.keys())
    
    modified = []
    for pid in common:
        if ids1[pid]['text'] != ids2[pid]['text']:
            modified.append(pid)
    
    return {
        'only_in_vault1': len(only_in_1),
        'only_in_vault2': len(only_in_2),
        'common': len(common),
        'modified': len(modified),
        'details': {
            'only_in_1': [ids1[pid]['name'] for pid in only_in_1],
            'only_in_2': [ids2[pid]['name'] for pid in only_in_2],
            'modified': [ids1[pid]['name'] for pid in modified]
        }
    }


def main():
    parser = argparse.ArgumentParser(
        description='PromptVault Sync - Export/Import for team sharing',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Export entire vault
  python prompt_sync.py export my_vault.json -o export.json
  
  # Export only high-rated prompts
  python prompt_sync.py export my_vault.json -o export.json --min-rating 4
  
  # Export specific categories
  python prompt_sync.py export my_vault.json -o export.json --categories system,task
  
  # Import with skip strategy (default - skip duplicates)
  python prompt_sync.py import my_vault.json --from export.json
  
  # Import with replace strategy (replace duplicates)
  python prompt_sync.py import my_vault.json --from export.json --strategy replace
  
  # Compare two vaults
  python prompt_sync.py diff vault1.json vault2.json
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Command')
    
    # Export command
    export_parser = subparsers.add_parser('export', help='Export vault')
    export_parser.add_argument('vault', help='Source vault file')
    export_parser.add_argument('-o', '--output', required=True, help='Export output file')
    export_parser.add_argument('--categories', help='Comma-separated categories to include')
    export_parser.add_argument('--min-rating', type=int, help='Minimum rating to include')
    export_parser.add_argument('--include-private', action='store_true',
                              help='Include notes and changelog')
    
    # Import command
    import_parser = subparsers.add_parser('import', help='Import prompts')
    import_parser.add_argument('vault', help='Destination vault file')
    import_parser.add_argument('--from', dest='import_file', required=True, help='Import source file')
    import_parser.add_argument('--strategy', choices=['skip', 'replace', 'merge'], default='skip',
                              help='Strategy for handling duplicates (default: skip)')
    import_parser.add_argument('--update-existing', action='store_true',
                              help='Update existing prompts with newer data')
    
    # Diff command
    diff_parser = subparsers.add_parser('diff', help='Compare two vaults')
    diff_parser.add_argument('vault1', help='First vault file')
    diff_parser.add_argument('vault2', help='Second vault file')
    diff_parser.add_argument('-v', '--verbose', action='store_true', help='Show detailed differences')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    try:
        if args.command == 'export':
            categories = [c.strip() for c in args.categories.split(',')] if args.categories else None
            
            count = export_vault(
                args.vault,
                args.output,
                categories=categories,
                min_rating=args.min_rating,
                include_private=args.include_private
            )
            
            print(f"✓ Exported {count} prompts to {args.output}")
        
        elif args.command == 'import':
            stats = import_vault(
                args.vault,
                args.import_file,
                merge_strategy=args.strategy,
                update_existing=args.update_existing
            )
            
            print(f"\n=== Import Summary ===")
            print(f"Total in import file: {stats['total']}")
            print(f"Added: {stats['added']}")
            print(f"Replaced: {stats['replaced']}")
            print(f"Skipped: {stats['skipped']}")
            
            if stats['errors']:
                print(f"Errors: {len(stats['errors'])}")
                for err in stats['errors']:
                    print(f"  - {err}")
            
            print(f"\n✓ Import complete. Vault updated: {args.vault}")
        
        elif args.command == 'diff':
            diff = diff_vaults(args.vault1, args.vault2)
            
            print(f"\n=== Vault Comparison ===")
            print(f"Only in {args.vault1}: {diff['only_in_vault1']}")
            print(f"Only in {args.vault2}: {diff['only_in_vault2']}")
            print(f"Common: {diff['common']}")
            print(f"Modified: {diff['modified']}")
            
            if args.verbose:
                details = diff['details']
                
                if details['only_in_1']:
                    print(f"\nOnly in {args.vault1}:")
                    for name in details['only_in_1']:
                        print(f"  - {name}")
                
                if details['only_in_2']:
                    print(f"\nOnly in {args.vault2}:")
                    for name in details['only_in_2']:
                        print(f"  - {name}")
                
                if details['modified']:
                    print(f"\nModified:")
                    for name in details['modified']:
                        print(f"  - {name}")
    
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
