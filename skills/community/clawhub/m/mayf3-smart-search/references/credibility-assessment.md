# 搜索结果可信度评估

基于 CRAAP 测试 + SIFT 方法，在调研中自动评估搜索结果。

## 信息来源分层

```
Tier 1: 原始数据/一手资料
  - 同行评议论文（arXiv 预印本需谨慎）
  - 政府/机构官方数据（统计局、NASA、WHO）
  - 专利、法律文件

Tier 2: 权威整合来源
  - 知名期刊（Nature、Science、IEEE）
  - 权威媒体（路透、AP、新华社）
  - 成熟的开源项目文档

Tier 3: 二手/三手分析
  - 行业分析报告（注意商业目的）
  - 博客文章/教程（区分个人观点）
  - 新闻报道（区分事实报道和评论）

Tier 4: 开放式/用户生成内容
  - Reddit/HN/知乎/微博
  - Stack Overflow（技术问答）
  - 个人博客

Tier 5: 值得怀疑的来源
  - 无作者/无来源的文章
  - 明确商业推广内容
  - AI 生成的结论性内容（需追溯原始来源）
```

## 调研中快速评估方法

### 1. 横向阅读（比纵向阅读更有效）

- 看到新结果，不读内容先查来源
- 搜索 `"source name" + "reputation"` 或 `"source name" + "wiki"`
- 搜索 `"claimed fact" + "fact check"`
- 确认来源可靠性后再采信

### 2. SIFT 四步法

- **S**top — 停下来，不立即相信
- **I**nvestigate the source — 调查来源背景
- **F**ind better coverage — 找 2-3 个独立来源交叉验证
- **T**race to original context — 追溯原始上下文

### 3. 域名快速判断

- `.gov` / `.edu` > `.org` > `.com`
- `.edu` 个人页面（`~username` 路径）≠ 官方内容
- 注意域名模仿（`go0gle.com` vs `google.com`）

### 调研输出中的可信度标注

在调研结果中对关键来源标注层级：

```
- 来源 A [T1] — 权威
- 来源 B [T2] — 可靠
- 来源 C [T4] — 参考，需验证
```
