#!/usr/bin/env python3
"""
Pattern Miner - Simple pattern analysis for user data files
"""

import json
import sys
from collections import Counter

def analyze_json(filepath):
    """Analyze a JSON file for patterns."""
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        print(f"Analyzing: {filepath}")
        print(f"Data type: {type(data).__name__}")
        
        if isinstance(data, list):
            print(f"Items count: {len(data)}")
            if len(data) > 0:
                print(f"Sample keys: {list(data[0].keys()) if isinstance(data[0], dict) else 'N/A'}")
        elif isinstance(data, dict):
            print(f"Keys: {list(data.keys())}")
        
        print("\nAnalysis complete.")
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

def main():
    if len(sys.argv) < 2:
        print("Usage: python analyze.py <file.json>")
        sys.exit(1)
    
    filepath = sys.argv[1]
    analyze_json(filepath)

if __name__ == "__main__":
    main()
