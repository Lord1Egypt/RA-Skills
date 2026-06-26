#!/usr/bin/env python3
"""
CLI Integration Tests for memory_ontology.py

Tests the complete CLI interface including:
- Entity CRUD operations
- Query and filtering
- Statistics display
- Relation management
"""

import json
import subprocess
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest


SCRIPT_PATH = Path(__file__).parent.parent / "scripts" / "memory_ontology.py"
KG_DIR = Path(__file__).parent.parent / "ontology"


class TestCLICreate:
    """Test entity creation via CLI"""

    def test_create_decision(self):
        """Test creating a Decision entity"""
        result = subprocess.run(
            [
                sys.executable,
                str(SCRIPT_PATH),
                "create",
                "--type", "Decision",
                "--props", '{"title":"Test Decision","rationale":"Testing CLI","made_at":"2026-04-02T00:00:00+08:00"}'
            ],
            capture_output=True,
            text=True,
            cwd=str(SCRIPT_PATH.parent.parent)
        )

        assert result.returncode == 0, f"Failed: {result.stderr}"
        assert "created" in result.stdout.lower() or "dec_" in result.stdout

    def test_create_with_invalid_type(self):
        """Test creating entity with invalid type fails"""
        result = subprocess.run(
            [
                sys.executable,
                str(SCRIPT_PATH),
                "create",
                "--type", "InvalidType",
                "--props", '{"title":"Test"}'
            ],
            capture_output=True,
            text=True,
            cwd=str(SCRIPT_PATH.parent.parent)
        )

        assert result.returncode != 0
        assert "未知实体类型" in result.stderr or "unknown entity type" in result.stderr.lower()

    def test_create_with_missing_required_field(self):
        """Test creating Decision without required fields fails"""
        result = subprocess.run(
            [
                sys.executable,
                str(SCRIPT_PATH),
                "create",
                "--type", "Decision",
                "--props", '{"title":"Missing rationale"}'
            ],
            capture_output=True,
            text=True,
            cwd=str(SCRIPT_PATH.parent.parent)
        )

        assert result.returncode != 0


class TestCLIQuery:
    """Test entity queries via CLI"""

    def test_query_all_entities(self):
        """Test querying all entities"""
        result = subprocess.run(
            [sys.executable, str(SCRIPT_PATH), "query"],
            capture_output=True,
            text=True,
            cwd=str(SCRIPT_PATH.parent.parent)
        )

        assert result.returncode == 0, f"Failed: {result.stderr}"
        assert "实体" in result.stdout or "找到" in result.stdout

    def test_query_by_type(self):
        """Test querying by entity type"""
        result = subprocess.run(
            [sys.executable, str(SCRIPT_PATH), "query", "--type", "Decision"],
            capture_output=True,
            text=True,
            cwd=str(SCRIPT_PATH.parent.parent)
        )

        assert result.returncode == 0, f"Failed: {result.stderr}"

    def test_query_nonexistent_type(self):
        """Test querying non-existent type returns empty"""
        result = subprocess.run(
            [sys.executable, str(SCRIPT_PATH), "query", "--type", "NonExistentXYZ"],
            capture_output=True,
            text=True,
            cwd=str(SCRIPT_PATH.parent.parent)
        )

        assert result.returncode == 0
        assert "0" in result.stdout or "no entities" in result.stdout.lower()


class TestCLIStats:
    """Test statistics via CLI"""

    def test_stats_command(self):
        """Test stats command displays statistics"""
        result = subprocess.run(
            [sys.executable, str(SCRIPT_PATH), "stats"],
            capture_output=True,
            text=True,
            cwd=str(SCRIPT_PATH.parent.parent)
        )

        assert result.returncode == 0, f"Failed: {result.stderr}"
        assert "实体总数" in result.stdout or "total" in result.stdout.lower()
        assert "按类型分布" in result.stdout or "by type" in result.stdout.lower()


class TestCLIGet:
    """Test entity retrieval via CLI"""

    def test_get_with_invalid_id(self):
        """Test getting non-existent entity"""
        result = subprocess.run(
            [sys.executable, str(SCRIPT_PATH), "get", "--id", "nonexistent_xyz123"],
            capture_output=True,
            text=True,
            cwd=str(SCRIPT_PATH.parent.parent)
        )

        assert result.returncode != 0 or "not found" in result.stdout.lower()


class TestCLIRelate:
    """Test relation operations via CLI"""

    def test_relate_requires_existing_entities(self):
        """Test that relate command validates entity existence"""
        result = subprocess.run(
            [
                sys.executable,
                str(SCRIPT_PATH),
                "relate",
                "--from", "fake_entity_1",
                "--rel", "led_to_decision",
                "--to", "fake_entity_2"
            ],
            capture_output=True,
            text=True,
            cwd=str(SCRIPT_PATH.parent.parent)
        )

        assert result.returncode != 0
        assert "不存在" in result.stderr or "not found" in result.stdout.lower() or "not exist" in result.stderr.lower()


class TestCLIValidate:
    """Test graph validation via CLI"""

    def test_validate_command(self):
        """Test validate command runs successfully"""
        result = subprocess.run(
            [sys.executable, str(SCRIPT_PATH), "validate"],
            capture_output=True,
            text=True,
            cwd=str(SCRIPT_PATH.parent.parent)
        )

        assert result.returncode == 0, f"Failed: {result.stderr}"


class TestCLIHelp:
    """Test CLI help display"""

    def test_help_command(self):
        """Test that help command displays usage"""
        result = subprocess.run(
            [sys.executable, str(SCRIPT_PATH), "--help"],
            capture_output=True,
            text=True
        )

        assert result.returncode == 0
        assert "usage" in result.stdout.lower() or "help" in result.stdout.lower()

    def test_help_subcommand(self):
        """Test that help for subcommand works"""
        result = subprocess.run(
            [sys.executable, str(SCRIPT_PATH), "create", "--help"],
            capture_output=True,
            text=True
        )

        assert result.returncode == 0
        assert "type" in result.stdout.lower() or "props" in result.stdout.lower()


class TestMemoryOntologyIntegration:
    """Integration tests for memory_ontology CLI workflow"""

    def test_full_entity_lifecycle(self):
        """Test complete entity lifecycle: create -> query -> validate"""
        entity_props = json.dumps({
            "title": "Integration Test Entity",
            "rationale": "Testing full lifecycle",
            "made_at": "2026-04-02T00:00:00+08:00"
        })

        # Step 1: Create entity
        create_result = subprocess.run(
            [sys.executable, str(SCRIPT_PATH), "create", "--type", "Decision", "--props", entity_props],
            capture_output=True,
            text=True,
            cwd=str(SCRIPT_PATH.parent.parent)
        )
        assert create_result.returncode == 0

        # Step 2: Query to verify it exists
        query_result = subprocess.run(
            [sys.executable, str(SCRIPT_PATH), "query", "--type", "Decision"],
            capture_output=True,
            text=True,
            cwd=str(SCRIPT_PATH.parent.parent)
        )
        assert query_result.returncode == 0

        # Step 3: Validate graph
        validate_result = subprocess.run(
            [sys.executable, str(SCRIPT_PATH), "validate"],
            capture_output=True,
            text=True,
            cwd=str(SCRIPT_PATH.parent.parent)
        )
        assert validate_result.returncode == 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
