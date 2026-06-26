# Stage / Reference Matrix

Use this table as a quick audit sheet for the current `novel-studio` design.

| 阶段 | 主要 references | 各 reference 职责 | 阶段核心交付物 |
|---|---|---|---|
| Discovery stage | `hot-search-scan.md` | 做热点搜索、趋势扫描、平台差异观察，输出市场信号 | `00A_热点扫描.md` |
| Discovery stage | `intake.md` | 收集用户偏好、限制、平台倾向、优先级，形成可用需求摘要 | `00B_用户偏好.md` |
| Discovery stage | `platform-profiles.md` | 约束平台模式差异，把“平台选择”转成结构选择 | `00C_底盘与切口决策.md` |
| Discovery stage | `market-research.md` | 结合热点扫描和用户偏好，做题材比较、TOP1推荐、标题候选与最终结论 | `00_选题报告.md` |
| Discovery stage | `topic-report-template.md` | 规定 `00_选题报告.md` 的固定模板，确保报告有结论层、不是信息堆积 | `00_选题报告.md`（按模板产出） |
| Story planning stage | `outlining.md` | 根据选题报告做想法扩展、故事承诺、结构选择、大纲与前几章方向 | `01_想法.md`、`02_大纲.md`、可选 `04_章节骨架.md` |
| Story planning stage | `style-bible.md` | 锁定叙述方式、节奏密度、对话比例、禁用套路，防止后续风格漂移 | `01A_风格圣经.md` |
| Story planning stage | `anti-template-checklist.md` | 检查选题是不是只有题材名、没有发动机 | `00C_底盘与切口决策.md`、`01B_总主线与卷级推进.md` |
| Story planning stage | `book-level-review.md` | 提前判断长篇承重风险，把总主线和卷级推进写死 | `01B_总主线与卷级推进.md` |
| Character system stage | `character-bible.md` | 定义主角、核心配角、反派、关系、动机、冲突、弧线 | `03_人物小传.md`、`characters/*.md` |
| Drafting stage | `opening-design.md` | 为第一批正文设置开篇门，明确前三章、前十章、前二十章任务 | `04A_开篇设计.md` |
| Drafting stage | `drafting.md` | 生成真实章节初稿、章节推进、批次写作、自检、防敷衍 | `manuscript/*.md` |
| Drafting stage | `continuity-ledgers.md` | 维护世界规则、伏笔、关系、资源四类账本，防止长篇漂移 | `05B_世界规则账本.md`、`05C_伏笔回收台账.md`、`05D_关系状态表.md`、`05E_能力与资源变化表.md` |
| Polishing stage | `polishing.md` | 润色正文、去AI痕迹、提高清晰度、节奏和情绪表现 | 润色后的 `manuscript/*.md` |
| Proofreading stage | `proofreading.md` | 做 continuity / logic / OOC / consistency 检查，形成问题清单或无阻塞结论，并给出明确 gate judgment | 校对结论、修订建议、明确 judgment |
| Final review and delivery stage | `final-review.md` | 做最终交付判断：pass / conditional pass / rework required | 最终评审结论、交付说明 |
| Final review and delivery stage | `file-structure.md` | 规定项目目录、命名、顶层文件、characters / manuscript 结构 | 完整项目目录结构 |
| Final review and delivery stage | `feishu-sync.md` | 规定飞书 Wiki 同步逻辑、目录映射、节点创建规则 | 可选 Feishu Wiki 同步结果 |
| 全流程支撑 | `workflow.md` | 定义总流程、阶段门禁、用户明确放行规则、回退逻辑 | 流程约束本身（不直接产出小说内容） |
| 全流程支撑 | `state-management.md` | 规定 `.novel-state.json` 的读取、写回、审批、阻塞、恢复逻辑 | `.novel-state.json` |

## Quick stage summary

### Discovery stage
- 目标：先看市场，再收偏好，再形成结论型选题报告
- 交付：`00A_热点扫描.md`、`00B_用户偏好.md`、`00_选题报告.md`

### Story planning stage
- 目标：把选题结论变成可执行故事骨架
- 交付：`01_想法.md`、`01A_风格圣经.md`、`01B_总主线与卷级推进.md`、`02_大纲.md`、可选 `04_章节骨架.md`

### Character system stage
- 目标：把人物体系做成可直接支持写作的角色包
- 交付：`03_人物小传.md`、`characters/*.md`

### Drafting stage
- 目标：先通过 Opening Gate，再产出真实可用初稿
- 交付：`04A_开篇设计.md`、`manuscript/*.md`、`05B-05E` 账本

### Polishing stage
- 目标：提升语言质量和人类感
- 交付：润色后的 `manuscript/*.md`

### Proofreading stage
- 目标：拦截逻辑、一致性、人设问题
- 交付：校对结果 + 修订建议 + 明确 judgment

### Final review and delivery stage
- 目标：判断能否交付，并完成交付/同步
- 交付：最终评审结论、交付说明、可选飞书同步结果
