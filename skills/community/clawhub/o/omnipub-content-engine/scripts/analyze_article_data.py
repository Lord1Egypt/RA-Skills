#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OmniPub Content Engine - 数据复盘分析器
粘贴公众号/头条后台数据 -> 趋势对比 -> 归因诊断 -> HTML复盘报告

用法:
  python analyze_article_data.py --csv "平台,标题,发布时间,阅读量,曝光,涨粉,转发,在看,评论,完读率,分享率" 
  python analyze_article_data.py --file data.csv
  python analyze_article_data.py --demo          # 内置示例数据演示

CSV表头(顺序固定, 逗号分隔):
  平台, 标题, 发布时间, 阅读量, 曝光量, 涨粉, 转发, 在看(公众号)/评论(头条), 评论数, 完读率%, 分享率%
  # 平台: 公众号 或 头条
  # 曝光量: 公众号可留空(0), 头条填推荐量
"""
import argparse
import csv
import io
import json
import os
import sys
from datetime import datetime

BRAND = "心明增长实验室"
COLORS = {"green": "#639922", "purple": "#534AB7", "blue": "#2196F3",
          "amber": "#BA7517", "red": "#A32D2D", "gray": "#888780"}

FIELDS = ["platform", "title", "pub_time", "reads", "views", "followers",
          "shares", "likes", "comments", "finish_rate", "share_rate"]

HEADER_MAP = {"平台": "platform", "标题": "title", "发布时间": "pub_time",
              "阅读量": "reads", "曝光量": "views", "涨粉": "followers",
              "转发": "shares", "在看": "likes", "评论": "comments",
              "完读率": "finish_rate", "分享率": "share_rate"}

DEMO_CSV = """平台,标题,发布时间,阅读量,曝光量,涨粉,转发,在看,评论,完读率,分享率
公众号,《命力：你的底层驱动力系统》,2026-08-10 20:00,1280,0,46,52,31,9,48,4.1
公众号,《道力：建立人生坐标系》,2026-08-12 20:00,860,0,22,21,12,4,35,2.4
头条,《命力：你的底层驱动力系统》,2026-08-10 20:10,6200,98000,35,120,0,28,19,1.9
头条,《道力：建立人生坐标系》,2026-08-12 20:10,2400,76000,18,45,0,9,11,1.9
"""


def parse_csv(raw: str) -> list:
    reader = csv.DictReader(io.StringIO(raw.strip()))
    rows = []
    for r in reader:
        mapped = {HEADER_MAP.get(k.strip(), k.strip()): v for k, v in r.items()}
        row = {k: mapped.get(k, "").strip() for k in FIELDS}
        try:
            row["reads"] = int(float(row["reads"] or 0))
            row["views"] = int(float(row["views"] or 0))
            row["followers"] = int(float(row["followers"] or 0))
            row["shares"] = int(float(row["shares"] or 0))
            row["likes"] = int(float(row["likes"] or 0))
            row["comments"] = int(float(row["comments"] or 0))
            row["finish_rate"] = float(row["finish_rate"] or 0)
            row["share_rate"] = float(row["share_rate"] or 0)
        except ValueError as e:
            print(f"[警告] 跳过无法解析的行: {r.get('title','?')} ({e})")
            continue
        rows.append(row)
    return rows


def ctr(row) -> float:
    """点击率: 阅读/曝光 (头条); 公众号无曝光返回None"""
    if row["platform"] == "头条" and row["views"] > 0:
        return round(row["reads"] / row["views"] * 100, 2)
    return None


def diagnose(rows: list) -> list:
    """归因诊断: 输出 [问题, 严重度(高/中/低), 诊断, 建议]"""
    findings = []
    if not rows:
        return findings

    # 全局均值基准
    avg_reads = sum(r["reads"] for r in rows) / len(rows)
    avg_followers = sum(r["followers"] for r in rows) / len(rows)

    for r in rows:
        title = r["title"][:18]
        reads = r["reads"]
        r_ctr = ctr(r)

        # 问题2: 有热度没浏览量 (头条: 曝光高但点击低)
        if r_ctr is not None and r["views"] >= 30000 and r_ctr < 8:
            findings.append({
                "severity": "高", "title": title, "type": "有热度没浏览量",
                "detail": f"曝光 {r['views']:,} 但点击率仅 {r_ctr}%（行业经验基准 8-15%）。说明推荐给量了，但标题/封面/首段没接住。",
                "action": "重写标题钩子（数字/冲突/悬念三选一）；检查封面图信息量与标题一致性；头条首段是否3秒给结论。"
            })
        # 问题1: 整体没数据
        elif reads < avg_reads * 0.5:
            findings.append({
                "severity": "中", "title": title, "type": "整体没数据",
                "detail": f"阅读 {reads} 低于同批均值 {avg_reads:.0f} 的 50%。",
                "action": "回溯选题评分卡：热度是否误判/发布时机是否过峰；检查是否被限流（违规词/诱导）；账号垂直度是否足够。"
            })
        # 问题3: 有点击没完读
        if r["finish_rate"] and r["finish_rate"] < 30:
            findings.append({
                "severity": "中", "title": title, "type": "点开没读完",
                "detail": f"完读率 {r['finish_rate']}%（基准 40%+）。标题兑现了，但中段流失严重。",
                "action": "段落砍30%信息冗余；小标题明示收益；每500字问一次'关读者什么事'。"
            })
        # 问题4: 完读不错但不涨粉/不互动
        if r["finish_rate"] and r["finish_rate"] >= 40 and r["followers"] < 20:
            findings.append({
                "severity": "低", "title": title, "type": "读完不转化",
                "detail": f"完读率 {r['finish_rate']}% 不错，但涨粉仅 {r['followers']}。",
                "action": "文末CTA不够具体：加'关注回复关键词领资料'；推荐阅读挂同主题高价值文章。"
            })

    # 跨平台对比
    wx = [r for r in rows if r["platform"] == "公众号"]
    tt = [r for r in rows if r["platform"] == "头条"]
    if wx and tt:
        wx_avg = sum(r["reads"] for r in wx) / len(wx)
        tt_avg = sum(r["reads"] for r in tt) / len(tt)
        if tt_avg > wx_avg * 3:
            findings.append({
                "severity": "低", "title": "跨平台", "type": "头条>公众号",
                "detail": f"头条均读 {tt_avg:.0f} 远高于公众号 {wx_avg:.0f}。",
                "action": "公众号侧优化标题与封面（公众号靠打开率）；内容向头条倾斜首发。"
            })
    return findings


def render_html(rows: list, findings: list) -> str:
    """生成复盘报告 HTML（品牌色系）"""
    if not rows:
        return "<p>无数据可分析</p>"
    avg_reads = sum(r["reads"] for r in rows) / len(rows)
    rows_sorted = sorted(rows, key=lambda r: r["reads"], reverse=True)

    cards = ""
    for r in rows_sorted:
        c = ctr(r)
        c_str = f"{c}%" if c is not None else "—"
        cards += f"""
        <div style="background:#fff;border:1px solid #eee;border-radius:10px;padding:14px 16px;margin:10px 0;">
          <div style="display:flex;justify-content:space-between;align-items:center;">
            <span style="font-weight:500;color:#2C2C2A;font-size:14px;">{r['title']}</span>
            <span style="background:{COLORS['green']};color:#fff;border-radius:4px;padding:2px 8px;font-size:12px;">{r['platform']}</span>
          </div>
          <div style="display:flex;gap:18px;margin-top:10px;color:#555;font-size:13px;flex-wrap:wrap;">
            <span>阅读 <b style="color:{COLORS['blue']};">{r['reads']:,}</b></span>
            <span>曝光 <b>{r['views']:,}</b></span>
            <span>点击率 <b>{c_str}</b></span>
            <span>完读 <b>{r['finish_rate']}%</b></span>
            <span>涨粉 <b style="color:{COLORS['purple']};">{r['followers']}</b></span>
            <span>转发 <b>{r['shares']}</b></span>
            <span>评论 <b>{r['comments']}</b></span>
          </div>
        </div>"""

    findings_html = ""
    if findings:
        sev_color = {"高": COLORS["red"], "中": COLORS["amber"], "低": COLORS["blue"]}
        for f in findings:
            findings_html += f"""
            <div style="background:#fff;border:1px solid #eee;border-left:4px solid {sev_color.get(f['severity'],COLORS['gray'])};border-radius:8px;padding:12px 16px;margin:10px 0;">
              <div style="display:flex;gap:10px;align-items:center;margin-bottom:6px;">
                <span style="background:{sev_color.get(f['severity'],COLORS['gray'])};color:#fff;border-radius:4px;padding:1px 8px;font-size:12px;">{f['severity']}</span>
                <span style="font-weight:500;color:#2C2C2A;font-size:14px;">{f['type']}</span>
                <span style="color:#999;font-size:12px;">{f['title']}</span>
              </div>
              <p style="margin:4px 0;color:#555;font-size:13px;line-height:1.6;">{f['detail']}</p>
              <p style="margin:4px 0;color:{COLORS['purple']};font-size:13px;line-height:1.6;"><b>建议：</b>{f['action']}</p>
            </div>"""
    else:
        findings_html = f'<div style="background:{COLORS["green"]}22;border:1px solid {COLORS["green"]};border-radius:8px;padding:14px 16px;color:#3B6D11;font-size:14px;">表现健康，无明显归因问题。继续保持同选题节奏。</div>'

    return f"""<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="utf-8">
<title>内容复盘报告 - {BRAND}</title></head>
<body style="margin:0;background:#f7f7f5;font-family:-apple-system,'PingFang SC','Microsoft YaHei',sans-serif;">
<div style="max-width:760px;margin:0 auto;padding:28px 20px;">
  <h1 style="font-size:20px;font-weight:500;color:#2C2C2A;margin:0 0 4px;">内容数据复盘报告</h1>
  <p style="color:#888;font-size:13px;margin:0 0 20px;">{BRAND} · 生成于 {datetime.now().strftime('%Y-%m-%d %H:%M')} · 共 {len(rows)} 篇</p>

  <div style="background:#fff;border:1px solid #eee;border-radius:12px;padding:16px 20px;margin-bottom:20px;">
    <p style="font-size:14px;color:#555;margin:0;">同批文章平均阅读 <b style="color:{COLORS['blue']};">{avg_reads:.0f}</b> · 最高单篇 <b style="color:{COLORS['purple']};">{rows_sorted[0]['reads']:,}</b>（{rows_sorted[0]['title'][:12]}…）</p>
  </div>

  <h2 style="font-size:16px;font-weight:500;color:{COLORS['green']};margin:20px 0 10px;">文章表现</h2>
  {cards}

  <h2 style="font-size:16px;font-weight:500;color:{COLORS['green']};margin:24px 0 10px;">归因诊断</h2>
  {findings_html}

  <p style="color:#aaa;font-size:12px;margin-top:28px;text-align:center;">数据来源：平台后台导出 · 复盘结论建议回流选题库 · {BRAND}</p>
</div>
</body></html>"""


def main():
    ap = argparse.ArgumentParser(description="OmniPub 数据复盘分析器")
    ap.add_argument("--csv", help="直接传CSV字符串（逗号分隔）")
    ap.add_argument("--file", help="从CSV文件读取")
    ap.add_argument("--demo", action="store_true", help="用示例数据演示")
    ap.add_argument("--out", default="08-复盘报告.html", help="输出HTML路径")
    args = ap.parse_args()

    raw = ""
    if args.demo:
        raw = DEMO_CSV
    elif args.file:
        with open(args.file, "r", encoding="utf-8-sig") as f:
            raw = f.read()
    elif args.csv:
        raw = args.csv
    else:
        print("请提供数据：--csv \"...\" 或 --file data.csv 或 --demo")
        sys.exit(1)

    rows = parse_csv(raw)
    if not rows:
        print("没有解析到有效数据行。")
        sys.exit(1)

    findings = diagnose(rows)
    html = render_html(rows, findings)
    with open(args.out, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"[完成] 分析 {len(rows)} 篇，归因发现 {len(findings)} 条。报告已输出: {args.out}")
    for f in findings:
        print(f"  [{f['severity']}] {f['type']} | {f['title']}")


if __name__ == "__main__":
    main()
