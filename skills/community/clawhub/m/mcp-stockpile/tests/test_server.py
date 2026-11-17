"""
Unit tests for Stockpile MCP Server.
"""

import json
import unittest
from mcp_stockpile.tools import TOOLS_METADATA, execute_tool
from mcp_stockpile.client import StockpileClient


class TestMCPServer(unittest.TestCase):
    def test_tools_metadata(self):
        """Verify tool metadata consistency and schemas."""
        self.assertGreaterEqual(len(TOOLS_METADATA), 20)
        names = [t["name"] for t in TOOLS_METADATA]
        self.assertIn("set_store_message_receiver", names)
        self.assertIn("add_store_item", names)
        self.assertIn("fulfill_order", names)
        self.assertIn("evaluate_item_collectibility", names)
        self.assertIn("run_inventory_sweep", names)

        for tool in TOOLS_METADATA:
            self.assertIn("name", tool)
            self.assertIn("description", tool)
            self.assertIn("inputSchema", tool)
            schema = tool["inputSchema"]
            self.assertEqual(schema.get("type"), "object")
            self.assertIn("properties", schema)

    def test_evaluate_item_collectibility(self):
        """Verify offline appraisal evaluation tool."""
        client = StockpileClient()
        result = execute_tool(
            "evaluate_item_collectibility",
            {
                "item_name": "First Edition Dune 1965",
                "category": "rare books",
                "condition": "Mint",
                "provenance_notes": "First printing signed archival"
            },
            client=client
        )
        self.assertIn("content", result)
        data = json.loads(result["content"][0]["text"])
        self.assertEqual(data["item_name"], "First Edition Dune 1965")
        self.assertGreaterEqual(data["rarity_score"], 90)
        self.assertIn("Grail", data["rarity_tier"])
        self.assertTrue(data["escrow_recommended"])


if __name__ == "__main__":
    unittest.main()
