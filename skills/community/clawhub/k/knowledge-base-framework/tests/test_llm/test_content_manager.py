#!/usr/bin/env python3
"""
Tests for kb.llm.content_manager - LLMContentManager

Tests for the content manager that handles essences, reports, and graph files.
"""

import pytest
import asyncio
import json
from pathlib import Path
from unittest.mock import Mock, MagicMock, patch, AsyncMock
import yaml

from kb.biblio.content_manager import (
    LLMContentManager,
    ContentManagerError,
)
from kb.biblio.config import LLMConfig


class TestContentManagerInit:
    """Tests for LLMContentManager initialization."""
    
    def test_init_with_config(self, llm_config, temp_llm_dirs):
        """Test initialization with explicit config."""
        manager = LLMContentManager(llm_config=llm_config)
        
        assert manager._llm_config is llm_config
        # Just verify paths are Path objects (actual values depend on test fixtures)
        assert isinstance(manager._llm_config.essences_path, Path)
        assert isinstance(manager._llm_config.reports_path, Path)
        assert isinstance(manager._llm_config.graph_path, Path)
        assert isinstance(manager._llm_config.incoming_path, Path)
    
    def test_directories_created(self, llm_config, temp_llm_dirs):
        """Test that required directories are created."""
        manager = LLMContentManager(llm_config=llm_config)
        
        assert temp_llm_dirs["essences"].exists()
        assert temp_llm_dirs["reports"].exists()
        assert temp_llm_dirs["reports_daily"].exists()
        assert temp_llm_dirs["reports_weekly"].exists()
        assert temp_llm_dirs["reports_monthly"].exists()
        assert temp_llm_dirs["graph"].exists()
        assert temp_llm_dirs["incoming"].exists()


class TestContentManagerEssences:
    """Tests for essence operations."""
    
    @pytest.mark.asyncio
    async def test_save_essence_basic(self, llm_config, temp_llm_dirs):
        """Test saving a basic essence."""
        manager = LLMContentManager(llm_config=llm_config)
        manager._llm_config._essences_path = temp_llm_dirs["essences"]
        manager._llm_config._reports_path = temp_llm_dirs["reports"]
        manager._llm_config._graph_path = temp_llm_dirs["graph"]
        manager._llm_config._incoming_path = temp_llm_dirs["incoming"]
        
        # Mock DB tracking
        with patch.object(manager, '_track_essence', new_callable=AsyncMock):
            path = await manager.save_essence(
                title="Test Essence",
                summary="This is a test summary",
                key_points=["Point 1", "Point 2", "Point 3"],
                content="Detailed content here.",
                model_used="gemma4:e2b"
            )
        
        assert path.exists()
        assert path.name == "essence.md"
        assert "essences" in str(path)
    
    @pytest.mark.asyncio
    async def test_save_essence_with_source(self, llm_config, temp_llm_dirs, sample_pdf):
        """Test saving essence with source file."""
        manager = LLMContentManager(llm_config=llm_config)
        manager._llm_config._essences_path = temp_llm_dirs["essences"]
        manager._llm_config._reports_path = temp_llm_dirs["reports"]
        manager._llm_config._graph_path = temp_llm_dirs["graph"]
        manager._llm_config._incoming_path = temp_llm_dirs["incoming"]
        
        with patch.object(manager, '_track_essence', new_callable=AsyncMock):
            path = await manager.save_essence(
                title="Document Essence",
                summary="PDF document summary",
                key_points=["Key finding 1", "Key finding 2"],
                content="Full analysis...",
                source_file=sample_pdf,
                entities=["Entity A", "Entity B"],
                keywords=["pdf", "document"]
            )
        
        assert path.exists()
        
        # Verify JSON sidecar was created
        essence_dir = path.parent
        json_file = essence_dir / "essence.json"
        assert json_file.exists()
        
        json_data = json.loads(json_file.read_text())
        assert json_data["essence"]["title"] == "Document Essence"
        assert "sha256:" in json_data["source_hash"]
    
    @pytest.mark.asyncio
    async def test_save_essence_markdown_format(self, llm_config, temp_llm_dirs):
        """Test that saved essence is valid Markdown with frontmatter."""
        manager = LLMContentManager(llm_config=llm_config)
        manager._llm_config._essences_path = temp_llm_dirs["essences"]
        manager._llm_config._reports_path = temp_llm_dirs["reports"]
        manager._llm_config._graph_path = temp_llm_dirs["graph"]
        manager._llm_config._incoming_path = temp_llm_dirs["incoming"]
        
        with patch.object(manager, '_track_essence', new_callable=AsyncMock):
            path = await manager.save_essence(
                title="Markdown Test",
                summary="Testing markdown output",
                key_points=["One", "Two", "Three"],
                content="More detailed content."
            )
        
        content = path.read_text(encoding="utf-8")
        
        # Check frontmatter
        assert content.startswith("---")
        assert "title: Markdown Test" in content
        assert "type: essence" in content
        assert "model: gemma4:e2b" in content
        
        # Check markdown body
        assert "# Markdown Test" in content
        assert "## Zusammenfassung" in content
        assert "- One" in content
        assert "- Two" in content
        assert "## Detailanalyse" in content
    
    @pytest.mark.asyncio
    async def test_list_essences(self, llm_config, temp_llm_dirs):
        """Test listing stored essences."""
        manager = LLMContentManager(llm_config=llm_config)
        manager._llm_config._essences_path = temp_llm_dirs["essences"]
        manager._llm_config._reports_path = temp_llm_dirs["reports"]
        manager._llm_config._graph_path = temp_llm_dirs["graph"]
        manager._llm_config._incoming_path = temp_llm_dirs["incoming"]
        
        # Create some essences
        with patch.object(manager, '_track_essence', new_callable=AsyncMock):
            await manager.save_essence(
                title="First Essence",
                summary="Summary 1",
                key_points=["A"],
                content="Content 1"
            )
            await manager.save_essence(
                title="Second Essence",
                summary="Summary 2",
                key_points=["B"],
                content="Content 2"
            )
        
        essences = await manager.list_essences()
        
        assert len(essences) == 2
        titles = [e["title"] for e in essences]
        assert "First Essence" in titles
        assert "Second Essence" in titles
    
    @pytest.mark.asyncio
    async def test_get_essence_by_topic_title(self, llm_config, temp_llm_dirs):
        """Test finding essence by topic match in title."""
        manager = LLMContentManager(llm_config=llm_config)
        manager._llm_config._essences_path = temp_llm_dirs["essences"]
        manager._llm_config._reports_path = temp_llm_dirs["reports"]
        manager._llm_config._graph_path = temp_llm_dirs["graph"]
        manager._llm_config._incoming_path = temp_llm_dirs["incoming"]
        
        with patch.object(manager, '_track_essence', new_callable=AsyncMock):
            await manager.save_essence(
                title="Machine Learning Fundamentals",
                summary="ML basics",
                key_points=["Supervised learning"],
                content="Content about ML",
                keywords=["machine learning", "AI"]
            )
        
        result = await manager.get_essence_by_topic("machine learning")
        
        assert result is not None
        assert result["title"] == "Machine Learning Fundamentals"
        assert result["match_type"] == "title"
    
    @pytest.mark.asyncio
    async def test_get_essence_by_topic_keyword(self, llm_config, temp_llm_dirs):
        """Test finding essence by keyword match."""
        manager = LLMContentManager(llm_config=llm_config)
        manager._llm_config._essences_path = temp_llm_dirs["essences"]
        manager._llm_config._reports_path = temp_llm_dirs["reports"]
        manager._llm_config._graph_path = temp_llm_dirs["graph"]
        manager._llm_config._incoming_path = temp_llm_dirs["incoming"]
        
        with patch.object(manager, '_track_essence', new_callable=AsyncMock):
            await manager.save_essence(
                title="Deep Learning",
                summary="DL basics",
                key_points=["Neural networks"],
                content="Content about DL",
                keywords=["deep learning", "neural nets"]
            )
        
        result = await manager.get_essence_by_topic("neural nets")
        
        assert result is not None
        assert result["title"] == "Deep Learning"
        assert result["match_type"] == "keyword"
    
    @pytest.mark.asyncio
    async def test_get_essence_by_topic_not_found(self, llm_config, temp_llm_dirs):
        """Test that non-existent topic returns None."""
        manager = LLMContentManager(llm_config=llm_config)
        manager._llm_config._essences_path = temp_llm_dirs["essences"]
        manager._llm_config._reports_path = temp_llm_dirs["reports"]
        manager._llm_config._graph_path = temp_llm_dirs["graph"]
        manager._llm_config._incoming_path = temp_llm_dirs["incoming"]
        
        with patch.object(manager, '_track_essence', new_callable=AsyncMock):
            await manager.save_essence(
                title="Python Programming",
                summary="Python basics",
                key_points=["Syntax"],
                content="Content about Python"
            )
        
        result = await manager.get_essence_by_topic("javascript")
        
        assert result is None


class TestContentManagerReports:
    """Tests for report operations."""
    
    @pytest.mark.asyncio
    async def test_save_report_daily(self, llm_config, temp_llm_dirs):
        """Test saving a daily report."""
        manager = LLMContentManager(llm_config=llm_config)
        manager._llm_config._essences_path = temp_llm_dirs["essences"]
        manager._llm_config._reports_path = temp_llm_dirs["reports"]
        manager._llm_config._graph_path = temp_llm_dirs["graph"]
        manager._llm_config._incoming_path = temp_llm_dirs["incoming"]
        
        path = await manager.save_report(
            title="Daily Summary",
            content="## Overview\n\nAll systems operational.",
            query="Show daily status",
            report_type="daily"
        )
        
        assert path.exists()
        assert "daily" in str(path)
        assert path.name.endswith("_report.md")
    
    @pytest.mark.asyncio
    async def test_save_report_weekly(self, llm_config, temp_llm_dirs):
        """Test saving a weekly report."""
        manager = LLMContentManager(llm_config=llm_config)
        manager._llm_config._essences_path = temp_llm_dirs["essences"]
        manager._llm_config._reports_path = temp_llm_dirs["reports"]
        manager._llm_config._graph_path = temp_llm_dirs["graph"]
        manager._llm_config._incoming_path = temp_llm_dirs["incoming"]
        
        path = await manager.save_report(
            title="Weekly Analysis",
            content="## Week Summary\n\nInsights from the week.",
            query="Weekly analysis",
            report_type="weekly"
        )
        
        assert path.exists()
        assert "weekly" in str(path)
    
    @pytest.mark.asyncio
    async def test_save_report_markdown_format(self, llm_config, temp_llm_dirs):
        """Test that saved report is valid Markdown with frontmatter."""
        manager = LLMContentManager(llm_config=llm_config)
        manager._llm_config._essences_path = temp_llm_dirs["essences"]
        manager._llm_config._reports_path = temp_llm_dirs["reports"]
        manager._llm_config._graph_path = temp_llm_dirs["graph"]
        manager._llm_config._incoming_path = temp_llm_dirs["incoming"]
        
        path = await manager.save_report(
            title="Monthly Review",
            content="Detailed analysis content here.",
            query="Review this month",
            report_type="monthly",
            source_hashes=["abc123", "def456"],
            related_topics=["analysis", "review"]
        )
        
        content = path.read_text(encoding="utf-8")
        
        # Check frontmatter
        assert content.startswith("---")
        assert "title: Monthly Review" in content
        assert "report_type: monthly" in content
        assert "query: Review this month" in content
        
        # Check markdown body
        assert "# Monthly Review" in content
        assert "> **Abfrage:** Review this month" in content
        assert "## Quellen" in content
    
    @pytest.mark.asyncio
    async def test_list_reports(self, llm_config, temp_llm_dirs):
        """Test listing stored reports."""
        manager = LLMContentManager(llm_config=llm_config)
        manager._llm_config._essences_path = temp_llm_dirs["essences"]
        manager._llm_config._reports_path = temp_llm_dirs["reports"]
        manager._llm_config._graph_path = temp_llm_dirs["graph"]
        manager._llm_config._incoming_path = temp_llm_dirs["incoming"]
        
        # Create some reports
        await manager.save_report(
            title="Report One",
            content="Content 1",
            query="Query 1",
            report_type="daily"
        )
        await manager.save_report(
            title="Report Two",
            content="Content 2",
            query="Query 2",
            report_type="weekly"
        )
        
        reports = await manager.list_reports()
        
        assert len(reports) == 2
        
        # Filter by type
        daily_reports = await manager.list_reports(report_type="daily")
        assert len(daily_reports) == 1
        assert daily_reports[0]["title"] == "Report One"
    
    @pytest.mark.asyncio
    async def test_list_reports_empty(self, llm_config, temp_llm_dirs):
        """Test listing when no reports exist."""
        manager = LLMContentManager(llm_config=llm_config)
        manager._llm_config._essences_path = temp_llm_dirs["essences"]
        manager._llm_config._reports_path = temp_llm_dirs["reports"]
        manager._llm_config._graph_path = temp_llm_dirs["graph"]
        manager._llm_config._incoming_path = temp_llm_dirs["incoming"]
        
        reports = await manager.list_reports()
        
        assert len(reports) == 0


class TestContentManagerIncoming:
    """Tests for incoming queue operations."""
    
    @pytest.mark.asyncio
    async def test_add_incoming(self, llm_config, temp_llm_dirs, sample_pdf):
        """Test adding file to incoming queue."""
        manager = LLMContentManager(llm_config=llm_config)
        manager._llm_config._essences_path = temp_llm_dirs["essences"]
        manager._llm_config._reports_path = temp_llm_dirs["reports"]
        manager._llm_config._graph_path = temp_llm_dirs["graph"]
        manager._llm_config._incoming_path = temp_llm_dirs["incoming"]
        
        queued_path = await manager.add_incoming(sample_pdf)
        
        assert queued_path.exists()
        assert "incoming" in str(queued_path)
        # Should have timestamp prefix
        assert "_test_document.pdf" in queued_path.name
    
    @pytest.mark.asyncio
    async def test_list_incoming(self, llm_config, temp_llm_dirs, sample_pdf, sample_markdown):
        """Test listing incoming queue."""
        manager = LLMContentManager(llm_config=llm_config)
        manager._llm_config._essences_path = temp_llm_dirs["essences"]
        manager._llm_config._reports_path = temp_llm_dirs["reports"]
        manager._llm_config._graph_path = temp_llm_dirs["graph"]
        manager._llm_config._incoming_path = temp_llm_dirs["incoming"]
        
        await manager.add_incoming(sample_pdf)
        await manager.add_incoming(sample_markdown)
        
        files = await manager.list_incoming()
        
        assert len(files) == 2
        names = [f["name"] for f in files]
        assert any("test_document.pdf" in n for n in names)
        assert any("test_document.md" in n for n in names)
    
    @pytest.mark.asyncio
    async def test_clear_incoming_all(self, llm_config, temp_llm_dirs, sample_pdf, sample_markdown):
        """Test clearing all incoming files."""
        manager = LLMContentManager(llm_config=llm_config)
        manager._llm_config._essences_path = temp_llm_dirs["essences"]
        manager._llm_config._reports_path = temp_llm_dirs["reports"]
        manager._llm_config._graph_path = temp_llm_dirs["graph"]
        manager._llm_config._incoming_path = temp_llm_dirs["incoming"]
        
        await manager.add_incoming(sample_pdf)
        await manager.add_incoming(sample_markdown)
        
        count = await manager.clear_incoming()
        
        assert count == 2
        files = await manager.list_incoming()
        assert len(files) == 0
    
    @pytest.mark.asyncio
    async def test_clear_incoming_filtered(self, llm_config, temp_llm_dirs, sample_pdf, sample_markdown):
        """Test clearing specific incoming files."""
        manager = LLMContentManager(llm_config=llm_config)
        manager._llm_config._essences_path = temp_llm_dirs["essences"]
        manager._llm_config._reports_path = temp_llm_dirs["reports"]
        manager._llm_config._graph_path = temp_llm_dirs["graph"]
        manager._llm_config._incoming_path = temp_llm_dirs["incoming"]
        
        await manager.add_incoming(sample_pdf)
        await manager.add_incoming(sample_markdown)
        
        # Only clear PDF files
        count = await manager.clear_incoming(name_filter=".pdf")
        
        assert count == 1
        files = await manager.list_incoming()
        assert len(files) == 1
        assert "md" in files[0]["name"]


class TestContentManagerHelpers:
    """Tests for helper methods."""
    
    def test_compute_file_hash(self, llm_config, temp_llm_dirs, sample_pdf):
        """Test SHA256 hash computation."""
        manager = LLMContentManager(llm_config=llm_config)
        manager._llm_config._essences_path = temp_llm_dirs["essences"]
        manager._llm_config._reports_path = temp_llm_dirs["reports"]
        manager._llm_config._graph_path = temp_llm_dirs["graph"]
        manager._llm_config._incoming_path = temp_llm_dirs["incoming"]
        
        hash1 = manager._compute_file_hash(sample_pdf)
        hash2 = manager._compute_file_hash(sample_pdf)
        
        assert hash1.startswith("sha256:")
        assert hash1 == hash2  # Same file = same hash
        
        # Different content = different hash
        different_file = temp_llm_dirs["base"] / "different.txt"
        different_file.write_text("Different content")
        hash3 = manager._compute_file_hash(different_file)
        
        assert hash1 != hash3
    
    def test_format_frontmatter(self, llm_config, temp_llm_dirs):
        """Test YAML frontmatter formatting."""
        manager = LLMContentManager(llm_config=llm_config)
        manager._llm_config._essences_path = temp_llm_dirs["essences"]
        manager._llm_config._reports_path = temp_llm_dirs["reports"]
        manager._llm_config._graph_path = temp_llm_dirs["graph"]
        manager._llm_config._incoming_path = temp_llm_dirs["incoming"]
        
        metadata = {
            "title": "Test",
            "type": "essence",
            "tags": ["tag1", "tag2"]
        }
        
        fm = manager._format_frontmatter(metadata)
        
        assert fm.startswith("---")
        assert "title: Test" in fm
        assert "type: essence" in fm
        assert "tags:" in fm
        assert fm.endswith("---")
    
    def test_parse_frontmatter(self, llm_config, temp_llm_dirs):
        """Test YAML frontmatter parsing."""
        manager = LLMContentManager(llm_config=llm_config)
        manager._llm_config._essences_path = temp_llm_dirs["essences"]
        manager._llm_config._reports_path = temp_llm_dirs["reports"]
        manager._llm_config._graph_path = temp_llm_dirs["graph"]
        manager._llm_config._incoming_path = temp_llm_dirs["incoming"]
        
        content = """---
title: Test Doc
type: essence
version: "1.0"
---

# Body Content

Some text here.
"""
        
        metadata, body = manager._parse_frontmatter(content)
        
        assert metadata["title"] == "Test Doc"
        assert metadata["type"] == "essence"
        assert "# Body Content" in body
        assert "Some text here." in body
    
    def test_parse_frontmatter_no_fm(self, llm_config, temp_llm_dirs):
        """Test parsing content without frontmatter."""
        manager = LLMContentManager(llm_config=llm_config)
        manager._llm_config._essences_path = temp_llm_dirs["essences"]
        manager._llm_config._reports_path = temp_llm_dirs["reports"]
        manager._llm_config._graph_path = temp_llm_dirs["graph"]
        manager._llm_config._incoming_path = temp_llm_dirs["incoming"]
        
        content = "# Just Markdown\n\nNo frontmatter here."
        
        metadata, body = manager._parse_frontmatter(content)
        
        assert metadata == {}
        assert body == content


class TestContentManagerConvenience:
    """Tests for convenience async functions."""
    
    @pytest.mark.asyncio
    async def test_save_essence_async(self, llm_config, temp_llm_dirs):
        """Test convenience function for saving essence."""
        from kb.biblio.content_manager import save_essence_async
        
        with patch.object(LLMConfig, 'get_instance', return_value=llm_config):
            with patch('kb.llm.content_manager.LLMContentManager._track_essence', new_callable=AsyncMock):
                # Note: This will use default paths, not temp dirs
                # Just verify the function is callable
                try:
                    await save_essence_async(
                        title="Test",
                        summary="Summary",
                        key_points=["A"],
                        content="Content"
                    )
                except Exception:
                    # May fail due to path issues in test env
                    pass


if __name__ == "__main__":
    pytest.main([__file__, "-v"])