#!/usr/bin/env python3
"""
Documentation Generator - README Updater

Updates README with generated content.
"""

import re
from pathlib import Path
from typing import Optional


class READMEUpdater:
    """Updates README.md with generated content"""

    def __init__(self, root_path: str):
        self.root = Path(root_path).resolve()
        self.readme_path = self.root / 'README.md'

    def update_toc(self, max_depth: int = 3) -> str:
        """Update table of contents"""
        if not self.readme_path.exists():
            return "README.md not found"

        content = self.readme_path.read_text(encoding='utf-8')

        # Find existing TOC
        toc_pattern = r'## Table of Contents.*?(?=\n## |\Z)'
        existing_toc = re.search(toc_pattern, content, re.DOTALL)

        # Generate new TOC
        toc = self._generate_toc(content, max_depth)

        if existing_toc:
            # Replace existing TOC
            new_content = content[:existing_toc.start()] + toc + content[existing_toc.end():]
        else:
            # Insert after first heading
            first_heading = re.search(r'^# .+$', content, re.MULTILINE)
            if first_heading:
                insert_pos = first_heading.end()
                new_content = content[:insert_pos] + '\n\n' + toc + content[insert_pos:]
            else:
                new_content = toc + '\n\n' + content

        self.readme_path.write_text(new_content, encoding='utf-8')
        return f"✅ Updated table of contents in README.md"

    def _generate_toc(self, content: str, max_depth: int) -> str:
        """Generate table of contents from headings"""
        lines = ["## Table of Contents", ""]

        # Find all headings
        heading_pattern = r'^(#{2,4})\s+(.+)$'

        for match in re.finditer(heading_pattern, content, re.MULTILINE):
            level = len(match.group(1))
            title = match.group(2).strip()

            if level > max_depth + 1:  # +1 because we skip H1
                continue

            # Skip the TOC heading itself
            if title == "Table of Contents":
                continue

            # Generate anchor
            anchor = self._generate_anchor(title)

            # Indent based on level
            indent = "  " * (level - 2)
            lines.append(f"{indent}- [{title}](#{anchor})")

        return "\n".join(lines)

    def _generate_anchor(self, title: str) -> str:
        """Generate GitHub-style anchor from heading"""
        # Remove code backticks
        anchor = title.replace('`', '')
        # Convert to lowercase
        anchor = anchor.lower()
        # Replace spaces with hyphens
        anchor = anchor.replace(' ', '-')
        # Remove special characters
        anchor = re.sub(r'[^\w\-]', '', anchor)
        return anchor

    def insert_api_docs(self, api_docs_path: str) -> str:
        """Insert API docs into README"""
        if not self.readme_path.exists():
            return "README.md not found"

        api_path = Path(api_docs_path)
        if not api_path.exists():
            return f"API docs not found: {api_docs_path}"

        content = self.readme_path.read_text(encoding='utf-8')
        api_content = api_path.read_text(encoding='utf-8')

        # Find or create API section
        api_section_pattern = r'## API.*?(?=\n## |\Z)'
        existing_api = re.search(api_section_pattern, content, re.DOTALL)

        new_section = f"## API Reference\n\nSee [API Documentation]({api_docs_path})\n"

        if existing_api:
            new_content = content[:existing_api.start()] + new_section + content[existing_api.end():]
        else:
            new_content = content + '\n\n' + new_section

        self.readme_path.write_text(new_content, encoding='utf-8')
        return f"✅ Added API reference to README.md"


def main():
    import argparse

    parser = argparse.ArgumentParser(description='README Updater')
    parser.add_argument('--root', '-r', default='.', help='Project root')
    parser.add_argument('--update-toc', action='store_true', help='Update table of contents')
    parser.add_argument('--insert-api', help='Insert API docs reference')

    args = parser.parse_args()

    updater = READMEUpdater(args.root)

    if args.update_toc:
        print(updater.update_toc())
    elif args.insert_api:
        print(updater.insert_api_docs(args.insert_api))
    else:
        print("No action specified. Use --update-toc or --insert-api")


if __name__ == '__main__':
    main()
