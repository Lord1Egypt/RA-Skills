#!/usr/bin/env python3
"""
Batch search processor - Efficiently search multiple queries
"""

import sys
import os
import json
import time
import argparse
from pathlib import Path
from typing import List, Dict
from concurrent.futures import ThreadPoolExecutor, as_completed
from search import SearchEngine

class BatchSearch:
    """Process multiple search queries efficiently"""
    
    def __init__(self, max_workers: int = 3):
        self.engine = SearchEngine()
        self.max_workers = max_workers
        self.results = []
        self.metrics = {
            "total_queries": 0,
            "successful": 0,
            "failed": 0,
            "total_time": 0,
            "cache_hits": 0,
            "estimated_cost": 0.0
        }
    
    def search_single(self, query: str, num_results: int = 5) -> Dict:
        """Search single query with timing"""
        start_time = time.time()
        
        try:
            result = self.engine.search(query, num_results, use_cache=True)
            elapsed = time.time() - start_time
            
            # Update metrics
            if "error" not in result:
                self.metrics["successful"] += 1
                if result.get("cache_hit"):
                    self.metrics["cache_hits"] += 1
                self.metrics["estimated_cost"] += result.get("cost_estimate", 0.0)
            else:
                self.metrics["failed"] += 1
            
            result["processing_time_ms"] = int(elapsed * 1000)
            return result
            
        except Exception as e:
            elapsed = time.time() - start_time
            self.metrics["failed"] += 1
            return {
                "query": query,
                "error": str(e),
                "processing_time_ms": int(elapsed * 1000)
            }
    
    def process_file(self, input_file: str, output_file: str = None, 
                    num_results: int = 5, parallel: bool = True):
        """Process queries from file"""
        
        # Read queries
        queries = self.read_queries(input_file)
        self.metrics["total_queries"] = len(queries)
        
        print(f"[INFO] Processing {len(queries)} queries...", file=sys.stderr)
        
        start_time = time.time()
        
        if parallel and len(queries) > 1:
            self.process_parallel(queries, num_results)
        else:
            self.process_sequential(queries, num_results)
        
        total_time = time.time() - start_time
        self.metrics["total_time"] = total_time
        
        # Calculate additional metrics
        self.metrics["avg_time_per_query"] = total_time / len(queries) if queries else 0
        self.metrics["cache_hit_rate"] = (self.metrics["cache_hits"] / len(queries)) * 100 if queries else 0
        self.metrics["success_rate"] = (self.metrics["successful"] / len(queries)) * 100 if queries else 0
        
        # Output results
        output = {
            "metadata": self.metrics,
            "queries": queries,
            "results": self.results,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        
        if output_file:
            with open(output_file, 'w') as f:
                json.dump(output, f, indent=2)
            print(f"[INFO] Results saved to {output_file}", file=sys.stderr)
        
        # Print summary
        self.print_summary()
        
        return output
    
    def process_parallel(self, queries: List[str], num_results: int):
        """Process queries in parallel"""
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all tasks
            future_to_query = {
                executor.submit(self.search_single, query, num_results): query 
                for query in queries
            }
            
            # Collect results as they complete
            for future in as_completed(future_to_query):
                query = future_to_query[future]
                try:
                    result = future.result(timeout=60)
                    self.results.append(result)
                    print(f"[OK] Completed: {query[:50]}...", file=sys.stderr)
                except Exception as e:
                    print(f"[ERROR] Failed: {query[:50]}... - {e}", file=sys.stderr)
                    self.results.append({
                        "query": query,
                        "error": str(e)
                    })
    
    def process_sequential(self, queries: List[str], num_results: int):
        """Process queries one by one"""
        for i, query in enumerate(queries, 1):
            print(f"[{i}/{len(queries)}] Searching: {query[:50]}...", file=sys.stderr)
            
            result = self.search_single(query, num_results)
            self.results.append(result)
            
            # Small delay to respect rate limits
            if i < len(queries):
                time.sleep(0.5)
    
    def read_queries(self, input_file: str) -> List[str]:
        """Read queries from various file formats"""
        path = Path(input_file)
        
        if not path.exists():
            print(f"[ERROR] File not found: {input_file}", file=sys.stderr)
            return []
        
        queries = []
        
        # Try different formats
        if path.suffix.lower() == '.json':
            with open(path) as f:
                data = json.load(f)
                if isinstance(data, list):
                    queries = [str(q) for q in data if q]
                elif isinstance(data, dict) and 'queries' in data:
                    queries = [str(q) for q in data['queries'] if q]
        
        elif path.suffix.lower() in ['.csv', '.tsv']:
            import csv
            delimiter = ',' if path.suffix.lower() == '.csv' else '\t'
            with open(path) as f:
                reader = csv.reader(f, delimiter=delimiter)
                for row in reader:
                    if row and row[0].strip():
                        queries.append(row[0].strip())
        
        else:  # Assume text file, one query per line
            with open(path) as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):  # Skip comments
                        queries.append(line)
        
        # Deduplicate while preserving order
        seen = set()
        deduped = []
        for q in queries:
            if q not in seen:
                seen.add(q)
                deduped.append(q)
        
        print(f"[INFO] Read {len(queries)} queries, {len(deduped)} unique", file=sys.stderr)
        return deduped
    
    def print_summary(self):
        """Print batch processing summary"""
        print("\n" + "="*60, file=sys.stderr)
        print("BATCH SEARCH SUMMARY", file=sys.stderr)
        print("="*60, file=sys.stderr)
        
        metrics = self.metrics
        print(f"Total queries:      {metrics['total_queries']}", file=sys.stderr)
        print(f"Successful:         {metrics['successful']} ({metrics['success_rate']:.1f}%)", file=sys.stderr)
        print(f"Failed:             {metrics['failed']}", file=sys.stderr)
        print(f"Cache hits:         {metrics['cache_hits']} ({metrics['cache_hit_rate']:.1f}%)", file=sys.stderr)
        print(f"Total time:         {metrics['total_time']:.2f}s", file=sys.stderr)
        print(f"Avg time/query:     {metrics['avg_time_per_query']:.2f}s", file=sys.stderr)
        print(f"Estimated cost:     ${metrics['estimated_cost']:.4f}", file=sys.stderr)
        print(f"Cost per query:     ${metrics['estimated_cost']/metrics['total_queries']:.6f}" 
              if metrics['total_queries'] > 0 else "Cost per query:     $0.000000", file=sys.stderr)
        
        # Method distribution
        methods = {}
        for result in self.results:
            if "method" in result:
                method = result["method"]
                methods[method] = methods.get(method, 0) + 1
        
        if methods:
            print("\nMethod distribution:", file=sys.stderr)
            for method, count in sorted(methods.items(), key=lambda x: x[1], reverse=True):
                percentage = (count / metrics['total_queries']) * 100
                print(f"  {method:15} {count:4} ({percentage:.1f}%)", file=sys.stderr)
        
        print("="*60, file=sys.stderr)

def main():
    parser = argparse.ArgumentParser(description="Batch search processor")
    parser.add_argument("input", help="Input file with queries (txt, csv, json)")
    parser.add_argument("-o", "--output", help="Output JSON file")
    parser.add_argument("-n", "--num-results", type=int, default=5, 
                       help="Number of results per query")
    parser.add_argument("--parallel", type=int, default=3,
                       help="Number of parallel workers (default: 3)")
    parser.add_argument("--sequential", action="store_true",
                       help="Process sequentially instead of parallel")
    
    args = parser.parse_args()
    
    batch = BatchSearch(max_workers=args.parallel)
    
    result = batch.process_file(
        input_file=args.input,
        output_file=args.output,
        num_results=args.num_results,
        parallel=not args.sequential
    )
    
    # Print first few results as example
    if result["results"]:
        print("\nFirst result example:", file=sys.stderr)
        first_result = result["results"][0]
        if "error" not in first_result:
            print(json.dumps({
                "query": first_result.get("query"),
                "method": first_result.get("method"),
                "num_results": len(first_result.get("results", [])),
                "cache_hit": first_result.get("cache_hit", False)
            }, indent=2))

if __name__ == "__main__":
    main()