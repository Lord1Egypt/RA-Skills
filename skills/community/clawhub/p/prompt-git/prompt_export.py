#!/usr/bin/env python3
"""
PromptGit - Export/Import
Export and import prompts for sharing.

Author: Shadow Rose
License: MIT
"""

import json
import os
from typing import List, Dict
from datetime import datetime
from prompt_git import PromptRepository, PromptVersion


class PromptExporter:
    """Export and import prompts."""
    
    EXPORT_VERSION = '1.0'
    
    def __init__(self, repo: PromptRepository):
        """
        Initialize exporter.
        
        Args:
            repo: PromptRepository instance
        """
        self.repo = repo
    
    def export_prompt(self, name: str, include_history: bool = False) -> Dict:
        """
        Export a single prompt to portable format.
        
        Args:
            name: Prompt name
            include_history: Include full version history
        
        Returns:
            Dict with export data
        """
        # Get current version
        current = self.repo.get_version(name)
        if not current:
            raise ValueError(f"Prompt not found: {name}")
        
        # Get metadata
        index = self.repo._load_index()
        metadata = index.get(name, {})
        
        export_data = {
            'format': 'promptgit_export',
            'version': self.EXPORT_VERSION,
            'exported_at': datetime.utcnow().isoformat(),
            'name': name,
            'category': metadata.get('category', 'general'),
            'tags': metadata.get('tags', []),
            'current_version': current.id,
            'current_content': current.content,
        }
        
        if include_history:
            versions = self.repo.list_versions(name)
            export_data['history'] = []
            
            for v in versions:
                # Load content
                version_obj = self.repo.get_version(name, v.id)
                if version_obj:
                    export_data['history'].append({
                        'id': v.id,
                        'timestamp': v.timestamp,
                        'note': v.note,
                        'tags': v.tags,
                        'content': version_obj.content
                    })
        
        return export_data
    
    def export_to_file(self, name: str, output_path: str, 
                      include_history: bool = False):
        """
        Export prompt to JSON file.
        
        Args:
            name: Prompt name
            output_path: Output file path
            include_history: Include full version history
        """
        data = self.export_prompt(name, include_history=include_history)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
    
    def export_multiple(self, names: List[str], output_path: str,
                       include_history: bool = False):
        """
        Export multiple prompts to a single file.
        
        Args:
            names: List of prompt names
            output_path: Output file path
            include_history: Include full version history
        """
        exports = []
        
        for name in names:
            try:
                data = self.export_prompt(name, include_history=include_history)
                exports.append(data)
            except ValueError as e:
                print(f"Warning: {e}")
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump({
                'format': 'promptgit_export_bundle',
                'version': self.EXPORT_VERSION,
                'exported_at': datetime.utcnow().isoformat(),
                'prompts': exports
            }, f, indent=2)
    
    def import_prompt(self, data: Dict, overwrite: bool = False,
                     preserve_history: bool = True) -> str:
        """
        Import a prompt from export data.
        
        Args:
            data: Export data dict
            overwrite: Allow overwriting existing prompt
            preserve_history: Import full history if available
        
        Returns:
            Imported prompt name
        """
        # Validate format
        if data.get('format') != 'promptgit_export':
            raise ValueError("Invalid export format")
        
        name = data['name']
        
        # Check if exists
        existing = self.repo.get_version(name)
        if existing and not overwrite:
            raise ValueError(f"Prompt already exists: {name}. Use --overwrite to replace.")
        
        # Import history if available and requested
        if preserve_history and 'history' in data:
            # Clear existing history if overwriting
            if existing:
                versions_path = self.repo._get_versions_path(name)
                if os.path.exists(versions_path):
                    os.remove(versions_path)
            
            # Import each version in order
            for v_data in data['history']:
                try:
                    self.repo.save(
                        name,
                        v_data['content'],
                        note=v_data.get('note', ''),
                        category=data.get('category', 'general'),
                        tags=v_data.get('tags', [])
                    )
                except ValueError:
                    # Skip duplicates
                    pass
        else:
            # Import current version only
            self.repo.save(
                name,
                data['current_content'],
                note='Imported from export',
                category=data.get('category', 'general'),
                tags=data.get('tags', [])
            )
        
        return name
    
    def import_from_file(self, file_path: str, overwrite: bool = False,
                        preserve_history: bool = True) -> List[str]:
        """
        Import prompt(s) from JSON file.
        
        Args:
            file_path: Input file path
            overwrite: Allow overwriting existing prompts
            preserve_history: Import full history if available
        
        Returns:
            List of imported prompt names
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        imported = []
        
        # Check if bundle or single export
        if data.get('format') == 'promptgit_export_bundle':
            # Multiple prompts
            for prompt_data in data.get('prompts', []):
                try:
                    name = self.import_prompt(
                        prompt_data,
                        overwrite=overwrite,
                        preserve_history=preserve_history
                    )
                    imported.append(name)
                except ValueError as e:
                    print(f"Warning: {e}")
        else:
            # Single prompt
            name = self.import_prompt(
                data,
                overwrite=overwrite,
                preserve_history=preserve_history
            )
            imported.append(name)
        
        return imported
    
    def export_markdown(self, name: str, output_path: str):
        """
        Export prompt as markdown file with metadata.
        
        Args:
            name: Prompt name
            output_path: Output markdown file path
        """
        current = self.repo.get_version(name)
        if not current:
            raise ValueError(f"Prompt not found: {name}")
        
        index = self.repo._load_index()
        metadata = index.get(name, {})
        
        versions = self.repo.list_versions(name)
        
        md_content = f"""# {name}

**Category:** {metadata.get('category', 'general')}  
**Tags:** {', '.join(metadata.get('tags', []))}  
**Created:** {metadata.get('created', 'unknown')}  
**Modified:** {metadata.get('modified', 'unknown')}  
**Versions:** {len(versions)}

---

## Current Version

```
{current.content}
```

---

## Version History

"""
        
        for v in reversed(versions):
            tags_str = ', '.join(v.tags) if v.tags else 'none'
            md_content += f"- `{v.id[:8]}...` — {v.timestamp} — {v.note} [tags: {tags_str}]\n"
        
        md_content += "\n---\n\n*Exported from PromptGit*\n"
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(md_content)


def main():
    """CLI interface for export/import."""
    import argparse
    import sys
    
    parser = argparse.ArgumentParser(
        description='PromptGit Export/Import'
    )
    parser.add_argument(
        '--storage',
        help='Storage directory (default: ~/.promptgit)'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Export command
    export_parser = subparsers.add_parser('export', help='Export prompt')
    export_parser.add_argument('name', help='Prompt name')
    export_parser.add_argument('output', help='Output file path')
    export_parser.add_argument('--history', action='store_true', help='Include history')
    export_parser.add_argument('--markdown', action='store_true', help='Export as markdown')
    
    # Export multiple
    export_multi_parser = subparsers.add_parser('export-multi', help='Export multiple prompts')
    export_multi_parser.add_argument('output', help='Output file path')
    export_multi_parser.add_argument('--names', nargs='+', required=True, help='Prompt names')
    export_multi_parser.add_argument('--history', action='store_true', help='Include history')
    
    # Import command
    import_parser = subparsers.add_parser('import', help='Import prompt')
    import_parser.add_argument('file', help='Import file path')
    import_parser.add_argument('--overwrite', action='store_true', help='Overwrite existing')
    import_parser.add_argument('--no-history', action='store_true', help='Skip history')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    # Initialize
    repo = PromptRepository(storage_dir=args.storage)
    exporter = PromptExporter(repo)
    
    try:
        if args.command == 'export':
            if args.markdown:
                exporter.export_markdown(args.name, args.output)
                print(f"✅ Exported to markdown: {args.output}")
            else:
                exporter.export_to_file(
                    args.name,
                    args.output,
                    include_history=args.history
                )
                print(f"✅ Exported: {args.output}")
        
        elif args.command == 'export-multi':
            exporter.export_multiple(
                args.names,
                args.output,
                include_history=args.history
            )
            print(f"✅ Exported {len(args.names)} prompts to: {args.output}")
        
        elif args.command == 'import':
            imported = exporter.import_from_file(
                args.file,
                overwrite=args.overwrite,
                preserve_history=not args.no_history
            )
            
            print(f"✅ Imported {len(imported)} prompts:")
            for name in imported:
                print(f"  - {name}")
    
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
