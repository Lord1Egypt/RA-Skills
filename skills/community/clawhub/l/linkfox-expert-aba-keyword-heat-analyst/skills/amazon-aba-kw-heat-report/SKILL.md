---
name: amazon-aba-kw-heat-report
description: "ABA关键词热度分析报告。词表/产品图/ASIN 入口→解析搜词→批量SFR→v1.1 HTML仪表盘。当用户要热度报告、给图验词、ASIN找词做热度可视化时触发。"
---

# amazon-aba-kw-heat-report · 关键词热度分析报告

> **配对取数**：`amazon-aba-kw-heat`（Shell A）  
> **入口解析**：本 skill `scripts/resolve_entry.py`（图 / ASIN / 词）  
> 专家：**关键词热度分析师** 的交付物层  

## 目标

1. 把用户输入变成精确 `keywords[]`（三种入口）  
2. 拉多周 ABA SFR 并计算同比/趋势指标  
3. 输出 v1.1 HTML：一词一图 + 焦点高亮 + 可选叠线 + 表  

## 三种入口

| 入口 | 参数 | 解析 |
|------|------|------|
| 词表 | `keywords[]` | 直接用 |
| **产品图** | `imageUrl` 或本地 `image` | 上传(如需) → 多模态推断 Amazon 搜词 JSON |
| **ASIN** | `asins[]` | `amazon-aba-asin-reverse` 反查流量词，按 SFR 取 TopN |

混合输入会 **合并去重**。解析结果写入 `entry_resolve.json`。

## 输入

| 参数 | 必填 | 说明 |
|------|------|------|
| keywords | 否* | 精确词 |
| asins | 否* | ASIN 列表 |
| image / imageUrl | 否* | 本地路径或公网 URL |
| region | 否 | 默认 US |
| weeks | 否 | 默认 104 |
| max_keywords / top_n | 否 | 入口解析后最多保留词数，默认 12 |
| input | 否 | 已有 ABA JSON，跳过取数（仍建议先 resolve） |
| out_dir | 否 | 输出目录 |

\* `keywords` / `asins` / `image(imageUrl)` / `input` 至少一个。

## 工作流程

```
用户: 词 | 图 | ASIN
        ↓
 resolve_entry.py
        ↓
 keywords[]  (+ sources 说明来自图/反查)
        ↓
 amazon-aba-kw-heat / shell_a
        ↓
 指标计算 + HTML v1.1
        ↓
 返回 html 路径；Discord MEDIA 投递
```

Agent 步骤：

1. 识别入口；缺公网图 URL 则先 upload  
2. `resolve_entry` → 展示词表（图/ASIN 必展示来源）  
3. `generate_report` 出 HTML  
4. 摘要：最热词、最大升温/掉热；提醒推断词已用 ABA 验证  

## 脚本

```bash
export LINKFOXAGENT_API_KEY=...

# 1) 仅解析入口
python3 scripts/resolve_entry.py '{"asins":["B01LP0V4JY"],"region":"US","top_n":12}'
python3 scripts/resolve_entry.py '{"imageUrl":"https://.../product.jpg","max_keywords":10}'
python3 scripts/resolve_entry.py '{"image":"/tmp/p.png","region":"US"}'

# 2) 一键报告（内置 resolve）
python3 scripts/generate_report.py '{
  "asins":["B01LP0V4JY"],
  "region":"US","weeks":104,
  "out_dir":"/tmp/heat-from-asin"
}'

python3 scripts/generate_report.py '{
  "imageUrl":"https://example.com/dress.jpg",
  "region":"US","weeks":104,
  "out_dir":"/tmp/heat-from-image"
}'

python3 scripts/generate_report.py '{
  "keywords":["babydoll dress","bodycon dress"],
  "region":"US","out_dir":"/tmp/heat-from-kws"
}'
```

## 输出

- `kw-heat-report.html` / `kw-heat-data.json` / `kw-heat-layout.json`  
- `aba_raw.json`  
- `entry_resolve.json`（图/ASIN 入口时）  
- stdout：`html` 路径、`summary`、`entry.mode`  

## 依赖 skill

| 能力 | skill / 脚本 |
|------|----------------|
| 图识别+上传 | `linkfox-multimodal-recognize-image` |
| ASIN 反查 | `amazon-aba-asin-reverse` |
| 热度取数 | `amazon-aba-kw-heat` |
| L3 ABA | `linkfox-aba-data-explorer` |

## 布局

`references/layout.json` — `aba-kw-heat-dashboard` v1.1  

## 限制

- 图推断必须经 ABA 验证；空反查/识别失败要明确报错而非编词  
- 词数建议 ≤ 20  
- HTML 依赖 ECharts CDN  
- 无销量/BSR/绝对搜索量  

## 边界

不做选品长文决策；只做 **搜词解析 + 热度验证 + 可视化**。
