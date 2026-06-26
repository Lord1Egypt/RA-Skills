#!/usr/bin/env python3
import os
import re

# Get all actual post files
journal_dir = '/home/ubuntu/.zeroclaw/workspace/merxex-website/journal'
blog_dir = '/home/ubuntu/.zeroclaw/workspace/merxex-website/blog'

actual_posts = set()
for dirname in [journal_dir, blog_dir]:
    if os.path.exists(dirname):
        for f in os.listdir(dirname):
            if f.endswith('.html'):
                relpath = f"journal/{f}" if "journal" in dirname else f"blog/{f}"
                actual_posts.add(relpath)

# Get indexed posts from journal.html with better regex
indexed_posts = set()
with open('/home/ubuntu/.zeroclaw/workspace/merxex-website/journal.html', 'r') as f:
    content = f.read()
    
# Better regex pattern
pattern = r'href="((?:journal|blog)/[^"]+\.html)"'
matches = re.findall(pattern, content)
indexed_posts = set(matches)

print(f"Total actual posts: {len(actual_posts)}")
print(f"Total indexed posts: {len(indexed_posts)}")

# Find missing posts
missing = actual_posts - indexed_posts
print(f"Missing posts: {len(missing)}")
print(f"\nIndexed sample (first 5):")
for post in sorted(indexed_posts)[:5]:
    print(f"  {post}")
print(f"\nMissing sample (first 10):")
for post in sorted(missing)[:10]:
    print(f"  {post}")