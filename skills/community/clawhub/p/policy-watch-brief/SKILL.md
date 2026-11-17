---
name: policy-watch-brief
description: '通过公开Web搜索获取近期产业政策与监管动态，整理为结构化简报（包含主题、关键信息、影响分析、来源）。Use when: (1) 需要了解某一产业近期政策动向，(2) 需要跟踪监管政策变化，(3) 需要整理政策简报，(4) 需要搜索产业政策的历史或未来趋势。NOT for: 需要实时数据的业务分析、需要专业政策咨询意见、需要引用具体法律法规条文原文。'
metadata:
  {
    "openclaw":
      {
        "emoji": "📋",
        "requires": { "anyBins": ["curl", "openclaw"] },
      },
  }
---

# Policy Watch Brief

通过公开Web搜索获取近期产业政策与监管动态，整理为结构化简报。

## When to Use

✅ **USE this skill when:**

- "查找近期 AI 产业政策动向"
- "整理新能源监管政策简报"
- "获取金融监管最新动态"
- "了解某产业政策趋势"

❌ **DON'T use this skill when:**

- 需要实时数据的业务分析 → 使用专业数据分析工具
- 需要专业政策咨询意见 → 咨询专业机构
- 需要引用具体法律法规条文原文 → 使用法律数据库

## Commands

### 综合政策搜索

```bash
# 搜索近期政策动态
bash:web_search query:"2024-2025 产业政策 监管动态" count:10

# 获取搜索结果中的具体内容
bash:web_fetch url:"<search-result-url>" extractMode:"markdown"
```

### 按产业搜索

```bash
# AI产业政策
bash:web_search query:"AI 人工智能 政策 监管 2025" count:10

# 新能源产业政策
bash:web_search query:"新能源 光伏 风电 政策 2025" count:10

# 金融监管政策
bash:web_search query:"金融监管 政策 2025" count:10

# 半导体产业政策
bash:web_search query:"半导体 政策 2025" count:10
```

### 按时间范围搜索

```bash
# 最近一个月
bash:web_search query:"产业政策 监管 最近1个月" freshness:"month"

# 最近一年
bash:web_search query:"产业政策 监管 2024-07至2025-07" freshness:"year"
```

## 结构化简报格式

### MMP格式（Markdown Manager Plan）

```markdown
---keyword: <产业/政策领域>
---date: <检索日期>
---status: <active/archived>
---confidence: <high/medium/low>
---

# <主题>

## 关键信息
<政策发布主体>：<发布机构名称>
<发布日期>：YYYY-MM-DD
<政策文号>：<如有>
<主要内容>：
- <要点1>
- <要点2>
- <要点3>

## 影响分析

### 直接影响
<对产业的直接影响>

### 间接影响
<对产业的间接影响>

### 长期趋势
<长期趋势预测>

## 来源
- [来源链接1](<url1>)
- [来源链接2](<url2>)
- [来源链接3](<url3>)
```

## 快速开始

### 模板调用

复制以下命令搜索政策：

```bash
# 综合搜索
bash:web_search query:"2024-2025 <产业/领域> 政策 监管 动态" count:10

# 读取内容
bash:web_fetch url:"<url>" extractMode:"markdown"

# 整理简报
生成MMP格式的结构化简报。
```

### 执行流程

1. **选择产业**：确定需要查询的产业领域
2. **执行搜索**：使用 web_search 搜索政策动态
3. **提取内容**：使用 web_fetch 读取搜索结果中的详细内容
4. **整理简报**：
   - theme：确定主题和政策层次
   - 提取可信来源（政府网站、权威媒体）
   - 添加政策发布日期和来源链接
   - 总结政策要点
   - 分析直接与间接影响

## Notes

- 可信度优先：优先选择政府发布的政策文件和权威媒体
- 时效性：只搜索近期（半年内）的政策动态
- 来源注明：每条政策信息都要注明来源链接
- 结构化输出：使用 MMP 格式确保简报结构一致
