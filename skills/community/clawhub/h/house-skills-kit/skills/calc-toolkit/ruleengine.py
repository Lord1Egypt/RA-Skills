#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
house-skills-kit 工具库 · 三层规则引擎 v1.0
铁律（2026-08-29 定盘）：
  层1 default（全国默认档）→ 层2 城市/区域覆盖 → 层3 用户"我的模板"（JSON，可存可恢复）
  每个数字必须可标注：规则版本 + 来源 + 时点（as_of）
  未内置城市 = 自动继承 default 并提示"同级模板+一键改"
"""
import json
import os

KIT_TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))
RULES_FILE = os.path.join(KIT_TOOLS_DIR, "rules", "cities.yaml")
USER_TPL_DIR = os.path.join(KIT_TOOLS_DIR, "my_templates")

try:
    import yaml as _pyyaml
except ImportError:  # 零依赖兜底：内置迷你解析器（规则文件限定子集）
    _pyyaml = None


def _mini_scalar(s):
    s = s.strip()
    if len(s) >= 2 and s[0] == s[-1] and s[0] in "\"'":
        return s[1:-1]
    try:
        return int(s)
    except ValueError:
        pass
    try:
        return float(s)
    except ValueError:
        return s


def _strip_comment(line):
    """去行尾注释：# 前有空格或行首 #，且不在引号内。"""
    out, in_q, q = [], False, ""
    for i, ch in enumerate(line):
        if ch in "\"'":
            if not in_q:
                in_q, q = True, ch
            elif ch == q:
                in_q = False
        if ch == "#" and not in_q and (i == 0 or line[i - 1] in " \t"):
            break
        out.append(ch)
    return "".join(out).rstrip()


def _mini_yaml_load(text):
    """解析本项目规则文件的 YAML 子集：2空格缩进、key: value、引号串、行尾#注释。无列表。"""
    root = {}
    stack = [(-1, root)]
    for raw in text.splitlines():
        line = _strip_comment(raw)
        if not line.strip():
            continue
        indent = len(line) - len(line.lstrip(" "))
        key, _, val = line.strip().partition(":")
        key, val = key.strip(), val.strip()
        while stack and indent <= stack[-1][0]:
            stack.pop()
        parent = stack[-1][1]
        if val == "":
            parent[key] = {}
            stack.append((indent, parent[key]))
        else:
            parent[key] = _mini_scalar(val)
    return root


def _load_yaml_file(path):
    with open(path, encoding="utf-8") as f:
        text = f.read()
    if _pyyaml is not None:
        return _pyyaml.safe_load(text)
    return _mini_yaml_load(text)


def _deep_merge(base, override):
    """dict 深合并：override 覆盖 base，其余保留。"""
    out = dict(base) if isinstance(base, dict) else base
    if isinstance(override, dict):
        out = dict(base) if isinstance(base, dict) else {}
        for k, v in override.items():
            if isinstance(v, dict) and isinstance(base.get(k), dict):
                out[k] = _deep_merge(base[k], v)
            else:
                out[k] = v
    return out


def load_all():
    return _load_yaml_file(RULES_FILE)


def list_cities():
    data = load_all()
    return sorted(data.get("cities", {}).keys())


def rules_version():
    return load_all().get("rules_version", "?")


def get_rules(domain, city=None, district=None, user_template=None, overrides=None):
    """
    domain: 'loan' | 'tax' | 'discount'
    overrides: 层4·命令行即时覆盖 {'键': 值}（最高优先级，不入模板）
    返回 (merged, provenance)
      merged: 合并后的参数 dict（不含 _meta）
      provenance: 每个顶层键的来源说明 dict
    """
    data = load_all()
    default = data.get("default", {}).get(domain, {})
    prov = {k: {"source": "全国默认档", "as_of": default.get("_as_of", data.get("rules_version", "?"))}
            for k in default if not k.startswith("_")}

    chain = []
    if city:
        c = data.get("cities", {}).get(city)
        if c is None:
            cities_hint = "、".join(list_cities()[:8])
            print(f"[提示] 未内置城市「{city}」，已套用全国默认档（同级模板）。"
                  f"可编辑 {os.path.relpath(RULES_FILE, KIT_TOOLS_DIR)} 新增，或用 --template 传自定义模板。"
                  f"内置城市示例：{cities_hint}…")
        else:
            chain.append((city, c))

    if district and city:
        c = data.get("cities", {}).get(city) or {}
        d = (c.get("districts") or {}).get(district)
        if d:
            chain.append((f"{city}/{district}", d))

    if user_template:
        ut = _load_user_template(user_template)
        ud = (ut.get(domain) or {})
        if ud:
            chain.append((f"我的模板:{user_template}", ud))

    merged = dict(default)
    merged.pop("_as_of", None)
    for label, chunk in chain:
        dom = chunk.get(domain) or {}
        dom = {k: v for k, v in dom.items() if not k.startswith("_")}
        for k, v in dom.items():
            merged[k] = v
            prov[k] = {"source": label,
                       "as_of": chunk.get("_as_of") or chunk.get(domain, {}).get("_as_of") or rules_version()}
        # 城市级元信息
        if chunk.get("_note"):
            merged["_note"] = chunk["_note"]

    # 层4：--set 即时覆盖（最高优先级；来源标注为"本次指定"）
    # 支持 agent_rate=0.01（提升到顶层，工具内优先读取）与 fees.agent_rate=0.01（点路径写入嵌套）
    if overrides:
        for k, v in overrides.items():
            merged[k] = v
            prov[k] = {"source": "本次指定(--set)", "as_of": "即时生效"}
            if "." in k:
                parent, child = k.split(".", 1)
                merged.setdefault(parent, {})
                if isinstance(merged[parent], dict):
                    merged[parent][child] = v

    merged["_provenance"] = prov
    merged["_rules_version"] = rules_version()
    if city:
        merged["_city"] = city
    return merged, prov


# ---------- 层3：我的模板（安全加固 1.4.1：路径一律收敛在 my_templates/ 内） ----------
def _safe_tpl_name(name):
    """模板名只允许字母/数字/中文/下划线/连字符，剥离一切路径成分，杜绝目录穿越。"""
    base = os.path.basename(str(name).replace("\\", "/")).strip()
    if base in ("", ".", "..") or not all(c.isalnum() or c in "_-" or ord(c) > 127 for c in base):
        raise ValueError(f"模板名只能含中文/字母/数字/下划线/连字符: {name!r}")
    return base


def save_user_template(name, payload):
    base = _safe_tpl_name(name)
    os.makedirs(USER_TPL_DIR, exist_ok=True)
    path = os.path.join(USER_TPL_DIR, f"{base}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    return path


def _load_user_template(name):
    base = _safe_tpl_name(name)
    path = os.path.join(USER_TPL_DIR, f"{base}.json")
    if not os.path.exists(path):
        raise FileNotFoundError(f"我的模板不存在: {base}（用 --save-template 先保存）")
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def list_user_templates():
    if not os.path.isdir(USER_TPL_DIR):
        return []
    return sorted(f[:-5] for f in os.listdir(USER_TPL_DIR) if f.endswith(".json"))


def fmt_provenance(prov, keys):
    """输出『参数来源表』：每个数字标版本来源。"""
    lines = ["参数来源（规则版本可追溯）："]
    for k in keys:
        p = prov.get(k, {})
        lines.append(f"  · {k} = 来源[{p.get('source','?')}] 版本[{p.get('as_of','?')}]")
    return "\n".join(lines)


COMPLIANCE = "⚠ 结果为估算，实际以银行审批、税务核定与开发商备案价为准。政策随时更新，用前请核对当地最新公告。"
