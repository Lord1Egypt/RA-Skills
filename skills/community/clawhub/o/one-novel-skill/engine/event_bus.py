#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
event_bus.py — 统一事件总线 (v6: 线程安全)

串联所有引擎的输出，解决信息孤岛问题。
引擎发布事件 → 订阅者消费事件 → 编排层统一处理。

v6 增强:
- 所有公开方法增加 threading.Lock 保护
- get_event_bus() 双重检查锁
"""

import logging
import threading
from dataclasses import dataclass, field
from typing import Dict, List, Any, Callable, Optional
from enum import Enum

_log = logging.getLogger("event_bus")


class EventType(str, Enum):
    ENGINE_ANALYZED = "engine_analyzed"
    CHAPTER_GENERATED = "chapter_generated"
    CONTRACT_CONFIRMED = "contract_confirmed"
    PREWRITING_PREVIEW_READY = "prewriting_preview_ready"
    MEMORY_CONFLICT = "memory_conflict"
    REDLINE_VIOLATED = "redline_violated"
    QUALITY_GATE_RESULT = "quality_gate_result"
    PERSIST_COMPLETED = "persist_completed"
    CHAPTER_FAILED = "chapter_failed"
    BATCH_COMPLETED = "batch_completed"


@dataclass
class Event:
    type: EventType
    chapter: int
    data: Dict[str, Any] = field(default_factory=dict)
    source: str = ""


class EventBus:
    """统一事件总线 — 发布/订阅模式（线程安全）"""

    def __init__(self):
        self._lock = threading.Lock()
        self._subscribers: Dict[EventType, List[Callable]] = {
            et: [] for et in EventType
        }
        self._event_log: List[Event] = []

    def subscribe(self, event_type: EventType, callback: Callable):
        with self._lock:
            self._subscribers[event_type].append(callback)

    def unsubscribe(self, event_type: EventType, callback: Callable):
        with self._lock:
            if callback in self._subscribers[event_type]:
                self._subscribers[event_type].remove(callback)

    def publish(self, event: Event):
        with self._lock:
            self._event_log.append(event)
            # 复制订阅者列表，避免在锁内执行回调时死锁
            subscribers = list(self._subscribers.get(event.type, []))
        for callback in subscribers:
            try:
                callback(event)
            except Exception as e:
                _log.warning(f"EventBus: subscriber for {event.type} failed: {e}")

    def get_log(self, limit: int = 50) -> List[Dict]:
        with self._lock:
            return [
                {"type": e.type.value, "chapter": e.chapter, "source": e.source,
                 "data_keys": list(e.data.keys())}
                for e in self._event_log[-limit:]
            ]

    def get_by_type(self, event_type: EventType, limit: int = 20) -> List[Event]:
        with self._lock:
            return [e for e in self._event_log if e.type == event_type][-limit:]

    def clear(self):
        with self._lock:
            self._event_log.clear()

    def stats(self) -> Dict[str, int]:
        with self._lock:
            counts = {}
            for e in self._event_log:
                counts[e.type.value] = counts.get(e.type.value, 0) + 1
            return counts


# 全局单例（双重检查锁）
_bus_instance: Optional[EventBus] = None
_bus_lock = threading.Lock()


def get_event_bus() -> EventBus:
    global _bus_instance
    if _bus_instance is None:
        with _bus_lock:
            if _bus_instance is None:
                _bus_instance = EventBus()
    return _bus_instance


def reset_event_bus():
    global _bus_instance
    with _bus_lock:
        _bus_instance = EventBus()
