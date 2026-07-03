"""JSON-based persistent storage for intent configurations."""
import json
import os
import uuid
from datetime import datetime
from typing import Optional

from .models import Intent


class IntentStore:
    """Manage intent CRUD with JSON file persistence."""

    def __init__(self, data_dir: str = None):
        if data_dir is None:
            data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
        os.makedirs(data_dir, exist_ok=True)
        self.file_path = os.path.join(data_dir, "intents.json")
        self._intents: dict[str, Intent] = {}
        self._load()

    def _load(self):
        """Load intents from JSON file or create defaults."""
        if os.path.exists(self.file_path):
            with open(self.file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            for d in data:
                intent = Intent.from_dict(d)
                self._intents[intent.id] = intent
        else:
            self._init_defaults()
            self._save()

    def _save(self):
        """Persist all intents to JSON."""
        data = [i.to_dict() for i in self._intents.values()]
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def _init_defaults(self):
        """Create initial default intents."""
        now = datetime.now().isoformat()
        defaults = [
            Intent(
                id=str(uuid.uuid4())[:8], name="编写代码", description="新建文件/功能/模块",
                category="CODE", sub_category="write", icon="\U0001f4bb",
                keywords=[
                    {"type": "keyword", "value": "写", "weight": 1.5},
                    {"type": "keyword", "value": "创建", "weight": 1.2},
                    {"type": "keyword", "value": "新建", "weight": 1.2},
                    {"type": "keyword", "value": "实现", "weight": 1.0},
                    {"type": "keyword", "value": "开发", "weight": 1.0},
                ],
                patterns=[r"(写|创建|新建|实现|开发).*(代码|文件|模块|功能|项目)"],
                route_skill="karpathy-principles", route_description="编码最佳实践",
                priority=10, created_at=now, updated_at=now,
            ),
            Intent(
                id=str(uuid.uuid4())[:8], name="修复Bug", description="Bug修复与调试",
                category="CODE", sub_category="fix", icon="\U0001f41b",
                keywords=[
                    {"type": "keyword", "value": "修复", "weight": 1.5},
                    {"type": "keyword", "value": "bug", "weight": 1.5},
                    {"type": "keyword", "value": "报错", "weight": 1.3},
                    {"type": "keyword", "value": "错误", "weight": 1.0},
                    {"type": "keyword", "value": "调试", "weight": 1.0},
                ],
                patterns=[r"(修复|修|修一下|改).*(bug|错误|报错|问题)"],
                route_skill="workflow-verifier", route_description="Bug验证流程",
                priority=10, created_at=now, updated_at=now,
            ),
            Intent(
                id=str(uuid.uuid4())[:8], name="代码审查", description="代码Review与优化建议",
                category="CODE", sub_category="review", icon="\U0001f50d",
                keywords=[
                    {"type": "keyword", "value": "审查", "weight": 1.5},
                    {"type": "keyword", "value": "review", "weight": 1.5},
                    {"type": "keyword", "value": "检查", "weight": 1.0},
                    {"type": "keyword", "value": "优化", "weight": 1.0},
                ],
                patterns=[r"(审查|review|检查|看一下).*(代码|文件)"],
                route_skill="code-reviewer", route_description="Code Review",
                priority=8, created_at=now, updated_at=now,
            ),
            Intent(
                id=str(uuid.uuid4())[:8], name="知识问答", description="概念解释与知识查询",
                category="KNOW", sub_category="define", icon="\U0001f4da",
                keywords=[
                    {"type": "keyword", "value": "是什么", "weight": 1.5},
                    {"type": "keyword", "value": "为什么", "weight": 1.3},
                    {"type": "keyword", "value": "如何", "weight": 1.2},
                    {"type": "keyword", "value": "解释", "weight": 1.2},
                    {"type": "keyword", "value": "怎么", "weight": 1.0},
                ],
                patterns=[r"(什么是|为什么|如何|怎么).*(?!代码)"],
                route_skill="mempalace-assistant", route_description="知识库查询",
                priority=9, created_at=now, updated_at=now,
            ),
            Intent(
                id=str(uuid.uuid4())[:8], name="任务执行", description="文件操作/命令执行/搜索",
                category="TASK", sub_category="execute", icon="\u2699\ufe0f",
                keywords=[
                    {"type": "keyword", "value": "帮我", "weight": 1.5},
                    {"type": "keyword", "value": "执行", "weight": 1.3},
                    {"type": "keyword", "value": "运行", "weight": 1.2},
                    {"type": "keyword", "value": "搜索", "weight": 1.0},
                    {"type": "keyword", "value": "删除", "weight": 1.2},
                    {"type": "keyword", "value": "读取", "weight": 1.0},
                    {"type": "keyword", "value": "下载", "weight": 1.0},
                    {"type": "keyword", "value": "上传", "weight": 1.0},
                    {"type": "keyword", "value": "安装", "weight": 1.0},
                    {"type": "keyword", "value": "部署", "weight": 1.0},
                ],
                patterns=[r"(帮我|请帮我|麻烦).*(做|执行|运行|搜索|读取|删除|下载|上传|安装|部署|清理|整理|创建)"],
                route_skill="skill-creator", route_description="任务编排",
                priority=9, created_at=now, updated_at=now,
            ),
            Intent(
                id=str(uuid.uuid4())[:8], name="日常闲聊", description="问候/闲聊/反馈",
                category="CHAT", sub_category="chat", icon="\U0001f4ac",
                keywords=[
                    {"type": "keyword", "value": "你好", "weight": 2.0},
                    {"type": "keyword", "value": "hi", "weight": 2.0},
                    {"type": "keyword", "value": "今天天气", "weight": 1.5},
                    {"type": "keyword", "value": "谢谢", "weight": 1.2},
                    {"type": "keyword", "value": "再见", "weight": 1.2},
                    {"type": "keyword", "value": "怎么样", "weight": 1.0},
                ],
                patterns=[r"^(hi|你好|嘿|hey|hello|今天天气|今天|怎么样)"],
                route_skill="general-chat", route_description="通用对话",
                priority=1, created_at=now, updated_at=now,
            ),
        ]
        for intent in defaults:
            self._intents[intent.id] = intent

    # --- CRUD ---

    def get_all(self, enabled_only: bool = False) -> list[Intent]:
        intents = list(self._intents.values())
        if enabled_only:
            intents = [i for i in intents if i.enabled]
        return sorted(intents, key=lambda x: -x.priority)

    def get(self, intent_id: str) -> Optional[Intent]:
        return self._intents.get(intent_id)

    def create(self, data: dict) -> Intent:
        now = datetime.now().isoformat()
        intent_id = data.get("id") or str(uuid.uuid4())[:8]
        intent = Intent(
            id=intent_id, name=data["name"],
            description=data.get("description", ""),
            category=data["category"], sub_category=data["sub_category"],
            icon=data.get("icon", "?"),
            keywords=data.get("keywords", []),
            patterns=data.get("patterns", []),
            route_skill=data.get("route_skill", ""),
            route_description=data.get("route_description", ""),
            priority=data.get("priority", 0),
            enabled=data.get("enabled", True),
            created_at=now, updated_at=now,
        )
        self._intents[intent.id] = intent
        self._save()
        return intent

    def update(self, intent_id: str, data: dict) -> Optional[Intent]:
        intent = self._intents.get(intent_id)
        if not intent:
            return None
        for field in ["name", "description", "category", "sub_category",
                       "icon", "keywords", "patterns", "route_skill",
                       "route_description", "priority", "enabled"]:
            if field in data:
                setattr(intent, field, data[field])
        intent.updated_at = datetime.now().isoformat()
        self._save()
        return intent

    def delete(self, intent_id: str) -> bool:
        if intent_id in self._intents:
            del self._intents[intent_id]
            self._save()
            return True
        return False

    def stats(self) -> dict:
        categories = {}
        for i in self._intents.values():
            categories[i.category] = categories.get(i.category, 0) + 1
        return {
            "total": len(self._intents),
            "enabled": sum(1 for i in self._intents.values() if i.enabled),
            "disabled": sum(1 for i in self._intents.values() if not i.enabled),
            "by_category": categories,
        }
