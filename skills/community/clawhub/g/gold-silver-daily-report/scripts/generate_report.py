#!/usr/bin/env python3
"""
generate_report.py — 用当日数据渲染「黄金白银行情日报」HTML。

用法:
  python3 generate_report.py --data report_data.json \
      --template assets/report_template.html \
      --out 黄金白银日报-2026-07-22.html

数据 JSON 字段 (与 assets/report_template.html 的 {{占位符}} 一一对应):
  report_date      例如 "2026年7月22日（周三）"
  data_asof        例如 "亚盘盘中 14:20（北京时间）"
  header_tag       例如 "现货金 4,069.76 USD/oz · 金银比 69.6 · 白银领涨 +3.75%"
  conclusion_text  结论段 HTML(无需含"结论："前缀)
  risk_items       5 条风险的 <li>...</li> HTML
  disclaimer       免责声明文本
  dashboard_note   仪表盘说明
  gsr_big          金银比大数字，例如 "69.6"
  gsr_min / gsr_mean / gsr_max   半年最低/均值/最高(纯数字字符串)
  gsr_min_label / gsr_max_label  半年最低/最高日期标注，例如 "1/29" / "7/17"
  gsr_note         金银比解读
  sec1_rows / sec1_note      核心数据表 tbody + 说明
  sec2_rows / sec2_note      国内 T+D 表 tbody + 说明
  sec3_rows / sec3_note      宏观指标表 tbody + 说明
  sec4_note        第四节指路说明
  sec5_cards       四卡 HTML(实际利率/美元/央行购金/地缘)
  sec6_cards       两卡 HTML(金银比视角/光伏去银化) + note
  sec7_bull / sec7_bear   利多/利空 <li> 列表
  sec8_rows / sec8_note   机构目标价表 tbody + 说明
  sec9_cal / sec9_levels  事件日历 / 技术价位 HTML
  gold90_json      黄金近90天双向价格 JS 对象字符串: {"usd":{dates,values,min,max},"rmb":{...}}
  gsr_script       由 build_gsr_series.py 生成的 <script> 片段(定义 dates/values/gsrMean)

注意:
  - 占位符若未在 JSON 中提供，将保留原样并在 stderr 提示，便于排查。
  - 本脚本只负责"渲染"，数据真实性与联网检索由调用方(SKILL 流程)保证。
"""
import argparse
import json
import os
import re

PLACEHOLDER = re.compile(r'\{\{(\w+)\}\}')


def main():
    ap = argparse.ArgumentParser(description="渲染黄金白银行情日报 HTML")
    ap.add_argument('--data', required=True, help='当日数据 JSON 路径')
    ap.add_argument('--template', required=True, help='assets/report_template.html 路径')
    ap.add_argument('--out', required=True, help='输出 HTML 路径')
    args = ap.parse_args()

    with open(args.data, encoding='utf-8') as f:
        data = json.load(f)
    with open(args.template, encoding='utf-8') as f:
        html = f.read()

    # 大小写不敏感匹配：模板占位符常为大写(如 {{REPORT_DATE}})，
    # 而数据 JSON 习惯小写(如 report_date)，统一转大写比对。
    lookup = {k.upper(): v for k, v in data.items()}
    missing = []

    def repl(m):
        key = m.group(1).upper()
        if key in lookup and lookup[key] is not None:
            return str(lookup[key])
        missing.append(m.group(1))
        return m.group(0)

    html = PLACEHOLDER.sub(repl, html)

    if missing:
        uniq = sorted(set(missing))
        print("警告: 以下占位符未在数据中提供，已保留原样: " + ", ".join(uniq), file=__import__('sys').stderr)

    with open(args.out, 'w', encoding='utf-8') as f:
        f.write(html)

    print("已生成 {} ({} bytes)".format(args.out, os.path.getsize(args.out)))


if __name__ == '__main__':
    main()
