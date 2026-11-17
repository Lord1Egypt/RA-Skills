"""
Unit tests for Stockpile API client.
"""

import unittest
from mcp_stockpile.client import StockpileClient


class TestStockpileClient(unittest.TestCase):
    def test_client_init_defaults(self):
        client = StockpileClient()
        self.assertEqual(client.base_url, "https://stockpile.market/api")
        self.assertEqual(client.api_key, "")

    def test_client_init_custom(self):
        client = StockpileClient(base_url="http://localhost:8000/api/", api_key="sk_live_test_123")
        self.assertEqual(client.base_url, "http://localhost:8000/api")
        self.assertEqual(client.api_key, "sk_live_test_123")


if __name__ == "__main__":
    unittest.main()
