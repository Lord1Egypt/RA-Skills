"""Stack-specific analyzers."""

from .base import StackAnalyzer
from .node import NodeAnalyzer
from .python import PythonAnalyzer
from .go import GoAnalyzer

__all__ = [
    'StackAnalyzer',
    'NodeAnalyzer',
    'PythonAnalyzer',
    'GoAnalyzer'
]

# Registry mapping stack names to their analyzers
STACK_REGISTRY = {
    'node': NodeAnalyzer(),
    'python': PythonAnalyzer(),
    'go': GoAnalyzer()
}


def get_analyzer(stack: str) -> StackAnalyzer:
    """Get the appropriate analyzer for a given stack."""
    return STACK_REGISTRY.get(stack)
