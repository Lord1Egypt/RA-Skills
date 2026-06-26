#!/usr/bin/env python3
"""Batch process multiple papers with error handling and logging."""

import sys
import os
import json
import time
from pathlib import Path
from datetime import datetime

# Import local modules
sys.path.insert(0, str(Path(__file__).parent))
from extract_paper import extract
from read_table import read_headers
from write_table import write_row


def setup_logging(output_dir):
    """Setup logging for batch processing."""
    log_file = Path(output_dir) / f"batch_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    return log_file


def process_single_paper(paper_path, table_path, headers, domain, log_file):
    """Process a single paper with full error handling."""
    result = {
        'paper': str(paper_path),
        'status': 'pending',
        'timestamp': datetime.now().isoformat(),
        'extraction': {},
        'errors': [],
        'warnings': []
    }
    
    try:
        # Step 1: Extract text
        print(f"Processing: {paper_path.name}")
        extraction = extract(str(paper_path), structured=True)
        
        if extraction.startswith("[ERROR:"):
            result['status'] = 'failed'
            result['errors'].append(f"Extraction failed: {extraction}")
            return result
        
        try:
            extraction_data = json.loads(extraction)
        except json.JSONDecodeError:
            extraction_data = {'full_text': extraction, 'sections': {}}
        
        result['extraction'] = {
            'text_length': len(extraction_data.get('full_text', '')),
            'sections_found': list(extraction_data.get('sections', {}).keys()),
            'metadata': extraction_data.get('metadata', {})
        }
        
        # Step 2: LLM extraction (this would be called by the main agent)
        # For now, we just prepare the data
        result['status'] = 'extracted'
        result['llm_input'] = {
            'headers': headers,
            'domain': domain,
            'paper_text': extraction_data.get('full_text', '')[:5000]  # First 5000 chars for preview
        }
        
        return result
        
    except Exception as e:
        result['status'] = 'failed'
        result['errors'].append(f"Unexpected error: {str(e)}")
        return result


def batch_process(papers_dir, table_path, output_dir=None):
    """Process all papers in a directory."""
    papers_path = Path(papers_dir)
    table_path = Path(table_path)
    
    # Setup output directory
    if output_dir is None:
        output_dir = papers_path / "output"
    output_dir = Path(output_dir)
    output_dir.mkdir(exist_ok=True)
    
    # Setup logging
    log_file = setup_logging(output_dir)
    
    # Read table headers
    table_info = read_headers(str(table_path))
    if isinstance(table_info, list) and table_info[0].startswith("[ERROR:"):
        print(f"Error reading table: {table_info[0]}")
        return
    
    headers = table_info['headers']
    domain = table_info['domain']
    
    print(f"Table domain: {domain}")
    print(f"Headers: {', '.join(headers)}")
    print(f"Log file: {log_file}")
    print("-" * 60)
    
    # Find all papers
    supported_extensions = {'.pdf', '.docx', '.txt'}
    papers = [f for f in papers_path.iterdir() if f.suffix.lower() in supported_extensions]
    
    if not papers:
        print(f"No papers found in {papers_dir}")
        return
    
    print(f"Found {len(papers)} papers to process")
    print("-" * 60)
    
    # Process each paper
    results = []
    success_count = 0
    failed_count = 0
    
    for i, paper in enumerate(papers, 1):
        print(f"\n[{i}/{len(papers)}] ", end="")
        
        result = process_single_paper(paper, table_path, headers, domain, log_file)
        results.append(result)
        
        if result['status'] == 'extracted':
            success_count += 1
            print("✓")
        else:
            failed_count += 1
            print("✗")
            if result['errors']:
                print(f"  Errors: {'; '.join(result['errors'])}")
        
        # Save progress log after each paper
        with open(log_file, 'w', encoding='utf-8') as f:
            json.dump({
                'batch_info': {
                    'total': len(papers),
                    'success': success_count,
                    'failed': failed_count,
                    'timestamp': datetime.now().isoformat()
                },
                'results': results
            }, f, ensure_ascii=False, indent=2)
        
        # Brief pause to avoid overwhelming the system
        time.sleep(0.1)
    
    # Final summary
    print("\n" + "=" * 60)
    print("BATCH PROCESSING COMPLETE")
    print("=" * 60)
    print(f"Total papers: {len(papers)}")
    print(f"Successful: {success_count}")
    print(f"Failed: {failed_count}")
    print(f"Log saved to: {log_file}")
    
    return results


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: batch_process.py <papers_directory> <table_path> [output_directory]", file=sys.stderr)
        sys.exit(1)
    
    papers_dir = sys.argv[1]
    table_path = sys.argv[2]
    output_dir = sys.argv[3] if len(sys.argv) > 3 else None
    
    batch_process(papers_dir, table_path, output_dir)
