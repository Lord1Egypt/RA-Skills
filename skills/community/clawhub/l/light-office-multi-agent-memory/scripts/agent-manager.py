#!/usr/bin/env python3
"""
多Agent记忆系统 - 动态Agent管理脚本（通用版）

功能：
  支持Agent自动增加和减少：
  1. Agent注册/注销
  2. 动态发现Agent
  3. Agent状态监控
  4. 自动调整记忆分配

作者：光光教授 (光光事务所)
版本：v1.0.0
许可证：MIT
"""

import os
import sys
import json
import time
import hashlib
from pathlib import Path
from datetime import datetime, timedelta

# ============================================================
# 配置
# ============================================================

WORKSPACE = Path(os.environ.get("MEMORY_WORKSPACE", "/tmp/memory-workspace"))
AGENT_DIR = WORKSPACE / "agents"
CONFIG_DIR = WORKSPACE / "config"

# Agent配置
AGENT_CONFIG = {
    "auto_discover": True,          # 自动发现Agent
    "health_check_interval": 300,   # 健康检查间隔（秒）
    "max_agents": 100,              # 最大Agent数量
    "memory_per_agent": 1024,       # 每个Agent默认记忆大小（KB）
    "auto_scale": True,             # 自动扩展
    "scale_threshold": 0.8          # 扩展阈值（80%）
}

# ============================================================
# Agent注册表
# ============================================================

class AgentRegistry:
    """Agent注册表"""
    
    def __init__(self):
        self.agent_dir = AGENT_DIR
        self.agent_dir.mkdir(parents=True, exist_ok=True)
        self.registry_file = self.agent_dir / "registry.json"
        
        # 加载或创建注册表
        if self.registry_file.exists():
            with open(self.registry_file, "r", encoding="utf-8") as f:
                self.registry = json.load(f)
        else:
            self.registry = {
                "agents": {},
                "metadata": {
                    "created": datetime.now().isoformat(),
                    "updated": datetime.now().isoformat(),
                    "version": "1.0"
                }
            }
    
    def register_agent(self, agent_id, agent_config=None):
        """注册Agent"""
        print(f"[Registry] 注册Agent: {agent_id}")
        
        if agent_id in self.registry["agents"]:
            print(f"[WARN] Agent已存在: {agent_id}")
            return False
        
        # 创建Agent配置
        if agent_config is None:
            agent_config = {
                "id": agent_id,
                "name": f"Agent-{agent_id}",
                "status": "active",
                "registered_at": datetime.now().isoformat(),
                "last_heartbeat": datetime.now().isoformat(),
                "memory_size": AGENT_CONFIG["memory_per_agent"],
                "hooks_enabled": True,
                "rrf_enabled": True,
                "graph_enabled": True
            }
        
        self.registry["agents"][agent_id] = agent_config
        self.registry["metadata"]["updated"] = datetime.now().isoformat()
        
        # 创建Agent目录
        agent_path = self.agent_dir / agent_id
        agent_path.mkdir(parents=True, exist_ok=True)
        
        # 保存注册表
        with open(self.registry_file, "w", encoding="utf-8") as f:
            json.dump(self.registry, f, ensure_ascii=False, indent=2)
        
        print(f"[Registry] Agent注册成功: {agent_id}")
        return True
    
    def unregister_agent(self, agent_id):
        """注销Agent"""
        print(f"[Registry] 注销Agent: {agent_id}")
        
        if agent_id not in self.registry["agents"]:
            print(f"[WARN] Agent不存在: {agent_id}")
            return False
        
        # 更新状态
        self.registry["agents"][agent_id]["status"] = "inactive"
        self.registry["agents"][agent_id]["unregistered_at"] = datetime.now().isoformat()
        self.registry["metadata"]["updated"] = datetime.now().isoformat()
        
        # 保存注册表
        with open(self.registry_file, "w", encoding="utf-8") as f:
            json.dump(self.registry, f, ensure_ascii=False, indent=2)
        
        print(f"[Registry] Agent注销成功: {agent_id}")
        return True
    
    def get_agent(self, agent_id):
        """获取Agent配置"""
        return self.registry["agents"].get(agent_id)
    
    def list_agents(self, status="active"):
        """列出Agent"""
        agents = []
        for agent_id, config in self.registry["agents"].items():
            if config["status"] == status:
                agents.append(config)
        return agents
    
    def get_stats(self):
        """获取注册表统计"""
        total = len(self.registry["agents"])
        active = sum(1 for a in self.registry["agents"].values() if a["status"] == "active")
        inactive = sum(1 for a in self.registry["agents"].values() if a["status"] == "inactive")
        
        return {
            "total": total,
            "active": active,
            "inactive": inactive,
            "max_agents": AGENT_CONFIG["max_agents"],
            "utilization": active / AGENT_CONFIG["max_agents"] if AGENT_CONFIG["max_agents"] > 0 else 0
        }


# ============================================================
# 动态Agent发现
# ============================================================

class AgentDiscoverer:
    """Agent发现器"""
    
    def __init__(self):
        self.registry = AgentRegistry()
    
    def discover_agents(self):
        """发现Agent"""
        print(f"[Discoverer] 发现Agent...")
        
        discovered = 0
        
        # 扫描Agent目录
        for agent_path in self.registry.agent_dir.iterdir():
            if agent_path.is_dir() and agent_path.name != "registry.json":
                agent_id = agent_path.name
                
                # 检查Agent是否已注册
                if self.registry.get_agent(agent_id) is None:
                    # 自动注册
                    self.registry.register_agent(agent_id)
                    discovered += 1
        
        print(f"[Discoverer] 发现 {discovered} 个新Agent")
        return discovered


# ============================================================
# Agent健康检查
# ============================================================

class AgentHealthChecker:
    """Agent健康检查器"""
    
    def __init__(self):
        self.registry = AgentRegistry()
    
    def check_health(self, agent_id):
        """检查Agent健康"""
        agent = self.registry.get_agent(agent_id)
        if agent is None:
            return False
        
        # 检查心跳
        last_heartbeat = datetime.fromisoformat(agent["last_heartbeat"])
        now = datetime.now()
        
        if (now - last_heartbeat).total_seconds() > AGENT_CONFIG["health_check_interval"]:
            print(f"[HealthChecker] Agent心跳超时: {agent_id}")
            agent["status"] = "unhealthy"
            return False
        
        return True
    
    def check_all(self):
        """检查所有Agent健康"""
        print(f"[HealthChecker] 检查所有Agent健康...")
        
        healthy = 0
        unhealthy = 0
        
        for agent_id, config in self.registry.registry["agents"].items():
            if self.check_health(agent_id):
                healthy += 1
            else:
                unhealthy += 1
        
        print(f"[HealthChecker] 健康: {healthy}, 不健康: {unhealthy}")
        return {"healthy": healthy, "unhealthy": unhealthy}


# ============================================================
# 自动扩展
# ============================================================

class AutoScaler:
    """自动扩展器"""
    
    def __init__(self):
        self.registry = AgentRegistry()
    
    def check_scale(self):
        """检查是否需要扩展"""
        stats = self.registry.get_stats()
        utilization = stats["utilization"]
        
        print(f"[AutoScaler] 利用率: {utilization:.2%}")
        
        if utilization > AGENT_CONFIG["scale_threshold"]:
            print(f"[AutoScaler] 需要扩展！利用率 {utilization:.2%} > 阈值 {AGENT_CONFIG['scale_threshold']:.2%}")
            return True
        
        return False
    
    def scale_up(self, count=1):
        """扩展"""
        print(f"[AutoScaler] 扩展 {count} 个Agent...")
        
        registered = 0
        for i in range(count):
            agent_id = f"auto-agent-{datetime.now().strftime('%Y%m%d%H%M%S')}-{i}"
            if self.registry.register_agent(agent_id):
                registered += 1
        
        print(f"[AutoScaler] 扩展成功: {registered}/{count}")
        return registered
    
    def scale_down(self, count=1):
        """收缩"""
        print(f"[AutoScaler] 收缩 {count} 个Agent...")
        
        agents = self.registry.list_agents(status="active")
        unregistered = 0
        
        for agent in agents[:count]:
            if self.registry.unregister_agent(agent["id"]):
                unregistered += 1
        
        print(f"[AutoScaler] 收缩成功: {unregistered}/{count}")
        return unregistered


# ============================================================
# 主函数
# ============================================================

def main():
    """主函数"""
    print("=" * 60)
    print("多Agent记忆系统 - 动态Agent管理测试")
    print("=" * 60)
    
    # 1. 注册Agent
    print("\n[测试1] 注册Agent")
    registry = AgentRegistry()
    registry.register_agent("agent-001")
    registry.register_agent("agent-002")
    registry.register_agent("agent-003")
    
    # 2. 列出Agent
    print("\n[测试2] 列出Agent")
    agents = registry.list_agents()
    print(f"  活跃Agent: {len(agents)}")
    for agent in agents:
        print(f"  - {agent['id']}: {agent['name']}")
    
    # 3. 获取统计
    print("\n[测试3] 获取统计")
    stats = registry.get_stats()
    print(f"  总Agent: {stats['total']}")
    print(f"  活跃Agent: {stats['active']}")
    print(f"  不活跃Agent: {stats['inactive']}")
    print(f"  利用率: {stats['utilization']:.2%}")
    
    # 4. 发现Agent
    print("\n[测试4] 发现Agent")
    discoverer = AgentDiscoverer()
    discovered = discoverer.discover_agents()
    print(f"  发现: {discovered}")
    
    # 5. 健康检查
    print("\n[测试5] 健康检查")
    health_checker = AgentHealthChecker()
    health = health_checker.check_all()
    print(f"  健康: {health['healthy']}")
    print(f"  不健康: {health['unhealthy']}")
    
    # 6. 自动扩展
    print("\n[测试6] 自动扩展")
    scaler = AutoScaler()
    need_scale = scaler.check_scale()
    print(f"  需要扩展: {need_scale}")
    
    if need_scale:
        scaler.scale_up(2)
    
    # 7. 注销Agent
    print("\n[测试7] 注销Agent")
    registry.unregister_agent("agent-003")
    
    # 8. 最终统计
    print("\n[测试8] 最终统计")
    stats = registry.get_stats()
    print(f"  总Agent: {stats['total']}")
    print(f"  活跃Agent: {stats['active']}")
    print(f"  不活跃Agent: {stats['inactive']}")
    print(f"  利用率: {stats['utilization']:.2%}")
    
    print("\n✅ 动态Agent管理测试完成")


if __name__ == "__main__":
    main()
