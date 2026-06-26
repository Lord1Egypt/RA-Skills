"""Example NIMA plugins."""

from typing import Dict, Any
from nima_core.plugin_registry import NIMAPlugin

class ExampleScorer(NIMAPlugin):
    """Example scorer plugin - counts keyword matches."""

    name = "example_scorer"
    version = "1.0.0"

    def __init__(self):
        self.keywords = []

    def initialize(self, config: Dict[str, Any]) -> None:
        self.keywords = config.get('keywords', [])

    def shutdown(self) -> None:
        raise NotImplementedError("Override in subclass")

    def score_memory(self, memory: Dict, context: Dict) -> float:
        """Score based on keyword matches."""
        text = memory.get('content', '').lower()
        matches = sum(1 for kw in self.keywords if kw.lower() in text)
        return min(1.0, matches / max(1, len(self.keywords)))

class ExampleEmbedder(NIMAPlugin):
    """Example embedder plugin - returns hash-based vectors."""

    name = "example_embedder"
    version = "1.0.0"

    def __init__(self):
        self.dimension = 128  # Default dimension

    def initialize(self, config: Dict[str, Any]) -> None:
        self.dimension = config.get('dimension', 128)

    def shutdown(self) -> None:
        raise NotImplementedError("Override in subclass")

    def embed(self, text: str) -> list:
        """Simple hash-based embedding with safety checks."""
        if not text:
            return [0.0] * self.dimension
        vec = [0.0] * self.dimension
        text_repeated = text * (self.dimension // len(text) + 1)
        for i, c in enumerate(text_repeated[:self.dimension]):
            vec[i] = ord(c)
        max_val = max(vec) if vec else 1
        if max_val == 0:
            return [0.0] * self.dimension
        return [v / max_val for v in vec]
    
    def get_dimension(self) -> int:
        return self.dimension

def register_examples():
    """Register example plugins with the global registry."""
    from nima_core.plugin_registry import get_registry
    reg = get_registry()
    reg.register(ExampleScorer())
    reg.register(ExampleEmbedder())
