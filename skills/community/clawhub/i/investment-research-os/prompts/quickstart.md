# Investment Research OS — 快速使用指南

## 一分钟上手

### 方式1：命令行（最快）
```bash
cd ~/.qclaw/workspace
python scripts/investment_research_os.py \
  --target "腾讯" \
  --question "市场是否低估腾讯未来3年的盈利增长？" \
  --horizon "中期" \
  --objective "买入"
```

### 方式2：获取数据 + 生成报告
```bash
python scripts/investment_research_os.py \
  --target "英伟达" \
  --question "英伟达的AI芯片垄断地位能维持多久？" \
  --fetch-data
```

### 方式3：AI对话（最完整）
直接对我说：
```
研究腾讯，市场是否低估腾讯未来3年的盈利增长？
```
我会执行完整10层研究流程，给你最终的CIO裁决。

---

## 研究流程

```
用户输入（投资问题）
        ↓
Layer 0: 投资问题重构
        ↓
数据采集（NeoData + OpenAlex + World Bank）
        ↓
┌─────────────────────────────────────────┐
│  6个Agent并行研究（可选）：               │
│  Agent1 行业分析师 → 行业状态机          │
│  Agent2 公司分析师 → 6维度框架           │
│  Agent3 财务分析师 → 盈利质量+仓位       │
│  Agent4 估值分析师 → 三情景估值           │
│  Agent5 预期差分析师 → 共识vs反共识       │
│  Agent6 红队分析师 → 做空逻辑            │
└─────────────────────────────────────────┘
        ↓
CIO裁决 → 投资结论 + 仓位
        ↓
报告保存 → research/{公司}_{日期}.md
```

---

## 核心五问

研究任何标的都必须回答：

1. **市场定价什么？** → 当前估值反映了什么预期？
2. **市场错在哪里？** → 预期差在哪里？
3. **预期差有多大？** → 量化差距
4. **赔率风险比如何？** → 三情景概率加权
5. **如何下注？** → 仓位 + 止损

---

## 报告模板

生成的报告包含10个Layer：
- Layer 0：投资问题定义
- Layer 1：行业状态机
- Layer 2：公司分析框架
- Layer 3：护城河评分
- Layer 4：财务数据
- Layer 5：预期差分析（核心）
- Layer 6：三情景估值
- Layer 7：催化剂系统
- Layer 8：红队报告
- Layer 9：投资结论（CIO）
- Layer 10：仓位建议

---

## 快速 vs 完整研究

| 模式 | 时间 | 覆盖 |
|------|------|------|
| 快速研究 | 5分钟 | Layer0→4→8→9，跳过红队 |
| 完整研究 | 15-20分钟 | 全部10层 |
| 比较研究 | 20分钟 | 多标的并行→CIO排序 |

---

## 文件结构

```
skills/investment-research-os/
├── SKILL.md              # 主技能定义
└── prompts/
    ├── master.md         # 主控台提示词
    ├── agent1-industry.md
    ├── agent2-company.md
    ├── agent3-financial.md
    ├── agent4-valuation.md
    ├── agent5-expectation-gap.md
    ├── agent6-redteam.md
    ├── cio.md
    └── quickstart.md     # 本文件

scripts/
└── investment_research_os.py  # 研究执行器

research/
└── research_{公司}_{日期}.md  # 生成的研究报告
```

---

## 常见投资问题示例

```
研究英伟达，AI芯片需求是否被高估？
研究腾讯，视频号广告增长能否持续？
研究苹果，AI功能对iPhone销量影响多大？
研究特斯拉，Robotaxi落地概率有多少？
研究贵州茅台，消费降级对高端白酒影响？
```
