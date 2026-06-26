# Prompt Templates

Ready-to-use prompts for each input type. The user can copy these directly or the agent can adapt them.

**Note on agent output conventions:** All analyses should use source attribution tags (`[原文直接报告]`, `[原文Methods]`, `[原文Discussion]`, `[图片识别]`, `[教学性说明]`). Module C must start with the label legend. Do not infer sample size from df. Use the paper's exact terminology for response labels and conditions.

## Type 1: Full Results Section

```
请帮我拆解这篇论文的 Results 部分：

[粘贴 Results 全文]

要求：
1. 文献信息简表（研究主题、问题、假设、样本、IV/DV）
2. Results 结构地图（按小节拆解）
3. 逐句功能标注（使用 14 类标签）
4. 每张图表导读（含 1 分钟 PPT 讲解稿）
5. 写法提取（可迁移的英文句型和中文对应表达）
6. 批判性检查（统计报告完整性、过度解释、因果表达等）
7. 最终总结（写作逻辑、最值得模仿的 3 点、最需警惕的 3 点）

请用中文输出，专业但不堆砌术语。
```

## Type 2: Single Results Subsection

```
请拆解这篇论文 Results 中的这一小节：

[粘贴小节内容]

本小节对应的图表：[图X / 表Y，如无则标注"无"]

要求：
- 文献信息简表（根据小节和上下文推断，标注"推测"）
- 逐句功能标注
- 图表导读
- 写法提取
- 批判性检查

请用中文输出。
```

## Type 3: Figure Caption + Result Paragraph

```
这张图的结果段落怎么写/怎么讲？

Figure caption:
[粘贴 caption]

对应的结果段落：
[粘贴段落]

要求：
- 图表导读（回答什么问题、横纵坐标含义、关键模式）
- 逐句分析作者如何引导读者看图
- 1 分钟 PPT 讲解稿（中文）
- 提取可模仿的句型

请用中文输出。
```

## Type 4: Abstract + Methods + Results

```
请综合拆解这篇论文的结果部分：

Abstract:
[粘贴]

Methods (关键部分):
[粘贴]

Results:
[粘贴]

要求：
完整 A–G 模块分析，特别注意：
- 摘要中承诺的结果是否都在 Results 中兑现
- Methods 中的设计是否在 Results 中被完整报告
- 是否有 Results 中出现但 Methods 中未提及的分析
```

## Type 5: PDF Excerpt (Partial / Messy)

```
我从一篇 PDF 中复制了以下内容，请帮我拆解：

[粘贴内容]

（可能包含 Abstract / Methods / Results 的片段，格式可能混乱）

要求：
- 先判断内容属于论文的哪个部分
- 根据内容类型选择适当的模块分析
- 如果内容不全，明确说明哪些分析受限于信息不足
```

## Type 6: PDF File Upload

```
请帮我拆解这篇论文的 Results 部分。

[直接上传 PDF 文件]

要求：
- 从 PDF 提取全文，自动识别并提取 Results 部分
- 如果 Results 和 Discussion 合并，请标注
- 然后完整 A–G 模块分析

请用中文输出。
```

**Agent note:** When receiving a PDF file, the agent should:
1. Extract text with `pdftotext -layout <pdf_path> /tmp/paper_extracted.txt`
2. If `pdftotext` returns empty/garbled (scanned PDF), tell user to provide a text-selectable PDF or paste Results text manually
3. Scan extracted text for `Results` / `Results and Discussion` / `结果` heading
4. Extract from that heading to the next major heading (`Discussion`, `4.`, `References`, etc.)
5. Print the detected Results section summary so the user can confirm
6. Proceed to Modules A–G

**PDF input types handled:**
- `.pdf` file attachment in webchat/desktop
- Any local path to a PDF on the user's machine
- If the PDF is on the user's machine (not uploaded), use `read` to find the path then `exec` with `pdftotext`

## Type 7: Figure Screenshot + Caption + Body Text

```
请帮我分析这张图，并结合论文正文一起拆解：

[上传图表截图]

Figure caption:
[粘贴 caption]

正文中讨论该图的结果段落：
[粘贴段落]

要求：
- 从图片识别横纵坐标、分组、误差线、关键模式
- 对比「图片读到什么」vs「caption 说了什么」vs「正文强调了什么」
- 1 分钟 PPT 讲解稿（中文）
- 批判性检查：图片展示的结果与正文描述是否一致？是否有选择性强调？

请用中文输出。
```

**Agent note:** Use the `image` tool (vision model) to analyze the figure screenshot. Prompt it to extract: axes labels and units, condition/group labels, legend entries, error bar type, salient patterns. Cross-reference vision output with caption and body text in Module D.

## Type 8: Open-Ended Request

```
User: "帮我拆这篇文献结果部分"
Agent: "请提供 Results 部分的文本，我可以做完整的 7 模块拆解。如果你只有部分内容（如某一小节、某个图表段落），也可以直接贴过来。"

User: "这张图怎么讲"
Agent: "请提供：① Figure caption；② 论文正文中讨论这张图的段落；③ 如果有图表截图也可以一并发送。目前我先根据 caption 和正文来分析。"

User: "这个结果段落在写什么"
Agent: "请粘贴这一段。我会逐句标注每句话的功能（14 类标签），然后总结段落的逻辑结构。"
```

## Quick Extraction Variant

When the user only wants writing strategies (Module E):

```
请提取这篇 Results 的写作策略：

[粘贴 Results 或段落]

重点提取：
- 结果开头方式
- 图表引导句型
- 关键发现句
- 不显著结果表达
- 可模仿的英文句型（3–5 句）
- 对应的中文表达
```

## Compare Two Papers Variant

```
请比较这两篇论文的 Results 写作策略：

Paper A (Results):
[粘贴]

Paper B (Results):
[粘贴]

比较维度：
- 结果组织逻辑的差异
- 图表引导方式
- 评价性语言使用频率和强度
- 统计报告完整性
- 限制承认程度
- 哪篇更值得模仿（请说明理由）
```
