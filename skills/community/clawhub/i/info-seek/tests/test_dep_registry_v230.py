#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_dep_registry_v230.py — S1 守护：外部依赖统一注册表（27 断言）

方向②阶段A「建表零回归」：验证 deps/registry.yaml + core/dep_registry.py
的声明完整性、接口契约、零第三方硬依赖、委托桥一致性与双导入登记。

分组：
  A 声明 / schema（A1-A8）
  B 接口契约     （B1-B9）
  C 零硬依赖 / 内嵌回退（C1-C3）
  D 委托桥一致性 （D1-D3）
  E 双导入登记   （E1）
  F 单向依赖     （F1）
  G 缓存         （G1-G2）

约束：本套件不自我 SKIP；不依赖任何可选第三方（全部条件断言）。
"""

import importlib
import os
import re
import sys
from pathlib import Path

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for p in (os.path.join(ROOT, "core"), ROOT, os.path.join(ROOT, "scripts")):
    if p not in sys.path:
        sys.path.insert(0, p)

import dep_registry as dr  # noqa: E402

PASS, FAIL = [], []


def ok(name, cond, detail=""):
    (PASS if cond else FAIL).append(name)
    print(f"  [{'PASS' if cond else 'FAIL'}] {name}" + (f" — {detail}" if detail else ""))


# ── A 声明 / schema ─────────────────────────────────────────────────────
print("=== A 声明 / schema ===")
all_deps = dr.list_deps()
names = [d.get("name") for d in all_deps]
ok("A1 注册表加载 ≥19 项", len(all_deps) >= 19, f"实测={len(all_deps)} 来源={dr.registry_source()}")
ok("A2 事实来源 ∈ {yaml, embedded}", dr.registry_source() in ("yaml", "embedded"),
   f"来源={dr.registry_source()}")
ok("A3 每项含 name/kind 且 kind 合法",
   all(d.get("name") and d.get("kind") in dr._VALID_KINDS for d in all_deps),
   f"非法项={[d.get('name') for d in all_deps if d.get('kind') not in dr._VALID_KINDS]}")
ok("A4 python_pkg 均声明 import",
   all(d.get("import") for d in all_deps if d.get("kind") == "python_pkg"),
   f"缺失={[d.get('name') for d in all_deps if d.get('kind') == 'python_pkg' and not d.get('import')]}")
ok("A5 cli_binary 均声明 cli",
   all(d.get("cli") for d in all_deps if d.get("kind") == "cli_binary"),
   f"cli 项={[d.get('name') for d in all_deps if d.get('kind') == 'cli_binary']}")
ok("A6 browser_binary 均含非空 probe",
   all(d.get("probe") for d in all_deps if d.get("kind") == "browser_binary"),
   f"浏览器项={[d.get('name') for d in all_deps if d.get('kind') == 'browser_binary']}")
ok("A7 jieba/pypinyin 委托 jieba_bridge",
   dr.get_dep("jieba").get("delegate", "").startswith("jieba_bridge:")
   and dr.get_dep("pypinyin").get("delegate", "").startswith("jieba_bridge:"),
   f"jieba={dr.get_dep('jieba').get('delegate')} pypinyin={dr.get_dep('pypinyin').get('delegate')}")
ok("A8 name 唯一无重复", len(names) == len(set(names)),
   f"重复={[n for n in names if names.count(n) > 1]}")

# ── B 接口契约 ──────────────────────────────────────────────────────────
print("\n=== B 接口契约 ===")
st_unknown = dr.dep_status("__not_a_dep__")
ok("B1 未声明依赖返回 declared=False（不抛错）",
   st_unknown.get("declared") is False and st_unknown.get("available") is False,
   f"declared={st_unknown.get('declared')}")
st_yaml = dr.dep_status("PyYAML")
ok("B2 已声明依赖 declared=True 且 available 为 bool",
   st_yaml.get("declared") is True and isinstance(st_yaml.get("available"), bool),
   f"available={st_yaml.get('available')} version={st_yaml.get('version')}")
ok("B3 is_available 返回 bool", isinstance(dr.is_available("PyYAML"), bool))
ok("B4 import_optional 未声明依赖 → None", dr.import_optional("__not_a_dep__") is None)
mod_yaml = dr.import_optional("PyYAML")
ok("B5 import_optional 与 dep_status 一致",
   (mod_yaml is not None) == st_yaml.get("available"),
   f"模块={type(mod_yaml).__name__ if mod_yaml else None} available={st_yaml.get('available')}")
raised, exc = False, None
try:
    dr.require("__not_a_dep__")
except dr.DependencyMissing as e:
    raised, exc = True, e
ok("B6 require 不可用依赖抛 DependencyMissing", raised,
   f"异常={type(exc).__name__ if exc else None}")
ok("B7 DependencyMissing.code=0 且携带 install_hint 属性",
   raised and exc.code == 0 and hasattr(exc, "install_hint"),
   f"code={getattr(exc, 'code', None)}")
py_deps = dr.list_deps("python_pkg")
ok("B8 list_deps(kind) 过滤正确且非空",
   len(py_deps) >= 1 and all(d.get("kind") == "python_pkg" for d in py_deps),
   f"python_pkg={len(py_deps)} 全部={len(all_deps)}")
ok("B9 get_dep('jieba').delegate == 'jieba_bridge:get_jieba'",
   dr.get_dep("jieba").get("delegate") == "jieba_bridge:get_jieba",
   f"实测={dr.get_dep('jieba').get('delegate')}")

# ── C 零硬依赖 / 内嵌回退 ───────────────────────────────────────────────
print("\n=== C 零硬依赖 / 内嵌回退 ===")
src = Path(dr.__file__).read_text(encoding="utf-8")
bad_toplevel = re.findall(
    r"^import\s+(yaml|jieba|pypinyin|httpx|summa|playwright|cryptography|keyring|"
    r"schedule|opentelemetry|whisper)\b", src, re.M)
ok("C1 无顶层第三方 import（零硬依赖）", not bad_toplevel,
   f"命中={bad_toplevel}")

_saved_path, _saved_cache = dr._REGISTRY_PATH, dr._cache
try:
    dr._REGISTRY_PATH = Path("/nonexistent/infoseek_deps_xyz.yaml")
    dr.reset()
    src_embedded = dr.registry_source()
    n_embedded = len(dr.list_deps())
finally:
    dr._REGISTRY_PATH = _saved_path
    dr.reset()
ok("C2 表文件缺失时回退内嵌且项数 ≥19",
   src_embedded == "embedded" and n_embedded >= 19,
   f"来源={src_embedded} 项数={n_embedded}")

emb = dr._DEFAULT_DEPS
ok("C3 内嵌默认无重复 name",
   len({d.get("name") for d in emb}) == len(emb),
   f"内嵌项数={len(emb)}")

# ── D 委托桥一致性 ──────────────────────────────────────────────────────
print("\n=== D 委托桥一致性 ===")
try:
    import jieba_bridge as jb
    _jb_ok = callable(getattr(jb, "get_jieba", None))
except Exception:
    jb, _jb_ok = None, False
ok("D1 jieba_bridge.get_jieba 可调用（委托目标存在）", _jb_ok,
   f"bridge={'ok' if _jb_ok else '不可用'}")
ok("D2 dep_status('jieba') 走委托路径（detail 含『委托』）",
   "委托" in dr.dep_status("jieba").get("detail", ""),
   f"detail={dr.dep_status('jieba').get('detail')}")
if _jb_ok:
    bridge_avail = jb.get_jieba() is not None
else:
    bridge_avail = False
ok("D3 委托结果与 bridge 直接调用一致（单一真源）",
   dr.dep_status("jieba").get("available") == bridge_avail,
   f"dep={dr.dep_status('jieba').get('available')} bridge={bridge_avail}")

# ── E 双导入登记 ────────────────────────────────────────────────────────
print("\n=== E 双导入登记 ===")
ok("E1 顶层名与 core. 包路径指向同一模块对象",
   sys.modules.get("dep_registry") is sys.modules.get("core.dep_registry") is not None,
   f"dep_registry={'✓' if sys.modules.get('dep_registry') is not None else '✗'} "
   f"core.dep_registry={'✓' if sys.modules.get('core.dep_registry') is not None else '✗'}")

# ── F 单向依赖 ──────────────────────────────────────────────────────────
print("\n=== F 单向依赖 ===")
cap_imports = re.findall(r"^\s*(?:import|from)\s+[\w.]*capability_registry", src, re.M)
ok("F1 dep_registry 不 import cap 层（单向依赖）", not cap_imports,
   f"命中={cap_imports}")

# ── G 缓存 ──────────────────────────────────────────────────────────────
print("\n=== G 缓存 ===")
s1 = dr.dep_status("PyYAML")
s2 = dr.dep_status("PyYAML")
ok("G1 dep_status 命中进程内缓存（同一对象）", s1 is s2)
dr.reset()
s3 = dr.dep_status("PyYAML")
ok("G2 reset() 后状态缓存清空（重算新对象）", s3 is not s1)

print(f"\ndep_registry: {len(PASS)} PASS / {len(FAIL)} FAIL")
if FAIL:
    print("未通过：" + ", ".join(FAIL))
sys.exit(1 if FAIL else 0)
