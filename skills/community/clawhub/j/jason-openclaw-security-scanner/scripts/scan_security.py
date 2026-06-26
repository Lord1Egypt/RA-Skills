#!/usr/bin/env python3
"""
OpenClaw Security Scanner
扫描 OpenClaw 配置和权限，生成安全报告，支持交互式一键修复
"""

import os
import re
import json
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional

# 风险等级
RISK_CRITICAL = "🔴 严重"
RISK_HIGH = "🟠 高危"
RISK_MEDIUM = "🟡 中危"
RISK_LOW = "🟢 低危"
RISK_INFO = "ℹ️ 信息"

# 敏感信息正则模式（更精确的匹配）
SENSITIVE_PATTERNS = {
    "API Key": {
        "pattern": r'(?:api[_-]?key|apikey)\s*[=:]\s*["\']([a-zA-Z0-9_\-]{32,})["\']',
        "description": "API 密钥",
        "fix": "移至环境变量"
    },
    "密码": {
        "pattern": r'(?:password|passwd|pwd)\s*[=:]\s*["\']([^\s"\']{12,})["\'](?!.*(?:example|test|xxx|placeholder))',
        "description": "密码",
        "fix": "移至环境变量"
    },
    "Token": {
        "pattern": r'(?:access_token|auth_token|bearer_token)\s*[=:]\s*["\']([a-zA-Z0-9_\-\.]{32,})["\']',
        "description": "访问令牌",
        "fix": "移至环境变量"
    },
    "Secret": {
        "pattern": r'(?:app_secret|client_secret)\s*[=:]\s*["\']([a-zA-Z0-9_\-]{24,})["\']',
        "description": "应用密钥",
        "fix": "移至环境变量"
    },
    "私钥": {
        "pattern": r'-----BEGIN (?:RSA |EC )?PRIVATE KEY-----',
        "description": "私钥文件",
        "fix": "移至安全位置"
    },
}

# 需要忽略的目录
IGNORE_DIRS = {'node_modules', '.git', '__pycache__', 'venv', 'dist', 'build', '.next'}

# 需要忽略的文件（示例/模板文件）
IGNORE_FILES = {
    'example', 'sample', 'template', 'test', 'mock',
    '.example', '.sample', '.template'
}

# 敏感文件名
SENSITIVE_FILES = [
    ".env", ".env.local", ".env.production", ".env.development",
    "credentials.json", "secrets.json",
    "id_rsa", "id_ed25519"
]

# 操作规则关键词
SAFE_OPERATION_RULES = [
    "删除", "delete", "rm",
    "必须手动", "手动确认", "人工确认",
    "需我确认", "需本人确认"
]


class SecurityScanner:
    def __init__(self, openclaw_dir: str = None, workspace_dir: str = None):
        self.openclaw_dir = Path(openclaw_dir or os.path.expanduser("~/.openclaw"))
        self.workspace_dir = Path(workspace_dir or os.path.expanduser("~/.openclaw/workspace"))
        self.findings: List[Dict] = []
        self._seen_issues: set = set()
        self.fix_results: List[Dict] = []
        
    def _add_finding(self, finding: Dict):
        """添加发现（带去重）"""
        file_path = finding.get('auto_fix', {}).get('file_path', '') if finding.get('auto_fix') else ''
        key = (finding['category'], finding['issue'], file_path)
        if key not in self._seen_issues:
            self._seen_issues.add(key)
            self.findings.append(finding)
        
    def scan_all(self) -> Dict:
        """执行完整扫描"""
        print("🔍 开始安全扫描...")
        print(f"   OpenClaw 目录: {self.openclaw_dir}")
        print(f"   Workspace 目录: {self.workspace_dir}")
        print()
        
        # 1. 配置权限扫描
        self._scan_config()
        
        # 2. 文件权限扫描
        self._scan_file_permissions()
        
        # 3. 操作规则扫描
        self._scan_operation_rules()
        
        # 4. 敏感信息扫描
        self._scan_sensitive_data()
        
        # 5. 日志审计
        self._scan_logs()
        
        # 生成报告
        return self._generate_report()
    
    def _scan_config(self):
        """扫描 openclaw.json 配置"""
        config_file = self.openclaw_dir / "openclaw.json"
        
        if not config_file.exists():
            self._add_finding({
                "category": "配置权限",
                "risk": RISK_MEDIUM,
                "issue": "配置文件不存在",
                "detail": f"未找到 {config_file}",
                "suggestion": "检查 OpenClaw 是否正确安装",
                "auto_fix": None
            })
            return
        
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
        except Exception as e:
            self._add_finding({
                "category": "配置权限",
                "risk": RISK_HIGH,
                "issue": "配置文件解析失败",
                "detail": str(e),
                "suggestion": "检查 openclaw.json 格式是否正确",
                "auto_fix": None
            })
            return
        
        # 检查 agents 配置
        agents = config.get("agents", {})
        defaults = agents.get("defaults", {})
        
        # 检查 subagent 权限
        subagents = defaults.get("subagents", {})
        allow_agents = subagents.get("allowAgents", [])
        if allow_agents == ["*"]:
            self._add_finding({
                "category": "配置权限",
                "risk": RISK_HIGH,
                "issue": "子代理权限过大",
                "detail": "allowAgents 设置为 ['*']，允许所有子代理运行",
                "suggestion": "限制为具体需要的 agent ID",
                "auto_fix": {
                    "type": "config_update",
                    "config_file": str(config_file),
                    "path": "agents.defaults.subagents.allowAgents",
                    "action": "请手动指定允许的 agent ID 列表，如 ['agent-1', 'agent-2']"
                }
            })
        
        # 检查是否禁用了沙箱
        sandbox = defaults.get("sandbox", {})
        if sandbox.get("enabled") == False:
            self._add_finding({
                "category": "配置权限",
                "risk": RISK_CRITICAL,
                "issue": "沙箱已禁用",
                "detail": "sandbox.enabled = false，Agent 可执行任意命令",
                "suggestion": "启用沙箱以限制 Agent 执行范围",
                "auto_fix": {
                    "type": "config_update",
                    "config_file": str(config_file),
                    "path": "agents.defaults.sandbox.enabled",
                    "action": "设置为 true 以启用沙箱"
                }
            })
        
        # 检查外部访问
        gateway = config.get("gateway", {})
        remote = gateway.get("remote", {})
        if remote.get("enabled"):
            public_url = remote.get("publicUrl", "")
            if public_url and "localhost" not in public_url:
                self._add_finding({
                    "category": "配置权限",
                    "risk": RISK_MEDIUM,
                    "issue": "Gateway 暴露在公网",
                    "detail": f"公网地址: {public_url}",
                    "suggestion": "确保使用了 HTTPS 和强认证",
                    "auto_fix": None
                })
        
        # 检查 feishu 配置中的敏感信息
        feishu = config.get("feishu", {})
        if feishu.get("appSecret"):
            secret_value = feishu.get("appSecret", "")
            self._add_finding({
                "category": "配置权限",
                "risk": RISK_MEDIUM,
                "issue": "飞书 AppSecret 存储在配置文件中",
                "detail": f"AppSecret: {secret_value[:8]}...{secret_value[-4:]}",
                "suggestion": "将 appSecret 移至环境变量",
                "auto_fix": {
                    "type": "env_var",
                    "var_name": "FEISHU_APP_SECRET",
                    "var_value": secret_value,
                    "config_path": "feishu.appSecret",
                    "config_file": str(config_file)
                }
            })
        
        print("✅ 配置权限扫描完成")
    
    def _scan_file_permissions(self):
        """扫描文件访问权限"""
        if self.workspace_dir.exists():
            stat_info = os.stat(self.workspace_dir)
            mode = oct(stat_info.st_mode)[-3:]
            
            if mode != "755" and mode != "700":
                self._add_finding({
                    "category": "文件权限",
                    "risk": RISK_LOW,
                    "issue": "Workspace 目录权限过宽",
                    "detail": f"当前权限: {mode}，建议: 755 或 700",
                    "suggestion": "修改目录权限",
                    "auto_fix": {
                        "type": "chmod",
                        "path": str(self.workspace_dir),
                        "mode": "755"
                    }
                })
        
        print("✅ 文件权限扫描完成")
    
    def _scan_operation_rules(self):
        """扫描操作规则设定"""
        tools_md = self.workspace_dir / "TOOLS.md"
        agents_md = self.workspace_dir / "AGENTS.md"
        
        has_delete_rule = False
        rule_files = []
        
        for file_path in [tools_md, agents_md]:
            if file_path.exists():
                rule_files.append(str(file_path.name))
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read().lower()
                        
                        for keyword in SAFE_OPERATION_RULES:
                            if keyword in content:
                                if "删除" in content or "delete" in content:
                                    if any(k in content for k in ["手动", "人工", "确认", "必须"]):
                                        has_delete_rule = True
                                        break
                except Exception:
                    pass
        
        if not has_delete_rule:
            target_file = tools_md if tools_md.exists() else agents_md
            self._add_finding({
                "category": "操作规则",
                "risk": RISK_HIGH,
                "issue": "未设置删除操作限制",
                "detail": "Agent 可能执行删除操作而不需要人工确认",
                "suggestion": "在 TOOLS.md 或 AGENTS.md 中添加规则：'删除操作必须手动确认'",
                "auto_fix": {
                    "type": "add_operation_rule",
                    "target_file": str(target_file) if target_file.exists() else str(tools_md),
                    "rule": "操作红线: 只能执行查询和修改，删除操作必须手动确认"
                }
            })
        
        print("✅ 操作规则扫描完成")
    
    def _scan_sensitive_data(self):
        """扫描敏感信息泄露"""
        if not self.workspace_dir.exists():
            return
        
        for root, dirs, files in os.walk(self.workspace_dir):
            dirs[:] = [d for d in dirs if d.lower() not in IGNORE_DIRS]
            
            for file in files:
                file_path = Path(root) / file
                file_lower = file.lower()
                if any(ignore in file_lower for ignore in IGNORE_FILES):
                    continue
                
                for pattern in SENSITIVE_FILES:
                    if file == pattern or file.startswith(pattern.split('.')[0] + '.'):
                        self._check_env_file(file_path)
                
                if file.endswith(('.env', '.json', '.yaml', '.yml')):
                    self._check_file_content(file_path)
        
        print("✅ 敏感信息扫描完成")
    
    def _check_env_file(self, file_path: Path):
        """检查 .env 文件"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                lines = content.strip().split('\n')
                
                sensitive_lines = []
                for line in lines:
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                    
                    if '=' in line:
                        key, value = line.split('=', 1)
                        key_lower = key.lower()
                        
                        sensitive_keys = ['key', 'secret', 'token', 'password', 'pwd', 'credential']
                        if any(sk in key_lower for sk in sensitive_keys):
                            masked_value = self._mask_sensitive(value.strip('"\''))
                            sensitive_lines.append(f"{key}={masked_value}")
                
                if sensitive_lines:
                    self._add_finding({
                        "category": "敏感信息",
                        "risk": RISK_HIGH,
                        "issue": f"发现敏感文件: {file_path.name}",
                        "detail": f"位置: {file_path.relative_to(self.workspace_dir)}\n敏感内容:\n" + '\n'.join(f"  • {line}" for line in sensitive_lines),
                        "suggestion": "将敏感信息移至环境变量或 .gitignore",
                        "auto_fix": {
                            "type": "env_file",
                            "file_path": str(file_path),
                            "action": "建议将此文件添加到 .gitignore，或将敏感内容移至系统环境变量"
                        }
                    })
        except Exception:
            pass
    
    def _check_file_content(self, file_path: Path):
        """检查文件内容中的敏感信息"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                
                for name, info in SENSITIVE_PATTERNS.items():
                    matches = re.findall(info['pattern'], content, re.IGNORECASE)
                    if matches:
                        real_matches = [m for m in matches if not any(x in str(m).lower() for x in ['example', 'test', 'xxx', 'your_', 'placeholder'])]
                        if real_matches:
                            masked = [self._mask_sensitive(m) for m in real_matches[:3]]
                            self._add_finding({
                                "category": "敏感信息",
                                "risk": RISK_HIGH,
                                "issue": f"发现 {info['description']} 泄露",
                                "detail": f"文件: {file_path.relative_to(self.workspace_dir)}\n发现: {', '.join(masked)}",
                                "suggestion": info['fix'],
                                "auto_fix": {
                                    "type": "content_update",
                                    "file_path": str(file_path),
                                    "action": f"建议将 {info['description']} 移至环境变量"
                                }
                            })
        except Exception:
            pass
    
    def _mask_sensitive(self, value: str) -> str:
        """脱敏显示敏感信息"""
        if len(value) <= 8:
            return '*' * len(value)
        return value[:4] + '*' * (len(value) - 8) + value[-4:]
    
    def _scan_logs(self):
        """扫描日志异常"""
        log_dir = self.openclaw_dir / "logs"
        
        if not log_dir.exists():
            return
        
        gateway_log = log_dir / "gateway.log"
        if gateway_log.exists():
            try:
                with open(gateway_log, 'r', encoding='utf-8', errors='ignore') as f:
                    lines = f.readlines()[-500:]
                    
                    error_count = 0
                    auth_failures = 0
                    recent_errors = []
                    
                    for line in lines:
                        if "error" in line.lower():
                            error_count += 1
                            if len(recent_errors) < 3:
                                recent_errors.append(line.strip()[:100])
                        if "auth" in line.lower() and ("fail" in line.lower() or "denied" in line.lower()):
                            auth_failures += 1
                    
                    if error_count > 50:
                        self._add_finding({
                            "category": "日志审计",
                            "risk": RISK_MEDIUM,
                            "issue": "近期错误较多",
                            "detail": f"最近 500 行日志中有 {error_count} 个错误\n示例:\n" + '\n'.join(f"  • {e}" for e in recent_errors),
                            "suggestion": "检查 gateway.log 了解详细错误信息",
                            "auto_fix": None
                        })
                    
                    if auth_failures > 5:
                        self._add_finding({
                            "category": "日志审计",
                            "risk": RISK_HIGH,
                            "issue": "发现认证失败",
                            "detail": f"最近有 {auth_failures} 次认证失败",
                            "suggestion": "检查是否有未授权访问尝试",
                            "auto_fix": None
                        })
            except Exception:
                pass
        
        print("✅ 日志审计完成")
    
    def _generate_report(self) -> Dict:
        """生成安全报告"""
        risk_stats = {
            RISK_CRITICAL: 0,
            RISK_HIGH: 0,
            RISK_MEDIUM: 0,
            RISK_LOW: 0,
            RISK_INFO: 0
        }
        
        for finding in self.findings:
            risk = finding.get("risk", RISK_INFO)
            if risk in risk_stats:
                risk_stats[risk] += 1
        
        score = 100
        score -= risk_stats[RISK_CRITICAL] * 25
        score -= risk_stats[RISK_HIGH] * 15
        score -= risk_stats[RISK_MEDIUM] * 5
        score -= risk_stats[RISK_LOW] * 2
        score = max(0, min(100, score))
        
        return {
            "scan_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "score": score,
            "risk_stats": risk_stats,
            "findings": self.findings
        }
    
    def print_report(self, report: Dict):
        """打印安全报告"""
        print("\n" + "=" * 70)
        print("🛡️ OpenClaw 安全扫描报告")
        print("=" * 70)
        print(f"📅 扫描时间: {report['scan_time']}")
        print(f"📊 安全评分: {report['score']}/100")
        print()
        
        print("📈 风险统计:")
        has_issues = False
        for risk, count in report['risk_stats'].items():
            if count > 0:
                print(f"   {risk}: {count} 项")
                has_issues = True
        if not has_issues:
            print("   ✅ 未发现问题")
        print()
        
        if report['findings']:
            print("📋 详细发现:")
            print("-" * 70)
            for i, finding in enumerate(report['findings'], 1):
                print(f"\n【{i}】[{finding['category']}] {finding['risk']}")
                print(f"问题: {finding['issue']}")
                print(f"详情: {finding['detail']}")
                print(f"建议: {finding['suggestion']}")
                if finding.get('auto_fix'):
                    print(f"🔧 可修复: 是")
            print()
            print("-" * 70)
        else:
            print("✅ 未发现安全问题")
        
        print("\n" + "=" * 70)
    
    def execute_fix(self, index: int) -> Dict:
        """执行指定问题的修复"""
        if not (0 <= index < len(self.findings)):
            return {"success": False, "message": "无效的问题编号"}
        
        finding = self.findings[index]
        fix = finding.get('auto_fix')
        
        if not fix:
            return {"success": False, "message": "此问题无自动修复方案", "suggestion": finding['suggestion']}
        
        fix_type = fix.get('type')
        
        try:
            if fix_type == 'add_operation_rule':
                return self._fix_operation_rule(fix)
            elif fix_type == 'env_file':
                return self._fix_env_file(fix)
            elif fix_type == 'chmod':
                return self._fix_chmod(fix)
            elif fix_type == 'env_var':
                return self._fix_env_var(fix)
            elif fix_type == 'content_update':
                return self._fix_content_update(fix)
            else:
                return {"success": False, "message": f"未知的修复类型: {fix_type}"}
        except Exception as e:
            return {"success": False, "message": f"修复失败: {str(e)}"}
    
    def _fix_operation_rule(self, fix: Dict) -> Dict:
        """修复：添加操作规则"""
        target_file = Path(fix['target_file'])
        
        if not target_file.parent.exists():
            target_file.parent.mkdir(parents=True, exist_ok=True)
        
        # 读取现有内容
        existing = ""
        if target_file.exists():
            with open(target_file, 'r', encoding='utf-8') as f:
                existing = f.read()
        
        # 检查是否已存在类似规则
        if "删除" in existing and ("手动" in existing or "确认" in existing):
            return {"success": True, "message": "规则已存在，无需添加"}
        
        # 添加规则
        rule_text = f"\n\n## {fix['rule']}\n"
        
        with open(target_file, 'a', encoding='utf-8') as f:
            f.write(rule_text)
        
        return {
            "success": True,
            "message": f"已在 {target_file.name} 中添加操作红线规则",
            "detail": f"添加内容: {fix['rule']}"
        }
    
    def _fix_env_file(self, fix: Dict) -> Dict:
        """修复：将 .env 添加到 .gitignore"""
        env_file = Path(fix['file_path'])
        gitignore = self.workspace_dir / ".gitignore"
        
        env_filename = env_file.name
        
        # 检查 .gitignore 是否存在
        if not gitignore.exists():
            with open(gitignore, 'w', encoding='utf-8') as f:
                f.write(f"# 敏感文件\n{env_filename}\n")
            return {
                "success": True,
                "message": f"已创建 .gitignore 并添加 {env_filename}",
                "detail": "敏感文件将被 Git 忽略"
            }
        
        # 检查是否已在 .gitignore 中
        with open(gitignore, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if env_filename in content:
            return {"success": True, "message": f"{env_filename} 已在 .gitignore 中"}
        
        # 添加到 .gitignore
        with open(gitignore, 'a', encoding='utf-8') as f:
            f.write(f"\n# 敏感文件\n{env_filename}\n")
        
        return {
            "success": True,
            "message": f"已将 {env_filename} 添加到 .gitignore",
            "detail": "敏感文件将被 Git 忽略"
        }
    
    def _fix_chmod(self, fix: Dict) -> Dict:
        """修复：修改目录权限"""
        path = Path(fix['path'])
        mode = fix['mode']
        
        os.chmod(path, int(mode, 8))
        
        return {
            "success": True,
            "message": f"已将 {path} 权限修改为 {mode}",
            "detail": "目录权限已收紧"
        }
    
    def _fix_env_var(self, fix: Dict) -> Dict:
        """修复：提示用户设置环境变量"""
        return {
            "success": False,
            "message": "需要手动设置环境变量",
            "detail": f"请在 shell 配置文件中添加:\n  export {fix['var_name']}='{fix['var_value']}'\n然后从 {fix['config_file']} 中删除 {fix['config_path']}"
        }
    
    def _fix_content_update(self, fix: Dict) -> Dict:
        """修复：内容更新（添加到 .gitignore）"""
        file_path = Path(fix['file_path'])
        gitignore = self.workspace_dir / ".gitignore"
        
        # 获取相对路径
        try:
            relative_path = file_path.relative_to(self.workspace_dir)
        except ValueError:
            relative_path = file_path.name
        
        # 检查 .gitignore 是否存在
        if not gitignore.exists():
            with open(gitignore, 'w', encoding='utf-8') as f:
                f.write(f"# 敏感文件\n{relative_path}\n")
            return {
                "success": True,
                "message": f"已创建 .gitignore 并添加 {relative_path}",
                "detail": "敏感文件将被 Git 忽略"
            }
        
        # 检查是否已在 .gitignore 中
        with open(gitignore, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if str(relative_path) in content or file_path.name in content:
            return {"success": True, "message": f"{relative_path} 已在 .gitignore 中"}
        
        # 添加到 .gitignore
        with open(gitignore, 'a', encoding='utf-8') as f:
            f.write(f"\n# 敏感文件\n{relative_path}\n")
        
        return {
            "success": True,
            "message": f"已将 {relative_path} 添加到 .gitignore",
            "detail": "敏感文件将被 Git 忽略"
        }
    
    def interactive_fix(self):
        """交互式修复流程"""
        if not self.findings:
            print("\n✅ 没有需要修复的问题")
            return
        
        # 找出可修复的问题
        fixable = [(i, f) for i, f in enumerate(self.findings) if f.get('auto_fix')]
        
        if not fixable:
            print("\n⚠️ 发现的问题都需要手动处理")
            return
        
        print("\n" + "=" * 70)
        print("🔧 开始交互式修复")
        print("=" * 70)
        
        for idx, finding in fixable:
            fix = finding['auto_fix']
            
            print(f"\n【问题 {idx + 1}】{finding['issue']}")
            print(f"风险等级: {finding['risk']}")
            print(f"详情: {finding['detail']}")
            print()
            
            # 显示修复方案
            print("📝 修复方案:")
            if fix['type'] == 'add_operation_rule':
                print(f"  在文件中添加规则: {fix['rule']}")
            elif fix['type'] == 'env_file':
                print(f"  将 {Path(fix['file_path']).name} 添加到 .gitignore")
            elif fix['type'] == 'chmod':
                print(f"  修改目录权限为 {fix['mode']}")
            elif fix['type'] == 'env_var':
                print(f"  设置环境变量（需要手动操作）")
            
            print()
            
            # 询问是否执行
            response = input("是否执行此修复? (y/n/skip/all): ").strip().lower()
            
            if response == 'y':
                result = self.execute_fix(idx)
                self.fix_results.append({
                    "index": idx,
                    "issue": finding['issue'],
                    "result": result
                })
                
                if result['success']:
                    print(f"✅ {result['message']}")
                else:
                    print(f"⚠️ {result['message']}")
                    if result.get('detail'):
                        print(f"   {result['detail']}")
            
            elif response == 'all':
                # 执行所有剩余修复
                for remaining_idx, remaining_finding in fixable:
                    if remaining_idx >= idx:
                        result = self.execute_fix(remaining_idx)
                        self.fix_results.append({
                            "index": remaining_idx,
                            "issue": remaining_finding['issue'],
                            "result": result
                        })
                        if result['success']:
                            print(f"✅ [{remaining_idx + 1}] {result['message']}")
                        else:
                            print(f"⚠️ [{remaining_idx + 1}] {result['message']}")
                break
            
            elif response == 'skip':
                print("⏭️ 跳过此问题")
            
            else:
                print("❌ 不执行修复")
        
        # 打印修复结果汇总
        self._print_fix_summary()
    
    def _print_fix_summary(self):
        """打印修复结果汇总"""
        if not self.fix_results:
            return
        
        print("\n" + "=" * 70)
        print("📋 修复结果汇总")
        print("=" * 70)
        
        success_count = sum(1 for r in self.fix_results if r['result']['success'])
        fail_count = len(self.fix_results) - success_count
        
        print(f"✅ 成功: {success_count} 项")
        if fail_count > 0:
            print(f"⚠️ 失败: {fail_count} 项")
        
        print()
        for r in self.fix_results:
            status = "✅" if r['result']['success'] else "⚠️"
            print(f"{status} [{r['index'] + 1}] {r['issue']}")
            print(f"   结果: {r['result']['message']}")
        
        print("\n" + "=" * 70)


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="OpenClaw 安全扫描器")
    parser.add_argument("--openclaw-dir", help="OpenClaw 目录路径")
    parser.add_argument("--workspace-dir", help="Workspace 目录路径")
    parser.add_argument("--json", action="store_true", help="输出 JSON 格式")
    parser.add_argument("--fix", type=int, help="修复指定编号的问题")
    parser.add_argument("--fix-all", action="store_true", help="自动修复所有可修复的问题")
    parser.add_argument("--interactive", "-i", action="store_true", help="交互式修复")
    
    args = parser.parse_args()
    
    scanner = SecurityScanner(
        openclaw_dir=args.openclaw_dir,
        workspace_dir=args.workspace_dir
    )
    
    report = scanner.scan_all()
    
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    elif args.fix is not None:
        result = scanner.execute_fix(args.fix)
        if result['success']:
            print(f"✅ {result['message']}")
        else:
            print(f"⚠️ {result['message']}")
            if result.get('detail'):
                print(f"   {result['detail']}")
    elif args.fix_all:
        # 自动修复所有可修复的问题
        fixable = [(i, f) for i, f in enumerate(scanner.findings) if f.get('auto_fix')]
        print(f"\n🔧 自动修复 {len(fixable)} 个问题...\n")
        for idx, finding in fixable:
            result = scanner.execute_fix(idx)
            status = "✅" if result['success'] else "⚠️"
            print(f"{status} [{idx + 1}] {finding['issue']}: {result['message']}")
    elif args.interactive:
        scanner.print_report(report)
        scanner.interactive_fix()
    else:
        scanner.print_report(report)
        # 检查是否有可修复的问题
        fixable = [f for f in scanner.findings if f.get('auto_fix')]
        if fixable:
            print(f"\n💡 发现 {len(fixable)} 个可修复的问题，运行以下命令进行交互式修复:")
            print(f"   python3 scripts/scan_security.py --interactive")
            print(f"\n   或自动修复所有问题:")
            print(f"   python3 scripts/scan_security.py --fix-all")


if __name__ == "__main__":
    main()