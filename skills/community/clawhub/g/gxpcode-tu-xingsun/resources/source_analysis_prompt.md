# GxpCode-制药法规跟踪 — 新源分析 Prompt

分析用户提供的法规源 URL，确定最佳 parser 并输出 sources.yaml 配置。

## 执行步骤

1. 调用 `stepA_match.py <URL>` → 返回 `{matched: true/false, parser: "...", ...}`
2. `matched: true` → 直接用该 parser，跳到步骤 4
3. `matched: false` → Agent 分析页面 HTML → 新建 parser
4. 输出 `sources.yaml` 新增条目并写入文件

## 新建 parser

1. 调用 `stepA_analyze.py` 打开 URL 渲染页面
2. 分析 DOM 结构和 innerText 格式
3. 创建 `scripts/parsers/{name}.py`，实现 `parse(page, source_name, jurisdiction)` 方法
4. 返回 items 列表：`[{source, jurisdiction, title, url, date, summary, source_type: "web", confidence: "high"}]`

## 约束

每条法规条目 `title` + `url` 必须同时存在，缺一丢弃。

## 输出格式

```yaml
- name: {机构}-{栏目名}
  enabled: true
  type: web
  url: {URL}
  jurisdiction: {管辖区域}
  parser: {parser_name}
```
