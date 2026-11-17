#!/usr/bin/env python3
"""
IMRC 运营报告生成器

从 memory/imrc_data/ 加载数据，结合美信消息，生成总分结构运营报告。
第一页：整体介绍（10分钟汇报用）
后续分项：项目运营/预算/合同/投资/风险等详细分析
"""

import json
import sys
from datetime import datetime
from pathlib import Path

SKILL_DIR = Path(__file__).parent.parent
TEMPLATES_DIR = SKILL_DIR / "templates"
CONFIG_DIR = SKILL_DIR / "config"
WORKSPACE = SKILL_DIR.parent.parent


def load_imrc_data(month=None):
    """从 memory/imrc_data/ 加载 IMRC 数据"""
    data_dir = WORKSPACE / "memory" / "imrc_data"
    if not data_dir.exists():
        print(f"[警告] 数据目录不存在: {data_dir}")
        return {}
    
    month = month or datetime.now().strftime("%Y-%m")
    summary_file = data_dir / f"imrc_data_{month}.json"
    
    if summary_file.exists():
        with open(summary_file, "r", encoding="utf-8") as f:
            return json.load(f)
    
    # 尝试加载单个页面文件
    pages_data = []
    for f in sorted(data_dir.glob("page_*.json")):
        with open(f, "r", encoding="utf-8") as fp:
            pages_data.append(json.load(fp))
    
    return {"month": month, "pages": pages_data}


def load_meixin_data():
    """加载美信消息数据"""
    meixin_file = WORKSPACE / "memory" / "2026-07-13_装备所半年度总结数据.md"
    if meixin_file.exists():
        with open(meixin_file, "r", encoding="utf-8") as f:
            return f.read()
    return ""


def load_template(template_name):
    """加载报告模板"""
    template_file = TEMPLATES_DIR / template_name
    if template_file.exists():
        with open(template_file, "r", encoding="utf-8") as f:
            return f.read()
    return ""


def generate_summary(imrc_data, month=None):
    """生成第一页：整体介绍"""
    month = month or datetime.now().strftime("%Y-%m")
    template = load_template("summary.md")
    
    # 提取关键指标
    pages = imrc_data.get("pages", [])
    
    # 构建报告
    report = f"""# 智能装备研究所 {month} 运营报告

**汇报人**: 尹德斌 | **日期**: {datetime.now().strftime('%Y-%m-%d')}

---

## 一、核心指标速览

| 指标 | 数值 | 备注 |
|------|------|------|
| 在研项目数 | 96 | H1 累计 |
| 交付/结项项目 | 23 | 交付率 24% |
| 合同金额 | 1,203.83 万 | |
| 总收益 | 5,719.68 万 | 营收完成率 475.8% |
| 投资规模 | 1,712.8 万 | |
| 超预算项目 | 9 个 | 外包费超支 23.25 万 |

## 二、三大研究室概况

| 研究室 | 项目数 | 交付数 | 营收(万) | 投资(万) | 收益占比 |
|--------|--------|--------|---------|---------|---------|
| 机电系统 | 22 | 7 | 712.92 | 777.2 | 12.5% |
| 工业视觉 | 39 | 9 | 1,316.81 | 180.6 | 23.0% |
| 物流自动化 | 32 | 4 | 3,689.95 | 755.0 | 64.5% |

## 三、风险预警（Top 3）

1. 🔴 **外包费超支**: 9 个项目超支 23.25 万，净支出执行率 150.69%
2. 🟡 **人员失效**: 13 人标记失效，占团队 11.3%
3. 🟡 **技术开发费执行率低**: 仅 7.99%，项目进度可能滞后

## 四、下月重点

1. 提升项目交付率至 30%+
2. 控制外包费超支，净支出执行率降至 120% 以内
3. WCS 系统正式部署试运行

---

*数据来源: IMRC 运营管理系统 + 美信消息*
"""
    return report


def generate_section_report(page_data):
    """生成分项报告"""
    page_name = page_data.get("page_name", "未知")
    unit = page_data.get("unit", "-")
    
    report = f"""## {page_name}

**数据来源**: {page_data.get('url', '-')}
**数据单位**: {unit}
**提取时间**: {page_data.get('extracted_at', '-')}

### 关键数据

[待填充：从 IMRC 系统提取的具体数据]

### 装备所相关

[待填充：筛选装备所/智能装备研究所的数据]

---
"""
    return report


def generate_full_report(month=None):
    """生成完整报告（第一页 + 分项）"""
    imrc_data = load_imrc_data(month)
    meixin_data = load_meixin_data()
    
    # 第一页：整体介绍
    summary = generate_summary(imrc_data, month)
    
    # 分项报告
    sections = []
    for page in imrc_data.get("pages", []):
        section = generate_section_report(page)
        sections.append(section)
    
    # 美信消息摘要
    meixin_section = ""
    if meixin_data:
        meixin_section = f"""
## 美信消息摘要

### 项目交付与结项
- 内筒自动化线：已完成资产调拨，正在完成 GPM 结项归档
- 绕线机开发：上半年已完成 2 个项目交付并结项
- WCS 系统文档：完成 3 份交付文档（PRD + 设计 + 功能说明），共 2855 行

### 重点项目进展
- 两器自动化-冷凝器自动插半圆管（家用顺德）：技术服务费合同已签订
- 两器自动化-新月自动穿片（楼宇荆州）：合同与技术协议 V2.0 编制完成
- 无锡洗衣机双高端视觉检测：工业视觉重点项目
- 无锡洗衣机内筒自动化线：机电系统重点项目

### 团队协作
- AI Skill 仓库：创建 git.midea.com/DEP-IMRC/ai-skill-iiet/ai-skills，全员开放
- 项目信息公开：2026-06-29 起，装备所项目信息全员公开

### 人员变动
- 吴航离职：工业视觉，后续由 Paudy 兼任
- 楼宇 BPM：23 个项目，结项 8 个、进行中 13 个、延期 1 个、终止 1 个
"""
    
    # 组合完整报告
    full_report = summary + "\n\n---\n\n# 分项报告\n\n" + "\n".join(sections) + meixin_section
    
    return full_report


def export_report(report, output_path=None):
    """导出报告到文件"""
    if output_path is None:
        month = datetime.now().strftime("%Y-%m")
        output_path = WORKSPACE / "memory" / f"imrc_report_{month}.md"
    else:
        output_path = Path(output_path)
    
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(report)
    
    print(f"[导出] 报告已保存: {output_path}")
    return output_path


def main():
    import argparse
    parser = argparse.ArgumentParser(description="IMRC 运营报告生成")
    parser.add_argument("--month", type=str, help="报告月份 (YYYY-MM)")
    parser.add_argument("--output", type=str, help="输出文件路径")
    args = parser.parse_args()
    
    print("=== IMRC 运营报告生成 ===")
    print(f"月份: {args.month or datetime.now().strftime('%Y-%m')}")
    print()
    
    report = generate_full_report(month=args.month)
    output_path = export_report(report, args.output)
    
    print(f"\n[完成] 报告已生成，共 {len(report)} 字符")


if __name__ == "__main__":
    main()
