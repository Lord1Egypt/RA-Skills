"""Tests for mcp_server — MCP tool registration."""

import os
import pytest


class TestMCPModule:
    def test_importable(self):
        """MCP server module should be importable."""
        import mcp_server
        assert hasattr(mcp_server, "MemoryGuardianServer")

    def test_server_class_has_handlers(self):
        """Server class should have tool handler methods."""
        import mcp_server
        server = mcp_server.MemoryGuardianServer(".")
        assert hasattr(server, "handle_memory_status")
        assert hasattr(server, "handle_memory_query")
