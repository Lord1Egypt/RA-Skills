#!/usr/bin/env python3
"""
NCBI Search Skill Unit Tests

Test suite to verify database detection, rate limiting, and SQLite caching.
"""

import os
import sys
import unittest
import time
import shutil
import sqlite3

# Adjust paths to import our modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ncbi_utils import get_cached_response, set_cache_response, get_cache_key, rate_limit
import ncbi_utils
from ncbi_search import detect_database


class TestNCBISearchSkill(unittest.TestCase):
    
    def setUp(self):
        """Prepare isolation for tests."""
        # Isolate cache database to a test database
        self.original_cache_dir = ncbi_utils.CACHE_DIR
        self.original_cache_db = ncbi_utils.CACHE_DB_PATH
        
        self.test_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".test_ncbi_cache")
        ncbi_utils.CACHE_DIR = self.test_dir
        ncbi_utils.CACHE_DB_PATH = os.path.join(self.test_dir, "test_cache.db")
        
        # Clean potential leftovers
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
            
        os.makedirs(self.test_dir, exist_ok=True)
        
        # Ensure NCBI_NO_CACHE is not active during cache tests
        self.original_no_cache = os.environ.get("NCBI_NO_CACHE")
        if "NCBI_NO_CACHE" in os.environ:
            del os.environ["NCBI_NO_CACHE"]

    def tearDown(self):
        """Restore global states and clean up test files."""
        ncbi_utils.CACHE_DIR = self.original_cache_dir
        ncbi_utils.CACHE_DB_PATH = self.original_cache_db
        
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
            
        if self.original_no_cache is not None:
            os.environ["NCBI_NO_CACHE"] = self.original_no_cache
        elif "NCBI_NO_CACHE" in os.environ:
            del os.environ["NCBI_NO_CACHE"]

    def test_database_detection(self):
        """Test the intelligence and routing of detect_database."""
        # 1. dbSNP rs patterns
        self.assertEqual(detect_database("rs429358"), "snp")
        self.assertEqual(detect_database("Show me details of rs1112"), "snp")
        
        # 2. ClinVar VCV patterns
        self.assertEqual(detect_database("VCV000242862"), "clinvar")
        self.assertEqual(detect_database("clinvar variation VCV000012345"), "clinvar")
        
        # 3. Known Genes
        self.assertEqual(detect_database("APOE gene"), "gene")
        self.assertEqual(detect_database("BRCA1 expression"), "gene")
        
        # 4. Universal Gene Regex Match (un-hardcoded genes)
        self.assertEqual(detect_database("SHANK3 function"), "gene")
        self.assertEqual(detect_database("FMR1 mutation"), "gene")
        
        # 5. Gene/Disease combined with publication keywords -> PubMed
        self.assertEqual(detect_database("APOE review"), "pubmed")
        self.assertEqual(detect_database("SHANK3 paper on autism"), "pubmed")
        self.assertEqual(detect_database("COVID-19 vaccine clinical trial"), "pubmed")
        
        # 6. Database keywords
        self.assertEqual(detect_database("Escherichia coli taxonomy"), "taxonomy")
        self.assertEqual(detect_database("human protein sequence"), "protein")
        self.assertEqual(detect_database("yeast genome assembly"), "assembly")
        
        # 7. Default fallback to PubMed
        self.assertEqual(detect_database("flu treatment and prevention"), "pubmed")

    def test_sqlite_cache_write_and_read(self):
        """Test that data can be correctly saved to and loaded from local SQLite cache."""
        url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
        params = {"db": "pubmed", "term": "Alzheimer"}
        response_text = '{"esearchresult": {"count": "150000", "idlist": ["123", "456"]}}'
        
        # Verify first check is a miss
        self.assertIsNone(get_cached_response(url, params))
        
        # Set cache
        set_cache_response(url, params, response_text)
        
        # Verify second check is a hit
        cached = get_cached_response(url, params)
        self.assertEqual(cached, response_text)

    def test_cache_invalidation_by_no_cache_env(self):
        """Test that setting NCBI_NO_CACHE=1 bypasses caching."""
        os.environ["NCBI_NO_CACHE"] = "1"
        url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
        params = {"db": "pubmed", "term": "Alzheimer"}
        response_text = '{"some": "data"}'
        
        # Should not write to cache when disabled
        set_cache_response(url, params, response_text)
        self.assertIsNone(get_cached_response(url, params))

    def test_rate_limiting(self):
        """Test rate limiting interval mechanism."""
        # Temporarily shorten default interval to speed up tests, but keeping it measurable
        ncbi_utils.MIN_REQUEST_INTERVAL = 0.1
        
        start_time = time.time()
        rate_limit()  # 1st call
        rate_limit()  # 2nd call (should block until 0.1s elapsed)
        rate_limit()  # 3rd call (should block until 0.2s elapsed)
        duration = time.time() - start_time
        
        # The total time for 3 calls with 2 intervals of 0.1s should be at least 0.2s
        self.assertGreaterEqual(duration, 0.18)


if __name__ == "__main__":
    unittest.main()
