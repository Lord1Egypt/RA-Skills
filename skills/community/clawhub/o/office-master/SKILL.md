---
name: office-master
description: >-
  办公效率技能库：覆盖 Office/PDF 与 Markdown 双向转换、专业演示设计与 PPT 编程自动化四大能力，并附文档样式与演示大纲的确定性检查脚本；另提供办公品牌与模板上下文记忆，让多次产出保持统一版式。
  当用户说"Word 转 Markdown"、"Markdown 转 PPT"、"文档转换"、"演示设计"、"PPT 自动化"、"样式检查"、"记住品牌与模板偏好"、"办公上下文"时触发。
agent_created: true
metadata:
  version: 1.0.0
  category: 办公效率
  difficulty: 进阶
  architecture: superpower
---

# 办公效率大师

> 把 AI 变成一名「接管格式工作」的办公搭档，让文档在 Office 与 Markdown 间自由流转，并产出品牌级演示。

本技能采用 **superpower 架构**：`SKILL.md` 只做路由，深层 playbook 放在 `references/` 中**按需加载**，细粒度能力放在 `skills/` 子技能，确定性检查交给 `scripts/`，可复用规范放在 `assets/`。

## 何时使用

- 把 Word/Excel/PPT/PDF 转成 Markdown 进入 Git 或做 AI 分析时
- 把 Markdown 生成 Word/PPT/PDF 交付件（带品牌模板）时
- 需要专业级演示设计（品牌风格、排版体系、一致性）时
- 需要 python-pptx 编程批量操作 .pptx（创建/改/提取）时
- 想自动校验文档标题层级、演示大纲结构（CI 门禁）时
- 团队要统一 Office 文档与演示的交付规范时
- 需要让多次文档 / PPT 产出保持统一品牌与版式时

## 能力索引（超级技能路由）

| 任务 | 读取 / 调用 | 关键词（grep 线索） |
|------|------------|---------------------|
| Office↔Markdown 往返、工具选型、失真规避 | [references/office-md-roundtrip.md](references/office-md-roundtrip.md) | 格式转换 往返 markitdown pandoc 源真相 |
| 演示设计系统、品牌风格选型、一致性验证 | [references/presentation-design-system.md](references/presentation-design-system.md) | 演示设计 品牌风格 版式 一致性 python-pptx |
| 文档样式门禁方法论、规则卡控、CI 嵌入 | [references/doc-style-quality-gates.md](references/doc-style-quality-gates.md) | 样式门禁 标题层级 阈值 规则文件 CI |
| Office/PDF 转 Markdown（细粒度调用） | [skills/office-to-md/SKILL.md](skills/office-to-md/SKILL.md) | office-to-md markitdown Word Excel PDF |
| Markdown 转 Office（细粒度调用） | [skills/md-to-office/SKILL.md](skills/md-to-office/SKILL.md) | md-to-office pandoc Word PPT PDF |
| 专业演示设计（细粒度调用） | [skills/presentation-designer/SKILL.md](skills/presentation-designer/SKILL.md) | presentation-designer 品牌 排版 动画 |
| PPT 编程自动化（细粒度调用） | [skills/ppt-automation/SKILL.md](skills/ppt-automation/SKILL.md) | ppt-automation python-pptx 幻灯片 模板 |
| 办公品牌/模板上下文记忆、跨会话复用品牌色板与版式骨架 | [skills/office-context/SKILL.md](skills/office-context/SKILL.md) + [references/office-context-playbook.md](references/office-context-playbook.md) | 上下文 记忆 品牌 模板 office-context 偏好 复用 版式 |

## 内置脚本（确定性、可重复执行）

放在 `scripts/`，纯标准库、零依赖、只读、不联网，规则来自 `assets/`：

- [scripts/check_doc_style.py](scripts/check_doc_style.py) — 校验 Markdown 标题层级一致性（单一 H1、不跳级、重复 slug、frontmatter、残留 token）
- [scripts/check_ppt_brief.py](scripts/check_ppt_brief.py) — 校验演示大纲结构（页数、页标题长度、重复、正文长度）

两者均剥离围栏代码块：块内 `#` / `##` 是注释，不当标题、不当幻灯片页、不算残留 token。

运行示例：

```bash
python3 scripts/check_doc_style.py --check-rules            # 自检规则（0 错误）
python3 scripts/check_doc_style.py docs/ README.md          # 查标题层级（对稿件跑）
python3 scripts/check_ppt_brief.py assets/presentation-brief-template.md   # 查大纲
```

> 作用域：只对**交付稿件**（要转 Word/PPT/PDF 的 .md）跑。别对含 `SKILL.md` 的技能仓库根
> 递归跑——`SKILL.md` 用 `name`/`description`/`metadata`，没有 `title` 键，会刷出无关误报。
> 判断依据与踩坑见 [references/doc-style-quality-gates.md](references/doc-style-quality-gates.md) 第 3、6 节。

## 模板资源

`assets/` 提供可直接套用的规范与模板（被上述脚本读取执行、且自检 0 错误）：

- [assets/doc-style-rules.json](assets/doc-style-rules.json) — 样式/大纲检查规则（单一 H1、深度、必检 token、页数等）
- [assets/presentation-brief-template.md](assets/presentation-brief-template.md) — 演示大纲标准模板（层级/结构均合规的范本）
- [assets/office-context.example.json](assets/office-context.example.json) — 办公上下文示例（品牌五件套 + 模板路径范本，复制改 `assets/office-context.json`）

## 核心原则（始终遵循）

1. **渐进式加载**：先读本路由表与对应 `references/`，再动手；不凭记忆猜工具与语法。
2. **源真相单向**：设一个格式为源（通常 MD），另一方向只派生，避免双向覆盖漂移。
3. **转换前置门禁**：结构规范在转换前校验，比事后修 Office 省力。
4. **样式即功能**：标题层级错 = 分页/目录错，不是美观问题，是正确性。
5. **设计守边界**：脚本只报结构偏差，美观与表达由人定，不替你拍板。
6. **明确边界**：脚本只做确定性检查、只出报告；品牌选择与内容由人负责。

## 与其他技能协作

- 技术文档生成 → `skills-repo/docs-writer`
- 提交/版本规范 → `skills-repo/productivity-master`
- 跨会话个人知识 / 第二大脑记忆 → `skills-repo/productivity-master` 的 `memory-keeper`（与本仓库 `office-context` 正交：前者管知识，本技能只管办公交付物的品牌与版式上下文）
- 本仓库所有子技能来源见各自 `source` 字段，均为 skills.sh 社区成熟技能衍生（仅 `office-context` 为原创，见其字段）
