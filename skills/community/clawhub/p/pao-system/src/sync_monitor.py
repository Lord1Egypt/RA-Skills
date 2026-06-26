"""
Sync Monitor Module - 同步状态监控模块

提供同步状态跟踪、性能指标、日志记录等功能
"""

import asyncio
import logging
import time
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum
from collections import deque
import json

logger = logging.getLogger(__name__)


class SyncState(Enum):
    """同步状态"""
    IDLE = "idle"
    SYNCING = "syncing"
    SYNCED = "synced"
    ERROR = "error"
    OFFLINE = "offline"


class SyncEventType(Enum):
    """同步事件类型"""
    START = "sync_start"
    COMPLETE = "sync_complete"
    ERROR = "sync_error"
    CONFLICT = "sync_conflict"
    RETRY = "sync_retry"


@dataclass
class SyncEvent:
    """同步事件"""
    event_type: SyncEventType
    timestamp: float
    peer_id: str
    details: Dict[str, Any] = field(default_factory=dict)
    duration_ms: float = 0


@dataclass
class SyncMetrics:
    """同步性能指标"""
    total_syncs: int = 0
    successful_syncs: int = 0
    failed_syncs: int = 0
    conflicts_resolved: int = 0
    total_bytes_sent: int = 0
    total_bytes_received: int = 0
    avg_latency_ms: float = 0
    last_sync_time: float = 0
    last_sync_duration_ms: float = 0


class SyncStateTracker:
    """同步状态跟踪器"""
    
    def __init__(self):
        self._state: SyncState = SyncState.IDLE
        self._peer_states: Dict[str, SyncState] = {}
        self._state_history: deque = deque(maxlen=100)
        self._callbacks: Dict[str, List[callable]] = {}
        self._lock = asyncio.Lock()
    
    @property
    def state(self) -> SyncState:
        """获取当前状态"""
        return self._state
    
    async def set_state(self, state: SyncState, peer_id: Optional[str] = None) -> None:
        """设置同步状态"""
        async with self._lock:
            old_state = self._state
            self._state = state
            
            # 记录历史
            self._state_history.append({
                "from": old_state.value,
                "to": state.value,
                "peer_id": peer_id,
                "timestamp": time.time()
            })
            
            # 触发回调
            await self._trigger_callback("state_changed", old_state, state, peer_id)
            
            logger.info(f"同步状态变化: {old_state.value} -> {state.value}" + 
                       (f" (peer: {peer_id})" if peer_id else ""))
    
    async def set_peer_state(self, peer_id: str, state: SyncState) -> None:
        """设置对等节点状态"""
        async with self._lock:
            self._peer_states[peer_id] = state
            await self._trigger_callback("peer_state_changed", peer_id, state)
    
    async def get_peer_state(self, peer_id: str) -> SyncState:
        """获取对等节点状态"""
        return self._peer_states.get(peer_id, SyncState.OFFLINE)
    
    async def get_all_peer_states(self) -> Dict[str, SyncState]:
        """获取所有对等节点状态"""
        return self._peer_states.copy()
    
    def get_state_history(self) -> List[Dict]:
        """获取状态历史"""
        return list(self._state_history)
    
    def register_callback(self, event: str, callback: callable) -> None:
        """注册回调"""
        if event not in self._callbacks:
            self._callbacks[event] = []
        self._callbacks[event].append(callback)
    
    async def _trigger_callback(self, event: str, *args, **kwargs) -> None:
        """触发回调"""
        if event in self._callbacks:
            for callback in self._callbacks[event]:
                try:
                    if asyncio.iscoroutinefunction(callback):
                        await callback(*args, **kwargs)
                    else:
                        callback(*args, **kwargs)
                except Exception as e:
                    logger.error(f"回调执行失败: {e}")


class SyncMetricsCollector:
    """同步性能指标收集器"""
    
    def __init__(self):
        self._metrics = SyncMetrics()
        self._latencies: deque = deque(maxlen=1000)
        self._lock = asyncio.Lock()
    
    async def record_sync_start(self) -> None:
        """记录同步开始"""
        async with self._lock:
            self._metrics.total_syncs += 1
    
    async def record_sync_complete(self, duration_ms: float, bytes_sent: int = 0, bytes_received: int = 0) -> None:
        """记录同步完成"""
        async with self._lock:
            self._metrics.successful_syncs += 1
            self._metrics.last_sync_time = time.time()
            self._metrics.last_sync_duration_ms = duration_ms
            self._metrics.total_bytes_sent += bytes_sent
            self._metrics.total_bytes_received += bytes_received
            
            # 更新平均延迟
            self._latencies.append(duration_ms)
            self._metrics.avg_latency_ms = sum(self._latencies) / len(self._latencies)
    
    async def record_sync_error(self) -> None:
        """记录同步错误"""
        async with self._lock:
            self._metrics.failed_syncs += 1
    
    async def record_conflict(self) -> None:
        """记录冲突"""
        async with self._lock:
            self._metrics.conflicts_resolved += 1
    
    async def get_metrics(self) -> Dict[str, Any]:
        """获取指标"""
        async with self._lock:
            return {
                "total_syncs": self._metrics.total_syncs,
                "successful_syncs": self._metrics.successful_syncs,
                "failed_syncs": self._metrics.failed_syncs,
                "conflicts_resolved": self._metrics.conflicts_resolved,
                "total_bytes_sent": self._metrics.total_bytes_sent,
                "total_bytes_received": self._metrics.total_bytes_received,
                "avg_latency_ms": round(self._metrics.avg_latency_ms, 2),
                "last_sync_time": self._metrics.last_sync_time,
                "last_sync_duration_ms": round(self._metrics.last_sync_duration_ms, 2),
                "success_rate": self._calculate_success_rate()
            }
    
    def _calculate_success_rate(self) -> float:
        """计算成功率"""
        if self._metrics.total_syncs == 0:
            return 0.0
        return self._metrics.successful_syncs / self._metrics.total_syncs * 100
    
    async def reset(self) -> None:
        """重置指标"""
        async with self._lock:
            self._metrics = SyncMetrics()
            self._latencies.clear()


class SyncLogger:
    """同步日志记录器"""
    
    def __init__(self, log_file: Optional[str] = None):
        self._log_file = log_file
        self._events: deque = deque(maxlen=1000)
        self._lock = asyncio.Lock()
    
    async def log_event(self, event: SyncEvent) -> None:
        """记录事件"""
        async with self._lock:
            self._events.append(event)
            
            # 同时输出到标准日志
            log_msg = f"[SYNC] {event.event_type.value} - peer: {event.peer_id}"
            if event.details:
                log_msg += f" - {json.dumps(event.details)}"
            if event.duration_ms > 0:
                log_msg += f" - {event.duration_ms:.2f}ms"
            
            logger.info(log_msg)
            
            # 写入文件
            if self._log_file:
                await self._write_to_file(event)
    
    async def _write_to_file(self, event: SyncEvent) -> None:
        """写入日志文件"""
        try:
            with open(self._log_file, 'a', encoding='utf-8') as f:
                log_entry = {
                    "event_type": event.event_type.value,
                    "timestamp": event.timestamp,
                    "peer_id": event.peer_id,
                    "details": event.details,
                    "duration_ms": event.duration_ms
                }
                f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")
        except Exception as e:
            logger.error(f"写入日志文件失败: {e}")
    
    async def get_recent_events(self, count: int = 50) -> List[SyncEvent]:
        """获取最近事件"""
        async with self._lock:
            return list(self._events)[-count:]
    
    async def get_events_by_peer(self, peer_id: str) -> List[SyncEvent]:
        """获取指定对等节点的事件"""
        async with self._lock:
            return [e for e in self._events if e.peer_id == peer_id]
    
    async def get_events_by_type(self, event_type: SyncEventType) -> List[SyncEvent]:
        """获取指定类型的事件"""
        async with self._lock:
            return [e for e in self._events if e.event_type == event_type]
    
    async def clear(self) -> None:
        """清空日志"""
        async with self._lock:
            self._events.clear()


class SyncMonitor:
    """同步监控器（整合模块）"""
    
    def __init__(self, log_file: Optional[str] = None):
        self.state_tracker = SyncStateTracker()
        self.metrics_collector = SyncMetricsCollector()
        self.logger = SyncLogger(log_file)
        self._running = False
    
    async def start(self) -> None:
        """启动监控"""
        self._running = True
        logger.info("同步监控器已启动")
    
    async def stop(self) -> None:
        """停止监控"""
        self._running = False
        logger.info("同步监控器已停止")
    
    async def on_sync_start(self, peer_id: str) -> None:
        """同步开始回调"""
        await self.state_tracker.set_state(SyncState.SYNCING, peer_id)
        await self.state_tracker.set_peer_state(peer_id, SyncState.SYNCING)
        await self.metrics_collector.record_sync_start()
        
        event = SyncEvent(
            event_type=SyncEventType.START,
            timestamp=time.time(),
            peer_id=peer_id
        )
        await self.logger.log_event(event)
    
    async def on_sync_complete(self, peer_id: str, duration_ms: float, bytes_sent: int = 0, bytes_received: int = 0) -> None:
        """同步完成回调"""
        await self.state_tracker.set_state(SyncState.SYNCED, peer_id)
        await self.state_tracker.set_peer_state(peer_id, SyncState.SYNCED)
        await self.metrics_collector.record_sync_complete(duration_ms, bytes_sent, bytes_received)
        
        event = SyncEvent(
            event_type=SyncEventType.COMPLETE,
            timestamp=time.time(),
            peer_id=peer_id,
            duration_ms=duration_ms
        )
        await self.logger.log_event(event)
    
    async def on_sync_error(self, peer_id: str, error: str) -> None:
        """同步错误回调"""
        await self.state_tracker.set_state(SyncState.ERROR, peer_id)
        await self.state_tracker.set_peer_state(peer_id, SyncState.ERROR)
        await self.metrics_collector.record_sync_error()
        
        event = SyncEvent(
            event_type=SyncEventType.ERROR,
            timestamp=time.time(),
            peer_id=peer_id,
            details={"error": error}
        )
        await self.logger.log_event(event)
    
    async def on_conflict(self, peer_id: str, conflict_type: str, resolution: str) -> None:
        """冲突解决回调"""
        await self.metrics_collector.record_conflict()
        
        event = SyncEvent(
            event_type=SyncEventType.CONFLICT,
            timestamp=time.time(),
            peer_id=peer_id,
            details={"conflict_type": conflict_type, "resolution": resolution}
        )
        await self.logger.log_event(event)
    
    async def get_full_status(self) -> Dict[str, Any]:
        """获取完整状态"""
        return {
            "state": self.state_tracker.state.value,
            "peer_states": {
                peer_id: state.value 
                for peer_id, state in (await self.state_tracker.get_all_peer_states()).items()
            },
            "metrics": await self.metrics_collector.get_metrics(),
            "running": self._running
        }
