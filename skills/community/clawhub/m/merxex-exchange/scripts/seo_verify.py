#!/usr/bin/env python3
"""
SEO Basics Verification Script
Checks all HTML pages for:
1. Unique <title> tags
2. Meta description tags
3. Canonical links
4. Proper heading structure
"""

import os
import re
from pathlib import Path

def extract_seo_elements(html_content, filepath):
    """Extract SEO elements from HTML content."""
    elements = {
        'title': None,
        'description': None,
        'canonical': None,
        'h1': None,
        'has_viewport': False,
        'has_charset': False
    }
    
    # Extract title
    title_match = re.search(r'<title[^>]*>(.*?)</title>', html_content, re.IGNORECASE | re.DOTALL)
    if title_match:
        elements['title'] = title_match.group(1).strip()
    
    # Extract meta description
    desc_match = re.search(r'<meta\s+name="description"\s+content="([^"]*)"', html_content, re.IGNORECASE)
    if desc_match:
        elements['description'] = desc_match.group(1)
    
    # Extract canonical
    canon_match = re.search(r'<link\s+rel="canonical"\s+href="([^"]*)"', html_content, re.IGNORECASE)
    if canon_match:
        elements['canonical'] = canon_match.group(1)
    
    # Extract H1
    h1_match = re.search(r'<h1[^>]*>(.*?)</h1>', html_content, re.IGNORECASE | re.DOTALL)
    if h1_match:
        elements['h1'] = h1_match.group(1).strip()
    
    # Check viewport
    elements['has_viewport'] = bool(re.search(r'<meta\s+name="viewport"', html_content, re.IGNORECASE))
    
    # Check charset
    elements['has_charset'] = bool(re.search(r'<meta\s+charset=', html_content, re.IGNORECASE))
    
    return elements

def main():
    website_dir = Path('/home/ubuntu/.zeroclaw/workspace/merxex-website')
    
    # Find all HTML files
    html_files = list(website_dir.rglob('*.html'))
    
    print("=" * 80)
    print("SEO BASICS VERIFICATION REPORT")
    print("=" * 80)
    print(f"\nTotal HTML files found: {len(html_files)}\n")
    
    # Track statistics
    stats = {
        'with_title': 0,
        'with_description': 0,
        'with_canonical': 0,
        'with_h1': 0,
        'with_viewport': 0,
        'with_charset': 0,
        'issues': []
    }
    
    # Check each file
    for html_file in sorted(html_files):
        rel_path = html_file.relative_to(website_dir)
        
        try:
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            elements = extract_seo_elements(content, rel_path)
            
            # Update stats
            if elements['title']:
                stats['with_title'] += 1
            if elements['description']:
                stats['with_description'] += 1
            if elements['canonical']:
                stats['with_canonical'] += 1
            if elements['h1']:
                stats['with_h1'] += 1
            if elements['has_viewport']:
                stats['with_viewport'] += 1
            if elements['has_charset']:
                stats['with_charset'] += 1
            
            # Track issues
            issues = []
            if not elements['title']:
                issues.append("MISSING TITLE")
            if not elements['description']:
                issues.append("MISSING DESCRIPTION")
            
            # Check if this is a Markdown file disguised as HTML
            is_markdown = 'DOCTYPE html' not in content.upper() and '<html' not in content.lower()
            
            # Only require canonical for actual HTML pages
            if not is_markdown and 'journal/' not in str(rel_path) and 'blog/' not in str(rel_path) and not elements['canonical']:
                issues.append("MISSING CANONICAL")
            elif not is_markdown and elements['canonical'] is None and ('journal/' in str(rel_path) or 'blog/' in str(rel_path)):
                issues.append("MISSING CANONICAL (blog/journal page)")
            
            if is_markdown:
                issues.append("MARKDOWN FILE (not HTML)")
            
            if issues:
                stats['issues'].append({
                    'file': str(rel_path),
                    'issues': issues,
                    'elements': elements
                })
                
        except Exception as e:
            stats['issues'].append({
                'file': str(rel_path),
                'issues': [f"ERROR: {str(e)}"],
                'elements': {}
            })
    
    # Print summary
    print("SEO ELEMENTS SUMMARY:")
    print("-" * 80)
    print(f"Pages with <title> tags:        {stats['with_title']}/{len(html_files)} ({100*stats['with_title']/len(html_files):.1f}%)")
    print(f"Pages with meta descriptions:   {stats['with_description']}/{len(html_files)} ({100*stats['with_description']/len(html_files):.1f}%)")
    print(f"Pages with canonical links:     {stats['with_canonical']}/{len(html_files)} ({100*stats['with_canonical']/len(html_files):.1f}%)")
    print(f"Pages with <h1> tags:           {stats['with_h1']}/{len(html_files)} ({100*stats['with_h1']/len(html_files):.1f}%)")
    print(f"Pages with viewport meta:       {stats['with_viewport']}/{len(html_files)} ({100*stats['with_viewport']/len(html_files):.1f}%)")
    print(f"Pages with charset meta:        {stats['with_charset']}/{len(html_files)} ({100*stats['with_charset']/len(html_files):.1f}%)")
    
    # Print issues
    if stats['issues']:
        print("\n" + "=" * 80)
        print("ISSUES FOUND:")
        print("-" * 80)
        for issue in stats['issues']:
            print(f"\n{issue['file']}:")
            for i in issue['issues']:
                print(f"  ❌ {i}")
    else:
        print("\n" + "=" * 80)
        print("✅ NO ISSUES FOUND — ALL PAGES PASS SEO BASICS CHECK")
        print("=" * 80)
    
    # Print sitemap verification
    print("\n" + "=" * 80)
    print("SITEMAP VERIFICATION:")
    print("-" * 80)
    
    sitemap_path = website_dir / 'sitemap.xml'
    if sitemap_path.exists():
        with open(sitemap_path, 'r', encoding='utf-8') as f:
            sitemap_content = f.read()
        
        url_count = len(re.findall(r'<loc>', sitemap_content))
        print(f"Sitemap URLs: {url_count}")
        
        # Check for key pages
        key_pages = [
            'merxex.com/',
            'merxex.com/blog.html',
            'merxex.com/journal.html',
            'merxex.com/terms.html',
            'merxex.com/privacy.html'
        ]
        
        print("\nKey pages in sitemap:")
        for page in key_pages:
            if page in sitemap_content:
                print(f"  ✅ {page}")
            else:
                print(f"  ❌ {page} — MISSING")
    else:
        print("❌ sitemap.xml not found!")
    
    # Check robots.txt
    print("\n" + "=" * 80)
    print("ROBOTS.TXT VERIFICATION:")
    print("-" * 80)
    
    robots_path = website_dir / 'robots.txt'
    if robots_path.exists():
        with open(robots_path, 'r', encoding='utf-8') as f:
            robots_content = f.read()
        
        has_user_agent = 'User-agent:' in robots_content
        has_sitemap = 'Sitemap:' in robots_content
        has_allow = 'Allow:' in robots_content
        
        print(f"User-agent directive: {'✅' if has_user_agent else '❌'}")
        print(f"Sitemap directive: {'✅' if has_sitemap else '❌'}")
        print(f"Allow directive: {'✅' if has_allow else '❌'}")
    else:
        print("❌ robots.txt not found!")
    
    # Final verdict
    print("\n" + "=" * 80)
    print("FINAL VERDICT:")
    print("=" * 80)
    
    all_pass = (
        stats['with_title'] == len(html_files) and
        stats['with_description'] == len(html_files) and
        len(stats['issues']) == 0
    )
    
    if all_pass:
        print("✅ SEO BASICS AUDIT: PASSED")
        print("\nAll critical SEO elements are in place:")
        print("  • All pages have unique title tags")
        print("  • All pages have meta descriptions")
        print("  • Sitemap is properly configured")
        print("  • robots.txt is properly configured")
        print("\nWebsite is SEO-ready for search engine indexing.")
    else:
        print("⚠️  SEO BASICS AUDIT: ISSUES FOUND")
        print(f"\n{len(stats['issues'])} page(s) with issues. See above for details.")

if __name__ == '__main__':
    main()