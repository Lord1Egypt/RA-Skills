#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
控制与安全感（M7c）——把开关交回用户手里

三件事：
1. 模块开关：记忆/人格/关怀/趋势/多模态 等，可单独关
2. 特征权重可调：用户觉得「Agent 理解错我了」，直接改对应特征的可信度
3. 遗忘某段关系：一次性清掉人格 + 关系演化 + 该关系的记忆（数据主权）

所有设置落在 ~/.love-companion/data/settings.json，可导出、可清空。
"""

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

# 允许 `python scripts/panel/controls.py` 直接跑（此时 sys.path[0] 是脚本所在目录）
_ROOT = Path(__file__).resolve().parents[2]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from scripts.core import settings as core_settings  # noqa: E402
from scripts.core.storage import write_json  # noqa: E402

# 可开关的模块（与 schema.settings_template()["模块开关"] 对应）
MODULES = ("记忆系统", "人格克隆", "用户理解", "语气后处理",
           "主动关怀", "趋势感知", "多模态", "可解释面板")

VOICE_LEVELS = ("关闭", "轻柔", "标准", "深度")


def _now() -> str:
    return datetime.now().isoformat(timespec="seconds")


class Controls:
    """用户控制面"""

    def __init__(self, data_dir: Optional[str] = None):
        self.data_dir = core_settings.resolve_data_dir(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.file = self.data_dir / "settings.json"

    # ---------- IO ----------

    def _load(self) -> Dict[str, Any]:
        # 深合并：用户 settings.json 只覆盖它写明的叶子，缺省回退模板
        base = core_settings.load(str(self.data_dir))
        base.setdefault("特征权重", {})
        return base

    def _save(self, settings: Dict[str, Any]) -> None:
        settings["updated_at"] = _now()
        write_json(self.file, settings)

    # ---------- 1. 模块开关 ----------

    def enabled(self, module: str) -> bool:
        return bool(self._load().get("模块开关", {}).get(module, False))

    def toggle(self, module: str, on: Optional[bool] = None) -> bool:
        """切换模块开关；on 为空则取反"""
        if module not in MODULES:
            raise KeyError(f"未知模块 {module!r}，可选：{', '.join(MODULES)}")
        s = self._load()
        s.setdefault("模块开关", {})
        s["模块开关"][module] = (not s["模块开关"].get(module, False)) if on is None else bool(on)
        self._save(s)
        return s["模块开关"][module]

    def switches(self) -> Dict[str, bool]:
        return dict(self._load().get("模块开关", {}))

    # ---------- 2. 特征权重 ----------

    def set_weight(self, feature_path: str, value: float) -> float:
        """修正 Agent 对自己的理解

        Args:
            feature_path: 形如 "沟通风格.句式长度"、"依恋类型.判断"、"大五人格.外向性"
            value: 0–1，越大表示这条判断越可信；0 等于「别用它」
        """
        if not feature_path:
            raise ValueError("feature_path 不能为空")
        v = max(0.0, min(1.0, float(value)))
        s = self._load()
        s.setdefault("特征权重", {})[feature_path] = round(v, 2)
        self._save(s)
        return v

    def weight(self, feature_path: str) -> Optional[float]:
        return self._load().get("特征权重", {}).get(feature_path)

    def weights(self) -> Dict[str, float]:
        return dict(self._load().get("特征权重", {}))

    def reset_weight(self, feature_path: str) -> bool:
        s = self._load()
        removed = s.get("特征权重", {}).pop(feature_path, None) is not None
        if removed:
            self._save(s)
        return removed

    def apply_weights(self, persona: Dict[str, Any]) -> Dict[str, Any]:
        """把用户权重套用到画像上：权重低于 0.3 的字段标记为「存疑」，不参与注入"""
        weights = self.weights()
        if not weights:
            return persona
        marked = json.loads(json.dumps(persona, ensure_ascii=False))   # 深拷贝
        for path, w in weights.items():
            parts = path.split(".")
            node = marked
            for p in parts[:-1]:
                if not isinstance(node, dict) or p not in node:
                    node = None
                    break
                node = node[p]
            if isinstance(node, dict) and parts[-1] in node:
                if w < 0.3:
                    node[parts[-1]] = "" if isinstance(node[parts[-1]], str) else 0.0
                node["置信度"] = round(float(w), 2)
        return marked

    # ---------- 语气强度 ----------

    def set_voice(self, level: str) -> str:
        if level not in VOICE_LEVELS:
            raise KeyError(f"未知强度 {level!r}，可选：{', '.join(VOICE_LEVELS)}")
        s = self._load()
        s["语气强度"] = level
        self._save(s)
        return level

    # ---------- 3. 遗忘某段关系 ----------

    def forget(self, slug: str, drop_memories: bool = True) -> Dict[str, int]:
        """遗忘某段关系：人格 + 关系演化 +（可选）该关系的记忆

        Returns:
            {"persona": 0/1, "relation": 0/1, "memories": n}
        """
        result = {"persona": 0, "relation": 0, "memories": 0, "persona_v1": 0}
        try:
            from scripts.persona.library import PersonaLibrary
            lib = PersonaLibrary(str(self.data_dir))
            if lib.exists(slug):
                result["persona"] = 1 if lib.purge(slug) else 0
        except Exception:  # noqa: BLE001 - 人格库不可读不该中断遗忘
            pass

        try:
            from scripts.persona.mirror import MirrorModel
            result["relation"] = 1 if MirrorModel(str(self.data_dir)).clear(slug) else 0
        except Exception:  # noqa: BLE001
            pass

        if drop_memories:
            try:
                from scripts.memory.store import MemoryStore
                result["memories"] = MemoryStore(str(self.data_dir)).delete_conversation(slug)
            except Exception:  # noqa: BLE001
                pass

        # 当前生效的 persona.json 通常就是这段关系的人设；
        # 人格库清了而 persona.json 留着，等于「忘了人却还顶着她的名字说话」
        try:
            from scripts.manager import LoveCompanionManager
            manager = LoveCompanionManager(str(self.data_dir))
            pf = self.data_dir / "persona.json"
            if pf.exists():
                manager.reset_persona()
                result["persona_v1"] = 1
            else:
                result["persona_v1"] = 0
        except Exception:  # noqa: BLE001
            result["persona_v1"] = 0
        return result

    # ---------- 数据主权 ----------

    def status(self) -> Dict[str, Any]:
        """一句话概览，供「说明当前设置」类问题使用"""
        s = self._load()
        return {
            "schema_version": s.get("schema_version"),
            "开启模块": [m for m, v in self.switches().items() if v],
            "语气强度": s.get("语气强度"),
            "人工修正的特征": list((s.get("特征权重") or {}).keys()),
            "注入预算合计": (s.get("注入预算") or {}).get("合计上限"),
            "updated_at": s.get("updated_at"),
        }

    def export_all(self) -> str:
        """导出全部可导出数据（不含人格历史版本）"""
        payload: Dict[str, Any] = {"settings": self._load()}
        for name, loader in (
            ("memory", ("scripts.memory.store", "MemoryStore", "export")),
            ("trends", ("scripts.trends.store", "TrendStore", "export")),
        ):
            try:
                mod = __import__(loader[0], fromlist=[loader[1]])
                inst = getattr(mod, loader[1])(str(self.data_dir))
                payload[name] = json.loads(getattr(inst, loader[2])())
            except Exception:  # noqa: BLE001
                payload[name] = None
        try:
            from scripts.user.profile import UserProfileStore
            payload["user_persona"] = UserProfileStore(str(self.data_dir)).get()
        except Exception:  # noqa: BLE001
            payload["user_persona"] = None
        return json.dumps(payload, ensure_ascii=False, indent=2)

    def purge_all(self) -> List[str]:
        """一键清除本地所有数据（危险操作，返回被清文件列表）"""
        removed: List[str] = []
        for name in ("memory.json", "user_persona.json", "user_signals.json",
                     "trends.json", "trend_sources.json", "relations.json",
                     "care_state.json", "multimodal.json", "explanations.json",
                     "settings.json"):
            f = self.data_dir / name
            if f.exists():
                f.unlink()
                removed.append(name)
        import shutil
        persona_dir = self.data_dir / "personas"
        if persona_dir.exists():
            shutil.rmtree(persona_dir, ignore_errors=True)
            removed.append("personas/")
        return removed


if __name__ == "__main__":
    import sys
    c = Controls()
    cmd = sys.argv[1] if len(sys.argv) > 1 else "status"
    if cmd == "status":
        print(json.dumps(c.status(), ensure_ascii=False, indent=2))
    elif cmd == "off" and len(sys.argv) > 2:
        print(f"{sys.argv[2]} -> {c.toggle(sys.argv[2], False)}")
    elif cmd == "on" and len(sys.argv) > 2:
        print(f"{sys.argv[2]} -> {c.toggle(sys.argv[2], True)}")
    else:
        print("用法: controls.py status | on <模块> | off <模块>")
