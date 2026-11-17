# -*- coding: utf-8 -*-
"""
题型插件加载器：扫描当前目录下的 g_*.py，导出 GENERATORS 与 PLUGIN_LEVELS。

每个插件需提供：
    LEVELS = [1,2,3,4]        # 该题型适用的等级（仅作参考/自动纳入）
    def gen(level, rng, lang): -> (title, instruction, html, answer)

新增题型：直接往本目录丢一个 g_xxx.py 即可，无需改动主程序。
"""
import importlib
import os
import pkgutil

GENERATORS = {}
PLUGIN_LEVELS = {}


def _load():
    here = os.path.dirname(__file__)
    for mod in pkgutil.iter_modules([here]):
        name = mod.name
        if not name.startswith("g_") or name == "g_base":
            continue
        key = name[2:]  # 去掉 g_ 前缀
        try:
            m = importlib.import_module(f"generators.{name}")
            if hasattr(m, "gen"):
                GENERATORS[key] = m.gen
                PLUGIN_LEVELS[key] = getattr(m, "LEVELS", list(range(1, 5)))
        except Exception as e:  # noqa
            print(f"[warn] 加载插件 {name} 失败: {e}")


_load()


def load_generators():
    return GENERATORS, PLUGIN_LEVELS
