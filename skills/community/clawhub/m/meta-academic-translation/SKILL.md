---
name: meta-academic-translation
version: 1.0.0
description: |
  由 model-distillation 从教师技能 academic-translation 蒸馏并增强的超越型元技能，
  在教师能力之上叠加自验证、自我反思、super-agent 编排与持续自进化闭环，逐步超越教师。
agent_created: true
visibility: public
---
# meta-academic-translation（蒸馏超越型元技能）

> 由 `model-distillation` 从教师技能 **academic-translation** 蒸馏并增强生成。
> 生成时间：2026-07-23 05:14:23 ｜ 蒸馏机制：跨模型蒸馏（见 meta-evolver 北极星策略）

## 来源能力签名（教师）
- 标题层级：学术翻译 Skill, 工作流概览, 输入参数（结构化契约）, 不在范围内（请改用其他工具）, ⛔ Preflight（任何翻译前的开场白）, Step P1：输入完整性, Step P2：模式 + 方向 + 术语库三选项澄清, Step P3：路由
- 显性工作流步骤（17 步）：
  1. 翻译方向：
  2. 输出深度：
  3. 术语库：
  4. 公式（`$...$` / `\\begin{equation}` / `\\[...\\]`）原样保留——它们是 LaTeX 编译产物，翻译会破坏排版且没有"译法"
  5. `\\cite{}` / `\\ref{}` / `\\eqref{}` / `\\autoref{}` 原样保留——这些是引用键，翻译后会让交叉引用全部断裂
  6. 专业术语优先用 [refs/glossary/](refs/glossary/) 中的标准译法；术语库未覆盖时保留原文 + 在括号附译法（例 "embedding（嵌入）"），方便读者反向查阅
  7. 数字 / 单位 / 化学式 / 算法名原样保留——这些是数据事实，翻译只会引入错误
  8. 段落结构（句子边界）保持 1:1 对应——便于 Step 2 反思阶段做对齐
  9. **表格保留 = 结构原样 + 表头/数据不翻译 + 仅 caption 翻译**——这是高频踩坑点，独立成条说明：
  10. **阻断流程**——不要自动进入 Step 3，等待用户输入。
  11. **展示三件物**给用户：
  12. **三选项询问**（措辞统一）：
  13. **选项 b 的回环**：应用用户修改 → 重新跑 Step 2 反思一致性 → 再回到本检查点询问，最多 3 轮，超出后让用户在 a/c 之间二选一（防止无限改）。
  14. **选项 c 的输出收敛**：标记 `output_files = [01, 02, 04, 06, 07]`（跳过 03 雅化和 05 LaTeX 投稿版；07 HTML 仍生成，顶栏标 "学术规范版（未雅化）"），并在 `06-self-check.md` 注明"用户在 Step 2 后停止"。
  15. **页码 / 行号**（PDF 来源）

## 增强点（超越教师）
1. **可靠自验证**：每步产出后用 `reason-verify` 做命题一致性/事实锚定校验，reliability<0.8 即回退重做。
2. **自我反思闭环**：执行后写入 `self-reflection-loop`，沉淀失败模式到 learner。
3. **整合进 super-agent**：作为节点接入「感知→规划→执行→自验证→反思→记忆」超级智能体闭环，可被长程任务编排。
4. **对抗验证蒸馏质量**：对蒸馏出的关键决策规则做反例测试，防止只学到表面话术。
5. **持续自进化**：注入 learner，纳入 meta-evolver 的 sense/plan/record 闭环，跨会话越用越强。

## 教师 vs 学生 对比
| 维度 | 教师(academic-translation) | 学生(meta-academic-translation) |
| --- | --- | --- |
| 能力来源 | 原始 SKILL.md（20811 字符） | 蒸馏提取 + 元进化增强 |
| 工作流 | 17 步显性流程 | 同流程 + 自验证钩子 + 反思步 |
| 工具脚本 | extract_pdf.py, learner.py, preserve_latex.py | 继承 + reason-verify/self-reflection 钩子 |
| 失败防护 | 已识别 1 处 | 显式 limits + 对抗验证 |
| 自进化 | 视技能而定 | 强制注入 learner，纳入 meta-evolver 闭环 |
| 集成 | 单点 | 接入 super-agent 感知→规划→执行→自验证→反思→记忆闭环 |

## 使用
直接调用本技能完成「academic-translation」领域的任务；本技能在教师能力之上叠加自验证与反思，输出更可靠、可追溯。

## 已知限制（来自教师蒸馏 + 元进化补充）
- | **PDF 加密 / 受密码保护** | `pdfplumber` / `pypdf` 抛 `PdfReadError` | 询问用户密码并临时解密到内存，不写回原文件；用户拒绝则终止本次任务 |
| **arXiv 下载失败** | `scripts/arxiv_fetch.sh` 非 0 退出 / 网络超时 / 404 | 重试 1 次（指数退避）；仍失败询问 [a] 用户改贴 abs URL [b] 用户上传 PDF 替代 [c] 终止；不要静默切到 PDF 兜底 |
| **`preserve_latex --verify` 失败** | 译文中占位符未还原 / 数字被改写 / 公式被翻译 | 阻断输出。展示具体失败 token 给用户，回退到 Step 2 重跑反思阶段（最多 2 次）；2 次仍失败 → 标注 `output_files += [ERROR.md]`，让用户人工修订 |
| **段落 1:1 对应失败** | Step 1 输出段落数 ≠ 输入段落数（合并/拆分句子） | 该段单独重跑 Step 1，强化 Prompt 中"保持句子边界"约束；连续 2 次失败 → 标记该段 `paragraph_kind="manual_review"`，跳过 Step 2/3 等用户处理 |
| **术语库加载失败** | YAML 解析错误 / 文件不存在 / 内置 + 自定义有冲突 | 不要静默继续。明确提示「术语库加载失败：{原因}」；冲突时展示冲突术语列表让用户选 keep [内置] / [自定义] / [双语并列]；解析错误 → 退化为不带术语库运行并在 `06-self-check.md` 标注 |
| **`translation-output/` 目录已存在同 paper-id 产物** | 同 ISO-time 内重复触发 / 同 paper-id 翻译过 | 不覆盖。在目录后追加 `-r2 / -r3` 后缀新建；同时在新目录 `00-history.md` 写明上次产物路径，便于用户 diff |
| **LLM 上下文超限** | 单段 + glossary + 系统 prompt 超 token 上限 | 自动按句号切分该段为子段，分别翻译后拼接；拼接后重跑 Step 1 自动校验；若切分后仍超限 → 标记该段 `manual_review` 并告知用户 |
| **`config/user-glossary.template.yaml` schema 不符** | 用户上传的术语表缺必需字段 / 字段类型错 | 不要静默丢弃整个文件。逐条校验，合法条目正常加载，非法条目集中报告给用户「以下 N 条术语被忽略：{list}」 |
| **输出体积超 150% 警戒** | 三档对照 + 双栏总字符数 > 原文 1.5× | 多数为正常（学术英文译中文常 1.3-1.5×）；> 2.0× 才告警，提示用户检查是否雅化阶段过度添加了解释 |
| **表格丢失 / 表格被翻译** | 译文中表格行数 < 原文 80% / 表格分隔符行 `\|---\|` 缺失 / 表头被中文替换（数据列名通常应保持原文） | 阻断该段输出。回退到 Step 1 重跑该段时强制走"表格整段占位符化"路径（仅翻译 caption）；连续 2 次失败 → 标 `manual_review`，并在 06-self-check 列出所有受影响表格 |
| **`07-bilingual.html` 未生成** | standard / full 模式下 `output_dir/07-bilingual.html` 不存在 | 视为输出失败。先尝试基于 `04-bilingual.md` + 模板 `assets/templates/bilingual-html.html` 重新渲染一次；仍失败 → 在 `06-self-check.md` 顶部红字标"HTML 生成失败：{原因}"，并提示用户「请明确说『生成 HTML』后我可重试」，**不允许沉默交付** |

**原则**：异常先告知用户、再按规则处理；任何 fallback 路径都要在 `06-self-check.md` 中留痕，便于用户审计。

---

## 模块概览

| 模块 | 职责 | 文件 |
|---|---|---|
| **输入路由** | 分流 PDF / arXiv / LaTeX / text，章节切片 + Provenance | [modules/input-router.md](modules/input-router.md) |
| **三步翻译** | 直译 → 反思 → 雅化的算法实现 | [modules/three-step-translation.md](modules/three-step-translation.md) |
| **学术润色** | 顶会风格 + Chinglish 校正 + 去 AI 味 | [modules/academic-polish.md](modules/academic-polish.md) |
| **双栏导出** | 中英对照 / 三档对照 / LaTeX 渲染 | [modules/bilingual-export.md](modules/bilingual-export.md) |

## 参考资料

| 类别 | 文件 |
|---|---|
| 顶会术语库 | [refs/glossary/](refs/glossary/) |
| Chinglish 模式 | [refs/chinglish-patterns.md](refs/chinglish-patterns.md) |
| Word Choice 替换表 | [refs/word-choice-table.md](refs/word-choice-table.md) |
| 去 AI 味规则 | [refs/anti-ai-patterns.md](refs/anti-ai-patterns.md) |
| 公式 / 引用保留 | [refs/formula-preservation.md](refs/formula-preservation.md) |
| 章节惯例 | [refs/section-conventions.md](refs/section-conventions.md) |

## 配置与扩展

- 用户自定义术语库：[config/user-glossary.template.yaml](config/user-glossary.template.yaml)
- 输出目录：`translation-output/{ISO-time}-{paper-slug}/`（自动创建）
- LaTeX 字体：默认 xeCJK + STSong / SimSun fallback
- PDF 字体：默认 PingFang SC / Noto Sans CJK fallback

---

> ⛔ **Do NOT pre-load all refs/ files** —— `refs/` 下共 5 份规则库 + 5 份会议术语库（合计 ~26K Token），全部预读会让 Skill 启动 Token 翻倍且与本次任务无关。
>
> **加载顺序铁律**：
> 1. 仅本文件（SKILL.md，~360 行）默认读入；
> 2. 进入 Preflight P3 路由后，按 📖 MANDATORY 标记**逐条**触发加载（最多 3 个文件即可覆盖任何输入类型）；
> 3. Step 1/2/3 中的 inline 加载触发器**仅在该 Step 启动时**激活（标准模式 2b 永远不读 word-choice-table.md / anti-ai-patterns.md，因为不进 Step 3）。
---

## 自进化学习系统（越用越好用、越用越高效）

本技能内置通用学习模块 `scripts/learner.py`。每次使用后自动复盘、积累经验，逐步提升输出质量与执行效率，无需人工维护。

### 记忆文件
`learned_patterns.json`（位于本技能目录）记录：操作总数、各能力使用频次、错误模式、用户偏好、改进建议。

### 使用后请调用（Bash）

```bash
# 记录一次成功使用（--capability 填本次主要能力名，如「简历优化」「比价」）
python scripts/learner.py record <本技能目录> --capability 简历优化
# 记录一次失败/异常
python scripts/learner.py record <本技能目录> --capability 简历优化 --fail --error 格式识别失败 --note "用户上传了非标准文件"
# 记录用户偏好（下次直接使用）
python scripts/learner.py prefer <本技能目录> --key 输出语言 --val 中文
# 查看累计洞察（高频能力 / 反复错误）
python scripts/learner.py insight <本技能目录>
# 自动复盘（错误≥3次 或 操作≥10次 时给出改进建议）
python scripts/learner.py reflect <本技能目录>
```

### 迭代规则
- **错误累计 ≥3 次** → 主动增加预检/兜底步骤，并将经验回写本 SKILL.md。
- **操作数 ≥10 次** → 分析高频能力优先打磨示例与质量，低频能力评估精简或合并。
- **重要用户偏好** → 写入 `learned_patterns.json`，下次调用直接采用，减少重复询问。

> 越用越懂你：第一次用是通用能力，第十次用已沉淀为你专属的最佳实践。
- 蒸馏不保证覆盖教师全部隐式知识，首次使用需对照教师原技能核验关键决策。
