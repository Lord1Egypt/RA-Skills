"""
Multi-Robot Skill 主接口

这是一个通用的多机器人协同控制接口，适用于各种 AI Agent 框架。
"""

import logging
from typing import Any, Dict, List, Optional, Callable

from .core.task_planner import TaskPlanner, Task, TaskPlan, TaskType
from .core.coordinator import Coordinator, ExecutionResult
from .core.state_manager import StateManager, SystemStatus
from .core.error_handler import ErrorHandler, ErrorConfig, ErrorStrategy
from .adapters.base import RobotAdapter, RobotCapability
from .adapters.vansbot_adapter import VansbotAdapter
from .adapters.puppypi_adapter import PuppyPiAdapter


logger = logging.getLogger(__name__)


class MultiRobotSkill:
    """
    多机器人协同控制 Skill

    这是主要的接口类，提供了简单易用的 API 来控制多个机器人协同工作。
    适用于各种 AI Agent 框架（Claude Code、OpenClaw 等）。

    示例:
        >>> skill = MultiRobotSkill()
        >>> skill.register_robot("vansbot", "http://192.168.3.113:5000")
        >>> skill.register_robot("dog1", "http://localhost:8000", robot_id=1)
        >>> result = skill.execute_task("让机械臂抓取0号物体")
    """

    def __init__(self, max_workers: int = 4, log_level: str = "INFO"):
        """
        初始化 Skill

        Args:
            max_workers: 最大并行工作线程数
            log_level: 日志级别
        """
        # 设置日志
        logging.basicConfig(
            level=getattr(logging, log_level),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

        # 初始化核心组件
        self.planner = TaskPlanner()
        self.coordinator = Coordinator(max_workers=max_workers)
        self.state_manager = StateManager()
        self.error_handler = ErrorHandler()

        # 机器人注册表
        self.robots: Dict[str, RobotAdapter] = {}

        logger.info("MultiRobotSkill 初始化完成")

    def register_adapter(self, adapter: RobotAdapter, auto_connect: bool = True) -> bool:
        """
        注册一个已实例化的适配器（供 Agent 动态生成适配器后注入）

        Args:
            adapter: 已实例化的 RobotAdapter 子类对象
            auto_connect: 是否自动调用 connect()

        Returns:
            bool: 注册是否成功

        示例:
            >>> class MyAdapter(RobotAdapter): ...
            >>> skill.register_adapter(MyAdapter("my_robot", "http://..."))
        """
        try:
            if auto_connect and not adapter.connect():
                logger.error(f"无法连接到机器人: {adapter.name}")
                return False

            self.robots[adapter.name] = adapter
            self.coordinator.register_robot(adapter)
            self.state_manager.register_robot(adapter)

            logger.info(f"成功注册适配器: {adapter.name} ({adapter.robot_type.value})")
            return True

        except Exception as e:
            logger.error(f"注册适配器失败: {adapter.name}, 错误: {e}")
            return False

    def register_robot(
        self,
        name: str,
        endpoint: str,
        robot_type: str = "auto",
        **config
    ) -> bool:
        """
        注册机器人（内置类型快捷方式）

        Args:
            name: 机器人名称（唯一标识）
            endpoint: 机器人端点（URL）
            robot_type: 机器人类型 ("vansbot", "puppypi", "auto")
            **config: 其他配置参数

        Returns:
            bool: 注册是否成功
        """
        try:
            if robot_type == "vansbot" or (robot_type == "auto" and "vansbot" in name.lower()):
                adapter = VansbotAdapter(name, endpoint, **config)
            elif robot_type == "puppypi" or (robot_type == "auto" and "dog" in name.lower()):
                robot_id = config.get("robot_id", 1)
                adapter = PuppyPiAdapter(name, endpoint, robot_id, **config)
            else:
                logger.error(f"未知的机器人类型: {robot_type}，请使用 register_adapter() 注入自定义适配器")
                return False

            return self.register_adapter(adapter)

        except Exception as e:
            logger.error(f"注册机器人失败: {name}, 错误: {e}")
            return False

    def unregister_robot(self, name: str):
        """注销机器人"""
        if name in self.robots:
            adapter = self.robots[name]
            adapter.disconnect()
            del self.robots[name]
            self.coordinator.unregister_robot(name)
            self.state_manager.unregister_robot(name)
            logger.info(f"注销机器人: {name}")

    def get_robot(self, name: str) -> Optional[RobotAdapter]:
        """获取机器人适配器"""
        return self.robots.get(name)

    def list_robots(self) -> List[str]:
        """列出所有已注册的机器人"""
        return list(self.robots.keys())

    def get_robot_capabilities(self, robot_name: str) -> List[RobotCapability]:
        """获取机器人能力列表"""
        robot = self.get_robot(robot_name)
        if robot:
            return robot.get_capabilities()
        return []

    def execute_plan(self, plan: TaskPlan) -> List[ExecutionResult]:
        """
        执行任务计划

        Args:
            plan: 任务计划

        Returns:
            List[ExecutionResult]: 执行结果列表

        示例:
            >>> plan = skill.create_plan("测试计划")
            >>> task = skill.create_task("vansbot", "detect_objects")
            >>> plan.add_task(task)
            >>> results = skill.execute_plan(plan)
        """
        # 验证计划
        valid, error_msg = self.planner.validate_plan(plan)
        if not valid:
            logger.error(f"任务计划验证失败: {error_msg}")
            raise ValueError(f"任务计划无效: {error_msg}")

        # 更新系统状态
        self.state_manager.set_system_status(SystemStatus.RUNNING)

        try:
            # 执行计划
            results = self.coordinator.execute_plan(plan)

            # 更新系统状态
            self.state_manager.set_system_status(SystemStatus.IDLE)

            return results

        except Exception as e:
            self.state_manager.set_system_status(SystemStatus.ERROR)
            logger.error(f"执行任务计划失败: {e}")
            raise

    def create_plan(self, name: str, description: str = "") -> TaskPlan:
        """
        创建任务计划

        Args:
            name: 计划名称
            description: 计划描述

        Returns:
            TaskPlan: 任务计划对象
        """
        return self.planner.create_plan(name, description)

    def create_task(
        self,
        robot: str,
        action: str,
        params: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> Task:
        """
        创建任务

        Args:
            robot: 机器人名称
            action: 动作名称
            params: 动作参数
            **kwargs: 其他任务参数（name, description, depends_on, timeout等）

        Returns:
            Task: 任务对象
        """
        return self.planner.create_atomic_task(
            robot=robot,
            action=action,
            params=params,
            **kwargs
        )

    def create_parallel_tasks(self, tasks: List[Task], **kwargs) -> Task:
        """创建并行任务"""
        return self.planner.create_parallel_task(tasks, **kwargs)

    def create_sequential_tasks(self, tasks: List[Task], **kwargs) -> Task:
        """创建顺序任务"""
        return self.planner.create_sequential_task(tasks, **kwargs)

    def get_status(self) -> Dict[str, Any]:
        """
        获取系统状态

        Returns:
            Dict: 系统状态信息
        """
        return self.state_manager.to_dict()

    def on_event(self, event_name: str, callback: Callable):
        """
        注册事件回调

        支持的事件:
        - plan_started: 计划开始执行
        - plan_completed: 计划执行完成
        - plan_failed: 计划执行失败
        - task_started: 任务开始执行
        - task_completed: 任务执行完成
        - task_failed: 任务执行失败
        - task_error: 任务执行异常

        Args:
            event_name: 事件名称
            callback: 回调函数

        示例:
            >>> skill.on_event("task_completed", lambda e: print(f"任务完成: {e}"))
        """
        self.coordinator.on_event(event_name, callback)

    def configure_error_handling(self, config: Dict[str, Any]):
        """
        配置错误处理

        Args:
            config: 错误处理配置
                - max_retries: 最大重试次数
                - retry_delay: 重试延迟（秒）
                - timeout: 超时时间（秒）
                - default_strategy: 默认策略 ("retry", "skip", "abort", "rollback", "continue")

        示例:
            >>> skill.configure_error_handling({
            ...     "max_retries": 3,
            ...     "retry_delay": 1.0,
            ...     "default_strategy": "retry"
            ... })
        """
        error_config = ErrorConfig(
            max_retries=config.get("max_retries", 3),
            retry_delay=config.get("retry_delay", 1.0),
            timeout=config.get("timeout", 60.0),
            default_strategy=ErrorStrategy(config.get("default_strategy", "retry"))
        )
        self.error_handler = ErrorHandler(error_config)

    def start_monitoring(self, interval: float = 1.0):
        """
        启动状态监控

        Args:
            interval: 监控间隔（秒）
        """
        self.state_manager.start_monitoring(interval)

    def stop_monitoring(self):
        """停止状态监控"""
        self.state_manager.stop_monitoring()

    def shutdown(self):
        """关闭 Skill"""
        logger.info("关闭 MultiRobotSkill")

        # 停止监控
        self.stop_monitoring()

        # 断开所有机器人
        for name in list(self.robots.keys()):
            self.unregister_robot(name)

        # 关闭协调器
        self.coordinator.shutdown()

    def __enter__(self):
        """上下文管理器入口"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器出口"""
        self.shutdown()
