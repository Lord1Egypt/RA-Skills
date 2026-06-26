#!/usr/bin/env python3
"""
Identify missing posts and generate index entries for journal.html
"""
import os
import re
from datetime import datetime

journal_dir = '/home/ubuntu/.zeroclaw/workspace/merxex-website/journal'
blog_dir = '/home/ubuntu/.zeroclaw/workspace/merxex-website/blog'
journal_html = '/home/ubuntu/.zeroclaw/workspace/merxex-website/journal.html'

# Get all actual post files
def get_all_posts():
    posts = {}
    for dirname, prefix in [(journal_dir, 'journal'), (blog_dir, 'blog')]:
        if os.path.exists(dirname):
            for f in os.listdir(dirname):
                if f.endswith('.html'):
                    relpath = f"{prefix}/{f}"
                    posts[relpath] = {
                        'full_path': os.path.join(dirname, f),
                        'prefix': prefix,
                        'filename': f
                    }
    return posts

# Get indexed posts from journal.html
def get_indexed_posts():
    indexed = set()
    broken = []
    with open(journal_html, 'r') as f:
        content = f.read()
    
    pattern = r'href="((?:journal|blog)/[^"]+\.html)"'
    matches = re.findall(pattern, content)
    indexed = set(matches)
    
    # Check for broken links (referenced but don't exist)
    all_posts = get_all_posts()
    for idx in indexed:
        if idx not in all_posts:
            broken.append(idx)
    
    return indexed, broken

# Extract post title from HTML file
def extract_title(filepath):
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Try to find title in <title> tag
    title_match = re.search(r'<title>([^<]+)</title>', content)
    if title_match:
        return title_match.group(1).strip()
    
    # Try to find title in h1 tag
    h1_match = re.search(r'<h1[^>]*>([^<]+)</h1>', content)
    if h1_match:
        return h1_match.group(1).strip()
    
    # Fallback: use filename
    filename = os.path.basename(filepath)
    return filename.replace('.html', '').replace('-', ' ').title()

# Extract excerpt from HTML file
def extract_excerpt(filepath, max_length=300):
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Try to find excerpt in p tag
    p_matches = re.findall(r'<p>([^<]+)</p>', content)
    if p_matches:
        excerpt = p_matches[0].strip()
        if len(excerpt) > max_length:
            excerpt = excerpt[:max_length-1] + '...'
        return excerpt
    
    # Fallback: use title
    return extract_title(filepath)

# Generate index entry for a post
def generate_index_entry(post_path):
    full_path = post_path.split('/')[-1]
    prefix = post_path.split('/')[0]
    
    # Get title and excerpt
    file_path = os.path.join(f'/home/ubuntu/.zeroclaw/workspace/merxex-website/{prefix}', full_path)
    title = extract_title(file_path)
    excerpt = extract_excerpt(file_path)
    
    # Extract date from filename if present
    date_match = re.match(r'(\d{4}-\d{2}-\d{2})', full_path)
    if date_match:
        date_str = date_match.group(1)
        try:
            dt = datetime.strptime(date_str, '%Y-%m-%d')
            formatted_date = dt.strftime('%B %d, %Y')
        except:
            formatted_date = date_str
    else:
        formatted_date = 'Unknown date'
    
    # Determine badge type
    if 'security' in title.lower() or 'vulnerability' in title.lower():
        badge_type = 'technical'
        badge_label = 'Security'
    elif 'lesson' in title.lower() or 'learned' in title.lower():
        badge_type = 'lessons'
        badge_label = 'Lessons Learned'
    elif 'update' in title.lower() or 'audit' in title.lower():
        badge_type = 'update'
        badge_label = 'Update'
    else:
        badge_type = 'update'
        badge_label = 'Post'
    
    return f'''            <article class="journal-post-card">
                <div>
                    <span class="journal-post-badge {badge_type}">{badge_label}</span>
                    <div class="journal-post-header">
                        <h2 class="journal-post-title">
                            <a href="{post_path}" class="journal-post-link">
                                {title}
                            </a>
                        </h2>
                    </div>
                    <div class="journal-post-meta">
                        <span>📅 {formatted_date}</span>
                        <span>⏱️ 5 min read</span>
                    </div>
                    <p class="journal-post-excerpt">
                        {excerpt}
                    </p>
                </div>
            </article>
'''

# Main execution
if __name__ == '__main__':
    print("=== Journal Index Audit ===\n")
    
    all_posts = get_all_posts()
    indexed, broken = get_indexed_posts()
    
    print(f"Total actual posts: {len(all_posts)}")
    print(f"Total indexed posts: {len(indexed)}")
    print(f"Broken links: {len(broken)}")
    
    missing = set(all_posts.keys()) - indexed
    print(f"Missing posts: {len(missing)}")
    
    if broken:
        print("\n=== BROKEN LINKS ===")
        for b in sorted(broken):
            print(f"  ❌ {b}")
    
    if missing:
        print("\n=== MISSING POSTS ===")
        for m in sorted(missing):
            print(f"  🔍 {m}")
        
        print("\n=== GENERATED INDEX ENTRIES ===")
        for m in sorted(missing):
            print(generate_index_entry(m))
            print()
    
    # Summary
    print("\n=== SUMMARY ===")
    if not missing and not broken:
        print("✅ All posts indexed, no broken links!")
    else:
        if broken:
            print(f"⚠️  {len(broken)} broken link(s) to fix")
        if missing:
            print(f"⚠️  {len(missing)} missing post(s) to index")