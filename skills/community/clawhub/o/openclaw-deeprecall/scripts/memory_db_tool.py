#!/usr/bin/env python3
"""
memory_db_tool.py - Command-line interface for SQLite memory retrieval tools
Uses memory_retriever.py module-level functions for singleton access.
"""

import sys
import os
import json
import argparse
import asyncio
from pathlib import Path
from memory_retriever import MemoryRetriever, retrieve_l1_facts, retrieve_l2_raw, cleanup_raw_files, _get_retriever

def main():
    parser = argparse.ArgumentParser(description="SQLite memory database retrieval tool")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # search command
    search_parser = subparsers.add_parser("search", help="Search L1 structured facts")
    search_parser.add_argument("query", help="Search query (empty for latest)")
    search_parser.add_argument("--limit", type=int, default=5, help="Number of results (default: 5)")
    
    # read command
    read_parser = subparsers.add_parser("read", help="Read L2 raw archive")
    read_parser.add_argument("source_file", help="Source filename (e.g., 'example-project-update.md')")
    
    # stats command
    stats_parser = subparsers.add_parser("stats", help="Show database statistics")
    
    # cleanup command
    cleanup_parser = subparsers.add_parser("cleanup", help="Cleanup raw .md files (preserves database)")
    cleanup_parser.add_argument("--retention-days", type=int, default=1, 
                               help="Keep files newer than N days (default: 1)")
    cleanup_parser.add_argument("--max-size-kb", type=int, default=250,
                               help="Maximum total size in KB (default: 250)")
    cleanup_parser.add_argument("--dry-run", action="store_true",
                               help="Show what would be deleted without actually deleting")
    cleanup_parser.add_argument("--memory-dir", type=str,
                               help="Custom memory directory path (default: auto-detect)")
    
    # summarize command
    summarize_parser = subparsers.add_parser("summarize", help="Summarize memory files using LLM")
    summarize_parser.add_argument("--process-all", action="store_true",
                                 help="Process all unprocessed memory files")
    summarize_parser.add_argument("--process-file", type=str,
                                 help="Process a specific memory file")
    summarize_parser.add_argument("--no-store-raw", action="store_true",
                                 help="Do not store raw content to L2 archive")
    summarize_parser.add_argument("--test-config", action="store_true",
                                 help="Test OpenClaw configuration and API connectivity")
    
    args = parser.parse_args()
    
    if args.command == "search":
        result = retrieve_l1_facts(args.query, args.limit)
        print(result)
    
    elif args.command == "read":
        result = retrieve_l2_raw(args.source_file)
        print(result)
    
    elif args.command == "stats":
        retriever = _get_retriever()
        stats = retriever.get_table_stats()
        print(json.dumps(stats, indent=2, ensure_ascii=False))
    
    elif args.command == "cleanup":
        print("=== Memory File Cleanup ===\n")
        print("IMPORTANT: This only cleans raw .md session files in workspace/memory/")
        print("           L1/L2 data in memory.db is PERMANENT and will NOT be affected.\n")
        
        if args.dry_run:
            print("DRY RUN MODE: No files will be deleted.\n")
        
        # Execute cleanup (supports dry-run)
        result = cleanup_raw_files(
            retention_days=args.retention_days,
            max_size_kb=args.max_size_kb,
            memory_dir=args.memory_dir,
            dry_run=args.dry_run
        )
        
        # Display results
        print("Cleanup Summary:")
        print(f"  Status: {result.get('status', 'unknown')}")
        
        if result.get('status') in ['skipped', 'dry_run', 'completed']:
            if result.get('reason'):
                print(f"  Reason: {result['reason']}")
            
            print(f"  Memory Directory: {result.get('memory_dir', 'unknown')}")
            print(f"  Config: {result.get('config', {}).get('retention_days', args.retention_days)} day(s), "
                  f"{result.get('config', {}).get('max_size_kb', args.max_size_kb)} KB max")
            
            if 'total_files_before' in result:
                print(f"  Total Files Before: {result['total_files_before']}")
                print(f"  Total Size Before: {result['total_size_before_kb']:.2f} KB")
                print(f"  Files {'to Delete' if args.dry_run else 'Deleted'}: {result['deleted_files_count']}")
                print(f"  Size {'to Free' if args.dry_run else 'Freed'}: {result['deleted_size_kb']:.2f} KB")
                print(f"  Remaining Files: {result['remaining_files_count']}")
                print(f"  Remaining Size: {result['remaining_size_kb']:.2f} KB")
                
                if result.get("deleted_files"):
                    print(f"\n  Files {'that would be deleted' if args.dry_run else 'deleted'}:")
                    for filename in result["deleted_files"][:10]:  # Limit display count
                        print(f"    - {filename}")
                    if len(result["deleted_files"]) > 10:
                        print(f"    ... and {len(result['deleted_files']) - 10} more")
        else:
            print(f"  Error: {result.get('reason', 'Unknown error')}")
    
    elif args.command == "summarize":
        # Import summarizer and run async function
        try:
            from memory_summarizer import DeepRecallSummarizer
            
            summarizer = DeepRecallSummarizer()
            
            if args.test_config:
                # Test configuration using the unified method
                summarizer.test_configuration()
            
            elif args.process_all:
                store_raw = not args.no_store_raw
                print(f"Processing all files (store_raw: {store_raw})...")
                stats = asyncio.run(summarizer.process_all_files(store_raw=store_raw))
                print("\nSummarization Complete:")
                print(f"  Files processed: {stats['files_processed']}")
                print(f"  Facts extracted: {stats['facts_extracted']}")
                print(f"  Facts stored: {stats['facts_stored']}")
                print(f"  Raw content stored: {stats['raw_content_stored']}")
            
            elif args.process_file:
                store_raw = not args.no_store_raw
                print(f"Processing file: {args.process_file} (store_raw: {store_raw})...")
                
                file_path = Path(args.process_file)
                if not file_path.is_absolute():
                    file_path = Path(summarizer.memory_dir) / file_path
                
                success = asyncio.run(summarizer.process_single_file(file_path, store_raw))
                if success:
                    print("File processed successfully")
                else:
                    print("File processing failed")
                    sys.exit(1)
            
            else:
                print("Please specify an action for summarize command:")
                print("  --process-all     Process all unprocessed files")
                print("  --process-file    Process a specific file")
                print("  --test-config     Test OpenClaw configuration")
        
        except ImportError as e:
            print(f"Error importing summarizer: {e}")
            print("Make sure memory_summarizer.py is in the same directory")
            sys.exit(1)
    
    else:
        parser.print_help()

if __name__ == "__main__":
    main()