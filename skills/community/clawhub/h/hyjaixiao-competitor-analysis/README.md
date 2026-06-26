# 📊 竞品分析神器 v1.0 (标准付费版)

> **输入你的产品和竞品，自动输出完整竞品分析报告。**
> 创业、立项、融资前必做的一步。

## 📦 包含文件

```
competitor-analyzer-v1/
├── competitor_analyzer.py    # 主程序 (直接运行)
├── SKILL.md                  # OpenClaw 配置
└── README.md                 # 本文件
```

## 🚀 快速开始

```bash
# 1. 安装
pip install requests

# 2. 设置 API Key (推荐)
export OPENAI_API_KEY="sk-xxx"

# 3. 一键分析
python3 competitor_analyzer.py \
  --product "AI短视频生成器" \
  --competitors "剪映,Pika,RunwayML,HeyGen" \
  --strengths "中文支持好,竖屏优化,自动化程度高" \
  --market "国内自媒体创作者"
```

## 📖 详细用法

### 快速检查模式（不调 API）

```bash
python3 competitor_analyzer.py \
  --product "我的笔记App" \
  --competitors "Notion,飞书,语雀" \
  --quick
```

### 带完整场景信息

```bash
python3 competitor_analyzer.py \
  --product "AI客服机器人" \
  --competitors "智齿科技,网易七鱼,Udesk" \
  --category "SAAS客服工具" \
  --strengths "AI大模型驱动,免训练,即接即用" \
  --market "中小电商企业" \
  --output ./my_reports
```

### 查看历史报告

```bash
python3 competitor_analyzer.py --product "" --history
```

## 📋 报告结构

完整报告包含5大板块：

```
一、行业概览
  ├─ 市场规模与趋势
  ├─ 主要玩家格局
  └─ 进入壁垒

二、竞品逐一分析
  ├─ 产品定位
  ├─ 目标用户
  ├─ 核心功能
  ├─ 定价策略
  ├─ 差异优势
  ├─ 弱点
  ├─ 市场口碑
  └─ 近半年动态

三、对比矩阵（★★★★★评分）
  ├─ 价格
  ├─ 功能深度
  ├─ 易用性
  ├─ 目标用户契合度
  ├─ 品牌影响力
  └─ 技术创新度

四、战略建议
  ├─ 短期（1-3个月）
  ├─ 中期（3-6个月）
  └─ 长期（6-12个月）

五、风险预警
```

## 🔧 环境变量

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `OPENAI_API_KEY` | - | OpenAI API Key (推荐) |
| `OPENAI_BASE` | `https://api.openai.com/v1` | API地址（可换代理/兼容API） |
| `OPENAI_MODEL` | `gpt-4o-mini` | 模型（便宜够用） |
| `CA_OUTPUT_DIR` | `./ca_output` | 输出目录 |
| `CA_FREE_MODE` | `false` | 强制模板模式（不调API） |

## 💰 成本估算

一次深度分析（5个竞品）使用 gpt-4o-mini：
- 输入约 2000 token → ¥0.003
- 输出约 4000 token → ¥0.006
- **总成本 ≈ ¥0.01**

对比请一个商业分析师做竞品报告：¥2000-5000

## 💡 常见问题

**Q: 没有 API Key 能用吗？**
A: 能。不走 API Key 时自动使用模板模式，生成报告框架，你手动填写具体内容。

**Q: 可以分析哪些行业？**
A: 任何行业都可以。AI会基于你的产品描述和竞品名称推断行业情况。

**Q: 报告可以直接用来融资吗？**
A: 建议作为初稿框架使用。AI分析提供方向和逻辑支撑，正式场合建议结合人工调研数据。

**Q: 竞品越多效果越好？**
A: 建议3-5个核心竞品。太多会导致分析深度不足。

---

**版本:** 1.0.0 | **类型:** 标准付费款 | **定价:** ¥39.9
