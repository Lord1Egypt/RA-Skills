#!/usr/bin/env python3
"""
OCR Extract Tool
Extract text from images using Tesseract OCR
"""

import subprocess
import sys
import os
import argparse
import re
from pathlib import Path

def run_tesseract(image_path, lang='chi_sim+eng', output_file=None):
    """Run Tesseract OCR on an image"""
    try:
        cmd = ['tesseract', image_path]
        
        if output_file:
            # Output to file (without extension)
            base_name = str(Path(output_file).with_suffix(''))
            cmd.extend([base_name, '-l', lang])
        else:
            # Output to stdout
            cmd.extend(['stdout', '-l', lang])
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding='utf-8',
            check=True
        )
        
        if output_file:
            # Tesseract adds .txt extension automatically
            txt_file = f"{base_name}.txt"
            if os.path.exists(txt_file):
                with open(txt_file, 'r', encoding='utf-8') as f:
                    return f.read()
            else:
                return f"OCR completed, but output file not found: {txt_file}"
        else:
            return result.stdout
            
    except subprocess.CalledProcessError as e:
        return f"Error running Tesseract: {e.stderr}"
    except FileNotFoundError:
        return "Error: Tesseract not found. Please install Tesseract OCR."
    except Exception as e:
        return f"Unexpected error: {str(e)}"

def extract_financial_info(text):
    """Extract financial information from OCR text"""
    info = {
        'companies': [],
        'stock_codes': [],
        'financial_metrics': [],
        'keywords': []
    }
    
    # Extract company names (Chinese companies often end with 股份, 科技, 集团, etc.)
    company_patterns = [
        r'#([^\s#]+)',  # Hashtags
        r'【([^】]+)】',  # Brackets
        r'([\u4e00-\u9fa5A-Za-z0-9]+股份)',  # Company names
        r'([\u4e00-\u9fa5A-Za-z0-9]+科技)',
        r'([\u4e00-\u9fa5A-Za-z0-9]+集团)'
    ]
    
    for pattern in company_patterns:
        matches = re.findall(pattern, text)
        info['companies'].extend(matches)
    
    # Extract stock codes (e.g., 000001.SZ, 600000.SH)
    stock_codes = re.findall(r'(\d{6}\.[A-Z]{2,4})', text)
    info['stock_codes'] = list(set(stock_codes))
    
    # Extract financial metrics
    metric_patterns = [
        r'同比增长\s*([0-9.]+%)',
        r'利润\s*([0-9.]+亿元)',
        r'增长\s*([0-9.]+%)',
        r'合同\s*([0-9.]+亿元)',
        r'中标\s*([^\s]+)'
    ]
    
    for pattern in metric_patterns:
        matches = re.findall(pattern, text)
        info['financial_metrics'].extend(matches)
    
    # Extract keywords
    keywords = ['公告', '知道', '商业航天', '智能电网', '机器人', '绿色电力', 
                '电气', '设备', '应用', '领域', '电力设施']
    found_keywords = [kw for kw in keywords if kw in text]
    info['keywords'] = found_keywords
    
    # Remove duplicates
    info['companies'] = list(set(info['companies']))
    
    return info

def analyze_image(image_path, lang='chi_sim+eng', detailed=False):
    """Analyze image and extract structured information"""
    print(f"Analyzing: {image_path}")
    
    # Extract text
    text = run_tesseract(image_path, lang)
    
    if text.startswith("Error"):
        print(text)
        return None
    
    # Extract financial information
    info = extract_financial_info(text)
    
    # Print results
    print("\n" + "="*50)
    print("OCR ANALYSIS REPORT")
    print("="*50)
    
    print(f"\n📊 Summary:")
    print(f"  Companies found: {len(info['companies'])}")
    print(f"  Stock codes: {len(info['stock_codes'])}")
    print(f"  Financial metrics: {len(info['financial_metrics'])}")
    print(f"  Keywords: {len(info['keywords'])}")
    
    if info['companies']:
        print(f"\n🏢 Companies:")
        for company in info['companies'][:10]:  # Limit to 10
            print(f"  • {company}")
    
    if info['stock_codes']:
        print(f"\n📈 Stock Codes:")
        for code in info['stock_codes'][:10]:  # Limit to 10
            print(f"  • {code}")
    
    if info['financial_metrics']:
        print(f"\n💰 Financial Metrics:")
        for metric in info['financial_metrics'][:10]:  # Limit to 10
            print(f"  • {metric}")
    
    if info['keywords']:
        print(f"\n🔑 Keywords:")
        for keyword in info['keywords']:
            print(f"  • {keyword}")
    
    if detailed:
        print(f"\n📝 Full Text (first 1000 chars):")
        print(text[:1000] + "..." if len(text) > 1000 else text)
    
    print("\n" + "="*50)
    
    return {
        'text': text,
        'info': info
    }

def main():
    parser = argparse.ArgumentParser(description='OCR Tool for extracting text from images')
    parser.add_argument('image', help='Path to image file')
    parser.add_argument('--lang', default='chi_sim+eng', help='Language for OCR (default: chi_sim+eng)')
    parser.add_argument('--output', '-o', help='Output file for extracted text')
    parser.add_argument('--detailed', '-d', action='store_true', help='Show detailed output including full text')
    parser.add_argument('--extract-only', '-e', action='store_true', help='Only extract text, no analysis')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.image):
        print(f"Error: Image file not found: {args.image}")
        sys.exit(1)
    
    if args.extract_only:
        # Just extract text
        text = run_tesseract(args.image, args.lang, args.output)
        if args.output:
            print(f"Text extracted to: {args.output}")
        else:
            print(text)
    else:
        # Full analysis
        analyze_image(args.image, args.lang, args.detailed)

if __name__ == '__main__':
    main()