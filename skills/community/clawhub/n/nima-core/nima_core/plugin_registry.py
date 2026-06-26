"""Simple plugin registry for NIMA Core."""

from typing import Dict, List, Optional, Protocol, Any
import logging

logger = logging.getLogger(__name__)

class NIMAPlugin(Protocol):
    """Base protocol for all NIMA plugins."""
    name: str
    version: str
    
    def initialize(self, config: Dict[str, Any]) -> None: ...
    def shutdown(self) -> None: ...

class PluginRegistry:
    """Simple registry for NIMA plugins."""
    
    def __init__(self):
        self._plugins: Dict[str, NIMAPlugin] = {}
    
    def register(self, plugin: NIMAPlugin) -> None:
        """Register a plugin."""
        self._plugins[plugin.name] = plugin
        logger.info(f"Registered plugin: {plugin.name} v{plugin.version}")
    
    def get(self, name: str) -> Optional[NIMAPlugin]:
        """Get plugin by name."""
        return self._plugins.get(name)
    
    def list_all(self) -> List[str]:
        """List all registered plugins."""
        return list(self._plugins.keys())

# Global registry instance
_registry = PluginRegistry()

def get_registry() -> PluginRegistry:
    """Get the global plugin registry instance."""
    return _registry
