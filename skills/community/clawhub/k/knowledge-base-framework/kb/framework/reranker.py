"""
Re-Ranking for Knowledge Base Hybrid Search
===========================================

Phase 6: Cross-Encoder Re-Ranking after initial hybrid search.
Uses ms-marco-MiniLM-L-6-v2 Cross-Encoder for precise relevance scoring.

Source: KB_Erweiterungs_Plan.md (Phase 6)
"""

import logging
import threading
from typing import Optional, List
from dataclasses import dataclass
from .exceptions import ProviderError

logger = logging.getLogger(__name__)


@dataclass
class RerankResult:
    """Result from re-ranking."""
    index: int  # Original index in result list
    original_result: dict  # Original search result
    rerank_score: float  # Cross-encoder score
    rerank_reason: str = ""  # Optional explanation


class Reranker:
    """
    Cross-Encoder Re-Ranker for search results.
    
    Phase 6: Uses ms-marco-MiniLM-L-6-v2 to re-rank hybrid search results.
    Cross-Encoders are more accurate than bi-encoders (embeddings) because
    they encode the query and document together, allowing for attention-based
    relevance scoring.
    
    Usage:
        reranker = Reranker()
        reranked = reranker.rerank(query, initial_results)
    """
    
    # Cross-Encoder models for re-ranking
    RERANK_MODELS = {
        "ms-marco-MiniLM-L-6-v2": {
            "description": "Microsoft MARCO MiniLM - best for general re-ranking",
            "max_length": 512,
        },
        "cross-encoder/ms-marco-MiniLM-L-6-v2": {
            "description": "Same as above (alternate name)",
            "max_length": 512,
        },
        "cross-encoder-de-MiniLM-L-6-v2": {
            "description": "German-optimized cross-encoder",
            "max_length": 512,
        }
    }
    
    def __init__(
        self,
        model_name: str = "ms-marco-MiniLM-L-6-v2",
        device: Optional[str] = None
    ):
        """
        Initialize Reranker.
        
        Args:
            model_name: Cross-encoder model name
            device: Device for inference ("cpu", "cuda", "mps")
        """
        self.model_name = model_name
        self._model = None
        self._device = device
        
        logger.info(f"Reranker init: model={model_name}")
    
    @property
    def model(self):
        """Lazy-load Cross-Encoder model."""
        if self._model is None:
            from sentence_transformers import CrossEncoder
            self._model = CrossEncoder(self.model_name)
            logger.info(f"Cross-Encoder loaded: {self.model_name}")
        return self._model
    
    def rerank(
        self,
        query: str,
        results: List[dict],
        top_k: int = 20
    ) -> List[dict]:
        """
        Re-rank search results using Cross-Encoder.
        
        Args:
            query: Original search query
            results: List of initial search results (dicts with at least 'content_full' or 'content_preview')
            top_k: Number of top results to return
            
        Returns:
            Re-ranked list of results with rerank_score added
        """
        if not results:
            return []
        
        if not query or not query.strip():
            return results
        
        # Prepare query-document pairs
        pairs = []
        for r in results:
            # Use full content if available, otherwise preview
            doc = r.get('content_full') or r.get('content_preview') or ""
            
            # Truncate long documents (Cross-Encoders have max length)
            if len(doc) > 2000:
                doc = doc[:2000]
            
            pairs.append((query, doc))
        
        # Compute relevance scores
        try:
            scores = self.model.predict(pairs)
            
            # Add scores to results and sort
            scored_results = []
            for i, r in enumerate(results):
                r_copy = r.copy()
                r_copy['rerank_score'] = float(scores[i])
                scored_results.append(r_copy)
            
            # Sort by rerank_score descending
            scored_results.sort(key=lambda x: x['rerank_score'], reverse=True)
            
            logger.info(f"Re-ranked {len(results)} results with {self.model_name}")
            
            return scored_results[:top_k]
            
        except Exception as e:
            logger.warning(f"Cross-Encoder prediction failed: {e}")
            self._last_rerank_error = ProviderError(f"Reranking failed: {e}")
            self._last_rerank_error.__cause__ = e
            # Return original results with 0.0 rerank_score
            for r in results:
                r_copy = r.copy()
                r_copy['rerank_score'] = 0.0
            return results
    
    def rerank_with_explanation(
        self,
        query: str,
        results: List[dict],
        top_k: int = 20
    ) -> List[RerankResult]:
        """
        Re-rank with additional explanation.
        
        Args:
            query: Original search query
            results: List of initial search results
            top_k: Number of top results to return
            
        Returns:
            List of RerankResult with explanations
        """
        reranked = self.rerank(query, results, top_k)
        
        rerank_results = []
        for i, r in enumerate(reranked):
            # Simple explanation: highlight matched terms
            doc = r.get('content_full') or r.get('content_preview') or ""
            query_terms = set(query.lower().split())
            matched_in_doc = [t for t in query_terms if t in doc.lower()]
            
            reason = f"Matched terms: {', '.join(matched_in_doc[:5])}" if matched_in_doc else "No explicit match found"
            
            rerank_results.append(RerankResult(
                index=i,
                original_result=r,
                rerank_score=r.get('rerank_score', 0.0),
                rerank_reason=reason
            ))
        
        return rerank_results
    
    def get_supported_models(self) -> List[str]:
        """Return list of supported model names."""
        return list(self.RERANK_MODELS.keys())


# =============================================================================
# Global instance (lazy)
# =============================================================================

_global_reranker: Optional[Reranker] = None
_reranker_lock = threading.RLock()

def get_reranker(**kwargs) -> Reranker:
    """Get or create global Reranker instance (thread-safe)."""
    global _global_reranker
    if _global_reranker is None:
        with _reranker_lock:
            if _global_reranker is None:
                _global_reranker = Reranker(**kwargs)
    return _global_reranker


def rerank(query: str, results: List[dict], **kwargs) -> List[dict]:
    """
    Convenience function to re-rank results.
    
    Args:
        query: Search query
        results: Initial search results
        **kwargs: Passed to Reranker
        
    Returns:
        Re-ranked results
    """
    return get_reranker(**kwargs).rerank(query, results)


# =============================================================================
# Main: Quick Test
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Cross-Encoder Re-Ranker - Quick Test")
    print("=" * 60)
    
    reranker = Reranker()
    
    # Test query and results
    test_query = "MTHFR Genmutation Behandlung"
    
    test_results = [
        {
            "section_id": "sec1",
            "content_preview": "Die MTHFR Genmutation C677T beeinflusst den Folsäure-Stoffwechsel.",
            "content_full": "Die MTHFR Genmutation C677T ist eine häufige genetische Variante. Sie führt zu erhöhtem Homocystein.",
            "combined_score": 0.8
        },
        {
            "section_id": "sec2", 
            "content_preview": "Behandlung mit 5-MTHF und Vitamin B12.",
            "content_full": "Die Behandlung der MTHFR Mutation umfasst 5-MTHF Supplementierung. Vitamin B12 wird als Cofaktor empfohlen.",
            "combined_score": 0.7
        },
        {
            "section_id": "sec3",
            "content_preview": "Unrelated content about cooking.",
            "content_full": "Dieses Rezept für Pasta ist sehr lecker. Kochen Sie die Nudeln al dente.",
            "combined_score": 0.6
        },
        {
            "section_id": "sec4",
            "content_preview": "Homocystein und Methylierung sind wichtig.",
            "content_full": "Erhöhter Homocystein-Spiegel durch MTHFR Mutation. Methylierung ist ein wichtiger Prozess.",
            "combined_score": 0.75
        }
    ]
    
    print(f"\n[1] Query: {test_query}")
    print(f"    Initial results: {len(test_results)}")
    
    print(f"\n[2] Supported Models:")
    for model in reranker.get_supported_models():
        info = reranker.RERANK_MODELS[model]
        print(f"   - {model}: {info['description']}")
    
    print(f"\n[3] Re-ranking...")
    reranked = reranker.rerank(test_query, test_results, top_k=4)
    
    print(f"\n[4] Results after re-ranking:")
    print(f"    {'Rank':<6} {'Section ID':<12} {'Combined':<10} {'Rerank':<10} Content Preview")
    print(f"    {'-'*70}")
    for i, r in enumerate(reranked):
        print(f"    {i+1:<6} {r['section_id']:<12} {r['combined_score']:<10.3f} {r['rerank_score']:<10.3f} {r['content_preview'][:40]}...")
    
    print("\n[5] Re-ranking with explanation:")
    explained = reranker.rerank_with_explanation(test_query, test_results, top_k=2)
    for er in explained:
        print(f"    Rank {er.index+1}: score={er.rerank_score:.3f}")
        print(f"    Reason: {er.rerank_reason}")
    
    print("\n" + "=" * 60)
    print("Test Complete!")
    print("=" * 60)