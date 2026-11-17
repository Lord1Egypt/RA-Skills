"""
配置管理器
负责加载/保存配置文件，测试连接，以及对话式参数确认。
"""

import json
import os
from typing import Dict, Any, Optional, Tuple


class ConfigManager:
    """配置管理器"""

    DEFAULT_CONFIG_PATH = "D:/knowledge_skill/config.json"

    def __init__(self, config_path: str = None):
        self.config_path = config_path or self.DEFAULT_CONFIG_PATH
        self.config = self.load()

    def load(self) -> dict:
        """加载配置文件"""
        if os.path.exists(self.config_path):
            with open(self.config_path, "r", encoding="utf-8") as f:
                return json.load(f)
        else:
            raise FileNotFoundError(f"配置文件不存在: {self.config_path}")

    def save(self, config: dict = None):
        """保存配置文件"""
        if config:
            self.config = config
        with open(self.config_path, "w", encoding="utf-8") as f:
            json.dump(self.config, f, ensure_ascii=False, indent=2)

    def get(self, key: str, default=None):
        """获取配置项（支持点号路径）"""
        keys = key.split(".")
        value = self.config
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default
        return value if value is not None else default

    def set(self, key: str, value: Any):
        """设置配置项（支持点号路径）"""
        keys = key.split(".")
        target = self.config
        for k in keys[:-1]:
            if k not in target:
                target[k] = {}
            target = target[k]
        target[keys[-1]] = value

    # ==================== 连接测试 ====================

    def test_llm_connection(self) -> Tuple[bool, str]:
        """测试 LLM 模型连接"""
        import requests

        llm_config = self.config.get("llm", {})
        base_url = llm_config.get("base_url", "")
        api_key = llm_config.get("api_key", "")
        model = llm_config.get("model", "")
        test_msg = llm_config.get("test_message", "Hello, reply 'OK'.")
        test_endpoint = llm_config.get("test_endpoint", "/chat/completions")

        try:
            payload = {
                "model": model,
                "messages": [{"role": "user", "content": test_msg}],
                "max_tokens": 50
            }
            resp = requests.post(
                f"{base_url}{test_endpoint}",
                json=payload,
                headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
                timeout=30
            )
            if resp.status_code == 200:
                return True, f"LLM 连接成功 ✓ (模型: {model})"
            else:
                return False, f"LLM 返回错误: {resp.status_code} - {resp.text[:200]}"
        except requests.exceptions.ConnectionError:
            return False, f"无法连接到 LLM 服务 ({base_url})"
        except Exception as e:
            return False, f"LLM 连接测试失败: {e}"

    def test_vision_connection(self) -> Tuple[bool, str]:
        """测试视觉模型连接"""
        import requests

        llm_config = self.config.get("llm", {})
        base_url = llm_config.get("base_url", "")
        api_key = llm_config.get("api_key", "")
        vision_model = llm_config.get("vision_model", llm_config.get("model", ""))

        try:
            payload = {
                "model": vision_model,
                "messages": [{"role": "user", "content": "Hello, reply 'OK'."}],
                "max_tokens": 50
            }
            resp = requests.post(
                f"{base_url}/chat/completions",
                json=payload,
                headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
                timeout=30
            )
            if resp.status_code == 200:
                return True, f"视觉模型连接成功 ✓ (模型: {vision_model})"
            else:
                return False, f"视觉模型返回错误: {resp.status_code}"
        except Exception as e:
            return False, f"视觉模型测试失败: {e}"

    def test_easy_dataset_connection(self) -> Tuple[bool, str]:
        """测试 EasyDataset 连接"""
        import requests

        ed_config = self.config.get("easy_dataset", {})
        base_url = ed_config.get("base_url", "http://localhost:1717")

        try:
            resp = requests.get(f"{base_url}/", timeout=10)
            return True, f"EasyDataset 连接成功 ✓ ({base_url})"
        except requests.exceptions.ConnectionError:
            return False, f"无法连接到 EasyDataset ({base_url})，请确认 Docker 容器已启动"
        except Exception as e:
            return False, f"EasyDataset 连接测试失败: {e}"

    def test_mongo_connection(self) -> Tuple[bool, str]:
        """测试 MongoDB 连接"""
        try:
            from pymongo import MongoClient
            mongo_config = self.config.get("mongodb", {})
            uri = mongo_config.get("uri", "mongodb://localhost:27017")

            client = MongoClient(uri, serverSelectionTimeoutMS=5000)
            client.admin.command("ping")
            client.close()
            return True, f"MongoDB 连接成功 ✓ ({uri})"
        except Exception as e:
            return False, f"MongoDB 连接失败: {e}"

    def run_all_tests(self) -> list:
        """运行所有连接测试"""
        results = []
        results.append(("LLM 服务", *self.test_llm_connection()))
        results.append(("视觉模型", *self.test_vision_connection()))
        results.append(("EasyDataset", *self.test_easy_dataset_connection()))
        results.append(("MongoDB", *self.test_mongo_connection()))
        return results

    def test_and_report(self) -> bool:
        """测试所有连接并打印报告"""
        print("\n" + "=" * 60)
        print("  连接状态测试")
        print("=" * 60)

        results = self.run_all_tests()
        all_ok = True
        for name, ok, msg in results:
            status = "✅" if ok else "❌"
            print(f"  {status} {name}: {msg}")
            if not ok:
                all_ok = False

        print("=" * 60)
        return all_ok

    # ==================== 参数确认 ====================

    def get_params_for_confirm(self) -> list:
        """获取需要确认的参数列表"""
        ds = self.config.get("dataset_generation", {})
        return [
            ("文本切片最小长度", ds.get("chunk_min_length", 2500), "字符"),
            ("文本切片最大长度", ds.get("chunk_max_length", 4000), "字符"),
            ("切片重叠长度", ds.get("chunk_overlap", 200), "字符"),
            ("每N字符生成问题", ds.get("question_generation_length", 240), "字符"),
            ("每块预期问题数", ds.get("question_count_per_chunk", 5), "个"),
            ("任务并发数", ds.get("concurrency_limit", 3), "个"),
            ("导出格式", ds.get("export_format", "alpaca"), ""),
            ("导出文件类型", ds.get("export_file_type", "json"), ""),
            ("任务超时时间", ds.get("task_timeout_minutes", 720), "分钟"),
        ]

    def print_params_confirm_list(self):
        """打印参数确认列表"""
        params = self.get_params_for_confirm()
        print("\n" + "=" * 60)
        print("  数据集生成参数确认")
        print("=" * 60)
        for i, (name, value, unit) in enumerate(params, 1):
            unit_str = f" {unit}" if unit else ""
            print(f"  [{i}] {name}: {value}{unit_str}")
        print("=" * 60)
