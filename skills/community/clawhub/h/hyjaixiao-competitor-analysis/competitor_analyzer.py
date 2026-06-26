#!/usr/bin/env python3
"""
Competitor Analyzer v1.0 - 竞品分析神器
标准付费版 ¥39.9

输入你的产品/业务，自动分析竞品，输出结构化竞品报告

用法:
  python3 competitor_analyzer.py --product "我的产品" --competitors "竞品A,竞品B,竞品C"
  python3 competitor_analyzer.py --product "AI视频生成器" --competitors "剪映,Pika,RunwayML,HeyGen" --output ./report

依赖:
  pip install requests
  OpenAI API Key (或兼容API)
"""

import os
import sys
import json
import time
import argparse
import hashlib
from pathlib import Path
from datetime import datetime

VERSION = "1.0.0"

# ========== 配置 ==========

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
OPENAI_BASE = os.environ.get("OPENAI_BASE", "https://api.openai.com/v1")
OPENAI_MODEL = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")

OUTPUT_DIR = Path(os.environ.get("CA_OUTPUT_DIR", "./ca_output"))

# 如果没有OpenAI Key，使用内置模板（免费模式）
FREE_MODE = os.environ.get("CA_FREE_MODE", "false").lower() == "true"

# ========== 分析框架 Prompt ==========

ANALYSIS_PROMPT = """你是一位资深竞品分析师。请对以下产品进行全面的竞品分析。

【我的产品】{product}
【产品类别】{category}
【我的核心优势】{strengths}
【目标市场】{market}
【竞品列表】{competitors}

请按以下结构生成分析报告：

## 一、行业概览
- 市场规模与趋势
- 主要玩家格局
- 进入壁垒

## 二、竞品逐一分析（每个竞品独立分析）

### [竞品名称]
- **产品定位**: 一句话描述
- **目标用户**: 核心用户画像
- **核心功能**: 3-5个关键功能
- **定价策略**: 价格区间/模式
- **差异优势**: 对比我的产品的优势
- **弱点**: 对比我的产品的劣势
- **市场口碑**: 用户反馈简评（可合理推断）
- **近半年动态**: 可能的新功能或战略方向

## 三、对比矩阵

| 维度 | 我的产品 | 竞品1 | 竞品2 | 竞品3 |
|------|---------|-------|-------|-------|
| 价格 | | | | |
| 功能深度 | | | | |
| 易用性 | | | | |
| 目标用户契合度 | | | | |
| 品牌影响力 | | | | |
| 技术创新度 | | | | |

评分：★★★★★ / ★★★★☆ / ★★★☆☆ / ★★☆☆☆ / ★☆☆☆☆

## 四、战略建议

基于以上分析，给出3-5条可执行的竞争策略：
1. 短期（1-3个月）：最容易切入的机会点
2. 中期（3-6个月）：需要资源投入的差异化方向
3. 长期（6-12个月）：构建护城河的方向

## 五、风险预警
- 可能被竞品反超的风险点
- 需要关注的市场变化

要求：
1. 分析要有逻辑，不能模糊
2. 对比要有依据，可合理推断
3. 建议要可执行，不能纸上谈兵
4. 语气专业但不废话
5. 每个竞品独立成段，便于阅读

直接输出完整报告，Markdown格式。"""

# ========== 内置模板（免费模式用） ==========

def generate_template_report(product, category, strengths, market, competitors_list):
    """生成基于规则的分析报告模板（免费模式）"""
    now = datetime.now().strftime("%Y-%m-%d")
    
    report = f"""# 竞品分析报告：{product}

> 生成日期：{now} | 分析模式：模板分析
> 提示：本报告为框架模板，核心分析需结合AI LLM完成。

---

## 一、行业概览

**产品类别：** {category}
**目标市场：** {market}
**核心优势：** {strengths}

### 市场格局
本报告涉及的{len(competitors_list)}个竞品：{', '.join(competitors_list)}

---

## 二、竞品逐一分析

"""
    for i, comp in enumerate(competitors_list, 1):
        report += f"""### {i}. {comp}

| 维度 | 描述 |
|------|------|
| **产品定位** | [需分析] |
| **目标用户** | [需分析] |
| **核心功能** | [需分析] |
| **定价策略** | [需分析] |
| **差异优势** | [需分析] |
| **弱点** | [需分析] |
| **市场口碑** | [需分析] |

---
"""
    
    report += f"""
## 三、对比矩阵

| 维度 | {product} | {' | '.join(competitors_list)} |
|------|{'-' * len(product)}|{'|'.join(['-' * len(c) for c in competitors_list])}|
| 价格 | ★★★☆☆ | {' | '.join(['★★★☆☆'] * len(competitors_list))} |
| 功能深度 | ★★★☆☆ | {' | '.join(['★★★☆☆'] * len(competitors_list))} |
| 易用性 | ★★★☆☆ | {' | '.join(['★★★☆☆'] * len(competitors_list))} |
| 目标用户契合度 | ★★★☆☆ | {' | '.join(['★★★☆☆'] * len(competitors_list))} |
| 品牌影响力 | ★★★☆☆ | {' | '.join(['★★★☆☆'] * len(competitors_list))} |
| 技术创新度 | ★★★☆☆ | {' | '.join(['★★★☆☆'] * len(competitors_list))} |

---

## 四、战略建议

1. **短期（1-3个月）**：[需分析]
2. **中期（3-6个月）**：[需分析]
3. **长期（6-12个月）**：[需分析]

---

## 五、风险预警

- [需分析]

---

> 💡 **提示:** 如需深度分析报告（含AI生成的具体竞品洞察、评分和战略建议），请设置 OPENAI_API_KEY。
"""
    return report


# ========== 工具函数 ==========

def log(msg):
    ts = time.strftime("%H:%M:%S")
    print(f"[{ts}] {msg}", flush=True)

def ensure_dir(d):
    Path(d).mkdir(parents=True, exist_ok=True)


# ========== 核心 ==========

def generate_report(product, category, strengths, market, competitors):
    """调用LLM生成竞品分析报告"""
    if not OPENAI_API_KEY:
        log("⚠️ 未设置 OPENAI_API_KEY，使用模板模式（评分和建议需要手动填写）")
        return generate_template_report(product, category, strengths, market, competitors)

    import requests

    prompt = ANALYSIS_PROMPT.format(
        product=product,
        category=category or "未指定",
        strengths=strengths or "未指定",
        market=market or "未指定",
        competitors="\n".join([f"- {c}" for c in competitors])
    )

    log(f"  调用 {OPENAI_MODEL} 分析 {len(competitors)} 个竞品...")

    try:
        resp = requests.post(
            f"{OPENAI_BASE}/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENAI_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": OPENAI_MODEL,
                "messages": [
                    {"role": "system", "content": "你是顶尖的商业分析师和竞争策略顾问。输出结构清晰、分析深入、建议可执行的竞品分析报告。"},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.5,
                "max_tokens": 6000
            },
            timeout=180
        )
        data = resp.json()
        if "choices" in data and len(data["choices"]) > 0:
            content = data["choices"][0]["message"]["content"]
            # 去除可能的```markdown包装
            if content.startswith("```"):
                lines = content.split("\n")
                if lines[0].strip().startswith("```"):
                    lines = lines[1:]
                if lines and lines[-1].strip() == "```":
                    lines = lines[:-1]
                content = "\n".join(lines)
            log(f"  ✅ 报告生成完成 ({len(content)}字符)")
            return content
        else:
            err = data.get("error", {}).get("message", "未知错误")
            log(f"  ❌ API错误: {err}")
            return generate_template_report(product, category, strengths, market, competitors)
    except Exception as e:
        log(f"  ❌ 请求失败: {e}")
        return generate_template_report(product, category, strengths, market, competitors)


def save_report(product, report, output_dir):
    """保存报告"""
    safe_name = product.replace("/", "_").replace(" ", "_")[:30]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"竞品分析_{safe_name}_{timestamp}.md"
    filepath = output_dir / filename

    filepath.write_text(report, encoding="utf-8")
    log(f"  💾 已保存: {filepath}")
    return filepath


def list_history(output_dir):
    """列出历史报告"""
    files = sorted(output_dir.glob("*.md"))
    if not files:
        log("暂无历史报告")
        return

    log(f"\n📚 历史报告 ({len(files)}份)")
    log("-" * 60)
    for f in files:
        size = f.stat().st_size
        modified = datetime.fromtimestamp(f.stat().st_mtime).strftime("%m-%d %H:%M")
        name = f.stem
        log(f"  {modified}  {size:>6}B  {name}")


def quick_check(product, competitors):
    """快速竞品检查（轻量版）"""
    log(f"\n⚡ 快速竞品概览")

    report = f"""# 竞品快速检查：{product}

> 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}
> 模式：快速概览

---

## 竞品列表

"""
    for i, comp in enumerate(competitors, 1):
        report += f"{i}. **{comp}** — [需深度分析]\n"

    report += f"""
## 初步判断

建议对这 {len(competitors)} 个竞品做深度分析，使用命令：

```bash
python3 competitor_analyzer.py \\
  --product "{product}" \\
  --competitors "{','.join(competitors)}"
```

或加上产品信息做精准分析：

```bash
python3 competitor_analyzer.py \\
  --product "{product}" \\
  --competitors "{','.join(competitors)}" \\
  --strengths "你的核心优势" \\
  --market "你的目标市场"
```
"""
    return report


# ========== 主流程 ==========

def main():
    parser = argparse.ArgumentParser(description=f"竞品分析神器 v{VERSION}")
    parser.add_argument("--product", required=True, help="你的产品/业务名称")
    parser.add_argument("--competitors", required=True, help="竞品列表，逗号分隔")
    parser.add_argument("--category", help="产品类别 (可选)", default="")
    parser.add_argument("--strengths", help="你的核心优势 (可选)", default="")
    parser.add_argument("--market", help="目标市场 (可选)", default="")
    parser.add_argument("--quick", action="store_true", help="快速检查模式（不生成深度分析）")
    parser.add_argument("--output", default=None, help="输出目录")
    parser.add_argument("--history", action="store_true", help="查看历史报告")
    args = parser.parse_args()

    global OUTPUT_DIR
    if args.output:
        OUTPUT_DIR = Path(args.output)
    else:
        OUTPUT_DIR = OUTPUT_DIR / datetime.now().strftime("%Y%m%d")

    ensure_dir(OUTPUT_DIR)

    if args.history:
        list_history(OUTPUT_DIR)
        return

    competitors = [c.strip() for c in args.competitors.split(",") if c.strip()]

    log(f"{'='*50}")
    log(f"📊 竞品分析神器 v{VERSION}")
    log(f"产品: {args.product}")
    log(f"竞品: {', '.join(competitors)}")
    log(f"模式: {'快速概览' if args.quick else '深度分析'}")
    log(f"{'='*50}")

    if args.quick:
        report = quick_check(args.product, competitors)
    else:
        report = generate_report(
            args.product, args.category, args.strengths,
            args.market, competitors
        )

    filepath = save_report(args.product, report, OUTPUT_DIR)

    # 显示报告摘要（前50行）
    lines = report.split("\n")
    print("\n" + "\n".join(lines[:50]))
    if len(lines) > 50:
        print(f"\n... (共 {len(lines)} 行，完整报告见文件)")

    log(f"\n{'='*50}")
    log(f"✅ 完成！报告体积: {len(report)}字符")
    log(f"📂 输出: {filepath}")
    log(f"\n💡 提示: 使用 --history 查看所有历史报告")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        log("\n⚠️ 用户中断")
        sys.exit(1)
    except Exception as e:
        log(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
