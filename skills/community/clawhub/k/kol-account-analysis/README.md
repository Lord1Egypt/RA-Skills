# 达人账号深度分析（KOL Account Analysis）

> 把达人分析从"加工过的数据摘要"升级为"一次可以复用的账号理解"：他稳定在讲什么、用户实际接收到了什么、商品能以什么身份进入、合作怎么落地。

## 一句话定位

回答五个问题，五段缺一不可：

> 他稳定在讲什么 + 他具体怎么表达 + 用户实际接收到了什么 + 商品能以什么身份进入 + **合作怎么落地**

前四段是内容与接收理解，最后一段（v2.0 新增）把结论落到具体的**合作形态建议**与**风险清单**，而非停在"适合/不适合"。

## 架构

```
kol-account-analysis/
├── SKILL.md                            # 入口（流程 + 规则速查 + 边界）
├── scripts/
│   └── collect_account.py              # T4 浏览器自动化采集骨架（Playwright）
├── references/
│   ├── task-definition.md              # Step 1 任务定义句五要素 + 样本量自适应
│   ├── platform-context.md             # 平台生态差异与信号校准（v2.0 新增）
│   ├── data-collection.md              # Step 2 证据采集与整理标准
│   ├── data-sources.md                 # 数据来源分层与合规红线
│   ├── collection-playbook.md          # T4 采集执行协议（v2.1 新增）
│   ├── works-analysis.md               # Step 3 读作品（生命周期 + 爆款归因 + 硬广检查）
│   ├── comments-analysis.md            # Step 4 读评论（七维 + 信任资产信号）
│   ├── batch-processing.md             # 评论量大时的批量执行协议
│   ├── collaboration-judgment.md       # Step 5 合作判断（五问 + 合作形态 + 风险清单）
│   ├── honest-boundaries.md            # 职责边界（不做什么）
│   └── rules.md                        # 核心规则完整版（R1-R19）
├── templates/
│   └── report-template.md              # 最终交付报告模板
├── trace-schema.json                   # 执行轨迹契约
└── VERIFICATION.md                     # 部署后验证包
```

## 核心流程（强制顺序，不可跳步）

| Step | 名称 | 门控（不满足则停止） |
|------|------|--------------------|
| 1 | 定义任务与平台语境 | 任务定义句五要素完整 + 平台校准明确，否则不许翻作品 |
| 2 | 采集与整理证据 | 作品清单 + 按作品对应的评论明细 + 口径说明齐备 |
| 3 | 读作品：他稳定在讲什么 | 母题清单 + 数据分布（最低/中位/最高）+ 生命周期阶段判定 |
| 4 | 读评论：用户接收到了什么 | 七维计数表 + 掩盖信号检查 + 信任资产信号 |
| 5 | 合作判断：商品以什么身份进入 | 五问 + 合作形态建议 + 风险清单 + 证据边界声明 |

## 快速开始

```
# 分析单个达人
帮我深度分析一下 @某某达人 的账号，我们想在抖音让他承接新品内容任务
这个博主能不能承接我们的新品内容任务（小红书）

# 合作决策
判断这位达人适不适合我们的商品，应该以什么身份进入，适合什么合作形态

# 风险排查
评估这位达人和我们品牌合作的风险

# 产出 Brief 输入
基于账号分析结论，给我合作 Brief 需要的输入
```

## 核心规则

- 爆款是结果不是原因，只挑爆款看会掉进幸存者偏差
- 不看平均值，看最低值/中位数/最高值
- 标签（"时尚""美妆"）不算分析，内容母题才算
- 母题/做法只有在数据好的作品里反复出现、在数据差的作品里明显少见，才算候选规律
- 平台决定信号权重：同一信号在不同平台含义不同
- 达人有生命周期：上升/成熟/衰退决定合作策略
- 爆款要归因：可复制的（选题/结构）与不可复制的（时机/热点）分开
- 结论要落到合作形态建议，不能停在"适合/不适合"
- 合作前必过风险清单（舆情/立场/粉丝冲突/水军痕迹）
- 评论每类维度都要看到实际数量，有数才有判断
- 公开数据支持不了的结论不能下；商业结果由品牌自有数据回答

## 职责边界（不做什么）

- 按粉丝量/报价/CPM/画像的批量筛选排序
- 投放后的商业效果归因
- 商品卖点价值分析
- 刷量/数据造假鉴定

## 数据来源（证据质量分层）

| 层 | 渠道 | 用途 |
|----|------|------|
| T1 官方平台后台 | 巨量星图 / 蒲公英 / 磁力聚星 / 花火 | 报价、商单表现、真实粉丝画像 |
| T2 官方开放 API | 星图开放平台、授权服务商 API | 结构化达人/商单数据 |
| T3 第三方数据工具 | 蝉妈妈 / 飞瓜 / 千瓜 / 新榜 | 历史趋势、品类榜单、达人筛选 |
| T4 公开页面采集 | 达人主页作品列表 + 评论区 | 作品数据、评论原文（主粮） |
| T5 人工导出/截图 | 后台截图、达人自报数据 | 补充性数据块 |

合规红线：只采公开可见数据、控频、评论去标识化、禁止用推算值冒充实测值。详见 `references/data-sources.md`。

## 输出模板

使用 `templates/report-template.md`：任务定义与平台语境 → 作品层分析 → 评论层分析 → 合作判断（五问 + 合作形态 + 风险清单）→ 证据边界 → 跨达人对比卡。

## 品牌归属

- 擎漫网络 | Qomob.AI

---

## License

MIT License

Copyright (c) 2026 擎漫网络 | Qomob.AI

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

---

# 加入群聊

<div align="center">
  <img src="https://qomob.ai/xskill.jpg" width="600" alt="XSkill">
</div>
