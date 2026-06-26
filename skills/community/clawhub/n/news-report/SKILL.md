---
name: news-report
description: "多引擎资讯采集 + 深色仪表盘 HTML 报告生成。输入关键词，自动采集资讯、LLM 分析提炼、生成专业报告并发送。触发词：生成资讯报告、采集资讯分析、行业资讯报告、news report、资讯采集。"
---

# 资讯采集报告生成器 (news-report)

输入一个关键词或主题，自动完成：多引擎资讯采集 → LLM 分析提炼 → 生成深色仪表盘风格 HTML 报告 → 发送给用户。

---

## 触发示例

> 「帮我生成一份关于 OpenClaw 的资讯报告」
> 「采集 Dify 最新动态，生成分析报告」
> 「生成一份讯飞星火大模型的行业资讯报告」

---

## 完整流程

### Step 1：采集原始资讯

```bash
python3 scripts/fetch_news.py \
  --keyword "关键词" \
  --engines "bing,bing_cn,ddg,brave" \
  --count 20 \
  --output /tmp/raw_news.json
```

**支持引擎：** `bing`（国际）、`bing_cn`（中文）、`ddg`（DuckDuckGo）、`brave`、`sogou`、`baidu`

---

### Step 2：LLM 分析提炼（核心步骤）

读取 `/tmp/raw_news.json` 采集结果，结合 LLM **自身知识库**，生成完整报告数据 JSON，保存到 `/tmp/report_data.json`。

**报告数据结构（必须严格遵守）：**

```json
{
  "title":    "报告主标题（含关键词）",
  "subtitle": "副标题，如：AI框架生态全景解读",
  "date":     "YYYY-MM-DD",
  "keyword":  "搜索关键词",
  "kpis": [
    {"num":"190K+", "label":"GitHub Stars", "sub":"90天增长", "color":"blue"},
    {"num":"25+",   "label":"支持平台",     "sub":"消息平台数", "color":"orange"},
    {"num":"88%",   "label":"企业采用率",   "sub":"年增长数据", "color":"green"},
    {"num":"400+",  "label":"安全漏洞",     "sub":"已知CVE",    "color":"red"}
  ],
  "summary": "执行摘要，2-3句话概括核心发现，可包含 <strong> 标签高亮关键词",
  "timeline": [
    {"date":"2025年11月", "title":"事件标题", "desc":"事件描述", "color":"blue"},
    {"date":"2026年2月",  "title":"收购完成", "desc":"详细描述", "color":"green"}
  ],
  "news": [
    {
      "num": 1,
      "date": "2026-02-16",
      "source": "InfoWorld",
      "title": "资讯标题",
      "body": "资讯摘要（2-3句）",
      "tag": "战略收购",
      "tag_color": "blue"
    }
  ],
  "analysis": {
    "tech":  {"title":"技术亮点", "icon":"⚡", "color":"blue",  "items":["要点1","要点2"]},
    "risk":  {"title":"风险挑战", "icon":"⚠️","color":"red",   "items":["风险1","风险2"]},
    "trend": {"title":"未来趋势", "icon":"🚀", "color":"green", "items":["趋势1","趋势2"]}
  },
  "comparison": {
    "headers": ["产品","定位","评分","状态"],
    "rows": [
      ["产品A","定位描述","★★★★★","活跃"],
      ["产品B","定位描述","★★★☆☆","稳定"]
    ]
  },
  "conclusion": {
    "pros":  ["优势1","优势2","优势3"],
    "risks": ["风险1","风险2","风险3"],
    "refs":  [
      {"title":"参考价值1", "body":"说明文字"},
      {"title":"参考价值2", "body":"说明文字"}
    ]
  },
  "source_note": "数据来源：xxx · 报告日期：xxx · 由 astronClaw AI 生成"
}
```

**tag_color 可选值：** `blue` / `orange` / `green` / `red` / `purple` / `gold`

**⚠️ 重要说明：**
- `kpis` 数组固定4个，颜色建议：第1个blue、第2个orange、第3个green、第4个red
- `news` 数组固定10条，每条必须有真实的 `source` 来源
- `timeline` 5-7个事件，按时间顺序排列
- `analysis` 固定包含 tech / risk / trend 三个模块，每个 5-6 条
- 如无竞品数据，`comparison` 可省略

生成的 JSON 保存为 `/tmp/report_data.json`。

---

### Step 3：生成 HTML 报告

```bash
python3 scripts/gen_report.py \
  --data /tmp/report_data.json \
  --output /Users/eric/.openclaw/workspace/report_KEYWORD_MMDD.html
```

输出文件命名规范：`report_{关键词拼音/英文}_{MMDD}.html`

---

### Step 4：发送给用户

使用 `message` 工具将 HTML 文件发送到飞书。

---

## 快速示例（完整命令）

```bash
# Step 1：采集
python3 scripts/fetch_news.py \
  --keyword "讯飞星火大模型" \
  --engines "bing,bing_cn,ddg,baidu" \
  --count 20 \
  --output /tmp/raw_news.json

# Step 2：LLM 分析（见上方数据结构）→ 生成 /tmp/report_data.json

# Step 3：生成 HTML
python3 scripts/gen_report.py \
  --data /tmp/report_data.json \
  --output /Users/eric/.openclaw/workspace/report_xfyun_0309.html
```

---

## 注意事项

- 采集可能因网络限制返回空结果（尤其 Google），此时以 LLM 自身知识补充
- HTML 报告完全自包含，无外部依赖，可直接用浏览器打开
- 报告生成约 30-60 秒（含采集+生成）
- 输出文件大小约 20-40KB

---

## 依赖

- Python 3（标准库，无需额外安装）
- 网络访问（采集时需要）
