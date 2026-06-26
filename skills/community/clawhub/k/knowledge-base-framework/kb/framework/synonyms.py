"""
Synonym Expansion for Knowledge Base Query Processing
=====================================================

Phase 2: SynonymExpander with medical/technical thesaurus.
Expands queries before search for better recall.

Source: KB_Erweiterungs_Plan.md (Phase 2)
"""

import json
import logging
import threading
from pathlib import Path
from typing import Optional
from .stopwords import StopwordHandler

logger = logging.getLogger(__name__)

# Resolve data directory relative to this file
_DATA_DIR = Path(__file__).parent / "data"


def _load_synonyms_json(filename: str) -> dict:
    """Load synonyms from a JSON data file.

    Args:
        filename: Name of the JSON file in the data directory

    Returns:
        Dictionary mapping terms to synonym lists
    """
    json_path = _DATA_DIR / filename
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        logger.warning(f"Synonyms JSON not found: {json_path}, using empty fallback")
        return {}
    except json.JSONDecodeError as e:
        logger.warning(f"Synonyms JSON parse error ({filename}): {e}, using empty fallback")
        return {}


# Load synonym data at module level (from JSON)
MEDICAL_SYNONYMS: dict = _load_synonyms_json("synonyms_medical.json")
TECHNICAL_SYNONYMS: dict = _load_synonyms_json("synonyms_technical.json")


class SynonymExpander:
    """
    Query expansion via medical and technical synonyms.
    
    Expands query terms before search to improve recall.
    For example:
    - "Herzinfarkt" → "Herzinfarkt Herzattacke myocardial infarction heart attack"
    - "Bluthochdruck" → "Bluthochdruck Hypertension arterielle Hypertonie"
    
    Synonym data is loaded from:
    - data/synonyms_medical.json
    - data/synonyms_technical.json
    
    Two-tier approach:
    1. Exact synonym lookup (fast)
    2. Conceptual expansion (slower, optional)
    """
    
    def __init__(self, use_medial: bool = True, use_technical: bool = True):
        """
        Initialize SynonymExpander.
        
        Args:
            use_medial: Include medical synonyms
            use_technical: Include technical synonyms
        """
        self.use_medial = use_medial
        self.use_technical = use_technical
        self.stopword_handler = StopwordHandler()
        
        # Build combined lookup from JSON-loaded data
        self._synonym_map: dict[str, list[str]] = {}
        if use_medial:
            self._synonym_map.update(MEDICAL_SYNONYMS)
        if use_technical:
            self._synonym_map.update(TECHNICAL_SYNONYMS)
        
        logger.info(f"SynonymExpander init: {len(self._synonym_map)} base terms")
    
    def _clean_term(self, term: str) -> str:
        """Clean and normalize a term."""
        return term.lower().strip()
    
    def _is_stopword(self, term: str) -> bool:
        """Check if term is a stopword."""
        return self.stopword_handler.is_stopword(term)
    
    def expand_term(self, term: str) -> list[str]:
        """
        Expand a single term with synonyms.
        
        Args:
            term: Single term to expand
            
        Returns:
            List including original term and all synonyms
        """
        clean = self._clean_term(term)
        if not clean or self._is_stopword(clean):
            return [clean] if clean else []
        
        if clean in self._synonym_map:
            synonyms = self._synonym_map[clean]
            return [clean] + synonyms
        
        return [clean]
    
    def expand_query(
        self, 
        query: str, 
        include_original: bool = True
    ) -> str:
        """
        Expand a full query string with synonyms.
        
        Args:
            query: Query string to expand
            include_original: Include original terms in expanded query
            
        Returns:
            Expanded query string with synonyms added
        """
        if not query or not query.strip():
            return query
        
        # Parse terms (simple whitespace split)
        terms = query.split()
        expanded_terms = []
        
        for term in terms:
            clean = self._clean_term(term)
            
            # Skip very short terms
            if len(clean) < 2:
                expanded_terms.append(term)
                continue
            
            # Skip stopwords
            if self._is_stopword(clean):
                expanded_terms.append(term)
                continue
            
            # Expand
            synonyms = self.expand_term(clean)
            
            if include_original:
                expanded_terms.append(term)
            
            # Add synonyms (without duplicates)
            for syn in synonyms:
                if syn not in [t.lower() for t in expanded_terms]:
                    expanded_terms.append(syn)
        
        return " ".join(expanded_terms)
    
    def get_synonyms(self, term: str) -> list[str]:
        """
        Get all synonyms for a term (without original).
        
        Args:
            term: Term to look up
            
        Returns:
            List of synonyms (not including original)
        """
        clean = self._clean_term(term)
        return self._synonym_map.get(clean, [])
    
    def has_synonyms(self, term: str) -> bool:
        """Check if a term has known synonyms."""
        return self._clean_term(term) in self._synonym_map
    
    def add_custom_synonym(
        self, 
        term: str, 
        synonyms: list[str],
        category: str = "custom"
    ) -> None:
        """
        Add custom synonyms at runtime.
        
        Args:
            term: Base term (lowercase)
            synonyms: List of synonym terms
            category: Category label (for debugging)
        """
        clean = self._clean_term(term)
        if clean in self._synonym_map:
            # Merge with existing
            existing = set(self._synonym_map[clean])
            existing.update(synonyms)
            self._synonym_map[clean] = list(existing)
        else:
            self._synonym_map[clean] = synonyms
        
        logger.info(f"Added {len(synonyms)} custom synonyms for '{term}' ({category})")


# =============================================================================
# Global instance (lazy)
# =============================================================================

_global_expander: Optional[SynonymExpander] = None
_expander_lock = threading.RLock()

def get_expander(**kwargs) -> SynonymExpander:
    """Get or create global SynonymExpander instance (thread-safe)."""
    global _global_expander
    if _global_expander is None:
        with _expander_lock:
            if _global_expander is None:
                _global_expander = SynonymExpander(**kwargs)
    return _global_expander


def expand_query(query: str, **kwargs) -> str:
    """
    Convenience function to expand a query.
    
    Args:
        query: Query string to expand
        **kwargs: Passed to SynonymExpander
        
    Returns:
        Expanded query string
    """
    return get_expander(**kwargs).expand_query(query)


# =============================================================================
# Main: Quick Test
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Synonym Expander - Quick Test")
    print("=" * 60)
    
    expander = SynonymExpander()
    
    # Test medical terms
    test_queries = [
        "herzinfarkt behandlung",
        "bluthochdruck medikamente",
        "mthfr mutation methylierung",
        "diabetes symptome",
        "ki suchmaschine vektordatenbank",
        "obsidian vault markdown",
    ]
    
    print("\n[1] Query Expansion Tests:")
    for q in test_queries:
        expanded = expander.expand_query(q)
        print(f"\n   Original: {q}")
        print(f"   Expanded: {expanded}")
    
    print("\n[2] Single Term Lookup:")
    for term in ["herzinfarkt", "ki", "embedding", "mthfr"]:
        syns = expander.get_synonyms(term)
        print(f"   '{term}' → {syns[:5]}{'...' if len(syns) > 5 else ''}")
    
    print("\n[3] Custom Synonym Addition:")
    expander.add_custom_synonym("test", ["probe", "versuch", "examination"], "test_category")
    print(f"   Added 'test' → {expander.get_synonyms('test')}")
    
    print("\n" + "=" * 60)
    print("Test Complete!")
    print("=" * 60)