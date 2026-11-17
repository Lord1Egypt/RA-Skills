# -*- coding: utf-8 -*-
"""
题型插件加载器

约定：本目录下所有 `g_*.py` 文件为一个题型插件模块，模块内需定义：
    TOPICS : dict  { topic_key: gen_func(level, rng, lang) }
    LEVELS : list  (可选) 该模块题型适用的等级列表；省略表示加入全部等级

新增题型 = 往本目录丢一个 g_xxx.py 文件，无需改动主脚本。
"""
import os
import importlib


def load_generators():
    """返回 (GENERATORS, PLUGIN_LEVELS)。
    GENERATORS: topic_key -> gen_func(level, rng, lang)
    PLUGIN_LEVELS: topic_key -> 适用等级列表或 None
    """
    gens = {}
    levels = {}
    here = os.path.dirname(os.path.abspath(__file__))
    for fn in sorted(os.listdir(here)):
        if fn.startswith("g_") and fn.endswith(".py"):
            mod = importlib.import_module("generators." + fn[:-3])
            topics = getattr(mod, "TOPICS", None)
            if not topics:
                continue
            lv = getattr(mod, "LEVELS", None)
            for key, fnc in topics.items():
                gens[key] = fnc
                levels[key] = lv
    return gens, levels
