#!/usr/bin/env python3
"""
build_gsr_series.py — 生成金银比(GSR)近半年序列的 <script> 片段，供日报仪表盘③注入。

用法:
  python3 build_gsr_series.py --current 69.6 --end-date 7/22
  python3 build_gsr_series.py --json gsr_input.json --out gsr_snippet.js

说明:
  - 内置一段"参考重建"序列(1/21–7/21 真实锚点 + 6/18–7/17 真实日度值)，用于无实时数据时的近似骨架。
    真实锚点来源: T-GolDream / IndexMundi 月度均值、格林大华期货半年报极值(1/29 低 45)、
    6/18–7/17 为 T-GolDream 真实日度值。
  - 若提供 --json(含 dates/values 数组)，优先采用真实检索序列(更准确)。
  - 输出的 dates/values/gsrMean 可直接粘贴进 assets/report_template.html 的 #gsrChart 脚本区。
  - 注意: 内置序列会随时间过时，正式日报请以当日联网检索的真实 GSR 为准。
"""
import argparse
import json

# 内置参考序列 (短日期标签 M/D -> GSR)，覆盖 1/21–7/21
BUILTIN = {
    '1/21': 62, '1/24': 55, '1/28': 46, '1/29': 45.0, '1/31': 51,
    '2/7': 57, '2/14': 60, '2/21': 62, '2/28': 61,
    '3/7': 64, '3/14': 66, '3/21': 65, '3/28': 67, '3/31': 67,
    '4/4': 64, '4/11': 62, '4/18': 61, '4/25': 62, '4/30': 63,
    '5/2': 62, '5/9': 60, '5/16': 55, '5/23': 58, '5/30': 60, '5/31': 60,
    '6/1': 59.5, '6/8': 61, '6/13': 63,
    '6/18': 64.09, '6/19': 64.12, '6/20': 63.99, '6/21': 63.99, '6/22': 63.57,
    '6/23': 66.54, '6/24': 67.82, '6/25': 68.96, '6/26': 68.77, '6/27': 68.98,
    '6/28': 68.98, '6/29': 69.34, '6/30': 67.28,
    '7/1': 67.69, '7/2': 67.45, '7/3': 66.76, '7/4': 66.8, '7/5': 66.8, '7/6': 67.04,
    '7/7': 68.1, '7/8': 70.05, '7/9': 68.26, '7/10': 68.46, '7/11': 68.67, '7/12': 68.67,
    '7/13': 69.14, '7/14': 68.89, '7/15': 70.05, '7/16': 71.0, '7/17': 72.05,
    '7/18': 71.9, '7/19': 71.9, '7/20': 71.0, '7/21': 69.6,
}


def build(current=None, end_date=None, json_path=None):
    if json_path:
        with open(json_path, encoding='utf-8') as f:
            d = json.load(f)
        dates = list(d['dates'])
        values = [float(v) for v in d['values']]
    else:
        dates = list(BUILTIN.keys())
        values = list(BUILTIN.values())
        if end_date and current is not None:
            if end_date == dates[-1]:
                values[-1] = current
            else:
                dates.append(end_date)
                values.append(current)
    mean = round(sum(values) / len(values), 2)
    lo = min(values)
    hi = max(values)
    return dates, values, mean, lo, hi


def render(dates, values, mean):
    dates_js = json.dumps(dates, ensure_ascii=False)
    values_js = json.dumps(values)
    head = "// 金银比(GSR)近半年序列 — 由 build_gsr_series.py 生成\n"
    head += "// dates/values 为真实序列(联网检索或内置参考重建)，gsrMean 为半年均值\n"
    return (head
            + "var dates = " + dates_js + ";\n"
            + "var values = " + values_js + ";\n"
            + "var gsrMean = " + str(mean) + ";\n")


def main():
    ap = argparse.ArgumentParser(description="生成金银比近半年序列 <script> 片段")
    ap.add_argument('--current', type=float, help='当日 GSR，覆盖/追加末点')
    ap.add_argument('--end-date', type=str, help='末点短日期标签(如 7/22)，需与内置 M/D 格式一致')
    ap.add_argument('--json', dest='json_path', help='真实 GSR 序列 JSON({dates,values})')
    ap.add_argument('--out', help='输出 .js 片段路径')
    args = ap.parse_args()

    dates, values, mean, lo, hi = build(args.current, args.end_date, args.json_path)
    snippet = render(dates, values, mean)
    stats = "// 统计: 点数={} 均值={} 最低={} 最高={}\n".format(len(values), mean, lo, hi)
    out = stats + snippet

    if args.out:
        with open(args.out, 'w', encoding='utf-8') as f:
            f.write(out)
        print("已写出 {}（{} 点，均值 {}，最低 {}，最高 {}）".format(args.out, len(values), mean, lo, hi))
    else:
        print(out)


if __name__ == '__main__':
    main()
