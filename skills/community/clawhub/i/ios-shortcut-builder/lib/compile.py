#!/usr/bin/env python3
"""compile.py — 把一份配方（recipe.json）编译成 .shortcut 文件。

配方是人写的、也是 AI 写的，所以规则要少、要能报错：
  - 未知动作 / 未知参数键 → 立刻报错，并告诉你合法值是什么
  - 控制流用 if / repeat / repeat_each / menu 四个关键字
  - 变量用 {clipboard} {now} {input} {prev} {battery} {location} {repeat_item} 插值
"""
from __future__ import annotations

import difflib
import json
import plistlib
import re
from pathlib import Path

import shortcutkit as sk

HERE = Path(__file__).resolve().parent
REGISTRY = HERE / "registry.json"

# 需要「先跑一个动作」才能拿到的变量（惰性插入，同一变量只取一次）
VAR_ACTIONS = {
    "clipboard": lambda s: s.action("is.workflow.actions.getclipboard"),
    "battery": lambda s: s.action("is.workflow.actions.getbatterylevel"),
    "location": lambda s: s.action("is.workflow.actions.getcurrentlocation"),
}

# 内置变量：不用跑动作，直接是可插值的附件
BUILTIN_VARS = {
    "now": sk.current_date,
    "input": sk.shortcut_input,
    "repeat_item": sk.repeat_item,
}

# 跑到就停下等人的动作；自动化场景里是硬伤
INTERACTIVE = {
    "is.workflow.actions.choosefrommenu",
    "is.workflow.actions.alert",
    "is.workflow.actions.ask",
    "is.workflow.actions.dictatetext",
}

CONDITIONS = {
    "is": "is", "等于": "is",
    "is_not": "is_not", "不等于": "is_not",
    "contains": "contains", "包含": "contains",
    "does_not_contain": "does_not_contain", "不包含": "does_not_contain",
    "begins_with": "begins_with", "开头是": "begins_with",
    "ends_with": "ends_with", "结尾是": "ends_with",
    "greater_than": "greater_than", "大于": "greater_than",
    "less_than": "less_than", "小于": "less_than",
    "is_greater_than": "greater_than", "is_less_than": "less_than",
    "greater_or_equal": "greater_or_equal", "大于等于": "greater_or_equal",
    "less_or_equal": "less_or_equal", "小于等于": "less_or_equal",
    "has_any_value": "has_any_value", "有值": "has_any_value",
    "has_no_value": "has_no_value", "没值": "has_no_value",
}


class RecipeError(Exception):
    pass


class Compiler:
    def __init__(self, registry_path: Path = REGISTRY):
        reg = json.loads(registry_path.read_text(encoding="utf-8"))
        self.actions = {a["alias"]: a for a in reg["actions"]}
        self.groups = reg["groups"]
        self._vars: dict[str, dict] = {}
        self._prev = None
        self._prev_void = False   # 上一步只打开 URL、不产生输出
        self.warnings: list[str] = []

    # ---------------- 变量 ----------------
    def resolve_var(self, name: str):
        name = name.strip()
        if name == "prev":
            if self._prev_void:
                raise RecipeError(
                    "上一步是 shortcut.run / script.run，它只是打开一个 URL 让系统去跑别的指令，"
                    "拿不到它的输出，{prev} 会是空的。\n"
                    "要用到结果，就把那段逻辑直接写进本配方；"
                    "或者改用 shortcutkit 的原生 runworkflow 动作（见 references/actions.md 末尾）。")
            if self._prev is None:
                raise RecipeError("配方第一步就用了 {prev}，它指上一步输出，前面还没有动作")
            return sk.ref(self._prev)
        if name in BUILTIN_VARS:
            return BUILTIN_VARS[name]()
        if name in self._vars:
            return sk.ref(self._vars[name])
        if name not in VAR_ACTIONS:
            raise RecipeError(
                f"未知变量 {{{name}}}；可用：prev / " + " / ".join(
                    list(BUILTIN_VARS) + list(VAR_ACTIONS)))
        act = VAR_ACTIONS[name](self._s)
        self._vars[name] = act
        return sk.ref(act)

    def interpolate(self, value):
        """字符串里的 {var} 换成引用；无占位符原样返回。"""
        if not isinstance(value, str) or "{" not in value:
            return value
        parts, buf, i = [], "", 0
        while i < len(value):
            ch = value[i]
            if ch == "{":
                j = value.find("}", i)
                if j == -1:
                    buf += ch
                    i += 1
                    continue
                name = value[i + 1:j]
                if not name.strip():
                    buf += ch
                    i += 1
                    continue
                if buf:
                    parts.append(buf)
                    buf = ""
                parts.append(self.resolve_var(name))
                i = j + 1
            else:
                buf += ch
                i += 1
        if buf:
            parts.append(buf)
        return sk.text(*parts) if len(parts) > 1 else parts[0]

    def value_of(self, raw):
        if isinstance(raw, dict):
            # 已经是构造好的 token（比如 sk.text() 拼出来的），原样用
            if str(raw.get("WFSerializationType", "")).startswith("WFTextToken"):
                return raw
            if set(raw) == {"ref"}:
                return self.resolve_var(raw["ref"])
            raise RecipeError(f"不认识的取值写法 {raw}；引用变量请写 {{\"ref\": \"clipboard\"}}")
        return self.interpolate(raw)

    # ---------------- 单步 ----------------
    def emit(self, steps, _depth=0):
        if not isinstance(steps, list):
            raise RecipeError("steps 必须是数组")
        for step in steps:
            if not isinstance(step, dict) or "do" not in step:
                raise RecipeError(f"每一步都要有 do 字段，收到：{step}")
            self.emit_one(step, _depth)

    def emit_one(self, step, depth):
        kw = step["do"]
        if kw in ("if", "repeat", "repeat_each", "menu"):
            return getattr(self, f"_cf_{kw}")(step, depth)

        spec = self.actions.get(kw)
        if spec is None:
            near = difflib.get_close_matches(kw, self.actions, n=3, cutoff=0.4)
            raise RecipeError(
                f"没有叫 {kw!r} 的动作。" + (f"你是不是想写：{', '.join(near)}？" if near else "")
                + f"\n用 `sc catalog` 看全部 {len(self.actions)} 个动作")

        params = {k: v for k, v in step.items() if k != "do"}
        impl = spec.get("impl")
        self._prev_void = False
        if impl:
            self._prev = getattr(self, f"_impl_{impl}")(params)
            return self._prev

        unknown = [k for k in params if k not in spec["params"]]
        if unknown:
            raise RecipeError(
                f"{kw} 没有参数 {unknown}；它接受：{sorted(spec['params']) or '（无参数）'}")
        if not params:
            self.warnings.append(f"{kw} 没给任何参数，生成的动作在手机上可能是空的")

        kwargs = {k: self.value_of(v) for k, v in params.items()}
        if spec["ident"] == "is.workflow.actions.sendmessage":
            self._check_recipients(params)
        self._prev = self._s.action(spec["ident"], **kwargs)
        return self._prev

    def _check_recipients(self, params):
        """短信收件人只认号码/邮箱，填联系人名在手机上会静默失败。"""
        raw = str(params.get("WFSendMessageActionRecipients", ""))
        for part in re.split(r"[,;，；]", raw):
            p = part.strip()
            if not p or "{" in p:
                continue
            if re.fullmatch(r"\+?[\d\s()-]{5,}", p) or "@" in p:
                continue
            self.warnings.append(
                f"收件人「{p}」不像号码或邮箱。iOS 只按号码/邮箱发，"
                "填联系人名（如「老婆」）在手机上会发不出去——换成 138xxxx 或 a@b.com")

    # ---------------- 特殊实现 ----------------
    def _as_ref(self, raw):
        """把取值转成「能作为动作输入」的形态。

        iOS 的输入参数只认动作输出（ref），不认裸文本；纯文本要先落成一个
        「文本」动作再引用。不这么做就会撞上 shortcutkit 的
        "expected a reference (ref(), variable(), shortcut_input(), ...)"。
        """
        val = self.value_of(raw)
        if isinstance(val, dict) and val.get("WFSerializationType") == "WFTextTokenAttachment":
            return val
        act = self._s.action("is.workflow.actions.gettext", WFTextActionText=val)
        return sk.ref(act)

    def _impl_set_clipboard(self, p):
        text = p.get("WFInput") or p.get("text")
        if text is None:
            raise RecipeError("clipboard.set 必须给 WFInput（要写入的内容）")
        return self._s.action("is.workflow.actions.setclipboard",
                              WFInput=self._as_ref(text))

    def _impl_add_reminder(self, p):
        kwargs = {"WFCalendarItemTitle": self.value_of(p.get("WFCalendarItemTitle", ""))}
        if p.get("WFCalendarItemNotes"):
            kwargs["WFCalendarItemNotes"] = self.value_of(p["WFCalendarItemNotes"])
        rem = self._s.action("is.workflow.actions.addnewreminder", **kwargs)
        # 列表必须写死，否则手机上会当场弹列表选择
        rem["WFWorkflowActionParameters"]["WFCalendarItemCalendar"] = "任务"
        rem["WFWorkflowActionParameters"]["WFCalendarDescriptor"] = {
            "Identifier": "<x-apple-reminderkit://REMCDList/D78E2703-4FAC-4FD6-94F0-E2423A3D572F>",
            "Title": "任务", "IsAllCalendar": False}
        return rem

    def _impl_lowpower(self, p):
        mode = str(p.get("operation", "toggle")).lower()
        if mode in ("on", "off"):
            return self._s.action("is.workflow.actions.lowpowermode.set",
                                  operation="set", OnValue=(mode == "on"))
        return self._s.action("is.workflow.actions.lowpowermode.set", operation="toggle")

    def _impl_run_shortcut(self, p):
        name = p.get("name")
        if not name:
            raise RecipeError("shortcut.run 必须给 name（目标快捷指令名）")
        enc = self._s.action("is.workflow.actions.urlencode",
                             WFInput=self._as_ref(name))
        url = sk.text("shortcuts://run-shortcut?name=", sk.ref(enc))
        if p.get("input"):
            enc_in = self._s.action("is.workflow.actions.urlencode",
                                    WFInput=self._as_ref(p["input"]))
            url = sk.text("shortcuts://run-shortcut?name=", sk.ref(enc),
                          "&input=text&text=", sk.ref(enc_in))
        self._prev_void = True
        self.warnings.append("shortcut.run 走 URL scheme：会跳到别的快捷指令，但拿不到它的输出")
        return self._s.action("is.workflow.actions.openurl", WFInput=self._as_ref(url))

    def _impl_run_scriptable(self, p):
        name = p.get("name")
        if not name:
            raise RecipeError("script.run 必须给 name（Scriptable 脚本名）")
        enc = self._s.action("is.workflow.actions.urlencode",
                             WFInput=self._as_ref(name))
        url = sk.text("scriptable:///run/", sk.ref(enc))
        self._prev_void = True
        self.warnings.append("script.run 走 URL scheme：会跳进 Scriptable，但拿不到它的输出")
        return self._s.action("is.workflow.actions.openurl", WFInput=self._as_ref(url))

    # ---------------- 控制流 ----------------
    def _cf_if(self, step, depth):
        subject = self.value_of(step.get("subject"))
        op = step.get("op", "is")
        cond = CONDITIONS.get(op)
        if cond is None:
            raise RecipeError(f"if 的 op 不认识：{op}；可用：{', '.join(sorted(CONDITIONS))}")
        value = self.value_of(step["value"]) if "value" in step else None
        gid = self._s.if_(subject, cond, value)
        self.emit(step.get("then", []), depth + 1)
        if step.get("else"):
            self._s.otherwise(gid)
            self.emit(step["else"], depth + 1)
        self._s.end_if(gid)
        self._prev = None

    def _cf_repeat(self, step, depth):
        n = step.get("count")
        if n is None:
            raise RecipeError("repeat 必须给 count")
        gid = self._s.repeat_count(int(n))
        self.emit(step.get("steps", []), depth + 1)
        self._s.end_repeat_count(gid)
        self._prev = None

    def _cf_repeat_each(self, step, depth):
        if "each" not in step:
            raise RecipeError("repeat_each 必须给 each（要遍历的内容）")
        gid = self._s.repeat_each(self.value_of(step["each"]))
        self.emit(step.get("steps", []), depth + 1)
        self._s.end_repeat_each(gid)
        self._prev = None

    def _cf_menu(self, step, depth):
        items = step.get("items")
        if not items:
            raise RecipeError("menu 必须给 items（数组，每项 {title, steps}）")
        gid = self._s.choose_from_menu(step.get("prompt", "选一个"), [i["title"] for i in items])
        for item in items:
            self._s.menu_item(gid, item["title"])
            self.emit(item.get("steps", []), depth + 1)
        self._s.end_menu(gid)
        self._prev = None

    # ---------------- 顶层 ----------------
    def build(self, recipe: dict, out_path: Path) -> dict:
        name = recipe.get("name")
        if not name:
            raise RecipeError("配方缺 name（快捷指令名，只能用英文数字下划线）")
        if not all(c.isascii() and (c.isalnum() or c in "_-") for c in name):
            raise RecipeError(f"name 只能用 ASCII 字母数字下划线连字符，收到 {name!r}")

        self._s = sk.Shortcut(name, color=recipe.get("color", "Blue"),
                              glyph=recipe.get("glyph", 61440))
        self._vars.clear()
        self._prev = None
        self._prev_void = False
        self.emit(recipe.get("steps", []))

        out_path.parent.mkdir(parents=True, exist_ok=True)
        self._s.write(str(out_path))
        doc = plistlib.load(open(out_path, "rb"))
        # 需要人点的动作放进自动化会卡住，提前说清楚
        blocking = [a for a in doc.get("WFWorkflowActions", [])
                    if a["WFWorkflowActionIdentifier"] in INTERACTIVE
                    and (a["WFWorkflowActionIdentifier"] != "is.workflow.actions.choosefrommenu"
                         or a.get("WFWorkflowActionParameters", {}).get("WFControlFlowMode") == 0)]
        if blocking:
            self.warnings.append(
                f"配方里有 {len(blocking)} 个需要人操作的动作（菜单/弹框/输入框/听写），"
                "放进「自动化」跑到那里仍会停下等人——想全自动就别用它们")
        doc["WFWorkflowName"] = name
        plistlib.dump(doc, open(out_path, "wb"), fmt=plistlib.FMT_BINARY)
        return self.report(doc, out_path)

    def report(self, doc, out_path) -> dict:
        acts = doc["WFWorkflowActions"]
        control = {"is.workflow.actions.conditional", "is.workflow.actions.repeat.count",
                   "is.workflow.actions.repeat.each", "is.workflow.actions.choosefrommenu"}
        opens = closes = 0
        for a in acts:
            if a["WFWorkflowActionIdentifier"] in control:
                mode = a.get("WFWorkflowActionParameters", {}).get("WFControlFlowMode")
                opens += mode == 0
                closes += mode == 2
        bad = [i for i, a in enumerate(acts) if "UUID" in a or "GroupingIdentifier" in a]
        return {
            "out": str(out_path),
            "name": doc.get("WFWorkflowName"),
            "actions": len(acts),
            "control_flow": f"{opens} 开 / {closes} 关",
            "balanced": opens == closes,
            "canonical": not bad,
            "warnings": self.warnings,
        }


def load_recipe(path: Path) -> dict:
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise RecipeError(f"找不到配方文件 {path}")
    except json.JSONDecodeError as e:
        raise RecipeError(f"{path} 不是合法 JSON：第 {e.lineno} 行 {e.msg}")
