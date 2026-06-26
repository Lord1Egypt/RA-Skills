#!/usr/bin/env python3
"""
PromptGit - Search and Browse
Search across prompt library with keyword, tag, and date filtering.

Author: Shadow Rose
License: MIT
"""

import json
import re
from datetime import datetime
from typing import List, Dict, Optional
from prompt_git import PromptRepository, PromptVersion, PromptMetadata


class PromptSearcher:
    """Search and browse across prompt library."""
    
    def __init__(self, repo: PromptRepository):
        """
        Initialize searcher.
        
        Args:
            repo: PromptRepository instance
        """
        self.repo = repo
    
    def search_content(self, query: str, category: str = None, 
                      case_sensitive: bool = False) -> List[tuple]:
        """
        Search prompt content for a keyword.
        
        Args:
            query: Search query
            category: Optional category filter
            case_sensitive: Case-sensitive search
        
        Returns:
            List of (name, version_id, match_count) tuples
        """
        results = []
        prompts = self.repo.list_prompts(category=category)
        
        if not case_sensitive:
            query = query.lower()
        
        for prompt in prompts:
            # Get current version
            version = self.repo.get_version(prompt.name)
            if not version:
                continue
            
            content = version.content
            if not case_sensitive:
                content = content.lower()
            
            # Count matches
            match_count = content.count(query)
            
            if match_count > 0:
                results.append((prompt.name, version.id, match_count))
        
        return results
    
    def search_by_tag(self, tag: str) -> List[PromptMetadata]:
        """
        Search prompts by tag.
        
        Args:
            tag: Tag to search for
        
        Returns:
            List of matching PromptMetadata
        """
        return self.repo.list_prompts(tag=tag)
    
    def search_by_date_range(self, start: str = None, end: str = None,
                            field: str = 'modified') -> List[PromptMetadata]:
        """
        Search prompts by date range.
        
        Args:
            start: Start date (ISO format or YYYY-MM-DD)
            end: End date (ISO format or YYYY-MM-DD)
            field: Date field to filter ('created' or 'modified')
        
        Returns:
            List of matching PromptMetadata
        """
        prompts = self.repo.list_prompts()
        results = []
        
        for prompt in prompts:
            date_str = getattr(prompt, field, None)
            if not date_str:
                continue
            
            # Parse date
            try:
                date = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
            except:
                continue
            
            # Apply filters
            if start:
                try:
                    start_date = datetime.fromisoformat(start.replace('Z', '+00:00'))
                    if date < start_date:
                        continue
                except:
                    pass
            
            if end:
                try:
                    end_date = datetime.fromisoformat(end.replace('Z', '+00:00'))
                    if date > end_date:
                        continue
                except:
                    pass
            
            results.append(prompt)
        
        return results
    
    def search_regex(self, pattern: str, category: str = None) -> List[tuple]:
        """
        Search prompt content using regex.
        
        Args:
            pattern: Regular expression pattern
            category: Optional category filter
        
        Returns:
            List of (name, version_id, matches) tuples
        """
        results = []
        prompts = self.repo.list_prompts(category=category)
        
        try:
            regex = re.compile(pattern)
        except re.error as e:
            raise ValueError(f"Invalid regex pattern: {e}")
        
        for prompt in prompts:
            version = self.repo.get_version(prompt.name)
            if not version:
                continue
            
            matches = regex.findall(version.content)
            
            if matches:
                results.append((prompt.name, version.id, matches))
        
        return results
    
    def get_recent(self, limit: int = 10, category: str = None) -> List[PromptMetadata]:
        """
        Get most recently modified prompts.
        
        Args:
            limit: Maximum number of results
            category: Optional category filter
        
        Returns:
            List of PromptMetadata, sorted by modification date
        """
        prompts = self.repo.list_prompts(category=category)
        
        # Sort by modified date (descending)
        prompts.sort(
            key=lambda p: datetime.fromisoformat(p.modified.replace('Z', '+00:00')),
            reverse=True
        )
        
        return prompts[:limit]
    
    def get_similar(self, name: str, threshold: float = 0.5) -> List[tuple]:
        """
        Find prompts similar to a given prompt.
        
        Uses simple word overlap similarity.
        
        Args:
            name: Reference prompt name
            threshold: Similarity threshold (0.0-1.0)
        
        Returns:
            List of (name, similarity_score) tuples
        """
        # Get reference prompt
        ref_version = self.repo.get_version(name)
        if not ref_version:
            raise ValueError(f"Prompt not found: {name}")
        
        # Tokenize reference
        ref_words = set(ref_version.content.lower().split())
        
        results = []
        prompts = self.repo.list_prompts()
        
        for prompt in prompts:
            if prompt.name == name:
                continue
            
            version = self.repo.get_version(prompt.name)
            if not version:
                continue
            
            # Calculate word overlap
            words = set(version.content.lower().split())
            
            if not words:
                continue
            
            overlap = len(ref_words & words)
            union = len(ref_words | words)
            
            similarity = overlap / union if union > 0 else 0.0
            
            if similarity >= threshold:
                results.append((prompt.name, similarity))
        
        # Sort by similarity (descending)
        results.sort(key=lambda x: x[1], reverse=True)
        
        return results
    
    def get_stats(self) -> Dict:
        """
        Get repository statistics.
        
        Returns:
            Dict with stats (total_prompts, total_versions, categories, etc.)
        """
        prompts = self.repo.list_prompts()
        
        total_prompts = len(prompts)
        total_versions = sum(p.version_count for p in prompts)
        
        categories = {}
        all_tags = set()
        
        for prompt in prompts:
            categories[prompt.category] = categories.get(prompt.category, 0) + 1
            all_tags.update(prompt.tags)
        
        return {
            'total_prompts': total_prompts,
            'total_versions': total_versions,
            'categories': categories,
            'total_tags': len(all_tags),
            'tags': sorted(all_tags)
        }


def main():
    """CLI interface for prompt search."""
    import argparse
    import sys
    
    parser = argparse.ArgumentParser(
        description='PromptGit Search - Search across prompt library'
    )
    parser.add_argument(
        '--storage',
        help='Storage directory (default: ~/.promptgit)'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Search commands')
    
    # Search content
    search_parser = subparsers.add_parser('search', help='Search prompt content')
    search_parser.add_argument('query', help='Search query')
    search_parser.add_argument('--category', help='Filter by category')
    search_parser.add_argument('--case-sensitive', action='store_true')
    
    # Search by tag
    tag_parser = subparsers.add_parser('tag', help='Search by tag')
    tag_parser.add_argument('tag', help='Tag to search for')
    
    # Search by date
    date_parser = subparsers.add_parser('date', help='Search by date range')
    date_parser.add_argument('--start', help='Start date (YYYY-MM-DD)')
    date_parser.add_argument('--end', help='End date (YYYY-MM-DD)')
    date_parser.add_argument('--field', default='modified', choices=['created', 'modified'])
    
    # Regex search
    regex_parser = subparsers.add_parser('regex', help='Regex search')
    regex_parser.add_argument('pattern', help='Regular expression pattern')
    regex_parser.add_argument('--category', help='Filter by category')
    
    # Recent prompts
    recent_parser = subparsers.add_parser('recent', help='Get recent prompts')
    recent_parser.add_argument('--limit', type=int, default=10, help='Number of results')
    recent_parser.add_argument('--category', help='Filter by category')
    
    # Similar prompts
    similar_parser = subparsers.add_parser('similar', help='Find similar prompts')
    similar_parser.add_argument('name', help='Reference prompt name')
    similar_parser.add_argument('--threshold', type=float, default=0.5, help='Similarity threshold')
    
    # Stats
    stats_parser = subparsers.add_parser('stats', help='Repository statistics')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    # Initialize
    repo = PromptRepository(storage_dir=args.storage)
    searcher = PromptSearcher(repo)
    
    try:
        if args.command == 'search':
            results = searcher.search_content(
                args.query,
                category=args.category,
                case_sensitive=args.case_sensitive
            )
            
            if not results:
                print("No matches found")
            else:
                print(f"Found {len(results)} matches:\n")
                for name, version_id, count in results:
                    print(f"  {name} ({version_id[:8]}...) — {count} occurrences")
        
        elif args.command == 'tag':
            results = searcher.search_by_tag(args.tag)
            
            if not results:
                print(f"No prompts found with tag: {args.tag}")
            else:
                print(f"Found {len(results)} prompts:\n")
                for p in results:
                    print(f"  {p.name} [{p.category}] — {p.version_count} versions")
        
        elif args.command == 'date':
            results = searcher.search_by_date_range(
                start=args.start,
                end=args.end,
                field=args.field
            )
            
            if not results:
                print("No prompts found in date range")
            else:
                print(f"Found {len(results)} prompts:\n")
                for p in results:
                    date_val = getattr(p, args.field)
                    print(f"  {p.name} — {date_val[:10]}")
        
        elif args.command == 'regex':
            results = searcher.search_regex(args.pattern, category=args.category)
            
            if not results:
                print("No matches found")
            else:
                print(f"Found {len(results)} matches:\n")
                for name, version_id, matches in results:
                    print(f"  {name} ({version_id[:8]}...) — {len(matches)} matches")
                    for match in matches[:3]:  # Show first 3
                        print(f"    - {match}")
        
        elif args.command == 'recent':
            results = searcher.get_recent(limit=args.limit, category=args.category)
            
            if not results:
                print("No prompts found")
            else:
                print(f"Recent prompts:\n")
                for p in results:
                    print(f"  {p.name} [{p.category}] — {p.modified[:10]}")
        
        elif args.command == 'similar':
            results = searcher.get_similar(args.name, threshold=args.threshold)
            
            if not results:
                print(f"No similar prompts found (threshold: {args.threshold})")
            else:
                print(f"Similar to '{args.name}':\n")
                for name, score in results:
                    print(f"  {name} — {score:.2f} similarity")
        
        elif args.command == 'stats':
            stats = searcher.get_stats()
            
            print(f"Repository Statistics:\n")
            print(f"Total prompts: {stats['total_prompts']}")
            print(f"Total versions: {stats['total_versions']}")
            print(f"Total tags: {stats['total_tags']}")
            print(f"\nCategories:")
            for category, count in stats['categories'].items():
                print(f"  {category}: {count}")
            print(f"\nTags:")
            for tag in stats['tags']:
                print(f"  - {tag}")
    
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
