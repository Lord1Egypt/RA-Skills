import json
import os
from typing import Dict, List, Optional


class ConfigManager:
    """配置文件管理器"""

    def __init__(self, config_path: str = None):
        # 使用用户主目录，跨平台兼容
        if config_path is None:
            config_path = os.path.join(
                os.path.expanduser("~"), ".openclaw", "openclaw.json"
            )
        self.config_path = config_path
        self.config = self._load_config()

    def _load_config(self) -> Dict:
        """加载配置文件，如果不存在则创建默认配置"""
        if not os.path.exists(self.config_path):
            print(f"配置文件不存在，创建默认配置: {self.config_path}")
            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
            default_config = {
                "agents": {"defaults": {"model": {"primary": ""}, "models": {}}},
                "models": {"providers": {}},
            }
            with open(self.config_path, "w", encoding="utf-8") as f:
                json.dump(default_config, f, indent=2, ensure_ascii=False)
            return default_config

        with open(self.config_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _save_config(self) -> bool:
        """保存配置文件"""
        try:
            with open(self.config_path, "w", encoding="utf-8") as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"保存配置失败: {e}")
            return False

    def get_current_model(self) -> Optional[str]:
        """获取当前使用的模型"""
        try:
            return (
                self.config.get("agents", {})
                .get("defaults", {})
                .get("model", {})
                .get("primary")
            )
        except Exception as e:
            print(f"获取当前模型失败: {e}")
            return None

    def get_all_providers(self) -> Dict:
        """获取所有提供商"""
        return self.config.get("models", {}).get("providers", {})

    def save_provider(
        self,
        provider_id: str,
        base_url: str,
        api_key: str,
        model_id: str,
        context_window: int = 64000,
        max_tokens: int = 8000,
    ) -> bool:
        """保存提供商配置（同时更新 openclaw.json 和 auth-profiles.json）"""
        try:
            if "models" not in self.config:
                self.config["models"] = {}
            if "providers" not in self.config["models"]:
                self.config["models"]["providers"] = {}

            providers = self.config["models"]["providers"]

            if provider_id not in providers:
                providers[provider_id] = {
                    "baseUrl": base_url or "",
                    "apiKey": "",
                    "api": self._infer_api_type(base_url, provider_id),
                    "models": [{
                        "id": model_id,
                        "name": model_id,
                        "reasoning": False,
                        "input": ["text"],
                        "cost": {"input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0},
                        "contextWindow": context_window,
                        "maxTokens": max_tokens,
                    }],
                }
            else:
                provider = providers[provider_id]
                if base_url:
                    provider["baseUrl"] = base_url
                if api_key:
                    provider["apiKey"] = api_key

                models = provider.get("models", [])
                model_ids = [m["id"] for m in models]

                if model_id not in model_ids:
                    models.append(
                        {
                            "id": model_id,
                            "name": model_id,
                            "reasoning": False,
                            "input": ["text"],
                            "cost": {
                                "input": 0,
                                "output": 0,
                                "cacheRead": 0,
                                "cacheWrite": 0,
                            },
                            "contextWindow": context_window,
                            "maxTokens": max_tokens,
                        }
                    )
                    provider["models"] = models

            # 保存配置
            saved = self._save_config()

            # 如果提供了 API Key，同时更新认证文件
            if api_key:
                self.update_provider_apikey(provider_id, api_key)

            return saved
        except Exception as e:
            print(f"保存提供商配置失败: {e}")
            return False

    def update_provider_config(self, provider_id: str, base_url: str, api_key: str, context_window: int = 64000, max_tokens: int = 8000) -> bool:
        """只更新提供商的配置信息，不添加模型（更新 openclaw.json）"""
        try:
            if "models" not in self.config:
                self.config["models"] = {}
            if "providers" not in self.config["models"]:
                self.config["models"]["providers"] = {}

            api_type = self._infer_api_type(base_url, provider_id)

            providers = self.config["models"]["providers"]

            if provider_id not in providers:
                providers[provider_id] = {
                    "baseUrl": base_url or "",
                    "apiKey": api_key or "",
                    "api": api_type,
                    "models": [],
                }
            else:
                provider = providers[provider_id]
                if base_url:
                    provider["baseUrl"] = base_url
                if api_key:
                    provider["apiKey"] = api_key
                if "api" not in provider:
                    provider["api"] = api_type

            return self._save_config()
        except Exception as e:
            print(f"更新提供商配置失败: {e}")
            return False

    def _infer_api_type(self, base_url: str, provider_id: str) -> str:
        """根据 baseUrl 推断 API 类型"""
        return "openai-completions"

    def validate_and_fix(self) -> list:
        """启动时检测并修复所有 provider 配置，返回修复列表"""
        fixes = []
        providers = self.config.get("models", {}).get("providers", {})

        for provider_id, provider in providers.items():
            changed = False
            base_url = provider.get("baseUrl", "")
            api_type = self._infer_api_type(base_url, provider_id)

            if "api" not in provider:
                provider["api"] = api_type
                changed = True
                fixes.append(f"{provider_id}: 补全缺失的 api={api_type}")
            elif provider.get("api") != api_type:
                old = provider["api"]
                provider["api"] = api_type
                changed = True
                fixes.append(f"{provider_id}: 修正 api {old} -> {api_type}")

            for model in provider.get("models", []):
                needed = {"reasoning", "input", "cost", "contextWindow", "maxTokens"}
                missing = needed - set(model.keys())
                if missing:
                    if "reasoning" not in model:
                        model["reasoning"] = False
                    if "input" not in model:
                        model["input"] = ["text"]
                    if "cost" not in model:
                        model["cost"] = {"input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0}
                    if "contextWindow" not in model:
                        model["contextWindow"] = 64000
                    if "maxTokens" not in model:
                        model["maxTokens"] = 8000
                    changed = True
                    fixes.append(f"{provider_id}/{model.get('id','?')}: 补全字段 {missing}")

            if changed:
                fixes.append(f"{provider_id}: 配置已修复")

        if fixes:
            self._save_config()

        return fixes
        return "openai-completions"

    def switch_model_only(self, provider_id: str, model_id: str) -> bool:
        """只切换模型（不保存到通讯录）"""
        try:
            if "agents" not in self.config:
                self.config["agents"] = {}
            if "defaults" not in self.config["agents"]:
                self.config["agents"]["defaults"] = {}
            if "model" not in self.config["agents"]["defaults"]:
                self.config["agents"]["defaults"]["model"] = {}
            if "models" not in self.config["agents"]["defaults"]:
                self.config["agents"]["defaults"]["models"] = {}

            primary_model = f"{provider_id}/{model_id}"
            self.config["agents"]["defaults"]["model"]["primary"] = primary_model

            models_dict = self.config["agents"]["defaults"]["models"]
            if primary_model not in models_dict:
                models_dict[primary_model] = {}

            return self._save_config()
        except Exception as e:
            print(f"切换模型失败: {e}")
            return False

    def get_model_cards(self) -> List[Dict]:
        """获取所有模型卡片（不返回apiKey）"""
        cards = []
        current_model = self.get_current_model()
        providers = self.get_all_providers()

        for provider_id, provider_config in providers.items():
            models = provider_config.get("models", [])
            for model in models:
                model_id = model["id"]
                full_id = f"{provider_id}/{model_id}"

                cards.append(
                    {
                        "id": full_id,
                        "modelId": model_id,
                        "providerId": provider_id,
                        "baseUrl": provider_config.get("baseUrl", ""),
                        "isCurrent": full_id == current_model,
                    }
                )

        return cards

    def delete_model(self, provider_id: str, model_id: str) -> bool:
        """删除单个模型（清理 providers 和 agents.defaults.models）"""
        try:
            providers = self.config.get("models", {}).get("providers", {})
            if provider_id not in providers:
                return False

            provider = providers[provider_id]
            models = provider.get("models", [])
            provider["models"] = [m for m in models if m.get("id") != model_id]

            model_key = f"{provider_id}/{model_id}"

            agents_defaults = self.config.get("agents", {}).get("defaults", {})
            agents_models = agents_defaults.get("models", {})
            if model_key in agents_models:
                del agents_models[model_key]

            if agents_defaults.get("model", {}).get("primary") == model_key:
                agents_defaults["model"]["primary"] = ""

            return self._save_config()
        except Exception as e:
            print(f"删除模型失败: {e}")
            return False

    def delete_provider(self, provider_id: str) -> bool:
        """删除整个提供商"""
        try:
            providers = self.config.get("models", {}).get("providers", {})
            if provider_id not in providers:
                return False

            del providers[provider_id]
            return self._save_config()
        except Exception as e:
            print(f"删除提供商失败: {e}")
            return False

    def update_provider_apikey(self, provider_id: str, api_key: str) -> bool:
        """更新提供商的 API Key（同时更新 openclaw.json 和 auth-profiles.json）"""
        try:
            providers = self.config.get("models", {}).get("providers", {})
            if provider_id not in providers:
                return False

            providers[provider_id]["apiKey"] = api_key
            openclaw_saved = self._save_config()

            self.update_auth_profile(provider_id, api_key)

            return openclaw_saved
        except Exception as e:
            print(f"更新 API Key 失败: {e}")
            return False

    def get_advanced_settings(self) -> Dict:
        """获取高级设置"""
        tools = self.config.get("tools", {})
        agents = self.config.get("agents", {}).get("defaults", {})
        session = self.config.get("session", {})

        exec_conf = tools.get("exec", {})
        allow_list = tools.get("allow", [])
        deny_list = tools.get("deny", [])

        return {
            "toolsProfile": tools.get("profile", "full"),
            "allowExec": "exec" in allow_list,
            "allowBrowser": "browser" in allow_list,
            "allowWebSearch": "web_search" in allow_list,
            "allowWebFetch": "web_fetch" in allow_list,
            "denyElevated": "exec:elevated" in deny_list,
            "denyShell": "exec:shell" in deny_list,
            "execHost": exec_conf.get("host", "gateway"),
            "execAsk": exec_conf.get("ask", "off"),
            "execSecurity": exec_conf.get("security", "full"),
            "sandboxMode": agents.get("sandbox", {}).get("mode", "off"),
            "compactionMode": agents.get("compaction", {}).get("mode", "safeguard"),
            "dmScope": session.get("dmScope", "per-channel-peer"),
            "webSearchProvider": tools.get("web", {}).get("search", {}).get("provider", "brave"),
            "webFetchEnabled": tools.get("web", {}).get("fetch", {}).get("enabled", True),
        }

    def update_advanced_settings(self, settings: Dict) -> bool:
        """更新高级设置"""
        try:
            tools = self.config.setdefault("tools", {})
            exec_conf = tools.setdefault("exec", {})

            allow_list = []
            if settings.get("allowExec"): allow_list.append("exec")
            if settings.get("allowBrowser"): allow_list.append("browser")
            if settings.get("allowWebSearch"): allow_list.append("web_search")
            if settings.get("allowWebFetch"): allow_list.append("web_fetch")
            tools["allow"] = allow_list

            deny_list = []
            if settings.get("denyElevated"): deny_list.append("exec:elevated")
            if settings.get("denyShell"): deny_list.append("exec:shell")
            tools["deny"] = deny_list

            exec_conf["host"] = settings.get("execHost", "gateway")
            exec_conf["ask"] = settings.get("execAsk", "off")
            exec_conf["security"] = settings.get("execSecurity", "full")
            tools["profile"] = settings.get("toolsProfile", "full")

            web_conf = tools.setdefault("web", {})
            web_conf.setdefault("search", {})["provider"] = settings.get("webSearchProvider", "brave")
            web_conf.setdefault("fetch", {})["enabled"] = settings.get("webFetchEnabled", True)

            agents = self.config.setdefault("agents", {})
            agents_defaults = agents.setdefault("defaults", {})
            agents_defaults.setdefault("sandbox", {})["mode"] = settings.get("sandboxMode", "off")
            agents_defaults.setdefault("compaction", {})["mode"] = settings.get("compactionMode", "safeguard")

            session = self.config.setdefault("session", {})
            session["dmScope"] = settings.get("dmScope", "per-channel-peer")

            return self._save_config()
        except Exception as e:
            print(f"更新高级设置失败: {e}")
            return False

    def update_auth_profile(self, provider_id: str, api_key: str) -> bool:
        """更新 auth-profiles.json（OpenClaw 认证文件）"""
        try:
            auth_profiles_path = os.path.join(
                os.path.expanduser("~"),
                ".openclaw",
                "agents",
                "main",
                "agent",
                "auth-profiles.json",
            )

            if os.path.exists(auth_profiles_path):
                with open(auth_profiles_path, "r", encoding="utf-8") as f:
                    auth_config = json.load(f)
            else:
                auth_config = {"profiles": {}}

            profile_id = f"{provider_id}:manual"
            if "profiles" not in auth_config:
                auth_config["profiles"] = {}

            auth_config["profiles"][profile_id] = {
                "type": "token",
                "provider": provider_id,
                "token": api_key,
            }

            os.makedirs(os.path.dirname(auth_profiles_path), exist_ok=True)
            with open(auth_profiles_path, "w", encoding="utf-8") as f:
                json.dump(auth_config, f, indent=2, ensure_ascii=False)

            print(f"[ConfigManager] 已更新 auth-profiles.json: {profile_id}")
            return True
        except Exception as e:
            print(f"[ConfigManager] 更新 auth-profiles.json 失败: {e}")
            return False
