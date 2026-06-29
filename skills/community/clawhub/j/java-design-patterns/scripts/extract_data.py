#!/usr/bin/env python3
"""从 firecrawl JSON 结果中提取模式页面数据"""
import json
import os
import re
import sys

FILE = os.path.expanduser(
    "~/.claude/projects/-Users-wufengsheng/48ef65f3-98db-4f7c-9d95-36c1815729f5/"
    "tool-results/mcp-firecrawl-mcp-firecrawl_crawl-1782351365733.txt"
)
DATA_DIR = os.path.expanduser("~/.claude/skills/java-design-patterns/data")
os.makedirs(DATA_DIR, exist_ok=True)

SKIP_SLUGS = {
    "cqrs", "dao", "fluentinterface", "layers", "microservices-aggregator",
    "reader-writer-lock", "thread-pool"
}

CATEGORY_MAP = {
    "Architectural": "architectural",
    "Behavioral": "behavioral",
    "Concurrency": "concurrency",
    "Creational": "creational",
    "Data access": "data-access",
    "Functional": "functional",
    "Integration": "integration",
    "Resilience": "resilience",
    "Testing": "testing",
    "Messaging": "messaging",
    "Performance optimization": "performance-optimization",
    "Resource management": "resource-management",
    "Idiom": "idiom",
    "Service Discovery": "service-discovery",
}

with open(FILE, 'r', encoding='utf-8') as f:
    raw = f.read()

# Treat as raw JSON
try:
    data = json.loads(raw)
except json.JSONDecodeError as e:
    print(f"JSON parse error: {e}", file=sys.stderr)
    # Try to clean up: replace control characters
    cleaned = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', '', raw)
    data = json.loads(cleaned)

saved = 0
mapping_lines = []

for entry in data.get('data', []):
    meta = entry.get('metadata', {})
    url = meta.get('sourceURL', '') or meta.get('url', '')
    markdown = entry.get('markdown', '')
    category = meta.get('articleSection', '')

    if not url or url == 'https://java-design-patterns.com/patterns/':
        continue

    # Extract slug
    slug = url.replace('https://java-design-patterns.com/patterns/', '').rstrip('/')
    if not slug:
        continue

    # Skip invalid slugs
    if '.html' in slug or ':' in slug or slug in SKIP_SLUGS:
        continue

    # Save markdown
    filepath = os.path.join(DATA_DIR, f"{slug}.md")
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(markdown)
    saved += 1

    # Build category mapping
    if category:
        dir_name = CATEGORY_MAP.get(category, 'uncategorized')
        mapping_lines.append(f"{dir_name}|{slug}")

# Save category mapping
mapping_path = os.path.join(DATA_DIR, 'category-mapping.txt')
with open(mapping_path, 'w', encoding='utf-8') as f:
    f.write('\n'.join(mapping_lines))

print(f"Saved: {saved} markdown files")
print(f"Category mapping: {len(mapping_lines)} entries")
