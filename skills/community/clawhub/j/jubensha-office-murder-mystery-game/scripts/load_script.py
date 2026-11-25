#!/usr/bin/env python3
"""剧本加载器：references/<剧本>/ 目录 → 内存模型。

目录约定
--------
    <剧本>/
    ├── meta.md                 # ## meta / ## 阶段 / ## AI 自主交互
    ├── truth.md                # ## 真相（任何角色都读不到）
    ├── characters/
    │   ├── 00-detective.md          # ## 属性 / ## 公开口径 / ## 私下真相 / ## 禁止透露
    │   └── ...
    └── clues/
        ├── place-file-cabinet.md  # 每个 ## 是一张线索
        └── person-colleague-a.md

只依赖标准库。
"""

from __future__ import annotations

import os
import re

CLUE_SEP = "-"

# 线索文件名的类型前缀：兼容中文与英文（文件名可用英文，游戏内仍用各自语言）
CLUE_KIND_ALIASES = {
    "地点": "地点",
    "place": "地点",
    "location": "地点",
    "人身": "人身",
    "person": "人身",
    "body": "人身",
    "秘密": "秘密",
    "secret": "秘密",
}


# ---------------------------------------------------------------- 基础解析


def split_h2(text: str) -> tuple[str, dict[str, str]]:
    """按 `## ` 切分。返回 (前言, {标题: 正文})。"""
    parts = re.split(r"^## ", text, flags=re.M)
    sections: dict[str, str] = {}
    for chunk in parts[1:]:
        name, _, body = chunk.partition("\n")
        sections[name.strip()] = body.strip()
    return parts[0].strip(), sections


def split_h3(text: str) -> list[tuple[str, str]]:
    """按 `### ` 切分。返回 [(标题, 正文)]。"""
    parts = re.split(r"^### ", text, flags=re.M)
    out = []
    for chunk in parts[1:]:
        name, _, body = chunk.partition("\n")
        out.append((name.strip(), body.strip()))
    return out


def bullets(text: str) -> list[str]:
    return [line[2:].strip() for line in text.splitlines() if line.startswith("- ")]


def kv(text: str) -> dict[str, str]:
    """把 `- key: value` / `- key：value` 解析成 dict。"""
    out: dict[str, str] = {}
    for line in bullets(text):
        for sep in ("：", ":"):
            if sep in line:
                key, val = line.split(sep, 1)
                out[key.strip()] = val.strip()
                break
    return out


def as_bool(val: str | None, default: bool = False) -> bool:
    if val is None:
        return default
    return val.strip() in ("是", "true", "True", "yes", "1")


def as_int(val: str | None, default: int) -> int:
    try:
        return int(str(val).strip())
    except (TypeError, ValueError):
        return default


def _read(path: str) -> str:
    with open(path, encoding="utf-8") as f:
        return f.read()


# ---------------------------------------------------------------- 模型


class Character:
    def __init__(self, key: str, path: str):
        _, secs = split_h2(_read(path))
        props = kv(secs.get("属性", ""))
        # 文件名可以英文；游戏内名字用 `名称` 覆盖（不写则用文件名）
        self.key = props.get("名称") or key
        self.path = path  # 原文件路径（审计用）
        self.role = props.get("身份", "")
        self.can_lie = as_bool(props.get("可以说谎"), False)
        self.is_culprit = as_bool(props.get("是否犯人"), False)
        self.public = bullets(secs.get("公开口径", ""))
        self.private = (secs.get("私下真相", "") or "").strip()
        self.forbidden = bullets(secs.get("禁止透露", ""))

    def __repr__(self) -> str:
        return f"<Character {self.key}>"


class Clue:
    def __init__(self, target: str, kind: str, path: str):
        _, secs = split_h2(_read(path))
        # 可选的 `## 属性` 元信息块：让文件名全英文化，同时保留游戏内的目标名
        props = kv(secs.pop("属性", ""))
        self.target = props.get("目标") or target
        raw_kind = str(props.get("类型") or kind).strip()
        self.kind = CLUE_KIND_ALIASES.get(raw_kind, raw_kind)
        self.path = path
        self.items: dict[str, str] = {k: v for k, v in secs.items() if v}

    def drillables(self, item: str) -> list[str]:
        """线索里标注的「可深入调查 X」目标。"""
        text = self.items.get(item, "")
        return re.findall(r"可深入调查\s*([^\s）)]+)", text)


class Script:
    def __init__(self, case_dir: str):
        self.dir = case_dir
        meta_text = _read(os.path.join(case_dir, "meta.md"))
        _, secs = split_h2(meta_text)

        self.meta = kv(secs.get("meta", ""))
        # 英文剧本名：决定状态目录 ~/.jubensha/<slug>/
        self.slug = self._resolve_slug()
        self.ai = kv(secs.get("AI 自主交互", ""))
        self.phases = self._parse_phases(secs.get("阶段", ""))
        self.truth_path = os.path.join(case_dir, "truth.md")

        self.human = self.meta.get("人类角色", "")
        self.culprit_name = self.meta.get("犯人", "")  # 兼容旧数据，不推荐
        self.max_turn = as_int(self.meta.get("轮次上限"), 40)
        # 人类默认是侦探（不在场参与者/嫌疑人名单里），所以 AI 不该投他
        self.human_votable = as_bool(self.meta.get("人类可被投票"), False)

        # AI 回答里允许的“反问”：每对每轮 2 个问答来回
        self.ai_q_per_pair_round = as_int(self.ai.get("每对每轮问答上限", self.ai.get("每对每轮提问上限")), 2)
        self.ai_q_per_pair_game = as_int(self.ai.get("每对每局问答上限", self.ai.get("每对每局提问上限")), 20)
        # 每轮每人是否可以把其余 N-1 个人都问一遍（默认是）
        self.ai_ask_all = self.ai.get("每轮每人可问对象数", "全部") in ("全部", "是", "yes")

        # 人类是不是“常规在场角色”（嫌疑人/目击者之一），而不是侦探/DM
        # —— 决定 AI 能不能反过来问他
        self.human_is_actor = self._resolve_human_is_actor()

        self.actions = [a.strip() for a in re.split(r"[,，\s]+", self.meta.get("支持动作", "ask,vote,pass")) if a.strip()]

        self.characters: dict[str, Character] = {}
        self.character_paths: dict[str, str] = {}
        char_dir = os.path.join(case_dir, "characters")
        for fname in sorted(os.listdir(char_dir)):
            if not fname.endswith(".md"):
                continue
            key = re.sub(r"^\d+[-_]?", "", fname[:-3])
            char = Character(key, os.path.join(char_dir, fname))
            self.characters[char.key] = char
            self.character_paths[char.key] = char.path

        self.clues: dict[str, Clue] = {}
        clue_dir = os.path.join(case_dir, "clues")
        if os.path.isdir(clue_dir):
            for fname in sorted(os.listdir(clue_dir)):
                if not fname.endswith(".md") or CLUE_SEP not in fname:
                    continue
                kind, target = fname[:-3].split(CLUE_SEP, 1)
                clue = Clue(target, kind, os.path.join(clue_dir, fname))
                self.clues[clue.target] = clue

    def _resolve_slug(self) -> str:
        """英文剧本名：状态目录 `~/.jubensha/<slug>/` 的唯一标识。

        优先读 `meta.md` 的 `英文名`；没有就从目录名里提炼 ASCII 部分。
        """
        raw = str(self.meta.get("英文名") or "").strip().lower()
        if not raw:
            raw = os.path.basename(os.path.normpath(self.dir)).lower()
        raw = re.sub(r"[^a-z0-9-]+", "-", raw).strip("-")
        return raw or "script"

    def _resolve_human_is_actor(self) -> bool:
        """判定人类扮演的是否为普通在场角色。

        优先级：
          1. meta 显式声明 `人类角色类型`（侦探 / 嫌疑人 / 在场者 …）
          2. `人类可被投票`
          3. `AI 可反问人类`
          4. 人类是否出现在 `AI 角色` 名单里（无侦探本时人类会占用一个嫌疑人位）
        """
        kind = self.meta.get("人类角色类型", "").strip()
        if kind:
            return kind in ("嫌疑人", "角色", "在场者", "目击者", "玩家")
        if as_bool(self.meta.get("人类可被投票"), False):
            return True
        if as_bool(self.ai.get("AI 可反问人类"), False):
            return True
        ai_names = [a.strip() for a in re.split(r"[,，\s]+", self.meta.get("AI 角色", "")) if a.strip()]
        return bool(self.human and self.human in ai_names)

    # -- 阶段 ---------------------------------------------------------
    @staticmethod
    def _parse_phases(text: str) -> list[dict]:
        phases = []
        for idx, (name, body) in enumerate(split_h3(text)):
            title = re.sub(r"^\d+\s*", "", name)
            opts = kv(body)
            phases.append(
                {
                    "index": idx,
                    "name": title,
                    "可被问次数": as_int(opts.get("可被问次数"), 999),
                    "可搜证": as_bool(opts.get("可搜证"), True),
                    "可对质": as_bool(opts.get("可对质"), False),
                    "对质次数上限": as_int(opts.get("对质次数上限"), 3),
                    "必须投票才能结束": as_bool(opts.get("必须投票才能结束"), False),
                }
            )
        return phases or [{"index": 0, "name": "默认", "可被问次数": 999, "可搜证": True, "可对质": True, "对质次数上限": 3, "必须投票才能结束": False}]

    # -- 便捷 ---------------------------------------------------------
    @property
    def culprit(self) -> str:
        """凶手名字。**惰性读取 `truth.md`**——正常游玩过程中只被调用于
        结算和 AI 投票，角色 prompt 永远不含它。

        优先 `truth.md` 的 `## 凶手`（推荐）；旧剧本回退到 `meta.md` 的 `犯人`。
        """
        if getattr(self, "_culprit", None) is None:
            self._culprit = self._parse_culprit()
        return self._culprit

    def _parse_culprit(self) -> str:
        if self.culprit_name:
            return self.culprit_name
        try:
            _, secs = split_h2(_read(self.truth_path))
        except OSError:
            return ""
        raw = (secs.get("凶手", "") or "").strip()
        return raw.splitlines()[0].strip().rstrip("。.").strip() if raw else ""

    @property
    def ai_names(self) -> list[str]:
        return [n for n in self.characters if n != self.human]

    def others(self, name: str) -> list[str]:
        return [n for n in self.characters if n != name]

    def vote_weight(self, name: str) -> int:
        raw = self.meta.get("票数权重", "")
        for part in re.split(r"[,，\s]+", raw):
            if "=" in part:
                who, val = part.split("=", 1)
                if who.strip() == name:
                    return as_int(val, 1)
        return 1

    def read_truth(self) -> str:
        """全流程唯一一次读取真相。"""
        return _read(self.truth_path) if os.path.exists(self.truth_path) else ""


def load(case_dir: str) -> Script:
    return Script(case_dir)
