"""
PAO System Integrator - 系统集成器

整合所有模块，确保协同工作：
- 设备发现与通信
- 技能管理
- 情境感知
- 学习循环
- 数据同步
- 记忆系统
"""

import asyncio
import logging
from typing import Optional, Dict, Any
from dataclasses import dataclass

from .core.config import ConfigManager, PAOConfig
from .core.device import DeviceRegistry, DeviceInfo
from .core.discovery import DeviceDiscoveryService
from .core.communication import Communication
from .core.sync import SyncEngine, SyncStatus
from .core.storage import StorageManager, StorageConfig as CoreStorageConfig
from .core.memory import MemorySystem
from .core.heartbeat import HeartbeatManager, HeartbeatConfig

from .skill_manager import SkillManager, SkillCategory, SkillLevel
from .context_awareness import ContextAwareness, ContextType
from .learning_loop import LearningLoop, FeedbackType

logger = logging.getLogger(__name__)


@dataclass
class SystemStatus:
    """系统状态"""
    initialized: bool = False
    device_id: Optional[str] = None
    connected_peers: int = 0
    skills_loaded: int = 0
    memory_items: int = 0
    sync_status: str = "idle"
    errors: list = None

    def __post_init__(self):
        if self.errors is None:
            self.errors = []


class PAOSystemIntegrator:
    """
    PAO系统集成器

    整合所有核心模块，提供统一的系统入口
    """

    def __init__(self, config_path: Optional[str] = None):
        self.config_manager = ConfigManager(config_path)
        self.config: PAOConfig = self.config_manager.config

        # 核心组件
        self.device_registry: Optional[DeviceRegistry] = None
        self.discovery_service: Optional[DeviceDiscoveryService] = None
        self.communication: Optional[Communication] = None
        self.sync_engine: Optional[SyncEngine] = None
        self.storage_manager: Optional[StorageManager] = None
        self.memory_system: Optional[MemorySystem] = None
        self.heartbeat_manager: Optional[HeartbeatManager] = None

        # 智能组件
        self.skill_manager: Optional[SkillManager] = None
        self.context_awareness: Optional[ContextAwareness] = None
        self.learning_loop: Optional[LearningLoop] = None

        # 系统状态
        self.status = SystemStatus()
        self._running = False

    async def initialize(self) -> bool:
        """
        初始化所有系统组件

        Returns:
            bool: 初始化是否成功
        """
        logger.info("🚀 初始化PAO系统...")

        try:
            # 1. 初始化设备注册表
            self.device_registry = DeviceRegistry()
            self.status.device_id = self.config.device_id

            # 2. 初始化存储管理器
            self.storage_manager = StorageManager(self.config.storage)
            await self.storage_manager.initialize()

            # 3. 初始化记忆系统
            self.memory_system = MemorySystem()
            await self.memory_system.load()
            self.status.memory_items = len(self.memory_system.memories)

            # 4. 初始化设备发现服务
            self.discovery_service = DeviceDiscoveryService(
                config=self.config,
                device_registry=self.device_registry,
                on_device_discovered=self._on_device_discovered,
                on_device_lost=self._on_device_lost
            )

            # 5. 初始化通信模块
            self.communication = Communication(
                device_id=self.config.device_id,
                config=self.config
            )

            # 6. 初始化同步引擎
            self.sync_engine = SyncEngine(
                memory_system=self.memory_system,
                local_device_id=self.config.device_id
            )

            # 7. 初始化技能管理器
            self.skill_manager = SkillManager()
            await self.skill_manager.initialize()
            self.status.skills_loaded = len(self.skill_manager.registry._skills)

            # 8. 初始化情境感知
            self.context_awareness = ContextAwareness()
            await self.context_awareness.register_default_scenes()

            # 9. 初始化学习循环
            self.learning_loop = LearningLoop()
            await self.learning_loop.start()

            # 10. 初始化心跳管理器
            self.heartbeat_manager = HeartbeatManager(
                device_id=self.config.device_id,
                config=HeartbeatConfig(
                    interval=30,      # 30秒心跳间隔
                    timeout=90,      # 90秒超时判定离线
                    check_interval=10  # 10秒检查间隔
                )
            )
            # 设置发送器（复用通信模块）
            self.heartbeat_manager.set_sender(self.communication)
            # 注册设备状态变化回调
            self.heartbeat_manager.register_callback(self._on_heartbeat_status_change)
            await self.heartbeat_manager.start()

            # 启动设备发现
            await self.discovery_service.start()

            self.status.initialized = True
            self._running = True

            logger.info("✅ PAO系统初始化完成")
            logger.info(f"   设备ID: {self.status.device_id}")
            logger.info(f"   技能数量: {self.status.skills_loaded}")
            logger.info(f"   记忆数量: {self.status.memory_items}")

            return True

        except Exception as e:
            logger.error(f"❌ 系统初始化失败: {e}")
            self.status.errors.append(str(e))
            return False

    async def start(self):
        """启动系统"""
        if not self.status.initialized:
            success = await self.initialize()
            if not success:
                raise RuntimeError("系统初始化失败")

        logger.info("▶️ 启动PAO系统服务...")

        # 启动设备发现
        if self.discovery_service:
            await self.discovery_service.start()

        # 启动同步引擎
        if self.sync_engine:
            await self.sync_engine.start()

        self._running = True
        logger.info("✅ PAO系统已启动")

    async def stop(self):
        """停止系统"""
        logger.info("⏹️ 停止PAO系统...")

        self._running = False

        # 停止各组件
        if self.heartbeat_manager:
            await self.heartbeat_manager.stop()

        if self.discovery_service:
            await self.discovery_service.stop()

        if self.sync_engine:
            await self.sync_engine.stop()

        if self.learning_loop:
            await self.learning_loop.stop()

        if self.storage_manager:
            await self.storage_manager.close()

        logger.info("✅ PAO系统已停止")

    # ==================== 事件回调 ====================

    def _on_device_discovered(self, device: DeviceInfo):
        """设备发现回调"""
        logger.info(f"📡 发现新设备: {device.name} ({device.device_id})")
        self.status.connected_peers = len(self.device_registry.list_devices())

    def _on_device_lost(self, device_id: str):
        """设备丢失回调"""
        logger.info(f"📡 设备丢失: {device_id}")
        self.status.connected_peers = len(self.device_registry.list_devices())

    def _on_sync_status_change(self, status: SyncStatus):
        """同步状态变化回调"""
        self.status.sync_status = status.value
        logger.debug(f"🔄 同步状态: {status.value}")

    def _on_heartbeat_status_change(self, device_id: str, old_status, new_status):
        """心跳状态变化回调"""
        from .core.heartbeat import HeartbeatStatus

        logger.info(f"💓 设备状态变化 [{device_id}]: {old_status.value} -> {new_status.value}")

        # 如果设备离线，从设备注册表移除
        if new_status == HeartbeatStatus.DEAD:
            logger.warning(f"⚠️ 设备离线 [{device_id}]，从注册表移除")
            self.device_registry.unregister_device(device_id)

        # 更新连接数
        self.status.connected_peers = len(self.device_registry.list_online_devices())

    # ==================== 技能管理 ====================

    async def search_skills(self, query: str) -> list:
        """搜索技能"""
        if not self.skill_manager:
            return []
        return await self.skill_manager.search_skills(query)

    async def apply_skill(self, skill_id: str, params: Dict[str, Any],
                       score: float, feedback: str) -> bool:
        """应用技能并评分"""
        if not self.skill_manager:
            return False

        # 应用技能
        result = await self.skill_manager.apply_skill(skill_id, params, score, feedback)

        # 提交学习反馈
        if self.learning_loop:
            await self.learning_loop.submit_feedback(
                FeedbackType.EXPLICIT,
                skill_id,
                params,
                score,
                feedback
            )

        return result

    async def get_skill_stats(self, skill_id: str) -> Dict[str, Any]:
        """获取技能统计"""
        if not self.skill_manager:
            return {}
        return await self.skill_manager.get_skill_stats(skill_id)

    # ==================== 情境感知 ====================

    async def get_current_context(self) -> Dict[str, Any]:
        """获取当前上下文"""
        if not self.context_awareness:
            return {}

        contexts = await self.context_awareness.collect_all()
        scene = await self.context_awareness.recognize_scene()

        return {
            "contexts": contexts,
            "scene": scene,
            "summary": await self.context_awareness.summarize_context()
        }

    # ==================== 记忆管理 ====================

    async def store_memory(self, memory_type: str, content: Any,
                          priority: int = 5) -> str:
        """存储记忆"""
        if not self.memory_system:
            return None

        memory_id = await self.memory_system.add_memory(
            memory_type=memory_type,
            content=content,
            priority=priority
        )
        self.status.memory_items = len(self.memory_system.memories)
        return memory_id

    async def retrieve_memories(self, query: str, limit: int = 10) -> list:
        """检索记忆"""
        if not self.memory_system:
            return []
        return await self.memory_system.search_memories(query, limit)

    # ==================== 同步管理 ====================

    async def sync_with_peer(self, peer_id: str) -> bool:
        """与指定对等节点同步"""
        if not self.sync_engine:
            return False

        try:
            await self.sync_engine.connect_peer(peer_id)
            await self.sync_engine.sync_now()
            return True
        except Exception as e:
            logger.error(f"同步失败: {e}")
            return False

    def get_sync_status(self) -> Dict[str, Any]:
        """获取同步状态"""
        if not self.sync_engine:
            return {"status": "unavailable"}

        status = self.sync_engine.get_status()
        return {
            "status": status.status.value if hasattr(status, 'status') else str(status),
            "connected_peers": status.connected_peers if hasattr(status, 'connected_peers') else 0,
            "pending_changes": status.pending_changes if hasattr(status, 'pending_changes') else 0
        }

    # ==================== 系统状态 ====================

    def get_system_status(self) -> SystemStatus:
        """获取系统状态"""
        self.status.connected_peers = len(self.device_registry.get_all_devices()) if self.device_registry else 0
        return self.status

    async def run_diagnostics(self) -> Dict[str, Any]:
        """运行系统诊断"""
        diagnostics = {
            "system": {
                "initialized": self.status.initialized,
                "running": self._running,
                "device_id": self.status.device_id
            },
            "components": {},
            "errors": self.status.errors
        }

        # 检查各组件
        components = [
            ("device_registry", self.device_registry),
            ("discovery_service", self.discovery_service),
            ("communication", self.communication),
            ("sync_engine", self.sync_engine),
            ("storage_manager", self.storage_manager),
            ("memory_system", self.memory_system),
            ("skill_manager", self.skill_manager),
            ("context_awareness", self.context_awareness),
            ("learning_loop", self.learning_loop)
        ]

        for name, component in components:
            diagnostics["components"][name] = {
                "available": component is not None,
                "status": "ok" if component else "unavailable"
            }

        return diagnostics


# ==================== 便捷函数 ====================

async def create_pao_system(config_path: Optional[str] = None) -> PAOSystemIntegrator:
    """创建并初始化PAO系统"""
    system = PAOSystemIntegrator(config_path)
    await system.initialize()
    return system
