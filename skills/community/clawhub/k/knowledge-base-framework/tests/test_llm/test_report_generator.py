#!/usr/bin/env python3
"""
Tests for kb.llm.generator.report_generator - ReportGenerator

Tests for daily, weekly, and monthly report generation.
"""

import pytest
import asyncio
import json
from datetime import datetime, timezone, timedelta
from pathlib import Path
from unittest.mock import Mock, MagicMock, patch, AsyncMock

from kb.biblio.generator.report_generator import (
    ReportGenerator,
    ReportGeneratorError,
    ReportGenerationResult,
)
from kb.biblio.config import LLMConfig
from kb.biblio.engine.base import LLMResponse, LLMProvider
from kb.biblio.content_manager import LLMContentManager


# --- Fixtures ---


@pytest.fixture
def report_config(llm_config, temp_llm_dirs):
    """LLM config with temp dirs."""
    llm_config._essences_path = temp_llm_dirs["essences"]
    llm_config._reports_path = temp_llm_dirs["reports"]
    llm_config._graph_path = temp_llm_dirs["graph"]
    llm_config._incoming_path = temp_llm_dirs["incoming"]
    return llm_config


@pytest.fixture
def mock_engine():
    """Create a mock OllamaEngine that returns canned responses."""

    class MockEngine:
        def __init__(self):
            self._config = type("C", (), {"model": "gemma4:e2b"})()
            self._call_count = 0

        async def generate_async(self, prompt, **kwargs):
            self._call_count += 1
            return LLMResponse(
                content=(
                    "## Zusammenfassung\n\nTägliche Zusammenfassung.\n\n"
                    "## Neue Erkenntnisse\n\n- Punkt 1\n- Punkt 2\n\n"
                    "## Trends\n\nAufsteigender Trend.\n\n"
                    "## Hotspot-Analyse\n\nTopic A ist dominant.\n\n"
                    "## Empfehlungen\n\nWeiter recherchieren.\n"
                ),
                model="gemma4:e2b",
                provider=LLMProvider.OLLAMA,
                done=True,
                tokens=100,
            )

        def generate(self, prompt, **kwargs):
            self._call_count += 1
            return LLMResponse(
                content="Mocked response",
                model="gemma4:e2b",
                provider=LLMProvider.OLLAMA,
                done=True,
            )

        def get_model_name(self):
            return "gemma4:e2b"

        def is_available(self):
            return True

    return MockEngine()


@pytest.fixture
def content_mgr(report_config):
    """Create LLMContentManager with temp dirs."""
    mgr = LLMContentManager(llm_config=report_config)
    mgr._llm_config._essences_path = report_config._essences_path
    mgr._llm_config._reports_path = report_config._reports_path
    mgr._llm_config._graph_path = report_config._graph_path
    mgr._llm_config._incoming_path = report_config._incoming_path
    return mgr


@pytest.fixture
def report_generator(report_config, mock_engine, content_mgr):
    """Create ReportGenerator with mocked dependencies."""
    return ReportGenerator(
        llm_config=report_config,
        engine=mock_engine,
        content_manager=content_mgr,
    )


@pytest.fixture
def sample_essences(temp_llm_dirs):
    """Create sample essences in the temp directory."""
    essences_path = temp_llm_dirs["essences"]
    now = datetime.now(timezone.utc)

    essences = []
    for i in range(3):
        essence_hash = f"hash_{i:04d}"
        essence_dir = essences_path / essence_hash
        essence_dir.mkdir(parents=True, exist_ok=True)

        essence_data = {
            "version": "1.0",
            "source_hash": f"sha256:{essence_hash}",
            "extracted_at": (now - timedelta(hours=i * 4)).isoformat(),
            "model": "gemma4:e2b",
            "essence": {
                "title": f"Test Essence {i}",
                "summary": f"Summary for essence {i}",
                "key_points": [f"Point {i}.1", f"Point {i}.2"],
                "entities": [f"Entity {i}", "Shared Entity"],
                "keywords": [f"keyword{i}", "shared-keyword"],
                "relationships": [
                    {"from": f"Entity {i}", "type": "related_to", "to": "Shared Entity"}
                ],
            },
        }

        json_file = essence_dir / "essence.json"
        json_file.write_text(json.dumps(essence_data, indent=2), encoding="utf-8")

        md_file = essence_dir / "essence.md"
        md_file.write_text(
            f"---\ntitle: Test Essence {i}\n---\n\n# Test Essence {i}\n\nSummary {i}\n",
            encoding="utf-8",
        )

        essences.append({
            "hash": essence_hash,
            "path": str(md_file),
            "title": f"Test Essence {i}",
            "extracted_at": essence_data["extracted_at"],
            "model": "gemma4:e2b",
            "source_hash": f"sha256:{essence_hash}",
        })

    return essences


@pytest.fixture
def sample_daily_reports(temp_llm_dirs):
    """Create sample daily reports in the temp directory."""
    daily_path = temp_llm_dirs["reports_daily"]
    now = datetime.now(timezone.utc)

    reports = []
    for i in range(3):
        ts = (now - timedelta(days=i)).strftime("%Y%m%d_%H%M%S")
        filename = f"{ts}_report.md"
        report_file = daily_path / filename

        metadata = {
            "title": f"Daily Report Day {i}",
            "report_type": "daily",
            "generated_at": (now - timedelta(days=i)).isoformat(),
            "query": f"Daily status day {i}",
            "model": "gemma4:e2b",
        }

        content = f"---\ntitle: Daily Report Day {i}\nreport_type: daily\n---\n\n# Daily Report Day {i}\n\nSummary for day {i}.\n"
        report_file.write_text(content, encoding="utf-8")

        reports.append({
            "path": str(report_file),
            "title": f"Daily Report Day {i}",
            "report_type": "daily",
            "generated_at": metadata["generated_at"],
        })

    return reports


# --- Test Classes ---


class TestReportGeneratorInit:
    """Tests for ReportGenerator initialization."""

    def test_init_with_config(self, report_config, mock_engine, content_mgr):
        """Test initialization with explicit config."""
        gen = ReportGenerator(
            llm_config=report_config,
            engine=mock_engine,
            content_manager=content_mgr,
        )
        assert gen._config is report_config
        assert gen._engine is mock_engine
        assert gen._content_manager is content_mgr

    def test_load_template_from_file(self, report_config, mock_engine, content_mgr):
        """Test that template is loaded from file if available."""
        gen = ReportGenerator(
            llm_config=report_config,
            engine=mock_engine,
            content_manager=content_mgr,
        )
        # Template should be loaded (either from file or default)
        assert gen._template is not None
        assert len(gen._template) > 0

    def test_default_template(self):
        """Test the default template content."""
        template = ReportGenerator._default_template()
        assert "{{ title }}" in template
        assert "{{ query }}" in template
        assert "{{ content }}" in template


class TestReportGenerationResult:
    """Tests for ReportGenerationResult."""

    def test_success_result(self):
        """Test creating a successful result."""
        result = ReportGenerationResult(
            report_type="daily",
            success=True,
            report_path=Path("/tmp/report.md"),
            period_start="2026-04-14T00:00:00Z",
            period_end="2026-04-15T00:00:00Z",
            sections_included=["Zusammenfassung", "Neue Erkenntnisse"],
            model_used="gemma4:e2b",
            duration_ms=1500,
            sources_count=5,
        )

        assert result.report_type == "daily"
        assert result.success is True
        assert result.report_path == Path("/tmp/report.md")
        assert len(result.sections_included) == 2
        assert result.error is None

    def test_failure_result(self):
        """Test creating a failed result."""
        result = ReportGenerationResult(
            report_type="weekly",
            success=False,
            error="LLM timeout",
        )

        assert result.report_type == "weekly"
        assert result.success is False
        assert result.error == "LLM timeout"
        assert result.report_path is None

    def test_to_dict(self):
        """Test serialization to dict."""
        result = ReportGenerationResult(
            report_type="monthly",
            success=True,
            report_path=Path("/tmp/monthly.md"),
            period_start="2026-04-01T00:00:00Z",
            period_end="2026-04-30T00:00:00Z",
            sections_included=["Summary"],
            model_used="gemma4:e2b",
            duration_ms=3000,
            sources_count=20,
        )

        d = result.to_dict()

        assert d["report_type"] == "monthly"
        assert d["success"] is True
        assert d["report_path"] == "/tmp/monthly.md"
        assert d["sources_count"] == 20


class TestDailyReport:
    """Tests for daily report generation."""

    @pytest.mark.asyncio
    async def test_generate_daily_report(
        self, report_generator, sample_essences, temp_llm_dirs
    ):
        """Test generating a daily report."""
        result = await report_generator.generate_daily_report()

        assert result.success is True
        assert result.report_type == "daily"
        assert result.report_path is not None
        assert result.report_path.exists()
        assert result.model_used == "gemma4:e2b"
        assert result.duration_ms > 0
        assert len(result.sections_included) > 0

    @pytest.mark.asyncio
    async def test_daily_report_content(
        self, report_generator, sample_essences, temp_llm_dirs
    ):
        """Test that daily report file has correct structure."""
        result = await report_generator.generate_daily_report()

        assert result.success is True
        content = result.report_path.read_text(encoding="utf-8")

        # Should have frontmatter
        assert content.startswith("---")
        # Should have report type in frontmatter
        assert "report_type: daily" in content

    @pytest.mark.asyncio
    async def test_daily_report_custom_period(
        self, report_generator, sample_essences
    ):
        """Test daily report with custom period."""
        now = datetime.now(timezone.utc)
        start = now - timedelta(hours=12)

        result = await report_generator.generate_daily_report(
            period_start=start,
            period_end=now,
        )

        assert result.success is True
        assert result.period_start == start.isoformat()
        assert result.period_end == now.isoformat()

    @pytest.mark.asyncio
    async def test_daily_report_with_progress(
        self, report_generator, sample_essences
    ):
        """Test daily report with progress callback."""
        progress_calls = []

        def on_progress(stage, detail):
            progress_calls.append((stage, detail))

        result = await report_generator.generate_daily_report(on_progress=on_progress)

        assert result.success is True
        assert len(progress_calls) > 0
        stages = [p[0] for p in progress_calls]
        assert "collecting" in stages
        assert "generating" in stages
        assert "saving" in stages
        assert "complete" in stages

    @pytest.mark.asyncio
    async def test_daily_report_no_essences(
        self, report_generator, temp_llm_dirs
    ):
        """Test daily report when no essences exist."""
        result = await report_generator.generate_daily_report()

        # Should still succeed, just with empty content
        assert result.success is True
        assert result.sources_count == 0


class TestWeeklyReport:
    """Tests for weekly report generation."""

    @pytest.mark.asyncio
    async def test_generate_weekly_report(
        self, report_generator, sample_essences, sample_daily_reports
    ):
        """Test generating a weekly report."""
        result = await report_generator.generate_weekly_report()

        assert result.success is True
        assert result.report_type == "weekly"
        assert result.report_path is not None
        assert result.report_path.exists()

    @pytest.mark.asyncio
    async def test_weekly_report_content(
        self, report_generator, sample_essences, sample_daily_reports
    ):
        """Test that weekly report file has correct type."""
        result = await report_generator.generate_weekly_report()

        assert result.success is True
        content = result.report_path.read_text(encoding="utf-8")
        assert "report_type: weekly" in content

    @pytest.mark.asyncio
    async def test_weekly_report_with_progress(
        self, report_generator, sample_essences, sample_daily_reports
    ):
        """Test weekly report with progress callback."""
        progress_calls = []

        def on_progress(stage, detail):
            progress_calls.append((stage, detail))

        result = await report_generator.generate_weekly_report(on_progress=on_progress)

        assert result.success is True
        stages = [p[0] for p in progress_calls]
        assert "collecting" in stages
        assert "generating" in stages


class TestMonthlyReport:
    """Tests for monthly report generation."""

    @pytest.mark.asyncio
    async def test_generate_monthly_report(
        self, report_generator, sample_essences, temp_llm_dirs
    ):
        """Test generating a monthly report."""
        result = await report_generator.generate_monthly_report()

        assert result.success is True
        assert result.report_type == "monthly"
        assert result.report_path is not None
        assert result.report_path.exists()

    @pytest.mark.asyncio
    async def test_monthly_report_graph_data(
        self, report_generator, sample_essences, temp_llm_dirs
    ):
        """Test that monthly report generates graph data."""
        result = await report_generator.generate_monthly_report()

        assert result.success is True

        # Check that graph file was created
        graph_path = temp_llm_dirs["graph"]
        graph_files = list(graph_path.glob("*_knowledge_graph.json"))
        assert len(graph_files) > 0

        # Verify graph structure
        graph_data = json.loads(graph_files[0].read_text(encoding="utf-8"))
        assert "nodes" in graph_data
        assert "edges" in graph_data
        assert "stats" in graph_data
        assert "period" in graph_data

    @pytest.mark.asyncio
    async def test_monthly_report_content(
        self, report_generator, sample_essences, temp_llm_dirs
    ):
        """Test monthly report file content."""
        result = await report_generator.generate_monthly_report()

        assert result.success is True
        content = result.report_path.read_text(encoding="utf-8")
        assert "report_type: monthly" in content


class TestGenericReport:
    """Tests for the generic generate_report method."""

    @pytest.mark.asyncio
    async def test_invalid_report_type(self, report_generator):
        """Test that invalid report type raises error."""
        with pytest.raises(ReportGeneratorError, match="Invalid report type"):
            await report_generator.generate_report(
                report_type="quarterly",
                period_start=datetime.now(timezone.utc) - timedelta(days=1),
                period_end=datetime.now(timezone.utc),
            )

    @pytest.mark.asyncio
    async def test_generate_report_with_tags(
        self, report_generator, sample_essences
    ):
        """Test that tags are passed through to ContentManager."""
        result = await report_generator.generate_daily_report(tags=["test", "automated"])

        assert result.success is True


class TestHotspotDetection:
    """Tests for hotspot computation."""

    def test_compute_hotspots(self, report_generator, sample_essences):
        """Test hotspot detection from essences."""
        hotspots = report_generator._compute_hotspots(sample_essences)

        assert isinstance(hotspots, list)
        # "Shared Entity" and "shared-keyword" appear in all 3 essences
        topics = [h["topic"] for h in hotspots]
        assert any("shared" in t for t in topics)

    def test_compute_hotspots_empty(self, report_generator):
        """Test hotspot detection with no essences."""
        hotspots = report_generator._compute_hotspots([])
        assert hotspots == []


class TestGraphDataGeneration:
    """Tests for graph data generation."""

    def test_generate_graph_data(self, report_generator, sample_essences):
        """Test graph data structure."""
        now = datetime.now(timezone.utc)
        start = now - timedelta(days=1)

        graph = report_generator._generate_graph_data(
            sample_essences, [], start, now
        )

        assert "nodes" in graph
        assert "edges" in graph
        assert "stats" in graph
        assert "period" in graph
        assert graph["stats"]["total_nodes"] > 0
        assert graph["stats"]["total_edges"] > 0

    def test_graph_data_with_hotspots(self, report_generator, sample_essences):
        """Test that hotspots are marked in graph nodes."""
        now = datetime.now(timezone.utc)
        start = now - timedelta(days=1)

        hotspots = report_generator._compute_hotspots(sample_essences)
        graph = report_generator._generate_graph_data(
            sample_essences, hotspots, start, now
        )

        # At least some nodes should be marked as hotspot
        hotspot_nodes = [
            n for n in graph["nodes"]
            if n.get("hotspot", False)
        ]
        assert len(hotspot_nodes) > 0


class TestDataCollection:
    """Tests for data collection methods."""

    @pytest.mark.asyncio
    async def test_collect_essences_for_period(
        self, report_generator, sample_essences
    ):
        """Test collecting essences within a time period."""
        now = datetime.now(timezone.utc)
        start = now - timedelta(hours=25)

        essences = await report_generator._collect_essences_for_period(start, now)

        assert len(essences) > 0

    @pytest.mark.asyncio
    async def test_collect_essences_empty_period(
        self, report_generator, sample_essences
    ):
        """Test collecting essences for a period with no data."""
        far_future = datetime.now(timezone.utc) + timedelta(days=365)
        start = far_future
        end = far_future + timedelta(hours=24)

        essences = await report_generator._collect_essences_for_period(start, end)

        assert len(essences) == 0

    @pytest.mark.asyncio
    async def test_collect_reports_for_period(
        self, report_generator, sample_daily_reports
    ):
        """Test collecting reports within a time period."""
        now = datetime.now(timezone.utc)
        start = now - timedelta(days=10)

        reports = await report_generator._collect_reports_for_period(
            "daily", start, now
        )

        assert len(reports) > 0


class TestPromptBuilding:
    """Tests for prompt construction."""

    def test_build_daily_prompt(self, report_generator):
        """Test daily prompt structure."""
        now = datetime.now(timezone.utc)
        start = now - timedelta(hours=24)

        prompt = report_generator._build_daily_prompt(
            essences=[{"hash": "test", "title": "Test Essence"}],
            hotspots=[{"topic": "AI", "count": 3, "type": "keyword"}],
            period_start=start,
            period_end=now,
        )

        assert "Zusammenfassung" in prompt
        assert "24h" in prompt or "Stunden" in prompt
        assert "Test Essence" in prompt
        assert "AI" in prompt

    def test_build_weekly_prompt(self, report_generator):
        """Test weekly prompt structure."""
        now = datetime.now(timezone.utc)
        start = now - timedelta(days=7)

        prompt = report_generator._build_weekly_prompt(
            daily_reports=[],
            essences=[],
            hotspots=[],
            period_start=start,
            period_end=now,
        )

        assert "Wochenbericht" in prompt or "wöchentlichen" in prompt
        assert "Trend" in prompt

    def test_build_monthly_prompt(self, report_generator):
        """Test monthly prompt structure."""
        now = datetime.now(timezone.utc)
        start = now - timedelta(days=30)

        prompt = report_generator._build_monthly_prompt(
            weekly_reports=[],
            essences=[],
            hotspots=[],
            period_start=start,
            period_end=now,
        )

        assert "Monatsbericht" in prompt or "monatlichen" in prompt
        assert "Wissensgraph" in prompt or "Graph" in prompt


class TestSectionExtraction:
    """Tests for section extraction from generated content."""

    def test_extract_sections(self, report_generator):
        """Test extracting markdown headings from content."""
        content = (
            "## Zusammenfassung\n\nText\n\n"
            "## Neue Erkenntnisse\n\nMore text\n\n"
            "## Empfehlungen\n\nFinal text\n"
        )

        sections = report_generator._extract_sections(content, "daily")

        assert "Zusammenfassung" in sections
        assert "Neue Erkenntnisse" in sections
        assert "Empfehlungen" in sections

    def test_extract_sections_empty(self, report_generator):
        """Test extracting sections from content without headings."""
        content = "Just some plain text without headings."

        sections = report_generator._extract_sections(content, "daily")
        assert len(sections) == 0


class TestGenerationStats:
    """Tests for generation statistics."""

    @pytest.mark.asyncio
    async def test_get_generation_stats(
        self, report_generator, sample_daily_reports
    ):
        """Test getting report generation stats."""
        stats = await report_generator.get_generation_stats()

        assert "daily" in stats
        assert "weekly" in stats
        assert "monthly" in stats
        assert "count" in stats["daily"]
        assert "last" in stats["daily"]


class TestRetryLogic:
    """Tests for LLM retry logic."""

    @pytest.mark.asyncio
    async def test_retry_on_empty_response(self, report_config, content_mgr):
        """Test that retry happens on empty LLM response."""

        class FailingEngine:
            def __init__(self):
                self._call_count = 0

            async def generate_async(self, prompt, **kwargs):
                self._call_count += 1
                if self._call_count <= 2:
                    return LLMResponse(
                        content="",
                        model="gemma4:e2b",
                        provider=LLMProvider.OLLAMA,
                        done=True,
                    )
                return LLMResponse(
                    content="## Zusammenfassung\n\nSuccess on retry.\n",
                    model="gemma4:e2b",
                    provider=LLMProvider.OLLAMA,
                    done=True,
                    tokens=50,
                )

            def generate(self, prompt, **kwargs):
                return LLMResponse(
                    content="", model="gemma4:e2b",
                    provider=LLMProvider.OLLAMA, done=True
                )

        engine = FailingEngine()
        gen = ReportGenerator(
            llm_config=report_config,
            engine=engine,
            content_manager=content_mgr,
        )

        result = await gen.generate_daily_report()

        # Should succeed after retries
        assert result.success is True
        assert engine._call_count >= 3  # 2 failures + 1 success


if __name__ == "__main__":
    pytest.main([__file__, "-v"])