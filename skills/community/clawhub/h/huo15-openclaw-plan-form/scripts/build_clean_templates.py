#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成三个【干净、已重命名、无示例数据】的标准空白模板到 assets/templates/。

这些是给人看的“格式参考件”——回答了用户两点要求：
  - 模板名是临时的 -> 用 schema 的 display_name 重命名
  - 模板里有示例数据 -> 从 schema 现搭，天然无示例数据
实际转换输出由 fill_template.py 生成（日期区按真实数据展开）。

用法: python build_clean_templates.py [输出目录]
"""
from __future__ import annotations
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_forms import load_schema
from lib_xlsx import write_form

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_OUT = os.path.join(HERE, "..", "assets", "templates")


def main():
    out_dir = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_OUT
    os.makedirs(out_dir, exist_ok=True)
    schema = load_schema()
    for t in schema["templates"]:
        fname = f"{t['display_name']}-模板.xlsx"
        path = os.path.join(out_dir, fname)
        res = write_form(path, t, rows=None, dates=[], blank_placeholder=True)
        print(f"✓ {fname}  ({res['n_cols']} 列, sheet='{res['sheet']}')")
    print(f"\n输出目录: {os.path.abspath(out_dir)}")


if __name__ == "__main__":
    main()
