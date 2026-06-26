#!/usr/bin/env python3
"""
PromptVault - Team Prompt Library
Organize, rate, and share prompts with your team

Author: Shadow Rose
License: MIT
"""

import sys
import os
import json
import argparse
from datetime import datetime
from pathlib import Path
import hashlib

# Load config from JSON
import types as _types
def _load_config():
    _defaults = {
        "VAULT_PATH": "./prompt_vault.json",
        "DEFAULT_CATEGORIES": ["system", "task", "template", "snippet", "chain"],
    }
    for _path in ("config.json", "config_example.json"):
        if os.path.exists(_path):
            try:
                with open(_path, "r", encoding="utf-8") as _f:
                    _data = json.load(_f)
                    _defaults.update(_data)
                    return _types.SimpleNamespace(**_defaults)
            except json.JSONDecodeError:
                pass
    return _types.SimpleNamespace(**_defaults)
config = _load_config()


class PromptVault:
    """Main prompt library manager"""
    
    def __init__(self, vault_path=None):
        self.vault_path = Path(vault_path or config.VAULT_PATH)
        self.vault = self._load_vault()
    
    def _load_vault(self):
        """Load vault from disk"""
        if not self.vault_path.exists():
            return {
                'version': '1.0',
                'created': datetime.now().isoformat(),
                'prompts': []
            }
        
        try:
            with open(self.vault_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading vault: {e}")
            print("Starting with empty vault.")
            return {'version': '1.0', 'created': datetime.now().isoformat(), 'prompts': []}
    
    def _save_vault(self):
        """Save vault to disk"""
        self.vault_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Create backup before saving
        if self.vault_path.exists():
            backup_path = self.vault_path.with_suffix('.json.bak')
            self.vault_path.replace(backup_path)
        
        with open(self.vault_path, 'w', encoding='utf-8') as f:
            json.dump(self.vault, f, indent=2, ensure_ascii=False)
    
    def _generate_id(self, prompt_text):
        """Generate unique ID for a prompt"""
        return hashlib.sha256(prompt_text.encode()).hexdigest()[:12]
    
    def add_prompt(self, name, text, category='task', tags=None, author='', notes='', 
                   model_compat='', rating=None):
        """Add a new prompt to the vault"""
        prompt_id = self._generate_id(text)
        
        # Check if prompt already exists
        existing = self.get_prompt(prompt_id)
        if existing:
            print(f"Warning: Prompt with ID {prompt_id} already exists.")
            return None
        
        prompt = {
            'id': prompt_id,
            'name': name,
            'text': text,
            'category': category,
            'tags': tags or [],
            'author': author,
            'notes': notes,
            'model_compat': model_compat,
            'rating': rating,
            'usage_count': 0,
            'created': datetime.now().isoformat(),
            'modified': datetime.now().isoformat(),
            'changelog': []
        }
        
        self.vault['prompts'].append(prompt)
        self._save_vault()
        
        return prompt_id
    
    def get_prompt(self, prompt_id):
        """Get a prompt by ID"""
        for p in self.vault['prompts']:
            if p['id'] == prompt_id:
                return p
        return None
    
    def update_prompt(self, prompt_id, **kwargs):
        """Update an existing prompt"""
        prompt = self.get_prompt(prompt_id)
        if not prompt:
            raise ValueError(f"Prompt not found: {prompt_id}")
        
        # Record changes in changelog
        changes = []
        for key, value in kwargs.items():
            if key in prompt and prompt[key] != value:
                changes.append(f"{key}: {prompt[key]} → {value}")
                prompt[key] = value
        
        if changes:
            prompt['changelog'].append({
                'date': datetime.now().isoformat(),
                'changes': changes
            })
            prompt['modified'] = datetime.now().isoformat()
            self._save_vault()
        
        return prompt
    
    def rate_prompt(self, prompt_id, rating, notes=''):
        """Rate a prompt (1-5 stars)"""
        if not 1 <= rating <= 5:
            raise ValueError("Rating must be between 1 and 5")
        
        prompt = self.get_prompt(prompt_id)
        if not prompt:
            raise ValueError(f"Prompt not found: {prompt_id}")
        
        prompt['rating'] = rating
        if notes:
            prompt['notes'] = prompt.get('notes', '') + f"\n[Rating {rating}/5] {notes}"
        
        prompt['modified'] = datetime.now().isoformat()
        self._save_vault()
        
        return prompt
    
    def increment_usage(self, prompt_id):
        """Increment usage counter for a prompt"""
        prompt = self.get_prompt(prompt_id)
        if prompt:
            prompt['usage_count'] = prompt.get('usage_count', 0) + 1
            self._save_vault()
    
    def search(self, query='', category=None, tags=None, author=None, min_rating=None):
        """Search prompts by various criteria"""
        results = []
        
        for prompt in self.vault['prompts']:
            # Query search (name, text, notes)
            if query:
                query_lower = query.lower()
                searchable = f"{prompt['name']} {prompt['text']} {prompt.get('notes', '')}".lower()
                if query_lower not in searchable:
                    continue
            
            # Category filter
            if category and prompt['category'] != category:
                continue
            
            # Tags filter (any tag matches)
            if tags:
                prompt_tags = [t.lower() for t in prompt.get('tags', [])]
                filter_tags = [t.lower() for t in tags]
                if not any(t in prompt_tags for t in filter_tags):
                    continue
            
            # Author filter
            if author and author.lower() not in prompt.get('author', '').lower():
                continue
            
            # Rating filter
            if min_rating and (prompt.get('rating') or 0) < min_rating:
                continue
            
            results.append(prompt)
        
        return results
    
    def delete_prompt(self, prompt_id):
        """Delete a prompt"""
        original_count = len(self.vault['prompts'])
        self.vault['prompts'] = [p for p in self.vault['prompts'] if p['id'] != prompt_id]
        
        if len(self.vault['prompts']) < original_count:
            self._save_vault()
            return True
        return False
    
    def list_categories(self):
        """List all unique categories"""
        categories = set(p['category'] for p in self.vault['prompts'])
        return sorted(categories)
    
    def list_tags(self):
        """List all unique tags"""
        tags = set()
        for p in self.vault['prompts']:
            tags.update(p.get('tags', []))
        return sorted(tags)
    
    def stats(self):
        """Get vault statistics"""
        total = len(self.vault['prompts'])
        if total == 0:
            return {
                'total': 0,
                'by_category': {},
                'avg_rating': 0,
                'top_used': []
            }
        
        by_category = {}
        for p in self.vault['prompts']:
            cat = p['category']
            by_category[cat] = by_category.get(cat, 0) + 1
        
        rated = [p for p in self.vault['prompts'] if p.get('rating')]
        avg_rating = sum(p['rating'] for p in rated) / len(rated) if rated else 0
        
        top_used = sorted(
            self.vault['prompts'],
            key=lambda p: p.get('usage_count', 0),
            reverse=True
        )[:10]
        
        return {
            'total': total,
            'by_category': by_category,
            'avg_rating': round(avg_rating, 2),
            'top_used': [(p['name'], p.get('usage_count', 0)) for p in top_used if p.get('usage_count', 0) > 0]
        }


def print_prompt(prompt, verbose=False):
    """Pretty print a prompt"""
    stars = '⭐' * (prompt.get('rating') or 0)
    
    print(f"\n{'='*60}")
    print(f"ID: {prompt['id']}")
    print(f"Name: {prompt['name']} {stars}")
    print(f"Category: {prompt['category']}")
    
    if prompt.get('tags'):
        print(f"Tags: {', '.join(prompt['tags'])}")
    
    if prompt.get('author'):
        print(f"Author: {prompt['author']}")
    
    if prompt.get('model_compat'):
        print(f"Models: {prompt['model_compat']}")
    
    print(f"Usage: {prompt.get('usage_count', 0)} times")
    print(f"\n{prompt['text']}")
    
    if verbose:
        if prompt.get('notes'):
            print(f"\nNotes:\n{prompt['notes']}")
        
        if prompt.get('changelog'):
            print(f"\nChangelog:")
            for entry in prompt['changelog'][-3:]:  # Last 3 changes
                print(f"  {entry['date']}: {'; '.join(entry['changes'])}")
    
    print('='*60)


def main():
    parser = argparse.ArgumentParser(
        description='PromptVault - Team Prompt Library Manager',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Add a new prompt
  prompt_vault.py add "System: Helpful" --text "You are a helpful assistant." --category system
  
  # Search for prompts
  prompt_vault.py search "code review" --category task
  
  # Rate a prompt
  prompt_vault.py rate abc123def456 --rating 5 --notes "Works great with Claude"
  
  # List all prompts
  prompt_vault.py list --category system
  
  # Show statistics
  prompt_vault.py stats
        """
    )
    
    parser.add_argument('--vault', default=config.VAULT_PATH, help='Vault file path')
    
    subparsers = parser.add_subparsers(dest='command', help='Command')
    
    # Add command
    add_parser = subparsers.add_parser('add', help='Add a new prompt')
    add_parser.add_argument('name', help='Prompt name')
    add_parser.add_argument('--text', required=True, help='Prompt text')
    add_parser.add_argument('--category', default='task', choices=config.DEFAULT_CATEGORIES,
                           help='Prompt category')
    add_parser.add_argument('--tags', help='Comma-separated tags')
    add_parser.add_argument('--author', default='', help='Prompt author')
    add_parser.add_argument('--notes', default='', help='Usage notes')
    add_parser.add_argument('--models', default='', help='Compatible models')
    add_parser.add_argument('--rating', type=int, choices=[1,2,3,4,5], help='Initial rating')
    
    # Search command
    search_parser = subparsers.add_parser('search', help='Search prompts')
    search_parser.add_argument('query', nargs='?', default='', help='Search query')
    search_parser.add_argument('--category', help='Filter by category')
    search_parser.add_argument('--tags', help='Filter by tags (comma-separated)')
    search_parser.add_argument('--author', help='Filter by author')
    search_parser.add_argument('--min-rating', type=int, help='Minimum rating')
    search_parser.add_argument('-v', '--verbose', action='store_true', help='Show full details')
    
    # List command
    list_parser = subparsers.add_parser('list', help='List prompts')
    list_parser.add_argument('--category', help='Filter by category')
    list_parser.add_argument('-v', '--verbose', action='store_true', help='Show full details')
    
    # Get command
    get_parser = subparsers.add_parser('get', help='Get a specific prompt')
    get_parser.add_argument('id', help='Prompt ID')
    get_parser.add_argument('-v', '--verbose', action='store_true', help='Show full details')
    get_parser.add_argument('--use', action='store_true', help='Increment usage counter')
    
    # Rate command
    rate_parser = subparsers.add_parser('rate', help='Rate a prompt')
    rate_parser.add_argument('id', help='Prompt ID')
    rate_parser.add_argument('--rating', type=int, required=True, choices=[1,2,3,4,5])
    rate_parser.add_argument('--notes', default='', help='Rating notes')
    
    # Update command
    update_parser = subparsers.add_parser('update', help='Update a prompt')
    update_parser.add_argument('id', help='Prompt ID')
    update_parser.add_argument('--name', help='New name')
    update_parser.add_argument('--text', help='New text')
    update_parser.add_argument('--category', help='New category')
    update_parser.add_argument('--tags', help='New tags (comma-separated)')
    update_parser.add_argument('--notes', help='New notes')
    
    # Delete command
    delete_parser = subparsers.add_parser('delete', help='Delete a prompt')
    delete_parser.add_argument('id', help='Prompt ID')
    delete_parser.add_argument('--confirm', action='store_true', help='Skip confirmation')
    
    # Stats command
    stats_parser = subparsers.add_parser('stats', help='Show vault statistics')
    
    # Categories command
    cat_parser = subparsers.add_parser('categories', help='List all categories')
    
    # Tags command
    tags_parser = subparsers.add_parser('tags', help='List all tags')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    vault = PromptVault(args.vault)
    
    try:
        if args.command == 'add':
            tags = [t.strip() for t in args.tags.split(',')] if args.tags else []
            prompt_id = vault.add_prompt(
                name=args.name,
                text=args.text,
                category=args.category,
                tags=tags,
                author=args.author,
                notes=args.notes,
                model_compat=args.models,
                rating=args.rating
            )
            print(f"Prompt added successfully!")
            print(f"ID: {prompt_id}")
        
        elif args.command == 'search':
            tags = [t.strip() for t in args.tags.split(',')] if args.tags else None
            results = vault.search(
                query=args.query,
                category=args.category,
                tags=tags,
                author=args.author,
                min_rating=args.min_rating
            )
            
            print(f"\nFound {len(results)} prompt(s):")
            for p in results:
                print_prompt(p, verbose=args.verbose)
        
        elif args.command == 'list':
            results = vault.search(category=args.category)
            print(f"\nTotal: {len(results)} prompt(s)")
            for p in results:
                if args.verbose:
                    print_prompt(p, verbose=True)
                else:
                    stars = '⭐' * (p.get('rating') or 0)
                    print(f"[{p['id']}] {p['name']} {stars} ({p['category']})")
        
        elif args.command == 'get':
            prompt = vault.get_prompt(args.id)
            if not prompt:
                print(f"Prompt not found: {args.id}")
                return
            
            if args.use:
                vault.increment_usage(args.id)
            
            print_prompt(prompt, verbose=args.verbose)
        
        elif args.command == 'rate':
            vault.rate_prompt(args.id, args.rating, args.notes)
            print(f"Prompt rated {args.rating}/5")
        
        elif args.command == 'update':
            updates = {}
            if args.name:
                updates['name'] = args.name
            if args.text:
                updates['text'] = args.text
            if args.category:
                updates['category'] = args.category
            if args.tags:
                updates['tags'] = [t.strip() for t in args.tags.split(',')]
            if args.notes:
                updates['notes'] = args.notes
            
            vault.update_prompt(args.id, **updates)
            print("Prompt updated successfully")
        
        elif args.command == 'delete':
            if not args.confirm:
                prompt = vault.get_prompt(args.id)
                if prompt:
                    print(f"Delete prompt: {prompt['name']}?")
                    response = input("Type 'yes' to confirm: ")
                    if response.lower() != 'yes':
                        print("Cancelled")
                        return
            
            if vault.delete_prompt(args.id):
                print("Prompt deleted")
            else:
                print("Prompt not found")
        
        elif args.command == 'stats':
            stats = vault.stats()
            print("\n=== Vault Statistics ===")
            print(f"Total prompts: {stats['total']}")
            print(f"Average rating: {stats['avg_rating']}/5")
            print(f"\nBy category:")
            for cat, count in sorted(stats['by_category'].items()):
                print(f"  {cat}: {count}")
            
            if stats['top_used']:
                print(f"\nMost used:")
                for name, count in stats['top_used']:
                    print(f"  {name}: {count} times")
        
        elif args.command == 'categories':
            cats = vault.list_categories()
            print(f"\nCategories ({len(cats)}):")
            for cat in cats:
                count = sum(1 for p in vault.vault['prompts'] if p['category'] == cat)
                print(f"  {cat}: {count} prompts")
        
        elif args.command == 'tags':
            tags = vault.list_tags()
            print(f"\nTags ({len(tags)}):")
            for tag in tags:
                print(f"  {tag}")
    
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
