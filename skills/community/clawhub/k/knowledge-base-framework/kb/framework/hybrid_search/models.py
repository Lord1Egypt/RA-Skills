"""
Search Result and Configuration Models
=======================================

Data models for the hybrid search system.
"""

from dataclasses import dataclass


@dataclass
class SearchResult:
    """Single search result with combined scoring."""
    section_id: str
    file_id: str
    file_path: str
    section_header: str
    content_preview: str
    content_full: str
    section_level: int
    importance_score: float
    keywords: list[str]
    
    # Combined scores
    semantic_score: float = 0.0   # ChromaDB similarity
    keyword_score: float = 0.0    # SQLite keyword match
    combined_score: float = 0.0    # Weighted combination
    
    # Source info
    source: str = ""  # "chroma", "sqlite", "hybrid"


@dataclass
class SearchConfig:
    """Configuration for hybrid search."""
    # Weights for score combination
    semantic_weight: float = 0.60   # 60% semantic
    keyword_weight: float = 0.40     # 40% keyword
    
    # ChromaDB settings - more results for better results
    semantic_limit: int = 100        # Top N from semantic search
    keyword_limit: int = 100       # Top N from keyword search
    
    # Final results
    final_limit: int = 20
    
    # Minimum scores - lower for more results
    min_combined_score: float = 0.05
    
    # Boost factors
    importance_boost: bool = True    # Boost by importance_score
    recency_boost: bool = False       # Boost recent content
    keyword_exact_boost: float = 1.5 # Boost exact keyword matches
    
    # Score normalization
    normalize_scores: bool = True    # Normalize scores to 0-1 range