#!/usr/bin/env python3
"""
ADR - Architecture Decision Records Manager
"""

import argparse
import re
import sys
from datetime import datetime
from pathlib import Path


class ADRManager:
    """Manages Architecture Decision Records"""
    
    VALID_STATUSES = ['proposed', 'accepted', 'rejected', 'deprecated', 'superseded']
    
    def __init__(self, root_path: str):
        self.root = Path(root_path).resolve()
        self.adr_dir = self.root / 'docs' / 'adr'
    
    def _ensure_adr_dir(self):
        """Ensure ADR directory exists"""
        self.adr_dir.mkdir(parents=True, exist_ok=True)
    
    def _get_next_number(self) -> int:
        """Get next ADR number"""
        if not self.adr_dir.exists():
            return 1
        
        max_num = 0
        for f in self.adr_dir.glob('*.md'):
            match = re.match(r'^(\d+)-', f.name)
            if match:
                max_num = max(max_num, int(match.group(1)))
        
        return max_num + 1
    
    def _slugify(self, title: str) -> str:
        """Convert title to filename slug"""
        slug = title.lower()
        slug = re.sub(r'[^\w\s-]', '', slug)
        slug = re.sub(r'[-\s]+', '-', slug)
        return slug
    
    def create(self, title: str, status: str = 'proposed') -> Path:
        """Create a new ADR"""
        self._ensure_adr_dir()
        
        if status not in self.VALID_STATUSES:
            raise ValueError(f"Invalid status: {status}. Use: {', '.join(self.VALID_STATUSES)}")
        
        number = self._get_next_number()
        slug = self._slugify(title)
        filename = f"{number:04d}-{slug}.md"
        filepath = self.adr_dir / filename
        
        content = self._generate_template(title, status, number)
        filepath.write_text(content, encoding='utf-8')
        
        return filepath
    
    def _generate_template(self, title: str, status: str, number: int) -> str:
        """Generate MADR template"""
        date = datetime.now().strftime('%Y-%m-%d')
        
        return f"""# {number}. {title}

Date: {date}
Status: {status}
Deciders: [your name]

## Context and Problem Statement

[Describe the context and the problem]

## Decision Drivers

- [driver 1]
- [driver 2]

## Considered Options

- [option 1]
- [option 2]

## Decision Outcome

Chosen option: "[option 1]"

### Positive Consequences

- [consequence 1]
- [consequence 2]

### Negative Consequences

- [consequence 1]
- [consequence 2]

## Links

- [Related ADR]
"""
    
    def list(self, status_filter: str = None) -> list:
        """List all ADRs"""
        if not self.adr_dir.exists():
            return []
        
        adrs = []
        for f in sorted(self.adr_dir.glob('*.md')):
            if f.name == 'index.md':
                continue
            
            adr = self._parse_adr(f)
            if adr:
                if status_filter is None or adr.get('status') == status_filter:
                    adrs.append(adr)
        
        return adrs
    
    def _parse_adr(self, filepath: Path) -> dict:
        """Parse ADR file"""
        content = filepath.read_text(encoding='utf-8')
        
        # Extract number and title from filename
        match = re.match(r'^(\d+)-(.+)\.md$', filepath.name)
        if not match:
            return None
        
        number = int(match.group(1))
        slug = match.group(2)
        
        # Extract title from first heading
        title_match = re.search(r'^#\s+\d+\.\s+(.+)$', content, re.MULTILINE)
        title = title_match.group(1) if title_match else slug.replace('-', ' ')
        
        # Extract status
        status_match = re.search(r'^Status:\s*(\w+)', content, re.MULTILINE | re.IGNORECASE)
        status = status_match.group(1).lower() if status_match else 'unknown'
        
        # Extract date
        date_match = re.search(r'^Date:\s*(\d{4}-\d{2}-\d{2})', content, re.MULTILINE)
        date = date_match.group(1) if date_match else None
        
        return {
            'number': number,
            'title': title,
            'status': status,
            'date': date,
            'filepath': filepath,
            'slug': slug,
        }
    
    def update_status(self, number: int, new_status: str, superseded_by: int = None):
        """Update ADR status"""
        if new_status not in self.VALID_STATUSES:
            raise ValueError(f"Invalid status: {new_status}")
        
        # Find the ADR file
        adr_file = None
        for f in self.adr_dir.glob('*.md'):
            if f.name == 'index.md':
                continue
            match = re.match(r'^(\d+)-', f.name)
            if match and int(match.group(1)) == number:
                adr_file = f
                break
        
        if not adr_file:
            raise FileNotFoundError(f"ADR #{number} not found")
        
        content = adr_file.read_text(encoding='utf-8')
        
        # Update status
        content = re.sub(
            r'^(Status:\s*)\w+',
            f'\\g<1>{new_status}',
            content,
            flags=re.MULTILINE | re.IGNORECASE
        )
        
        # Add superseded link if applicable
        if new_status == 'superseded' and superseded_by:
            content += f"\n\nSuperseded by: [{superseded_by:04d}]({superseded_by:04d}-*.md)\n"
        
        adr_file.write_text(content, encoding='utf-8')
        
        return adr_file


def run_create(args):
    """Create new ADR"""
    manager = ADRManager(args.root)
    
    try:
        filepath = manager.create(args.title, args.status)
        print(f"✅ Created: {filepath}")
        print()
        print("Next steps:")
        print(f"1. Edit: {filepath}")
        print("2. Run: python3 scripts/main.py lint")
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


def run_list(args):
    """List ADRs"""
    manager = ADRManager(args.root)
    adrs = manager.list(args.status)
    
    if not adrs:
        print("No ADRs found")
        return
    
    print("\n📋 Architecture Decision Records")
    print(f"{'='*60}")
    
    # Group by status
    by_status = {}
    for adr in adrs:
        status = adr['status']
        if status not in by_status:
            by_status[status] = []
        by_status[status].append(adr)
    
    for status in manager.VALID_STATUSES:
        if status in by_status:
            print(f"\n{status.upper()}:")
            for adr in by_status[status]:
                print(f"  [{adr['number']:04d}] {adr['title']}")


def run_update(args):
    """Update ADR status"""
    manager = ADRManager(args.root)
    
    try:
        filepath = manager.update_status(args.number, args.status, args.superseded_by)
        print(f"✅ Updated: {filepath}")
        print(f"   New status: {args.status}")
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


def run_lint(args):
    """Lint ADRs"""
    manager = ADRManager(args.root)
    adrs = manager.list()
    
    print("\n🔍 ADR Lint Results")
    print(f"{'='*60}")
    
    if not adrs:
        print("No ADRs to check")
        return
    
    for adr in adrs:
        issues = []
        
        content = adr['filepath'].read_text(encoding='utf-8')
        
        # Check required sections
        required_sections = ['Context', 'Decision', 'Consequences']
        for section in required_sections:
            if section not in content:
                issues.append(f"Missing '{section}' section")
        
        # Check date
        if not adr['date']:
            issues.append("No date in header")
        
        # Check status
        if adr['status'] not in manager.VALID_STATUSES:
            issues.append(f"Invalid status: {adr['status']}")
        
        if issues:
            print(f"\n⚠️  {adr['filepath'].name}")
            for issue in issues:
                print(f"   - {issue}")
        else:
            print(f"✅ {adr['filepath'].name}")


def main():
    parser = argparse.ArgumentParser(
        description='ADR - Architecture Decision Records',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 main.py create "Use Redis for caching"
  python3 main.py list
  python3 main.py update 1 --status accepted
  python3 main.py lint
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # create command
    create_parser = subparsers.add_parser('create', help='Create new ADR')
    create_parser.add_argument('title', help='ADR title')
    create_parser.add_argument('--status', default='proposed', 
                              choices=['proposed', 'accepted', 'rejected', 'deprecated', 'superseded'])
    create_parser.add_argument('--root', default='.', help='Project root')
    create_parser.set_defaults(func=run_create)
    
    # list command
    list_parser = subparsers.add_parser('list', help='List ADRs')
    list_parser.add_argument('--status', choices=['proposed', 'accepted', 'rejected', 'deprecated', 'superseded'])
    list_parser.add_argument('--root', default='.', help='Project root')
    list_parser.set_defaults(func=run_list)
    
    # update command
    update_parser = subparsers.add_parser('update', help='Update ADR status')
    update_parser.add_argument('number', type=int, help='ADR number')
    update_parser.add_argument('--status', required=True, choices=['proposed', 'accepted', 'rejected', 'deprecated', 'superseded'])
    update_parser.add_argument('--superseded-by', type=int, help='Superseding ADR number')
    update_parser.add_argument('--root', default='.', help='Project root')
    update_parser.set_defaults(func=run_update)
    
    # lint command
    lint_parser = subparsers.add_parser('lint', help='Lint ADRs')
    lint_parser.add_argument('--root', default='.', help='Project root')
    lint_parser.set_defaults(func=run_lint)
    
    args = parser.parse_args()
    
    if args.command is None:
        parser.print_help()
        sys.exit(1)
    
    args.func(args)


if __name__ == '__main__':
    main()
