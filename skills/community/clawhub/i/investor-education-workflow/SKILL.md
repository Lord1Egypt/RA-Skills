---
name: investor-education-workflow
version: 1.1.0
description: "［何时使用］当用户需要投资者教育内容时；当用户说'写篇投教文章'、'解释这个投资概念'、'做个投教卡片'、'定投是什么'、'如何防骗'时触发。基于 LLM Wiki 机制的投教内容生产与分发工作流。"
author: 燃冰 & ant
created: 2026-04-24
skill_type: 通用🟡
allowed-tools: [Bash, Read, Write, Exec, WebSearch]
related_skills: [investment-advisory-workflow, investment-workflow, fund-analyzer-pro, holding-diagnoser, expression-layer, ljg-skills]
tags: [投资者教育，投教，知识普及，行为金融，LLM Wiki]
---

# investor-education-workflow: 投教工作流 🎯

## 📋 功能描述

帮助用户**系统化生产与分发投资者教育内容**。基于 LLM Wiki 机制，实现"知识库优先 → 搜索补充 → 转译大白话 → 多形式输出 → 反馈入库"的完整闭环。

**适用场景：**
- 投教内容生产（文章/卡片/语音/视频脚本）
- 知识点转译（专业术语 → 大白话）
- 客户问答响应（1 对 1/群发/讲座）
- 知识库维护（LLM Wiki编译与更新）

**边界条件：**
- 不替代持牌投教机构
- 知识准确性与合规由 IE 负责，内容生成与格式转换由 `expression-layer` 负责
- 知识库路径：`knowledge/investor-education/wiki/`
- 原始素材路径：`knowledge/investor-education/raw/`

---

## 🔄 核心处理流程（5 阶段）

### 阶段①：检索知识库
**动作**：在 `knowledge/investor-education/wiki/` 中全文检索关键词。
**输出**：命中 → 提取结构化知识点（定义/案例/话术）；未命中 → 进入阶段②。
**调用 Skill**：`Read`（读取 Wiki Markdown 文件）

### 阶段②：定向搜索补充 + 逻辑提取
**触发条件**：知识库未命中 / 内容过时 / 问题非常具体。
**动作**：
1. **搜索**：限定官方域名（`site:nerc.edu.cn` 等），获取原始材料。
2. **提取因果链**：搜索内容往往是新闻摘要或碎片信息。**必须先提取逻辑**，再转译。
   - 识别核心变量（如：降准 → 利率 ↓ → 债基 ↑）
   - 构建因果链（A 导致 B，B 影响 C）
   - 剔除矛盾/过时信息
**输出**：结构化因果链 + 来源标注。
**调用 Skill**：`searxng` + `url-to-markdown`

### 阶段③：合规拦截 + 转译大白话 + 意图标记
**动作**：
1. **合规拦截**：检测用户请求是否触碰红线。
   - 🔴 **红线**：推荐具体基金/股票代码、承诺收益、预测短期涨跌、代客理财。
   - 🟡 **转化协议**：若触碰红线，**不直接拒绝**，而是转化为投教内容。
     - 例：用户"推荐只下周必涨的基" → 转化为"如何自己筛选优质基金"或"为什么预测短期涨跌是陷阱"。
     - 标记 `intent: plain` 或 `card`，输出教育性内容。
2. **转译**：将阶段①/②的内容转译为大白话。
   - 去术语化：用生活类比（"PE=回本年限，像买店铺看租金"）
   - 场景化：嵌入普通人能遇到的情境
   - 行为化：直接告诉客户"你该做什么/不该做什么"
3. **意图标记**（必须输出结构化参数）：
   ```yaml
   intent: plain | writes | card | wechat | multi
   mold: -l | -i | -c | -w | -b  # 仅 intent=card 时必填
   audience: 儿童 | 新手 | 进阶 | 专业  # 可选，指导转译难度
   ```
**输出**：结构化内容 + 意图参数。
**调用 Skill**：`ljg-learn`（概念解剖）

### 阶段④：多形式输出（调用表达层）
**动作**：将阶段③的内容 + 意图参数传递给 `expression-layer`。
**调用方式**：
```yaml
调用 expression-layer，传入：
- content: [阶段③的结构化内容/因果链]
- intent: [plain/writes/card/wechat/multi]
- mold: [-l/-i/-c/-w/-b]  # 仅 card 时传
- audience: [儿童/新手/进阶/专业] # 可选
```
**输出**：表达层返回最终成品（Markdown/PNG/HTML/公众号）。
**调用 Skill**：`expression-layer`

### 阶段⑤：反馈入库
**动作**：将本次生成的内容、客户反馈、使用频次结构化回填至知识库。
**入库路径**：
- 新知识点 → `knowledge/investor-education/wiki/entities/` 或 `concepts/`
- 客户问答 → `knowledge/investor-education/raw/qa/`
- 反馈标记 → 在 Wiki 页面底部追加元数据：
  ```markdown
  ---
  使用频次：高/中/低
  理解难度：⭐/⭐⭐/⭐⭐⭐/⭐⭐⭐⭐/⭐⭐⭐⭐⭐
  最后更新：2026-04-24
  关联偏误：过度自信/损失厌恶/羊群效应
  ---
  ```
**调用 Skill**：`task-state-tracker`

---

## 📚 五大模块知识库

| 模块 | 内容 | 对应 Skill |
|------|------|-----------|
| 模块 1：投资基本功 | 金融基础/基本面分析/技术分析/财经素养 | `ljg-learn`, `fund-analyzer-pro` |
| 模块 2：市场认知与风险扫描 | 资本市场全景/风险识别/合规交易 | `decision-checklist`, `content-compliance` |
| 模块 3：行为管理 | 行为金融学/常见偏误/策略矫正 | `decision-checklist`, `ljg-relationship` |
| 模块 4：投资规划与生命周期 | 财务规划/资产配置/退休规划 | `fund-allocator`, `ljg-rank` |
| 模块 5：投资者陪伴与持续成长 | 分层学习路径/多元形式/日常陪伴 | `companion-script`, `ljg-plain`, `ljg-card` |

详细五大模块说明 → `references/five-modules.md`
LLM Wiki 架构 → `references/llm-wiki.md`
四专家思维框架 → `references/four-experts.md`

---

## ⚠️ 常见错误

**错误 1：知识库不存在**
```
问题：
• 阶段①检索失败，因为 knowledge/investor-education/ 目录未创建
• 流程断裂

解决：
✓ 首次使用时，先创建目录骨架（mkdir -p knowledge/investor-education/{raw,wiki/{entities,concepts,summaries}}）
✓ 导入种子数据（10 个高频知识点 Wiki 页面）
✓ 若目录不存在，直接跳至阶段②搜索
```

**错误 2：未调用表达层**
```
问题：
• 阶段④直接输出 Markdown，未调用 expression-layer
• 无法生成卡片/公众号/语音

解决：
✓ 阶段④必须调用 expression-layer，传入 content + intent + mold
✓ 不要自己生成 PNG/HTML，让表达层路由
```

**错误 3：意图标记缺失或参数不全**
```
问题：
• 未标记 intent 或 mold，表达层不知道要出 plain 还是 card，或默认用错模具
• 路由失败或输出格式不匹配

解决：
✓ 阶段③必须输出完整意图参数（intent + mold + audience）
✓ 歧义时主动询问用户："需要大白话解释、深度文章，还是可视化卡片？大字还是信息图？"
```

**错误 4：搜索源非官方**
```
问题：
• 阶段②搜索返回自媒体文章，非官方源
• 内容合规风险

解决：
✓ 搜索时必须限定 site:nerc.edu.cn OR site:sse.org.cn OR site:szse.cn
✓ 优先使用中国投资者网、交易所投教基地
```

**错误 5：合规请求硬拒绝**
```
问题：
• 用户问"推荐只下周必涨的基"，AI 直接回复"我不能推荐"
• 错失教育机会，用户体验差

解决：
✓ 执行"合规拦截与转化"协议
✓ 不拒绝，而是转化："预测短期涨跌是陷阱，我教你 3 个自己筛选基金的方法..."
✓ 标记 intent: plain 或 card，输出教育性内容
```

---

## 🧪 使用示例

**输入：**
```
客户问："什么是市盈率（PE）？能不能说人话？"
```

**预期输出：**
- 阶段①：检索知识库 → 命中"市盈率"Wiki 页面
- 阶段③：转译大白话 → 标记 intent: plain
- 阶段④：调用 expression-layer → 返回口语化解释（≤200 字）
- 阶段⑤：入库 → 标记"理解难度⭐⭐"，关联"锚定效应"

**输入：**
```
写篇投教文章：定投为什么能对抗择时焦虑？发到公众号。
```

**预期输出：**
- 阶段①/②：检索/搜索 → 获取定投原理 + 行为金融学素材
- 阶段③：转译 → 标记 intent: wechat
- 阶段④：调用 expression-layer → 返回公众号推文（HTML+ 封面）
- 阶段⑤：入库 → 标记"使用频次高"

---

## 🔧 故障排查

| 问题 | 检查项 |
|------|--------|
| 阶段①失败 | knowledge/investor-education/wiki/ 是否存在？是否有种子数据？ |
| 阶段④失败 | 是否调用了 expression-layer？intent 标记是否正确？ |
| 输出格式错误 | expression-layer 路由矩阵是否包含该意图？ |
| 搜索非官方 | 搜索命令是否包含 site:nerc.edu.cn 等限定？ |
| 未入库 | 阶段⑤是否执行？wiki 页面底部元数据是否追加？ |

---

## 🔗 相关资源

- 五大模块知识库：`references/five-modules.md`
- LLM Wiki 架构：`references/llm-wiki.md`
- 四专家思维框架：`references/four-experts.md`
- 表达层路由：`../expression-layer/SKILL.md`
- 报告模板：`templates/education-template.md`
- 标准参考：`docs/SKILL-STANDARD-v3.md`
