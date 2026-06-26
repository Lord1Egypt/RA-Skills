# 格式检查执行矩阵（v2）

> 来源默认：`institution-format-guide` + `historical-defect-checklist`；另叠加公开版保留的补充规则 `format-public-addendum.md`（仅覆盖明确保留项）
>
> 说明：
> - **显式规则** = 原规范直接给了字体/字号/位置/格式
> - **一致性规则** = 原规范或往届问题只要求“统一/规范”，未给精确数值，因此按同类对象 dominant pattern 检查是否失配
> - **结构规则** = 检查是否存在、是否放对位置、是否编号规范、是否缺项

| 分区 / 对象 | 必查项 | 规则类型 | 来源 | 落地实现 |
|---|---|---|---|---|
| 封面 / 扉页 / 声明 | 分区识别、必备字段存在性（分类号/密级、UDC、学位论文、校名、日期、中英扉页要素、声明/授权书）、前置顺序检查；前置表格不参与正文/表内一致性统计 | 结构 | institution-format-guide 结构章节 + 用户补充口径 | `format_checker.py` front matter object model + zone classifier + table-cell zone filter |
| 中文摘要标题 | 一级标题（黑体二号、居中） | 显式 | institution-format-guide 4.1 | `format_checker.py` heading rule |
| 中文摘要正文 | 小四宋体 / 英文数字同号 / 对齐与缩进一致性 | 显式 + 一致性 | institution-format-guide 4.2 | `format_checker.py` body rule + consistency |
| 中文关键词 | 关键词标签、正文同号、词项内容 | 显式 + 结构 | institution-format-guide 摘要示例 | `format_checker.py` keyword rule |
| 英文 Abstract 标题 | 一级标题 | 显式 | institution-format-guide 4.1 | `format_checker.py` heading rule |
| 英文摘要正文 | 与中文摘要同类检查 | 显式 + 一致性 | institution-format-guide 4.2 | `format_checker.py` body rule + consistency |
| 目录标题 | **黑体小三**（用户补充口径覆盖旧的“一级标题黑体二号”默认值） | 显式 | `format-public-addendum.md` | `format_checker.py` toc title override |
| 目录条目 | 字号符合标准、行距统一、点线/页码结构 | 一致性 + 结构 | historical-defect-checklist 目录条款 | `format_checker.py` toc checks |
| 一级标题 | 黑体二号、居中 | 显式 | institution-format-guide 4.1 | `format_checker.py` heading1 |
| 二级标题 | 黑体三号、左对齐 | 显式 | institution-format-guide 4.1 | `format_checker.py` heading2 |
| 三级标题 | 黑体四号、左对齐 | 显式 | institution-format-guide 4.1 | `format_checker.py` heading3 |
| 四级标题 | 黑体小四、左对齐 | 显式 | institution-format-guide 4.1 | `format_checker.py` heading4 |
| 正文段落 | 小四宋体；英文数字同号；对齐、行距、段前后、缩进统一 | 显式 + 一致性 | institution-format-guide 3 / 4.2 + historical-defect-checklist | `format_checker.py` body consistency |
| 正文段落 | 中文与英文单词之间若出现空格则标注；不泛化到封面/目录 | 显式 | `format-public-addendum.md` | `format_checker.py` extra_space check |
| 图题 | 位于图下方；图号按章序号；五号宋体 | 显式 + 结构 | institution-format-guide 4.2.1 | `format_checker.py` figure caption + adjacency |
| 表题 | 位于表上方居中；表号按章序号；五号宋体 | 显式 + 结构 | institution-format-guide 4.2.2 | `format_checker.py` table caption + adjacency |
| 表内文字 | 不大于图题字号；表头与内容连在一起 | 显式 + 结构 | institution-format-guide 4.2.2 + historical-defect-checklist | `format_checker.py` table cell checks |
| 公式 | 单行居中；式号同行居右；按章编号 | 显式 + 结构 | institution-format-guide 4.2.3 | `format_checker.py` formula checks |
| 公式释义 | 释义表达方式统一 | 一致性 | historical-defect-checklist 公式条款 | `format_checker.py` formula explanation consistency |
| 页边距 | 版芯对应页边距是否匹配 A4 + 160×247 | 显式 | institution-format-guide 3 + historical-defect-checklist | `format_checker.py` section margin checks |
| 页眉 | 自摘要页起存在；5号楷体；左固定右章题；单线/双线样式存在 | 显式 + 结构 | institution-format-guide 3 | `format_checker.py` header checks + header XML border checks |
| 页码 | 页底居中；阿拉伯数字连续；两侧修饰；正文字体 Roman；摘要/空白页应有页码 | 显式 + 结构 | institution-format-guide 3 + historical-defect-checklist | `format_checker.py` footer/page number checks |
| 参考文献标题 | 一级标题 | 显式 | institution-format-guide 4.1 | `format_checker.py` heading1 |
| 参考文献条目 | 顺序编号、卷(期)、页码、信息完整性 | 显式 + 结构 | institution-format-guide 4.5 + historical-defect-checklist | `format_checker.py` reference checks |
| 附录 / 致谢 / 攻读期间成果 | 识别为后置分区，避免误按正文/参考文献规则乱报 | 结构 | institution-format-guide 2.3 / 4.3 | `format_checker.py` zone classifier |

## 已实现原则
1. **不再只报字号**：每类对象都至少对应一种可执行检查。
2. **没有精确数值的项目，不跳过**：改做一致性检查，并在报告里显式标注为 consistency-mode。
3. **规则承诺必须出现在报告覆盖面里**：即使某项最终无问题，也要在 `format-review-report.json` 的覆盖说明 / documentChecks 中出现。
4. **文档级问题需要可批注落点**：页眉、页码、页边距等若有问题，需提供可映射到正文的锚点，保证能进入 `annotations.json` / `annotated.docx`。
