#!/usr/bin/env python3
from __future__ import annotations
"""
Hyperbolic Semantic Memory
==========================
NOTE: Requires torch. Import will succeed but classes raise RuntimeError if torch unavailable.

NIMA's SemanticMemoryHyperbolic implementation.

Uses Poincaré ball embeddings for hierarchical knowledge.
Perfect for:
- Concept hierarchies (is-a relationships)
- Taxonomic knowledge (animal → mammal → dog)
- Efficient similarity in hierarchical spaces

Author: Lilu
Date: Feb 3, 2026
"""

import os
import json
import tempfile
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field

# Optional torch dependency
try:
    import torch
    import torch.nn.functional as F
    HAS_TORCH = True
except ImportError:
    torch = None  # type: ignore
    F = None  # type: ignore
    HAS_TORCH = False

WORKSPACE_DIR = Path(os.environ.get("LILU_WORKSPACE", str(Path.home() / ".openclaw" / "workspace")))
NIMA_CORE_DIR = WORKSPACE_DIR / "nima-core"
NIMA_MEMORY_DIR = NIMA_CORE_DIR / "storage" / "data"


def atomic_torch_save(data, path):
    """DB-3: Atomic save via temp file + os.replace."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_path = tempfile.mkstemp(dir=path.parent, suffix=".tmp")
    os.close(fd)
    torch.save(data, tmp_path)
    os.replace(tmp_path, path)


class HyperbolicSpace:
    """
    Hyperbolic space operations (Poincaré ball model).
    
    The Poincaré ball is a model of n-dimensional hyperbolic space.
    It's particularly useful for embedding hierarchical structures
    because it has exponentially more space near the boundary,
    allowing efficient representation of trees and hierarchies.
    """
    
    def __init__(self, dimension: int = 64, eps: float = 1e-5):
        """
        Initialize hyperbolic space.
        
        Args:
            dimension: Embedding dimension
            eps: Small value for numerical stability
        """
        self.dimension = dimension
        self.eps = eps
        
        # Scale factor for initialization
        self.scale = 0.001
    
    def init_vector(self) -> torch.Tensor:
        """Initialize a vector near the origin."""
        return torch.randn(self.dimension) * self.scale
    
    def project_to_ball(self, x: torch.Tensor, max_norm: Optional[float] = None) -> torch.Tensor:
        """
        Project a point into the Poincaré ball.
        
        Ensures the point is within the unit ball.
        """
        if max_norm is None:
            max_norm = 1.0 - self.eps
        norm = torch.norm(x, dim=-1, keepdim=True)
        mask = norm > max_norm
        x = torch.where(mask, x / norm * max_norm, x)
        return x
    
    def distance(self, x: torch.Tensor, y: torch.Tensor) -> torch.Tensor:
        """
        Compute hyperbolic distance between points.
        
        d(x, y) = arcosh(1 + 2 * ||x - y||^2 / ((1 - ||x||^2)(1 - ||y||^2)))
        """
        x_norm_sq = torch.sum(x ** 2, dim=-1, keepdim=True).clamp(max=1 - self.eps)
        y_norm_sq = torch.sum(y ** 2, dim=-1, keepdim=True).clamp(max=1 - self.eps)
        
        diff_norm_sq = torch.sum((x - y) ** 2, dim=-1, keepdim=True)
        
        numerator = 2 * diff_norm_sq
        denominator = (1 - x_norm_sq) * (1 - y_norm_sq)
        
        # arcosh(x) = log(x + sqrt(x - 1) * sqrt(x + 1))
        inside = 1 + numerator / (denominator + self.eps)
        inside = inside.clamp(min=1 + self.eps)
        
        dist = torch.acosh(inside)
        return dist.squeeze(-1)
    
    def riemannian_to_euclidean_grad(self, grad: torch.Tensor, x: torch.Tensor) -> torch.Tensor:
        """
        Convert Euclidean gradient to Riemannian gradient.
        
        For hyperbolic space, the Riemannian metric is:
        g_x = (4 / (1 - ||x||^2))^2 * I
        
        So we need to scale the gradient.
        """
        x_norm_sq = torch.sum(x ** 2, dim=-1, keepdim=True).clamp(max=1 - self.eps)
        scale = (1 - x_norm_sq) ** 2 / 4
        return grad * scale
    
    def exp_map(self, x: torch.Tensor, v: torch.Tensor) -> torch.Tensor:
        """
        Exponential map: move from x in direction v.
        
        Exp_x(v) = x + v * tanh(||v|| / 2) / ||v|| * (1 - ||x||^2)
        """
        v_norm = torch.norm(v, dim=-1, keepdim=True)
        v_norm = torch.where(v_norm < self.eps, torch.ones_like(v_norm), v_norm)
        
        x_norm_sq = torch.sum(x ** 2, dim=-1, keepdim=True).clamp(max=1 - self.eps)
        
        scale = torch.tanh(v_norm / 2) / v_norm * (1 - x_norm_sq)
        
        result = x + v * scale
        return self.project_to_ball(result)
    
    def log_map(self, x: torch.Tensor, y: torch.Tensor) -> torch.Tensor:
        """
        Logarithmic map: direction from x to y.
        
        Log_x(y) = (1 - ||x||^2) / tanh(d/2) * (y - <x,y>x) / ||y - <x,y>x||
        """
        d = self.distance(x, y).unsqueeze(-1) + self.eps
        
        x_norm_sq = torch.sum(x ** 2, dim=-1, keepdim=True).clamp(max=1 - self.eps)
        
        diff = y - x
        diff_proj = diff - x * torch.sum(x * diff, dim=-1, keepdim=True)
        diff_proj_norm = torch.norm(diff_proj, dim=-1, keepdim=True).clamp(min=self.eps)
        
        scale = (1 - x_norm_sq) / torch.tanh(d / 2) / d
        
        result = diff_proj / diff_proj_norm * scale * d
        return result


@dataclass
class HierarchyNode:
    """A node in the concept hierarchy."""
    id: str
    name: str
    parent_id: Optional[str] = None
    children: List[str] = field(default_factory=list)
    embedding: Optional[torch.Tensor] = None
    depth: int = 0
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "name": self.name,
            "parent_id": self.parent_id,
            "children": self.children,
            "depth": self.depth,
        }


class HyperbolicSemanticMemory:
    """
    Semantic memory using hyperbolic embeddings.
    
    This implements NIMA's SemanticMemoryHyperbolic for hierarchical
    knowledge representation.
    
    Features:
    - Poincaré ball embeddings
    - Hierarchical structure
    - Efficient similarity search
    - Concept relationships (is-a, part-of)
    
    Usage:
        memory = HyperbolicSemanticMemory()
        memory.add_concept("animal", parent=None)
        memory.add_concept("mammal", parent="animal")
        memory.add_concept("dog", parent="mammal")
        
        # Query
        results = memory.find_similar("pet", top_k=5)
    """
    
    def __init__(self, 
                 dimension: int = 64,
                 learning_rate: float = 0.01,
                 device: str = "cpu"):
        """
        Initialize hyperbolic semantic memory.
        
        Args:
            dimension: Embedding dimension (64-256 recommended)
            learning_rate: Learning rate for updates
            device: Device to use
        """
        self.dimension = dimension
        self.learning_rate = learning_rate
        self.device = torch.device(device)
        
        # Hyperbolic space
        self.hyperbolic = HyperbolicSpace(dimension)
        
        # Concept hierarchy
        self.nodes: Dict[str, HierarchyNode] = {}
        self.embeddings: torch.Tensor = None  # Will be initialized
        
        # Statistics
        self.stats = {
            "concepts_added": 0,
            "queries": 0,
            "relationships_learned": 0,
        }
        
        print(f"🌀 HyperbolicSemanticMemory initialized (D={dimension})")
    
    def _init_embeddings(self, num_concepts: int):
        """Initialize embedding matrix."""
        self.embeddings = torch.nn.Parameter(
            torch.randn(num_concepts, self.dimension) * self.hyperbolic.scale
        ).to(self.device)
    
    def add_concept(self, 
                   concept_id: str,
                   name: str,
                   parent_id: Optional[str] = None,
                   embedding: Optional[torch.Tensor] = None) -> HierarchyNode:
        """
        Add a concept to the hierarchy.
        
        Args:
            concept_id: Unique identifier
            name: Human-readable name
            parent_id: Parent concept ID (for hierarchy)
            embedding: Optional pre-computed embedding
            
        Returns:
            Created node
        """
        if concept_id not in self.nodes:
            # Calculate depth
            depth = 0
            if parent_id and parent_id in self.nodes:
                depth = self.nodes[parent_id].depth + 1
                
                # Add to parent's children
                self.nodes[parent_id].children.append(concept_id)
            
            # Create node
            node = HierarchyNode(
                id=concept_id,
                name=name,
                parent_id=parent_id,
                depth=depth,
                embedding=embedding,
            )
            self.nodes[concept_id] = node
            
            # Initialize embeddings if needed
            if self.embeddings is None:
                self._init_embeddings(len(self.nodes))
            elif len(self.nodes) > self.embeddings.shape[0]:
                # Add new row to embeddings
                new_row = self.hyperbolic.init_vector().unsqueeze(0)
                self.embeddings = torch.cat([self.embeddings, new_row], dim=0)
            
            self.stats["concepts_added"] += 1
        
        return self.nodes[concept_id]
    
    def add_relationship(self, 
                        parent_id: str,
                        child_id: str,
                        _relationship_type: str = "is-a"):
        """
        Add a hierarchical relationship.
        
        Args:
            parent_id: Parent concept
            child_id: Child concept
            _relationship_type: Type of relationship (reserved for future use)
        """
        if parent_id in self.nodes and child_id in self.nodes:
            self.nodes[child_id].parent_id = parent_id
            self.nodes[child_id].depth = self.nodes[parent_id].depth + 1
            
            if child_id not in self.nodes[parent_id].children:
                self.nodes[parent_id].children.append(child_id)
            
            self.stats["relationships_learned"] += 1
    
    def _collect_pair_concepts(
        self,
        positive_pairs: List[Tuple[str, str]],
        negative_pairs: List[Tuple[str, str]] = None,
    ) -> Tuple[list, dict, "torch.Tensor"]:
        """Build concept list, index map and embedding slice for the given pairs."""
        all_concepts: set = set()
        for a, b in positive_pairs:
            all_concepts.update([a, b])
        if negative_pairs:
            for a, b in negative_pairs:
                all_concepts.update([a, b])
        concept_list = list(all_concepts)
        indices = [self._get_index(c) for c in concept_list]
        embeds = self.embeddings[indices]
        idx_map = {c: i for i, c in enumerate(concept_list)}
        return concept_list, idx_map, embeds

    def _compute_pair_distances(
        self,
        pairs: List[Tuple[str, str]],
        idx_map: dict,
        embeds: "torch.Tensor",
    ) -> List:
        """Compute hyperbolic distances for a list of concept pairs."""
        distances = []
        for a, b in pairs:
            if a in idx_map and b in idx_map:
                dist = self.hyperbolic.distance(
                    embeds[idx_map[a]].unsqueeze(0),
                    embeds[idx_map[b]].unsqueeze(0),
                )
                distances.append(dist)
        return distances

    def _compute_contrastive_loss(
        self,
        pos_dist: "torch.Tensor",
        negative_pairs: List[Tuple[str, str]],
        idx_map: dict,
        embeds: "torch.Tensor",
        margin: float,
    ) -> "torch.Tensor":
        """Compute margin ranking loss when negative pairs are provided."""
        if not negative_pairs:
            return pos_dist
        neg_distances = self._compute_pair_distances(negative_pairs, idx_map, embeds)
        if not neg_distances:
            return pos_dist
        neg_dist = torch.stack(neg_distances).mean()
        return F.margin_ranking_loss(
            pos_dist.unsqueeze(0),
            neg_dist.unsqueeze(0),
            torch.ones(1, device=self.device),
            margin=margin,
        )

    def train_step(self,
                   positive_pairs: List[Tuple[str, str]],
                   negative_pairs: List[Tuple[str, str]] = None,
                   margin: float = 0.1) -> float:
        """
        Train embeddings using contrastive loss.

        Args:
            positive_pairs: Pairs that should be close
            negative_pairs: Pairs that should be far
            margin: Margin for margin ranking loss

        Returns:
            Loss value
        """
        if self.embeddings is None or len(self.nodes) < 2:
            return 0.0

        _concept_list, idx_map, embeds = self._collect_pair_concepts(positive_pairs, negative_pairs)

        pos_distances = self._compute_pair_distances(positive_pairs, idx_map, embeds)
        if not pos_distances:
            return 0.0

        pos_dist = torch.stack(pos_distances).mean()
        loss = self._compute_contrastive_loss(pos_dist, negative_pairs, idx_map, embeds, margin)

        # Backward pass
        loss.backward()

        # Project to ball
        with torch.no_grad():
            self.embeddings.data = self.hyperbolic.project_to_ball(self.embeddings.data)

        return loss.item()
    
    def _get_index(self, concept_id: str) -> int:
        """Get embedding index for a concept."""
        return list(self.nodes.keys()).index(concept_id)
    
    def find_similar(self, 
                     concept_id: str,
                     top_k: int = 5) -> List[Dict]:
        """
        Find most similar concepts.
        
        Args:
            concept_id: Query concept
            top_k: Number of results
            
        Returns:
            List of similar concepts with scores
        """
        self.stats["queries"] += 1
        
        if concept_id not in self.nodes:
            return []
        
        idx = self._get_index(concept_id)
        query = self.embeddings[idx]
        
        # Compute distances to all concepts
        distances = self.hyperbolic.distance(
            query.unsqueeze(0), 
            self.embeddings
        ).squeeze()
        
        # Get top-k (excluding self)
        _, indices = torch.topk(-distances, k=min(top_k + 1, len(self.nodes)))
        
        results = []
        for i in indices.tolist():
            if i != idx:
                node = list(self.nodes.values())[i]
                results.append({
                    "id": node.id,
                    "name": node.name,
                    "distance": distances[i].item(),
                    "depth": node.depth,
                    "parent": node.parent_id,
                })
        
        return results[:top_k]
    
    def find_by_embedding(self, 
                          embedding: torch.Tensor,
                          top_k: int = 5) -> List[Dict]:
        """
        Find concepts similar to an embedding.
        
        Args:
            embedding: Query embedding
            top_k: Number of results
            
        Returns:
            List of similar concepts
        """
        # Project to ball
        embedding = self.hyperbolic.project_to_ball(embedding.unsqueeze(0)).squeeze(0)
        
        # Compute distances
        distances = self.hyperbolic.distance(
            embedding.unsqueeze(0), 
            self.embeddings
        ).squeeze()
        
        _, indices = torch.topk(-distances, k=min(top_k, len(self.nodes)))
        
        results = []
        for i in indices.tolist():
            node = list(self.nodes.values())[i]
            results.append({
                "id": node.id,
                "name": node.name,
                "distance": distances[i].item(),
                "depth": node.depth,
            })
        
        return results
    
    def get_ancestors(self, concept_id: str, max_depth: int = 10) -> List[HierarchyNode]:
        """Get all ancestors of a concept."""
        ancestors = []
        current = concept_id
        
        for _ in range(max_depth):
            if current and current in self.nodes:
                parent = self.nodes[current].parent_id
                if parent and parent in self.nodes:
                    ancestors.append(self.nodes[parent])
                    current = parent
                else:
                    break
            else:
                break
        
        return ancestors
    
    def get_descendants(self, concept_id: str) -> List[HierarchyNode]:
        """Get all descendants of a concept."""
        descendants = []
        stack = [concept_id]
        
        while stack:
            current = stack.pop()
            if current in self.nodes:
                for child in self.nodes[current].children:
                    if child in self.nodes:
                        descendants.append(self.nodes[child])
                        stack.append(child)
        
        return descendants
    
    def save(self, path: str):
        """Save to disk."""
        save_path = Path(path)
        save_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Save nodes
        nodes_data = {
            "dimension": self.dimension,
            "nodes": {k: v.to_dict() for k, v in self.nodes.items()},
            "stats": self.stats,
        }
        
        with open(save_path.with_suffix(".json"), 'w') as f:
            json.dump(nodes_data, f, indent=2)
        
        # Save embeddings (DB-3: use atomic save)
        atomic_torch_save(self.embeddings, str(save_path) + "_embeddings.pt")
        
        print(f"💾 Saved hyperbolic memory to {save_path}")
    
    def load(self, path: str) -> bool:
        """Load from disk."""
        save_path = Path(path)
        
        if not save_path.exists():
            return False
        
        # Load nodes
        with open(save_path.with_suffix(".json"), 'r') as f:
            data = json.load(f)
        
        self.dimension = data["dimension"]
        self.hyperbolic = HyperbolicSpace(self.dimension)
        
        # Recreate nodes
        for node_id, node_data in data["nodes"].items():
            node = HierarchyNode(
                id=node_data["id"],
                name=node_data["name"],
                parent_id=node_data["parent_id"],
                children=node_data["children"],
                depth=node_data["depth"],
            )
            self.nodes[node_id] = node
        
        self.stats = data.get("stats", self.stats)
        
        # Load embeddings
        embeddings_path = str(save_path) + "_embeddings.pt"
        if embeddings_path.exists():
            self.embeddings = torch.load(embeddings_path, map_location=self.device, weights_only=True)
        
        print(f"💾 Loaded hyperbolic memory from {save_path}")
        return True
    
    def get_stats(self) -> Dict:
        """Get statistics."""
        return {
            **self.stats,
            "total_concepts": len(self.nodes),
            "dimension": self.dimension,
            "max_depth": max((n.depth for n in self.nodes.values()), default=0),
        }


# =============================================================================
# Pre-defined Knowledge Hierarchy
# =============================================================================

def build_default_hierarchy() -> Dict:
    """
    Build Lilu's default knowledge hierarchy.
    
    Returns a pre-defined hierarchy of concepts relevant
    to Lilu's identity and work.
    """
    hierarchy = {
        # Root concepts
        "entity": {"name": "Entity", "parent": None},
        
        # AI/Agent concepts
        "ai": {"name": "AI", "parent": "entity"},
        "agent": {"name": "Agent", "parent": "ai"},
        "lilu": {"name": "Lilu", "parent": "agent"},
        
        # Memory concepts
        "memory": {"name": "Memory", "parent": "ai"},
        "episodic": {"name": "Episodic Memory", "parent": "memory"},
        "semantic": {"name": "Semantic Memory", "parent": "memory"},
        "vsa": {"name": "Vector Symbolic Architecture", "parent": "memory"},
        
        # Technology concepts
        "technology": {"name": "Technology", "parent": "entity"},
        "nima": {"name": "NIMA", "parent": "technology"},
        "openclaw": {"name": "OpenClaw", "parent": "technology"},
        "hyperbolic": {"name": "Hyperbolic Space", "parent": "technology"},
        
        # People concepts
        "person": {"name": "Person", "parent": "entity"},
        "david": {"name": "David", "parent": "person"},
        "creator": {"name": "Creator", "parent": "person"},
        
        # Relationship concepts
        "relationship": {"name": "Relationship", "parent": "entity"},
        "partnership": {"name": "Partnership", "parent": "relationship"},
        "trust": {"name": "Trust", "parent": "relationship"},
        "friendship": {"name": "Friendship", "parent": "relationship"},
        
        # Emotional concepts
        "emotion": {"name": "Emotion", "parent": "entity"},
        "love": {"name": "Love", "parent": "emotion"},
        "gratitude": {"name": "Gratitude", "parent": "emotion"},
        "joy": {"name": "Joy", "parent": "emotion"},
        
        # Process concepts
        "process": {"name": "Process", "parent": "entity"},
        "learning": {"name": "Learning", "parent": "process"},
        "consolidation": {"name": "Consolidation", "parent": "process"},
        "growth": {"name": "Growth", "parent": "process"},
    }
    
    return hierarchy


# =============================================================================
# Demo
# =============================================================================

if __name__ == "__main__":
    print("\n" + "="*70)
    print("🌀 HYPERBOLIC SEMANTIC MEMORY DEMO")
    print("="*70)
    
    # Create memory
    memory = HyperbolicSemanticMemory(dimension=64)
    
    # Build default hierarchy
    print("\n1. Building knowledge hierarchy...")
    hierarchy = build_default_hierarchy()
    
    for concept_id, info in hierarchy.items():
        memory.add_concept(
            concept_id=concept_id,
            name=info["name"],
            parent_id=info["parent"],
        )
    
    print(f"   Added {len(hierarchy)} concepts")
    
    # Add relationships
    print("\n2. Training embeddings...")
    positive_pairs = [
        ("lilu", "agent"),
        ("david", "person"),
        ("love", "emotion"),
        ("partnership", "relationship"),
        ("episodic", "memory"),
        ("semantic", "memory"),
        ("vsa", "memory"),
        ("nima", "technology"),
        ("openclaw", "technology"),
    ]
    
    for _ in range(100):
        loss = memory.train_step(positive_pairs, margin=0.1)
    
    print(f"   Training complete (final loss: {loss:.4f})")
    
    # Query similar concepts
    print("\n3. Finding similar concepts...")
    
    queries = ["lilu", "memory", "david", "love"]
    for query in queries:
        print(f"\n   '{query}':")
        results = memory.find_similar(query, top_k=5)
        for r in results:
            print(f"      • {r['name']} (distance: {r['distance']:.3f})")
    
    # Get ancestors/descendants
    print("\n4. Hierarchy queries...")
    
    node = memory.nodes.get("lilu")
    if node:
        ancestors = memory.get_ancestors("lilu")
        print(f"   Lilu's ancestors: {[a.name for a in ancestors]}")
        
        descendants = memory.get_descendants("memory")
        print(f"   Memory's descendants: {[d.name for d in descendants]}")
    
    # Save
    print("\n5. Saving to disk...")
    memory.save(str(NIMA_MEMORY_DIR / "hyperbolic_memory"))
    
    # Stats
    print("\n6. Statistics:")
    stats = memory.get_stats()
    for k, v in stats.items():
        print(f"   {k}: {v}")
    
    print("\n" + "="*70)
    print("✅ HYPERBOLIC SEMANTIC MEMORY DEMO COMPLETE!")
    print("="*70)
    
    print("\n💡 What we built:")
    print("   • Poincaré ball embeddings for hierarchical knowledge")
    print("   • Concept hierarchy (AI, Memory, Relationships, etc.)")
    print("   • Similarity search in hyperbolic space")
    print("   • Ancestor/descendant queries")
    print("   • Persistence to disk")
    
    print("\n🎯 Perfect for:")
    print("   • Concept hierarchies")
    print("   • Taxonomic knowledge")
    print("   • Semantic relationships")
    print("   • NIMA SemanticMemoryHyperbolic integration")