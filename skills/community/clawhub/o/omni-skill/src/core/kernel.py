import time
import logging
import importlib
import inspect
from typing import Dict, Any, Type, List
from .interfaces import OmniPlugin, OmniRequest, OmniResponse, OmniErrorCode, EventType, OmniEvent
from .config import ConfigManager
from .metrics import CircuitBreaker, RateLimiter, with_timeout
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config.settings as settings

class EventBus:
    def __init__(self):
        self.listeners: Dict[EventType, List[Any]] = {e: [] for e in EventType}

    def subscribe(self, event_type: EventType, callback):
        self.listeners[event_type].append(callback)

    def publish(self, event: OmniEvent):
        for callback in self.listeners.get(event.event_type, []):
            try:
                callback(event)
            except Exception as e:
                logging.error(f"Error in event listener: {e}")

class PluginManager:
    def __init__(self, kernel):
        self.kernel = kernel
        self.plugins: Dict[str, OmniPlugin] = {}
        self.circuit_breakers: Dict[str, CircuitBreaker] = {}
        self.rate_limiters: Dict[str, RateLimiter] = {}

    def register(self, plugin_class: Type[OmniPlugin]):
        plugin = plugin_class()
        name = plugin.name
        
        # Dependency check
        for dep in plugin.dependencies:
            if dep not in self.plugins:
                logging.warning(f"Plugin {name} missing dependency {dep}")
        
        # Lifecycle: init
        try:
            plugin_config = self.kernel.config.get(f"plugin_{name}", {})
            plugin.on_init(plugin_config)
            
            self.plugins[name] = plugin
            self.circuit_breakers[name] = CircuitBreaker()
            
            # Use configured rate limit or default
            max_req = plugin_config.get("rate_limit_max", 100)
            window = plugin_config.get("rate_limit_window", 1.0)
            self.rate_limiters[name] = RateLimiter(max_req, window)
            
            self.kernel.events.publish(OmniEvent(
                event_type=EventType.PLUGIN_LOADED,
                source="PluginManager",
                timestamp=time.time(),
                data={"plugin_name": name}
            ))
            logging.info(f"Plugin {name} registered successfully.")
        except Exception as e:
            logging.error(f"Failed to initialize plugin {name}: {e}")

    def load_from_module(self, module_name: str):
        module = importlib.import_module(module_name)
        for name, obj in inspect.getmembers(module):
            if inspect.isclass(obj) and issubclass(obj, OmniPlugin) and obj is not OmniPlugin:
                self.register(obj)

    def execute(self, request: OmniRequest) -> OmniResponse:
        plugin_name = request.plugin_name
        if plugin_name not in self.plugins:
            return OmniResponse(code=OmniErrorCode.PLUGIN_NOT_FOUND, message=f"Plugin {plugin_name} not found")

        cb = self.circuit_breakers[plugin_name]
        rl = self.rate_limiters[plugin_name]

        if not cb.allow_request():
            return OmniResponse(code=OmniErrorCode.PLUGIN_CIRCUIT_BROKEN, message="Circuit breaker is OPEN")
        
        if not rl.allow_request():
            return OmniResponse(code=OmniErrorCode.RATE_LIMIT_EXCEEDED, message="Rate limit exceeded")

        plugin = self.plugins[plugin_name]
        start_time = time.time()
        
        try:
            # Lifecycle / Event: Before Execute
            self.kernel.events.publish(OmniEvent(
                event_type=EventType.BEFORE_EXECUTE,
                source=plugin_name,
                timestamp=start_time,
                data={"action": request.action}
            ))

            # Execute with timeout
            timeout = self.kernel.config.get("plugin_timeout", settings.PLUGIN_TIMEOUT_DEFAULT)
            result = with_timeout(plugin.execute, timeout, request.action, request.payload, request.context)
            
            cb.record_success()
            duration = time.time() - start_time
            
            self.kernel.events.publish(OmniEvent(
                event_type=EventType.AFTER_EXECUTE,
                source=plugin_name,
                timestamp=time.time(),
                data={"action": request.action, "duration": duration}
            ))
            
            return OmniResponse(
                code=OmniErrorCode.SUCCESS, 
                data=result,
                metrics={"duration_ms": duration * 1000}
            )

        except TimeoutError as te:
            cb.record_failure()
            return OmniResponse(code=OmniErrorCode.PLUGIN_EXECUTION_TIMEOUT, message=str(te))
        except Exception as e:
            cb.record_failure()
            self.kernel.events.publish(OmniEvent(
                event_type=EventType.ON_ERROR,
                source=plugin_name,
                timestamp=time.time(),
                data={"error": str(e)}
            ))
            return OmniResponse(code=OmniErrorCode.INTERNAL_ERROR, message=str(e))

    def shutdown_all(self):
        for name, plugin in self.plugins.items():
            try:
                plugin.on_destroy()
                logging.info(f"Plugin {name} destroyed gracefully.")
            except Exception as e:
                logging.error(f"Error destroying plugin {name}: {e}")

class MicroKernel:
    def __init__(self, config_path: str = "config.yaml"):
        self.config = ConfigManager(config_path)
        self.events = EventBus()
        self.plugins = PluginManager(self)
        self._is_running = False

    def start(self):
        self.config.load_config()
        self.events.publish(OmniEvent(
            event_type=EventType.KERNEL_STARTING,
            source="MicroKernel",
            timestamp=time.time(),
            data={}
        ))
        
        for plugin in self.plugins.plugins.values():
            plugin.on_start()
            
        self._is_running = True
        self.events.publish(OmniEvent(
            event_type=EventType.KERNEL_READY,
            source="MicroKernel",
            timestamp=time.time(),
            data={}
        ))
        logging.info("OmniSkill Kernel started successfully.")

    def shutdown(self):
        self.events.publish(OmniEvent(
            event_type=EventType.KERNEL_SHUTTING_DOWN,
            source="MicroKernel",
            timestamp=time.time(),
            data={}
        ))
        self.plugins.shutdown_all()
        self._is_running = False
        logging.info("OmniSkill Kernel shut down.")

    def dispatch(self, request: OmniRequest) -> OmniResponse:
        return self.plugins.execute(request)
