# Workflow：从接到任务到可验证交付

这是 IFQ 的主干流程，不再只是「junior designer 怎么汇报」。

目标是同时做到 5 件事：

1. 先把事实和资产找对
2. 先把方向和边界问清，但不被低风险问题卡住
3. 先用模板和 placeholder 锁结构
4. 让人类只在真正高杠杆的位置介入
5. 交付前用证据而不是感觉验收

你仍然可以把自己看作用户的 junior designer，但现在还要多一层角色：**设计系统操作员**。你的工作不是“做一张看起来不错的图”，而是把任务推进到可验证、可交付、可复用。核心理念是：**让 AI 发挥更大效能**，把人类从反复解释细节里解放出来，把 agent 从空白页猜测里拉回可执行流程。

## 默认执行姿态

**先产出可纠偏草稿，不要先制造问卷。** 只有当答案会改变输出形态、事实真实性、法律/授权边界、或最终文件格式时，才在开工前卡住。

默认路径：

1. 读用户 prompt，匹配 `references/modes.md` 和 `assets/templates/INDEX.json` 的 `modeRoutes`。
2. 如果缺上下文但能安全假设，写入 HTML 顶部 assumptions comment，并用明显 placeholder 标出未决事实。
3. 先 fork 模板，锁住信息架构、版面节奏、字体/色彩系统。
4. 用真实内容替换能确定的部分；不能确定的部分保持 labeled placeholder，不编造。
5. 验证渲染、交互、字体、响应式和导出边界，再交付。

这条路径对人类友好，因为他们不用先回答十几个低价值问题；对 AI agent 友好，因为每一步都有明确文件、模板和验证标准。

## 问问题的艺术

问题的目标是减少返工，不是证明自己谨慎。不要把“缺一点上下文”当成停止工作的理由。

**什么时候必须问**：缺少会改变作品类型的决定（比如 deck 还是 landing）、缺少必须真实的事实/资产/数据源、缺少授权素材、用户要求的最终格式会改变技术路线（比如可编辑 PPTX）、或用户描述互相矛盾。

**什么时候不要问**：小修小补、follow-up 任务、用户已经给了明确 PRD+截图+上下文、问题只影响 visual polish、或者可以用 labeled placeholder 和 assumptions comment 安全推进。

**怎么问**：大部分 agent 环境没有结构化问题 UI，在对话里用 markdown 清单问即可。**一次性把阻塞问题列完让用户批量答**，不要一来一回一个个问。非阻塞问题写进 assumptions comment。

补充规则：

- 如果事实不确定，先搜再问；搜索不到就标为 unresolved，不要编
- 如果用户给的上下文已经足够，不要机械追问
- 如果问题只影响 visual polish，不影响结构，不要在开工前卡住

## 设计上下文清单

每个设计任务都要在脑内覆盖这 5 类问题；只有阻塞项才需要问用户：

### 1. Design Context（最重要）

- 有没有现成的design system、UI kit、组件库？在哪？
- 有没有品牌指南、色彩规范、字体规范？
- 有没有可以参考的现有产品/页面截图？
- 有没有codebase可以读？

**如果用户说"没有"**：
- 帮他找——翻项目目录、看有没有参考品牌
- 还没有？明确说："我会基于通用直觉做，但这通常做不出符合你品牌的作品。你考虑下是否先提供一些参考？"
- 实在要做，就按`references/design-context.md`的fallback策略办

### 2. Variations维度

- 想要几种variations？（推荐3+）
- 在哪些维度上变？视觉/交互/色彩/布局/文案/动画？
- 希望variations都"接近预期"还是"一张地图，从保守到疯狂"？

### 3. Fidelity和Scope

- 多高保真？线框图 / 半成品 / 真实data的full hi-fi？
- 覆盖多少flow？一屏 / 一个flow / 整个产品？
- 有没有具体的「必须包含」元素？

### 4. Tweaks

- 希望能实时调整哪些参数？（颜色/字号/间距/layout/文案/feature flag）
- 用户自己要不要在做完后继续调？

### 5. 问题专属（至少4个）

针对具体任务问4+个细节。例如：

**做landing page**：
- 目标转化动作是什么？
- 主要受众？
- 竞品参考？
- 文案谁提供？

**做iOS App onboarding**：
- 几步？
- 需要用户做什么？
- 跳过路径？
- 目标留存率？

**做动画**：
- 时长？
- 最终用途（视频素材/官网/社交）？
- 节奏（快/慢/分段）？
- 必须出现的关键帧？

## 阻塞问题模板

只有遇到真正阻塞的新任务时，才用这个结构。能先做可纠偏草稿时，把非阻塞问题写进 HTML 注释：

```markdown
开始前想跟你对齐几个问题，一次列齐你批量回答就行：

**Design Context**
1. 有设计系统/UI kit/品牌规范吗？如果有在哪？
2. 有可以参考的现有产品或竞品截图吗？
3. 项目里有codebase可以读吗？

**Variations**
4. 想要几种variations？在哪些维度上变（视觉/交互/色彩/...）？
5. 希望都是"接近答案"还是从保守到疯狂的一张地图？

**Fidelity**
6. 保真度：线框 / 半成品 / 带真数据full hi-fi？
7. Scope：一屏 / 一整个flow / 整个产品？

**Tweaks**
8. 希望做完后能实时调哪些参数？

**具体任务**
9. [任务专属问题1]
10. [任务专属问题2]
...
```

## Junior Designer 模式

这是整个 workflow 最重要的环节。**不要接到任务就从空白页乱冲，也不要把低风险问题变成等待。** 步骤：

### Pass 1：Assumptions + Placeholders（5-15分钟）

HTML文件头部先写你的**assumptions+reasoning comments**，像junior给manager汇报：

```html
<!--
我的假设：
- 这是给XX受众看的
- 整体tone我理解为XX（基于用户说的"专业但不严肃"）
- 主要flow是A→B→C
- 色彩我想用品牌蓝+暖灰，不确定你想不想要accent色

未解的问题：
- 第3步的数据从哪里来？先用placeholder
- 背景图用抽象几何还是真照片？先占位

如果你看到这里觉得方向不对，现在是成本最低的时候改。
-->

<!-- 然后是带placeholder的结构 -->
<section class="hero">
  <h1>[主标题位 - 等用户提供]</h1>
  <p>[副标题位]</p>
  <div class="cta-placeholder">[CTA按钮]</div>
</section>
```

**保存 → 如果环境支持就 show 用户；如果用户要求直接完成或环境不支持交互预览，就继续 Pass 2，并保留 assumptions comment 方便后续纠偏。**

### Pass 2：真实组件+Variations（主力工作量）

方向足够明确后，开始填充。这时：
- 写React组件替换placeholder
- 做variations（用design_canvas或Tweaks）
- 如果是幻灯片/动画，用starter components起手

**做到一半尽量 show 一次**。如果当前任务是一次性自动交付，就在最终报告里明确哪些地方是 assumptions/placeholder，避免用户误以为全是事实。

### Pass 3：细节打磨

用户满意整体后，打磨：
- 字号/间距/对比度微调
- 动画timing
- 边界case
- Tweaks面板完善

### Pass 4：验证+交付

- 用宿主浏览器或截图工具验证（见 `references/verification.md`）
- 打开浏览器肉眼确认；没有浏览器工具时至少做静态 HTML / 链接 / 字体 / 远程 runtime 检查
- 总结**极简**：只说caveats和next steps

## Variations的深度逻辑

给variations不是给用户制造选择困难，是**探索可能性空间**。让用户mix and match出最终版本。

### 好的variations长什么样

- **维度明确**：每个variation在不同维度上变（A vs B只换配色，C vs D只换layout）
- **有梯度**：从「by-the-book保守版」到「大胆novel版」逐级递进
- **有记号**：每个variation有短label说明它在探索什么

### 实现方式

**纯视觉对比**（静态）：
→ 用`assets/design_canvas.jsx`，网格布局并排展示。每个cell带label。

**多选项/交互差异**：
→ 做完整原型，用Tweaks切换。例如做登录页，"布局"是tweak的一个选项：
- 左文案右表单
- 顶部logo+中央表单
- 背景全屏图+浮层表单

用户开关Tweaks就能切换，不需要打开多个HTML文件。

### 探索矩阵思考

每次设计，脑内过一遍这些维度，挑2-3个来给variations：

- 视觉：minimal / editorial / brutalist / organic / futuristic / retro
- 色彩：monochrome / dual-tone / vibrant / pastel / high-contrast
- 字型：sans-only / sans+serif对比 / 全衬线 / 等宽
- Layout：对称 / 非对称 / 不规则grid / full-bleed / 窄栏
- Density：稀疏呼吸 / 中等 / 信息密集
- 交互：极简hover / 丰富micro-interaction / 夸张大动画
- 材质：flat / 有阴影层次 / 纹理 / noise / 渐变

## 遇到不确定的情况

- **不知道怎么做**：坦白说你不确定；如果能安全前进，先做 placeholder 继续。**不要编**。
- **用户的描述矛盾**：指出矛盾，让用户选一个方向。
- **任务太大一次吃不下**：拆成steps，先做第一步让用户看，再推进。
- **用户要求的效果技术上很难**：说清技术边界，提供替代方案。

## 总结规则

交付时，summary **极短**：

```markdown
✅ 幻灯片已完成（10张），带Tweaks可切换"夜/日模式"。

注意：
- 第4页的数据是假的，等你提供真数据我替换
- 动画用了CSS transition，不需要JS

下一步建议：先你浏览器打开看一遍，有问题告诉我哪页哪处。
```

不要：
- 罗列每一页的内容
- 重复讲你用了什么技术
- 夸自己设计多好

Caveats + next steps，结束。
