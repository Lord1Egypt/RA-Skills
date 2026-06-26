"""
Context Awareness Module - 情境感知系统

提供上下文收集、场景识别、环境状态监测功能
"""

import asyncio
import time
import platform
import psutil
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum
from collections import defaultdict
import logging

logger = logging.getLogger(__name__)


class ContextType(Enum):
    """上下文类型"""
    DEVICE = "device"           # 设备信息
    TIME = "time"              # 时间信息
    LOCATION = "location"       # 位置信息
    ACTIVITY = "activity"       # 活动状态
    EMOTIONAL = "emotional"    # 情绪状态
    ENVIRONMENT = "environment" # 环境状态


@dataclass
class ContextData:
    """上下文数据"""
    context_type: ContextType
    data: Dict[str, Any]
    timestamp: float = field(default_factory=time.time)
    confidence: float = 1.0  # 置信度 0-1


@dataclass
class Scene:
    """场景"""
    scene_id: str
    name: str
    description: str
    context_requirements: Dict[ContextType, float]  # 需要的上下文类型和最低置信度
    metadata: Dict[str, Any] = field(default_factory=dict)


class DeviceContextCollector:
    """设备上下文收集器"""
    
    def __init__(self):
        self._device_info: Dict[str, Any] = {}
        self._system_info: Dict[str, Any] = {}
    
    async def collect(self) -> ContextData:
        """收集设备上下文"""
        try:
            # 基础设备信息
            self._device_info = {
                "platform": platform.system(),
                "platform_version": platform.version(),
                "machine": platform.machine(),
                "processor": platform.processor(),
            }
            
            # 系统资源
            self._system_info = {
                "cpu_percent": psutil.cpu_percent(interval=0.1),
                "memory_percent": psutil.virtual_memory().percent,
                "memory_available_mb": psutil.virtual_memory().available // (1024 * 1024),
                "disk_percent": psutil.disk_usage('/').percent,
            }
            
            # 电池状态（如果可用）
            try:
                battery = psutil.sensors_battery()
                if battery:
                    self._system_info["battery_percent"] = battery.percent
                    self._system_info["battery_charging"] = battery.power_plugged
            except Exception:
                pass
            
            return ContextData(
                context_type=ContextType.DEVICE,
                data={
                    "device": self._device_info,
                    "system": self._system_info
                }
            )
        except Exception as e:
            logger.error(f"设备上下文收集失败: {e}")
            return ContextData(
                context_type=ContextType.DEVICE,
                data={"error": str(e)}
            )
    
    async def get_device_id(self) -> str:
        """获取设备ID"""
        return f"{platform.node()}_{platform.machine()}"


class TimeContextCollector:
    """时间上下文收集器"""
    
    def __init__(self):
        self._last_update = 0
    
    async def collect(self) -> ContextData:
        """收集时间上下文"""
        now = time.time()
        local = time.localtime(now)
        
        # 计算时间段
        hour = local.tm_hour
        if 6 <= hour < 9:
            period = "morning"
        elif 9 <= hour < 12:
            period = "forenoon"
        elif 12 <= hour < 14:
            period = "noon"
        elif 14 <= hour < 18:
            period = "afternoon"
        elif 18 <= hour < 22:
            period = "evening"
        else:
            period = "night"
        
        # 计算星期
        weekdays = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
        weekday = weekdays[local.tm_wday]
        
        # 判断是否工作日
        is_workday = local.tm_wday < 5
        
        return ContextData(
            context_type=ContextType.TIME,
            data={
                "timestamp": now,
                "hour": hour,
                "minute": local.tm_min,
                "period": period,
                "weekday": weekday,
                "is_workday": is_workday,
                "date": time.strftime("%Y-%m-%d", local)
            }
        )


class ActivityContextCollector:
    """活动上下文收集器"""
    
    def __init__(self):
        self._current_activity: str = "idle"
        self._activity_history: List[Dict] = []
        self._focus_sessions: List[Dict] = []
    
    async def collect(self) -> ContextData:
        """收集活动上下文"""
        return ContextData(
            context_type=ContextType.ACTIVITY,
            data={
                "current_activity": self._current_activity,
                "recent_activities": self._activity_history[-5:],
                "focus_sessions_today": len(self._focus_sessions)
            }
        )
    
    async def set_activity(self, activity: str) -> None:
        """设置当前活动"""
        self._current_activity = activity
        self._activity_history.append({
            "activity": activity,
            "timestamp": time.time()
        })
        
        # 保持历史记录在合理范围
        if len(self._activity_history) > 100:
            self._activity_history = self._activity_history[-50:]
    
    async def start_focus_session(self) -> None:
        """开始专注会话"""
        self._focus_sessions.append({
            "start": time.time(),
            "end": None
        })
    
    async def end_focus_session(self) -> None:
        """结束专注会话"""
        if self._focus_sessions and self._focus_sessions[-1]["end"] is None:
            self._focus_sessions[-1]["end"] = time.time()


class EnvironmentContextCollector:
    """环境上下文收集器"""
    
    def __init__(self):
        self._network_status = "unknown"
        self._screen_status = "unknown"
    
    async def collect(self) -> ContextData:
        """收集环境上下文"""
        return ContextData(
            context_type=ContextType.ENVIRONMENT,
            data={
                "network_status": self._network_status,
                "screen_status": self._screen_status,
                "noise_level": "quiet"  # 简化版本
            }
        )
    
    async def set_network_status(self, status: str) -> None:
        """设置网络状态"""
        self._network_status = status
    
    async def set_screen_status(self, status: str) -> None:
        """设置屏幕状态"""
        self._screen_status = status


class SceneRecognizer:
    """场景识别器"""
    
    def __init__(self):
        self._scenes: Dict[str, Scene] = {}
        self._current_scene: Optional[str] = None
        self._context_history: List[ContextData] = []
    
    def register_scene(self, scene: Scene) -> None:
        """注册场景"""
        self._scenes[scene.scene_id] = scene
        logger.info(f"场景已注册: {scene.name}")
    
    async def recognize(self, contexts: List[ContextData]) -> Optional[str]:
        """识别当前场景"""
        best_match = None
        best_score = 0.0
        
        for scene_id, scene in self._scenes.items():
            score = self._calculate_scene_match(scene, contexts)
            if score > best_score and score >= 0.5:
                best_score = score
                best_match = scene_id
        
        if best_match != self._current_scene:
            old_scene = self._current_scene
            self._current_scene = best_match
            logger.info(f"场景切换: {old_scene} -> {best_match} (置信度: {best_score:.2f})")
        
        return self._current_scene
    
    def _calculate_scene_match(self, scene: Scene, contexts: List[ContextData]) -> float:
        """计算场景匹配度"""
        if not scene.context_requirements:
            return 0.0
        
        total_score = 0.0
        matched_count = 0
        
        for context in contexts:
            req_confidence = scene.context_requirements.get(context.context_type, 0)
            if req_confidence > 0 and context.confidence >= req_confidence:
                total_score += context.confidence
                matched_count += 1
        
        if not scene.context_requirements:
            return 0.0
        
        return total_score / len(scene.context_requirements) if matched_count > 0 else 0.0
    
    def get_current_scene(self) -> Optional[Scene]:
        """获取当前场景"""
        if self._current_scene:
            return self._scenes.get(self._current_scene)
        return None


class ContextAwareness:
    """情境感知系统（整合模块）"""
    
    def __init__(self):
        self.device_collector = DeviceContextCollector()
        self.time_collector = TimeContextCollector()
        self.activity_collector = ActivityContextCollector()
        self.environment_collector = EnvironmentContextCollector()
        self.scene_recognizer = SceneRecognizer()
        
        self._collectors = [
            self.device_collector,
            self.time_collector,
            self.activity_collector,
            self.environment_collector
        ]
        
        self._context_cache: List[ContextData] = []
        self._last_collection = 0
        self._collection_interval = 60  # 秒
    
    async def collect_all(self, force: bool = False) -> List[ContextData]:
        """收集所有上下文"""
        now = time.time()
        
        if not force and now - self._last_collection < self._collection_interval:
            return self._context_cache
        
        contexts = []
        for collector in self._collectors:
            try:
                context = await collector.collect()
                contexts.append(context)
            except Exception as e:
                logger.error(f"上下文收集失败: {collector.__class__.__name__}, {e}")
        
        self._context_cache = contexts
        self._last_collection = now
        
        return contexts
    
    async def recognize_scene(self) -> Optional[str]:
        """识别当前场景"""
        contexts = await self.collect_all()
        return await self.scene_recognizer.recognize(contexts)
    
    async def register_default_scenes(self) -> None:
        """注册默认场景"""
        default_scenes = [
            Scene(
                scene_id="work_morning",
                name="工作日上午",
                description="工作日上午专注工作",
                context_requirements={
                    ContextType.TIME: 0.8,
                    ContextType.ACTIVITY: 0.5
                }
            ),
            Scene(
                scene_id="work_afternoon",
                name="工作日下午",
                description="工作日下午继续工作",
                context_requirements={
                    ContextType.TIME: 0.8,
                    ContextType.ACTIVITY: 0.5
                }
            ),
            Scene(
                scene_id="coding",
                name="编程模式",
                description="专注于编程工作",
                context_requirements={
                    ContextType.DEVICE: 0.6,
                    ContextType.ACTIVITY: 0.7
                }
            ),
            Scene(
                scene_id="relaxed",
                name="休闲放松",
                description="非工作时间的休闲状态",
                context_requirements={
                    ContextType.TIME: 0.9,
                    ContextType.ENVIRONMENT: 0.3
                }
            ),
        ]
        
        for scene in default_scenes:
            self.scene_recognizer.register_scene(scene)
    
    async def summarize_context(self) -> Dict[str, Any]:
        """获取上下文摘要"""
        contexts = await self.collect_all()
        
        summary = {}
        for context in contexts:
            summary[context.context_type.value] = context.data
        
        current_scene = self.scene_recognizer.get_current_scene()
        if current_scene:
            summary["current_scene"] = {
                "name": current_scene.name,
                "description": current_scene.description
            }
        
        return summary
