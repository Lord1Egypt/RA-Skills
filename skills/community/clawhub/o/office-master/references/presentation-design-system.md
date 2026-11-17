# 演示设计系统与一致性验证（presentation-designer × ppt-automation 增量方法论）

> 子技能 `presentation-designer` 给 5 套品牌风格与排版体系，`ppt-automation` 用 python-pptx 落地。
> 本文档补它们**装不下**的决策层：怎么选品牌风格、怎么选每页版式、落地后怎么验证一致性、脚本能/不能替你做什么。

## 1. 决策树：选哪套品牌风格？

```
明确受众与场景
├─ 科技发布会 / 开发者大会？ → 科技 Keynote（深色、极简、大留白）
├─ 企业汇报 / 年报？ → 企业专业（稳重蓝、信息密度适中）
├─ 创业融资 / Pitch？ → 创业融资（强叙事、数据突出）
├─ 金融 / 投研？ → 金融精英（克制、权威感）
└─ 创意 / 营销？ → 创意大胆（强对比、字体表现力）
```

**铁律**：风格服务于受众，不是作者审美。融资用「科技 Keynote」会显得不务实，年报用「创意大胆」会显得不严谨。

## 2. 版式选择矩阵（每页用哪种）

| 内容类型 | 推荐版式 | 原因 |
|----------|----------|------|
| 开场/收尾 | 标题页 | 单焦点，留白大 |
| 问题陈述 | 节页 + 要点 | 制造张力 |
| 解决方案 | 对比 / 三段 | 突出差异 |
| 时间线 / 路线 | 时间线 | 顺序清晰 |
| 数据结果 | 数据图表页 | 一图胜千言 |
| 团队/背书 | 列表页 | 弱化装饰 |

```text
brief 结构（H2 即一页）：
## 开场        -> 标题页
## 问题        -> 节页
## 方案        -> 对比页
## 数据        -> 数据页
## 收尾        -> 标题页
```
> 这份 brief 结构正是 [scripts/check_ppt_brief.py](../scripts/check_ppt_brief.py) 校验的对象：每页 H2、标题不超 60 字、正文不超 400 字、无重复页。

## 3. 排版体系硬规则

| 要素 | 规范 |
|------|------|
| 字号层级 | 标题 24-96pt，正文 ≥18pt，禁小字 |
| 间距系统 | 8pt 基线网格，页边距统一 |
| 色彩 | 主色 ≤2，强调色 ≤1，禁彩虹 |
| 每页动画 | ≤3 个元素，入场淡入为主 |
| 字体 | 全篇 ≤2 款，标题/正文分明 |

## 4. 一致性验证清单（落地后必跑）

用 `ppt-automation` 或脚本抽取文本/属性后核对：

- [ ] 全篇字体 ≤2 款且一致
- [ ] 主色在所有页一致（非逐页手调）
- [ ] 标题字号统一，无忽大忽小
- [ ] 页边距/对齐统一
- [ ] 每页动画元素 ≤3
- [ ] 无两页标题完全相同（逻辑重复）

```bash
# 抽取全部幻灯片标题，人工或脚本比对重复与层级
python3 -c "import pptx; p=pptx.Presentation('deck.pptx'); \
  [print(s.shapes.title.text if s.shapes.title else '') for s in p.slides]"
```

## 5. python-pptx 落地要点

- 用**模板**而非空白演示文稿起步：`Presentation('brand.pptx')` 继承版式与配色。
- 批量生成固定版式时，操作 `slide.layouts[i]` 而非自由定位，保证一致。
- 图片分辨率 ≥1920×1080，避免拉伸模糊。
- 复杂图表先单独做图，再以图片嵌入，别用 python-pptx 手画。

## 6. 典型坑与规避

1. **风格错配受众**：融资用错风格 → 按第 1 节决策树选。
2. **一页塞太多**：信息过载 → 按版式矩阵拆页，每页一焦点。
3. **字体满天飞**：全篇 4-5 种字体 → 锁 ≤2 款。
4. **动画堆砌**：每页 10 个动画 → ≤3，入场为主。
5. **逐页手调样式**：易不一致 → 用模板/版式，不在单页硬改。
6. **忽略一致性验证**：视觉漂移无人发现 → 落地后跑第 4 节清单。

## 7. 实战：从 brief 到品牌级 PPT 的一天

```
09:00 用 assets/presentation-brief-template.md 写 brief，确保层级规范
09:30 python3 scripts/check_ppt_brief.py assets/presentation-brief-template.md  # 过结构门禁
10:00 presentation-designer 套「科技 Keynote」生成初稿
11:00 ppt-automation 用 python-pptx 以品牌模板精确落地
14:00 跑一致性清单（第 4 节）：字体/色/层级/边距/动画
15:00 发现第 3 页标题字号不一致 → 回模板改版式，重生成（不手调单页）
```

> 关键：所有修正回到「模板/版式」层，绝不在单页手改，否则下次批量生成又漂移。

## 8. 设计系统 Token 化（可复用内核）

把品牌规范抽成可加载的 token，而非写死在脚本：

```json
{
  "_comment": "品牌 token 示意（非本仓库脚本必读，仅说明思路）",
  "primary": "#0B66FF",
  "accent": "#FF6B00",
  "font_title": "PingFang SC",
  "font_body": "PingFang SC",
  "title_sizes": {"h1": 54, "h2": 32},
  "grid": 8
}
```

python-pptx 落地时读这份 token 设颜色/字体，保证「改一处全篇生效」。本仓库的 `doc-style-rules.json` 同理是样式规则的唯一事实来源。

## 9. CI 中的演示门禁

```yaml
# brief 结构 + 文档样式进 CI，防止不规范源进入设计流程
- run: python3 scripts/check_ppt_brief.py assets/presentation-brief-template.md
- run: python3 scripts/check_doc_style.py docs/
```

> 注意：CI 只能校验「结构/样式」，不能校验「美观」。视觉最终由人审；脚本把机械错误挡在门前。

## 10. 典型坑与规避（续）

7. **模板版式缺失**：python-pptx 用 `layouts[i]` 但模板没该版式 → 先用 PowerPoint 设计好版式再代码套。
8. **图片拉伸变形**：未按比例缩放 → 锁定宽高比，目标 ≥1920×1080。
9. **中文字体缺失**：环境无中文字体 → 嵌入字体或指定已安装字体（如 PingFang/微软雅黑）。
10. **brief 与成稿脱节**：brief 改了 PPT 没更 → 以 brief 为源，重生成而非手改 PPT。

## 11. 可勾选清单

- [ ] 品牌风格按受众决策树选定
- [ ] 每页版式匹配内容类型
- [ ] 字号/间距/色彩遵循排版体系
- [ ] brief 已用 check_ppt_brief 校验（页数/标题/正文/重复）
- [ ] 落地用模板继承版式，非空白自由定位
- [ ] 一致性清单全项通过（字体/色/层级/边距/动画）
- [ ] 图片分辨率 ≥1920×1080
- [ ] 复杂图表先制图再嵌入
- [ ] 设计 token 化，修正回模板层而非单页
- [ ] brief 为源，成稿靠重生成不手改
- [ ] 演示门禁已接入 CI（结构/样式级）

## 12. 风格速查卡

| 风格 | 主色倾向 | 字号感 | 适用 |
|------|----------|--------|------|
| 科技 Keynote | 深底 + 亮蓝 | 超大留白 | 发布会/技术 |
| 企业专业 | 稳重蓝/灰 | 适中 | 年报/汇报 |
| 创业融资 | 高对比 | 数据突出 | Pitch |
| 金融精英 | 藏青/金 | 克制 | 投研/路演 |
| 创意大胆 | 强撞色 | 表现力 | 营销/活动 |

记住：颜色是信号不是装饰。每套风格主色 ≤2、强调 ≤1，超额即乱。

## 13. 为什么一致性要机器辅助

人眼对「第 3 页标题小了 2pt、第 5 页主色偏了点」几乎无感，但观众整体会觉得「不对劲」。
一致性检查脚本把这类机械偏差量化出来，让人专注「表达是否成立」而非「像素是否对齐」。
脚本是尺子，不是设计师——它告诉你哪里偏，怎么改仍由人定。

## 14. 交付格式与兼容性

| 目标 | 格式 | 注意 |
|------|------|------|
| 放映 | .pptx | 嵌入字体防移位 |
| 只读分发 | .pdf | 用 PowerPoint「另存为 PDF」保版式 |
| 网页嵌入 | 导出图片/PDF | 动画转静态 |
| 协作编辑 | .pptx + 云 | 勿用 python-pptx 覆盖他人手动调整 |

> 一旦用 python-pptx 重新生成，会覆盖人工在 PowerPoint 里的手动微调。约定：脚本产出的是「基线版」，精细手调在基线之上、且不再被脚本覆盖。

## 15. 收尾自检（30 秒）

打开成稿，快速过三问：① 每页一眼能看懂在讲什么？② 字体/颜色从头到尾一致？③ 动画不抢戏（≤3/页）？
三问全过 → 可交付；任一不过 → 回模板/版式改，重生成。别在放映前夜手调 20 页——那是灾难源头。

## 16. 相关子技能与层次边界（L2→L3）

本篇是 **L2 决策层**：只解决「选哪套风格 / 每页用哪种版式 / 一致性怎么机器化验 / 交付格式怎么选」。
落地 API 与逐步操作由 L3 子技能承担，不在本篇复制：

| 你要做的事 | 去 L3 子技能 | 本篇只负责 |
|-----------|-------------|-----------|
| 具体的品牌风格套用与设计执行 | [skills/presentation-designer/SKILL.md](../skills/presentation-designer/SKILL.md) | 风格选型决策树与硬规则 |
| python-pptx 创建 / 修改 / 提取幻灯片 | [skills/ppt-automation/SKILL.md](../skills/ppt-automation/SKILL.md) | 只给落地要点，不列 API 签名 |
| 从 Markdown 生成 .pptx 的初始骨架 | [skills/md-to-office/SKILL.md](../skills/md-to-office/SKILL.md) | 交接「结构已分页」 |
| 从既有 .pptx 抽取文本做复用 | [skills/office-to-md/SKILL.md](../skills/office-to-md/SKILL.md) | 不涉及抽取参数 |
| 品牌五件套跨会话复用 | [skills/office-context/SKILL.md](../skills/office-context/SKILL.md) | 不存储品牌状态 |

同层 references（平级 L2，互不复制）：

- 上游结构就绪与往返失真 → [references/office-md-roundtrip.md](office-md-roundtrip.md)（其第 12 节是本篇的入口）
- brief / 大纲进 CI 的门禁方法论 → [references/doc-style-quality-gates.md](doc-style-quality-gates.md)（本篇第 9 节只引用命令）
- 品牌色板与模板路径的约定文件 → [references/office-context-playbook.md](office-context-playbook.md)

配套确定性工具：[scripts/check_ppt_brief.py](../scripts/check_ppt_brief.py)（大纲结构）+ [assets/presentation-brief-template.md](../assets/presentation-brief-template.md)（合规范本）。

边界一句话：**本篇决定「长什么样、怎么验一致」，L3 决定「怎么把它做出来」。**
