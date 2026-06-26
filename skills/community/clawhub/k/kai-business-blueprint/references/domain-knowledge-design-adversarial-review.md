# 对抗性评审报告：Domain-Knowledge实体扩展设计

**评审日期**: 2026-04-28
**评审者**: Claude Code（对抗性视角）
**目标**: 系统性识别设计缺陷、矛盾、遗漏、风险，确保设计质量

---

## 一、核心假设脆弱性分析

### 问题1：AI自动判断意图的可靠性假设

**设计假设**：
```
用户需求包含"know-how"、"领域知识"、"策略"、"痛点" → blueprintType = "domain-knowledge"
```

**对抗性质疑**：
- 用户输入模糊时，AI判断会出错吗？
- 例如：用户说"优化ROI策略" → "策略"关键词触发domain-knowledge，但用户实际想看的是系统架构（优化ROI的系统设计）
- 关键词匹配过于简单，缺乏上下文理解

**发现缺陷**：
- ❌ AI判断逻辑过于简单（关键词匹配），未考虑用户意图的语义理解
- ❌ 未定义fallback机制：AI判断错误时，用户如何纠正blueprintType？

**建议改进**：
- 新增判断优先级：用户明确指定蓝图类型 > 关键词频率分析 > 默认值
- 允许用户在JSON meta中手动设置blueprintType覆盖AI判断

---

### 问题2："强核心+弱扩展"的可行性假设

**设计假设**：
```
validator只校验核心字段（id/name/entityType），扩展字段直接放行
```

**对抗性质疑**：
- 扩展字段真的能完全放行吗？
- 用户可能在扩展字段中写入错误数据类型（如`severity: 123`而非字符串）
- freeflow渲染器可能崩溃于复杂嵌套结构（如`{"nested": {"deep": {"recursive": "object"}}}`）

**发现缺陷**：
- ❌ validator完全放行扩展字段，可能导致下游工具（viewer/export）崩溃
- ❌ 未定义扩展字段的数据类型约束：severity应该是枚举字符串，而非任意值
- ❌ freeflow渲染器缺乏容错设计：复杂结构降级显示策略未定义

**建议改进**：
- 定义常见扩展字段的soft schema（如severity: string枚举，level: integer）
- validator校验扩展字段时采用soft模式（警告而非报错）
- freeflow渲染器增加容错：嵌套层级>3时降级为文本卡片

---

### 问题3：freeflow自适应渲染的技术可行性假设

**设计假设**：
```
freeflow足够灵活，只需定义视觉样式，无需开发独立knowledge-graph视图模板
```

**对抗性质疑**：
- freeflow当前渲染逻辑基于system分层架构，knowledge实体没有layer/category字段
- freeflow如何布局大量knowledge实体（例如50个痛点、30个策略）？
- relations关系连线复杂时（多个solves、prevents交叉），freeflow能否正确渲染？

**发现缺陷**：
- ❌ freeflow布局算法未适配knowledge实体（无layer/category，无法自动分层）
- ❌ 未定义knowledge实体的布局策略（中心发散？网格布局？自由布局？）
- ❌ 大量实体场景下的性能问题未评估（100+实体时freeflow渲染速度）

**建议改进**：
- 定义knowledge布局策略：painPoints为中心，strategies围绕，其他实体外围
- 新增布局算法：entityType-based clustering（按实体类型聚类）
- 定义性能上限：超过50实体时分页渲染或简化连线

---

## 二、边界条件未覆盖

### 问题4：混合蓝图的处理逻辑缺失

**设计假设**：
```
两种类型互斥，不设计hybrid（避免复杂度）
```

**对抗性质疑**：
- 用户实际需求可能真的需要混合蓝图（既要系统架构，又要know-how策略）
- AI判断"优先domain-knowledge"的规则，会导致architecture实体被遗漏
- relations跨类型关联（strategy → capability）在纯domain-knowledge蓝图中失效（capability不存在）

**发现缺陷**：
- ❌ 混合需求强制选择单一蓝图类型，丢失部分用户需求
- ❌ 跨类型关联的实用性假设：如果blueprintType=domain-knowledge，用户不能添加capability实体，跨类型关联无法建立
- ❌ 未定义混合蓝图的处理策略（是否允许？如何存储？）

**建议改进**：
- 允许hybrid蓝图类型（blueprintType="hybrid"），同时填充architecture和knowledge实体
- 定义hybrid蓝图的处理规则：relations必须明确区分跨类型关系和同类型关系
- 或者：允许domain-knowledge蓝图中可选添加architecture实体（非强制）

---

### 问题5：用户自定义实体的边界模糊

**设计假设**：
```
允许用户自定义实体类型数组（validator不校验数组名称）
```

**对抗性质疑**：
- 用户自定义实体与预定义实体的命名冲突如何处理？（如用户自定义"strategies"数组）
- 用户自定义实体类型命名不规范时，freeflow如何渲染？（如`"MyCustomEntity"`而非`"myCustomEntity"`）
- 用户自定义实体如何建立关系？（entityType不在relations定义中）

**发现缺陷**：
- ❌ 未定义命名冲突处理策略：用户自定义数组名称与预定义实体类型冲突时，validator行为未明确
- ❌ 用户自定义entityType的命名规范未定义（推荐camelCase？允许任意字符串？）
- ❌ 用户自定义实体的relations关系类型未定义（如何建立custom → custom的关系？）

**建议改进**：
- 定义命名冲突策略：用户自定义数组名称优先级高于预定义（允许覆盖）
- 定义entityType命名规范：推荐camelCase，validator校验格式（至少3字符，无特殊符号）
- 新增通用关系类型：`relates`（任意实体之间的弱关联）

---

### 问题6：relations关系完整性约束缺失

**设计假设**：
```
relations数组表达实体关联，新增solves/prevents/measures等关系类型
```

**对抗性质疑**：
- relations中的from/to ID不存在时，validator如何处理？
- 循环依赖如何避免？（strategy → practice → strategy）
- 用户可能建立不合理关系（如metric → pitfall，无语义意义）

**发现缺陷**：
- ❌ relations ID引用完整性未校验：from/to ID不存在时，validator不报错
- ❌ 循环依赖检测缺失：AI或用户可能建立A→B→C→A的循环关系
- ❌ 关系语义合理性未校验：measures只能metric→strategy，但用户可能写metric→pitfall

**建议改进**：
- validator校验relations ID引用完整性（from/to ID必须在library中存在）
- validator检测循环依赖（A→B→C→A时报错）
- 定义关系语义约束表（measures只能metric→strategy等），validator校验

---

## 三、内部矛盾和冲突

### 问题7：决策3与决策1的矛盾

**决策3**：
```
knowledge实体可单向关联architecture实体（单向关联）
```

**决策1**：
```
blueprintType互斥：architecture | domain-knowledge（无hybrid）
```

**矛盾点**：
- 如果blueprintType=domain-knowledge，library中不存在architecture实体（capabilities等）
- 此时跨类型关联（strategy → capability）无法建立（capability不存在）
- 决策3的单向关联假设失效

**发现矛盾**：
- ❌ 决策3假设knowledge实体可以关联architecture实体，但决策1禁止混合蓝图
- ❌ "不强加architecture关联"的补充说明，在纯domain-knowledge蓝图中等价于"无法关联"

**建议改进**：
- 修改决策1：允许hybrid蓝图类型，或允许domain-knowledge蓝图中可选添加architecture实体
- 或修改决策3：删除跨类型关联定义，仅在用户明确需求时才建立跨类型关系

---

### 问题8：severity字段定义与实体类型定义表的矛盾

**实体类型定义表**：
```
| strategies | "strategy" | level（可选） | - | 3-10 |
```
表格显示strategies无severity字段。

**实体字段规范章节**：
```
strategies可选字段未提及severity字段
```

**Relations关系类型定义**：
```
未提及strategy的severity字段，但pitfall有severity字段
```

**矛盾点**：
- 实体类型定义表显示strategies无severity，但用户可能误用或自定义severity
- severity统一为"严重程度"，但策略的"严重程度"语义不清晰（策略的有效性？策略的风险性？）

**发现矛盾**：
- ❌ 决策5统一severity字段，但实体类型定义表排除strategies的severity字段
- ❌ severity语义不明确：painPoint的severity=痛点严重程度，strategy的severity=？（策略有效性？策略风险性？）

**建议改进**：
- 明确strategies的severity语义：策略风险等级（low=低风险策略，high=高风险策略）
- 或删除strategies的severity字段定义，明确severity仅适用于painPoints/rules/pitfalls

---

### 问题9：向后兼容保证与schema扩展的冲突

**向后兼容保证**：
```
blueprintType默认值"architecture"，现有JSON无需修改
```

**Schema扩展**：
```
新增meta.blueprintType字段，新增library.knowledge块
```

**冲突点**：
- 现有JSON schema validator可能采用schema-first策略（严格校验所有字段）
- 新增字段（blueprintType、knowledge）可能导致现有validator报错"未知字段"
- 向后兼容保证依赖于validator的field-first策略（只校验已知字段，放行未知字段）

**发现冲突**：
- ❌ 设计假设validator采用field-first策略，但现有validator可能采用schema-first策略
- ❌ 未检查现有validator的实现策略（需要代码审查）

**建议改进**：
- 检查现有schema_validator.py的实现策略（schema-first or field-first）
- 如果schema-first，需要改造为field-first + whitelist模式（校验已知字段，放行白名单字段）

---

## 四、遗漏的关键细节

### 问题10：entityType命名规范缺失

**设计假设**：
```
entityType字段标识实体类型，validator不校验entityType名称
```

**遗漏细节**：
- entityType命名规范未定义（推荐camelCase？允许任意字符串？允许中文？）
- entityType与knowledge数组名称的映射关系未定义（如`entityType="painPoint"`对应`painPoints`数组）
- 用户自定义entityType时，AI如何匹配到对应的数组？

**发现遗漏**：
- ❌ entityType命名规范未定义（大小写、字符集、长度限制）
- ❌ entityType与数组名称的映射规则未定义（`entityType="caseStudy"`应放在哪个数组？）

**建议改进**：
- 定义entityType命名规范：camelCase，至少3字符，仅字母，推荐与数组名称匹配
- 定义entityType与数组名称映射：`entityType="painPoint"` → `painPoints`数组，用户自定义entityType → 对应数组名称需手动指定

---

### 问题11：hints模板的编写质量保证缺失

**设计假设**：
```
hints模板包含checklist，AI从"痛点：..."描述中自动解析实体类型
```

**遗漏细节**：
- hints模板编写质量如何保证？（checklist条目格式不规范时，AI解析出错）
- hints模板的测试策略未定义（如何验证hints模板的有效性？）
- 行业模板的覆盖度如何评估？（跨境电商模板是否覆盖关键痛点？）

**发现遗漏**：
- ❌ hints checklist条目格式规范未定义（"痛点：..."格式是唯一标准吗？）
- ❌ hints模板的测试策略未定义（AI解析checklist时，提取准确率如何测试？）
- ❌ hints模板覆盖度评估缺失（如何确保模板包含行业关键实体？）

**建议改进**：
- 定义checklist条目格式规范：`实体类型：具体条目1、条目2`，允许AI自动解析
- 定义hints模板测试策略：生成10个测试蓝图，验证AI提取准确率（>80%）
- 定义hints模板覆盖度评估：每个实体类型至少3个典型条目，覆盖率>90%

---

### 问题12：freeflow渲染器的降级策略缺失

**设计假设**：
```
freeflow渲染knowledge实体，定义视觉样式
```

**遗漏细节**：
- freeflow渲染大量实体时的性能降级策略未定义（100+实体时如何处理？）
- freeflow渲染复杂嵌套字段时的容错策略未定义（用户自定义字段嵌套层级>3时如何显示？）
- freeflow渲染错误entityType时的fallback策略未定义（未知entityType如何显示？）

**发现遗漏**：
- ❌ 性能降级策略缺失：超过50实体时分页渲染或简化连线
- ❌ 容错策略缺失：复杂嵌套字段降级为文本卡片，避免渲染崩溃
- ❌ fallback策略缺失：未知entityType使用默认灰色样式

**建议改进**：
- 定义性能上限：超过50实体时简化渲染（隐藏次要连线，聚类显示）
- 定义容错策略：嵌套字段>3层级时显示为`{...}`文本卡片
- 定义fallback样式：未知entityType使用灰色默认样式 + generic图标

---

### 问题13：实施阶段的质量保证缺失

**设计假设**：
```
Phase 1 → Phase 2 → Phase 3顺序实施，每个Phase完成后回归测试
```

**遗漏细节**：
- Phase 1验收标准"AI可参照提取"如何量化？（提取准确率？）
- Phase 2验收标准"validator校验核心字段"如何测试？（单元测试覆盖率？）
- Phase 3验收标准"freeflow渲染knowledge实体"如何验证？（渲染质量评估？）

**发现遗漏**：
- ❌ Phase验收标准缺乏量化指标（准确率、覆盖率、渲染质量）
- ❌ 回归测试的具体测试用例未定义（现有architecture蓝图的测试清单）
- ❌ 跨Phase集成测试策略缺失（Phase 1 + Phase 2 + Phase 3集成后如何测试？）

**建议改进**：
- 定义量化验收标准：AI提取准确率>80%，validator单元测试覆盖率>90%，freeflow渲染质量评分>8/10
- 定义回归测试清单：现有10个architecture蓝图必须通过validator，导出视图不变
- 定义集成测试策略：生成5个domain-knowledge蓝图，完整流程验证（提取→校验→渲染→导出）

---

## 五、实施风险低估

### 问题14：Phase 2工作量低估

**设计估算**：
```
Phase 2：Validator改造（4-6小时）
```

**对抗性质疑**：
- validator改造可能涉及现有架构重构（schema-first → field-first）
- validator单元测试编写可能超出1-2小时（需要覆盖architecture、domain-knowledge、hybrid、用户自定义等场景）
- validator集成到cli.py可能需要修改多个命令（`--plan`、`--validate`、`--export`）

**发现风险**：
- ❌ validator改造工作量可能低估（现有validator架构不明确，可能需要重构）
- ❌ 单元测试编写工作量低估（需要覆盖10+测试场景）
- ❌ 集成工作量低估（需要修改多个cli命令）

**建议改进**：
- 调整Phase 2工作量估算：validator改造（3-4小时），单元测试（2-3小时），cli集成（1-2小时），总计6-9小时
- 新增Phase 2.5：validator架构审查（检查现有validator实现策略，0.5-1小时）

---

### 问题15：Phase 3技术难度低估

**设计估算**：
```
Phase 3：导出引擎改造（6-8小时）
```

**对抗性质疑**：
- freeflow渲染器改造可能涉及布局算法重构（从layer-based到entityType-based）
- freeflow渲染knowledge实体需要新增样式系统（颜色、形状、图标、severity分级）
- relations关系连线渲染需要新增箭头样式系统（实线、虚线、双向箭头）

**发现风险**：
- ❌ freeflow布局算法重构技术难度高（从layer-based改为entityType-based clustering）
- ❌ 样式系统设计复杂（颜色映射、形状渲染、图标集成、severity分级）
- ❌ 关系连线渲染复杂（不同关系类型的箭头样式、避免连线交叉）

**建议改进**：
- 调整Phase 3工作量估算：布局算法重构（3-4小时），样式系统（2-3小时），连线渲染（2-3小时），cli集成（1小时），总计8-11小时
- 新增Phase 3.5：freeflow渲染器原型验证（验证knowledge实体渲染可行性，2小时）

---

### 问题16：向后兼容测试覆盖率不足

**设计假设**：
```
所有现有architecture蓝图JSON必须通过validator校验
```

**对抗性质疑**：
- 现有多少个architecture蓝图？（demos目录下的蓝图数量）
- 回归测试清单未定义（具体测试哪些蓝图？）
- 导出视图兼容性未测试（现有architecture蓝图的导出视图是否改变？）

**发现风险**：
- ❌ 现有architecture蓝图数量未明确，回归测试覆盖率不足
- ❌ 导出视图兼容性未测试（freeflow渲染knowledge样式后，architecture实体的渲染是否受影响？）
- ❌ 性能兼容性未测试（新增knowledge渲染逻辑后，architecture蓝图导出速度是否下降？）

**建议改进**：
- 定义回归测试清单：遍历demos目录所有architecture蓝图（预计10-15个），逐一测试validator + export
- 定义导出视图兼容性测试：对比新旧导出结果（SVG diff），确保architecture视图不变
- 定义性能基准测试：导出速度应保持不变（允许±10%波动）

---

## 六、质量问题

### 问题17：文档结构不一致

**发现**：
- 实体字段规范章节详细（painPoints、strategies、rules等），但relations关系类型定义简略
- 导出视图渲染设计章节详细（样式定义），但AI提取指南章节简略（提取流程）
- Validator改造设计章节详细（代码示例），但实施路径章节简略（工作量估算）

**建议改进**：
- 补充relations关系类型详细定义（每个关系类型的语义、适用场景、错误示例）
- 补充AI提取详细流程（实体提取顺序的详细步骤、错误处理、hints解析逻辑）
- 补充实施路径详细清单（每个Phase的文件改动列表、测试用例清单、验收标准）

---

### 问题18：术语定义不一致

**发现**：
- "domain-knowledge蓝图"在不同章节表述不一致（有时称"knowledge蓝图"，有时称"know-how蓝图"，有时称"领域知识图谱"）
- "blueprintType"字段名称与"蓝图类型"概念混用（文档未明确区分字段名和概念名）
- "severity"字段在不同实体类型中语义不一致（painPoint的severity=痛点严重程度，strategy的severity=？）

**建议改进**：
- 统一术语：domain-knowledge蓝图（标准术语），knowledge蓝图（简写），禁止使用"know-how蓝图"、"领域知识图谱"
- 统一字段名与概念名：blueprintType（字段名），蓝图类型（概念名），明确区分
- 统一severity语义：severity=严重程度/风险等级，明确每个实体类型的severity语义

---

### 问题19：示例数据真实性不足

**发现**：
- 实体字段示例过于简单（如painPoint只有id/name/entityType，缺少真实业务上下文）
- relations关系示例过于抽象（如"测款节奏策略 → ROI不稳"，缺少完整JSON示例）
- 跨境电商hints模板的checklist过于简化（如"痛点：ROI不稳"，缺少具体业务场景描述）

**建议改进**：
- 补充完整JSON示例：包含10+实体的完整domain-knowledge蓝图JSON
- 补充relations完整示例：包含from/to/type/label的完整relations数组
- 补充跨境电商完整hints模板：包含业务上下文（如"痛点：ROI不稳（欧美市场电商类目，ROAS目标>3.0但实际波动2.0-5.0）")

---

## 七、对抗性评审总结

### 高危问题（P0，必须修复）

| 问题 | 影响 | 修复建议 |
|------|------|---------|
| 问题1：AI判断意图不可靠 | 用户需求被误解，生成错误蓝图类型 | 新增判断优先级 + 手动覆盖机制 |
| 问题4：混合蓝图处理逻辑缺失 | 用户混合需求被强制简化，丢失部分需求 | 允许hybrid蓝图类型或可选architecture实体 |
| 问题7：决策3与决策1矛盾 | 跨类型关联失效，无法建立strategy→capability关系 | 允许hybrid蓝图或删除跨类型关联定义 |
| 问题9：向后兼容保证与schema扩展冲突 | 现有validator可能报错，向后兼容失效 | 检查现有validator实现策略 + 改造方案 |
| 问题14：Phase 2工作量低估 | 实施延期，资源不足 | 调整工作量估算6-9小时 |

### 中危问题（P1，应该修复）

| 问题 | 影响 | 修复建议 |
|------|------|---------|
| 问题2：扩展字段完全放行 | 下游工具可能崩溃 | 定义soft schema + 容错设计 |
| 问题3：freeflow布局算法未适配 | knowledge实体无法正确布局 | 定义布局策略 + clustering算法 |
| 问题6：relations完整性约束缺失 | 循环依赖、不合理关系 | ID引用校验 + 循环依赖检测 + 语义约束 |
| 问题10：entityType命名规范缺失 | 用户自定义实体命名混乱 | 定义命名规范 + 映射规则 |
| 问题15：Phase 3技术难度低估 | 实施延期，质量不达标 | 调整工作量估算8-11小时 |
| 问题16：向后兼容测试不足 | 现有蓝图导出视图可能受影响 | 定义回归测试清单 + diff对比 |

### 低危问题（P2，建议修复）

| 问题 | 影响 | 修复建议 |
|------|------|---------|
| 问题5：用户自定义实体边界模糊 | 命名冲突、关系类型不清 | 定义命名冲突策略 + 通用关系类型 |
| 问题8：severity语义矛盾 | strategy的severity语义不清晰 | 明确strategy severity语义或删除定义 |
| 问题11：hints编写质量保证缺失 | AI提取准确率低 | 定义格式规范 + 测试策略 + 覆盖度评估 |
| 问题12：freeflow降级策略缺失 | 性能问题、渲染崩溃 | 定义性能上限 + 容错策略 + fallback样式 |
| 问题13：实施质量保证缺失 | 验收标准模糊、测试覆盖不足 | 定义量化验收标准 + 测试清单 + 集成测试 |
| 问题17：文档结构不一致 | 阅读困难、理解歧义 | 补充详细定义章节 |
| 问题18：术语定义不一致 | 理解歧义 | 统一术语使用 |
| 问题19：示例数据真实性不足 | 理解困难 | 补充完整JSON示例 |

---

## 八、修复优先级建议

**立即修复（P0）**：
- 问题1、4、7、9、14 → 这些问题直接影响设计可行性和实施成功率

**短期内修复（P1）**：
- 问题2、3、6、10、15、16 → 这些问题影响实施质量和稳定性

**长期迭代修复（P2）**：
- 问题5、8、11、12、13、17、18、19 → 这些问题影响使用体验和文档质量

---

## 九、对抗性评审结论

**总体评价**：
- 设计思路清晰，核心决策合理（强核心+弱扩展、freeflow渲染、单向关联）
- 但存在5个高危问题，直接影响设计可行性和实施成功率
- 中危问题影响实施质量和稳定性，需要在实施前修复
- 低危问题可以在实施过程中迭代修复

**修复建议**：
- 修复P0问题后，重新审查设计文档
- 补充缺失的关键细节（entityType命名规范、hints测试策略、freeflow降级策略）
- 调整工作量估算（Phase 2: 6-9小时，Phase 3: 8-11小时）
- 定义量化验收标准和回归测试清单

**下一步**：
- 修复高危问题
- 补充缺失细节
- 调整工作量估算
- 重新提交设计文档审查

---

**对抗性评审完成日期**: 2026-04-28
**评审者**: Claude Code（对抗性视角）