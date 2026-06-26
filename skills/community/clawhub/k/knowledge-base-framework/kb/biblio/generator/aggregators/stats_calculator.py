#!/usr/bin/env python3
"""
Report Statistics Calculator

Computes statistics and derived data for reports:
- Hotspot computation (delegated to report_prompts)
- Knowledge graph data generation for monthly reports
- Graph data persistence
- Report generation statistics
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict, Any

from kb.biblio.generator.report_prompts import compute_hotspots
from kb.base.logger import get_logger

logger = get_logger("kb.llm.generator.report.stats")


class StatsCalculator:
    """
    Computes statistics and derived data for report generation.

    Responsible for:
    - Hotspot computation (delegates to report_prompts.compute_hotspots)
    - Knowledge graph visualization data (nodes + edges)
    - Graph data file persistence
    - Report generation statistics

    Usage:
        calc = StatsCalculator(
            essences_path=config.essences_path,
            graph_path=config.graph_path,
        )
        hotspots = calc.compute_hotspots(essences)
        graph_data = calc.generate_graph_data(essences, hotspots, start, end)
    """

    def __init__(
        self,
        essences_path: Optional[Path] = None,
        graph_path: Optional[Path] = None,
    ):
        """
        Initialize the stats calculator.

        Args:
            essences_path: Path to essences directory (for reading essence data)
            graph_path: Path to graph output directory (for saving graph files)
        """
        self._essences_path = essences_path
        self._graph_path = graph_path

    def compute_hotspots(
        self,
        essences: List[Dict[str, Any]],
    ) -> List[Dict[str, str]]:
        """
        Identify hotspot topics that appear in multiple essences.

        Delegates to report_prompts.compute_hotspots.

        Args:
            essences: List of essence metadata dicts

        Returns:
            List of hotspot dicts with topic and count, sorted by count desc
        """
        if not self._essences_path:
            logger.warning("essences_path not configured, returning empty hotspots")
            return []
        return compute_hotspots(essences, self._essences_path)

    def generate_graph_data(
        self,
        essences: List[Dict[str, Any]],
        hotspots: List[Dict[str, str]],
        period_start: datetime,
        period_end: datetime,
    ) -> Dict[str, Any]:
        """
        Generate knowledge graph visualization data for monthly reports.

        Creates a JSON structure with nodes (entities/keywords) and edges
        (relationships) for graph rendering.

        Args:
            essences: All essences in the period
            hotspots: Identified hotspot topics
            period_start: Period start
            period_end: Period end

        Returns:
            Graph data dict with nodes and edges
        """
        if not self._essences_path:
            return {
                "period": {
                    "start": period_start.isoformat(),
                    "end": period_end.isoformat(),
                },
                "nodes": [],
                "edges": [],
                "stats": {"total_nodes": 0, "total_edges": 0, "hotspot_count": 0},
            }

        nodes = {}
        edges = []

        for essence in essences:
            hash_val = essence.get("hash", "")
            json_path = self._essences_path / hash_val / "essence.json"

            if not json_path.exists():
                continue

            try:
                data = json.loads(json_path.read_text(encoding="utf-8"))
                essence_data = data.get("essence", {})
            except (json.JSONDecodeError, IOError):
                continue

            # Add entity nodes
            for entity in essence_data.get("entities", []):
                if entity not in nodes:
                    nodes[entity] = {
                        "id": entity,
                        "type": "entity",
                        "weight": 0,
                    }
                nodes[entity]["weight"] += 1

            # Add keyword nodes
            for kw in essence_data.get("keywords", []):
                node_id = f"kw:{kw}"
                if node_id not in nodes:
                    nodes[node_id] = {
                        "id": node_id,
                        "label": kw,
                        "type": "keyword",
                        "weight": 0,
                    }
                nodes[node_id]["weight"] += 1

            # Add relationships as edges
            for rel in essence_data.get("relationships", []):
                from_entity = rel.get("from", "")
                to_entity = rel.get("to", "")
                rel_type = rel.get("type", "related_to")

                if from_entity and to_entity:
                    edges.append({
                        "source": from_entity,
                        "target": to_entity,
                        "type": rel_type,
                    })

        # Mark hotspots
        for hs in hotspots:
            topic = hs["topic"]

            # Check if it's already a node
            for node_id, node in nodes.items():
                label = node.get("label", node.get("id", ""))
                if label.lower() == topic or node_id.lower() == topic:
                    node["hotspot"] = True
                    node["hotspot_count"] = hs["count"]

        return {
            "period": {
                "start": period_start.isoformat(),
                "end": period_end.isoformat(),
            },
            "nodes": list(nodes.values()),
            "edges": edges,
            "stats": {
                "total_nodes": len(nodes),
                "total_edges": len(edges),
                "hotspot_count": len(hotspots),
            }
        }

    def save_graph_data(
        self,
        graph_data: Dict[str, Any],
        period_start: datetime,
    ) -> Path:
        """
        Save graph visualization data to the graph directory.

        Args:
            graph_data: Graph data dict with nodes and edges
            period_start: Used for filename

        Returns:
            Path to saved graph file

        Raises:
            ValueError: If graph_path is not configured
        """
        if not self._graph_path:
            raise ValueError("graph_path not configured")

        self._graph_path.mkdir(parents=True, exist_ok=True)

        timestamp = period_start.strftime("%Y%m%d")
        graph_file = self._graph_path / f"{timestamp}_knowledge_graph.json"

        graph_file.write_text(
            json.dumps(graph_data, indent=2, ensure_ascii=False),
            encoding="utf-8"
        )

        logger.info(
            f"Saved graph data",
            extra={"path": str(graph_file), "nodes": graph_data["stats"]["total_nodes"]}
        )

        return graph_file

    async def get_generation_stats(
        self,
        content_manager: Any,  # LLMContentManager
    ) -> Dict[str, Any]:
        """
        Get statistics about report generation.

        Args:
            content_manager: LLMContentManager for querying report metadata

        Returns:
            Dict with counts of reports by type and last generation times
        """
        stats = {
            "daily": {"count": 0, "last": None},
            "weekly": {"count": 0, "last": None},
            "monthly": {"count": 0, "last": None},
        }

        for report_type in ("daily", "weekly", "monthly"):
            reports = await content_manager.list_reports(
                report_type=report_type, limit=1
            )
            if reports:
                stats[report_type]["count"] = len(reports)
                stats[report_type]["last"] = reports[0].get("generated_at")

        return stats