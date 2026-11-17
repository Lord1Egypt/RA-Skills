# Office ↔ Markdown 双向往返工作流（office-master 增量方法论）

> 子技能 `office-to-md` / `md-to-office` 负责「格式互转」。本文档补它们**装不下**的编排层：
> 什么时候该往哪个方向转、用哪个工具、转换前后要做什么、怎么避免内容在往返中失真。

## 1. 决策树：该往哪转？

```
手上有 Office 文档，想做什么
├─ 想进 Git / 做 diff / AI 分析？ → office-to-md（Word/Excel/PPT/PDF → MD）
├─ 想交付正式文件？ → md-to-office（MD → Word/PPT/PDF）
└─ 已有 MD，要生成演示？ → md-to-office(PPT) 或 presentation-designer

转完之后还要再转回来吗？
├─ 是 → 警惕往返失真（见第 4 节），优先单向源为真
└─ 否 → 安全
```

**铁律**：选一个格式当「源真相」（source of truth），另一方向只作派生。别让 Word 和 MD 互相覆盖，否则必漂移。

## 2. 工具选型矩阵

| 任务 | 工具 | 优点 | 局限 |
|------|------|------|------|
| Office → MD | markitdown | 保留标题/表格/列表，批量 | 复杂排版/文本框丢失 |
| MD → Word/PDF | Pandoc | 模板驱动、格式稳 | 复杂 Word 排版不全 |
| MD → PPT | Pandoc / python-pptx | 按标题分页 | 无动画、版式简 |
| PPT 编程操作 | python-pptx | 精确控制、可批处理 | 高级效果不支持 |

```bash
# Office → MD（office-to-md 工作流）
pip install markitdown[all]
markitdown input.docx -o output.md

# MD → Word（md-to-office 工作流）
pandoc README.md -o output.docx --reference-doc=template.docx

# MD → PPT（按 H1/H2 分页）
pandoc deck.md -o deck.pptx
```

## 3. 转换前检查清单

- [ ] 确认「源真相」格式（Word 还是 MD），避免双向覆盖
- [ ] MD 侧标题层级规范（用 [scripts/check_doc_style.py](../scripts/check_doc_style.py) 校验，见 `doc-style-rules.json`）
- [ ] 图片是否需单独导出（markitdown 不嵌入图片）
- [ ] 表格是否复杂到需手工校（嵌套表常丢）
- [ ] 是否需要参考模板（Word 用 `--reference-doc`）

## 4. 往返失真与规避

| 元素 | 去程(Office→MD) | 回程(MD→Office) | 规避 |
|------|----------------|----------------|------|
| 标题层级 | 保留 | 保留 | 保证 MD 层级规范 |
| 表格 | 保留（简单表） | 保留 | 嵌套表先拆平 |
| 列表 | 保留 | 保留 | — |
| 图片 | 不嵌入（仅描述） | 需重新指定 | 用图床/独立资源目录 |
| 文本框/批注 | 丢失 | 不支持 | 重要内容移入正文 |
| 修订痕迹 | 不保留 | 不支持 | 定稿后再转 |
| 动画/过渡 | 不支持 | 不支持 | PPT 用 presentation-designer 后处理 |

> 关键：把「会丢的东西」提前搬到正文中。修订痕迹、批注、文本框若重要，先固化进正文再转，否则转换即消失。

## 5. 批量与目录级转换

```bash
# 批量把 ./docs 下所有 docx 转 md
for f in docs/*.docx; do
  markitdown "$f" -o "${f%.docx}.md"
done

# 批量把 md 转 docx（共用模板）
for f in *.md; do
  pandoc "$f" -o "${f%.md}.docx" --reference-doc=template.docx
done
```

> 批量前先对小样本验证格式，再全量；避免几百个文件一起出错难排查。

## 6. 典型坑与规避

1. **双向覆盖**：Word 改了又从旧 MD 转回 Word → 设源真相，派生方向单向。
2. **图片消失**：markitdown 不嵌入图 → 转完 MD 缺图，需配图床或资源目录。
3. **嵌套表崩坏**：多层表格转换后错位 → 先拆成平表再转。
4. **模板忘了带**：Pandoc 不指定 `--reference-doc` 用默认样式 → 交付件不统一。
5. **PDF  whence**：PDF 转 MD 只有文本层，扫描件需 OCR（Vision）而非 markitdown。
6. **PPT 动画没了**：Pandoc/python-pptx 无动画 → 需要动画用 presentation-designer 补。

## 7. 实战：把一个产品文档做成「MD 源 + Word 交付」

```
# 1) 作者用 MD 写（源真相），保证层级规范
python3 scripts/check_doc_style.py product.md        # 先过样式门禁

# 2) 发布时派生 Word 交付件（不回写 MD）
pandoc product.md -o dist/product.docx --reference-doc=brand.docx

# 3) 评审意见若改了 Word，手动同步回 MD（源真相），不反向覆盖
#    约定：Word 是派生，review 完删掉，避免双源
```

> 这套单向流是避免漂移的关键：永远只有 MD 能被改并重新生成 Word，Word 不回流。

## 8. 转换质量评分卡（交付前自检）

| 维度 | 通过标准 |
|------|----------|
| 标题层级 | 无跳级、单一 H1（check_doc_style 通过） |
| 表格 | 无错位、无合并单元格丢失 |
| 图片 | 全部存在且路径正确 |
| 列表 | 层级正确、无变正文 |
| 模板 | 字体/页边距符合品牌 |
| 链接 | 内部锚点存活（可用 docs-writer 的 check_md_links） |

任意一项不通过 → 回 MD 修正后重转，别在 Word 里手动补（否则下次生成又丢）。

## 9. CI 集成（源真相保护）

```yaml
# 仅校验 MD 源，防止不规范的源进入转换流水线
- run: python3 scripts/check_doc_style.py docs/
- run: python3 scripts/check_ppt_brief.py assets/presentation-brief-template.md
```

> 把样式/大纲门禁放在「转换前」而非「转换后」，从源头保证派生文件质量，比事后修 Word 省力。

## 10. 典型坑与规避（续）

7. **把 PDF 当可编辑源**：PDF 转回 MD 只有文本，版式全无 → PDF 只作归档，编辑回源格式。
8. **Excel 多 Sheet 混为一谈**：markitdown 每 Sheet 独立分节，转回时易串 → 转前确认 Sheet 边界。
9. **长文档一次转崩**：百页文档转换报错难定位 → 按章节分拆转换再拼。
10. **样式靠手工调**：每次 Pandoc 重生成都重置样式 → 用 `--reference-doc` 固化品牌，不手调。

## 11. 可勾选清单

- [ ] 已定「源真相」格式，派生方向单向
- [ ] MD 标题层级已用 check_doc_style 校验通过
- [ ] 图片/表格/批注等易丢元素已预处理
- [ ] 选对工具（markitdown / Pandoc / python-pptx）
- [ ] 批量前小样本验证
- [ ] 交付件用统一参考模板
- [ ] 动画/过渡等非结构元素已另行处理
- [ ] 转换质量评分卡全项通过
- [ ] 样式/大纲门禁已接入 CI（转换前）
- [ ] 评审改动已同步回源真相，未反向覆盖

## 12. 与演示技能的衔接

当 MD 源要变成幻灯片时，走两条互补路径：

- **快速分页**：`md-to-office` 的 Pandoc 路径，按 H1/H2 直接分页成 PPT——适合内部汇报、草稿。
- **品牌级设计**：把 MD 整理成 brief（用 [assets/presentation-brief-template.md](../assets/presentation-brief-template.md) 结构），交给 `presentation-designer` 套 5 套品牌风格，再用 `ppt-automation` 以 python-pptx 精确落地。

> 衔接点：brief 的层级规范（单一 H1、H2 为页）正是 [scripts/check_doc_style.py](../scripts/check_doc_style.py) 与 `check_ppt_brief.py` 校验的对象。源 MD 规范 → 自动分页不出错 → 设计层只管美化。

## 13. 格式映射速查

| Markdown | Word | PowerPoint | 备注 |
|----------|------|------------|------|
| `#`/`##` | 标题 1/2 | 标题页/节 | 分页依据 |
| `-` 列表 | 项目符号 | 要点 | 平铺 |
| `|---|` 表 | 表格 | 表格 | 简单表稳 |
| `![alt](x)` | 图片 | 图片 | 路径需存在 |
| `> 引文` | 引用块 | 引用框 | 样式随模板 |
| ````代码```` | 代码块 | 代码块 | 语言标注保高亮 |

记住这张表，写 MD 时就按目标格式组织，转换几乎零摩擦。

## 14. 何时**不**该转

转换不是银弹，以下情况别硬转：

- 高度设计感的宣传册/画册：版式靠视觉而非结构，转 MD 丢失所有设计 → 留在设计工具。
- 带宏/公式的复杂 Excel：markitdown 只取文本，公式变值 → 保留 xlsx 源。
- 扫描件 PDF：无文本层，markitdown 取不到 → 先 OCR 再决定。

识别「该转」与「不该转」比会转更重要；强行转换只会产出难维护的半成品。

## 15. 相关子技能与层次边界（L2→L3）

本篇是 **L2 决策层**：只解决「往哪转 / 用什么工具 / 怎么不失真 / 何时不该转」。
具体命令语法与参数细节由 L3 子技能承担，不在本篇复制：

| 你要做的事 | 去 L3 子技能 | 本篇只负责 |
|-----------|-------------|-----------|
| Office/PDF → Markdown 的实际调用 | [skills/office-to-md/SKILL.md](../skills/office-to-md/SKILL.md) | 判断该不该转、失真预期 |
| Markdown → Word/PPT/PDF 的实际调用 | [skills/md-to-office/SKILL.md](../skills/md-to-office/SKILL.md) | 选模板策略、源真相方向 |
| 转成 PPT 后的版式与品牌设计 | [skills/presentation-designer/SKILL.md](../skills/presentation-designer/SKILL.md) | 只交接「结构已就绪」 |
| .pptx 的编程批量改写 | [skills/ppt-automation/SKILL.md](../skills/ppt-automation/SKILL.md) | 不涉及 python-pptx API |
| 品牌 / 模板跨会话复用 | [skills/office-context/SKILL.md](../skills/office-context/SKILL.md) | 不存储品牌状态 |

同层 references（平级 L2，互不复制）：

- 转换前的结构门禁方法论 → [references/doc-style-quality-gates.md](doc-style-quality-gates.md)（本篇第 3、9 节只引用其命令，规则演进见该篇）
- 转成演示后的设计系统 → [references/presentation-design-system.md](presentation-design-system.md)（本篇第 12 节交接点的下游）
- 品牌 / 模板上下文的落地约定 → [references/office-context-playbook.md](office-context-playbook.md)

边界一句话：**本篇决定「转不转、往哪转」，L3 决定「怎么敲命令」，兄弟 L2 决定「转之前卡什么、转之后怎么设计」。**
