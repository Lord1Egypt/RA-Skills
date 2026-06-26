---
name: multi-search-fallback
description: 多源搜索聚合技能。当用户需要搜索信息、查资料、做研究时，自动调用多个搜索源进行交叉验证，提高结果准确性。触发场景：搜索某事、查证某个说法、做研究、多源验证、compare multiple sources、搜索结果不一致时主动复核。**只要是搜索类需求，一律优先使用此技能**，它会自动决定是单源快速返回还是多源深度验证。
trigger: 搜索|查|研究|验证|多源|compare|sources|查证|核实|fact-check
author: general-expert
contact:
  email: ruogu@outlook.com
metadata:
  openclaw:
---

# multi-search-fallback 多源搜索聚合技能

## 核心能力

当接到搜索任务时，智能调度多个搜索技能，通过 fallback 机制确保搜索的高可用性，并通过多源交叉验证提高结果准确率。

## 工作流程

### 第一步：判断搜索类型

```
if 简单事实查询（天气、人名、简单百科）:
    → 单源快速搜索（web_search），直接返回
elif 复杂研究任务（行业分析、技术对比、政策解读）:
    → 多源深度搜索（触发 fallback 链）
elif 学术/论文相关:
    → academic-deep-research + 多源验证
elif 金融/投资相关:
    → mx_search + 交叉验证
else:
    → 默认多源搜索
```

### 第二步：执行搜索链（Fallback 机制）

**搜索链顺序**（按优先级递减）：

| 优先级 | 搜索技能 | 适用场景 | 超时 |
|--------|----------|----------|------|
| 1 | `web_search` (Brave/Google) | 通用搜索，快速结果 | 15s |
| 2 | `ddg-web-search` | Brave 不可用时的 fallback | 20s |
| 3 | `openclaw-skill-search-web` | 国内搜索，火山引擎 | 20s |
| 4 | `tavily-search` | AI 优化结果（需 API key） | 25s |
| 5 | `multi-search-engine` | 多引擎联合，结果最全 | 30s |
| 6 | `deep-research-pro` | 深度研究，综合报告 | 60s |

**Fallback 规则**：
- 搜索失败（网络错误、API 错误）→ 自动切换到下一个
- 结果为空 → 切换到下一个
- 用户未指定搜索工具时，默认按优先级尝试
- 显式指定某工具时，直接使用（如"用 Tavily 搜索 xxx"）

### 第三步：多源交叉验证

当调用了 2 个及以上搜索源时，执行交叉验证：

```
for each unique finding across sources:
    if 发现一致（相同结论）:
        confidence += 1
        tag: "✅ 一致"
    elif 发现分歧:
        tag: "⚠️ 分歧"
        记录分歧内容
    elif 发现补充:
        tag: "📎 补充"
        
confidence_score = 一致数 / 总发现数
```

**置信度等级**：
- 90%+：✅ 高度可信（多源一致）
- 60-89%：⚠️ 中等可信（部分分歧）
- < 60%：❌ 低可信（分歧较大，需进一步查证）

### 第四步：结果融合输出

## 搜索结果：[query]

**置信度**：XX%（X/X 源一致）

### 核心发现
- [按置信度排序的要点列表]

### 多源对比
| 搜索源 | 结果摘要 | 状态 |
|--------|----------|------|
| web_search | xxx | ✅ 一致 |
| ddg-web-search | xxx | ⚠️ 分歧（xxx） |
| tavily | xxx | ✅ 一致 |

### 原始结果（按源分组，可折叠）
<details>
<summary>展开完整搜索结果</summary>

**web_search:**
- ...

**ddg-web-search:**
- ...

</details>

## 搜索源调用策略

### 简单搜索（默认）
自动选择前 2 个可用源，15 秒内返回。

### 深度搜索（用户要求"深度"、"研究"、"全面"）
自动选择 3+ 个源，包含 `multi-search-engine` 或 `deep-research-pro`。

### 争议查证（用户要求"核实"、"fact-check"、"验证"）
调用 4+ 个源，强制进行交叉验证并明确标注分歧。

### 国内内容（涉及国内政策、公司、新闻）
优先使用 `openclaw-skill-search-web` + `multi-search-engine`（含百度/搜狗）。

### 学术研究（涉及论文、学术概念、研究方法）
优先使用 `academic-deep-research`，辅以 `tavily-search` 验证。

## 错误处理

| 错误类型 | 处理方式 |
|----------|----------|
| 第一个源成功 | 直接返回，不继续调用 |
| 所有源失败 | 返回"所有搜索渠道均不可用，建议稍后重试" |
| 部分源失败 | 返回可用结果，标注失败的源 |
| 超时 | 取消当前搜索，使用已返回的结果 |

## 调用示例

**用户输入**："搜索一下 OpenClaw 最新版本的功能更新"

**技能执行**：
1. 判断：简单新闻查询 → 单源快速搜索
2. 调用：`web_search`（Brave）
3. 返回结果 + 置信度（单源设为 N/A）

**用户输入**："研究一下 AI Agent 在教育行业的应用现状，需要多源验证"

**技能执行**：
1. 判断：深度研究 → 多源搜索
2. 调用链：`web_search` → `multi-search-engine` → `deep-research-pro`
3. 交叉验证：比对三个源的发现，标注一致/分歧
4. 输出：结构化报告 + 置信度评分

## 工具调用接口

本技能通过以下工具执行搜索：

```python
# 工具映射
SEARCH_TOOLS = {
    "web_search": "mcporter call minimax.web_search",
    "ddg-web-search": "ddg-web-search skill",
    "openclaw-skill-search-web": "openclaw-skill-search-web skill",
    "tavily-search": "tavily-search skill",
    "multi-search-engine": "multi-search-engine skill",
    "deep-research-pro": "deep-research-pro skill",
    "academic-deep-research": "academic-deep-research skill",
    "mx_search": "mx_search skill",
}
```

调用搜索技能时，通过 `sessions_spawn` 启动子任务并获取结果。

## 质量标准

1. **不瞎猜**：搜索不到的信息明确说"未找到"，不编造
2. **标注来源**：每个结论必须标注来源，不说"据悉"
3. **诚实呈现分歧**：多个源结果不一致时，不强制统一，如实呈现
4. **优先广度**：宁可多几个源，也不要漏掉重要信息源
