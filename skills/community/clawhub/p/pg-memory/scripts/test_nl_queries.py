#!/usr/bin/env python3
"""
Simple NL Search Test for pg-memory v2.5.0
Tests natural language to SQL conversion without needing database connection.
"""

import sys
sys.path.insert(0, '~/.openclaw/workspace/skills/pg-memory/scripts')

from nl_query import NLQueryEngine, preview_sql

def test_nl_queries():
    """Test natural language query generation."""
    
    test_queries = [
        "Show me high importance observations from last week",
        "Find all observations tagged with docker",
        "What did I work on yesterday",
        "List active projects from this month",
        "Show me critical decisions from Q1",
        "Find observations with status resolved",
    ]
    
    print("=" * 70)
    print("pg-memory v2.5.0 - Natural Language Query Test")
    print("=" * 70)
    print()
    
    engine = NLQueryEngine()
    
    for i, query in enumerate(test_queries, 1):
        print(f"Test {i}: {query}")
        print("-" * 70)
        
        try:
            sql = engine.generate_sql(query)
            print(f"Generated SQL:")
            print(f"  {sql}")
            print()
        except Exception as e:
            print(f"Error: {e}")
            print()
    
    print("=" * 70)
    print("Tests complete!")
    print()
    print("To test with live database:")
    print("  python3 -c \"from nl_query import ask; print(ask('your question here'))\"")

if __name__ == "__main__":
    test_nl_queries()
