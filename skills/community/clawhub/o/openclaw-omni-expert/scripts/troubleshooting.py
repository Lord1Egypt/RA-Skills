#!/usr/bin/env python3
"""
OpenClaw 故障排查手册
THE TROUBLESHOOTING GUIDE - 全面的故障诊断与解决方案

作者：ProClaw
网站：www.ProClaw.top
联系方式：wechat:Mr-zifang

涵盖：
1. 安装部署故障
2. 配置故障
3. 运行故障
4. 性能故障
5. 网络故障
6. 安全故障
"""

import json
from typing import Dict, List, Optional, Any
from dataclasses import dataclass


# =============================================================================
# 故障分类
# =============================================================================

class IssueCategory(Enum):
    """故障分类"""
    INSTALLATION = "installation"      # 安装部署
    CONFIGURATION = "configuration"    # 配置问题
    RUNTIME = "runtime"                # 运行故障
    PERFORMANCE = "performance"       # 性能问题
    NETWORK = "network"               # 网络故障
    SECURITY = "security"             # 安全问题
    DATA = "data"                     # 数据问题


# =============================================================================
# 故障库
# =============================================================================

class TroubleshootingGuide:
    """完整故障排查手册"""

    # ========== 安装部署故障 ==========
    INSTALLATION_ISSUES = {
        "issue_001": {
            "id": "issue_001",
            "title": "Node.js 版本不兼容",
            "category": "installation",
            "severity": "critical",
            "symptoms": [
                "安装失败，报错 'Unsupported platform'",
                "npm install 报错",
                "启动时报错 'ENGINE_ERROR'"
            ],
            "causes": [
                "Node.js 版本低于 18 或高于 22",
                "使用了不兼容的 npm 版本",
                "系统缺少必要的编译工具"
            ],
            "diagnosis": [
                {"step": "检查 Node.js 版本", "command": "node --version"},
                {"step": "检查 npm 版本", "command": "npm --version"},
                {"step": "查看系统平台", "command": "uname -a"}
            ],
            "solutions": [
                {
                    "method": "安装正确的 Node.js 版本",
                    "steps": [
                        "卸载当前 Node.js: sudo apt remove nodejs",
                        "安装 nvm: curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash",
                        "安装 Node.js 22: nvm install 22",
                        "使用 Node.js 22: nvm use 22",
                        "验证: node --version"
                    ]
                },
                {
                    "method": "使用 Docker 部署",
                    "steps": [
                        "拉取镜像: docker pull node:22-alpine",
                        "运行容器: docker run -d -p 18789:18789 node:22-alpine",
                        "在容器内安装 OpenClaw"
                    ]
                }
            ],
            "prevention": "在安装前检查系统要求和 Node.js 版本兼容性",
            "references": []
        },
        "issue_002": {
            "id": "issue_002",
            "title": "权限不足导致安装失败",
            "category": "installation",
            "severity": "high",
            "symptoms": [
                "npm install 报错 'EACCES: permission denied'",
                "无法创建配置文件",
                "无法写入日志目录"
            ],
            "causes": [
                "以 root 用户运行 npm",
                "全局安装目录权限问题",
                "SELinux/AppArmor 限制"
            ],
            "solutions": [
                {
                    "method": "修复 npm 权限",
                    "steps": [
                        "创建 npm 配置目录: mkdir ~/.npm-global",
                        "配置 npm 使用新目录: npm config set prefix '~/.npm-global'",
                        "添加到 PATH: echo 'export PATH=~/.npm-global/bin:$PATH' >> ~/.bashrc",
                        "重新加载: source ~/.bashrc"
                    ]
                },
                {
                    "method": "使用 Yarn 替代",
                    "steps": [
                        "安装 Yarn: npm install -g yarn",
                        "使用 Yarn 安装: yarn global add openclaw"
                    ]
                }
            ]
        },
        "issue_003": {
            "id": "issue_003",
            "title": "网络问题导致安装失败",
            "category": "installation",
            "severity": "high",
            "symptoms": [
                "npm install 超时",
                "无法下载依赖包",
                "证书错误"
            ],
            "causes": [
                "网络代理配置问题",
                "国内网络访问 npm 源慢",
                "SSL 证书问题"
            ],
            "solutions": [
                {
                    "method": "切换到国内镜像源",
                    "steps": [
                        "设置淘宝镜像: npm config set registry https://registry.npmmirror.com",
                        "安装: npm install openclaw",
                        "验证源: npm config get registry"
                    ]
                },
                {
                    "method": "配置代理",
                    "steps": [
                        "设置 HTTP 代理: npm config set proxy http://proxy.example.com:8080",
                        "设置 HTTPS 代理: npm config set https-proxy http://proxy.example.com:8080"
                    ]
                }
            ]
        }
    }

    # ========== 配置故障 ==========
    CONFIGURATION_ISSUES = {
        "issue_101": {
            "id": "issue_101",
            "title": "API Key 无效或过期",
            "category": "configuration",
            "severity": "critical",
            "symptoms": [
                "API 调用返回 401 Unauthorized",
                "错误信息 'Invalid API key'",
                "请求被拒绝"
            ],
            "causes": [
                "API Key 填写错误",
                "API Key 已过期或被撤销",
                "Key 没有对应 API 的访问权限",
                "Key 被额度限制"
            ],
            "diagnosis": [
                {"step": "检查配置文件", "command": "cat ~/.openclaw/config.json | grep api_key"},
                {"step": "测试 API Key", "command": "curl -H 'Authorization: Bearer YOUR_KEY' https://api.openai.com/v1/models"},
                {"step": "检查 Key 状态", "action": "登录对应平台检查 Key 状态"}
            ],
            "solutions": [
                {
                    "method": "重新配置 API Key",
                    "steps": [
                        "登录 OpenAI/Anthropic 控制台",
                        "创建新的 API Key",
                        "更新配置文件 ~/.openclaw/config.json",
                        "重启 OpenClaw 服务",
                        "验证连接: openclaw config test-ai"
                    ]
                }
            ],
            "prevention": "定期检查 API Key 状态，设置额度提醒"
        },
        "issue_102": {
            "id": "issue_102",
            "title": "配置文件格式错误",
            "category": "configuration",
            "severity": "high",
            "symptoms": [
                "启动失败",
                "报错 'Invalid JSON' 或 'YAML syntax error'",
                "部分配置不生效"
            ],
            "causes": [
                "JSON 格式错误（逗号、引号等）",
                "YAML 缩进错误",
                "配置文件路径错误",
                "使用了不支持的配置项"
            ],
            "diagnosis": [
                {"step": "验证 JSON 格式", "command": "cat ~/.openclaw/config.json | python3 -m json.tool"},
                {"step": "验证 YAML 格式", "command": "cat ~/.openclaw/config.yaml | python3 -c 'import yaml; yaml.safe_load(open(\"config.yaml\"))'"},
                {"step": "检查配置文件路径", "command": "ls -la ~/.openclaw/"}
            ],
            "solutions": [
                {
                    "method": "重置配置文件",
                    "steps": [
                        "备份当前配置: cp ~/.openclaw/config.json ~/.openclaw/config.json.bak",
                        "删除损坏的配置: rm ~/.openclaw/config.json",
                        "重新生成: openclaw config init",
                        "按向导重新配置"
                    ]
                }
            ]
        },
        "issue_103": {
            "id": "issue_103",
            "title": "端口被占用",
            "category": "configuration",
            "severity": "medium",
            "symptoms": [
                "启动失败，报错 'Address already in use'",
                "无法访问 Web UI",
                "连接被拒绝"
            ],
            "causes": [
                "端口 18789 已被其他程序占用",
                "之前启动的 OpenClaw 未正常关闭",
                "多个 OpenClaw 实例冲突"
            ],
            "diagnosis": [
                {"step": "检查端口占用", "command": "lsof -i :18789 或 netstat -tlnp | grep 18789"},
                {"step": "检查 OpenClaw 进程", "command": "ps aux | grep openclaw"}
            ],
            "solutions": [
                {
                    "method": "停止占用进程",
                    "steps": [
                        "查找进程: lsof -ti :18789",
                        "终止进程: kill $(lsof -ti :18789)",
                        "或: pkill -f openclaw",
                        "重新启动: openclaw start"
                    ]
                },
                {
                    "method": "更换端口",
                    "config_change": {
                        "gateway": {"port": 18790}
                    }
                }
            ]
        }
    }

    # ========== 运行故障 ==========
    RUNTIME_ISSUES = {
        "issue_201": {
            "id": "issue_201",
            "title": "Gateway 无法启动",
            "category": "runtime",
            "severity": "critical",
            "symptoms": [
                "服务启动后立即退出",
                "健康检查失败",
                "日志显示 'Gateway startup failed'"
            ],
            "causes": [
                "配置文件错误",
                "端口被占用",
                "依赖服务未就绪",
                "内存不足"
            ],
            "diagnosis": [
                {"step": "查看详细日志", "command": "tail -100 ~/.openclaw/logs/openclaw.log"},
                {"step": "检查系统资源", "command": "free -h && df -h"},
                {"step": "检查依赖", "command": "openclaw health --verbose"}
            ],
            "solutions": [
                {
                    "method": "完整重启",
                    "steps": [
                        "停止服务: openclaw stop",
                        "清除临时文件: rm -rf ~/.openclaw/tmp/*",
                        "检查配置: openclaw config validate",
                        "重新启动: openclaw start",
                        "查看状态: openclaw status"
                    ]
                }
            ]
        },
        "issue_202": {
            "id": "issue_202",
            "title": "Agent 执行超时",
            "category": "runtime",
            "severity": "medium",
            "symptoms": [
                "Agent 任务长时间无响应",
                "报错 'Task timeout'",
                "请求被卡住"
            ],
            "causes": [
                "LLM API 响应慢",
                "工具执行时间过长",
                "网络延迟",
                "无限循环"
            ],
            "solutions": [
                {
                    "method": "优化超时配置",
                    "config_change": {
                        "agent": {
                            "timeout": 120,
                            "tool_timeout": 30
                        }
                    }
                },
                {
                    "method": "添加循环保护",
                    "config_change": {
                        "agent": {
                            "max_iterations": 10
                        }
                    }
                }
            ]
        },
        "issue_203": {
            "id": "issue_203",
            "title": "记忆数据丢失",
            "category": "runtime",
            "severity": "high",
            "symptoms": [
                "历史对话丢失",
                "上下文不连贯",
                "Agent 表现异常"
            ],
            "causes": [
                "向量数据库损坏",
                "磁盘空间不足",
                "配置被重置",
                "内存数据库未持久化"
            ],
            "diagnosis": [
                {"step": "检查向量数据库", "command": "ls -la ~/.openclaw/chroma/"},
                {"step": "检查磁盘空间", "command": "df -h ~/.openclaw"}
            ],
            "solutions": [
                {
                    "method": "恢复记忆备份",
                    "steps": [
                        "停止服务: openclaw stop",
                        "恢复备份: cp -r ~/.openclaw/backups/chroma/* ~/.openclaw/chroma/",
                        "重启服务: openclaw start"
                    ]
                }
            ]
        },
        "issue_204": {
            "id": "issue_204",
            "title": "工具调用失败",
            "category": "runtime",
            "severity": "medium",
            "symptoms": [
                "特定工具无法调用",
                "报错 'Tool not found'",
                "工具返回错误"
            ],
            "causes": [
                "工具未注册",
                "工具配置错误",
                "工具依赖缺失",
                "API Key 权限不足"
            ],
            "diagnosis": [
                {"step": "列出已注册工具", "command": "openclaw tools list"},
                {"step": "测试工具", "command": "openclaw tools test <tool_name>"}
            ],
            "solutions": [
                {
                    "method": "重新注册工具",
                    "steps": [
                        "编辑配置: openclaw config edit",
                        "添加工具配置",
                        "重启服务"
                    ]
                }
            ]
        }
    }

    # ========== 性能故障 ==========
    PERFORMANCE_ISSUES = {
        "issue_301": {
            "id": "issue_301",
            "title": "响应延迟过高",
            "category": "performance",
            "severity": "medium",
            "symptoms": [
                "API 响应时间 > 5 秒",
                "用户体验差",
                "超时错误增加"
            ],
            "causes": [
                "模型推理慢",
                "向量检索效率低",
                "网络延迟",
                "系统负载高"
            ],
            "diagnosis": [
                {"step": "分析响应时间分布", "command": "openclaw metrics latency"},
                {"step": "检查系统负载", "command": "top -bn1 | head -20"},
                {"step": "分析慢查询", "command": "openclaw logs --filter slow"}
            ],
            "solutions": [
                {
                    "method": "启用缓存",
                    "config_change": {
                        "cache": {
                            "enabled": True,
                            "ttl": 3600
                        }
                    }
                },
                {
                    "method": "优化向量检索",
                    "config_change": {
                        "memory": {
                            "vector": {
                                "ef_search": 100,
                                "hnsw_M": 16
                            }
                        }
                    }
                },
                {
                    "method": "使用更快的模型",
                    "config_change": {
                        "model": {"model": "gpt-4o-mini"}
                    }
                }
            ]
        },
        "issue_302": {
            "id": "issue_302",
            "title": "内存使用过高",
            "category": "performance",
            "severity": "high",
            "symptoms": [
                "系统内存接近耗尽",
                "出现 OOM",
                "性能急剧下降"
            ],
            "causes": [
                "向量数据过大",
                "上下文过长",
                "内存泄漏",
                "系统资源不足"
            ],
            "diagnosis": [
                {"step": "检查内存使用", "command": "free -h"},
                {"step": "分析 OpenClaw 内存", "command": "ps aux | grep openclaw"},
                {"step": "检查向量数据", "command": "du -sh ~/.openclaw/chroma/"}
            ],
            "solutions": [
                {
                    "method": "清理向量数据",
                    "steps": [
                        "删除旧数据: openclaw memory cleanup --older-than 30d",
                        "优化索引: openclaw memory optimize"
                    ]
                },
                {
                    "method": "限制上下文长度",
                    "config_change": {
                        "agent": {
                            "max_context_tokens": 32000
                        }
                    }
                }
            ]
        },
        "issue_303": {
            "id": "issue_303",
            "title": "CPU 使用率过高",
            "category": "performance",
            "severity": "medium",
            "symptoms": [
                "CPU 持续 100%",
                "系统响应慢",
                "风扇高速运转"
            ],
            "causes": [
                "并发请求过多",
                "后台任务占用高",
                "索引构建",
                "攻击/滥用"
            ],
            "solutions": [
                {
                    "method": "限制并发",
                    "config_change": {
                        "gateway": {
                            "rate_limit": {
                                "enabled": True,
                                "requests_per_minute": 60
                            }
                        }
                    }
                }
            ]
        }
    }

    # ========== 网络故障 ==========
    NETWORK_ISSUES = {
        "issue_401": {
            "id": "issue_401",
            "title": "无法连接外部 API",
            "category": "network",
            "severity": "critical",
            "symptoms": [
                "API 调用超时",
                "连接被拒绝",
                "SSL 错误"
            ],
            "causes": [
                "网络隔离",
                "代理配置错误",
                "防火墙阻止",
                "DNS 解析失败"
            ],
            "diagnosis": [
                {"step": "测试网络连通性", "command": "curl -v https://api.openai.com"},
                {"step": "检查 DNS", "command": "nslookup api.openai.com"},
                {"step": "检查防火墙", "command": "sudo iptables -L"}
            ],
            "solutions": [
                {
                    "method": "配置代理",
                    "config_change": {
                        "proxy": {
                            "http": "http://proxy:8080",
                            "https": "http://proxy:8080"
                        }
                    }
                }
            ]
        },
        "issue_402": {
            "id": "issue_402",
            "title": "Webhook 无法接收",
            "category": "network",
            "severity": "medium",
            "symptoms": [
                "Webhook 无响应",
                "消息接收失败",
                "回调超时"
            ],
            "causes": [
                "公网 IP 未配置",
                "防火墙阻止入站",
                "SSL 证书无效",
                "URL 配置错误"
            ],
            "solutions": [
                {
                    "method": "配置公网访问",
                    "steps": [
                        "获取公网 IP",
                        "配置防火墙: sudo ufw allow 80/tcp",
                        "配置 SSL 证书",
                        "更新 Webhook URL"
                    ]
                }
            ]
        }
    }

    # ========== 安全故障 ==========
    SECURITY_ISSUES = {
        "issue_501": {
            "id": "issue_501",
            "title": "API Key 泄露",
            "category": "security",
            "severity": "critical",
            "symptoms": [
                "异常 API 调用",
                "额度异常消耗",
                "未经授权的请求"
            ],
            "causes": [
                "配置文件权限过宽",
                "日志中记录了敏感信息",
                "代码仓库泄露",
                "网络被入侵"
            ],
            "solutions": [
                {
                    "method": "紧急处理",
                    "steps": [
                        "立即撤销泄露的 API Key",
                        "生成新的 API Key",
                        "更新所有配置文件",
                        "检查使用记录"
                    ]
                },
                {
                    "method": "安全加固",
                    "steps": [
                        "限制配置文件权限: chmod 600 ~/.openclaw/config.json",
                        "使用环境变量存储敏感信息",
                        "启用审计日志",
                        "配置 IP 白名单"
                    ]
                }
            ]
        },
        "issue_502": {
            "id": "issue_502",
            "title": "未授权访问",
            "category": "security",
            "severity": "critical",
            "symptoms": [
                "未预期的请求",
                "配置被篡改",
                "异常的管理员操作"
            ],
            "causes": [
                "未启用认证",
                "弱密码",
                "JWT 密钥泄露",
                "会话被劫持"
            ],
            "solutions": [
                {
                    "method": "启用认证",
                    "config_change": {
                        "authentication": {
                            "enabled": True,
                            "jwt_secret": "生成随机密钥",
                            "token_expiry": "1h"
                        }
                    }
                }
            ]
        }
    }

    # ========== 数据故障 ==========
    DATA_ISSUES = {
        "issue_601": {
            "id": "issue_601",
            "title": "数据库损坏",
            "category": "data",
            "severity": "critical",
            "symptoms": [
                "检索结果错误",
                "无法写入数据",
                "数据库报错"
            ],
            "causes": [
                "磁盘故障",
                "不正常关机",
                "并发写入冲突",
                "存储空间耗尽"
            ],
            "diagnosis": [
                {"step": "检查数据库状态", "command": "openclaw db check"},
                {"step": "检查磁盘健康", "command": "smartctl -a /dev/sda"}
            ],
            "solutions": [
                {
                    "method": "从备份恢复",
                    "steps": [
                        "停止服务: openclaw stop",
                        "备份损坏数据: mv ~/.openclaw/chroma ~/.openclaw/chroma.bak",
                        "恢复备份: cp -r ~/.openclaw/backups/chroma ~/.openclaw/",
                        "重启服务: openclaw start"
                    ]
                }
            ]
        },
        "issue_602": {
            "id": "issue_602",
            "title": "存储空间不足",
            "category": "data",
            "severity": "high",
            "symptoms": [
                "写入失败",
                "服务无响应",
                "报错 'No space left'"
            ],
            "solutions": [
                {
                    "method": "清理空间",
                    "steps": [
                        "清理日志: rm -rf ~/.openclaw/logs/*.log",
                        "清理临时文件: rm -rf ~/.openclaw/tmp/*",
                        "清理旧备份: openclaw backup cleanup --keep 3"
                    ]
                }
            ]
        }
    }

    @classmethod
    def get_all_issues(cls) -> Dict[str, Dict]:
        """获取所有故障"""
        all_issues = {}
        for category_issues in [
            cls.INSTALLATION_ISSUES,
            cls.CONFIGURATION_ISSUES,
            cls.RUNTIME_ISSUES,
            cls.PERFORMANCE_ISSUES,
            cls.NETWORK_ISSUES,
            cls.SECURITY_ISSUES,
            cls.DATA_ISSUES
        ]:
            all_issues.update(category_issues)
        return all_issues

    @classmethod
    def get_issues_by_category(cls, category: str) -> Dict[str, Dict]:
        """按分类获取故障"""
        category_map = {
            "installation": cls.INSTALLATION_ISSUES,
            "configuration": cls.CONFIGURATION_ISSUES,
            "runtime": cls.RUNTIME_ISSUES,
            "performance": cls.PERFORMANCE_ISSUES,
            "network": cls.NETWORK_ISSUES,
            "security": cls.SECURITY_ISSUES,
            "data": cls.DATA_ISSUES
        }
        return category_map.get(category, {})

    @classmethod
    def search_issues(cls, query: str) -> List[Dict]:
        """搜索故障"""
        results = []
        query_lower = query.lower()
        
        for issue in cls.get_all_issues().values():
            if (query_lower in issue.get("title", "").lower() or
                query_lower in str(issue.get("symptoms", [])).lower()):
                results.append(issue)
        
        return results


# =============================================================================
# 故障排查专家系统
# =============================================================================

class TroubleshootingExpert:
    """
    故障排查专家
    
    提供故障诊断和解决方案服务
    """

    def __init__(self):
        self.guide = TroubleshootingGuide()

    def diagnose(
        self,
        symptom: str,
        category: str = None
    ) -> List[Dict]:
        """
        根据症状诊断问题
        
        Args:
            symptom: 错误信息或症状描述
            category: 可选的分类限定
        """
        # 搜索匹配的故障
        issues = self.guide.search_issues(symptom)
        
        # 如果指定了分类，过滤结果
        if category:
            category_issues = self.guide.get_issues_by_category(category)
            issues = [i for i in issues if i["id"] in category_issues]
        
        return issues

    def get_solution(
        self,
        issue_id: str,
        method_index: int = 0
    ) -> Optional[Dict]:
        """
        获取解决方案
        
        Args:
            issue_id: 故障 ID
            method_index: 解决方案索引
        """
        issue = self.guide.get_all_issues().get(issue_id)
        if not issue:
            return None
        
        solutions = issue.get("solutions", [])
        if method_index < len(solutions):
            return solutions[method_index]
        
        return None

    def auto_fix(
        self,
        issue_id: str
    ) -> List[str]:
        """
        自动修复步骤
        
        Returns:
            修复命令列表
        """
        issue = self.guide.get_all_issues().get(issue_id)
        if not issue:
            return []
        
        commands = []
        for solution in issue.get("solutions", []):
            for step in solution.get("steps", []):
                if isinstance(step, str) and step.startswith("$"):
                    commands.append(step)
                elif isinstance(step, str):
                    commands.append(step)
        
        return commands

    def generate_report(
        self,
        symptom: str,
        diagnosis_result: List[Dict]
    ) -> str:
        """生成诊断报告"""
        report = f"""
# 故障诊断报告

## 症状
{symptom}

## 诊断结果

"""
        for i, issue in enumerate(diagnosis_result, 1):
            report += f"""
### 可能原因 {i}: {issue['title']}
- 严重程度: {issue['severity']}
- 分类: {issue['category']}

**可能原因:**
"""
            for cause in issue.get("causes", []):
                report += f"- {cause}\n"
            
            report += "\n**排查步骤:**\n"
            for diag in issue.get("diagnosis", []):
                if "command" in diag:
                    report += f"- {diag['step']}: `{diag['command']}`\n"
                else:
                    report += f"- {diag['step']}\n"
            
            report += "\n**解决方案:**\n"
            for j, solution in enumerate(issue.get("solutions", []), 1):
                report += f"{j}. **{solution.get('method', '方法')}**\n"
                for step in solution.get("steps", []):
                    report += f"   - {step}\n"
        
        return report


# =============================================================================
# 主函数
# =============================================================================

def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="OpenClaw 故障排查手册 v5.0"
    )

    # 查询
    parser.add_argument("--list", action="store_true", help="列出所有故障")
    parser.add_argument("--category", help="按分类筛选")
    parser.add_argument("--search", help="搜索故障")
    parser.add_argument("--issue-id", help="获取故障详情")
    parser.add_argument("--severity", choices=["critical", "high", "medium", "low"],
                       help="按严重程度筛选")

    # 诊断
    parser.add_argument("--diagnose", help="根据症状诊断")
    parser.add_argument("--fix", help="获取自动修复命令")

    # 报告
    parser.add_argument("--report", help="生成诊断报告")
    parser.add_argument("--output", "-o", help="输出文件路径")

    args = parser.parse_args()

    expert = TroubleshootingExpert()

    if args.list:
        issues = expert.guide.get_all_issues()
        for issue in issues.values():
            severity_icon = {"critical": "🔴", "high": "🟠", "medium": "🟡"}.get(issue["severity"], "⚪")
            print(f"{severity_icon} {issue['id']}: {issue['title']} [{issue['category']}]")

    elif args.category:
        issues = expert.guide.get_issues_by_category(args.category)
        for issue in issues.values():
            print(json.dumps(issue, indent=2, ensure_ascii=False))

    elif args.search:
        results = expert.search_issues(args.search)
        print(json.dumps(results, indent=2, ensure_ascii=False))

    elif args.issue_id:
        issue = expert.guide.get_all_issues().get(args.issue_id)
        if issue:
            print(json.dumps(issue, indent=2, ensure_ascii=False))
        else:
            print("故障不存在")

    elif args.diagnose:
        results = expert.diagnose(args.diagnose)
        report = expert.generate_report(args.diagnose, results)
        
        if args.output:
            Path(args.output).write_text(report)
            print(f"诊断报告已保存: {args.output}")
        else:
            print(report)

    elif args.fix:
        commands = expert.auto_fix(args.fix)
        print("自动修复命令:")
        for cmd in commands:
            print(f"  {cmd}")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
