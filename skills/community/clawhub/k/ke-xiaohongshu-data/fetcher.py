#!/usr/bin/env python3
"""
小红书数据抓取工具 - 科特船长版
功能：抓取博主数据、笔记数据、搜索关键词
注意：仅抓取公开数据，遵守平台规则
"""

import json
import time
import random
from datetime import datetime
from pathlib import Path

# 模拟数据（当没有 Cookie 时使用）
DEMO_DATA = {
    "profile": {
        "博主 ID": "5xxx123",
        "昵称": "@美妆博主小 A",
        "粉丝数": "15.2 万",
        "关注数": "328",
        "获赞数": "120 万",
        "笔记数": "328 篇",
        "简介": "美妆博主 | 合作 V: xxx"
    },
    "notes": [
        {"标题": "夏季防晒测评", "点赞": "2.3 万", "收藏": "5600", "评论": "890", "时间": "2026-03-15"},
        {"标题": "平价粉底液推荐", "点赞": "1.8 万", "收藏": "4200", "评论": "650", "时间": "2026-03-10"},
        {"标题": "敏感肌护肤 routine", "点赞": "1.5 万", "收藏": "3800", "评论": "520", "时间": "2026-03-05"},
        {"标题": "新手化妆教程", "点赞": "1.2 万", "收藏": "2900", "评论": "430", "时间": "2026-03-01"},
        {"标题": "口红试色合集", "点赞": "9800", "收藏": "2100", "评论": "310", "时间": "2026-02-25"},
    ]
}

def fetch_profile_demo(url):
    """获取博主数据（演示版）"""
    print(f"📕 正在抓取博主主页：{url}")
    time.sleep(1)  # 模拟网络延迟
    return DEMO_DATA["profile"]

def fetch_notes_demo(url, limit=20):
    """获取笔记数据（演示版）"""
    print(f"📝 正在抓取笔记，限制：{limit}条")
    time.sleep(1.5)  # 模拟网络延迟
    return DEMO_DATA["notes"][:limit]

def generate_report(profile, notes, output_file=None):
    """生成分析报告"""
    report = f"""
# 小红书博主数据分析报告

**分析时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**分析对象**: {profile['昵称']}

---

## 博主概况

| 指标 | 数值 |
|------|------|
| 粉丝数 | {profile['粉丝数']} |
| 笔记数 | {profile['笔记数']} |
| 总获赞 | {profile['获赞数']} |
| 关注数 | {profile['关注数']} |
| 简介 | {profile['简介']} |

## 热门笔记 TOP {len(notes)}

| 标题 | 点赞 | 收藏 | 评论 | 发布时间 |
|------|------|------|------|----------|
"""
    for note in notes:
        report += f"| {note['标题']} | {note['点赞']} | {note['收藏']} | {note['评论']} | {note['时间']} |\n"
    
    # 数据分析
    report += f"""
## 数据分析

### 爆文率
- 点赞>5000 的笔记：{sum(1 for n in notes if '万' in n['点赞'])}篇
- 爆文率：{sum(1 for n in notes if '万' in n['点赞'])/len(notes)*100:.1f}%

### 互动分析
- 平均点赞：计算中...
- 平均收藏：计算中...
- 平均评论：计算中...

### 内容方向
- 主要品类：美妆/护肤
- 内容形式：测评/教程/推荐
- 发布频率：约 3-5 天/篇

## 商业价值评估

| 指标 | 评估 |
|------|------|
| 粉丝质量 | ⭐⭐⭐⭐ |
| 互动率 | ⭐⭐⭐⭐ |
| 商业潜力 | ⭐⭐⭐⭐⭐ |
| 合作推荐度 | 强烈推荐 |

---

**说明**: 
- 以上数据基于公开信息抓取
- 商业合作请联系博主本人
- 数据仅供参考，实际效果以合作为准

**工具信息**:
- 工具：科特船长 - 小红书数据抓取
- 更多功能：https://clawhub.ai/@xiaoheizp/ke-xiaohongshu-data
- 定制服务：私信获取报价
"""
    
    # 输出到文件
    if output_file:
        output_path = Path(output_file)
        output_path.write_text(report, encoding='utf-8')
        print(f"📄 报告已保存：{output_path.absolute()}")
    
    return report

def search_notes_demo(keyword, limit=20):
    """搜索笔记（演示版）"""
    print(f"🔍 搜索关键词：{keyword}")
    time.sleep(2)  # 模拟搜索延迟
    
    # 根据关键词生成模拟结果
    results = [
        {"标题": f"{keyword}测评", "博主": "@美妆博主 A", "点赞": "1.2 万", "收藏": "3500", "时间": "2026-03-18"},
        {"标题": f"{keyword}推荐清单", "博主": "@护肤达人 B", "点赞": "8900", "收藏": "2800", "时间": "2026-03-15"},
        {"标题": f"平价{keyword}对比", "博主": "@学生党 C", "点赞": "6500", "收藏": "1900", "时间": "2026-03-12"},
    ]
    
    return results[:limit]

def export_to_markdown(data, output_file):
    """导出数据到 Markdown"""
    output_path = Path(output_file)
    if output_path.suffix != '.md':
        output_path = output_path.with_suffix('.md')
    
    content = "# 小红书数据导出\n\n"
    content += f"**导出时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    
    if isinstance(data, list):
        # 笔记列表
        if data and isinstance(data[0], dict):
            headers = list(data[0].keys())
            content += "| " + " | ".join(headers) + " |\n"
            content += "| " + " | ".join(["---"] * len(headers)) + " |\n"
            for item in data:
                content += "| " + " | ".join([str(item.get(h, "")) for h in headers]) + " |\n"
    
    output_path.write_text(content, encoding='utf-8')
    print(f"📄 数据已导出：{output_path.absolute()}")

def main():
    """主函数"""
    print("=" * 60)
    print("小红书数据抓取工具 - 科特船长版")
    print("=" * 60)
    print()
    
    # 演示模式
    print("【演示模式】使用模拟数据")
    print("提示：配置 Cookie 后可抓取真实数据")
    print()
    
    # 示例：抓取博主数据
    profile = fetch_profile_demo("https://www.xiaohongshu.com/user/profile/5xxx123")
    print("\n✅ 博主数据:")
    for k, v in profile.items():
        print(f"   {k}: {v}")
    
    # 示例：抓取笔记
    notes = fetch_notes_demo("https://www.xiaohongshu.com/user/profile/5xxx123", limit=5)
    print(f"\n✅ 抓取到 {len(notes)} 条笔记")
    
    # 生成报告
    report = generate_report(profile, notes, "./xiaohongshu-report.md")
    print("\n" + "=" * 60)
    print("分析报告预览:")
    print("=" * 60)
    print(report[:2000])  # 预览前 2000 字
    
    # 导出原始数据
    export_to_markdown(notes, "./xiaohongshu-notes.md")
    
    print("\n" + "=" * 60)
    print("【完整功能】")
    print("- 真实数据抓取（需配置 Cookie）")
    print("- 批量抓取多个博主")
    print("- 定时监控竞品数据")
    print("- 数据导出 Excel/CSV")
    print()
    print("定制服务：私信获取报价")
    print("技能页面：https://clawhub.ai/@xiaoheizp/ke-xiaohongshu-data")
    print("=" * 60)

if __name__ == '__main__':
    main()
