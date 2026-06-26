#!/usr/bin/env python3
"""
Get Chapter PDF from Philippines Tariff Commission website.
Handles Google Drive links and WAF protection.
"""

import sys
import os
import re
import time
import subprocess
from urllib.parse import urlparse, parse_qs


def extract_file_id_from_gdrive_url(url: str) -> str:
    """Extract Google Drive file ID from various URL formats."""
    # Format 1: https://drive.google.com/file/d/{FILE_ID}/view
    match = re.search(r'/file/d/([a-zA-Z0-9_-]+)', url)
    if match:
        return match.group(1)
    
    # Format 2: https://drive.google.com/open?id={FILE_ID}
    parsed = urlparse(url)
    if 'open' in parsed.path:
        qs = parse_qs(parsed.query)
        if 'id' in qs:
            return qs['id'][0]
    
    return None


def download_from_gdrive(file_id: str, output_path: str) -> bool:
    """Download file from Google Drive using curl."""
    download_url = f"https://drive.google.com/uc?export=download&id={file_id}"
    
    try:
        result = subprocess.run([
            "curl", "-s", "-L", "-A", 
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "-o", output_path, download_url
        ], capture_output=True, text=True, timeout=120)
        
        # Check if file was downloaded and is valid PDF
        if os.path.exists(output_path) and os.path.getsize(output_path) > 10000:
            with open(output_path, 'rb') as f:
                header = f.read(4)
                if header == b'%PDF':
                    return True
                else:
                    # Might be a confirmation page for large files
                    with open(output_path, 'r', errors='ignore') as f:
                        content = f.read(5000)
                        if 'confirm' in content.lower() or 'download' in content.lower():
                            print("Note: Large file requires confirmation. Trying alternative method...")
                            return download_large_file(file_id, output_path)
        
        return False
    except Exception as e:
        print(f"Error downloading: {e}")
        return False


def download_large_file(file_id: str, output_path: str) -> bool:
    """Download large files from Google Drive (requires confirmation)."""
    # For large files, use wget which handles confirmations better
    try:
        download_url = f"https://drive.google.com/uc?export=download&id={file_id}"
        result = subprocess.run([
            "wget", "--quiet", "--no-check-certificate",
            "-O", output_path, download_url
        ], capture_output=True, timeout=120)
        
        if os.path.exists(output_path) and os.path.getsize(output_path) > 10000:
            with open(output_path, 'rb') as f:
                header = f.read(4)
                if header == b'%PDF':
                    return True
        return False
    except Exception as e:
        print(f"Error with large file download: {e}")
        return False


def get_gdrive_link_with_playwright(chapter: str) -> str:
    """
    Use Playwright to click Chapter link and get Google Drive URL.
    Returns the Google Drive URL or empty string if failed.
    """
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("Error: playwright not installed. Install with: pip install playwright")
        print("Then run: playwright install chromium")
        return ""
    
    chapter_padded = chapter.zfill(2)
    target_text = f"Chapter {chapter_padded}"
    
    print(f"Opening browser to find {target_text}...")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Show browser for transparency
        page = browser.new_page(viewport={"width": 1400, "height": 900})
        
        try:
            # Navigate to tariff book page
            page.goto("https://www.tariffcommission.gov.ph/tariff-book-2022")
            page.wait_for_load_state("domcontentloaded")
            time.sleep(2)
            
            # Find and click the Chapter link
            print(f"Looking for {target_text} link...")
            
            # Try to find the link by text
            link = page.locator("a", has_text=target_text).first
            
            if link.count() == 0:
                # Try partial match
                link = page.locator(f"text={target_text}").first
            
            if link.count() > 0:
                # Get the href attribute
                href = link.get_attribute("href")
                print(f"Found link: {href}")
                
                # Check if it's a Google Drive link
                if href and "drive.google.com" in href:
                    browser.close()
                    return href
                else:
                    # Navigate to the link
                    print(f"Navigating to: {href}")
                    page.goto(href)
                    page.wait_for_load_state("domcontentloaded")
                    time.sleep(2)
                    
                    # Return current URL
                    current_url = page.url
                    browser.close()
                    return current_url
            else:
                print(f"Could not find {target_text} link")
                return ""
                
        except Exception as e:
            print(f"Error: {e}")
            return ""
        finally:
            try:
                browser.close()
            except:
                pass


def download_chapter(chapter: str, output_dir: str = ".") -> dict:
    """
    Download a Chapter PDF.
    
    Args:
        chapter: Chapter number (1-97)
        output_dir: Directory to save the PDF
        
    Returns:
        Dictionary with success status, file path, and source URL
    """
    chapter_padded = chapter.zfill(2)
    output_path = os.path.join(output_dir, f"Chapter_{chapter_padded}.pdf")
    
    # Step 1: Get Google Drive link using Playwright
    gdrive_url = get_gdrive_link_with_playwright(chapter)
    
    if not gdrive_url:
        return {
            "success": False,
            "file_path": "",
            "source_url": "",
            "error": "Could not get Google Drive link"
        }
    
    # Step 2: Extract file ID and download
    file_id = extract_file_id_from_gdrive_url(gdrive_url)
    
    if not file_id:
        return {
            "success": False,
            "file_path": "",
            "source_url": gdrive_url,
            "error": "Could not extract file ID from URL"
        }
    
    print(f"Downloading Chapter {chapter_padded}...")
    
    if download_from_gdrive(file_id, output_path):
        file_size = os.path.getsize(output_path)
        print(f"✓ Downloaded: {output_path} ({file_size/1024:.1f} KB)")
        return {
            "success": True,
            "file_path": output_path,
            "source_url": gdrive_url,
            "file_size": file_size
        }
    else:
        return {
            "success": False,
            "file_path": "",
            "source_url": gdrive_url,
            "error": "Download failed - may need manual download"
        }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: get_chapter_pdf.py <chapter_number> [output_directory]")
        print("\nExamples:")
        print("  python3 get_chapter_pdf.py 85")
        print("  python3 get_chapter_pdf.py 85 ./downloads")
        sys.exit(1)
    
    chapter = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "."
    
    result = download_chapter(chapter, output_dir)
    
    if result["success"]:
        print(f"\n✓ Success!")
        print(f"  File: {result['file_path']}")
        print(f"  Source: {result['source_url']}")
    else:
        print(f"\n✗ Failed: {result.get('error', 'Unknown error')}")
        if result.get('source_url'):
            print(f"  Manual download: {result['source_url']}")
        sys.exit(1)
