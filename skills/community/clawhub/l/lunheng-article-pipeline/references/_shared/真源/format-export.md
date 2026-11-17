> 版本：v2.18.1（发布版，与 SKILL.md version: 同步）

> 🌐 **语言政策**：产出语言由 Phase 0「目标语言」字段**显式选择**（中文 / English / 中英混 / 其他，**不设默认**），全流程以该字段为准；中文特化按**目标语言客观适用**——含中文时 **G14 中文 AI 痕迹闸必跑**（v2.12.40 起不再是可选项），纯外语时记 `n/a`（客观不适用，非「关闭」）；GB/T 7714-2015 引用规范为可选能力。二者均不构成使用者语种限制。

# 多格式导出（可选，默认 md）

> **原则**：主人不选就不加载导出逻辑，尽可能节省 token。
> **默认**：Phase 5 终稿输出 Markdown（当前行为，零额外 token）。
> **触发**：主人在 Phase 0 定题时或 Phase 5 终稿时选 `--format md/latex/docx/pdf`。
>
> ⚠️ **诚实声明**：**md 是完整支持的**；latex/docx/pdf 三格式是**实验性功能**——命令模板引用的 4 个依赖文件（参考文献.bib / academic-paper 模板 / academic-paper-template.docx / chinese-gb7714-2015-numeric.csl）**论衡当前不自动产出**，需主人自备（见下方「前置条件清单」），且 **pandoc/rsvg-convert 由主人手动跑**（零 exec）。选 latex/docx/pdf 前请确认已满足前置条件，否则会卡壳。**.bib 自动生成机制计划 v2.6.0 落地**。

## 〇、前置条件清单（latex/docx/pdf 必读）

主人选 latex/docx/pdf 前，需自备以下依赖（论衡不自动产出）：

| 依赖 | 用途 | 论衡现状 | 主人自备方式 |
|------|------|---------|------------|
| `final/证据包/参考文献.bib` | pandoc 引文数据（BibTeX 格式） | ❌ 不产出（论衡产出 GB/T 7714 文本，无 .bib 转换机制） | 主人从 T1 文献卡手动转 BibTeX，或等 v2.6.0 |
| `academic-paper`（LaTeX 模板） | `--format latex` 排版 | ❌ 仓库无此文件 | 主人提供 .tex 模板 |
| `academic-paper-template.docx` | `--format docx` 排版 | ❌ 仓库无此文件 | 主人提供 reference-doc |
| `chinese-gb7714-2015-numeric.csl` | 中文 GB/T 7714 引用样式 | ❌ 仓库无此文件 | 主人从 Zotero CSL 仓库下载 |

## 一、format 参数

| 参数 | 输出格式 | 适用场景 | 主人操作 |
|------|---------|---------|---------|
| `--format md`（默认） | Markdown | 公众号 / 知乎 / 商业评论 / 通用 | 无需操作 |
| `--format latex` | LaTeX 学术模板 | 学术论文投稿（LaTeX 排版） | 主人选 + 自备模板/bib/csl + pandoc + LaTeX 引擎 |
| `--format docx` | Word 学术模板 | 学术论文投稿（Word 排版） | 主人选 + 自备 reference-doc/bib/csl + pandoc |
| `--format pdf` | Markdown → PDF（含 SVG 图表嵌入） | 终稿存档 / 打印 | 主人选 + 自备模板/bib/csl + pandoc + rsvg-convert + LaTeX 引擎 |

## 二、导出命令（pandoc 模板）

> 🚫 **以下命令模板全部由「主人」在 host shell 手工执行** —— 论衡 agent（主控 + 全部子代理）**零 exec**，**不执行** `pandoc` / `rsvg-convert` / `xelatex` 或任何 shell 命令。本文件给出命令只为**让主人照抄**，不构成 agent 的执行面。

### `--format md`（默认）
无需额外命令，直接输出 `final/定稿.md`（当前行为）。

### `--format latex`

### `--format docx`

### `--format pdf`

## 三、SVG 图表嵌入（PDF 关键）

`--format pdf` 必须先处理 SVG 图表嵌入，否则图表丢失或变占位框：

> **零外发原则**：SVG 转 PDF 用 rsvg-convert（本地工具，零外发），pandoc 本地跑。⚠️ **本处「零外发」仅指该转换步骤不出网** —— **不等于全流程零外发**（全文/大纲/证据卡片的 LLM provider 外发见 Phase 0 同意口径与 [`external-services.md`](external-services.md)）。
> **⚠️ 替换破坏性警示**：SVG 嵌入的替换是**原地破坏**定稿.md 的临时操作，
> 必须复制备份 + 跑完恢复，否则交付的定稿.md 已被污染。

## 四、Phase 5 终检后的主人自行操作建议

多格式导出**已移出 Phase 0**（主人裁定 v2.12.56）：不在启动阶段预选，也不阻塞流水线。仅在 T8 终检完成后由主控向主人呈现选项与命令模板；执行者是主人本人，论衡 agent 不执行 shell。

### Phase 5（终稿，正式拍板）
**主控 T8 终检时必在对话里向主人主动呈现 6 选项**（不依赖 Phase 0 预选，主人不答 = 默认 md）：
```
- □ A. md（默认，零额外 token）— 公众号/知乎/小红书
- □ B. latex（学术论文投稿）— 需主人自备模板 + 手工跑 pandoc
- □ C. docx（学术论文投稿）— 需主人自备 reference-doc + 手工跑 pandoc
- □ D. pdf（终稿存档/打印）— 需主人自备模板 + 手工跑 pandoc + rsvg-convert
- □ E. 多格式全产（md + latex + docx + pdf 一起）
- □ F. 跳过（只要 md）
```
如主人选 B/C/D → T8 给出命令模板（§二），主人自备前置条件（§〇）后**手工跑 pandoc**；论衡 agent 不执行 shell。
如主人选 A/F → 仅输出 final/定稿.md。

## 四·四、表格样式约定（ECS 实战：16 格矩阵 docx 样式不可控）

- 正文表格统一 **pipe 表格**（`| |`），禁止 HTML 表格 / 嵌套表格（pandoc docx 兼容性）
- 单元格内禁用换行符（docx 转换即碎）；多值单元格用「；」分隔
- ≥8 列宽表（对比矩阵）→ T4 大纲阶段就拆为多子表（每表 ≤6 列），pandoc 参考模板 `academic-paper-template.docx` 预置 Table Grid 样式接管
- 表注写表下方普通段落（「表 N 注：」起头），不写在表格末行单元格内

## 四·五、导出前元数据清洗（ECS 实战：docx 残留 emoji 信任块）

**latex/docx/pdf 导出前必做**（md 默认格式跳过；清洗对象 = 定稿 export 副本，不动 run/ 原件）：
1. **遗留状态 emoji 清洗**：🟢/🟡/🔴/⚠️ 删除或改正文括注；信任级别本身必须保留文字取值——🟡 → `（数据为二手转引，须回溯原始来源）`；⚠️ → `（单方口径数据）`；🟢 直接删标记
2. **元信息自检块剥离**：字数自检表 / SHA256 校验行 / AI 痕迹检查计数表 / 心跳时间戳——这些是过程产物，不进交付稿
3. **清洗后核对**：清洗副本再过一遍 M-Form-7 白名单（操作员报告残留 = P0）；字数按清洗后版本重报（清洗删字后不得超过预算下限）

## 四·六、PDF 渲染验证（回应实测 #9：⚠️ 在 Noto Serif CJK 渲染成 △）

**触发**：主人选 `--format pdf` 并手工跑完 pandoc 后（零 exec，主人执行）。**目的**：抓字体 fallback 乱码（emoji 渲染成 △/豆腐块）与首页文本缺失。

**验证要点**：
- ⚠️ 等 emoji 若仍渲染成 △/□ → 交付文档内警示符号必须用 ▲（U+25B2 纯几何）或【警告】文本，不得用 ⚠️（来源侧已由 T5/主控模板约束；导出侧 §四·五 清洗兜底）
- 抽验结果主人确认后回填「渲染验证：✅」到交付说明；异常 → 定位是字体栈（模板 font-family 缺 emoji 字体）还是内容含 emoji（改 ▲/【警告】）

## 五、与字数判定表 / 投稿就绪检查表的关系

- 字数判定表：无论 format，所有格式都要过字数核验
- 投稿就绪检查表：Word/PDF 转换检查项在 v2.5.0 启用 `--format docx/pdf` 时激活

## 六、限制

- **零 exec**：pandoc / rsvg-convert 由主人在 host shell 手动跑；论衡 agent 不执行 shell 命令
- **模板依赖**：latex/docx/pdf 需主人自备模板（academic-paper.tex / academic-paper-template.docx）+ .bib + CSL（见 §〇 前置条件清单）
- **中文支持**：用 xelatex 引擎 + csl=chinese-gb7714-2015-numeric 处理中文引用
- **.bib 生成机制缺失**：论衡当前不产出 BibTeX，latex/docx/pdf 的 `--bibliography` 依赖主人手动转换；计划 v2.6.0 补 T1「文献卡 → .bib」自动生成
