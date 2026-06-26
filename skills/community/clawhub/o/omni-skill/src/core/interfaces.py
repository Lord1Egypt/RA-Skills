from enum import Enum
from typing import Any, Dict, List, Optional, Callable
from pydantic import BaseModel, Field

# 1. Error Codes
class OmniErrorCode(Enum):
    SUCCESS = 0
    PLUGIN_NOT_FOUND = 1001
    PLUGIN_INIT_FAILED = 1002
    PLUGIN_EXECUTION_TIMEOUT = 1003
    PLUGIN_CIRCUIT_BROKEN = 1004
    RATE_LIMIT_EXCEEDED = 1005
    CONFIG_VALIDATION_ERROR = 2001
    INTERNAL_ERROR = 5000

# 2. Input/Output Schemas
class OmniRequest(BaseModel):
    plugin_name: str = Field(..., description="Name of the plugin to execute")
    action: str = Field(..., description="Action or method to invoke on the plugin")
    payload: Dict[str, Any] = Field(default_factory=dict, description="Parameters for the action")
    context: Dict[str, Any] = Field(default_factory=dict, description="Shared context or environment variables")

class OmniResponse(BaseModel):
    code: OmniErrorCode = Field(default=OmniErrorCode.SUCCESS)
    message: str = Field(default="Success")
    data: Optional[Any] = Field(default=None)
    metrics: Dict[str, Any] = Field(default_factory=dict, description="Execution metrics (e.g., duration_ms, memory_usage)")

# 3. Event Model
class EventType(Enum):
    KERNEL_STARTING = "kernel_starting"
    KERNEL_READY = "kernel_ready"
    KERNEL_SHUTTING_DOWN = "kernel_shutting_down"
    PLUGIN_LOADED = "plugin_loaded"
    PLUGIN_UNLOADED = "plugin_unloaded"
    BEFORE_EXECUTE = "before_execute"
    AFTER_EXECUTE = "after_execute"
    ON_ERROR = "on_error"

class OmniEvent(BaseModel):
    event_type: EventType
    source: str
    timestamp: float
    data: Dict[str, Any]

# 4. Plugin Base Interface
class OmniPlugin:
    """Base class for all OmniSkill plugins."""
    name: str = "BasePlugin"
    version: str = "1.0.0"
    dependencies: List[str] = []
    
    def on_init(self, config: Dict[str, Any]) -> None:
        """Lifecycle Hook: Called when the plugin is initialized."""
        pass
        
    def on_start(self) -> None:
        """Lifecycle Hook: Called when the kernel starts."""
        pass
        
    def on_pause(self) -> None:
        """Lifecycle Hook: Called to pause operations."""
        pass
        
    def on_destroy(self) -> None:
        """Lifecycle Hook: Called during graceful shutdown to clean up resources."""
        pass
        
    def execute(self, action: str, payload: Dict[str, Any], context: Dict[str, Any]) -> Any:
        """Main execution entry point."""
        raise NotImplementedError("Plugins must implement the execute method")
