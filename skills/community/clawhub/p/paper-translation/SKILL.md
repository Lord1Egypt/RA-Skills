---
name: paper-translation
description: >
  ArXiv 论文精读级中文翻译，同步到 IMA 知识库 + 腾讯文档。
  基于 5 篇论文（MDL/Kunlun/OneTrans/RankMixer/MixFormer）3 轮迭代实战经验。
  触发场景：翻译论文、翻译 arxiv、论文精读、论文中文翻译、paper translation、
  translate paper、翻译这篇论文、帮我翻译、精读翻译、论文全文翻译、
  把这篇论文翻译成中文、翻译 arxiv 论文到知识库。
---

# ArXiv 论文精读翻译

Base directory for this skill: `{SKILL_DIR}`

将 ArXiv 论文逐段翻译成中文，生成双版本 Markdown（IMA + 腾讯文档），并上传到两个平台。

## 三条铁律

1. **完整翻译不精简** — 逐段翻译每个 paragraph，不遗漏任何论证细节。大模型倾向于"帮你归纳"，但用户要的是精读级翻译。
2. **译注显式标记** — 大模型解读必须用 `> **[译注]**：...` 引用块，绝不混入原文翻译。
3. **简称首次标全称，后续直接用** — 首次出现标注全称并核对原文，后续不再展开。避免错误展开（如 TA=Target Attention 被误写为 Transformer Aggregator）。

## 标准 6 步流程

### Step 1: 获取原文

```
web_fetch https://arxiv.org/html/<id>v<n>
```

- 只 fetch **一次**，节省 token
- 同步下载图片：`curl -sL -o x{n}.png https://arxiv.org/html/<paper_id>/x{n}.png`
- 下载后检查文件大小，相同大小的异常文件（404 垃圾响应）删除

### Step 2: 翻译生成

- **逐段翻译**，不做精简
- 首行元信息：原标题、arxiv 链接、年月、机构、翻译辅助大模型名称
- 简称首次出现标全称（核对原文），后续用简称
- 译注用 `> **[译注]**：...` 格式
- 结构化排版：多级标题 + 列表 + 加粗 + 表格 + 引用块
- 公式保留 LaTeX；**`\bm` 全部替换为 `\boldsymbol`**
- 图表按原文顺序插入**所在章节标题之后、小节正文之前**
- 参考文献完整列出

**表格处理策略**：
- 简单表格 → Markdown 表格重写（可搜索/编辑）
- 复杂表格（合并单元格/特殊排版）→ PyMuPDF 从 PDF 截取

### Step 3: 自动化校验

翻译完成后，运行校验脚本：

```bash
python3 {SKILL_DIR}/scripts/validate_translation.py <markdown_file>
```

校验项：

| 检查项 | 标准 |
|--------|------|
| 章节完整性 | 包含：摘要/引言/相关工作/方法/实验/结论/参考文献 |
| LaTeX 兼容性 | `\bm` 出现次数 = 0 |
| 译注标记 | 数量 > 0，格式为 `> **[译注]**` |
| 参考文献 | 条数列出供人工核对 |
| 图片链接 | 外链格式正确 |

### Step 4: 生成两版 Markdown

- **IMA 版**：图片用 arxiv 外链 URL / base64 data URI
- **腾讯文档版**：用脚本从 IMA 版自动替换图片链接为 image_id

图片上传流程：
1. `curl -sL -o x{n}.png https://arxiv.org/html/<paper_id>/x{n}.png` 下载
2. 腾讯文档：`mcporter call tencent-docs upload_image` → 拿 image_id
3. IMA：直接用 arxiv 外链 URL

详见 [references/platform-compat.md](references/platform-compat.md)

### Step 5: 上传 IMA 知识库

```bash
# create_media → COS 上传 → add_knowledge（media_type=7 = Markdown）
# 如遇 code=220030（限流），sleep 15s 重试，cos_key 仍有效
```

### Step 6: 上传腾讯文档

```bash
TITLE="【YYYY.MM｜组织】XXX 中文翻译"  # 必须 ≤36 字符
jq -n --arg title "$TITLE" --rawfile mdx "$FILE" --arg cf "markdown" \
  '{title:$title, mdx:$mdx, content_format:$cf}' > /tmp/args.json
mcporter call tencent-docs create_smartcanvas_by_mdx --args "$(cat /tmp/args.json)"
```

mcporter 传大参数**不支持 `--args-file`**，必须用 `--args "$(cat file.json)"`。

## 命名规范（强制）

| 平台 | 格式 | 约束 |
|------|------|------|
| 腾讯文档标题 | `【YYYY.MM｜组织】XXX 中文翻译` | ≤36 字符（按字符数，非字节） |
| IMA 文件名 | `【YYYY.MM｜组织】XXX 中文翻译.md` | 同名加 .md |

- 两平台**必须完全一致**，不加 `v2`/`图文版` 等后缀
- 示例：`【2026.02｜ByteDance】MixFormer 中文翻译`

## 翻译后 Checklist

完成翻译后逐项确认：

- [ ] `grep -c '\\bm'` = 0
- [ ] 简称首次出现已标全称且正确
- [ ] 译注均用 `> **[译注]**：...` 格式
- [ ] 图表位置与原文章节顺序一致
- [ ] 参考文献条数与原文一致
- [ ] IMA 版和腾讯文档版图片格式各自正确
- [ ] 两平台文件名/标题完全一致
- [ ] 首行包含论文元信息（标题/链接/年月/机构/大模型名称）

## 效率优化

- 只 `web_fetch` 一次原文（节省 token）
- 直接生成最终版，不生成中间草稿（减少 50%+ 工具调用）
- 图片下载 + 上传并行执行
- 用脚本自动从 IMA 版生成腾讯文档版
- 自动化校验脚本在上传前拦截格式问题

## 参考文档

- **踩坑经验 + 平台兼容性**：[references/platform-compat.md](references/platform-compat.md) — LaTeX 兼容、图片跨平台、API 限流等详细说明
- **迭代历史**：[references/iteration-history.md](references/iteration-history.md) — MixFormer v1→v3 的完整教训记录
