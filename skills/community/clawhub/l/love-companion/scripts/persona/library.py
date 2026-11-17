#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
伴侣人格库（M3a）——存储、增量合并、纠偏、版本回滚、在线编译

人格的三条进化路径：
- 追加记忆 → 增量 merge 进对应部分
- 对话纠正 → 写入 Correction 层，**立即生效**
- 版本管理 → 每次更新自动存档，支持回滚

数据位置：~/.love-companion/data/personas/
    index.json              索引（slug → 基本信息）
    {slug}.json             人格本体
    _versions/{slug}/v{n}.json   历史版本，用于回滚

红线：
- 只依赖标准库
- 在线只注入 compile_summary 产出的压缩摘要，人格全量不进上下文
- 每条人格可追溯到素材指纹（来源素材），禁止凭空生成
"""

import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence

# 允许 `python scripts/persona/library.py` 直接跑（此时 sys.path[0] 是脚本所在目录）
_ROOT = Path(__file__).resolve().parents[2]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from scripts.core import schema  # noqa: E402
from scripts.core import settings as core_settings  # noqa: E402
from scripts.core.storage import read_json, write_json  # noqa: E402
from scripts.pipeline.injector import estimate_tokens, truncate_to_tokens  # noqa: E402

_UNSAFE = re.compile(r"[^\w\u4e00-\u9fff\-]")


def _now() -> str:
    return datetime.now().isoformat(timespec="seconds")


def _to_v1(extracted: Dict[str, Any], base: Optional[Dict[str, Any]] = None,
           overwrite: bool = False) -> Dict[str, Any]:
    """三层提取 → v1 人设（内部小工具，见 persona/adapt.py）"""
    from scripts.persona.adapt import apply_to_v1
    return apply_to_v1(base, extracted, overwrite=overwrite)


def slugify(name: str) -> str:
    """中文名也能安全做文件名；空名回退到时间戳"""
    s = _UNSAFE.sub("-", (name or "").strip()).strip("-")
    if not s:
        s = "persona-" + datetime.now().strftime("%Y%m%d%H%M%S")
    return s[:40]


class PersonaLibrary:
    """伴侣人格库"""

    def __init__(self, data_dir: Optional[str] = None):
        self.data_dir = core_settings.resolve_data_dir(data_dir)
        self.root = self.data_dir / "personas"
        self.root.mkdir(parents=True, exist_ok=True)
        self.versions_root = self.root / "_versions"
        self.index_file = self.root / "index.json"

    # ---------- 索引 IO ----------

    def _load_index(self) -> Dict[str, Any]:
        data = read_json(self.index_file, {})
        return data if isinstance(data, dict) else {}

    def _save_index(self, index: Dict[str, Any]) -> None:
        write_json(self.index_file, index)

    def _path(self, slug: str) -> Path:
        return self.root / f"{slug}.json"

    # ---------- CRUD ----------

    def list(self) -> List[Dict[str, Any]]:
        index = self._load_index()
        return [dict(v, slug=k) for k, v in index.items()]

    def exists(self, slug: str) -> bool:
        return self._path(slug).exists()

    def get(self, slug: str) -> Optional[Dict[str, Any]]:
        data = read_json(self._path(slug), None)
        return data if isinstance(data, dict) else None

    def create(self, persona: Dict[str, Any], slug: Optional[str] = None) -> Dict[str, Any]:
        """新建一条人格（若同名已存在则走 merge，不覆盖）"""
        base = slug or slugify(persona.get("昵称") or persona.get("姓名") or "")
        if self.exists(base):
            return self.merge(base, persona)
        persona = dict(persona)
        persona.setdefault("schema_version", schema.SCHEMA_VERSION)
        persona.setdefault("纠偏", [])
        persona["v1人设"] = _to_v1(persona)
        persona["版本"] = 1
        persona["created_at"] = _now()
        persona["updated_at"] = _now()
        self._write(base, persona, snapshot=True)
        return persona

    def _write(self, slug: str, persona: Dict[str, Any], snapshot: bool = False) -> None:
        if snapshot:
            self._snapshot(slug, persona)
        persona["updated_at"] = _now()
        write_json(self._path(slug), persona)
        index = self._load_index()
        index[slug] = {
            "姓名": persona.get("姓名", ""),
            "昵称": persona.get("昵称", ""),
            "版本": persona.get("版本", 1),
            "语料量": persona.get("语料量", 0),
            "updated_at": persona["updated_at"],
        }
        self._save_index(index)

    def delete(self, slug: str) -> bool:
        """删除人格本体（历史版本保留，防止误删后可找回）"""
        p = self._path(slug)
        if not p.exists():
            return False
        p.unlink()
        index = self._load_index()
        index.pop(slug, None)
        self._save_index(index)
        return True

    # ---------- 增量合并（merger） ----------

    def merge(self, slug: str, incoming: Dict[str, Any]) -> Dict[str, Any]:
        """把新素材的提取结果增量合并进已有人格

        合并策略：
        - 列表：并集去重，新证据排前面，截断到长度上限
        - 数值：按语料量加权平均（新素材量越大权重越高）
        - 枚举字符串：新值非「未知」才覆盖，避免稀疏语料把结论洗掉
        - 素材指纹：累积去重，保证可溯源
        """
        current = self.get(slug)
        if current is None:
            return self.create(incoming, slug)

        old_n = max(1, int(current.get("语料量", 1)))
        new_n = max(1, int(incoming.get("语料量", 1)))
        w_old, w_new = old_n / (old_n + new_n), new_n / (old_n + new_n)

        for layer in ("声线", "思维", "性格"):
            cur_l = current.setdefault(layer, {}) or {}
            inc_l = incoming.get(layer, {}) or {}
            cur_l = dict(cur_l)
            for key, inc_v in inc_l.items():
                if key == "置信度":
                    continue
                cur_v = cur_l.get(key)
                if isinstance(inc_v, list) and key != "价值观":
                    merged = list(inc_v) + [x for x in (cur_v or []) if x not in inc_v]
                    cur_l[key] = merged[:12]
                elif isinstance(inc_v, (int, float)) and isinstance(cur_v, (int, float)):
                    cur_l[key] = round(float(cur_v) * w_old + float(inc_v) * w_new, 3)
                elif isinstance(inc_v, str):
                    if not cur_v or cur_v in ("未知", "混合型", "") or inc_v not in ("未知", "混合型", ""):
                        if inc_v:
                            cur_l[key] = inc_v
                else:
                    cur_l[key] = inc_v
            # 置信度随语料量增长
            cur_l["置信度"] = round(min(1.0, (cur_l.get("置信度", 0.0) or 0.0) + new_n / 500.0), 2)
            current[layer] = cur_l

        prints = list(current.get("来源素材", []))
        for fp in incoming.get("来源素材", []) or []:
            if fp not in prints:
                prints.append(fp)
        current["来源素材"] = prints
        current["语料量"] = old_n + new_n
        # 三层合并完，重新回写 v1 人设（已有值不覆盖，只填空）
        current["v1人设"] = _to_v1(current, base=current.get("v1人设"))
        current["版本"] = int(current.get("版本", 1)) + 1
        self._write(slug, current, snapshot=True)
        return current

    # ---------- 纠偏层（Correction） ----------

    def correct(self, slug: str, wrong: str, right: str = "") -> Dict[str, Any]:
        """对话纠偏：「ta 不会这样说，ta 会这样说」——写入即生效

        Args:
            wrong: 不该出现的说法
            right: 应该改成什么；为空表示「直接禁用」
        """
        persona = self.get(slug)
        if persona is None:
            raise KeyError(f"人格不存在：{slug}")
        persona.setdefault("纠偏", []).append({
            "wrong": (wrong or "").strip(),
            "right": (right or "").strip(),
            "created_at": _now(),
        })
        persona["纠偏"] = persona["纠偏"][-50:]      # 只留最近 50 条，防止无限膨胀
        persona["版本"] = int(persona.get("版本", 1)) + 1
        self._write(slug, persona, snapshot=True)
        return persona

    def corrections(self, slug: str) -> List[Dict[str, str]]:
        persona = self.get(slug) or {}
        return persona.get("纠偏", []) or []

    def apply_corrections(self, text: str, corrections: Sequence[Dict[str, str]]) -> str:
        """把纠偏规则应用到一段文本（编译摘要与后处理都会走这里）"""
        out = text or ""
        for c in corrections or []:
            wrong = c.get("wrong", "").strip()
            right = c.get("right", "").strip()
            if not wrong:
                continue
            if right:
                out = out.replace(wrong, right)
            else:
                out = out.replace(wrong, "")
        return re.sub(r"\s{2,}", " ", out).strip()

    # ---------- 版本管理 ----------

    def _snapshot(self, slug: str, persona: Dict[str, Any]) -> None:
        """写入前自动存档

        - 首次创建：把新建的人格存为 v1（保证「删除后仍可找回」）
        - 后续更新：把**更新前**的旧状态存档，版本号取旧状态的版本
        """
        p = self._path(slug)
        if p.exists():
            archived = read_json(p, persona)
            if not isinstance(archived, dict):
                archived = persona
        else:
            archived = persona
        vdir = self.versions_root / slug
        vdir.mkdir(parents=True, exist_ok=True)
        version = int(archived.get("版本", 1))
        write_json(vdir / f"v{version}.json", archived)

    def versions(self, slug: str) -> List[int]:
        vdir = self.versions_root / slug
        if not vdir.exists():
            return []
        nums = []
        for f in vdir.glob("v*.json"):
            try:
                nums.append(int(f.stem[1:]))
            except ValueError:
                continue
        return sorted(nums)

    def rollback(self, slug: str, version: int) -> Optional[Dict[str, Any]]:
        """回滚到指定版本（当前状态先存档，可再回滚回来）"""
        vfile = self.versions_root / slug / f"v{version}.json"
        if not vfile.exists():
            return None
        old = read_json(vfile, None)
        if not isinstance(old, dict):
            return None
        old["版本"] = int(old.get("版本", version)) + 1
        self._write(slug, old, snapshot=True)
        return old

    # ---------- 在线编译 ----------

    def compile_summary(self, slug: str, budget: Optional[int] = None) -> str:
        """编译成在线注入的「恋人行为卡」（默认 100 Token 硬预算）

        love-companion 自己的形态：由 v1 人设字段（姓名/对用户的称呼/对话风格/
        性格/相处模式/亲密尺度/内容边界）编译，不是三层提取的原始结构。
        纠偏规则作为底线追加。超预算直接截断，绝不让人格段挤占其它模块。
        """
        from scripts.persona.adapt import lover_card

        limit = int(budget if budget is not None
                    else core_settings.budget(str(self.data_dir), "人格指令"))
        persona = self.get(slug)
        if persona is None:
            return ""
        v1 = persona.get("v1人设") or _to_v1(persona)
        card = lover_card(v1, budget=limit)

        corrections = self.corrections(slug)
        if corrections:
            rules = [f"不要说「{c['wrong']}」" + (f"，要说「{c['right']}」" if c["right"] else "")
                     for c in corrections[-3:]]
            room = limit - estimate_tokens(card) - estimate_tokens("。纠偏：")
            if room > 0:
                card = card + "。纠偏：" + truncate_to_tokens("；".join(rules), room)
        return self.apply_corrections(card, corrections)

    # ---------- 与 v1 人设体系的打通 ----------

    def v1_persona(self, slug: str) -> Dict[str, Any]:
        """返回可直接写进 persona.json 的 v1 人设（用于 /恋人配置）"""
        persona = self.get(slug)
        if persona is None:
            return {}
        return persona.get("v1人设") or _to_v1(persona)

    def push_to_v1(self, slug: str, overwrite: bool = False) -> Dict[str, Any]:
        """把蒸馏结果写回 v1 的 persona.json，使人设真相源保持唯一

        Args:
            overwrite: False（默认）只填空——用户手写过的值不动，
                       亲密尺度/内容边界/对用户的称呼 永远不动。
        """
        from scripts.manager import LoveCompanionManager

        extracted = self.get(slug)
        if extracted is None:
            raise KeyError(f"人格不存在：{slug}")
        manager = LoveCompanionManager(str(self.data_dir))
        current = manager.get_persona()
        merged = _to_v1(extracted, base=current, overwrite=overwrite)
        merged.pop("_蒸馏", None)          # 内部元信息不写进用户人设
        return manager.set_persona(merged)

    @staticmethod
    def from_preset(preset_id: int) -> Dict[str, Any]:
        """取一套 v1 预设作为蒸馏基底（预设 → 素材校准，而不是二选一）"""
        from scripts.manager import LoveCompanionManager
        preset = LoveCompanionManager().load_preset(preset_id)
        return preset or {}

    # ---------- 导出 ----------

    def export(self, slug: str) -> str:
        persona = self.get(slug) or {}
        return json.dumps(persona, ensure_ascii=False, indent=2)

    def purge(self, slug: str) -> int:
        """彻底清除（含历史版本）——数据主权"""
        removed = 0
        p = self._path(slug)
        if p.exists():
            p.unlink()
            removed += 1
        vdir = self.versions_root / slug
        if vdir.exists():
            for f in vdir.glob("*.json"):
                f.unlink()
                removed += 1
            try:
                vdir.rmdir()
            except OSError:
                pass
        index = self._load_index()
        index.pop(slug, None)
        self._save_index(index)
        return removed


if __name__ == "__main__":
    import sys
    lib = PersonaLibrary()
    cmd = sys.argv[1] if len(sys.argv) > 1 else "list"
    if cmd == "list":
        print(json.dumps(lib.list(), ensure_ascii=False, indent=2))
    elif cmd == "summary" and len(sys.argv) > 2:
        s = lib.compile_summary(sys.argv[2])
        print(s)
        print(f"[tokens ~{estimate_tokens(s)}]")
    else:
        print("用法: library.py list | summary <slug>")
