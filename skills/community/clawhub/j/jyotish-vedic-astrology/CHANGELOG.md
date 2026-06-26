# 印度占星 Skill 更新日志

## v4.3.0（2026-05-03）— Dasha 浮点边界修复 + App UI 全面优化

> **触发原因**：多案例交叉验证中发现 Barack Obama 案例 Dasha 0/9 匹配，定位到浮点边界 bug。

### ① Dasha 浮点边界 bug 修复

**问题**：当 Moon 恰好在 Nakshatra 分界线上（如 Taurus 10.0° = Krittika/Rohini 边界），`moonLon % nakSpan` 由于浮点精度返回接近 nakSpan 的值（而非 0），导致 progress ≈ 1.0，将整个 Mahadasha 偏移一个完整周期。

**修复**：在 `computeDasha` 和 `computeDashaWithPratyantar` 中添加 `if(prog > 0.9999) prog = 0`。

**验证**：Barack Obama 修复前 0/9 → 修复后 9/9 匹配。4 案例汇总：Einstein 8/9, Jobs 8/9, Diana 8/9, Obama 9/9。

### ② App UI/UX 全面优化（jyotish-app v4.3.0）

- **暗色模式**：完整支持 `@media(prefers-color-scheme:dark)` + `[data-theme=dark]` + 手动切换按钮，星盘 SVG 颜色同步适配
- **CSS 变量修复**：6 处 `--text-primary`/`--card-bg`/`--border-color` 未定义变量 → 替换为正确的 `--text-heading`/`--bg-card`/`--border-card`
- **CSS 括号错误修复**：行 1741 游离的 `.rect-banner-btn` 规则和多余的 `}` 导致后续规则可能失效
- **北印度盘中心摘要**：新增与南印度盘一致的 Lagna + 月亮星宿 + Dasha + AK/DK 中心信息区
- **i18n 遗漏修复**：Karaka 标签、Transit 表头 8 列、Panchanga 标签、行星名称列 → 全部走 i18n 系统
- **死代码清理**：删除未调用的 `renderYogas()` 旧版函数（28 行）
- **Toast 通知**：4 处 `alert()` 替换为非阻塞式 Toast 组件（error/warning/success 三种样式）
- **主题切换按钮**：输入页和结果页各一个 🌙/☀️ 切换按钮，状态持久化到 localStorage

### 修改文件清单

| 文件 | 变更 |
|------|------|
| `jyotish-app/style.css` | 暗色模式变量 + Toast 样式 + 主题按钮样式 + 修复未定义变量/括号错误 |
| `jyotish-app/main.js` | Toast 系统 + 主题切换 + alert→toast + 删除死代码 + Transit 表头 i18n |
| `jyotish-app/chart-renderer.js` | 动态主题获取 + 北印盘中心摘要 + `THEME` → `_th` 动态切换 |
| `jyotish-app/renderers.js` | Karaka 标签 i18n + 行星名称国际化 + Panchanga 标签 i18n |
| `jyotish-app/index.html` | 主题切换按钮（输入页 + 结果页） |
| `SKILL.md` | 版本 4.2.0 → 4.3.0 |
| `CHANGELOG.md` | 新增 v4.3.0 记录 |

---

## v4.2.0（2026-04-27）— 强制外部验证门控（MEVG）

> **触发原因**：一楠多次强调"不要根据经验和固有认知去判断分析用户的情况，要全网去找针对性的内容，对应的知识点和相似案例分析综合分析反复验证"。v4.1.0 的 Transit Actionable Output 仅覆盖 Transit 预测环节的案例检索，缺少对静态分析、行星尊严判断、Yoga 识别等其他环节的外部验证要求。AI 反复跳过 web_search 验证，仅凭训练记忆输出解读。

### ① 新增 MEVG 强制外部验证门控协议

**问题**：AI 的训练数据中包含大量印度占星知识，但存在流派偏差、断章取义、缺乏具体性、文化偏见等问题。每次分析都仅凭记忆输出，不搜索外部权威来源验证。

**解决方案**：新增 `mandatory-verification-gate-protocol.md`（完整协议），核心措施：

- **三步验证法（V1→V2→V3）**：
  - V1 构建查询：为每个主要解读点生成英文检索词
  - V2 执行检索：web_search 搜索权威来源（L2≥4次≥3来源，L3≥8次≥5来源）
  - V3 交叉验证：对比来源一致性，仲裁分歧
- **权威来源优先级**：经典文本 > 知名占星师 > 专业网站 > 综合博客
- **强制输出格式**：每个分析章节末尾附验证状态表
- **门控通过/失败标准**：≥80% 主要声明有≥2来源→通过；未通过→降级置信度

### ② 工作流新增 3 个门控步骤

**SKILL.md 阶段描述更新**：
- 在强制工作流列表下方新增 v4.2.0 强制门控说明框

**ai-reading-workflow-prompt.md 升级至 v5.0.0**：
- 新增核心原则 #7："不凭记忆"（与"不跳步"同级）
- 新增 Step 3.11 MEVG-静态门控（验证所有静态解读声明）
- 新增 Step 4.10 MEVG-动态门控（验证所有 Transit/Dasha 解读）
- 新增 Step 5.5 MEVG-预测门控（100% 预测必须通过 5 项检查）
- 更新一页纸流程图（标注 3 个 MEVG 门控位置）

### ③ 预测清单新增 3 条 MEVG 强制项

- MEVG-静态门控（Step 3.11）
- MEVG-动态门控（Step 4.10）
- MEVG-预测门控（Step 5.5）

### ④ 执行纪律

- ❌ 解读章节缺少验证状态表 → 判定为未完成
- ❌ 主要声明无来源引用 → 判定为无效声明
- ❌ 整个分析无 web_search → 判定为严重违反流程
- ✅ 唯一豁免：纯数值计算

### 修改文件清单

| 文件 | 变更 |
|------|------|
| `references/mandatory-verification-gate-protocol.md` | ⭐ 新建 |
| `SKILL.md` | 版本 4.0.0→4.2.0 + 新增 MEVG 章节 + 更新预测清单 + 更新参考资料列表 |
| `references/ai-reading-workflow-prompt.md` | 版本 4.0.0→5.0.0 + 新增核心原则 + 3 个门控步骤 + 更新流程图 |
| `CHANGELOG.md` | 新增 v4.2.0 记录 |

---

## v4.1.0（2026-04-27）— Transit Actionable Output 强制升级

> **触发原因**：一楠追问"我是怎么被发现的？展示内容什么时候开始创作？"——发现Skill输出的Transit分析停留在"星盘数据陈述"层，缺少Actionable Output模块；动态预测依赖理论推断，缺乏真实案例支撑。

### ① Transit Actionable Output 强制规范

**问题**：Transit分析后AI只输出星盘数据（如"Jupiter入Cancer"），用户不知道该做什么。

**解决方案**：新增 `Transit Actionable Output 规范`（插入位置：SKILL.md「⚠️ 过境分析强制规范」之前），强制要求：
- 每条Transit预测输出三要素：**时间段**（精确到日/周/月）+ **具体行动类型**（发布内容/跟进联系人/保持在线/推进谈判）+ **置信度**（[A]=已验证/[B]=高概率/[C]=推断）
- 行动基础：必须有真实案例参照，禁止纯理论推断

**案例检索强制触发词**：
- "被发现"、"被赏识"、"被贵人"、"什么时候"、"应期"、"时机"
- "合作"、"破圈"、"突破"、"升职"、"移民"、"搬迁"

### ② Phase5 应期输出强制嵌入案例检索

**问题**：应期预测直接给时间窗口，没有真实案例作为参照，预测质量无法验证。

**解决方案**：阶段五从"五层验证法→精确时间窗口"升级为"五层验证法→精确时间窗口→**Actionable Output行动模块→案例检索**"：
- 动态预测（被发现/合作/应期/事件型）必须执行三步：
  1. 检索同类行星配置真实案例（`celebrity --config ...` 或 `web_search`）
  2. 对比D10/D9信号一致性
  3. 整合输出带案例参照的结论

### ③ 预测清单新增2条强制项

- **Transit Actionable Output**：每条Transit预测必须输出时间段+行动类型+置信度+未验证声明；动态预测必须先检索案例再给结论
- **案例检索**：动态预测强制三步法；禁用未经案例支撑的理论推断

### ④ 阶段四/五版本标注

- 阶段四：`⭐ v4.1.0 Transit行动规范强制执行`
- 阶段五：`⭐ v4.1.0 升级`

### 踩坑经验记录（v4.1.0）

> 当用户追问"具体细节"时，说明Skill输出停留在"数据陈述"层——这是系统性问题，需要在SKILL.md的Phase规范中强制嵌入Actionable Output模块，而非在单次对话中修复。


---

## v4.0.0（2026-04-27）— 质量保障四大升级

> **核心升级**：从"功能堆叠"转向"质量治理"——解决DK摇摆、来源不透明、精度不一致、预测无标注四大痛点

### ① Karaka系统自动识别（Step 0.5 强制检测）

**问题**：DK身份在不同Karaka系统（7星/8星/Sanjay Rath 8星）之间反复摇摆，导致配偶画像不一致。

**解决方案**：在 `ai-reading-workflow-prompt.md` 的入口路由后、阶段二之前，新增**Step 0.5 Karaka系统自动识别**（🔴🔴🔴三级必读区）：
- 三大主流Karaka系统对照表（K.N. Rao 7星/JH 8-Karaka/Sanjay Rath 8星）
- 自动识别规则表（PDF含PiK → JH制/PDF有8无PiK → Sanjay Rath/引擎计算 → 7星默认）
- 常见陷阱与纠正（JH的DK是第7低而非第1低、Sanjay Rath排除Mars作为DK候选）
- 强制输出格式：每份报告开头必须声明Karaka系统+DK+数据来源

### ② 来源标签三级体系（96个references文件全部标注）

**问题**：古典铁律、现代大师教学、Skill原创演绎混在一起，用户无法区分来源可靠性。

**解决方案**：定义六级来源标签体系，批量更新所有references文件：

| 标签 | 含义 | 数量 |
|------|------|------|
| 【古典·千年传承】 | BPHS/Jaimini Sutras/经典注释 | 7 |
| 【传统·现代大师】 | B.V. Raman/K.N. Rao/Sanjay Rath/Marc Boney | 8 |
| 【现代演绎·Skill整合】 | Skill原创/统计归纳/AI工程化 | 20 |
| 【混合·古典+传统+现代】 | 多源混合内容 | 32 |
| 【工具/模板】 | 工作流/模板/桥接文件 | 13 |
| 【案例库】 | 纯案例数据文件 | 12 |

标签格式：`> **来源标签**: 【类别】 — 简述`，插入在每个文件头部的`---`分隔符之前。

同时将已有的6个旧格式标签统一为新标准（badhaka/marc-boney/raman/shasti-hayani/vp-goel/ai-reading-workflow）。

### ③ 统一精度边界声明表

**问题**：不同文件中的精度声明不一致（有的±2天，有的±2-3小时，SSD又承认±6-12小时）。

**解决方案**：在 `ai-reading-workflow-prompt.md` §5.1 新增统一精度边界声明表：

| Dasha层级 | 精度范围 | 强制附注 |
|-----------|---------|---------|
| Maha Dasha (MD) | ±1-3个月 | 大方向趋势 |
| Antar Dasha (AD) | ±2-4周 | 年度能量走向 |
| Pratyantar (PD) | ±2-3天 | 月度活跃区间 |
| Sookshma (SD) | ±1-2天 | 周度参考 |
| Prana SSD | ±6-12小时 | ⚠️非精确时刻，仅供参考 |

所有含时间预测的输出末尾必须附加"精度与诚实声明"段。

### ④ 预测强制[A/B/C]置信度+验证状态标注

**问题**：预测结论缺乏置信度标记和验证状态声明，用户无法判断可靠性。

**解决方案**：在 `ai-reading-workflow-prompt.md` §5.0 新增两维度强制标注：

**置信度三级分类**（引用precision-reading-methodology.md §五）：
- ✅ [A] 已验证（倒推匹配度≥60%）
- ⭐ [B] 强推断（3+独立维度一致，未经验证）
- ⚡ [C] 假设（单一维度，缺多系统支撑）

**验证状态三档声明**：
- [已验证·N/N事件吻合] — 可给相对精确窗口
- [未经验证] — 必须降置信度至少一级，禁用[A]
- [校准异常·需重新评估] — 停止预测

每条预测结论必须包含：结论+置信度+验证状态+依据+精度边界+矛盾说明。

### ⑤ Mangal Dosha两派观点注释

在 `raman-house-judgment-methodology.md` §3.3 补充学派争议注释：
- 传统派（Raman）：Yogakaraka Mars → Dosha**减轻**
- 另一派：Yogakaraka Mars → Dosha**完全豁免**
- Skill默认采用Raman"减轻"说，同时标注"完全豁免"观点
- 一楠星盘实例：Mars@Cancer 12宫（落陷极浅+Neecha Bhanga）→ Mangal Dosha影响极弱

### 文件变更清单

| 文件 | 变更类型 |
|------|---------|
| `ai-reading-workflow-prompt.md` | v3.0→v4.0 重大更新：+Step 0.5 Karaka识别、+§5.0置信度/验证状态标注、+§5.1精度边界表、更新§5.3输出模板 |
| `raman-house-judgment-methodology.md` | +Mangal Dosha两派观点注释（§3.3） |
| `SKILL.md` | v3.13.1→v4.0.0：+新触发词(Karaka识别/DK身份/8-Karaka/来源标签/精度边界/SSD误差/未经验证标注) |
| 96个references文件 | 批量添加来源标签（+6个旧标签格式统一） |
| `dasha-transit-method.md` | +来源标签 |
| `multi-dasha-convergence-protocol.md` | +来源标签 |

### 版本跃迁说明

v3.x系列是"功能堆叠"阶段（从v3.7到v3.13，每次增加新模块/新文件）。v4.0.0标志着进入"质量治理"阶段——不再追求更多功能，而是确保已有功能的可靠性和透明度。这一转变的触发点是Kimi给出的优化方案审计，虽然其62%的问题诊断准确率不够理想，但确实暴露了四个真实痛点。

---

## v3.13.1（2026-04-26）— 用户体验优化 + qin_ruisheng条目补描述 + 速查指南

### qin_ruisheng_system.md 条目补描述

该文件自v3.3已存在于references/目录（754行），但SKILL.md参考列表中仅有"秦瑞生占星体系（华人占星师方法论）"一句话描述，与其他文件的描述质量严重不对齐。

v3.13.1将其扩展为完整内容摘要（恒星黄道vs回归黄道+27星宿+12宫+Kendra-Trikona+9星曜+5类Yoga+Vimshottari四层+四维一体预测+Gochara+8快速判断+12种Kaal Sarpa+金句12条），并更新section计数（4个→5个）。

### 实用速查指南新增

**`references/quick-reference-guide.md`** ⭐ v3.13.1 新增【实用入口·推荐优先阅读】

**用途**：用户提出问题时，快速定位到正确的分析路径和所需文件，不再迷失在96+个参考文件中。

**内容结构**（10大场景+引擎命令速查表）：

| 场景 | 触发条件 |
|------|---------|
| 场景一：全面解盘 | "帮我看盘" / "分析我的星盘" |
| 场景二：婚姻应期 | "什么时候结婚" / "感情应期" |
| 场景三：单项分析 | "事业" / "财运" / "学业" |
| 场景四：PDF星盘 | 用户上传PDF文件 |
| 场景五：无出生时间 | "没有出生时间" / "只有年月日" |
| 场景六：Prashna问事 | 单个具体问题（无出生数据） |
| 场景七：名人查询 | "查一下XXX的星盘" |
| 场景八：Double Transit | 特定行星过境查询 |
| 场景九：深度分析 | 高精度综合分析 |
| 场景十：质量控制 | 所有分析完成后必做 |

每个场景包含：执行顺序 + 所需参考文件 + 引擎命令模板。

### 引擎版本对齐

`scripts/jyotish_engine.py` 头注释版本：v3.7.0 → **v3.7.1**（与SKILL.md记录一致）

### SKILL.md变更

- 版本：v3.13.0 → **v3.13.1**
- 参考文件数：96 → **97**（新增quick-reference-guide.md）
- §1 AI解盘工作流：1个 → **2个**（新增速查指南）
- §16 高级技法与全球方法论：4个 → **5个**（qin_ruisheng_system.md条目扩充）
- qin_ruisheng_system.md #74：从一句话描述扩展为754行完整内容摘要

---

## v3.13.0（2026-04-26）— 文件注册清理 + 单事件问事协议 + 婚姻四技法验证体系

### 核心工作：系统性审计与注册补全

通过全面审计发现3个文件存在于references/目录但未注册到SKILL.md参考列表，通过交叉验证确认均有效后完成注册。

### 新增注册文件（3个）

**`references/single-event-inquiry-protocol.md`** ⭐ Prashna问事·单问题快判
- **用途**：当用户提出单个具体问题（不提供出生数据）时，按十步断卦模板执行Prashna分析
- **核心内容**：输入信息收集表（5字段）+ 阶段一铸造星盘 + 阶段二十步AI执行（征象星对比+Tajika Yoga检查+Sphuta组合+阻碍排查+时间判断）+ 阶段三综合结论格式 + 特殊场景协议（失物/健康/是非判断KP补充）
- **引擎集成**：`python3 scripts/jyotish_engine.py prashna --mode chart` 铸造即时星盘

**`references/marriage-timing-validation-methodology.md`** ⭐ 婚姻应期·技法验证
- **用途**：为婚姻/感情应期分析提供四技法交叉验证框架，基于10案例统计校准置信度
- **核心内容**：
  - 四技法交叉验证：Double Transit + DK木星激活 + UL激活 + Dasha支持
  - 7星系统统计：DK命中率90%，Dasha支持70%，UL激活40%，DT 20%
  - 8星系统统计：DK命中率100%，UL激活60%，DT 40%
  - **关键修正1**：DK Jaimini激活100%命中率存在虚命中（11/12星座被相位）→ 应作必要条件而非充分条件
  - **关键修正2**：出生时间必须转世界时（UT），否则Moon偏移6-8°
  - **关键修正3**：Double Transit应检验7宫/7主/功能DT/UL/DK多个目标组合
  - **关键修正4**：7星/8星双轨并行，不排他——80%案例两系统给出不同DK
- **来源**：10个名人案例验证（奥巴马/克林顿/盖茨/特朗普/朱莉/贝克汉姆/乔丹/梅根/马斯克/凯特王妃）

**`references/marriage-timing-comprehensive-techniques.md`**（补注册）⭐ 婚姻应期·综合技法
- **此前状态**：文件自v3.7.3已存在于references/目录，但SKILL.md参考列表从未注册
- **内容确认**：KN Rao Double Transit精确规则 + VP Goel功能征象星 + Jaimini DK木星过境激活法 + Upapada Lagna完整体系 + Ketu期感情特征 + 木星入庙Cancer 2026影响

### SKILL.md §14 Prashna体系升级

在Prashna问事占星区域新增两个能力区块：

1. **⭐ 单事件问事协议**：当用户提出单个具体问题（无出生数据）时，使用 `single-event-inquiry-protocol.md` 执行标准化十步断卦流程

2. **⭐ 婚姻应期技法交叉验证体系**：当分析婚姻/感情应期时，使用 `marriage-timing-validation-methodology.md` 执行四技法交叉验证，配合 `marriage-timing-comprehensive-techniques.md` 的KP/Rao/Dasha三层确认

### SKILL.md 参考列表编号修正

| 操作 | 文件 | 旧编号 | 新编号 |
|------|------|--------|--------|
| 新增注册 | single-event-inquiry-protocol.md | — | #83 |
| 新增注册 | marriage-timing-validation-methodology.md | — | #84 |
| 补注册 | marriage-timing-comprehensive-techniques.md | — | #85 |
| 顺延修正 | bhrigu-chakra-paddhati.md | #83 | #86 |
| 顺延修正 | high-status-spouse-yoga.md | #84 | #87 |
| 顺延修正 | darakaraka-complete-guide.md | #85 | #88 |
| 顺延修正 | yogi-avayogi-system.md | #86 | #89 |
| 顺延修正 | tithi-lord-relationship-system.md | #87 | #90 |
| 顺延修正 | rashi-tulya-navamsa-root-impulse.md | #88 | #91 |
| 顺延修正 | bhrigu-pada-dasha-marriage-counting.md | #89 | #92 |
| 顺延修正 | pancha-pakshi-nakshatra-systems.md | #90 | #93 |
| 顺延修正 | badhaka-obstacle-planet-guide.md | #91 | #94 |
| 顺延修正 | raman-house-judgment-methodology.md | #92 | #95 |
| 顺延修正 | shasti-hayani-dasha-guide.md | #93 | #93（不变） |
| 总计 | — | 96个 | **99个** |

> 注：原#93 shasti-hayani-dasha-guide.md在BCP章节，与Prashna/婚姻章节的三个新增文件不在同一section，因此编号不变。总文件数=96+3=99。

### CHANGELOG编号对齐说明

CHANGELOG中"v3.8.0新增案例库（13个）→编号58-70"的记录基于v3.8.0的编号体系。v3.10.0引入高地位配偶Yoga等5个新文件后，案例库文件被顺延重编号至#63-70。v3.13.0又引入3个新文件，总编号体系已完全对齐，SKILL.md正文编号为规范引用。

### 触发词优化

在frontmatter触发词中追加：`单事件问事`、`单事件查询`、`一楠星盘`、`婚姻四技法`、`Double Transit`、`Dasha支持`

### SKILL.md变更

- 版本：v3.12.1 → **v3.13.0**
- 参考文件数：96 → **99**（新增3个）
- §14 Prashna区域新增：单事件问事协议能力描述 + 婚姻四技法验证体系描述
- frontmatter触发词追加：单事件问事、单事件查询、一楠星盘、婚姻四技法
- 参考列表：83→99重新编号完毕

---

## v3.12.1（2026-04-26）— 精准解盘方法论集成

### 新增内容

**新增参考文件**（references/目录）：
- **precision-reading-methodology.md** ⭐⭐⭐⭐⭐（#96）

**核心内容**：
基于6位顶级占星师的实践共识，整合出系统化的精准解盘方法论：

1. **六大共识原则**：
   - 功能吉凶因盘而异（V.K. Choudhry Systems' Approach）
   - 单一技法不做结论（Marc Boney / K.N. Rao）
   - 规则前提先查（Marc Boney）
   - 案例验证 > 经典引述（K.N. Rao）
   - 先整体后细节（Hart de Fouw / Rao PACDARES）
   - 先验证过去，再预测未来（Rao核心方法论）

2. **PACDARES本命盘分析框架**（K.N. Rao）：
   - Position → Aspect → Conjunction → Dhana → Arishta → Raja → Exchange → Special Features
   - 8维度系统化分析，作为所有解读的地基

3. **九层复合方法**（L1-L9）：
   - L1 PACDARES → L2 分盘 → **L3 矛盾检查** → L4 Vimshottari → L5 AV+Transit → L6 条件Dasha → L7 Jaimini → L8 其他Jaimini → L9 Tajika
   - **做到L6，平均85%预测成功率**（Rao原话）

4. **L3矛盾检查协议**：
   - 四类矛盾：D1 vs D9、吉Yoga vs 凶相位、DK vs 7宫主、静态 vs 推运
   - 矛盾不回避，记录→解释→降低置信度→如实告知用户

5. **验证驱动分析流程**：
   - 倒推验证协议（4步）：收集已知事件→Dasha映射→评估匹配度→校准偏差
   - 匹配度<60%必须停止预测，先解决校准问题

6. **三级置信度系统**：
   - ✅ [A] 已验证（倒推命中）/ ⭐ [B] 强推断（3+独立维度）/ ⚡ [C] 假设（单一维度）

7. **10条常见教条失误及纠正**

8. **经典文献审慎使用**（Shyamasundara Dasa BPHS考证）：
   - BPHS非原始文本，包含19-20世纪插入
   - 推荐文献优先级：Brihat Jataka > Saravali > Phaladipika > BPHS核心 > Jaimini Sutras

9. **实战五步法**：PACDARES → 分盘+矛盾 → 倒推验证 → 推运L4-L9 → 输出

### SKILL.md 变更
- 版本：v3.12.0 → v3.12.1
- 参考文件数：95 → 96
- 新增触发词：精准解盘、验证驱动、PACDARES、倒推验证、复合方法、教条纠错、案例验证、置信度分级、矛盾检查、先验后推
- 新增"精准解盘方法论"section（核心方法论区域）
- 元能力新增：精准解盘方法论

### 信息来源
- K.N. Rao访谈（Journal of Astrology 2010年7/8月刊）
- V.K. Choudhry：Systems' Approach to Interpreting Horoscopes
- Shyamasundara Dasa："On the Authenticity of the BPHS"
- Marc Boney：Case Studies in Vedic Astrology
- Hart de Fouw & Robert Svoboda：Light on Life
- Sanjay Rath：Bṛhaspati Jyotiṣa课程体系
- Dr. A.K. Tripathi："True Astro Secrets"

---

## v3.12.0（2026-04-25）— 10本PDF书籍知识集成 + Kimi审计报告验证

### 知识来源

基于10本经典印度占星PDF书籍的深度提取与集成：
1. *Ancient Hindu Astrology For Modern Western Astrologer* — James Braha（187页，可提取）
2. *How to Judge a Horoscope Vol 1* (Houses I-VI) — B.V. Raman（310页，可提取）
3. *How to Judge a Horoscope Vol 2* (Houses VII-XII) — B.V. Raman（482页，可提取）
4. *Learn Successful Predictive Techniques of Hindu Astrology* — K.N. Rao（159页，可提取）
5. *Light on Life: An Introduction to the Astrology of India* — Hart de Fouw & Robert Svoboda（461页，可提取）
6. *Predict Effectively through Yogini Dasha* — V.P. Goel（63页，⚠️ 扫描件，无法提取文字）
7. *Predicting through Jaimini Astrology* — V.P. Goel（232页，可提取）
8. *Predicting through Jaimini's Chara Dasha* — K.N. Rao（135页，可提取）
9. *Predicting Through Shasti Hayani Dasha* — V.P. Goel（92页，⚠️ 扫描件，无法提取文字）
10. *Predicting Major Life Events: A Composite Approach* — Marc Boney（465页，可提取）

**PDF提取率**：8/10（2本为扫描件，通过在线源补充关键内容）

### Kimi审计报告验证

收到7项批评的Kimi审计报告，逐条与PDF书籍原文交叉验证：

| # | Kimi批评 | 验证结论 | 证据来源 |
|---|---------|---------|---------|
| 1 | "五系统混合有问题" | ❌ **无效** | Marc Boney全书 dedicate to K.N. Rao，"Composite Approach"即跨系统整合；V.P. Goel p.5："combines the two systems"；K.N. Rao 书中明确使用多系统 |
| 2 | "7/8星Karaka混乱" | ⚠️ **部分有效** | K.N. Rao明确支持7星（"First time in thousands of years showing the use of seven Karakas"）；Skill双轨方案已正确 |
| 3 | "宫位系统冲突" | ❌ **无效** | 所有10本书统一使用Whole Sign（整宫制），Jyotish不存在Placidus/Koch |
| 4 | "现代创新未标注来源" | ⚠️ **部分有效** | 建议对非古典技法标注来源等级 |
| 5 | "Ayanamsa单点问题" | ⚠️ **低优先级** | 全部作者统一使用Lahiri |
| 6 | "缺少Badhaka等模块" | ✅ **有效** | → 已创建 badhaka-obstacle-planet-guide.md |
| 7 | "Ashtottari条件检查自动化" | ✅ **有效** | 引擎级别改进，待后续实现 |

### 新增参考文件（5个）

- **`references/badhaka-obstacle-planet-guide.md`**：Badhaka障碍星系统完整指南
  - **12上升Badhaka Sthana+Badhakesh完整对照表**：Movable→11宫，Fixed→9宫，Dual→7宫
  - **Leo上升分析**：Badhakesh=Mars（9宫Aries主），结合一楠星盘实战
  - **五步分析协议**：确定Badhakesh→分析落宫/相位→检查Badhaka Sthana→评估关系→补救
  - 来源：【古典·BPHS】

- **`references/raman-house-judgment-methodology.md`**：B.V. Raman宫位判断方法论
  - **12上升完整Benefic/Malefic/Yogakaraka表**（B.V. Raman Vol 1 pp.16-18）
  - **六步宫位判断法**：宫主星→Karaka→落宫→相位→合相→综合评估
  - **第七宫婚姻分析六维度**（Vol 2 Ch.XI）
  - **Maraka死亡指示系统**：主Maraka=2宫主+7宫主，次级=Saturn，"生命宫"=3+8宫
  - **Mangal Dosha完整规则**
  - 来源：【古典·B.V. Raman】

- **`references/shasti-hayani-dasha-guide.md`**：Shasti Hayani条件Dasha指南
  - **适用条件**：太阳在1宫（Nakshatra-based条件Dasha）
  - **60年周期**：8行星固定顺序，Jupiter→Sun→Mars→Moon→Mercury→Venus→Saturn→Rahu，各10年
  - **三级Antar结构**：Antar→Pratyantar→Sookshma
  - **与其他条件Dasha对比**（Shodashottari/Dwisaptati Sama/Shastihayani）
  - 来源：V.P. Goel书籍（扫描件）+ AstroNidan在线源

- **`references/marc-boney-marriage-six-step.md`**：Marc Boney婚姻六步法
  - **六步法**：Venus评估→三视角7宫→Navamsa确认→Vimshottari支持→Jaimini DK激活→Double Transit
  - **核心创新**："三视角"7宫评估——从Lagna/Moon/Venus三个参考点看7宫
  - **同居vs正式婚姻区分**：不同征象星组合指向不同关系类型
  - **跨系统验证立场**：Marc Boney整本书 dedicate to K.N. Rao，明确使用Parashari+Jaimini+Transit整合
  - 来源：【现代创新·K.N. Rao学派】

- **`references/vp-goel-jaimini-dasha-systems.md`**：V.P. Goel Jaimini Dasha系统概览
  - **10种Jaimini Dasha系统概览**：Chara/Mandook/Sthira/Narayan/Navamsha/NSD/Trikon/Atmanadi等
  - **实现优先级**：P0（Chara已实现）→P1（Mandook/Narayan/Navamsha）→P2（Sthira/NSD）→P3（Trikon/Atmanadi）
  - **Argala四分之一度阻碍规则**：BPHS原典，星座内4个四分之一度（0-7°30'/7°30'-15°/15°-22°30'/22°30'-30°）决定Virodha有效性
  - **Jaimini星座相位规则**：Movable↔Fixed，Dual↔Dual
  - 来源：【现代·V.P. Goel研究】

### 现有参考文件补充（未改文件内容，仅标注待升级）

- `argala-complete-guide.md`：发现缺少四分之一度阻碍规则（V.P. Goel p.30/BPHS），建议后续升级
- `jaimini-complete-system.md`：缺少K.N. Rao和V.P. Goel书籍引证，建议补充来源标注
- `condition-dasha-complete.md`：缺少Shasti Hayani Dasha条目，建议后续补充
- `marriage-timing-comprehensive-techniques.md`：缺少Marc Boney六步法交叉引用

### 综合审计报告

- **审计报告文件**：`brain/372caffb.../10本PDF书籍知识审计报告.md`
- **10本PDF提取结果**：8本成功提取，2本扫描件（Yogini Dasha/Shasti Hayani Dasha by V.P. Goel）
- **新知识发现**：10项（Badhaka系统/Raman方法论/Shasti Hayani/Argala四分之一度/Marc Boney六步法/三视角/V.P. Goel 10种Dasha/Maraka系统/7星立场确认/跨系统验证）
- **现有文件冲突/错误**：10项（缺Badhaka/缺Raman表/缺四分之一度/缺来源引证等）

### SKILL.md 更新

- 版本 v3.11.0 → **v3.12.0**
- 参考文件总数：90 → **95**（新增5个）
- 新增 §17-§21 五个能力描述（Badhaka/Raman/Shasti Hayani/Marc Boney/V.P. Goel）
- §1 静态分析 新增 Badhaka+Raman 交叉引用
- §2 动态推运 新增 Shasti Hayani+V.P. Goel 交叉引用
- §3 关系占星 新增 Marc Boney 六步法交叉引用
- 触发词新增：Badhaka/障碍星/Badhakesh/宫位判断/Raman/Yogakaraka/每上升吉凶星/Shasti Hayani/60年周期/Marc Boney/婚姻六步法/三视角/V.P. Goel/10种Dasha/Mandook/Narayan/Maraka/死亡指示/生命宫/跨系统验证/多系统整合

---

## v3.11.0（2026-04-25）— 多元技法系统（5篇参考文件）

### 知识来源

基于4篇外部公众号文章（非用户原创）的学习与集成：
1. 「1印度占星」（~30,400字）：Tithi Lord 30历日关系系统 + Yogi/Ava Yogi入门 + 婚姻计数法 + Arudha Lagna关系分析 + Sanyasi组合
2. 「2印度占星」（~17,700字）：Pancha Pakshi五鸟择时术 + Navamsa根源冲动 + Yogi/Ava Yogi Dasha/Transit应用 + 宝石激活
3. 「3印度占星」（~28,800字）：Rashi Tulya Navamsa + Yogi/Ava Yogi综合分析（四因子）+ Nakshatra三计数体系 + Savya/Apasavya
4. 「4印度占星」（~19,600字）：Bhrigu Pada Dasha + Narayana Dasha D9变体

### 新增参考文件（5个）

- **`references/yogi-avayogi-system.md`**：Yogi/Ava Yogi/Duplicate Yogi行星系统完整指南
  - **计算方法**：Yogi点（上升+93°20'）→ Nakshatra主星 → 三行星指派
  - **四大影响因子**：财富领域 / 灵性距离 / 社交圈类型 / 支持者类型
  - **特殊判定**：上升与Yogi同Nakshatra=天生富裕业力；Dasha/Transit激活机制
  - **宝石疗法**：Yogi宝石→推荐；Ava Yogi宝石→严禁
  - **Trump/查尔斯案例** + 与Tithi Lord/Dasha/Navamsa/Argala/AV整合

- **`references/tithi-lord-relationship-system.md`**：Tithi Lord关系影响系统
  - **30 Tithi分配表**（8行星循环，Ketu排除）
  - **8种关系模式**：Sun=家庭支配型 / Moon=善变型 / Mars=热情独居矛盾型 / Mercury=青春智力型 / Jupiter=道德家庭型 / Venus=欲望美感型 / Saturn=延迟成熟型 / Rahu=非传统型
  - **Sanjay Rath"水龙头"理论**：Tithi Lord控制Jala（水元素）=情感流动模式
  - **整合**：Yogi交叉 / Dasha配合 / Navamsa配合 / Arudha Lagna内外分析

- **`references/rashi-tulya-navamsa-root-impulse.md`**：Rashi Tulya Navamsa与根源冲动系统
  - **Rashi Tulya Navamsa**：D1位置投射到D9坐标系，保持星座位置不变
  - **7行星根源冲动完整表**：太阳→自尊激励 / 月亮→快乐来源 / 火星→愤怒触发 / 水星→学习动机 / 木星→智慧方向 / 金星→欲望模式 / 土星→恐惧责任
  - **经典组合**：金星在火星Navamsa=无法满足的性欲 / 金星在土星Navamsa=孤独/同性倾向
  - **Navamsa分类规则**：火象→教育/孩子/名声；水象→不利健康/财富/名声

- **`references/bhrigu-pada-dasha-marriage-counting.md`**：Bhrigu Pada Dasha与婚姻计数法
  - **Bhrigu Pada Dasha**：行星推进法（Progression），不同于BCP固定周期，专用于婚姻时机
  - **Narayana Dasha D9变体**：在D9上应用Narayana Dasha得到婚姻专用时间线
  - **婚姻计数法**（Sanjay Rath秘传）：7宫主在D1的星座(A)→D9的星座(B)，从A数到B=关系数量
  - **Parivartana特殊处理**：行星交换需重新计算
  - **"婚姻"定义**：持续一年以上的认真关系

- **`references/pancha-pakshi-nakshatra-systems.md`**：Pancha Pakshi五鸟择时术+Nakshatra三体系+Savya/Apasavya
  - **Pancha Pakshi**：泰米尔传统择时术（Sri K N Rao推荐），5种鸟×5时段×高/低振动频率
  - **Nakshatra三计数体系**：Ashwinādi（创造/Srishti）/ Krittikādi（维持/Sthiti，Vimshottari）/ Ardrādi（毁灭/Samhāra）
  - **Savya/Apasavya**：27 Nakshatra每3个一组交替顺行/逆行（Vishnu三步法则）
  - **三系统协同**：日常择时/婚姻/创业/疾病场景的应用映射

### SKILL.md 更新
- 版本号：3.10.0 → 3.11.0（frontmatter + 更新记录 + 底部版本三处同步）
- 参考文件计数：85 → 90
- 新增 §16 多元技法系统（5个子节：Yogi系统 / Tithi Lord / RTN根源冲动 / Bhrigu Pada Dasha / Pancha Pakshi）
- 触发词扩展：Yogi / Ava Yogi / Tithi Lord / 根源冲动 / Rashi Tulya Navamsa / Bhrigu Pada Dasha / 婚姻计数 / Pancha Pakshi / 五鸟择时 / Nakshatra计数体系 / Savya/Apasavya 等
- 能力描述扩展：追加 Yogi/Ava Yogi行星系统 / Tithi Lord关系模式 / RTN根源冲动 / Bhrigu Pada Dasha婚姻推进法 / Pancha Pakshi五鸟择时术 / Nakshatra三计数体系 / Savya/Apasavya顺逆星宿

### 知识审计发现
- **P0 全新知识（7项）**：Yogi/Ava Yogi行星系统、Pancha Pakshi五鸟择时术、Rashi Tulya Navamsa、Navamsa Root Impulse根源冲动、Bhrigu Pada Dasha、婚姻计数法、Nakshatra三计数体系
- **P1 需系统化（2项）**：Tithi Lord关系影响、Savya/Apasavya星宿分组
- **P2 已覆盖（1项）**：Sahams敏感点（v3.9.0 prashna-complete-guide.md 已覆盖）→ 无需新增

## v3.10.0（2026-04-25）— BCP自然周期法 + 高地位配偶规则 + DK深度画像扩展

### 知识来源

基于3篇外部公众号文章（非用户原创）的学习与集成：
1. Tajika占星术 + Bhrigu Chakra Paddhati (BCP) 自然周期法（~23,000字）
2. 印度占星Jaimini系统的Darakaraka理解和说明（~19,500字）
3. 高地位配偶与婚后命运积极转变的占星规则与组合（~4,400字）

### 新增参考文件（2个）

- **`references/bhrigu-chakra-paddhati.md`**（~260行）：BCP自然周期法完整指南
  - **9大自然周期**：Moon(0-12)→Mercury(13-24)→Venus(25-36)→Sun(37-48)→Mars(49-60)→Jupiter(61-72)→Saturn(73-84)→Rahu(85-96)→Ketu(97-108)
  - **双轨激活法**：A轨（从上升起算对应宫位）+ B轨（从周期统治星位置起算），双轨交汇=最强激活点
  - **三要素解读法**：宫位→领域 + 宫主星→表现方式 + Karaka→天然征象，三者联动缩窄事件范围
  - **快查表**：年龄→宫位映射、周期主题速查
  - **与Dasha系统的关系**：BCP是自然周期（固定），Dasha是业力周期（因人而异），两者互补

- **`references/high-status-spouse-yoga.md`**（~180行）：高地位配偶Yoga判定规则
  - **3条核心规则**：
    1. 7宫+7宫主力量 > 上升+上升主力量（D1和D9双盘验证）
    2. 7宫主在D9形成Rajyoga
    3. 从7宫起算的Upachaya宫（3/6/10/11）在D1/D9有行星占据
  - **关键区分**：宫位=环境/背景，宫主星=人的实际能力
  - **Upachaya创新视角**：从7宫而非1宫起算Upachaya，男性凶星比吉星更有效（Rajas/Tamas原则）
  - **Sonya Gandhi案例验证**：D1 Cancer Lagna + D9 Aquarius Lagna
  - **整合映射**：与 spouse-multi-layer-methodology.md 的6层分析衔接

### 扩展参考文件（1个）

- **`references/darakaraka-complete-guide.md`** v1.0 → **v1.1**（332→~500行）
  - **⭐ §七 8颗行星DK深度画像**：Sun/Moon/Mars/Mercury/Jupiter/Venus/Saturn/Rahu，每颗5维度（性格特质/关系动态/生活方式/挑战与修行/特殊备注+吉凶相位）
  - **⭐ §八 DK与财富的关系**：5种财富模式（配偶财富支持/共享财务目标/财富来源与增长/伴侣财务态度/逆行DK财富挑战）+ 12宫DK财富速查表

### 配置审计修复

- **SKILL.md版本不一致修复**：frontmatter=3.9.0但body两处仍写3.8.0 → 统一为3.10.0
- **参考文件计数修复**：声明82个实际更多 → 更新为85个（82+2新增+1补注册）
- **darakaraka-complete-guide.md补注册**：该文件自v1.0起存在但从未注册到SKILL.md参考列表

### SKILL.md 更新

- 版本 v3.9.0 → **v3.10.0**
- 新增 §15 BCP自然周期法能力描述（9大周期+双轨激活+三要素解读）
- §3 关系占星 新增：高地位配偶Yoga判定 + darakaraka-complete-guide.md引用
- 参考文件总数：82 → **85**（新增bhrigu-chakra-paddhati.md #83 + high-status-spouse-yoga.md #84 + darakaraka-complete-guide.md #85补注册）
- 触发词新增：BCP、Bhrigu Chakra Paddhati、自然周期、小限法、高地位配偶、Upachaya、DK画像、DK财富
- 版本不一致修复：更新记录行 + 底部版本号统一为v3.10.0

### 知识盲区修复

1. ❌ 不了解BCP系统 → ✅ 9大自然周期+双轨激活+三要素解读完整覆盖
2. ❌ 缺少高地位配偶判定规则 → ✅ 3条核心规则+D1/D9验证+Upachaya创新视角
3. ❌ DK分析停留在12宫位含义 → ✅ 8行星5维度深度画像+DK财富5种模式
4. ❌ darakaraka-complete-guide.md未注册 → ✅ 补注册并扩展至v1.1

### 未修复的已知问题

- `cmd_dasha()` 不使用 `_add_chart_args()`，需手动传 `--moon-lon`（已知设计问题，记录但未改动代码）
- `--birthdate` 仅日期精度，无时/分（full-reading 已有内部绕过，独立 dasha 命令暂未改）
- `--nakshatra` 模式使用近似进度（0.125步长）

---

## v3.9.0（2026-04-25）— Prashna问事占星完整系统

### 新增参考文件（1个）

- **`references/prashna-complete-guide.md`**：Prashna问事占星完整指南（十大核心计算：Arudha Lagna+Trisphuta/Catusphuta/Pancasphuta+Gulika+Prana/Deha/Mrityu Sphuta+35 Sahams+Kunda验证+Chor Graha失物+Mrityu Chakra死亡轮+十步断卦框架+8类问题专题）⭐⭐⭐⭐⭐

### 引擎集成

- 新增 `scripts/prashna.py` 计算引擎
- `jyotish_engine.py` 新增 `prashna` 子命令（支持 chart/arudha/sphutas/sahams/lost-item/life/kunda 模式）
- SKILL.md §14 Prashna 问事占星系统（十步断卦框架+十大核心计算模块+适用场景）

### SKILL.md 更新

- 版本 v3.8.0 → **v3.9.0**
- 参考文件总数：81 → **82**（新增 prashna-complete-guide.md）
- 触发词新增：Prashna问事占星、问事占星、时卦、卜卦占星、问卜、Horary、问事、提问占星、Arudha Lagna、映像上升、Trisphuta、三重合点、Sphuta、Gulika、古利卡、Saham、敏感点、失物查询、寻物、Chor Graha、盗贼星、Kunda验证、Prasna Marga、十步断卦

---

## v3.8.0（2026-04-25）— 深度分析方法论体系：5篇实战经验总结

### 核心升级

将11页PDF完整深度分析实战中积累的方法论和推理技法经验，系统化为5篇独立参考文件，覆盖从排盘到解盘到推运的完整链路。

### 新增参考文件（5个）

- **`references/shadbala-interpretation-methodology.md`**：Shadbala六重力量实战解读方法论（约280行）
  - **五力量组合模式库**：全面型/位置依赖型/关系依赖型/时间敏感型/运动受限型
  - **Avastha联合诊断矩阵**：外强内壮/外强内伤/外弱内壮/外弱内伤四象限
  - **Bhava Bala实战解读**：四维宫位力量矩阵（Shirshodaya/Dig/Drig/总Bala）
  - **Vimsopaka分盘综合评分**：四套权重体系解读阈值表
  - **行星力量综合排名法**：Shadbala→Avastha修正→Vimsopaka修正→Bhava Bala关联→最终排名
  - **快速诊断口诀**

- **`references/multi-dasha-convergence-protocol.md`**：多Dasha收敛协议（约230行）
  - **六系统交叉验证**：Vimshottari+Ashtottari+Yogini+Moola+Narayana+Kalachakra
  - **收敛等级量化**：Level 0-4 概率提升（0%→85%）
  - **五步协议**：目标定义→逐系统提取→交叉对比→收敛量化→Transit确认
  - **PDF数据源提取指南**：JH PDF页面映射+提取要点
  - **收敛冲突处理**：三种冲突场景的处理方法
  - **实战输出模板**：标准化表格格式

- **`references/navamsa-marriage-deep-analysis.md`**：Navamsa婚姻深度分析协议（约300行）
  - **D9婚姻五维分析法**：D9上升/DK位置/Venus/7宫/DK-Lagna合相
  - **Vargottama婚姻意义**：19分盘频率分析+婚姻应用
  - **Pushkara Navamsa婚姻解读**：按元素分组的精确度数+婚姻分析应用
  - **D9婚姻8步旗标算法实操版**：绿旗/黄旗/红旗评分表+实战案例
  - **D9与D1矛盾处理**：核心原则"D9>D1在婚姻分析中"

- **`references/divisional-chart-deep-reading.md`**：分盘深度阅读工作流（约260行）
  - **三级方法论**：Level 1关键分盘速查（5分钟）/Level 2领域专项（15分钟）/Level 3全19分盘（45分钟）
  - **行星频率分析核心技法**：统计行星在19个分盘中的落座频率，≥40%=核心主题
  - **Vargottama检测矩阵**：D1-D9/多分盘/逆Vargottama/唯一Vargottama四种类型
  - **分盘组合阅读模式**：三角验证/生命线追踪/财富链/关系链
  - **Swiss Ephemeris交叉验证**：160验证点+一楠验证10/10 D9匹配

- **`references/deep-analysis-complete-workflow.md`**：综合深度分析完整工作流（约330行）
  - **12模块系统化方法**：D1基础→特殊Lagna→Jaimini Karaka→Shadbala→Avastha→Bhava Bala→Vimsopaka→19分盘→AV→多Dasha收敛→Navamsa婚姻→综合结论
  - **PDF 11页提取最佳实践**：完整页面映射+数据完整性门（P0/P1/P2）
  - **引擎调用流程**：full-reading+varga-full+shadbala+ashtakavarga
  - **报告生成**：12章结构+HTML输出
  - **质量检查清单**：数据准确性+分析完整性+解读质量

### SKILL.md 更新

- 版本 v3.7.4 → **v3.8.0**
- 新增 §12.5 深度分析方法论能力描述
- 参考文件总数：76 → **81**（新增5个深度分析方法论文件）
- 触发词新增：深度解盘、全面分析、星盘深度阅读、频率分析、收敛验证、婚姻深层分析、配偶画像、综合深度分析
- 更新记录行更新至v3.8.0

### 方法论核心价值

这5篇文件的核心价值在于将"经验"转化为"可复用方法"：

1. **Shadbala不再是数字游戏**——五力量组合模式让AI看到"行星的工作模式"而非仅看总分排名
2. **多Dasha收敛从3系统升级到6系统**——收敛概率从~65%提升到~85%+，且提供了PDF直接提取的路径
3. **Navamsa婚姻分析有了标准化8步旗标**——不再是"凭感觉判断D9好坏"，而是绿/黄/旗量化评分
4. **行星频率分析是新技法**——统计行星在19个分盘中的落座频率，识别"核心主题"和"锚点行星"
5. **12模块工作流是"解盘SOP"**——从零散分析到系统化流程，每次解盘都有标准化的模块和检查清单

## v3.7.4（2026-04-25）— P0: Ayanamsa模式修复 + 度数精度修正

### 核心修复

- **P0 #4**：`jyotish_engine.py` — **从未设置Lahiri Ayanamsa模式**
  - 根因：`import swisseph` 后没有调用 `swe.set_sid_mode(swe.SIDM_LAHIRI)`
  - Swiss Ephemeris默认使用非Lahiri模式，导致所有恒星黄道度数偏差约**0.88°**
  - 修复：在import后立即调用 `swe.set_sid_mode(swe.SIDM_LAHIRI)`
  - 影响：所有行星度数、Karaka度数、Transit匹配精度、Pushkara判断等均受影响
  - **Karaka排序不受影响**（排序顺序相同，但度数精度显著提升）

### 一楠星盘修正前后度数对比（1993-04-17 14:45 UTC+8）

| 行星 | v3.7.3b（非Lahiri） | v3.7.4（Lahiri） | PDF数据 | 偏差修正 |
|------|-------------------|-----------------|---------|---------|
| Mars | Cancer 0.43° | Cancer **1.32°** | 1°19'≈1.33° | +0.89° → ✅ |
| Sun | Aries 2.62° | Aries **3.51°** | 3°31'≈3.52° | +0.89° → ✅ |
| Jupiter | Virgo 12.94° | Virgo **13.82°** | — | +0.88° |
| Venus | Pisces 9.66° | Pisces **10.54°** | — | +0.88° |
| Moon | Aquarius 10.89° | Aquarius **11.78°** | — | +0.89° |
| Mercury | Pisces 7.65° | Pisces **8.53°** | — | +0.88° |
| Saturn | Aquarius 3.40° | Aquarius **4.29°** | — | +0.89° |
| Rahu | Scorpio 20.15° | Scorpio **21.03°** | — | +0.88° |

### 参考文档同步更新

- `marriage-timing-validation-methodology.md`：一楠对比表AK/DK度数修正为Lahiri精确值
- `darakaraka-complete-guide.md`：Sun入庙→入旺术语修正

### Karaka验证（v3.7.4 Lahiri修正后）

| 角色 | 7星 | 8星(S.Rath) | 度数 | PDF匹配 |
|------|-----|-------------|------|---------|
| AK | Jupiter | Jupiter | 13.82° | ✅ |
| DK | **Mars** | **Sun** | 1.32°/3.51° | ✅ Mars |

---

## v3.7.3b（2026-04-25）— Python引擎P0 Bug修复 + 参考文档4处数据修正

### Python计算引擎修复（scripts/）

- **P0 #1**：`jyotish_engine.py` — Chara Karaka 计算收到 0-360 完整经度而非 0-30 星座内度数
  - 新增 `planet_degs` dict（取 `degree_in_sign`），Karaka 计算用 0-30 度数，Navamsa/Chara Dasha 继续用完整经度
  - 影响：所有 Karaka 排名在修复前都是错误的（按黄道位置排序而非星座内度数）
- **P0 #2**：`jyotish_engine.py` — DK 提取路径 `ck7.get('DK', {}).get('planet', 'Moon')` 永远 fallback 到 Moon
  - 改为 `ck7['karaka_table']['Darakaraka']['planet']` 直接从结构化数据提取
  - 影响：Karakamsha 计算一直基于 Moon D9 而非 DK D9
- **P1**：`jaimini.py` — Rahu 逆行边界 `(30 - deg) % 30` 当 deg=0 时得到 0 而非 30
  - 改为 `30.0 - deg`（不取模，保留边界值用于排序）
- **术语修正**：status 标签 "入庙(Exalted)" → "入旺(Exalted)"（入庙=Own Sign，入旺=Exalted）

### 参考文档修正（references/）

1. `vimshottari_dasha_guide.md`：15° Aries 星宿边界错误（Ashwini → Bharani），补边界说明
2. `planetary-dignity-complete-reference.md`：水星逆行燃烧度数 12° → 8°（Parashari 标准）
3. `marriage-timing-comprehensive-techniques.md`：UL 计算公式重写，从混淆的模运算改为清晰的星座索引推导
4. `planets.md`：燃烧表补充逆行变体注释

### 验证（v3.7.3b，仍使用非Lahiri Ayanamsa）

一楠星盘修复前后对比（注意：此版本度数仍有~0.88°偏差，已在v3.7.4修正）：

| Karaka | 修复前(0-360排序) | 修复后(degree_in_sign) | PDF |
|--------|-------------------|----------------------|-----|
| AK | Venus(339.66°)❌ | Jupiter(12.94°)✅ | Jupiter |
| DK 7星 | Sun(2.62°)❌ | Mars(0.43°)✅ | Mars |
| DK 8星 | Sun(2.62°)✅ | Sun(2.62°)✅ | Sun |

### 其他更新

- `darakaraka-complete-guide.md`：三系统DK判定更新
- `marriage-timing-validation-methodology.md`：双轨验证数据更新

---

## v3.7.3（2026-04-25）— 行星尊严与度数完整参考手册

### 新增参考文件（1个）

- **`references/planetary-dignity-complete-reference.md`**：行星尊严与度数完整参考手册（约500行）
  - **精确旺衰度数表**：7大行星入庙/落陷精确度数 + 渐变效应说明
  - **Moolatrikona区间**：7大行星的原始三方度数范围
  - **行星友敌关系**：完整的五级友敌关系表
  - **行星生命阶段（Avastha）**：奇数/偶数星座的度数-阶段对照表（婴儿/青年/成年/老年/衰退）
  - **Sandhi交界点**：0°和29°的不稳定性规则
  - **燃烧阈值表**：6大行星精确燃烧度数（含逆行变体） + 燃烧减轻因素
  - **Neecha Bhanga落陷取消**：5大取消条件 + Parasara三法（逆行最强！） + Dusthana宫主特殊规则 + Neecha Bhanga Raja Yoga进阶条件
  - **Sect昼夜区分完整规则**：判定方法/两大阵营/各行星日夜盘角色变化/对配偶分析的影响/最强最弱公式
  - **丈夫征象星论证**：木星vs火星的古典论证 + 多层分析权重分配建议
  - **Pushkara Navamsha**：按元素分组的精确度数范围 + Pushkara Bhaga极致恩典度数
  - **Vargottama**：各行星Vargottama的婚姻意义 + Gandanta例外
  - **DK完整8步分析协议**：从计算到合盘验证的完整流程
  - **D9婚姻8步旗标算法**：Rao金星测试 + 绿/黄/红旗系统 + 最终评分解读
  - 来源：PocketPandit / Celesian / Parasara Jyotish (P.V.R. Narasimha Rao) / StarMeet / Vedicmarga / omai.app / Jothishi

### SKILL.md 更新

- 版本 v3.7.2 → **v3.7.3**
- 关系占星参考文件：2 → **3**
- 参考文件总数：75 → **76**（注：编号48新增，后续48→75全部重编为49→76，但旧编号#47仍为配偶方法论）
- 触发词新增：旺衰度数、行星燃烧、落陷取消、Neecha Bhanga、Sect昼夜、Pushkara、Vargottama、行星尊严、Moolatrikona、行星生命阶段、Avastha

### 知识盲区修复

此版本修复了此前分析中暴露的多个知识盲区：
1. ❌ "女命看木星"单一判据 → ✅ 多层分析+昼夜区分
2. ❌ 度数未精确到旺衰 → ✅ 精确度数+渐变效应+距离计算
3. ❌ 不了解行星生命阶段 → ✅ Avastha完整度数表
4. ❌ 燃烧影响未量化 → ✅ 6星阈值+减轻因素
5. ❌ 落陷取消条件不完整 → ✅ 5条件+Parasara三法
6. ❌ Sect对配偶分析的影响不清楚 → ✅ 完整Sect规则+对金/木/土/火的影响
7. ❌ 不了解Pushkara/Vargottama → ✅ 精确度数+婚姻意义

## v3.7.2（2026-04-25）— 配偶多层综合分析方法论

### 新增参考文件（1个）

- **`references/spouse-multi-layer-methodology.md`**：配偶多层综合分析方法论 v1.0
  - **6层交叉确认法**：DK（Jaimini，性别中立）+ 7宫主（婚姻运作）+ 金星（天然征象）+ 木星/月亮（传统Kalatra Karaka）+ 昼夜区分法（古典）+ Rahu辅助（8-Karaka DK）
  - **标准六步分析流程**：确定DK→分析7宫主→分析金星→传统征象+昼夜区分→辅助征象→综合交叉确认
  - **置信度评估标准**：4层确认=75%，5层以上=80%+
  - **Dasha时机判断**：三重共振法（Vimshottari + Chara Dasha + Transit）
  - **非传统关系适配**：同性/跨文化关系的征象星重映射
  - **常见误判纠正**：禁止"男命金星女命木星"单一判据
  - 来源：AstrologyForums / MysteryLores / 古典昼夜区分法（BPHS）+ Jaimini Sutras

### SKILL.md 更新

- 版本 v3.7.1 → **v3.7.2**
- 关系占星部分新增"配偶多层综合分析"能力描述
- 参考文件总数：74 → **75**
- 触发词新增：配偶分析、配偶星、配偶征象、婚姻分析、配偶画像、DK配偶星、多层配偶、昼夜区分

### 方法论核心原则

1. **DK描述"配偶是谁"**——性别中立，只看度数
2. **7宫主描述"婚姻怎么运作"**——不受性别影响
3. **金星描述"关系的品质"**——所有人的天然征象
4. **传统征象+昼夜区分是补充参考**——不是唯一判据
5. **多层交叉确认 > 单一判据**——至少4层确认才达到75%置信度

## v3.7.1（2026-04-25）— full-reading全自动综合解盘 + 三路径路由

### 引擎升级
- `scripts/jyotish_engine.py` v3.7.0 → **v3.7.1**
- 新增 `full-reading` 子命令：一条命令串起13个计算模块（chart/dasha/yoga/varga-full/aspects/jaimini/nakshatra-adv/argala/tajika/shadbala/ashtakavarga/validation/audit）
- 测试结果：12模块全部计算成功，0错误，耗时0.02秒

### 工作流升级
- `references/ai-reading-workflow-prompt.md` v1.0 → v3.0
- 新增三条入口路径路由：
  - **路径A**：精准出生信息 → `full-reading` 全自动计算
  - **路径B**：PDF/文字星盘 → 提取文档数据直接推算
  - **路径C**：时间不明确 → 互动式出生时间矫正 → 确认后走路径A

### SKILL.md 更新
- 版本 v3.7.0 → v3.7.1
- 引擎子命令表更新：21 → 22（新增 full-reading）
- 工作流部分重写为三路径路由结构

## v3.7.0（2026-04-25）— 7大新模块：BPHS十六分盘+精确相位+Jaimini+高级Nakshatra+Argala+Tajika+合盘

### 新增模块（7个）

- **`scripts/varga.py`**：BPHS Shodasavarga十六分盘完整计算
  - 支持全部16个分盘：D2/D3/D4/D7/D9/D10/D12/D16/D20/D24/D27/D30/D40/D45/D60
  - 每个分盘输出精确度数（非仅星座名）
  - D30 Trimsamsa 特殊不等宽映射
  - D9 含 Jaimini 分析（7宫/Venus/Jupiter/尊严状态）
  - D60 含业力分析（角宫吉凶星分布）

- **`scripts/aspects.py`**：度数精确相位系统（Drishti）
  - 标准7宫对冲 + 火星4/7/8 + 木星5/7/9 + 土星3/7/10
  - Orb分类：tight(≤3°) / moderate(≤6°) / loose(≤10°)
  - 计算每个相位的入相位/出相位状态
  - 合相精度分析

- **`scripts/jaimini.py`**：Jaimini系统完整实现
  - `calc_chara_karaka_7()`：7行星 Chara Karaka（AK→DK）
  - `calc_chara_karaka_8()`：8行星 Chara Karaka（含Rahu逆行度数处理）
  - `calc_chara_dasha()`：星座大运（基于上升奇偶性决定方向）
  - `calc_karakamsha()`：灵魂方向分析（DK的D9位置解读）

- **`scripts/nakshatra_advanced.py`**：高级Nakshatra分析
  - 精确Nakshatra定位（名称/Pada/度数/Gana/元素）
  - `calc_tara_bala()`：9循环Tara关系分析
  - `calc_sub_lord()`：KP系统 Sub-Lord 计算
  - `nakshatra_compatibility()`：Tara+元素+Gana综合兼容性

- **`scripts/argala.py`**：Argala门闩系统
  - 主Argala：2/4/11宫 → 财富/幸福/收益
  - 副Argala：5/8宫 → 权力/转化
  - Virodha（阻断）：12→2, 10→4, 3→11, 9→5, 2→8
  - 净评分计算和吉凶判定

- **`scripts/tajika.py`**：Tajika/Varshaphala年运盘
  - `calc_muntha()`：年度上升进展
  - `calc_year_lord()`：年度守护星 + 辅助星（2/5/9/11宫主）
  - `calc_mudda_dasha()`：12个月比例大运
  - `calc_tri_pataka()`：三旗系统评估

- **`scripts/synastry.py`**：合盘分析系统
  - Ashta Koota 36分制（8维度：Varna/Vashya/Tara/Yoni/Graha Maitri/Gana/Bhakuta/Nadi）
  - Mangal Dosha 检查（火星在1/2/4/7/8/12宫）
  - Papasamya 凶星抵消度评估
  - Dasha时间线兼容性分析
  - 自动生成化解建议

### 引擎升级（jyotish_engine.py）

- 版本 v3.6.0 → **v3.7.0**
- 新增7个CLI子命令：`varga-full` / `aspects` / `jaimini` / `nakshatra-adv` / `argala` / `tajika` / `synastry`
- 总子命令数：14 → **21**
- 所有新模块通过一楠星盘验证（1993-04-17 14:45）

### 验证结果

| 模块 | 子命令 | 一楠星盘验证 | 关键输出 |
|------|--------|-------------|---------|
| varga | varga-full | ✅ | D9 Navamsa 精确度数+尊严 |
| aspects | aspects | ✅ | 6个精确相位（Moon-Saturn合相等）|
| jaimini | jaimini | ✅ | AK=Venus, DK=Mars, Chara Dasha序列 |
| nakshatra | nakshatra-adv | ✅ | 9行星Tara Bala, Sub-Lord |
| argala | argala | ✅ | 9行星门闩分析 |
| tajika | tajika | ✅ | 33岁 Muntha=金牛座, YearLord=Venus |
| synastry | synastry | ✅ | Ashta Koota 26/36 (72.2%) |

## v3.6.0（2026-04-24）— CNWU16二次借鉴：report_builder + R2b列校验 + P3/P8/冲突仲裁

### 新增文件
- **`scripts/report_builder.py`**：MD→HTML报告生成器（羊皮纸主题）
  - 基于 CNWU16/vedic-astro-skills 的 report_builder.py 改编适配
  - 18项章节注册表，自动扫描多种 MD 命名模式
  - 羊皮纸CSS + 封面 + 目录 + A4打印优化
  - 中英文双语支持
  - 可通过 engine `report` 子命令调用
  - 浏览器打开后 Ctrl+P → Save as PDF

### 验证模块升级
- **`scripts/validate.py`**：新增 R2b BAV列→SAV列校验
  - 每个星座的7行星BAV bindus列向量之和 = 该星座SAV分数
  - 交叉验证行总和(R2)和列总和的一致性

### 审计管线升级（jyotish_engine.py cmd_audit）
- **P3 仓库耦合**（Warehouse Coupling）：
  - 双宫掌管=货物捆绑分析
  - 识别同时掌管两个宫位的行星（如水星同时掌管双子宫和处女宫）
  - 评估捆绑质量：凶吉混合/压力型/吉庆型/消耗型/中性
- **P8 年龄状态**（Age Status）：
  - 基于行星在星座中的度数区间判定生命周期
  - 婴幼(0-10°)=辅助型，青壮(10-20°)=主动型，老年(20-30°)=自动执行型
- **冲突仲裁3条规则**（Conflict Arbitration）：
  - 规则1: P1清理者+P7入旺 = "带毒高价值资产"（禁止说逢凶化吉）
  - 规则2: P5凶宫+BAV高 = "乱世出英雄"
  - 规则3: P1吉+P2受损 = "空有雄心无着力点"

### 子命令升级
- **新增 `report`** 子命令：调用 report_builder.py 生成 HTML 报告
  - 用法: `python3 jyotish_engine.py report <folder> --name "名字" --lagna "上升" --lang cn`
- 总子命令数：11 → 14

## v3.5.0（2026-04-24）— BPHS完整表校准 + R1-R10验证 + P1-P12审计 + 验前事
- **重写 `scripts/ashtakavarga.py`** v1.0 → v2.0：
  - 从简化 BAV_BASE + EXTRA_BINDHU（SAV=94❌）升级为完整 BPHS 8×8 贡献矩阵
  - 每颗行星的 BAV 从所有 8 个来源（7行星+Lagna）获得贡献，非仅自贡献
  - BPHS 校正：月亮 BAV 木星贡献去12宫→49，金星 BAV 水星贡献加12宫→52
  - SAV 总和 = 337 ✅（7行星 BAV 之和），含 Lagna 完整总分 = 386
  - 两组出生数据端到端验证通过（一楠+奥巴马）
- **新增 `scripts/validate.py`**：R1-R10 数学验证模块
  - R1: SAV 总和 = 337
  - R2: 各 BAV 行常数校验（Sun=48, Moon=49, ...）
  - R3: 水星延伸角 ≤ 28°
  - R4: 金星延伸角 ≤ 47°
  - R5: Rahu-Ketu 严格 180° 对冲
  - R6: 逆行合法性（太阳/月亮不逆行，Rahu/Ketu永远逆行）
  - R7: Dasha 大运年限链总和 = 120 年
  - R8: 行星完整性（7行星 + Rahu + Ketu + Lagna）
  - R9: 星座度数范围 [0, 30)
  - R10: 宫位连续性（1-12宫无断点）
- **升级 `scripts/jyotish_engine.py`** v3.4.0 → v3.5.0：
  - 11 → 13 个子命令（新增 validate/audit）
  - `chart --validate`：星盘计算附加 R1-R10 验证
  - `validate` 子命令：独立运行 R1-R10 校验
  - `audit` 子命令：P1-P12 行星审计管线（Identity/Health/Resource SAV/Road Condition/Exit SAV/Dignity/Shadbala/Aspects/Nakshatra/Yogas）
  - `predict --past-verify`：验前事模式（推断2-4个高信号历史时段，避免冷读效应）
- **来源**：CNWU16/vedic-astro-skills 仓库分析 + ZODIAQ BPHS 完整表

## v3.4.0（2026-04-24）— 高级计算引擎 + Hermes集成 + EventPredictionModel
- **新增 `scripts/shadbala.py`**：Shadbala六重力量计算模块
  - 完整实现Parashara系统六种Bala：Sthana（位置）、Dig（方向）、Kala（时间）、Chesta（运动）、Naisargika（天然）、Drik（相位）
  - 输出每颗行星的六维得分、总Virupas/Rupas、Ishta Bala百分比、强度等级（极强/强/充足/略弱/弱/极弱）
  - 行星力量排名
  - 端到端验证：一楠星盘 Sun 6.73 Rupas（强）、Moon 5.45 Rupas（略弱）
- **新增 `scripts/ashtakavarga.py`**：Ashtakavarga八分法计算模块
  - BAV（Bhinna Ashtakavarga）8源独立贡献表
  - SAV（Sarva Ashtakavarga）聚合评分 + 吉凶评估（极吉/吉利/中等/挑战）
  - Shodhya Pinda简化计算
  - ⚠️ 已知限制：SAV总分未达标准337（BAV_BASE表为简化版，需后续校准为完整Parashara表）
- **新增 `scripts/hermes_memory_core.py` + `scripts/hermes_bridge.py`**：Hermes Agent中间件
  - 零外部依赖（纯Python stdlib: sqlite3, json, os, re, datetime, hashlib）
  - FTS5全文搜索 + 6张SQLite表
  - 记忆存储/检索/上下文构建
- **新增 `scripts/event_prediction_model.py`**：事件预测规则引擎
  - 替代LAM深度学习模型（原0.17%准确率）
  - 三层验证法：静态星盘征象 + Dasha激活 + Transit触发
  - 覆盖婚姻/职业/财富/健康/教育/子女/旅行/灵性8大领域
  - Prediction dataclass：概率评分 + 风险等级 + 时机 + 关键因素 + 建议
- **升级 `scripts/jyotish_engine.py`** v3.3.1 → v3.4.0：
  - 8 → 11个子命令（新增 shadbala/ashtakavarga/memory）
  - 提取 `compute_chart_data()` 公共函数（chart/shadbala/ashtakavarga共用）
  - `predict` 子命令增强：优先使用 EventPredictionModel，降级到简化版
  - `memory` 子命令：store/search/context/stats 四种操作
  - `_add_chart_args()` 公共参数函数消除CLI定义重复
  - 行星数据增加 `speed` 字段（Shadbala Chesta Bala需要）
- **SKILL.md v3.4.0**：版本号+触发词（Shadbala/六重力量/Ashtakavarga/八分法/事件预测/记忆系统）+11子命令表+工作流增加步骤4-5/8/10

## v3.3.1（2026-04-24）— 计算引擎集成
- **新增 `scripts/jyotish_engine.py`**：印度占星统一计算引擎入口
  - 基于 Swiss Ephemeris 天文计算库（Lahiri Ayanamsa 恒星黄道标准）
  - 8大子命令：chart（星盘计算）、dasha（大运时间线）、yoga（格局识别）、predict（三层验证法）、varga（分盘D9/D10）、celebrity（名人案例查询）、db-stats（数据库统计）、transit（过境查询）
  - 自动连接外部数据源：验证数据库（15,840条）、名人CSV（15,807条）、过境配置（2026-2028）
  - 完成端到端验证：一楠星盘上升狮子座（11.66° vs PDF 12.63°）、D9上升巨蟹座（与PDF一致）
- **SKILL.md v3.3.1**：新增 §13 计算引擎集成说明 + 触发词增加（算星盘/排盘/计算星盘/查名人）
- **已知限制**：LAM深度学习模型（75.84MB）和 Hermes Agent 中间件未集成（超出 CLI 脚本能力范围）

## v3.2.0（2026-04-24）— Argala+AI工作流+Dasa Convergence实操化
- **新增 `argala-complete-guide.md`**：Argala行星干预体系完整指南
  - 四类型Argala（主Argala 2/4/11宫 + 次Argala 5/8宫 + Virodha反干预 + 特殊规则）
  - 12宫位完整Argala矩阵（主Argala + Virodha对照）
  - 10核心领域Argala分析模板（婚姻/事业/财富/子女/健康等）
  - Argala链追踪高级技法
  - PAC-DARES整合位置
- **新增 `ai-reading-workflow-prompt.md`**：AI解盘工作流Prompt工程
  - 7阶段完整执行引擎（PDF提取→意图路由→静态分析10步→动态推运7步→应期输出→补救→现代措辞包装）
  - 每个阶段的严格输出模板
  - 质量门Pass/Limited/Fail规则
  - 完整工作流一页纸速查
- **升级 `dasa-convergence-methodology.md` v2.0**：
  - 新增§〇 JH PDF数据源对照表（9大Dasha系统的PDF可提取性一目了然）
  - 新增§七 轻量Convergence三系统法（Vimsottari+Yogini+Chara，无需外部工具）
  - Yogini Dasha完整手工推算表（8位女神+年数+Nakshatra分组+定位公式）
  - Chara Dasha简化推算法（方向判断+Rashi Drishti速查）
  - 轻量Convergence实战模板（标准表格格式）
  - 一楠案例Yogini推算实战验证（Ulka周期=Venus统治=女命恋爱星确认）
- **SKILL.md v3.2.0**：新增2个参考文件注册（66文件总数）+Argala能力描述+AI工作流描述+预测清单增加Argala检查项和Dasa Convergence轻量法+触发词增加Argala/Yogini/Chara Dasha/AI解盘

## v3.1.0（2026-04-24）— 多Dasa收敛+技法补齐+案例库整合
- **新增 `dasa-convergence-methodology.md`**：Dasa Convergence多系统大运交叉验证方法论
  - 9大Dasha系统独立性对照表（Vimsottari/Yogini/Kalachakra/Sudasa/Chara/Narayana/Nadi/Ashtottari/Shodashottari）
  - Convergence五步法：目标领域→提取Dasha→逐系统检查→寻找重叠→Transit确认
  - Convergence等级量化：Level 0-3 概率提升公式
  - 一楠实战案例（Vimsottari+Yogini+Sudasa三系统收敛2027.3）
- **新增 `navatara-kantaka-shani-guide.md`**：双技法合并文件
  - Navatara九星链分析：27宿三组分组法+行星分布解读+一楠实战
  - Kantaka Shani刺土星：四敏感位置（1/4/8/10宫）+严重程度分级+缓解因素+一楠2025-2032 Kantaka预测
- **整合 `famous-case-library.md` v2.0**：
  - 从"1个案例"升级为"24个案例统一入口"
  - 分级索引：A级（AA级验证12个）、B级（1个，梦露⚠️）、C级（比对级11个）
  - 6大核心验证结论（100%支持率）
- **技法覆盖率提升**：58%→83%→补齐后约88%（M19 Navatara+M22 Kantaka Shani已覆盖）
- **SKILL.md v3.1.0**：新增2个参考文件注册（63文件总数）+Dasa Convergence能力描述+版本号更新

## v3.0.0（2026-04-24）— 管线重写：PDF→解盘→应期全链路
- **核心定位重定义**：Skill使命明确为"PDF输入→严谨解盘→精确推运应期输出"
- **重写 `pdf-chart-reading-guide.md` v3.0**（从v1.0升级）：
  - 补全9个P0数据断层：AL/UL/HL/GL特殊Lagna、Jaimini七Karakas、Shadbala六力量、Ashtakavarga BAV/SAV、Yoga清单、逆行/燃烧/战争标记、行星Drishti相位
  - 精确11页JH PDF页面映射
  - 数据完整性门（Quality Gate）：P0数据缺失时禁止完整分析
  - 交叉校验规则：D1 NK↔D9、SAV=337、Moon NK↔Dasha起始
  - 完整JSON Schema覆盖全量数据
  - 管线桥接：提取字段→分析方法→参考文件完整映射
- **升级 `timing-prediction-template.md` v2.0**（从v1.0升级）：
  - 五层验证法：本命征象→Dasha激活（五级Maha→Prana）→Transit触发（四参考点+Double Transit）→Jaimini+KP交叉确认→Varshaphala年运盘确认
  - 应期精度：主窗口（月级）+次窗口（周级）+关键触发日
  - 确认/延迟/取消信号系统
  - 五大事件专属应期公式（婚姻/事业/财富/子女/健康）
- **新增 `data-bridge-mapping.md`**：PDF提取字段→方法论需求全量对照表+外部数据依赖处理
- **SKILL.md v3.0.0**：加入PDF-first强制工作流+核心定位说明+新文件注册

## v2.1.2（2026-04-23）— 瘦身+质量修复
- 删除空占位符 `api_reference.md`、`example_asset.txt`
- 修复4个死链引用
- SKILL.md瘦身130+行：更新记录移至CHANGELOG.md

## v2.1.1（2026-04-23）— 资料审计修复
- 删除空占位符 `api_reference.md`、`example_asset.txt`
- 修复4个死链引用：planetary-configurations→planets.md、yoga-patterns→yoga_list.md、nakshatra-guide→nakshatra_deities.md、birth-time-rectification(基础)→birth-time-rectification-cases.md
- 补注册26个遗漏文件，修复4处编号重复
- 按逻辑重组为11个分类，60个文件全部添加引用路径
- 扩充 `kp-astrology-complete-system.md` v2.0：从4.5KB扩充至完整体系
- SKILL.md瘦身：更新记录移至本文件，精简核心优势列表

## v2.1.0（2026-04-23）— Yoga Timing + 静态解读最后一环
- 新增 `yoga-phala-timing-guide.md`：五大方法预测Yoga结果时机
- 新增 `retrograde-combustion-war-guide.md`：逆行/燃烧/行星战争深度指南
- 预测清单升级：加入逆行/燃烧/战争检查+Yoga Phala Timing步骤

## v2.0.0（2026-04-23）— 五大核心技法完整化
- 新增 `ketu-dual-nature-guide.md`：Ketu双重属性框架
- 新增 `shadbala-complete-methodology.md`：六种力量完整计算
- 新增 `tajika-yoga-complete-guide.md`：10种Tajika Yoga完整审计
- 新增 `pratyantar-calculation-guide.md`：Pratyantar精确计算
- 升级 `ashtakavarga-complete-system.md` v2.0

## v1.9.0（2026-04-23）— 多参考点过境分析强制规范
- 新增 `transit-multi-reference-guide.md`
- 修正：Chandra Lagna提升为强制基准
- 根因：实际分析中遗漏Chandra Lagna视角导致预测偏差

## v1.8.0 及更早（2026-04-20 ~ 2026-04-23）
- 新增过境综合实战、关系占星、Varshaphala年运盘、综合解盘工作流、27 Nakshatra中文速查
- 新增Jaimini完整体系、KP占星体系、补救措施体系、Ashtakavarga体系
- 新增常见误判纠错、现代措辞解读、PDF星盘读取、自动出生时间矫正
- 新增名人案例库、九层分盘体系、三系统协同分析、行星力量速查
