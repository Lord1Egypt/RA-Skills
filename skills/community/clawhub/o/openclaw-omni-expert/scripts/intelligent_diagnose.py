#!/usr/bin/env python3
"""
OpenClaw 智能诊断工具 v2.0
具备自学习、自推理、自进化能力的智能诊断系统

核心能力：
1. 预设模式匹配（已知问题快速响应）
2. 智能推理（未知问题的语义分析）
3. 实时知识获取（web_search 最新问题）
4. 自学习进化（记录成功案例，不断成长）
"""

import os
import sys
import json
import re
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime
from dataclasses import dataclass, asdict


@dataclass
class DiagnosticResult:
    """诊断结果"""
    status: str  # pass/warning/fail/unknown
    category: str
    title: str
    description: str
    solution: str
    confidence: float  # 0.0 - 1.0
    source: str  # knowledge_base / inference / web_search / manual
    learned: bool = False  # 是否已学习到知识库


class OpenClawKnowledgeBase:
    """自进化知识库"""

    def __init__(self, kb_dir: Optional[Path] = None):
        self.kb_dir = kb_dir or (Path.home() / ".openclaw" / "knowledge")
        self.kb_dir.mkdir(parents=True, exist_ok=True)
        self.db_file = self.kb_dir / "openclaw_knowledge.json"
        self.learned_file = self.kb_dir / "learned_cases.json"

        self.knowledge = self._load_knowledge()
        self.learned_cases = self._load_learned()

    def _load_knowledge(self) -> Dict:
        """加载内置知识库"""
        return {
            "error_patterns": [
                {
                    "pattern": r"Node.*version.*(\d+)",
                    "error_type": "node_version",
                    "severity": "critical",
                    "description": "Node.js 版本不兼容",
                    "solution_template": "OpenClaw 需要 Node.js v22+，当前版本 {version}。建议使用 nvm 管理 Node 版本：nvm install 22 && nvm use 22",
                    "keywords": ["node", "version", "v18", "v16", "require"]
                },
                {
                    "pattern": r"EACCES|Permission denied",
                    "error_type": "permission",
                    "severity": "high",
                    "description": "权限不足",
                    "solution_template": "使用 npm 用户目录安装：mkdir -p ~/.npm-global && npm config set prefix '~/.npm-global'",
                    "keywords": ["permission", "denied", "eacces", "root"]
                },
                {
                    "pattern": r"ETIMEDOUT|ECONNREFUSED|ENOTFOUND",
                    "error_type": "network",
                    "severity": "high",
                    "description": "网络连接问题",
                    "solution_template": "检查网络连接，考虑使用国内镜像源：npm config set registry https://registry.npmmirror.com",
                    "keywords": ["timeout", "connection", "refused", "network", "fetch"]
                },
                {
                    "pattern": r"port.*(\d+).*already in use|EADDRINUSE",
                    "error_type": "port_conflict",
                    "severity": "medium",
                    "description": "端口被占用",
                    "solution_template": "端口 {port} 被占用。查找占用进程：lsof -i :{port}，或更改 OpenClaw 端口配置",
                    "keywords": ["port", "in use", "address", "listen"]
                },
                {
                    "pattern": r"ENOENT|No such file|not found",
                    "error_type": "file_missing",
                    "severity": "high",
                    "description": "文件或目录缺失",
                    "solution_template": "相关文件或目录不存在。尝试重新安装 OpenClaw：npm uninstall -g openclaw && npm install -g openclaw",
                    "keywords": ["enoent", "not found", "missing", "exist"]
                },
                {
                    "pattern": r"WebSocket|ws://|wss://",
                    "error_type": "websocket",
                    "severity": "medium",
                    "description": "WebSocket 连接问题",
                    "solution_template": "WebSocket 连接失败。检查网络代理设置、防火墙配置，或确认服务地址正确",
                    "keywords": ["websocket", "ws", "connect", "upgrade"]
                },
                {
                    "pattern": r"ECONNRESET|connection reset",
                    "error_type": "connection_reset",
                    "severity": "medium",
                    "description": "连接被重置",
                    "solution_template": "连接被远程端重置。可能原因：网络不稳定、对方服务重启、请求超时。建议重试",
                    "keywords": ["reset", "connection", "peer", "abort"]
                },
                {
                    "pattern": r"certificate|SSL|TLS|self-signed",
                    "error_type": "ssl_cert",
                    "severity": "medium",
                    "description": "SSL 证书问题",
                    "solution_template": "SSL 证书验证失败。可尝试：1) 更新 CA 证书 2) 设置 NODE_TLS_REJECT_UNAUTHORIZED=0（仅开发环境）",
                    "keywords": ["certificate", "ssl", "tls", "cert", "verify"]
                },
                {
                    "pattern": r"out of memory|OOM|heap",
                    "error_type": "memory",
                    "severity": "high",
                    "description": "内存不足",
                    "solution_template": "系统内存不足。检查可用内存：free -m。如运行大模型，需增加内存或使用 swap",
                    "keywords": ["memory", "heap", "oom", "allocate"]
                },
                {
                    "pattern": r"JSON.parse|JSONDecode|syntax error",
                    "error_type": "config_json",
                    "severity": "high",
                    "description": "配置文件 JSON 格式错误",
                    "solution_template": "配置文件格式错误。检查 ~/.openclaw/openclaw.json 语法是否正确",
                    "keywords": ["json", "parse", "syntax", "unexpected"]
                }
            ],
            "system_patterns": {
                "linux": {
                    "check_commands": ["systemctl status openclaw", "journalctl -u openclaw"],
                    "common_issues": ["systemd权限", "服务启动失败", "日志位置: /var/log/openclaw"]
                },
                "macos": {
                    "check_commands": ["launchctl list | grep openclaw", "log show --predicate 'process == \"openclaw\"'"],
                    "common_issues": ["launchd权限", "Gatekeeper拦截", "日志位置: ~/Library/Logs/OpenClaw"]
                },
                "windows": {
                    "check_commands": ["Get-Service openclaw", "EventLog -LogName Application"],
                    "common_issues": ["PowerShell执行策略", "Windows Defender", "日志位置: %APPDATA%\\OpenClaw\\logs"]
                }
            },
            "last_updated": "2024-01-15T00:00:00Z"
        }

    def _load_learned(self) -> List[Dict]:
        """加载学习到的案例"""
        if self.learned_file.exists():
            try:
                with open(self.learned_file, 'r') as f:
                    return json.load(f)
            except Exception:
                pass
        return []

    def add_learned_case(self, error: str, solution: str, verification: str = ""):
        """添加学习到的案例"""
        case = {
            "error": error,
            "solution": solution,
            "verification": verification,
            "learned_at": datetime.now().isoformat(),
            "success_count": 1
        }

        # 检查是否已存在
        for existing in self.learned_cases:
            if error in existing.get("error", "") or existing.get("error", "") in error:
                existing["success_count"] += 1
                existing["last_used"] = datetime.now().isoformat()
                if solution and not existing.get("solution"):
                    existing["solution"] = solution
                self._save_learned()
                return

        self.learned_cases.append(case)
        self._save_learned()

    def _save_learned(self):
        """保存学习案例"""
        try:
            with open(self.learned_file, 'w') as f:
                json.dump(self.learned_cases, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"警告: 保存学习案例失败: {e}")

    def find_pattern_match(self, error_text: str) -> Optional[Dict]:
        """查找知识库匹配"""
        error_lower = error_text.lower()

        # 优先级1: 学习案例（最高优先级）
        for case in self.learned_cases:
            if case["error"].lower() in error_lower or error_lower in case["error"].lower():
                return {
                    "pattern": case["error"],
                    "solution": case["solution"],
                    "confidence": 0.95,
                    "source": "learned"
                }

        # 优先级2: 内置模式
        for item in self.knowledge["error_patterns"]:
            if any(kw in error_lower for kw in item["keywords"]):
                # 尝试提取变量
                match = re.search(item["pattern"], error_text, re.IGNORECASE)
                if match:
                    groups = match.groups()
                    solution = item["solution_template"]
                    for i, g in enumerate(groups):
                        if g:
                            solution = solution.replace(f"{{{i+1}}}", g)
                    return {
                        "pattern": item["pattern"],
                        "solution": solution,
                        "confidence": 0.85,
                        "source": "knowledge_base"
                    }
                return {
                    "pattern": item["pattern"],
                    "solution": item["solution_template"],
                    "confidence": 0.75,
                    "source": "knowledge_base"
                }

        return None

    def get_all_patterns(self) -> List[str]:
        """获取所有已知模式"""
        patterns = []
        for item in self.knowledge["error_patterns"]:
            patterns.append(f"{item['error_type']}: {item['description']}")
        for case in self.learned_cases:
            patterns.append(f"learned: {case['error'][:50]}...")
        return patterns


class ErrorAnalyzer:
    """错误推理引擎"""

    def __init__(self):
        self.error_categories = {
            "installation": ["install", "npm", "npm ERR", "pkg", "package"],
            "runtime": ["Error:", "Exception", "throw", "crash"],
            "configuration": ["config", "json", "yaml", "env", "setting"],
            "network": ["connect", "timeout", "fetch", "request", "http"],
            "permission": ["permission", "denied", "root", "sudo", "access"],
            "resource": ["memory", "cpu", "disk", "space", "limit"]
        }

    def analyze(self, error_text: str) -> Dict[str, Any]:
        """深度分析错误"""
        result = {
            "raw_error": error_text,
            "category": self._categorize(error_text),
            "severity": self._estimate_severity(error_text),
            "keywords": self._extract_keywords(error_text),
            "stack_trace": self._extract_stack_trace(error_text),
            "context": self._extract_context(error_text),
            "inference": self._infer_possible_causes(error_text)
        }
        return result

    def _categorize(self, error_text: str) -> str:
        """分类错误"""
        error_lower = error_text.lower()
        scores = {}

        for category, keywords in self.error_categories.items():
            score = sum(1 for kw in keywords if kw in error_lower)
            if score > 0:
                scores[category] = score

        if scores:
            return max(scores, key=scores.get)
        return "unknown"

    def _estimate_severity(self, error_text: str) -> str:
        """评估严重程度"""
        critical_keywords = ["fatal", "crash", "panic", "core dump", "segfault"]
        high_keywords = ["error", "failed", "cannot", "unable", "ERR!"]
        medium_keywords = ["warning", "warn", "deprecated"]
        low_keywords = ["info", "debug", "trace"]

        error_lower = error_text.lower()

        if any(kw in error_lower for kw in critical_keywords):
            return "critical"
        elif any(kw in error_lower for kw in high_keywords):
            return "high"
        elif any(kw in error_lower for kw in medium_keywords):
            return "medium"
        return "low"

    def _extract_keywords(self, error_text: str) -> List[str]:
        """提取关键词"""
        # 提取技术术语
        tech_terms = re.findall(r'\b(Node\.js|npm|Git|Python|WebSocket|SSL|TLS|JSON|YAML|API|SDK)\b', error_text)
        # 提取错误码
        error_codes = re.findall(r'\b(E[A-Z]{2,5}_\d+|0x[0-9a-fA-F]+|\d{3,4})\b', error_text)
        # 提取路径
        paths = re.findall(r'(/[a-zA-Z0-9_/.-]+)+', error_text)
        paths = [p for p in paths if len(p) > 5][:3]

        return {
            "technologies": list(set(tech_terms)),
            "error_codes": list(set(error_codes)),
            "paths": paths
        }

    def _extract_stack_trace(self, error_text: str) -> Optional[str]:
        """提取堆栈跟踪"""
        lines = error_text.split('\n')
        stack_lines = []

        for line in lines:
            if 'at ' in line or 'File "' in line or 'line ' in line.lower():
                stack_lines.append(line.strip())

        if stack_lines:
            return '\n'.join(stack_lines[:10])  # 只取前10行

        return None

    def _extract_context(self, error_text: str) -> Dict:
        """提取上下文信息"""
        # 提取版本信息
        versions = re.findall(r'(Node\.js|node|npm)[\s:]+v?(\d+\.\d+\.\d+)', error_text, re.IGNORECASE)
        # 提取时间戳
        timestamps = re.findall(r'\d{4}-\d{2}-\d{2}[T\s]\d{2}:\d{2}:\d{2}', error_text)

        return {
            "versions": [{"name": v[0], "version": v[1]} for v in versions],
            "timestamps": timestamps
        }

    def _infer_possible_causes(self, error_text: str) -> List[str]:
        """推理可能原因"""
        causes = []
        error_lower = error_text.lower()

        # 基于关键词推理
        if "timeout" in error_lower:
            causes.append("网络连接超时，可能是网络不稳定或目标服务器响应慢")
        if "econnrefused" in error_lower:
            causes.append("连接被拒绝，服务可能未启动或端口被防火墙拦截")
        if "enoent" in error_lower:
            causes.append("文件或目录不存在，可能是安装不完整或路径错误")
        if "eacces" in error_lower:
            causes.append("权限不足，可能需要使用 sudo 或修复目录权限")
        if "ebusy" in error_lower:
            causes.append("文件被占用，可能有进程正在使用该文件")
        if "enomem" in error_lower or "memory" in error_lower:
            causes.append("内存不足，可能需要增加可用内存或关闭其他程序")
        if "version" in error_lower and "node" in error_lower:
            causes.append("Node.js 版本不兼容，需要升级到 v22+")
        if "ssl" in error_lower or "certificate" in error_lower:
            causes.append("SSL 证书问题，可能需要更新证书或检查系统时间")
        if "parse" in error_lower and "json" in error_lower:
            causes.append("JSON 解析失败，配置文件格式错误")
        if "websocket" in error_lower or "ws://" in error_lower:
            causes.append("WebSocket 连接问题，可能是代理设置或网络策略导致")

        return causes


class IntelligentDiagnoser:
    """智能诊断主程序"""

    def __init__(self, use_web_search: bool = True, auto_learn: bool = True):
        self.kb = OpenClawKnowledgeBase()
        self.analyzer = ErrorAnalyzer()
        self.use_web_search = use_web_search
        self.auto_learn = auto_learn

    def diagnose(self, error_input: str, context: Optional[Dict] = None) -> DiagnosticResult:
        """
        智能诊断入口
        策略：知识库匹配 -> 推理分析 -> 实时搜索 -> 返回结果
        """
        print(f"\n{'='*60}")
        print(f"🧠 OpenClaw 智能诊断系统 v2.0")
        print(f"{'='*60}")

        # Step 1: 知识库匹配
        print("\n📚 [1/4] 搜索知识库...")
        kb_match = self.kb.find_pattern_match(error_input)

        if kb_match and kb_match["confidence"] >= 0.8:
            print(f"   ✅ 找到匹配 (置信度: {kb_match['confidence']:.0%})")
            return DiagnosticResult(
                status="known",
                category="knowledge_base",
                title="已知问题",
                description=kb_match.get("pattern", ""),
                solution=kb_match["solution"],
                confidence=kb_match["confidence"],
                source=kb_match["source"]
            )

        # Step 2: 深度推理分析
        print("\n🔍 [2/4] 深度分析错误...")
        analysis = self.analyzer.analyze(error_input)
        print(f"   分类: {analysis['category']}")
        print(f"   严重程度: {analysis['severity']}")

        if analysis['keywords']['technologies']:
            print(f"   技术栈: {', '.join(analysis['keywords']['technologies'])}")

        # Step 3: 推理解决方案
        print("\n💡 [3/4] 推理解决方案...")

        # 构建基于推理的解决方案
        inferred_solution = self._build_inferred_solution(analysis)

        if analysis['inference']:
            print("   推理的可能原因:")
            for cause in analysis['inference']:
                print(f"     - {cause}")

        # Step 4: 实时知识获取（如果启用）
        web_solution = None
        if self.use_web_search and analysis['category'] != 'unknown':
            print("\n🌐 [4/4] 查询最新知识...")
            web_solution = self._search_online(error_input, analysis)

        # 综合结果
        if web_solution:
            return DiagnosticResult(
                status="resolved",
                category=analysis['category'],
                title=f"通过实时搜索找到解决方案",
                description="\n".join(analysis['inference']) if analysis['inference'] else "基于错误分析推理",
                solution=web_solution,
                confidence=0.9,
                source="web_search"
            )
        elif inferred_solution:
            return DiagnosticResult(
                status="inferred",
                category=analysis['category'],
                title=f"推理的解决方案",
                description="\n".join(analysis['inference']) if analysis['inference'] else "基于错误特征推理",
                solution=inferred_solution,
                confidence=0.6,
                source="inference"
            )
        else:
            return DiagnosticResult(
                status="unknown",
                category=analysis['category'],
                title="未知问题",
                description=error_input[:200],
                solution="无法自动诊断。请提供更多上下文信息，或查看 OpenClaw 官方文档和 GitHub Issues",
                confidence=0.0,
                source="manual"
            )

    def _build_inferred_solution(self, analysis: Dict) -> str:
        """基于分析构建解决方案"""
        solutions = []

        category = analysis['category']

        # 基于类别的通用解决方案
        category_solutions = {
            "installation": "尝试完整重新安装：\n1. npm uninstall -g openclaw\n2. rm -rf ~/.openclaw\n3. npm cache clean --force\n4. npm install -g openclaw@latest",
            "runtime": "检查服务状态：\n1. openclaw gateway status\n2. 查看日志：tail -f ~/.openclaw/logs/*.log\n3. 尝试重启：openclaw gateway restart",
            "configuration": "检查配置文件：\n1. 验证 JSON 格式：cat ~/.openclaw/openclaw.json | python3 -m json.tool\n2. 检查环境变量：echo $OPENCLAW_*\n3. 使用配置向导：openclaw configure",
            "network": "检查网络设置：\n1. 测试连接：curl -v https://api.openclaw.ai\n2. 检查代理：echo $HTTP_PROXY\n3. 尝试更换镜像源：npm config set registry https://registry.npmmirror.com",
            "permission": "修复权限：\n1. 检查当前用户：whoami\n2. 修复目录权限：chmod 755 ~/.openclaw\n3. 如需 sudo 权限：sudo npm install -g openclaw",
            "resource": "检查资源使用：\n1. 内存：free -m\n2. 磁盘：df -h\n3. 关闭其他程序释放资源"
        }

        if category in category_solutions:
            solutions.append(category_solutions[category])

        if analysis['inference']:
            solutions.append("根据错误特征，建议：\n" + "\n".join(f"- {c}" for c in analysis['inference']))

        return "\n\n".join(solutions) if solutions else ""

    def _search_online(self, error: str, analysis: Dict) -> Optional[str]:
        """在线搜索解决方案（需要外部 web_search 能力）"""
        # 注意：这里需要智能体调用 web_search 工具
        # 脚本本身只负责构建搜索 query

        search_queries = []

        # 构建搜索查询
        if analysis['keywords']['technologies']:
            tech = analysis['keywords']['technologies'][0]
            search_queries.append(f"OpenClaw {tech} {analysis['category']} error fix")
        else:
            search_queries.append(f"OpenClaw error {error[:50]} solution")

        # 返回查询供智能体执行
        print(f"   建议搜索查询：")
        for q in search_queries:
            print(f"     - {q}")

        return None  # 实际搜索由智能体执行

    def learn_from_solution(self, error: str, solution: str, success: bool):
        """学习解决方案"""
        if self.auto_learn and success:
            self.kb.add_learned_case(error, solution)
            print(f"\n📝 已将新案例添加到知识库")

    def run_full_diagnosis(self) -> Dict:
        """运行完整系统诊断"""
        print("\n" + "="*60)
        print("🔧 OpenClaw 完整系统诊断")
        print("="*60)

        results = {
            "timestamp": datetime.now().isoformat(),
            "diagnostics": []
        }

        # 检查 OpenClaw 安装
        print("\n[1/6] 检查 OpenClaw 安装...")
        try:
            result = subprocess.run(
                ["openclaw", "--version"],
                capture_output=True, text=True, timeout=10
            )
            if result.returncode == 0:
                results["diagnostics"].append({
                    "check": "installation",
                    "status": "pass",
                    "detail": result.stdout.strip()
                })
                print(f"   ✅ {result.stdout.strip()}")
            else:
                results["diagnostics"].append({
                    "check": "installation",
                    "status": "fail",
                    "detail": "安装可能有问题"
                })
                print("   ❌ 未正确安装")
        except Exception as e:
            results["diagnostics"].append({
                "check": "installation",
                "status": "fail",
                "detail": str(e)
            })
            print(f"   ❌ 未安装: {e}")

        # 检查服务状态
        print("\n[2/6] 检查服务状态...")
        try:
            result = subprocess.run(
                ["openclaw", "gateway", "status"],
                capture_output=True, text=True, timeout=10
            )
            if "running" in result.stdout.lower():
                results["diagnostics"].append({
                    "check": "service",
                    "status": "pass",
                    "detail": "Gateway 运行中"
                })
                print("   ✅ Gateway 运行中")
            else:
                results["diagnostics"].append({
                    "check": "service",
                    "status": "warning",
                    "detail": result.stdout or "状态未知"
                })
                print("   ⚠️ Gateway 未运行")
        except Exception as e:
            results["diagnostics"].append({
                "check": "service",
                "status": "fail",
                "detail": str(e)
            })
            print(f"   ❌ 检查失败: {e}")

        # 检查端口
        print("\n[3/6] 检查端口占用 (18789)...")
        if sys.platform == "linux" or sys.platform == "darwin":
            result = subprocess.run(
                ["lsof", "-i", ":18789"],
                capture_output=True, text=True, timeout=5
            )
            if result.stdout.strip():
                results["diagnostics"].append({
                    "check": "port",
                    "status": "pass",
                    "detail": "端口被占用（正常）"
                })
                print(f"   ✅ 端口正常监听")
            else:
                results["diagnostics"].append({
                    "check": "port",
                    "status": "warning",
                    "detail": "端口未被占用"
                })
                print("   ⚠️ 端口未被占用")
        else:
            results["diagnostics"].append({
                "check": "port",
                "status": "skip",
                "detail": "Windows 跳过"
            })

        # 检查配置
        print("\n[4/6] 检查配置文件...")
        config_file = Path.home() / ".openclaw" / "openclaw.json"
        if config_file.exists():
            try:
                with open(config_file) as f:
                    config = json.load(f)
                has_model = "model" in config and config["model"].get("provider")
                has_channel = "channels" in config and config["channels"]

                if has_model and has_channel:
                    print("   ✅ 配置完整")
                    results["diagnostics"].append({
                        "check": "configuration",
                        "status": "pass",
                        "detail": "已配置模型和频道"
                    })
                else:
                    print("   ⚠️ 配置不完整")
                    results["diagnostics"].append({
                        "check": "configuration",
                        "status": "warning",
                        "detail": "缺少模型或频道配置"
                    })
            except Exception as e:
                print(f"   ❌ 配置文件错误: {e}")
                results["diagnostics"].append({
                    "check": "configuration",
                    "status": "fail",
                    "detail": f"JSON 解析错误: {e}"
                })
        else:
            print("   ⚠️ 配置文件不存在")
            results["diagnostics"].append({
                "check": "configuration",
                "status": "warning",
                "detail": "配置文件不存在"
            })

        # 检查日志
        print("\n[5/6] 检查最近错误...")
        log_dir = Path.home() / ".openclaw" / "logs"
        if log_dir.exists():
            log_files = list(log_dir.glob("*.log"))
            if log_files:
                latest_log = max(log_files, key=lambda p: p.stat().st_mtime)
                with open(latest_log, 'r') as f:
                    lines = f.readlines()
                    recent_errors = [l for l in lines if "error" in l.lower() or "Error" in l]
                    if recent_errors:
                        print(f"   ⚠️ 发现 {len(recent_errors)} 条错误")
                        results["diagnostics"].append({
                            "check": "logs",
                            "status": "warning",
                            "detail": f"最近 {len(recent_errors)} 条错误",
                            "sample": recent_errors[-1][:100]
                        })
                    else:
                        print("   ✅ 无错误")
                        results["diagnostics"].append({
                            "check": "logs",
                            "status": "pass",
                            "detail": "日志正常"
                        })
            else:
                print("   ℹ️ 无日志文件")
        else:
            print("   ℹ️ 日志目录不存在")

        # 知识库状态
        print("\n[6/6] 知识库状态...")
        kb_stats = self._get_kb_stats()
        print(f"   已知模式: {kb_stats['patterns']}")
        print(f"   学习案例: {kb_stats['learned']}")
        print(f"   最后更新: {kb_stats['last_updated']}")
        results["diagnostics"].append({
            "check": "knowledge_base",
            "status": "info",
            "detail": kb_stats
        })

        return results

    def _get_kb_stats(self) -> Dict:
        """获取知识库统计"""
        return {
            "patterns": len(self.kb.knowledge["error_patterns"]),
            "learned": len(self.kb.learned_cases),
            "last_updated": self.kb.knowledge.get("last_updated", "未知")
        }


def main():
    import argparse

    parser = argparse.ArgumentParser(description="OpenClaw 智能诊断工具 v2.0")
    parser.add_argument("--error", "-e", type=str, help="要诊断的错误信息")
    parser.add_argument("--file", "-f", type=str, help="包含错误的日志文件")
    parser.add_argument("--full", "-F", action="store_true", help="运行完整系统诊断")
    parser.add_argument("--no-web-search", action="store_true", help="禁用在线搜索")
    parser.add_argument("--learn", action="store_true", help="记录成功案例到知识库")
    parser.add_argument("--list-patterns", action="store_true", help="列出所有已知模式")
    parser.add_argument("--json", action="store_true", help="JSON 格式输出")
    parser.add_argument("--verbose", "-v", action="store_true", help="详细输出")

    args = parser.parse_args()

    diagnoser = IntelligentDiagnoser(
        use_web_search=not args.no_web_search,
        auto_learn=args.learn
    )

    # 列出已知模式
    if args.list_patterns:
        print("\n📚 OpenClaw 知识库 - 已知问题模式：\n")
        for i, pattern in enumerate(diagnoser.kb.get_all_patterns(), 1):
            print(f"  {i}. {pattern}")
        print()
        return

    # 完整系统诊断
    if args.full:
        results = diagnoser.run_full_diagnosis()
        if args.json:
            print(json.dumps(results, indent=2, ensure_ascii=False))
        return

    # 诊断指定错误
    error_text = ""
    if args.error:
        error_text = args.error
    elif args.file:
        try:
            with open(args.file, 'r') as f:
                error_text = f.read()
        except Exception as e:
            print(f"❌ 无法读取文件: {e}")
            sys.exit(1)
    else:
        print("❌ 请指定错误信息 (--error) 或日志文件 (--file)")
        print("   或使用 --full 运行完整系统诊断")
        print("   或使用 --list-patterns 查看已知问题模式")
        sys.exit(1)

    # 执行诊断
    result = diagnoser.diagnose(error_text)

    # 输出结果
    print("\n" + "="*60)
    print("📋 诊断结果")
    print("="*60)
    print(f"状态: {result.status}")
    print(f"分类: {result.category}")
    print(f"置信度: {result.confidence:.0%}")
    print(f"来源: {result.source}")
    print(f"\n描述:\n{result.description}")
    print(f"\n解决方案:\n{result.solution}")
    print("="*60)

    if args.verbose:
        print(f"\n💡 如需在线搜索最新解决方案，请在智能体对话中输入错误信息")
        print(f"   系统将自动查询 OpenClaw 官方文档和 GitHub Issues")


if __name__ == "__main__":
    main()
