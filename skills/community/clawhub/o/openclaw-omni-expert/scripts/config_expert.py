#!/usr/bin/env python3
"""
OpenClaw 配置专家系统 v5.0
THE CONFIGURATION EXPERT - 全面深度专业的配置系统

作者：ProClaw
网站：www.ProClaw.top
联系方式：wechat:Mr-zifang

支持：
1. AI 模型配置（OpenAI/Claude/DeepSeek/通义千问/Ollama等）
2. 通讯渠道配置（Telegram/Discord/飞书/企业微信等）
3. 网关配置（本地/远程/高可用）
4. 高级配置（记忆/插件/认证/日志）

配置即代码，专业可复用。
"""

import os
import sys
import json
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime
from dataclasses import dataclass
import copy


# =============================================================================
# 配置模板库
# =============================================================================

class ConfigTemplates:
    """配置模板库"""

    # OpenClaw 配置文件结构
    BASE_CONFIG = {
        "version": "1.0",
        "openclaw": {
            "data_dir": "~/.openclaw",
            "log_dir": "~/.openclaw/logs",
            "plugin_dir": "~/.openclaw/plugins"
        }
    }

    # AI 模型提供商配置模板
    AI_MODEL_TEMPLATES = {
        "openai": {
            "name": "OpenAI",
            "models": ["gpt-4o", "gpt-4o-mini", "gpt-4-turbo", "gpt-4", "gpt-3.5-turbo"],
            "config": {
                "provider": "openai",
                "model": "gpt-4o",
                "api_base": "https://api.openai.com/v1",
                "temperature": 0.7,
                "max_tokens": 4096
            },
            "setup_guide": {
                "step1": "访问 https://platform.openai.com/api-keys",
                "step2": "登录账号并创建新的 API Key",
                "step3": "复制 API Key 并妥善保存",
                "step4": "在配置中填入 API Key"
            },
            "best_for": "通用对话、代码生成、创意写作",
            "pricing": "按 token 计费，GPT-4o 性价比高"
        },
        "anthropic": {
            "name": "Anthropic Claude",
            "models": ["claude-sonnet-4-20250514", "claude-3-5-sonnet-20241022", "claude-3-opus", "claude-3-haiku"],
            "config": {
                "provider": "anthropic",
                "model": "claude-sonnet-4-20250514",
                "api_base": "https://api.anthropic.com/v1",
                "temperature": 0.7,
                "max_tokens": 4096
            },
            "setup_guide": {
                "step1": "访问 https://console.anthropic.com/",
                "step2": "注册并登录 Anthropic Console",
                "step3": "进入 API Keys 页面创建密钥",
                "step4": "在配置中填入 API Key"
            },
            "best_for": "长文本分析、复杂推理、代码审查",
            "pricing": "按 token 计费，Claude 3.5 Sonnet 性价比高"
        },
        "deepseek": {
            "name": "DeepSeek",
            "models": ["deepseek-chat", "deepseek-coder"],
            "config": {
                "provider": "deepseek",
                "model": "deepseek-chat",
                "api_base": "https://api.deepseek.com/v1",
                "temperature": 0.7,
                "max_tokens": 4096
            },
            "setup_guide": {
                "step1": "访问 https://platform.deepseek.com/",
                "step2": "注册并登录",
                "step3": "在 API Keys 页面创建密钥",
                "step4": "在配置中填入 API Key"
            },
            "best_for": "代码生成、数学推理、中文对话",
            "pricing": "价格较低，DeepSeek Coder 代码能力强"
        },
        "qwen": {
            "name": "阿里通义千问",
            "models": ["qwen-turbo", "qwen-plus", "qwen-max"],
            "config": {
                "provider": "qwen",
                "model": "qwen-plus",
                "api_base": "https://dashscope.aliyuncs.com/compatible-mode/v1",
                "api_key": "",  # 需要用户填入
                "temperature": 0.7,
                "max_tokens": 4096
            },
            "setup_guide": {
                "step1": "访问 https://dashscope.console.aliyun.com/",
                "step2": "注册阿里云账号并开通 DashScope",
                "step3": "在 API-KEY 管理页面创建密钥",
                "step4": "在配置中填入 API Key"
            },
            "best_for": "中文对话、阿里生态集成",
            "pricing": "有免费额度，qwen-plus 性能强"
        },
        "ollama": {
            "name": "Ollama (本地模型)",
            "models": ["llama3.3", "qwen2.5", "codellama", "mistral", "neural-chat"],
            "config": {
                "provider": "ollama",
                "model": "llama3.3",
                "api_base": "http://localhost:11434/v1",
                "temperature": 0.7,
                "max_tokens": 4096
            },
            "setup_guide": {
                "step1": "安装 Ollama: curl -fsSL https://ollama.com/install.sh | sh",
                "step2": "拉取模型: ollama pull llama3.3",
                "step3": "启动 Ollama 服务: ollama serve",
                "step4": "配置中使用 http://localhost:11434"
            },
            "best_for": "隐私敏感场景、无网络环境、完全离线",
            "pricing": "免费，但需要本地 GPU"
        },
        "azure": {
            "name": "Azure OpenAI",
            "models": ["gpt-4o", "gpt-4-turbo", "gpt-35-turbo"],
            "config": {
                "provider": "azure",
                "api_base": "",  # 需要填入 Azure 端点
                "api_key": "",   # 需要填入 Azure API Key
                "api_version": "2024-02-01",
                "deployment_name": "",  # 需要填入部署名称
                "temperature": 0.7,
                "max_tokens": 4096
            },
            "setup_guide": {
                "step1": "访问 Azure Portal 并创建 Azure OpenAI 资源",
                "step2": "在 Azure OpenAI Studio 部署模型",
                "step3": "获取端点 URL 和 API Key",
                "step4": "填入配置中的 api_base 和 deployment_name"
            },
            "best_for": "企业环境、合规要求、Azure 生态",
            "pricing": "企业定价，有 SLA 保障"
        },
        "gemini": {
            "name": "Google Gemini",
            "models": ["gemini-2.0-flash-exp", "gemini-1.5-pro", "gemini-1.5-flash"],
            "config": {
                "provider": "gemini",
                "model": "gemini-1.5-pro",
                "api_base": "https://generativelanguage.googleapis.com/v1beta",
                "api_key": "",  # 需要用户填入
                "temperature": 0.7,
                "max_tokens": 4096
            },
            "setup_guide": {
                "step1": "访问 https://aistudio.google.com/",
                "step2": "登录 Google 账号",
                "step3": "在 API Keys 页面创建密钥",
                "step4": "在配置中填入 API Key"
            },
            "best_for": "多模态处理、Google 生态集成",
            "pricing": "有免费额度，Gemini 1.5 Flash 免费用量大"
        }
    }

    # 通讯渠道配置模板
    CHANNEL_TEMPLATES = {
        "telegram": {
            "name": "Telegram",
            "required_fields": ["bot_token"],
            "config": {
                "enabled": True,
                "type": "telegram",
                "bot_token": "",  # 需要填入
                "chat_ids": [],   # 允许的聊天 ID 列表
                "allow_groups": False,
                "allow_private": True,
                "commands": ["/start", "/help", "/status"]
            },
            "setup_guide": {
                "step1": "在 Telegram 中搜索 @BotFather",
                "step2": "发送 /newbot 创建新机器人",
                "step3": "获取 Bot Token",
                "step4": "（可选）将机器人添加到群组，发送 /start 获取群组 ID"
            },
            "webhook_guide": "Telegram 使用轮询或 Webhook 接收消息，推荐 Webhook",
            "best_for": "私聊、群组管理、通知推送"
        },
        "discord": {
            "name": "Discord",
            "required_fields": ["bot_token", "guild_id", "channel_id"],
            "config": {
                "enabled": True,
                "type": "discord",
                "bot_token": "",  # 需要填入
                "guild_id": "",   # 服务器 ID
                "channel_ids": [],  # 频道 ID 列表
                "intents": ["message_content", "guild_messages"],
                "command_prefix": "!"
            },
            "setup_guide": {
                "step1": "访问 https://discord.com/developers/applications",
                "step2": "创建新 Application",
                "step3": "在 Bot 页面创建 Bot 并获取 Token",
                "step4": "在 OAuth2 URL Generator 中添加 bot 权限",
                "step5": "使用生成的链接邀请 Bot 到服务器"
            },
            "best_for": "社区运营、游戏集成、语音交互"
        },
        "feishu": {
            "name": "飞书",
            "required_fields": ["app_id", "app_secret"],
            "config": {
                "enabled": True,
                "type": "feishu",
                "app_id": "",      # 应用 ID
                "app_secret": "",  # 应用密钥
                "bot_name": "OpenClaw Bot",
                "event_subscription": True,
                "encrypt_key": "",  # 可选，加密密钥
                "verification_token": ""  # 可选，验证 Token
            },
            "setup_guide": {
                "step1": "访问 https://open.feishu.cn/app",
                "step2": "创建企业自建应用",
                "step3": "获取 App ID 和 App Secret",
                "step4": "在应用功能中开启机器人能力",
                "step5": "配置消息事件订阅"
            },
            "best_for": "企业内部协作、飞书生态集成"
        },
        "wecom": {
            "name": "企业微信",
            "required_fields": ["corp_id", "corp_secret", "agent_id"],
            "config": {
                "enabled": True,
                "type": "wecom",
                "corp_id": "",      # 企业 ID
                "corp_secret": "",  # 应用密钥
                "agent_id": "",     # 应用 AgentID
                "api_base": "https://qyapi.weixin.qq.com",
                "webhook_url": ""   # 可选，群机器人 Webhook
            },
            "setup_guide": {
                "step1": "登录企业微信管理后台",
                "step2": "创建自建应用，获取 AgentID 和 Secret",
                "step3": "获取企业 ID",
                "step4": "配置应用权限和可见范围"
            },
            "best_for": "企业微信生态、客户服务"
        },
        "slack": {
            "name": "Slack",
            "required_fields": ["bot_token", "app_token"],
            "config": {
                "enabled": True,
                "type": "slack",
                "bot_token": "",     # xoxb-... Token
                "app_token": "",     # xapp-... Token
                "team_id": "",
                "channels": [],      # 允许的频道 ID
                "command_prefix": "/"
            },
            "setup_guide": {
                "step1": "访问 https://api.slack.com/apps",
                "step2": "创建新 Slack App",
                "step3": "添加 Bot User 和 Bot Token Scopes",
                "step4": "安装应用到工作区获取 Bot Token",
                "step5": "（可选）启用 Socket Mode 获取 App Token"
            },
            "best_for": "团队协作、开发者集成"
        },
        "webhook": {
            "name": "自定义 Webhook",
            "required_fields": ["url"],
            "config": {
                "enabled": True,
                "type": "webhook",
                "url": "",           # Webhook URL
                "method": "POST",
                "headers": {},
                "template": {
                    "msg_type": "text",
                    "content": "{{message}}"
                }
            },
            "setup_guide": {
                "step1": "获取目标平台的 Webhook URL",
                "step2": "配置请求方法和请求头",
                "step3": "定义消息模板"
            },
            "best_for": "对接任意支持 Webhook 的平台"
        }
    }

    # 网关配置模板
    GATEWAY_TEMPLATES = {
        "local": {
            "name": "本地网关",
            "description": "在本地机器上运行 OpenClaw Gateway",
            "config": {
                "gateway": {
                    "host": "127.0.0.1",
                    "port": 18789,
                    "ssl": {
                        "enabled": False,
                        "cert_file": "",
                        "key_file": ""
                    },
                    "cors": {
                        "enabled": True,
                        "origins": ["http://localhost:3000"]
                    },
                    "rate_limit": {
                        "enabled": True,
                        "requests_per_minute": 60
                    }
                }
            },
            "best_for": "个人使用、开发测试"
        },
        "remote": {
            "name": "远程网关",
            "description": "在远程服务器上运行，可被多个客户端访问",
            "config": {
                "gateway": {
                    "host": "0.0.0.0",
                    "port": 18789,
                    "ssl": {
                        "enabled": True,
                        "cert_file": "/path/to/cert.pem",
                        "key_file": "/path/to/key.pem"
                    },
                    "cors": {
                        "enabled": True,
                        "origins": ["https://your-domain.com"]
                    },
                    "authentication": {
                        "enabled": True,
                        "jwt_secret": "",  # 需要填入
                        "token_expiry": "24h"
                    },
                    "rate_limit": {
                        "enabled": True,
                        "requests_per_minute": 120
                    }
                }
            },
            "best_for": "团队共享、公网访问"
        },
        "high_availability": {
            "name": "高可用配置",
            "description": "多实例部署，支持负载均衡和故障转移",
            "config": {
                "gateway": {
                    "cluster": {
                        "enabled": True,
                        "nodes": [
                            {"host": "node1.example.com", "port": 18789},
                            {"host": "node2.example.com", "port": 18789}
                        ],
                        "strategy": "round_robin",
                        "health_check_interval": 30
                    },
                    "ssl": {
                        "enabled": True,
                        "cert_file": "/path/to/cert.pem",
                        "key_file": "/path/to/key.pem"
                    },
                    "load_balancer": {
                        "enabled": True,
                        "health_check_path": "/api/health"
                    }
                }
            },
            "best_for": "生产环境、企业部署"
        }
    }

    # 记忆系统配置模板
    MEMORY_TEMPLATES = {
        "basic": {
            "name": "基础记忆",
            "description": "简单的上下文记忆，自动管理对话历史",
            "config": {
                "memory": {
                    "enabled": True,
                    "type": "basic",
                    "max_history": 100,
                    "summary_enabled": True,
                    "summary_threshold": 50
                }
            }
        },
        "vector": {
            "name": "向量记忆",
            "description": "基于向量数据库的记忆系统，支持语义检索",
            "config": {
                "memory": {
                    "enabled": True,
                    "type": "vector",
                    "provider": "chroma",  # chroma / qdrant / milvus
                    "chroma": {
                        "persist_directory": "~/.openclaw/chroma",
                        "collection_name": "openclaw_memory",
                        "embedding_model": "text-embedding-3-small"
                    }
                }
            },
            "setup_guide": {
                "step1": "安装 Chroma: pip install chromadb",
                "step2": "配置持久化目录",
                "step3": "设置 embedding 模型"
            }
        },
        "graph": {
            "name": "知识图谱记忆",
            "description": "基于知识图谱的记忆系统，支持复杂关系推理",
            "config": {
                "memory": {
                    "enabled": True,
                    "type": "graph",
                    "provider": "networkx",  # networkx / neo4j
                    "graph": {
                        "persist_file": "~/.openclaw/knowledge_graph.gpickle",
                        "max_nodes": 10000,
                        "inference_depth": 3
                    }
                }
            }
        }
    }


# =============================================================================
# 配置生成器
# =============================================================================

class ConfigGenerator:
    """配置生成器"""

    def __init__(self):
        self.templates = ConfigTemplates()

    def generate_complete_config(
        self,
        ai_provider: str,
        ai_api_key: str,
        channels: List[Dict] = None,
        gateway_mode: str = "local",
        memory_type: str = "basic",
        extra_config: Dict = None
    ) -> Dict:
        """
        生成完整配置

        Args:
            ai_provider: AI 模型提供商
            ai_api_key: API Key
            channels: 通讯渠道配置列表
            gateway_mode: 网关模式
            memory_type: 记忆类型
            extra_config: 额外配置
        """
        config = copy.deepcopy(self.templates.BASE_CONFIG)

        # AI 模型配置
        ai_config = self._generate_ai_config(ai_provider, ai_api_key)
        config["model"] = ai_config

        # 通讯渠道配置
        if channels:
            config["channels"] = self._generate_channels_config(channels)
        else:
            config["channels"] = []

        # 网关配置
        gateway_config = self._generate_gateway_config(gateway_mode)
        config["gateway"] = gateway_config

        # 记忆系统配置
        memory_config = self._generate_memory_config(memory_type)
        config["memory"] = memory_config

        # 额外配置
        if extra_config:
            config.update(extra_config)

        return config

    def _generate_ai_config(self, provider: str, api_key: str) -> Dict:
        """生成 AI 配置"""
        if provider not in self.templates.AI_MODEL_TEMPLATES:
            raise ValueError(f"不支持的 AI 提供商: {provider}")

        template = self.templates.AI_MODEL_TEMPLATES[provider]
        config = copy.deepcopy(template["config"])
        config["api_key"] = api_key

        return config

    def _generate_channels_config(self, channels: List[Dict]) -> List[Dict]:
        """生成通讯渠道配置"""
        result = []

        for channel in channels:
            channel_type = channel.get("type")
            if channel_type not in self.templates.CHANNEL_TEMPLATES:
                continue

            template = self.templates.CHANNEL_TEMPLATES[channel_type]
            config = copy.deepcopy(template["config"])

            # 合并用户提供的配置
            for key, value in channel.items():
                if value is not None:
                    config[key] = value

            result.append(config)

        return result

    def _generate_gateway_config(self, mode: str) -> Dict:
        """生成网关配置"""
        if mode not in self.templates.GATEWAY_TEMPLATES:
            mode = "local"

        template = self.templates.GATEWAY_TEMPLATES[mode]
        return copy.deepcopy(template["config"])

    def _generate_memory_config(self, memory_type: str) -> Dict:
        """生成记忆系统配置"""
        if memory_type not in self.templates.MEMORY_TEMPLATES:
            memory_type = "basic"

        template = self.templates.MEMORY_TEMPLATES[memory_type]
        return copy.deepcopy(template["config"])

    def validate_config(self, config: Dict) -> Tuple[bool, List[str]]:
        """
        验证配置

        Returns:
            (is_valid, error_messages)
        """
        errors = []

        # 验证 AI 配置
        if "model" not in config:
            errors.append("缺少 AI 模型配置")
        else:
            model = config["model"]
            if "provider" not in model:
                errors.append("AI 配置缺少 provider 字段")
            if "api_key" not in model or not model["api_key"]:
                errors.append("AI 配置缺少 api_key")

        # 验证网关配置
        if "gateway" in config:
            gw = config["gateway"]
            if "port" not in gw:
                errors.append("网关配置缺少 port")
            elif not isinstance(gw["port"], int):
                errors.append("网关端口必须是数字")

        # 验证渠道配置
        if "channels" in config:
            for i, channel in enumerate(config["channels"]):
                required = ["type"]
                for field in required:
                    if field not in channel:
                        errors.append(f"渠道 {i} 缺少 {field} 字段")

        return len(errors) == 0, errors


# =============================================================================
# 配置专家系统
# =============================================================================

class OpenClawConfigExpert:
    """
    OpenClaw 配置专家系统

    提供专业级的配置咨询和生成服务
    """

    def __init__(self):
        self.templates = ConfigTemplates()
        self.generator = ConfigGenerator()

    def get_ai_provider_info(self, provider: str = None) -> Dict:
        """获取 AI 提供商信息"""
        if provider:
            return self.templates.AI_MODEL_TEMPLATES.get(provider, {})
        else:
            # 返回所有提供商
            return {
                key: {
                    "name": val["name"],
                    "models": val["models"],
                    "best_for": val["best_for"],
                    "pricing": val["pricing"]
                }
                for key, val in self.templates.AI_MODEL_TEMPLATES.items()
            }

    def get_channel_info(self, channel_type: str = None) -> Dict:
        """获取通讯渠道信息"""
        if channel_type:
            return self.templates.CHANNEL_TEMPLATES.get(channel_type, {})
        else:
            return {
                key: {
                    "name": val["name"],
                    "required_fields": val["required_fields"],
                    "best_for": val["best_for"]
                }
                for key, val in self.templates.CHANNEL_TEMPLATES.items()
            }

    def recommend_config(self, use_case: str) -> Dict:
        """
        根据使用场景推荐配置

        Args:
            use_case: 使用场景
                - "personal": 个人使用
                - "team": 团队协作
                - "enterprise": 企业部署
                - "development": 开发测试
        """
        recommendations = {
            "personal": {
                "ai_provider": "openai",
                "ai_model": "gpt-4o-mini",
                "gateway_mode": "local",
                "memory_type": "basic",
                "channels": ["telegram"],
                "reason": "性价比最高，适合个人日常使用"
            },
            "team": {
                "ai_provider": "anthropic",
                "ai_model": "claude-3-5-sonnet-20241022",
                "gateway_mode": "remote",
                "memory_type": "vector",
                "channels": ["slack", "discord"],
                "reason": "长文本处理能力强，适合团队协作"
            },
            "enterprise": {
                "ai_provider": "azure",
                "ai_model": "gpt-4o",
                "gateway_mode": "high_availability",
                "memory_type": "graph",
                "channels": ["feishu", "wecom"],
                "reason": "企业级保障，SLA 支持"
            },
            "development": {
                "ai_provider": "ollama",
                "ai_model": "llama3.3",
                "gateway_mode": "local",
                "memory_type": "basic",
                "channels": [],
                "reason": "完全离线，零成本开发测试"
            }
        }

        return recommendations.get(use_case, recommendations["personal"])

    def generate_config_file(
        self,
        ai_provider: str,
        api_key: str,
        channels: List[Dict] = None,
        gateway_mode: str = "local",
        output_path: str = None
    ) -> str:
        """
        生成配置文件

        Args:
            ai_provider: AI 提供商
            api_key: API Key
            channels: 渠道配置
            gateway_mode: 网关模式
            output_path: 输出路径

        Returns:
            生成的配置内容
        """
        config = self.generator.generate_complete_config(
            ai_provider=ai_provider,
            ai_api_key=api_key,
            channels=channels,
            gateway_mode=gateway_mode
        )

        content = json.dumps(config, indent=2, ensure_ascii=False)

        if output_path:
            path = Path(output_path).expanduser()
            path.parent.mkdir(parents=True, exist_ok=True)
            with open(path, 'w') as f:
                f.write(content)
            print(f"配置文件已生成: {path}")

        return content

    def interactive_setup(self) -> Dict:
        """
        交互式配置向导

        返回用户选择的配置
        """
        config = {}

        # 1. 选择使用场景
        print("\n" + "="*60)
        print("OpenClaw 配置向导")
        print("="*60)

        print("\n请选择使用场景：")
        scenarios = [
            ("1", "个人使用", "性价比优先"),
            ("2", "团队协作", "功能全面"),
            ("3", "企业部署", "高可用保障"),
            ("4", "开发测试", "离线免费")
        ]

        for num, name, desc in scenarios:
            print(f"  {num}. {name} - {desc}")

        choice = input("\n请输入选项 [1]: ").strip() or "1"
        scenario_map = {"1": "personal", "2": "team", "3": "enterprise", "4": "development"}
        scenario = scenario_map.get(choice, "personal")

        # 获取推荐配置
        recommended = self.recommend_config(scenario)
        print(f"\n推荐配置：{recommended['reason']}")

        # 2. 选择 AI 提供商
        print("\n请选择 AI 模型提供商：")
        providers = self.get_ai_provider_info()

        provider_list = list(providers.keys())
        for i, (key, info) in enumerate(providers.items(), 1):
            is_recommended = " [推荐]" if key == recommended["ai_provider"] else ""
            print(f"  {i}. {info['name']}{is_recommended}")
            print(f"     适用: {info['best_for']}")

        provider_choice = input(f"\n请输入选项 [{provider_list.index(recommended['ai_provider'])+1}]: ").strip()
        if not provider_choice:
            ai_provider = recommended["ai_provider"]
        else:
            idx = int(provider_choice) - 1
            ai_provider = provider_list[idx] if 0 <= idx < len(provider_list) else provider_list[0]

        # 3. 输入 API Key
        print(f"\n请输入 {providers[ai_provider]['name']} API Key：")
        print("（输入时不显示，安全性保障）")
        import getpass
        api_key = getpass.getpass("API Key: ")

        if not api_key:
            print("错误: API Key 不能为空")
            return {}

        # 4. 选择通讯渠道
        print("\n是否配置通讯渠道？")
        print("  1. Telegram")
        print("  2. Discord")
        print("  3. 飞书")
        print("  4. 企业微信")
        print("  5. Slack")
        print("  6. 不配置")

        channel_choice = input("\n请选择 [6]: ").strip() or "6"
        channels = []

        if channel_choice != "6":
            channel_types = ["telegram", "discord", "feishu", "wecom", "slack"]
            if channel_choice in ["1", "2", "3", "4", "5"]:
                ch_type = channel_types[int(channel_choice) - 1]
                print(f"\n配置 {self.templates.CHANNEL_TEMPLATES[ch_type]['name']}：")

                channel_config = {"type": ch_type}

                template = self.templates.CHANNEL_TEMPLATES[ch_type]
                for field in template["required_fields"]:
                    value = input(f"  {field}: ")
                    channel_config[field] = value

                channels.append(channel_config)

        # 5. 选择网关模式
        print("\n请选择网关模式：")
        modes = list(self.templates.GATEWAY_TEMPLATES.keys())
        for i, mode in enumerate(modes, 1):
            info = self.templates.GATEWAY_TEMPLATES[mode]
            is_recommended = " [推荐]" if mode == recommended["gateway_mode"] else ""
            print(f"  {i}. {info['name']}{is_recommended}")
            print(f"     {info['description']}")

        gateway_choice = input(f"\n请选择 [1]: ").strip() or "1"
        gateway_idx = int(gateway_choice) - 1
        gateway_mode = modes[gateway_idx] if 0 <= gateway_idx < len(modes) else "local"

        # 6. 生成配置
        print("\n正在生成配置...")

        final_config = self.generator.generate_complete_config(
            ai_provider=ai_provider,
            ai_api_key=api_key,
            channels=channels if channels else None,
            gateway_mode=gateway_mode
        )

        return final_config


# =============================================================================
# 主函数
# =============================================================================

def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="OpenClaw 配置专家系统 v5.0"
    )

    # 信息查询
    parser.add_argument("--list-providers", action="store_true", help="列出所有 AI 提供商")
    parser.add_argument("--list-channels", action="store_true", help="列出所有通讯渠道")
    parser.add_argument("--provider-info", metavar="NAME", help="查看 AI 提供商详情")
    parser.add_argument("--channel-info", metavar="TYPE", help="查看渠道详情")
    parser.add_argument("--recommend", choices=["personal", "team", "enterprise", "development"],
                       help="获取配置推荐")

    # 配置生成
    parser.add_argument("--generate", action="store_true", help="生成配置文件")
    parser.add_argument("--ai-provider", help="AI 提供商")
    parser.add_argument("--ai-key", help="API Key")
    parser.add_argument("--output", "-o", help="输出文件路径")
    parser.add_argument("--gateway-mode", choices=["local", "remote", "high_availability"],
                       default="local", help="网关模式")

    # 交互式向导
    parser.add_argument("--interactive", "-i", action="store_true", help="启动交互式配置向导")

    args = parser.parse_args()

    expert = OpenClawConfigExpert()

    if args.list_providers:
        print("\n支持的 AI 模型提供商：\n")
        providers = expert.get_ai_provider_info()
        for key, info in providers.items():
            print(f"  {key}: {info['name']}")
            print(f"    模型: {', '.join(info['models'][:3])}...")
            print(f"    适用: {info['best_for']}")
            print(f"    定价: {info['pricing']}")
            print()

    elif args.list_channels:
        print("\n支持的通讯渠道：\n")
        channels = expert.get_channel_info()
        for key, info in channels.items():
            print(f"  {key}: {info['name']}")
            print(f"    必填: {', '.join(info['required_fields'])}")
            print(f"    适用: {info['best_for']}")
            print()

    elif args.provider_info:
        info = expert.get_ai_provider_info(args.provider_info)
        if info:
            print(f"\n{info['name']} 配置指南：\n")
            print(f"可用模型: {', '.join(info['models'])}")
            print(f"\n设置步骤:")
            for step, desc in info["setup_guide"].items():
                print(f"  {step}: {desc}")
            print(f"\n适用场景: {info['best_for']}")
            print(f"定价说明: {info['pricing']}")
        else:
            print(f"未知提供商: {args.provider_info}")

    elif args.channel_info:
        info = expert.get_channel_info(args.channel_info)
        if info:
            print(f"\n{info['name']} 配置指南：\n")
            print(f"必填字段: {', '.join(info['required_fields'])}")
            print(f"\n设置步骤:")
            for step, desc in info["setup_guide"].items():
                print(f"  {step}: {desc}")
            print(f"\n适用场景: {info['best_for']}")
        else:
            print(f"未知渠道: {args.channel_info}")

    elif args.recommend:
        rec = expert.recommend_config(args.recommend)
        print(f"\n{args.recommend} 场景推荐配置：\n")
        print(f"推荐理由: {rec['reason']}")
        print(f"\nAI 模型:")
        print(f"  提供商: {rec['ai_provider']}")
        print(f"  模型: {rec['ai_model']}")
        print(f"\n网关模式: {rec['gateway_mode']}")
        print(f"记忆系统: {rec['memory_type']}")
        print(f"通讯渠道: {', '.join(rec['channels']) or '无'}")

    elif args.generate:
        if not args.ai_provider or not args.ai_key:
            print("错误: --generate 需要 --ai-provider 和 --ai-key")
            return

        content = expert.generate_config_file(
            ai_provider=args.ai_provider,
            api_key=args.ai_key,
            gateway_mode=args.gateway_mode,
            output_path=args.output
        )

        print(f"\n生成的配置文件：\n")
        print(content)

    elif args.interactive:
        config = expert.interactive_setup()

        if config:
            print("\n" + "="*60)
            print("生成的配置：")
            print("="*60)
            print(json.dumps(config, indent=2, ensure_ascii=False))

            save = input("\n是否保存到 ~/.openclaw/openclaw.json？[Y/n]: ").strip().lower()
            if save != "n":
                output_path = Path.home() / ".openclaw" / "openclaw.json"
                expert.generate_config_file(
                    ai_provider=config.get("model", {}).get("provider"),
                    api_key=config.get("model", {}).get("api_key"),
                    channels=config.get("channels"),
                    gateway_mode=config.get("gateway", {}).get("mode", "local"),
                    output_path=str(output_path)
                )

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
