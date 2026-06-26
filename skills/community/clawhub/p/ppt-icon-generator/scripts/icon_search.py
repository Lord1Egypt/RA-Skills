#!/usr/bin/env python3
"""
Icon Search - Search and download icons from Iconify API
"""

import argparse
import json
import os
import sys
import urllib.request
import urllib.parse
from pathlib import Path

ICONIFY_API = "https://api.iconify.design"

def search_icons(query, limit=10, style=None):
    """Search icons from Iconify API"""
    try:
        # Search endpoint
        url = f"{ICONIFY_API}/search?query={urllib.parse.quote(query)}&limit={limit}"
        
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))
            return data.get('icons', [])
    except Exception as e:
        print(f"❌ Search failed: {e}")
        return []

def get_icon_info(icon_name):
    """Get icon details"""
    try:
        url = f"{ICONIFY_API}/{icon_name}.json"
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0'
        })
        
        with urllib.request.urlopen(req, timeout=10) as response:
            return json.loads(response.read().decode('utf-8'))
    except Exception as e:
        print(f"❌ Failed to get icon info: {e}")
        return None

def download_icon_png(icon_name, output_path, size=512, color=None):
    """Download icon as PNG"""
    try:
        # Build URL
        parts = icon_name.split(':')
        if len(parts) != 2:
            print(f"❌ Invalid icon name format: {icon_name}")
            return False
        
        prefix, name = parts
        
        # Try different endpoints
        urls = [
            f"{ICONIFY_API}/{prefix}/{name}.svg",
            f"https://api.simplesvg.com/{prefix}/{name}.svg"
        ]
        
        svg_content = None
        for url in urls:
            try:
                req = urllib.request.Request(url, headers={
                    'User-Agent': 'Mozilla/5.0'
                })
                with urllib.request.urlopen(req, timeout=10) as response:
                    svg_content = response.read().decode('utf-8')
                    break
            except:
                continue
        
        if not svg_content:
            print(f"❌ Could not download SVG for {icon_name}")
            return False
        
        # Convert SVG to PNG using cairosvg if available
        try:
            import cairosvg
            cairosvg.svg2png(bytestring=svg_content.encode('utf-8'), 
                           write_to=output_path,
                           output_width=size,
                           output_height=size)
            print(f"✅ Downloaded: {output_path}")
            return True
        except ImportError:
            # Fallback: save SVG
            svg_output = output_path.replace('.png', '.svg')
            with open(svg_output, 'w') as f:
                f.write(svg_content)
            print(f"⚠️  Saved as SVG (install cairosvg for PNG): {svg_output}")
            return True
            
    except Exception as e:
        print(f"❌ Download failed: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description='Search and download icons')
    parser.add_argument('--query', '-q', required=True, help='Search query')
    parser.add_argument('--limit', '-l', type=int, default=10, help='Number of results')
    parser.add_argument('--download', '-d', action='store_true', help='Download first result')
    parser.add_argument('--output', '-o', help='Output file path')
    parser.add_argument('--size', '-s', type=int, default=512, help='Icon size')
    
    args = parser.parse_args()
    
    print(f"🔍 Searching for: {args.query}")
    icons = search_icons(args.query, args.limit)
    
    if not icons:
        print("❌ No icons found")
        return 1
    
    print(f"\n📋 Found {len(icons)} icons:\n")
    for i, icon in enumerate(icons[:args.limit], 1):
        print(f"  {i}. {icon}")
    
    if args.download:
        if not args.output:
            safe_name = args.query.replace(' ', '_').lower()
            args.output = f"{safe_name}_icon.png"
        
        print(f"\n⬇️  Downloading: {icons[0]}")
        if download_icon_png(icons[0], args.output, args.size):
            print(f"✅ Saved to: {os.path.abspath(args.output)}")
            return 0
        return 1
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
