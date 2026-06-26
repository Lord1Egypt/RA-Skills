"""
Event-Based Architecture - Central event bus

Replaces polling with event-driven approach:
- Components publish events instead of direct calls
- Handlers subscribe to events of interest
- Asynchronous processing via queues
"""

import threading
import queue
import time
import uuid
from typing import Dict, List, Callable, Optional, Any
from dataclasses import dataclass, field
from enum import Enum, auto
from collections import defaultdict
import traceback

from kiwi.utils import kiwi_log


class EventType(Enum):
    """System event types."""
    # Audio events
    SPEECH_STARTED = auto()
    SPEECH_ENDED = auto()
    WAKE_WORD_DETECTED = auto()
    COMMAND_RECEIVED = auto()
    
    # State
    STATE_CHANGED = auto()
    DIALOG_MODE_ENTERED = auto()
    DIALOG_MODE_EXITED = auto()
    
    # OpenClaw
    LLM_THINKING_STARTED = auto()
    LLM_THINKING_ENDED = auto()
    LLM_TOKEN_RECEIVED = auto()
    LLM_RESPONSE_COMPLETE = auto()
    
    # TTS
    TTS_STARTED = auto()
    TTS_CHUNK_GENERATED = auto()
    TTS_CHUNK_PLAYING = auto()
    TTS_ENDED = auto()
    TTS_BARGE_IN = auto()
    
    # VAD
    VAD_SPEECH_DETECTED = auto()
    VAD_SILENCE_DETECTED = auto()
    
    # AEC
    AEC_ECHO_DETECTED = auto()
    AEC_ECHO_CANCELLED = auto()
    
    # Speaker
    SPEAKER_IDENTIFIED = auto()
    SPEAKER_BLOCKED = auto()
    
    # Errors
    ERROR_TRANSCRIPTION = auto()
    ERROR_TTS = auto()
    ERROR_LLM = auto()

    # Home Assistant
    HA_COMMAND_SENT = auto()
    HA_COMMAND_RESPONSE = auto()
    HA_CONNECTION_CHANGED = auto()

    # Exec Approval (OpenClaw post-filter)
    EXEC_APPROVAL_REQUESTED = auto()
    EXEC_APPROVAL_RESOLVED = auto()

    # Web Audio
    WEB_CLIENT_CONNECTED = auto()
    WEB_CLIENT_DISCONNECTED = auto()

    # System
    SYSTEM_STARTUP = auto()
    SYSTEM_SHUTDOWN = auto()
    CONFIG_RELOADED = auto()


@dataclass
class Event:
    """System event."""
    type: EventType
    payload: Dict[str, Any] = field(default_factory=dict)
    timestamp: float = field(default_factory=time.time)
    event_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    source: str = "unknown"
    
    def get(self, key: str, default=None):
        """Get value from payload."""
        return self.payload.get(key, default)
    
    def __repr__(self):
        return f"Event({self.type.name}, id={self.event_id}, src={self.source})"


class EventHandler:
    """Wrapper for event handler with priority and filters."""
    
    def __init__(
        self,
        callback: Callable[[Event], None],
        priority: int = 0,
        filter_func: Optional[Callable[[Event], bool]] = None,
        async_mode: bool = True
    ):
        self.callback = callback
        self.priority = priority
        self.filter_func = filter_func
        self.async_mode = async_mode
        self.call_count = 0
        self.total_time = 0.0
    
    def can_handle(self, event: Event) -> bool:
        """Check if handler can handle the event."""
        if self.filter_func is None:
            return True
        try:
            return self.filter_func(event)
        except Exception as e:
            kiwi_log("EVENT", f"Filter error: {e}", level="ERROR")
            return False
    
    def handle(self, event: Event):
        """Invoke the handler."""
        start = time.time()
        try:
            self.callback(event)
        except Exception as e:
            kiwi_log("EVENT", f"Handler error: {e}", level="ERROR")
            traceback.print_exc()
        finally:
            self.call_count += 1
            self.total_time += time.time() - start
    
    @property
    def avg_time(self) -> float:
        """Average execution time."""
        return self.total_time / max(1, self.call_count)


class EventBus:
    """
    Central event bus.

    Pub/Sub pattern for loose coupling of components.
    """
    
    def __init__(self, max_queue_size: int = 1000, num_workers: int = 2):
        self._handlers: Dict[EventType, List[EventHandler]] = defaultdict(list)
        self._event_queue: queue.Queue = queue.Queue(maxsize=max_queue_size)
        self._worker_threads: List[threading.Thread] = []
        self._num_workers = num_workers
        self._running = False
        self._stop_event = threading.Event()
        
        # Statistics
        self._events_published = 0
        self._events_processed = 0
        self._events_dropped = 0
        self._event_times: Dict[EventType, List[float]] = defaultdict(list)
        
        # History (for debugging)
        self._history: List[Event] = []
        self._max_history = 100
        
        self._lock = threading.RLock()
    
    def start(self):
        """Start event processing."""
        if self._running:
            return
        
        self._running = True
        self._stop_event.clear()
        
        for i in range(self._num_workers):
            worker = threading.Thread(
                target=self._worker_loop,
                name=f"EventWorker-{i}",
                daemon=True
            )
            worker.start()
            self._worker_threads.append(worker)
        
        kiwi_log("EVENT_BUS", f"Started with {self._num_workers} workers")
    
    def stop(self):
        """Stop event processing."""
        if not self._running:
            return
        
        self._running = False
        self._stop_event.set()
        
        # Add empty events to unblock workers
        for _ in range(self._num_workers):
            try:
                self._event_queue.put(None, block=False)
            except queue.Full:
                pass
        
        for worker in self._worker_threads:
            worker.join(timeout=2.0)
        
        self._worker_threads.clear()
        kiwi_log("EVENT_BUS", "Stopped")
    
    def _worker_loop(self):
        """Worker event processing loop."""
        while not self._stop_event.is_set():
            try:
                event = self._event_queue.get(timeout=0.1)
                if event is None:  # Stop signal
                    break
                
                self._process_event(event)
                
            except queue.Empty:
                continue
            except Exception as e:
                kiwi_log("EVENT_BUS", f"Worker error: {e}", level="ERROR")
    
    def _process_event(self, event: Event):
        """Process a single event."""
        start_time = time.time()
        
        with self._lock:
            handlers = list(self._handlers.get(event.type, []))
        
        # Sort by priority (higher = earlier)
        handlers.sort(key=lambda h: h.priority, reverse=True)
        
        for handler in handlers:
            if not handler.can_handle(event):
                continue
            
            if handler.async_mode:
                # Asynchronous processing in a separate thread
                threading.Thread(
                    target=handler.handle,
                    args=(event,),
                    daemon=True
                ).start()
            else:
                # Synchronous processing
                handler.handle(event)
        
        # Statistics
        processing_time = time.time() - start_time
        with self._lock:
            self._events_processed += 1
            self._event_times[event.type].append(processing_time)
            if len(self._event_times[event.type]) > 100:
                self._event_times[event.type] = self._event_times[event.type][-50:]
            
            # History
            self._history.append(event)
            if len(self._history) > self._max_history:
                self._history = self._history[-self._max_history:]
    
    def publish(
        self,
        event_type: EventType,
        payload: Optional[Dict[str, Any]] = None,
        source: str = "unknown",
        wait: bool = False
    ) -> Optional[Event]:
        """
        Publish event to the bus.

        Args:
            event_type: Event type
            payload: Event data
            source: Event source
            wait: If True, waits for processing (for critical events)

        Returns:
            Created event (if wait=True) or None
        """
        event = Event(
            type=event_type,
            payload=payload or {},
            source=source
        )
        
        try:
            if wait:
                # Synchronous publishing
                self._process_event(event)
                return event
            else:
                # Asynchronous publishing
                self._event_queue.put(event, block=False)
                with self._lock:
                    self._events_published += 1
                return event
                
        except queue.Full:
            with self._lock:
                self._events_dropped += 1
            kiwi_log("EVENT_BUS", f"Queue full, event dropped: {event_type.name}", level="WARNING")
            return None
    
    def subscribe(
        self,
        event_type: EventType,
        callback: Callable[[Event], None],
        priority: int = 0,
        filter_func: Optional[Callable[[Event], bool]] = None,
        async_mode: bool = True
    ) -> str:
        """
        Subscribe a handler to an event.

        Args:
            event_type: Event type
            callback: Handler function
            priority: Priority (higher = called earlier)
            filter_func: Event filter
            async_mode: Asynchronous processing

        Returns:
            Subscription ID (for unsubscribing)
        """
        handler = EventHandler(callback, priority, filter_func, async_mode)
        
        with self._lock:
            self._handlers[event_type].append(handler)
        
        handler_id = f"{event_type.name}_{id(handler)}"
        kiwi_log("EVENT_BUS", f"Subscribed {callback.__name__} to {event_type.name} (priority={priority})")
        
        return handler_id
    
    def subscribe_multi(
        self,
        event_types: List[EventType],
        callback: Callable[[Event], None],
        priority: int = 0,
        async_mode: bool = True
    ) -> List[str]:
        """Subscribe a single handler to multiple events."""
        ids = []
        for event_type in event_types:
            handler_id = self.subscribe(event_type, callback, priority, async_mode=async_mode)
            ids.append(handler_id)
        return ids
    
    def unsubscribe(self, event_type: EventType, handler_id: str) -> bool:
        """Unsubscribe a handler."""
        with self._lock:
            handlers = self._handlers.get(event_type, [])
            for handler in handlers:
                if f"{event_type.name}_{id(handler)}" == handler_id:
                    handlers.remove(handler)
                    return True
        return False
    
    def get_stats(self) -> Dict[str, Any]:
        """Return bus statistics."""
        with self._lock:
            avg_times = {
                event_type.name: sum(times) / len(times)
                for event_type, times in self._event_times.items()
                if times
            }
            
            handler_counts = {
                event_type.name: len(handlers)
                for event_type, handlers in self._handlers.items()
            }
            
            return {
                'events_published': self._events_published,
                'events_processed': self._events_processed,
                'events_dropped': self._events_dropped,
                'queue_size': self._event_queue.qsize(),
                'handlers_count': handler_counts,
                'avg_processing_time': avg_times,
                'drop_rate': self._events_dropped / max(1, self._events_published),
            }
    
    def get_recent_events(self, count: int = 10) -> List[Event]:
        """Return recent events."""
        with self._lock:
            return self._history[-count:]
    
    def clear_history(self):
        """Clear event history."""
        with self._lock:
            self._history.clear()


# Global event bus instance
_event_bus_instance: Optional[EventBus] = None
_event_bus_lock = threading.Lock()


def get_event_bus() -> EventBus:
    """Return global event bus instance (singleton)."""
    global _event_bus_instance
    
    if _event_bus_instance is None:
        with _event_bus_lock:
            if _event_bus_instance is None:
                _event_bus_instance = EventBus()
    
    return _event_bus_instance


def publish(
    event_type: EventType,
    payload: Optional[Dict[str, Any]] = None,
    source: str = "unknown",
    wait: bool = False
) -> Optional[Event]:
    """Convenience function for publishing events."""
    return get_event_bus().publish(event_type, payload, source, wait)


def subscribe(
    event_type: EventType,
    callback: Callable[[Event], None],
    priority: int = 0,
    async_mode: bool = True
) -> str:
    """Convenience function for subscribing to events."""
    return get_event_bus().subscribe(event_type, callback, priority, async_mode=async_mode)


# Usage examples
def example_usage():
    """Example of event bus usage."""
    bus = EventBus()
    bus.start()
    
    # Subscribe to events
    def on_speech_started(event: Event):
        print(f"Speech started at {event.timestamp}")
    
    def on_command(event: Event):
        command = event.get('command', 'unknown')
        print(f"Command received: {command}")
    
    bus.subscribe(EventType.SPEECH_STARTED, on_speech_started, priority=10)
    bus.subscribe(EventType.COMMAND_RECEIVED, on_command)
    
    # Publish events
    bus.publish(EventType.SPEECH_STARTED, {'volume': 0.5}, source="listener")
    bus.publish(EventType.COMMAND_RECEIVED, {'command': 'привет'}, source="listener")
    
    # Statistics
    print(f"\nStats: {bus.get_stats()}")
    
    time.sleep(1)
    bus.stop()


if __name__ == "__main__":
    example_usage()
