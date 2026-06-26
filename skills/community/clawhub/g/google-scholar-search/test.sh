#!/bin/bash
# Test script for Google Scholar Search skill

echo "=== Test 1: Basic Search ==="
python3 scripts/search_papers.py "machine learning" --limit 2
echo ""

echo "=== Test 2: Search with Year Filter ==="
python3 scripts/search_papers.py "deep learning" --year 2022-2024 --limit 2
echo ""

echo "=== Test 3: Search JSON Output ==="
python3 scripts/search_papers.py "neural networks" --json --limit 1
echo ""

echo "=== Test 4: Search with Min Citations ==="
python3 scripts/search_papers.py "quantum computing" --min-citations 100 --limit 2
echo ""

echo "All tests completed!"
