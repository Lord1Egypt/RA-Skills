#!/usr/bin/env python3
"""
Image extraction and download script for obsidian-save-article skill.
Downloads images from a webpage and saves them to a local folder.
"""

import os
import re
import hashlib
import urllib.request
import urllib.error
from urllib.parse import urljoin, urlparse
from html import unescape
import sys
import json

def get_url_hash(url):
    """Generate a short hash for URL to use as filename."""
    return hashlib.md5(url.encode()).hexdigest()[:12]

def is_valid_image_url(url):
    """Check if URL is a valid image link."""
    if not url:
        return False
    # Skip data URLs, javascript, etc.
    if url.startswith('data:') or url.startswith('javascript:') or url.startswith('mailto:'):
        return False
    # Check for image extension or Content-Type hint
    parsed = urlparse(url)
    path = parsed.path.lower()
    image_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg', '.bmp', '.ico')
    return any(path.endswith(ext) for ext in image_extensions) or 'image' in parsed.query

def download_image(url, save_dir, timeout=10):
    """
    Download an image from URL and save to save_dir.
    Returns the local filename if successful, None otherwise.
    """
    try:
        # Create headers to mimic browser
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        req = urllib.request.Request(url, headers=headers)
        
        with urllib.request.urlopen(req, timeout=timeout) as response:
            content = response.read()
            content_type = response.headers.get('Content-Type', '')
            
            # Determine extension
            ext = '.jpg'
            if 'png' in content_type:
                ext = '.png'
            elif 'gif' in content_type:
                ext = '.gif'
            elif 'webp' in content_type:
                ext = '.webp'
            elif 'svg' in content_type:
                ext = '.svg'
            elif 'bmp' in content_type:
                ext = '.bmp'
            elif not any(content_type.startswith(t) for t in ['image/', 'application/octet-stream']):
                # Not a valid image
                return None
            
            # Generate filename
            url_hash = get_url_hash(url)
            filename = f"img-{url_hash}{ext}"
            filepath = os.path.join(save_dir, filename)
            
            # Save file
            with open(filepath, 'wb') as f:
                f.write(content)
            
            return filename
            
    except Exception as e:
        print(f"Failed to download {url}: {e}", file=sys.stderr)
        return None

def extract_images_from_html(html_content, base_url):
    """
    Extract image URLs from HTML content.
    Returns a list of unique image URLs found in the content.
    """
    image_urls = set()
    
    # Pattern to find img tags
    img_pattern = re.compile(r'<img[^>]+src=["\']([^"\']+)["\']', re.IGNORECASE)
    
    for match in img_pattern.finditer(html_content):
        src = match.group(1)
        # Resolve relative URLs
        full_url = urljoin(base_url, unescape(src))
        image_urls.add(full_url)
    
    # Also find images in style="background-image: url(...)"
    bg_pattern = re.compile(r'background-image:\s*url\(["\']?([^"\')]+)["\']?\)', re.IGNORECASE)
    for match in bg_pattern.finditer(html_content):
        src = match.group(1)
        full_url = urljoin(base_url, unescape(src))
        if is_valid_image_url(full_url):
            image_urls.add(full_url)
    
    return list(image_urls)

def process_article(url, output_dir, images_subdir='images'):
    """
    Main function to fetch article, extract images, and prepare for markdown conversion.
    
    Returns a dict with:
    - html: Full HTML content
    - images: List of (original_url, local_filename) pairs
    - markdown: HTML converted to markdown (images as local refs)
    """
    print(f"Fetching article from: {url}", file=sys.stderr)
    
    # First, try to fetch raw HTML for image extraction
    html_content = None
    try:
        # Fetch raw HTML using a simple request
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
        })
        with urllib.request.urlopen(req, timeout=30) as response:
            html_content = response.read().decode('utf-8', errors='ignore')
            print(f"Fetched raw HTML, length: {len(html_content)}", file=sys.stderr)
    except Exception as e:
        print(f"Failed to fetch raw HTML: {e}", file=sys.stderr)
    
    # Also get markdown content via Jina.ai
    markdown_content = ""
    try:
        jina_url = f"https://r.jina.ai/{url}"
        req = urllib.request.Request(jina_url, headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        })
        with urllib.request.urlopen(req, timeout=30) as response:
            markdown_content = response.read().decode('utf-8')
    except Exception as e:
        print(f"Failed to fetch via Jina: {e}", file=sys.stderr)
    
    # Extract images from HTML
    image_urls = []
    if html_content:
        image_urls = extract_images_from_html(html_content, url)
        print(f"Found {len(image_urls)} images from HTML", file=sys.stderr)
    else:
        # Fallback: try to extract from markdown
        import re
        img_pattern = re.compile(r'!\[([^\]]*)\]\(([^)]+)\)')
        for match in img_pattern.finditer(markdown_content):
            img_url = match.group(2)
            if not img_url.startswith('data:'):
                full_url = urljoin(url, img_url)
                image_urls.append(full_url)
        print(f"Found {len(image_urls)} images from Markdown", file=sys.stderr)
    
    # Create images directory
    images_dir = os.path.join(output_dir, images_subdir)
    os.makedirs(images_dir, exist_ok=True)
    
    # Download images
    downloaded_images = []
    for img_url in image_urls:
        if is_valid_image_url(img_url):
            local_name = download_image(img_url, images_dir)
            if local_name:
                downloaded_images.append((img_url, local_name))
                print(f"Downloaded: {local_name}", file=sys.stderr)
    
    # Replace image URLs in markdown with local paths
    final_markdown = replace_image_urls_in_markdown(markdown_content, downloaded_images, url, images_subdir)
    
    return {
        'html': html_content or '',
        'images': downloaded_images,
        'markdown': final_markdown or markdown_content
    }

def convert_html_to_markdown_with_local_images(html, downloaded_images, images_subdir):
    """
    Convert HTML to Markdown, replacing image URLs with local paths.
    """
    # Create a mapping of original URL to local filename
    url_to_local = {orig: local for orig, local in downloaded_images}
    
    # Replace img src with local paths
    def replace_img_src(match):
        src = match.group(1)
        # Resolve relative URLs
        full_url = urljoin('', unescape(src))  # base is empty, so this just unescapes
        
        if full_url in url_to_local:
            local_file = url_to_local[full_url]
            return f'src="{images_subdir}/{local_file}"'
        return match.group(0)
    
    markdown = re.sub(r'<img[^>]+src=["\']([^"\']+)["\']', replace_img_src, markdown)
    
    # Clean up HTML tags but keep images
    # This is a simple conversion - for better results, consider using a proper HTML-to-Markdown library
    markdown = clean_html_to_markdown(markdown)
    
    return markdown

def replace_image_urls_in_markdown(markdown, downloaded_images, base_url, images_subdir):
    """
    Replace image URLs in markdown with local paths.
    """
    if not downloaded_images:
        return markdown
    
    # Create mapping of original URL to local filename
    url_to_local = {}
    for orig_url, local_name in downloaded_images:
        # Normalize the original URL for matching
        normalized_orig = orig_url
        url_to_local[normalized_orig] = local_name
        
    # Replace markdown image syntax: ![alt](url)
    def replace_markdown_img(match):
        alt_text = match.group(1) or ''
        img_url = match.group(2)
        
        # Resolve relative URL
        full_url = urljoin(base_url, img_url)
        
        # Check if we have a local version
        if full_url in url_to_local:
            local_name = url_to_local[full_url]
            return f'![{alt_text}]({images_subdir}/{local_name})'
        
        # Also try the original URL without resolution
        if img_url in url_to_local:
            local_name = url_to_local[img_url]
            return f'![{alt_text}]({images_subdir}/{local_name})'
        
        return match.group(0)
    
    result = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', replace_markdown_img, markdown)
    return result

def clean_html_to_markdown(html):
    """Simple HTML to Markdown conversion."""
    # Remove script and style tags
    html = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL | re.IGNORECASE)
    html = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.DOTALL | re.IGNORECASE)
    
    # Convert common HTML elements to Markdown
    # This is simplified - real implementation might use a library like html2text
    
    return html

if __name__ == '__main__':
    # Example usage: python script.py <url> <output_dir>
    if len(sys.argv) >= 3:
        url = sys.argv[1]
        output_dir = sys.argv[2]
        result = process_article(url, output_dir)
        print(json.dumps(result))
    else:
        print("Usage: python script.py <url> <output_dir>", file=sys.stderr)
        sys.exit(1)
