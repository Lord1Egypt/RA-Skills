# 输出样例（真实引擎产物，非手写）

由 v6.4.0 引擎对**真实公开文稿**生成，供集成前了解各 JSON 的结构与字段。

**数据源溯源**：演示文稿取自维基百科「免疫系统」条目正文
（https://zh.wikipedia.org/wiki/免疫系统 ，CC BY-SA 4.0；仅作演示输入，条目内容以原站为准）。
样例中的分数与判定由真实引擎对该文稿计算得出，未做任何手工修改。

按场景看样例（对应命令直接跑你的文稿即可得到同结构输出）：

- 集成前了解检测响应结构 → `detect_sample.json` — ai_detector / pp_api.detect_text 的完整响应（概率、分层证据、risk_bands、指纹）
- 想知道「这段像不像 AI 写的」怎么呈现 → `style_norm_llm_jargon_sample.json` — 规范自查第 7 查（LLM 腔三层）的 findings 结构，每条带命中句
- 想看改写建议长什么样 → `fix_suggest_sample.json` — 句子级建议（stats + top 建议，只指位不代改）
- 想看一次完整自查的全貌 → `workflow_sample.json` — pp_workflow 端到端报告（全部检查小节；段落文本已截断）
- 想看可视化的最终效果 → `report_html_sample.html` — 上述样例渲染的单文件仪表盘（浏览器直接打开）

使用场景级的「什么时候用哪个命令」，见 `references/best-practices.md`。
- `style_norm_llm_jargon_sample.json` — 规范自查第 7 查（llm_jargon 三层）的 findings 结构
- `fix_suggest_sample.json` — 句子级改写建议的结构（stats + top 建议）
- `workflow_sample.json` — pp_workflow 端到端报告的完整 JSON（全部检查小节；段落文本已截断）
- `report_html_sample.html` — 上述样例经 pp_report_html.py 渲染的单文件仪表盘（可直接浏览器打开）

编程接口见 SKILL.md § Python API；任何字段变更都会在 CHANGELOG 声明。
