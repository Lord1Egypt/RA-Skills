#!/usr/bin/env python3
"""
Report Data Aggregator

Collects and reads data for report generation:
- Essences within a time period
- Reports within a time period
- Full essence/report content from disk
- Sub-reports for aggregation (daily→weekly, weekly→monthly)
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict, Any

from kb.base.logger import get_logger

logger = get_logger("kb.llm.generator.report.aggregator")


class ReportDataAggregator:
    """
    Collects and reads data needed for report generation.

    Responsible for:
    - Querying the content manager for essences/reports in a period
    - Reading full essence/report content from disk
    - Collecting sub-reports for weekly/monthly aggregation

    Usage:
        aggregator = ReportDataAggregator(
            content_manager=manager,
            essences_path=config.essences_path,
        )
        essences = await aggregator.collect_essences(start, end)
        content = await aggregator.read_essence_content(hash_val)
    """

    def __init__(
        self,
        content_manager: Any,  # LLMContentManager
        essences_path: Optional[Path] = None,
    ):
        """
        Initialize the data aggregator.

        Args:
            content_manager: LLMContentManager instance for querying metadata
            essences_path: Path to essences directory (for reading full content)
        """
        self._content_manager = content_manager
        self._essences_path = essences_path

    async def collect_essences_for_period(
        self,
        period_start: datetime,
        period_end: datetime,
    ) -> List[Dict[str, Any]]:
        """
        Collect all essences created within the given period.

        Args:
            period_start: Start of period (inclusive)
            period_end: End of period (exclusive)

        Returns:
            List of essence metadata dicts that fall within the period
        """
        all_essences = await self._content_manager.list_essences(limit=1000)
        matching = []

        for essence in all_essences:
            extracted_at = essence.get("extracted_at")
            if not extracted_at:
                continue

            try:
                # Parse ISO timestamp
                if extracted_at.endswith("Z"):
                    essence_time = datetime.fromisoformat(
                        extracted_at.replace("Z", "+00:00")
                    )
                else:
                    essence_time = datetime.fromisoformat(extracted_at)

                if period_start <= essence_time < period_end:
                    matching.append(essence)

            except (ValueError, TypeError) as e:
                logger.warning(
                    f"Failed to parse essence timestamp: {extracted_at}",
                    extra={"error": str(e)}
                )
                continue

        return matching

    async def collect_reports_for_period(
        self,
        report_type: str,
        period_start: datetime,
        period_end: datetime,
    ) -> List[Dict[str, Any]]:
        """
        Collect all reports of a given type within the period.

        Args:
            report_type: Type of reports to collect (daily, weekly)
            period_start: Start of period (inclusive)
            period_end: End of period (exclusive)

        Returns:
            List of report metadata dicts
        """
        all_reports = await self._content_manager.list_reports(
            report_type=report_type, limit=100
        )
        matching = []

        for report in all_reports:
            generated_at = report.get("generated_at")
            if not generated_at:
                continue

            try:
                if generated_at.endswith("Z"):
                    report_time = datetime.fromisoformat(
                        generated_at.replace("Z", "+00:00")
                    )
                else:
                    report_time = datetime.fromisoformat(generated_at)

                if period_start <= report_time < period_end:
                    matching.append(report)

            except (ValueError, TypeError) as e:
                logger.warning(
                    f"Failed to parse report timestamp: {generated_at}",
                    extra={"error": str(e)}
                )
                continue

        return matching

    async def read_essence_content(
        self,
        essence_hash: str,
    ) -> Dict[str, Any]:
        """
        Read full essence content by hash.

        Args:
            essence_hash: The essence directory hash

        Returns:
            Essence data dict with parsed content
        """
        if not self._essences_path:
            return {"hash": essence_hash, "error": "essences_path not configured"}

        json_path = self._essences_path / essence_hash / "essence.json"

        if not json_path.exists():
            return {"hash": essence_hash, "error": "not_found"}

        try:
            data = json.loads(json_path.read_text(encoding="utf-8"))
            return {
                "hash": essence_hash,
                "title": data.get("essence", {}).get("title", "Untitled"),
                "summary": data.get("essence", {}).get("summary", ""),
                "key_points": data.get("essence", {}).get("key_points", []),
                "entities": data.get("essence", {}).get("entities", []),
                "keywords": data.get("essence", {}).get("keywords", []),
                "relationships": data.get("essence", {}).get("relationships", []),
                "extracted_at": data.get("extracted_at"),
                "model": data.get("model"),
            }
        except (json.JSONDecodeError, IOError) as e:
            logger.warning(
                f"Failed to read essence {essence_hash}",
                extra={"error": str(e)}
            )
            return {"hash": essence_hash, "error": str(e)}

    async def read_report_content(
        self,
        report_path: str,
    ) -> Dict[str, Any]:
        """
        Read full report content from file path.

        Args:
            report_path: Path to the report file

        Returns:
            Report data dict with parsed metadata and body
        """
        path = Path(report_path)
        if not path.exists():
            return {"path": report_path, "error": "not_found"}

        try:
            content = path.read_text(encoding="utf-8")
            metadata, body = self._content_manager._parse_frontmatter(content)

            return {
                "path": report_path,
                "title": metadata.get("title", "Untitled"),
                "report_type": metadata.get("report_type", "unknown"),
                "generated_at": metadata.get("generated_at"),
                "body": body[:5000],  # Limit body size for prompts
                "sources": metadata.get("sources", []),
            }
        except IOError as e:
            logger.warning(
                f"Failed to read report {report_path}",
                extra={"error": str(e)}
            )
            return {"path": report_path, "error": str(e)}

    async def collect_sub_reports(
        self,
        sub_report_type: str,
        period_start: datetime,
        period_end: datetime,
    ) -> List[Dict[str, Any]]:
        """
        Collect and read sub-reports for aggregation.

        Used by weekly reports (collecting daily) and monthly reports
        (collecting weekly).

        Args:
            sub_report_type: Type of sub-reports to collect ("daily" or "weekly")
            period_start: Period start
            period_end: Period end

        Returns:
            List of sub-report content dicts (excluding errored ones)
        """
        reports_meta = await self.collect_reports_for_period(
            sub_report_type, period_start, period_end
        )
        reports_data = []
        for r in reports_meta:
            r_content = await self.read_report_content(r.get("path", ""))
            if "error" not in r_content:
                reports_data.append(r_content)
        return reports_data