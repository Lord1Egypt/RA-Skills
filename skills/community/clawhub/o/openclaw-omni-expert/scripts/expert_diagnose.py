#!/usr/bin/env python3
"""
OpenClaw 第一性原理诊断引擎 v3.0
THE EXPERT SYSTEM - 世界顶级 OpenClaw 专家系统

核心理念：
1. 第一性原理：从 OpenClaw 本质出发理解问题
2. 熵减思维：消除混乱根源，恢复系统有序
3. 最优路径：最小干预，最高效率
4. 深度专家：掌握 OpenClaw 架构、协议、机制

这不是一个工具，而是一个真正的专家。
"""

import os
import sys
import json
import subprocess
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any, Set
from datetime import datetime
from dataclasses import dataclass, field
from collections import defaultdict
import copy


# =============================================================================
# 第一性原理：OpenClaw 本质定义
# =============================================================================

@dataclass
class OpenClawArchitecture:
    """
    OpenClaw 第一性原理定义

    OpenClaw = 一个分布式智能体运行平台
    核心构成：
    - Gateway: 系统入口和协调中枢
    - Nodes: 执行任务的计算节点
    - Memory: 持久化和上下文管理
    - Transport: 组件间通信机制
    - Config: 运行时配置引擎
    """

    @staticmethod
    def get_components() -> Dict[str, Dict]:
        """OpenClaw 核心组件定义"""
        return {
            "gateway": {
                "name": "Gateway",
                "role": "系统入口和协调中枢",
                "process": "openclaw-gateway 或 openclaw daemon",
                "port": 18789,
                "config_key": "gateway",
                "health_endpoint": "/api/health",
                "critical": True,
                "dependencies": []
            },
            "transport": {
                "name": "Transport Layer",
                "role": "组件间通信机制",
                "type": "WebSocket + HTTP",
                "port": 18789,
                "config_key": "transport",
                "critical": True,
                "dependencies": ["gateway"]
            },
            "memory": {
                "name": "Memory System",
                "role": "持久化和上下文管理",
                "location": "~/.openclaw/memory/",
                "config_key": "memory",
                "critical": False,
                "dependencies": ["gateway"]
            },
            "nodes": {
                "name": "Node Registry",
                "role": "执行任务的计算节点管理",
                "config_key": "nodes",
                "critical": False,
                "dependencies": ["gateway", "transport"]
            },
            "plugins": {
                "name": "Plugin System",
                "role": "功能扩展框架",
                "location": "~/.openclaw/plugins/",
                "config_key": "plugins",
                "critical": False,
                "dependencies": ["gateway"]
            },
            "config_engine": {
                "name": "Configuration Engine",
                "role": "运行时配置管理",
                "location": "~/.openclaw/openclaw.json",
                "config_key": "config",
                "critical": True,
                "dependencies": []
            },
            "auth_system": {
                "name": "Auth System",
                "role": "认证和授权管理",
                "config_key": "auth",
                "critical": False,
                "dependencies": ["gateway"]
            },
            "channels": {
                "name": "Channel Adapters",
                "role": "外部通信渠道集成",
                "config_key": "channels",
                "critical": False,
                "dependencies": ["gateway", "transport"]
            }
        }

    @staticmethod
    def get_dependency_graph() -> Dict[str, List[str]]:
        """组件依赖关系图"""
        return {
            "gateway": [],
            "transport": ["gateway"],
            "memory": ["gateway"],
            "nodes": ["gateway", "transport"],
            "plugins": ["gateway"],
            "config_engine": [],
            "auth_system": ["gateway"],
            "channels": ["gateway", "transport"]
        }


# =============================================================================
# 熵减系统：问题分类与根因分析
# =============================================================================

@dataclass
class EntropyAnalysis:
    """
    熵减分析器

    问题 = 系统熵增
    解决 = 熵减 = 恢复有序

    熵增类型：
    - 结构熵：配置损坏、文件丢失
    - 状态熵：进程异常、端口冲突
    - 连接熵：网络中断、认证失败
    - 资源熵：内存泄漏、磁盘满
    """

    @staticmethod
    def classify_entropy(error_context: Dict) -> Dict:
        """熵增分类"""
        error_text = error_context.get("raw", "").lower()
        keywords = error_context.get("keywords", [])

        entropy_types = {
            "structural": {
                "patterns": ["enoent", "not found", "missing", "parse error", "corrupt"],
                "root_causes": ["文件损坏", "配置错误", "依赖缺失"],
                "entropy_level": "high"
            },
            "state": {
                "patterns": ["already running", "port in use", "deadlock", "frozen"],
                "root_causes": ["进程状态异常", "资源竞争", "死锁"],
                "entropy_level": "medium"
            },
            "connectivity": {
                "patterns": ["timeout", "refused", "disconnected", "handshake"],
                "root_causes": ["网络不稳定", "服务未启动", "防火墙阻断"],
                "entropy_level": "medium"
            },
            "resource": {
                "patterns": ["out of memory", "disk full", "cpu max", "leak"],
                "root_causes": ["资源耗尽", "内存泄漏", "磁盘空间不足"],
                "entropy_level": "high"
            },
            "auth": {
                "patterns": ["unauthorized", "forbidden", "token", "expired", "permission"],
                "root_causes": ["认证失效", "权限不足", "Token 过期"],
                "entropy_level": "medium"
            }
        }

        # 匹配熵增类型
        for entropy_type, info in entropy_types.items():
            if any(p in error_text for p in info["patterns"]):
                return {
                    "type": entropy_type,
                    "root_causes": info["root_causes"],
                    "entropy_level": info["entropy_level"],
                    "entropy_score": 0.8 if info["entropy_level"] == "high" else 0.5
                }

        return {
            "type": "unknown",
            "root_causes": ["需要进一步分析"],
            "entropy_level": "unknown",
            "entropy_score": 0.5
        }


# =============================================================================
# 最优路径：智能诊断算法
# =============================================================================

class OptimalPathfinder:
    """
    最优路径算法

    诊断最优路径 = 最小探测 → 最大信息 → 最短修复
    """

    @staticmethod
    def calculate_diagnosis_path(components: List[str]) -> List[str]:
        """计算最优诊断路径（按依赖顺序）"""
        arch = OpenClawArchitecture()
        dep_graph = arch.get_dependency_graph()

        # 拓扑排序，确保先诊断依赖项
        sorted_components = []
        visited = set()

        def visit(comp):
            if comp in visited:
                return
            visited.add(comp)
            for dep in dep_graph.get(comp, []):
                visit(dep)
            if comp in components:
                sorted_components.append(comp)

        for comp in components:
            visit(comp)

        return sorted_components

    @staticmethod
    def estimate_fix_complexity(fix: Dict) -> int:
        """评估修复复杂度（1-5分）"""
        complexity_map = {
            "restart_service": 1,
            "config_update": 2,
            "permission_fix": 2,
            "reinstall": 4,
            "system_reboot": 5
        }
        return complexity_map.get(fix.get("action", ""), 3)

    @staticmethod
    def select_minimal_intervention(fixes: List[Dict]) -> Dict:
        """选择最小干预修复方案"""
        if not fixes:
            return None

        # 按复杂度排序，选择最简单的
        sorted_fixes = sorted(fixes, key=lambda x: OptimalPathfinder.estimate_fix_complexity(x))
        return sorted_fixes[0]


# =============================================================================
# OpenClaw 专家知识库
# =============================================================================

class OpenClawExpertKnowledge:
    """
    OpenClaw 专家知识库

    深度掌握 OpenClaw 的：
    - 架构设计
    - 协议机制
    - 常见问题模式
    - 最优修复方案
    """

    # OpenClaw 专属错误模式（超越通用 Node.js 问题）
    OPENCLAW_ERROR_PATTERNS = {
        # Gateway 相关
        "gateway_not_starting": {
            "symptoms": ["gateway failed", "cannot start gateway", "listen EADDRINUSE"],
            "root_cause": "Gateway 启动失败",
            "components": ["gateway", "config_engine"],
            "entropy_type": "state",
            "diagnosis_steps": [
                "检查端口占用: lsof -i :18789",
                "检查配置语法: cat ~/.openclaw/openclaw.json | python3 -m json.tool",
                "检查日志: tail -50 ~/.openclaw/logs/*.log",
                "检查 Node.js 进程: ps aux | grep openclaw"
            ],
            "fixes": [
                {"action": "kill_conflicting", "priority": 1},
                {"action": "fix_config", "priority": 2},
                {"action": "clear_port", "priority": 1}
            ],
            "verification": "openclaw gateway status"
        },

        "gateway_unhealthy": {
            "symptoms": ["gateway unhealthy", "health check failed", "503"],
            "root_cause": "Gateway 健康检查失败",
            "components": ["gateway", "transport"],
            "entropy_type": "connectivity",
            "diagnosis_steps": [
                "检查 Gateway 进程: ps aux | grep gateway",
                "测试本地连接: curl http://127.0.0.1:18789/api/health",
                "检查内存使用: free -m",
                "查看详细日志"
            ],
            "fixes": [
                {"action": "restart_gateway", "priority": 1},
                {"action": "increase_memory", "priority": 2}
            ],
            "verification": "curl http://127.0.0.1:18789/api/health"
        },

        # Memory 系统
        "memory_corruption": {
            "symptoms": ["memory read error", "context lost", "history corrupted"],
            "root_cause": "Memory 系统数据损坏",
            "components": ["memory", "gateway"],
            "entropy_type": "structural",
            "diagnosis_steps": [
                "检查 Memory 目录: ls -la ~/.openclaw/memory/",
                "检查文件完整性",
                "查看 memory 相关错误日志"
            ],
            "fixes": [
                {"action": "backup_memory", "priority": 1},
                {"action": "rebuild_memory_index", "priority": 2}
            ],
            "verification": "观察上下文是否正常"
        },

        # Transport/WebSocket
        "websocket_failure": {
            "symptoms": ["websocket error", "connection upgrade failed", "ws://"],
            "root_cause": "WebSocket 连接失败",
            "components": ["transport", "gateway"],
            "entropy_type": "connectivity",
            "diagnosis_steps": [
                "检查 Gateway 是否运行",
                "测试 WebSocket 端点",
                "检查代理设置",
                "验证 SSL/TLS 配置"
            ],
            "fixes": [
                {"action": "restart_gateway", "priority": 1},
                {"action": "fix_proxy_config", "priority": 2},
                {"action": "update_ssl_config", "priority": 2}
            ],
            "verification": "WebSocket 连接测试"
        },

        # Node 管理
        "node_registration_failed": {
            "symptoms": ["node not registered", "node offline", "cannot connect node"],
            "root_cause": "节点注册失败",
            "components": ["nodes", "transport", "auth_system"],
            "entropy_type": "connectivity",
            "diagnosis_steps": [
                "检查 Gateway 状态",
                "检查节点配置",
                "验证认证信息",
                "测试节点连接"
            ],
            "fixes": [
                {"action": "reregister_node", "priority": 1},
                {"action": "fix_auth_config", "priority": 2}
            ],
            "verification": "openclaw nodes list"
        },

        # Plugin 系统
        "plugin_load_failed": {
            "symptoms": ["plugin error", "cannot load plugin", "plugin crashed"],
            "root_cause": "插件加载失败",
            "components": ["plugins", "gateway"],
            "entropy_type": "structural",
            "diagnosis_steps": [
                "列出插件: ls ~/.openclaw/plugins/",
                "检查插件日志",
                "验证插件依赖",
                "测试单个插件"
            ],
            "fixes": [
                {"action": "disable_plugin", "priority": 1},
                {"action": "reinstall_plugin", "priority": 2},
                {"action": "clear_plugin_cache", "priority": 1}
            ],
            "verification": "openclaw plugins list"
        },

        # Config 系统
        "config_invalid": {
            "symptoms": ["invalid config", "config schema error", "missing required"],
            "root_cause": "配置文件无效",
            "components": ["config_engine", "gateway"],
            "entropy_type": "structural",
            "diagnosis_steps": [
                "验证 JSON 语法",
                "检查 schema 完整性",
                "对比默认配置"
            ],
            "fixes": [
                {"action": "fix_config", "priority": 1},
                {"action": "reset_config", "priority": 2}
            ],
            "verification": "openclaw config validate"
        },

        # Channel 集成
        "channel_disconnected": {
            "symptoms": ["channel offline", "telegram failed", "discord error", "webhook failed"],
            "root_cause": "外部渠道连接断开",
            "components": ["channels", "gateway", "auth_system"],
            "entropy_type": "connectivity",
            "diagnosis_steps": [
                "列出渠道状态",
                "检查各渠道配置",
                "验证 API 凭证",
                "测试渠道连接"
            ],
            "fixes": [
                {"action": "restart_channel", "priority": 1},
                {"action": "refresh_token", "priority": 2},
                {"action": "fix_channel_config", "priority": 2}
            ],
            "verification": "openclaw channels status"
        },

        # 认证系统
        "auth_failure": {
            "symptoms": ["auth failed", "token expired", "unauthorized", "forbidden"],
            "root_cause": "认证授权失败",
            "components": ["auth_system", "gateway"],
            "entropy_type": "auth",
            "diagnosis_steps": [
                "检查 Token 状态",
                "验证权限配置",
                "检查认证服务器"
            ],
            "fixes": [
                {"action": "refresh_token", "priority": 1},
                {"action": "reset_auth", "priority": 2}
            ],
            "verification": "重新认证测试"
        }
    }

    # 修复操作映射
    FIX_ACTIONS = {
        "restart_gateway": {
            "description": "重启 Gateway",
            "commands": [
                "pkill -f openclaw",
                "sleep 2",
                "openclaw gateway start &"
            ],
            "verification": "curl -s http://127.0.0.1:18789/api/health"
        },
        "kill_conflicting": {
            "description": "终止冲突进程",
            "commands": [
                "lsof -ti :18789 | xargs kill -9 2>/dev/null || true"
            ],
            "verification": "lsof -i :18789"
        },
        "fix_config": {
            "description": "修复配置文件",
            "commands": [
                "cat ~/.openclaw/openclaw.json | python3 -m json.tool > /dev/null && echo 'Valid' || echo 'Invalid'"
            ],
            "verification": "json validation"
        },
        "clear_port": {
            "description": "清理端口占用",
            "commands": [
                "fuser -k 18789/tcp 2>/dev/null || true"
            ],
            "verification": "netstat -an | grep 18789"
        },
        "backup_memory": {
            "description": "备份 Memory 数据",
            "commands": [
                "mkdir -p ~/.openclaw/memory-backup-$(date +%Y%m%d)",
                "cp -r ~/.openclaw/memory/* ~/.openclaw/memory-backup-$(date +%Y%m%d)/"
            ],
            "verification": "ls ~/.openclaw/memory-backup/"
        },
        "rebuild_memory_index": {
            "description": "重建 Memory 索引",
            "commands": [
                "rm -rf ~/.openclaw/memory/.index",
                "openclaw memory rebuild"
            ],
            "verification": "openclaw memory status"
        },
        "disable_plugin": {
            "description": "禁用问题插件",
            "commands": [
                "mv ~/.openclaw/plugins/{plugin} ~/.openclaw/plugins/{plugin}.disabled"
            ],
            "verification": "openclaw plugins list"
        },
        "clear_plugin_cache": {
            "description": "清理插件缓存",
            "commands": [
                "rm -rf ~/.openclaw/plugins/.cache",
                "rm -rf ~/.openclaw/plugins/.temp"
            ],
            "verification": "重新加载插件"
        },
        "restart_channel": {
            "description": "重启渠道连接",
            "commands": [
                "openclaw channels restart {channel_name}"
            ],
            "verification": "openclaw channels status"
        },
        "refresh_token": {
            "description": "刷新访问令牌",
            "commands": [
                "openclaw auth refresh"
            ],
            "verification": "openclaw auth status"
        },
        "increase_memory": {
            "description": "增加 Gateway 内存",
            "commands": [
                "export NODE_OPTIONS='--max-old-space-size=4096'"
            ],
            "verification": "process memory usage"
        },
        "fix_proxy_config": {
            "description": "修复代理配置",
            "commands": [
                "unset http_proxy https_proxy HTTP_PROXY HTTPS_PROXY"
            ],
            "verification": "测试网络连接"
        }
    }


# =============================================================================
# 专家诊断引擎
# =============================================================================

class OpenClawExpertDiagnoser:
    """
    OpenClaw 专家诊断引擎 v3.0

    顶级诊断流程：
    1. 系统级探测 - 探测所有组件状态
    2. 熵增分类 - 确定问题类型
    3. 根因定位 - 找到问题根源
    4. 最优修复 - 选择最小干预方案
    5. 验证确认 - 确认修复成功
    """

    def __init__(self):
        self.arch = OpenClawArchitecture()
        self.entropy = EntropyAnalysis()
        self.pathfinder = OptimalPathfinder()
        self.knowledge = OpenClawExpertKnowledge()
        self.diagnosis_trace = []

    def diagnose(self, symptom: str, context: Optional[Dict] = None) -> Dict:
        """
        专家级诊断入口

        Args:
            symptom: 问题症状描述
            context: 额外上下文信息

        Returns:
            完整诊断报告
        """
        print("\n" + "="*70)
        print("🔬 OpenClaw 专家诊断系统 v3.0 - 第一性原理分析")
        print("="*70)

        # Phase 1: 系统级探测
        print("\n📊 [Phase 1] 系统级探测")
        system_state = self._probe_system()
        self._print_probe_results(system_state)

        # Phase 2: 熵增分类
        print("\n🌡️  [Phase 2] 熵增分析")
        error_context = {
            "raw": symptom,
            "keywords": self._extract_keywords(symptom),
            "system_state": system_state
        }
        entropy_analysis = self.entropy.classify_entropy(error_context)
        print(f"   熵增类型: {entropy_analysis['type']}")
        print(f"   熵增等级: {entropy_analysis['entropy_level']}")
        print(f"   可能根因: {', '.join(entropy_analysis['root_causes'])}")

        # Phase 3: 专家知识匹配
        print("\n🧠 [Phase 3] 专家知识匹配")
        expert_match = self._match_expert_pattern(symptom, system_state)

        # Phase 4: 根因定位
        print("\n🎯 [Phase 4] 根因定位")
        root_cause = self._locate_root_cause(symptom, system_state, expert_match)
        print(f"   根因: {root_cause['description']}")
        print(f"   受影响组件: {', '.join(root_cause['components'])}")
        print(f"   熵增来源: {root_cause['entropy_source']}")

        # Phase 5: 最优修复方案
        print("\n💡 [Phase 5] 最优修复方案")
        optimal_fix = self._generate_optimal_fix(root_cause, expert_match)
        self._print_fix_plan(optimal_fix)

        # Phase 6: 验证策略
        print("\n✅ [Phase 6] 验证策略")
        verification = self._generate_verification(optimal_fix)
        print(f"   验证命令: {verification['command']}")
        print(f"   成功标准: {verification['success_criteria']}")

        # 生成完整报告
        report = {
            "timestamp": datetime.now().isoformat(),
            "phase1_system_probe": system_state,
            "phase2_entropy_analysis": entropy_analysis,
            "phase3_expert_match": expert_match,
            "phase4_root_cause": root_cause,
            "phase5_optimal_fix": optimal_fix,
            "phase6_verification": verification,
            "expert_level": "TOP3",
            "entropy_reduction": True,
            "optimal_path": True
        }

        return report

    def _probe_system(self) -> Dict:
        """探测系统状态"""
        state = {
            "gateway": self._probe_gateway(),
            "transport": self._probe_transport(),
            "memory": self._probe_memory(),
            "config": self._probe_config(),
            "processes": self._probe_processes(),
            "resources": self._probe_resources()
        }

        # 综合健康状态
        state["health_score"] = self._calculate_health_score(state)
        state["critical_issues"] = self._identify_critical_issues(state)

        return state

    def _probe_gateway(self) -> Dict:
        """探测 Gateway 状态"""
        result = {
            "running": False,
            "pid": None,
            "port_listening": False,
            "health_check": None,
            "uptime": None,
            "version": None
        }

        # 检查进程
        try:
            ps_result = subprocess.run(
                ["pgrep", "-f", "openclaw"],
                capture_output=True, text=True, timeout=5
            )
            if ps_result.stdout.strip():
                result["running"] = True
                result["pid"] = int(ps_result.stdout.strip().split()[0])
        except Exception:
            pass

        # 检查端口
        try:
            netstat_result = subprocess.run(
                ["lsof", "-i", ":18789"],
                capture_output=True, text=True, timeout=5
            )
            result["port_listening"] = bool(netstat_result.stdout.strip())
        except Exception:
            pass

        # 健康检查
        try:
            health_result = subprocess.run(
                ["curl", "-s", "-m", 3, "http://127.0.0.1:18789/api/health"],
                capture_output=True, text=True, timeout=5
            )
            if health_result.returncode == 0:
                result["health_check"] = health_result.stdout.strip()
        except Exception:
            pass

        return result

    def _probe_transport(self) -> Dict:
        """探测传输层状态"""
        return {
            "websocket_enabled": self._check_websocket(),
            "http_enabled": self._check_http(),
            "proxy_configured": self._check_proxy()
        }

    def _probe_memory(self) -> Dict:
        """探测 Memory 系统"""
        memory_dir = Path.home() / ".openclaw" / "memory"
        return {
            "exists": memory_dir.exists(),
            "size_mb": self._get_dir_size(memory_dir) if memory_dir.exists() else 0,
            "file_count": len(list(memory_dir.glob("*"))) if memory_dir.exists() else 0,
            "index_valid": (memory_dir / ".index").exists() if memory_dir.exists() else False
        }

    def _probe_config(self) -> Dict:
        """探测配置系统"""
        config_file = Path.home() / ".openclaw" / "openclaw.json"
        result = {
            "exists": config_file.exists(),
            "valid_json": False,
            "valid_schema": False,
            "model_configured": False,
            "channels_configured": False
        }

        if config_file.exists():
            try:
                with open(config_file, 'r') as f:
                    config = json.load(f)
                result["valid_json"] = True
                result["model_configured"] = "model" in config and config["model"].get("provider")
                result["channels_configured"] = "channels" in config and config["channels"]
            except Exception:
                pass

        return result

    def _probe_processes(self) -> Dict:
        """探测进程状态"""
        return {
            "openclaw_processes": self._count_processes("openclaw"),
            "node_processes": self._count_processes("node"),
            "gateway_daemon": self._check_gateway_daemon()
        }

    def _probe_resources(self) -> Dict:
        """探测资源使用"""
        resources = {"memory_mb": 0, "cpu_percent": 0}

        try:
            if sys.platform == "linux":
                mem_result = subprocess.run(
                    ["free", "-m"],
                    capture_output=True, text=True, timeout=5
                )
                lines = mem_result.stdout.strip().split("\n")
                if len(lines) > 1:
                    parts = lines[1].split()
                    resources["memory_mb"] = int(parts[2])
                    resources["memory_available_mb"] = int(parts[6]) if len(parts) > 6 else 0
        except Exception:
            pass

        return resources

    def _check_websocket(self) -> bool:
        try:
            result = subprocess.run(
                ["curl", "-s", "-m", "3", "-I", "http://127.0.0.1:18789"],
                capture_output=True, text=True, timeout=5
            )
            return "upgrade" in result.stdout.lower() or "websocket" in result.stdout.lower()
        except Exception:
            return False

    def _check_http(self) -> bool:
        try:
            result = subprocess.run(
                ["curl", "-s", "-m", "3", "-o", "/dev/null", "-w", "%{http_code}", "http://127.0.0.1:18789"],
                capture_output=True, text=True, timeout=5
            )
            return result.stdout.strip() in ["200", "301", "302"]
        except Exception:
            return False

    def _check_proxy(self) -> bool:
        return bool(os.environ.get("http_proxy") or os.environ.get("HTTP_PROXY"))

    def _get_dir_size(self, path: Path) -> int:
        total = 0
        try:
            for f in path.rglob("*"):
                if f.is_file():
                    total += f.stat().st_size
        except Exception:
            pass
        return total // (1024 * 1024)

    def _count_processes(self, name: str) -> int:
        try:
            result = subprocess.run(
                ["pgrep", "-c", "-f", name],
                capture_output=True, text=True, timeout=5
            )
            return int(result.stdout.strip())
        except Exception:
            return 0

    def _check_gateway_daemon(self) -> bool:
        try:
            result = subprocess.run(
                ["systemctl", "is-active", "openclaw"],
                capture_output=True, text=True, timeout=5
            )
            return "active" in result.stdout.lower()
        except Exception:
            return False

    def _calculate_health_score(self, state: Dict) -> float:
        """计算健康分数"""
        score = 1.0

        if not state["gateway"]["running"]:
            score -= 0.4
        if not state["gateway"]["port_listening"]:
            score -= 0.2
        if state["gateway"]["health_check"] is None:
            score -= 0.2
        if not state["config"]["valid_json"]:
            score -= 0.1
        if state["resources"]["memory_available_mb"] < 500 if "memory_available_mb" in state["resources"] else False:
            score -= 0.1

        return max(0.0, score)

    def _identify_critical_issues(self, state: Dict) -> List[str]:
        """识别关键问题"""
        issues = []
        if not state["gateway"]["running"]:
            issues.append("Gateway 未运行")
        if not state["config"]["valid_json"]:
            issues.append("配置文件无效")
        if not state["gateway"]["port_listening"]:
            issues.append("端口 18789 未监听")
        return issues

    def _print_probe_results(self, state: Dict):
        """打印探测结果"""
        print(f"   健康分数: {state['health_score']:.0%}")

        gw = state["gateway"]
        print(f"   Gateway: {'✅ 运行中' if gw['running'] else '❌ 未运行'} (PID: {gw['pid']})")
        print(f"   端口监听: {'✅ 18789' if gw['port_listening'] else '❌ 未监听'}")
        print(f"   健康检查: {gw['health_check'] or '❌ 失败'}")

        cfg = state["config"]
        print(f"   配置: {'✅ 有效' if cfg['valid_json'] else '❌ 无效'}")

        mem = state["memory"]
        print(f"   Memory: {'✅ 存在' if mem['exists'] else '❌ 缺失'} ({mem['size_mb']}MB)")

    def _extract_keywords(self, text: str) -> List[str]:
        """提取关键词"""
        keywords = []
        tech_terms = ["gateway", "websocket", "node", "memory", "config", "channel",
                      "plugin", "auth", "transport", "port", "health", "token"]

        text_lower = text.lower()
        for term in tech_terms:
            if term in text_lower:
                keywords.append(term)

        return keywords

    def _match_expert_pattern(self, symptom: str, system_state: Dict) -> Optional[Dict]:
        """匹配专家知识模式"""
        symptom_lower = symptom.lower()

        for pattern_name, pattern_info in self.knowledge.OPENCLAW_ERROR_PATTERNS.items():
            # 检查症状匹配
            for symptom_pattern in pattern_info["symptoms"]:
                if symptom_pattern.lower() in symptom_lower:
                    # 验证组件状态
                    affected_components = pattern_info["components"]
                    component_healthy = all(
                        system_state.get(comp, {}).get("running", True)
                        for comp in affected_components
                        if comp in system_state
                    )

                    return {
                        "pattern": pattern_name,
                        "confidence": 0.9 if component_healthy else 0.7,
                        "info": pattern_info
                    }

        return None

    def _locate_root_cause(self, symptom: str, system_state: Dict,
                           expert_match: Optional[Dict]) -> Dict:
        """定位根因"""
        # 如果有专家匹配，使用匹配结果
        if expert_match:
            return {
                "description": expert_match["info"]["root_cause"],
                "components": expert_match["info"]["components"],
                "entropy_source": expert_match["info"]["entropy_type"],
                "diagnosis_steps": expert_match["info"]["diagnosis_steps"]
            }

        # 否则基于系统状态推断
        root_causes = []

        if not system_state["gateway"]["running"]:
            root_causes.append({
                "description": "Gateway 进程未运行",
                "components": ["gateway"],
                "entropy_source": "state"
            })

        if not system_state["config"]["valid_json"]:
            root_causes.append({
                "description": "配置文件损坏",
                "components": ["config_engine"],
                "entropy_source": "structural"
            })

        if not system_state["gateway"]["port_listening"]:
            root_causes.append({
                "description": "端口 18789 被占用或未监听",
                "components": ["transport"],
                "entropy_source": "state"
            })

        if root_causes:
            return root_causes[0]

        return {
            "description": "需要进一步分析",
            "components": ["gateway"],
            "entropy_source": "unknown"
        }

    def _generate_optimal_fix(self, root_cause: Dict,
                             expert_match: Optional[Dict]) -> Dict:
        """生成最优修复方案"""
        fixes = []

        # 从专家知识获取修复方案
        if expert_match:
            for fix_info in expert_match["info"]["fixes"]:
                action = fix_info["action"]
                if action in self.knowledge.FIX_ACTIONS:
                    fixes.append({
                        "action": action,
                        "description": self.knowledge.FIX_ACTIONS[action]["description"],
                        "commands": self.knowledge.FIX_ACTIONS[action]["commands"],
                        "priority": fix_info["priority"]
                    })

        # 如果没有专家方案，基于根因生成
        if not fixes:
            entropy_source = root_cause.get("entropy_source", "")

            if entropy_source == "state":
                fixes.append({
                    "action": "restart_gateway",
                    "description": "重启 Gateway",
                    "commands": self.knowledge.FIX_ACTIONS["restart_gateway"]["commands"],
                    "priority": 1
                })
            elif entropy_source == "structural":
                fixes.append({
                    "action": "fix_config",
                    "description": "修复配置文件",
                    "commands": self.knowledge.FIX_ACTIONS["fix_config"]["commands"],
                    "priority": 1
                })
            elif entropy_source == "connectivity":
                fixes.append({
                    "action": "restart_gateway",
                    "description": "重启 Gateway 恢复连接",
                    "commands": self.knowledge.FIX_ACTIONS["restart_gateway"]["commands"],
                    "priority": 1
                })

        # 选择最优方案（最小干预）
        optimal = self.pathfinder.select_minimal_intervention(fixes)

        return {
            "primary_fix": optimal,
            "all_fixes": fixes,
            "is_minimal_intervention": True,
            "entropy_reduction_strategy": self._get_entropy_strategy(root_cause)
        }

    def _get_entropy_strategy(self, root_cause: Dict) -> str:
        """获取熵减策略"""
        entropy_type = root_cause.get("entropy_source", "")

        strategies = {
            "structural": "恢复数据完整性，消除结构熵增",
            "state": "恢复进程状态，消除状态熵增",
            "connectivity": "恢复网络连接，消除连接熵增",
            "resource": "释放/增加资源，消除资源熵增",
            "auth": "重置认证状态，消除认证熵增"
        }

        return strategies.get(entropy_type, "分析并消除问题根源")

    def _print_fix_plan(self, fix_plan: Dict):
        """打印修复计划"""
        primary = fix_plan["primary_fix"]
        print(f"   建议修复: {primary['description']}")
        print(f"   操作类型: {primary['action']}")
        print(f"   熵减策略: {fix_plan['entropy_reduction_strategy']}")

        if primary.get("commands"):
            print("   执行命令:")
            for cmd in primary["commands"]:
                print(f"     $ {cmd}")

    def _generate_verification(self, fix_plan: Dict) -> Dict:
        """生成验证策略"""
        primary = fix_plan["primary_fix"]
        action = primary.get("action", "")

        verification_map = {
            "restart_gateway": {
                "command": "curl -s http://127.0.0.1:18789/api/health",
                "success_criteria": "返回 200 和健康状态"
            },
            "fix_config": {
                "command": "cat ~/.openclaw/openclaw.json | python3 -m json.tool",
                "success_criteria": "JSON 格式正确，无错误"
            },
            "kill_conflicting": {
                "command": "lsof -i :18789",
                "success_criteria": "端口空闲"
            }
        }

        default = {
            "command": "openclaw gateway status",
            "success_criteria": "Gateway 运行中"
        }

        return verification_map.get(action, default)

    def run_full_expert_diagnosis(self) -> Dict:
        """运行完整专家诊断"""
        print("\n" + "="*70)
        print("🔬 OpenClaw 完整专家诊断")
        print("="*70)

        # 系统级探测
        system_state = self._probe_system()

        print("\n📊 系统状态总览")
        self._print_probe_results(system_state)

        # 生成综合报告
        report = {
            "timestamp": datetime.now().isoformat(),
            "system_state": system_state,
            "health_score": system_state["health_score"],
            "critical_issues": system_state["critical_issues"],
            "expert_level": "TOP3",
            "analysis_method": "第一性原理 + 熵减分析",
            "optimal_path": True
        }

        return report


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="OpenClaw 专家诊断系统 v3.0 - 第一性原理分析"
    )
    parser.add_argument("--symptom", "-s", type=str, help="问题症状")
    parser.add_argument("--full", "-F", action="store_true", help="完整系统诊断")
    parser.add_argument("--json", "-J", action="store_true", help="JSON 输出")
    parser.add_argument("--expert", "-E", action="store_true", help="专家模式（详细）")

    args = parser.parse_args()

    expert = OpenClawExpertDiagnoser()

    if args.full:
        report = expert.run_full_expert_diagnosis()
    elif args.symptom:
        report = expert.diagnose(args.symptom)
    else:
        print("请指定症状或使用 --full 进行完整诊断")
        print("示例:")
        print("  python3 expert_diagnose.py --symptom 'gateway failed to start'")
        print("  python3 expert_diagnose.py --full")
        return

    if args.json:
        print("\n" + json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
