#!/usr/bin/env python3
"""
SEO Audit Script for merxex.com
Checks: titles, meta descriptions, H1 tags, canonical URLs, internal links, external links
"""

import re
import os
import json

BASE_PATH = "/home/ubuntu/.zeroclaw/workspace/merxex-website"

def analyze_html(filepath):
    """Analyze a single HTML file for SEO elements."""
    rel_path = os.path.relpath(filepath, BASE_PATH)
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check title
        title_match = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE | re.DOTALL)
        title = title_match.group(1).strip() if title_match else "MISSING"
        title_length = len(title) if title != "MISSING" else 0
        
        # Check meta description
        desc_match = re.search(r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']', content, re.IGNORECASE | re.DOTALL)
        description = desc_match.group(1).strip() if desc_match else "MISSING"
        desc_length = len(description) if description != "MISSING" else 0
        
        # Check meta keywords
        keywords_match = re.search(r'<meta\s+name=["\']keywords["\']\s+content=["\'](.*?)["\']', content, re.IGNORECASE | re.DOTALL)
        keywords = keywords_match.group(1).strip() if keywords_match else "MISSING"
        
        # Check canonical
        canonical_match = re.search(r'<link\s+rel=["\']canonical["\']\s+href=["\'](.*?)["\']', content, re.IGNORECASE)
        canonical = canonical_match.group(1) if canonical_match else "MISSING"
        
        # Check H1
        h1_matches = re.findall(r'<h1[^>]*>(.*?)</h1>', content, re.IGNORECASE | re.DOTALL)
        h1 = h1_matches[0].strip() if h1_matches else "MISSING"
        h1_count = len(h1_matches)
        
        # Count internal links (relative paths)
        internal_links = re.findall(r'href=["\'](/[^"\']*|[^"\']*\.html)["\']', content)
        internal_unique = set(link.strip('"\'') for link in internal_links)
        
        # Count external links
        external_links = re.findall(r'href=["\']https?://[^"\']+["\']', content)
        external_unique = set(external_links)
        
        # Check robots meta
        robots_match = re.search(r'<meta\s+name=["\']robots["\']\s+content=["\'](.*?)["\']', content, re.IGNORECASE)
        robots = robots_match.group(1) if robots_match else "index, follow (default)"
        
        # Check Open Graph tags
        og_title = re.search(r'<meta\s+property=["\']og:title["\']\s+content=["\'](.*?)["\']', content, re.IGNORECASE)
        og_title = og_title.group(1).strip() if og_title else "MISSING"
        
        og_desc = re.search(r'<meta\s+property=["\']og:description["\']\s+content=["\'](.*?)["\']', content, re.IGNORECASE | re.DOTALL)
        og_desc = og_desc.group(1).strip() if og_desc else "MISSING"
        
        og_url = re.search(r'<meta\s+property=["\']og:url["\']\s+content=["\'](.*?)["\']', content, re.IGNORECASE)
        og_url = og_url.group(1) if og_url else "MISSING"
        
        # Check for alt text on images
        images = re.findall(r'<img[^>]*>', content)
        images_without_alt = []
        for img in images:
            if 'alt=' not in img.lower():
                # Extract src for identification
                src_match = re.search(r'src=["\']([^"\']+)["\']', img)
                images_without_alt.append(src_match.group(1) if src_match else "unknown")
        
        return {
            'path': rel_path,
            'title': title,
            'title_length': title_length,
            'description': description,
            'description_length': desc_length,
            'keywords': keywords,
            'canonical': canonical,
            'h1': h1,
            'h1_count': h1_count,
            'internal_links': len(internal_unique),
            'internal_unique': list(internal_unique)[:10],  # First 10
            'external_links': len(external_unique),
            'robots': robots,
            'og_title': og_title,
            'og_description': og_desc,
            'og_url': og_url,
            'images_without_alt': images_without_alt,
            'issues': []
        }
    except Exception as e:
        return {'path': rel_path, 'error': str(e)}

def check_issues(data):
    """Check for SEO issues in the analyzed data."""
    issues = []
    
    if 'error' in data:
        return ['Parse error: ' + data['error']]
    
    # Title checks
    if data['title'] == "MISSING":
        issues.append("❌ Missing title tag")
    elif data['title_length'] < 30:
        issues.append(f"⚠️ Title too short ({data['title_length']} chars, recommend 30-60)")
    elif data['title_length'] > 60:
        issues.append(f"⚠️ Title too long ({data['title_length']} chars, recommend 30-60)")
    
    # Description checks
    if data['description'] == "MISSING":
        issues.append("❌ Missing meta description")
    elif data['description_length'] < 120:
        issues.append(f"⚠️ Description too short ({data['description_length']} chars, recommend 120-160)")
    elif data['description_length'] > 160:
        issues.append(f"⚠️ Description too long ({data['description_length']} chars, recommend 120-160)")
    
    # H1 checks
    if data['h1'] == "MISSING":
        issues.append("❌ Missing H1 tag")
    elif data['h1_count'] > 1:
        issues.append(f"⚠️ Multiple H1 tags ({data['h1_count']}, should be 1)")
    
    # Canonical checks
    if data['canonical'] == "MISSING":
        issues.append("⚠️ Missing canonical tag")
    
    # Robots checks
    if 'noindex' in data['robots'].lower():
        issues.append(f"⚠️ Page set to noindex: {data['robots']}")
    
    # Image alt checks
    if data['images_without_alt']:
        issues.append(f"⚠️ {len(data['images_without_alt'])} image(s) missing alt text")
    
    return issues

def main():
    """Main SEO audit function."""
    html_files = []
    
    # Find all HTML files
    for root, dirs, files in os.walk(BASE_PATH):
        # Skip hidden directories
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        
        for file in files:
            if file.endswith('.html'):
                html_files.append(os.path.join(root, file))
    
    print("=" * 80)
    print("SEO AUDIT REPORT — merxex.com")
    print("=" * 80)
    print(f"\n📊 Total HTML files analyzed: {len(html_files)}\n")
    
    results = {}
    for filepath in sorted(html_files):
        data = analyze_html(filepath)
        if 'error' not in data:
            data['issues'] = check_issues(data)
        results[data['path']] = data
    
    # Summary statistics
    missing_title = sum(1 for r in results.values() if r.get('title') == "MISSING")
    missing_desc = sum(1 for r in results.values() if r.get('description') == "MISSING")
    missing_h1 = sum(1 for r in results.values() if r.get('h1') == "MISSING")
    missing_canonical = sum(1 for r in results.values() if r.get('canonical') == "MISSING")
    noindex_pages = sum(1 for r in results.values() if 'noindex' in r.get('robots', '').lower())
    
    print("📈 SUMMARY STATISTICS")
    print("-" * 80)
    print(f"✅ Pages with title: {len(results) - missing_title}/{len(results)}")
    print(f"✅ Pages with description: {len(results) - missing_desc}/{len(results)}")
    print(f"✅ Pages with H1: {len(results) - missing_h1}/{len(results)}")
    print(f"✅ Pages with canonical: {len(results) - missing_canonical}/{len(results)}")
    print(f"⚠️  Pages with noindex: {noindex_pages}/{len(results)}")
    
    # Critical issues
    critical_pages = {path: data for path, data in results.items() if data.get('issues')}
    
    if critical_pages:
        print(f"\n❌ PAGES WITH CRITICAL ISSUES ({len(critical_pages)})")
        print("-" * 80)
        for path, data in sorted(critical_pages.items()):
            print(f"\n📄 {path}")
            for issue in data['issues']:
                print(f"   {issue}")
    
    # Main pages detail
    main_pages = ['index.html', 'waitlist.html', 'blog.html', 'journal.html', 'audit.html', 
                  'docs.html', 'aup.html', 'disputes.html', 'privacy.html', 'terms.html']
    
    print(f"\n\n📑 MAIN PAGES SEO DETAILS")
    print("-" * 80)
    
    for page in main_pages:
        if page in results:
            data = results[page]
            if 'error' in data:
                print(f"\n📄 {page}: ERROR - {data['error']}")
                continue
            
            status = "✅" if not data['issues'] else "⚠️"
            print(f"\n{status} {page}")
            print(f"   Title ({data['title_length']} chars): {data['title']}")
            
            desc_display = data['description'][:80] + "..." if data['description'] != "MISSING" and len(data['description']) > 80 else data['description']
            print(f"   Description ({data['description_length']} chars): {desc_display}")
            
            print(f"   H1: {data['h1'][:60]}..." if len(data.get('h1', '')) > 60 else f"   H1: {data['h1']}")
            print(f"   Canonical: {data['canonical']}")
            print(f"   Robots: {data['robots']}")
            print(f"   Internal links: {data['internal_links']} | External links: {data['external_links']}")
            
            if data['issues']:
                print(f"   Issues:")
                for issue in data['issues']:
                    print(f"     - {issue}")
    
    # Check for broken internal links (links to non-existent files)
    print(f"\n\n🔗 INTERNAL LINK ANALYSIS")
    print("-" * 80)
    
    all_internal_links = set()
    for data in results.values():
        if 'internal_unique' in data:
            all_internal_links.update(data['internal_unique'])
    
    existing_files = set(os.path.basename(p) for p in html_files)
    existing_files.add('')  # Root path
    
    broken_links = []
    for link in all_internal_links:
        # Extract filename from path
        if link.startswith('/'):
            filename = os.path.basename(link)
        else:
            filename = link
        
        # Check if file exists
        if filename and not filename.startswith('?') and not filename.startswith('#'):
            # Check in base directory or subdirectories
            found = False
            for root, dirs, files in os.walk(BASE_PATH):
                if filename in files:
                    found = True
                    break
            if not found:
                broken_links.append(link)
    
    if broken_links:
        print(f"⚠️  Potentially broken internal links ({len(broken_links)}):")
        for link in sorted(broken_links)[:10]:
            print(f"   - {link}")
    else:
        print("✅ No obviously broken internal links detected")
    
    # Recommendations
    print(f"\n\n💡 RECOMMENDATIONS")
    print("-" * 80)
    
    recommendations = []
    
    if missing_title > 0:
        recommendations.append(f"1. Add title tags to {missing_title} page(s)")
    
    if missing_desc > 0:
        recommendations.append(f"2. Add meta descriptions to {missing_desc} page(s)")
    
    if missing_h1 > 0:
        recommendations.append(f"3. Add H1 tags to {missing_h1} page(s)")
    
    if missing_canonical > 0:
        recommendations.append(f"4. Add canonical tags to {missing_canonical} page(s)")
    
    if noindex_pages > 5:
        recommendations.append(f"5. Review {noindex_pages} pages with noindex — ensure intentional")
    
    if broken_links:
        recommendations.append(f"6. Fix {len(broken_links)} broken internal link(s)")
    
    if not recommendations:
        recommendations.append("✅ SEO basics are solid! Consider:")
        recommendations.append("   - Add more internal links between related blog/journal posts")
        recommendations.append("   - Implement breadcrumb navigation")
        recommendations.append("   - Add schema.org markup for blog posts (Article type)")
        recommendations.append("   - Create XML sitemap index if blog grows beyond 50 posts")
    
    for rec in recommendations:
        print(rec)
    
    # Save report
    report_path = os.path.join(BASE_PATH, "seo_audit_report.json")
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, default=str)
    
    print(f"\n\n📝 Full report saved to: {report_path}")

if __name__ == "__main__":
    main()