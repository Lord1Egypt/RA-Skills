"""
mindclaw.graph — Knowledge Graph engine.

Provides traversal, pathfinding, and relationship queries
on top of the edge table in MemoryStore.
"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass, field
from typing import Any, Optional

from .store import Memory, MemoryStore


@dataclass
class GraphNode:
    """A node in the knowledge graph (wraps a Memory)."""
    memory: Memory
    edges_out: list[dict[str, Any]] = field(default_factory=list)
    edges_in: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class GraphPath:
    """A path between two nodes in the graph."""
    nodes: list[str]           # memory ids in order
    edges: list[dict[str, Any]]
    total_weight: float = 0.0


class KnowledgeGraph:
    """
    High-level knowledge graph operations built on MemoryStore.

    Supports:
    - Adding entities and relationships
    - Traversal (neighbors, BFS paths)
    - Subgraph extraction
    - Relationship queries
    """

    def __init__(self, store: MemoryStore):
        self.store = store

    # -- Entity helpers -----------------------------------------------------

    def add_entity(
        self,
        name: str,
        entity_type: str = "entity",
        *,
        summary: str = "",
        importance: float = 0.6,
        tags: Optional[list[str]] = None,
        metadata: Optional[dict] = None,
    ) -> Memory:
        """Create a memory that represents a named entity in the graph."""
        mem = Memory(
            content=name,
            summary=summary,
            category=entity_type,
            tags=tags or [entity_type],
            importance=importance,
            metadata={**(metadata or {}), "graph_entity": True},
        )
        return self.store.add(mem)

    def link(
        self,
        source_id: str,
        target_id: str,
        relation: str,
        *,
        weight: float = 1.0,
        bidirectional: bool = False,
        metadata: Optional[dict] = None,
    ) -> list[str]:
        """
        Create a relationship between two memories.
        Returns list of created edge ids.
        """
        edge_ids = [
            self.store.add_edge(source_id, target_id, relation, weight, metadata)
        ]
        if bidirectional:
            inverse = _inverse_relation(relation)
            edge_ids.append(
                self.store.add_edge(target_id, source_id, inverse, weight, metadata)
            )
        return edge_ids

    def unlink(self, source_id: str, target_id: str, relation: Optional[str] = None) -> int:
        """Remove edges between two memories. Returns count removed."""
        edges = self.store.get_edges(source_id, direction="out")
        count = 0
        for e in edges:
            if e["target_id"] == target_id:
                if relation is None or e["relation"] == relation:
                    self.store.remove_edge(e["id"])
                    count += 1
        return count

    # -- Queries ------------------------------------------------------------

    def neighbors(
        self,
        memory_id: str,
        *,
        relation: Optional[str] = None,
        direction: str = "both",
        max_depth: int = 1,
    ) -> list[GraphNode]:
        """
        Get neighboring nodes up to max_depth hops.
        Returns unique GraphNodes reachable.
        """
        visited: set[str] = {memory_id}
        queue: deque[tuple[str, int]] = deque([(memory_id, 0)])
        results: list[GraphNode] = []

        while queue:
            current_id, depth = queue.popleft()
            if depth >= max_depth:
                continue

            edges = self.store.get_edges(current_id, direction=direction)
            for edge in edges:
                if relation and edge["relation"] != relation:
                    continue

                # Determine the neighbor id
                neighbor_id = (
                    edge["target_id"]
                    if edge["source_id"] == current_id
                    else edge["source_id"]
                )

                if neighbor_id in visited:
                    continue
                visited.add(neighbor_id)

                mem = self.store.get(neighbor_id)
                if mem is None:
                    continue

                node = GraphNode(
                    memory=mem,
                    edges_out=self.store.get_edges(neighbor_id, direction="out"),
                    edges_in=self.store.get_edges(neighbor_id, direction="in"),
                )
                results.append(node)
                queue.append((neighbor_id, depth + 1))

        return results

    def find_path(
        self,
        from_id: str,
        to_id: str,
        *,
        max_depth: int = 6,
    ) -> Optional[GraphPath]:
        """BFS shortest path between two memories."""
        if from_id == to_id:
            return GraphPath(nodes=[from_id], edges=[], total_weight=0)

        visited: set[str] = {from_id}
        # Each queue item: (current_id, path_of_ids, path_of_edges)
        queue: deque[tuple[str, list[str], list[dict]]] = deque(
            [(from_id, [from_id], [])]
        )

        while queue:
            current_id, path, edge_path = queue.popleft()
            if len(path) > max_depth:
                continue

            edges = self.store.get_edges(current_id, direction="out")
            for edge in edges:
                neighbor_id = edge["target_id"]
                if neighbor_id in visited:
                    continue
                visited.add(neighbor_id)

                new_path = path + [neighbor_id]
                new_edges = edge_path + [edge]

                if neighbor_id == to_id:
                    total_w = sum(e.get("weight", 1.0) for e in new_edges)
                    return GraphPath(
                        nodes=new_path,
                        edges=new_edges,
                        total_weight=total_w,
                    )

                queue.append((neighbor_id, new_path, new_edges))

        return None

    def subgraph(
        self,
        center_id: str,
        *,
        depth: int = 2,
    ) -> dict[str, Any]:
        """
        Extract a subgraph centered on a memory.
        Returns {nodes: [...], edges: [...]} suitable for visualization.
        """
        nodes_map: dict[str, dict] = {}
        edges_list: list[dict] = []
        visited_edges: set[str] = set()

        center = self.store.get(center_id)
        if center is None:
            return {"nodes": [], "edges": []}

        nodes_map[center_id] = {
            "id": center.id,
            "label": center.content[:60],
            "category": center.category,
            "importance": center.importance,
        }

        neighbors = self.neighbors(center_id, max_depth=depth)
        for node in neighbors:
            mid = node.memory.id
            nodes_map[mid] = {
                "id": mid,
                "label": node.memory.content[:60],
                "category": node.memory.category,
                "importance": node.memory.importance,
            }
            for e in node.edges_out + node.edges_in:
                eid = e["id"]
                if eid not in visited_edges:
                    visited_edges.add(eid)
                    # Only include edges where both nodes are in the subgraph
                    if e["source_id"] in nodes_map or e["target_id"] in nodes_map:
                        edges_list.append({
                            "id": eid,
                            "source": e["source_id"],
                            "target": e["target_id"],
                            "relation": e["relation"],
                            "weight": e.get("weight", 1.0),
                        })

        # Filter edges to only those with both endpoints in the subgraph
        edges_list = [
            e for e in edges_list
            if e["source"] in nodes_map and e["target"] in nodes_map
        ]

        return {
            "nodes": list(nodes_map.values()),
            "edges": edges_list,
        }

    def find_by_relation(
        self, relation: str, *, limit: int = 50
    ) -> list[tuple[Memory, Memory, dict]]:
        """Find all memory pairs connected by a specific relation."""
        results: list[tuple[Memory, Memory, dict]] = []
        seen: set[str] = set()

        # We need to scan edges — for now iterate all memories
        memories = self.store.list_memories(limit=500)
        for mem in memories:
            edges = self.store.get_edges(mem.id, direction="out")
            for e in edges:
                if e["relation"] == relation and e["id"] not in seen:
                    seen.add(e["id"])
                    target = self.store.get(e["target_id"])
                    if target:
                        results.append((mem, target, e))
                        if len(results) >= limit:
                            return results
        return results


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_INVERSE_MAP = {
    "related_to": "related_to",
    "causes": "caused_by",
    "caused_by": "causes",
    "part_of": "has_part",
    "has_part": "part_of",
    "depends_on": "depended_by",
    "depended_by": "depends_on",
    "created": "created_by",
    "created_by": "created",
    "precedes": "follows",
    "follows": "precedes",
    "belongs_to": "contains",
    "contains": "belongs_to",
}


def _inverse_relation(relation: str) -> str:
    """Get the inverse of a relation, or append '_inverse'."""
    return _INVERSE_MAP.get(relation, f"{relation}_inverse")
