# Skill生成与验证模块

## 执行触发

**本模块在workflow.json生成后自动执行：**
- **模式1**：在WORKFLOW.md（阶段2）完成后自动执行（阶段3）
- **模式2**：在DATASAVER录制工作流转换模块（阶段1）完成后自动执行（阶段2）

<mandatory-rule>
本模块是两种模式的最后阶段，负责将workflow.json转换为符合Claude Code标准的可复用Skill。
无论是模式1还是模式2，都会在生成workflow.json并得到用户确认后自动执行本模块。
</mandatory-rule>

## 步骤进度初始化（强制要求）

<mandatory-rule>
在执行本阶段任何操作前，必须先使用 TodoWrite 工具初始化以下步骤列表。
这是强制要求，不可跳过。
</mandatory-rule>

**初始化内容**：

使用 TodoWrite 工具创建以下 todos（全部设为 pending 状态）：

| 步骤 | content | activeForm |
|-----|---------|------------|
| 1 | 读取工作流文件 | 读取工作流文件中 |
| 2 | 创建Skill目录结构 | 创建Skill目录结构中 |
| 3 | 生成SKILL.md | 生成SKILL.md中 |
| 4 | 生成scripts/references文件 | 生成scripts/references文件中 |
| 5 | 验证Skill可用性 | 验证Skill可用性中 |
| 6 | 完成、发布与确认 | 完成、发布与确认中 |

**状态管理规则**：

1. **开始步骤前**：将该步骤标记为 `in_progress`
2. **完成步骤后**：立即将该步骤标记为 `completed`
3. **同一时间**：只能有一个步骤处于 `in_progress` 状态
4. **顺序执行**：必须按步骤顺序执行，不可跳过

## 概述

本模块负责将workflow.json转换为符合Claude Code标准的可复用Skill。通过生成标准化的Skill结构、验证功能完整性，确保生成的Skill高质量、高可用。

## 核心原则

### 1. 生成高质量Skill的五个原则

1. **简洁清晰**：主SKILL.md控制在500行以内，核心逻辑清晰
2. **渐进披露**：从概述到细节，层次分明
3. **参数友好**：提供清晰的参数说明和示例
4. **可维护性**：结构规范，易于更新
5. **自包含性**：不依赖外部资源

### 2. 质量保证机制

- **结构验证**：检查必需文件和目录
- **内容验证**：确保指令完整可执行
- **可用性推断**：基于前置阶段执行经验确认可用
- **迭代优化**：根据用户反馈改进

## 执行步骤

```
<mandatory-rule>
Skill的生成包含以下6个步骤，必须严格按此流程执行不能省略或者添加其他步骤：
</mandatory-rule>
```

### 1. 读取工作流文件

从当前工作目录读取WORKFLOW模块生成的工作流：
```
[当前工作目录]/workflow-workflows/[skill-name]-workflow.json
```

解析工作流结构，提取：
- `name`：Skill名称
- `description`：功能描述
- `platform`：目标平台
- `parameters`：用户参数列表
- `steps`：执行步骤

### 2. 创建Skill目录结构

使用 init_skill.py 在**当前工作目录**下创建标准化结构：
```bash
scripts/init_skill.py workflow-workflows/[skill-name]-workflow.json
```

创建的目录结构：
```
[当前工作目录]/workflow-skills/[skill-name]/
└── SKILL.md                    # 主文件（包含完整的执行指令）
```

**注意**：
- 默认只创建 SKILL.md 文件
- scripts/ 目录只在需要辅助脚本时再创建
- references/ 目录只在需要参考资料时再创建


### 3. 生成SKILL.md

<mandatory-rule>
[skill_template.md](assets/skill_template.md) - SKILL.md的标准格式和完整示例。
**在生成前必须读取此文件并参考其格式生成Skill。
</mandatory-rule>

#### 3.1 YAML头部
```yaml
---
name: xiaohongshu-post
description: 在小红书发布图文笔记
version: 1.0.0
---
```

#### 3.2 主体结构
```markdown
# 小红书图文笔记发布

## 概述
[基于workflow的description生成]

## 快速开始
用户："使用xiaohongshu-post发布一篇关于美食的笔记，参数如下：xxxxx"

## 必需参数
[基于parameters生成参数说明表]

## 执行流程

### 步骤1：[步骤描述]
**工具**：[tool_name]
**参数**：
- [参数名]: [参数值或占位符]

**说明**：[详细说明这一步的作用]

### 步骤2：[步骤描述]
...
[继续列出所有步骤，每个步骤包含工具、参数、说明]

### 收集页面数据步骤

当工作流中包含`purpose: "get_html_info"`的数据收集步骤时，**必须**使用 web-data-extractor：

**工具**：`web-data-extractor` skill

**调用方式**：调用 web-data-extractor skill，提取当前页面的[数据描述]

### 日期选择器相关步骤的处理

如果workflow.json中包含日期选择相关的步骤（如打开日历、导航月份、选择日期等），**必须**参考 [DATE_PICKER_HANDLING.md](references/DATE_PICKER_HANDLING.md) 中的"SKILL.md 生成模板"章节生成对应的SKILL.md内容。

**识别条件**（满足任一）：
- tool_call的selector包含：date, calendar, picker, month, year, time
- reasoning中提到"日期"、"时间"、"选择日期"
- 连续多个chrome_click_element点击数字1-31
- 页面文本包含"开始时间"、"结束时间"、"~"、"-"

## 重要提示

### 上下文保护策略

本Skill中的获取页面信息步骤（步骤X）使用了Task Tool进行上下文隔离：

- **为什么**：chrome_get_web_content() chrome_accessibility_snapshot()或chrome_screenshot()会返回大量数据（~84k tokens）
- **如果不隔离**：会迅速填满主agent上下文，导致后续步骤失败
- **Task Tool的作用**：创建独立的subagent处理大数据，只返回精简的结构化结果
- **重要**：执行此Skill时，不要修改Task Tool步骤为直接调用chrome工具

**核心原则**：

- 主agent提供意图（需要什么数据）
- Subagent调用工具、处理大数据、提取信息
- 返回精简结果（JSON格式，不是原始HTML）
- 保持主上下文清洁

### 动态参数机制

本Skill使用了动态选择器查找（步骤x），原因：

- xxx页面结构可能因更新而变化
- 使用`chrome_accessibility_snapshot`根据文本内容动态查找
- 即使页面改版，通过动态机制实时获取最新参数，Skill仍可正常工作

## 注意事项

### 平台特性

[基于platform生成平台特定的注意事项]

### 常见问题

**问题1：[问题描述]**

- 症状：[具体表现]
- 解决：[解决方案]

**问题2：[问题描述]**

- 症状：[具体表现]
- 解决：[解决方案]

[根据工作流步骤生成2-3个常见问题]
```

### 4. 生成scripts/ references/ 文件（可选）

如果需要则在scripts/ 目录下生成辅助脚本

如果需要则在references/ 目录下参考文件

### 5. 验证Skill可用性

#### 5.1 结构完整性检查

- SKILL.md存在且包含正确的YAML头
- 文件长度 < 500行

使用 validate_skill.py 脚本辅助检查：
```bash
scripts/validate_skill.py workflow-skills/[skill-name]/
```

#### 5.2 格式规范检查

- 参数占位符格式统一（{param_name}）
- 动态参数引用正确（{step_N.param}）

#### 5.3 内容一致性检查（基于前置阶段经验）

对比 workflow.json 验证：
- 步骤是否完整转换（workflow.steps → SKILL.md执行流程）
- 参数列表是否一致（workflow.parameters → SKILL.md必需参数）
- 动态参数的 step 引用是否正确（step_N 是否存在且有对应 output）

#### 5.4 可执行性推断

**核心逻辑**：前置阶段（LOG.md执行浏览器操作 / DATASAVER录制工作流转换模块实际执行验证）已成功完成，根据执行过程分析生成的 Skill 可用性。

检查 SKILL.md 内容：
- 步骤描述是否清晰可执行
- 关键信息是否已说明（选择器来源、Task Tool 用途）
- 是否包含必要的上下文保护策略说明
- 如存在日期选择器步骤，分析它是否具备良好的可用性

#### 5.5 问题修复（如发现问题）

如果检查发现问题，直接修复 SKILL.md：

| 问题类型 | 修复方法 |
|---------|---------|
| 格式错误 | 修正参数占位符格式、工具名格式 |
| 步骤遗漏 | 对比workflow.json补充遗漏步骤 |
| 参数引用错误 | 修正{step_N.param}引用 |
| 内容不一致 | 与workflow.json对齐 |

### 6. 完成、发布与确认

<mandatory-rule>
⚠️ 关键要求：在结束前，必须先向用户展示生成的Skill摘要并等待确认！
</mandatory-rule>

#### 步骤6.1：展示Skill摘要并等待用户确认

**展示Skill生成摘要：**

```
✅ Skill生成完成！

📊 生成统计：
- Skill名称：[skill-name]
- 包含步骤：5个
- 用户参数：3个
- 文件数量：7个

✅ 验证结果：
- 结构验证：通过
- 内容验证：通过
- 可用性检查：通过（基于前置阶段执行经验）

📁 文件位置：
[当前工作目录]/workflow-skills/[skill-name]/

🚀 使用方法：
直接说："使用xiaohongshu-post发布xxx"

---

请确认生成的Skill是否符合您的预期？

如果满意，我将：
1. 发布到服务端（如果环境支持）
2. 完成Skill创建流程

如果有需要调整的地方，请告诉我：
- Skill的步骤是否需要修改？
- 参数设置是否合理？
- 说明文档是否清晰？
- 其他任何需要改进的地方
```

**等待用户响应**：
- **用户确认满意/没有问题**：执行步骤6.3（发布到服务端）
- **用户提出修改意见**：根据反馈修改或者重新生成Skill

#### 步骤6.2：根据用户反馈重新生成（仅在用户提出意见时执行）

**分析用户反馈**：

1. **识别反馈类型**：
   - **步骤调整**：需要增加、删除或修改某些步骤
   - **参数修改**：参数命名、类型、默认值需要调整
   - **文档完善**：SKILL.md说明不够清晰，需要补充
   - **格式优化**：代码格式、结构组织需要改进
   - **功能增强**：需要添加错误处理、边界情况处理等

2. **定位修改位置**：
   - 步骤调整 → 修改SKILL.md的执行流程部分
   - 参数修改 → 修改SKILL.md的必需参数部分和workflow.json
   - 文档完善 → 修改SKILL.md的对应章节
   - 格式优化 → 调整SKILL.md的排版和结构
   - 功能增强 → 修改SKILL.md并可能更新workflow.json

3. **执行修改**：
   - 根据用户反馈编辑对应文件
   - 保持文件结构的一致性
   - 确保修改后仍符合Skill标准

4. **重新验证**（如果修改了关键部分）：
   - 如果修改了workflow.json → 运行validate_skill.py验证结构
   - 如果修改了步骤逻辑 → 可选择重新执行功能测试
   - 如果只是文档调整 → 不需要重新测试

5. **再次展示给用户并回到步骤6.1**：
   ```
   ✅ 已根据您的反馈进行修改
   
   📝 修改内容：
   - [列出具体修改项]
   
   📁 修改的文件：
   - [列出修改的文件路径]
   
   ---
   
   请确认修改后的Skill是否满意？
   ```

   **修改完成后**：返回步骤6.1重新等待用户确认，用户可以：
   - 确认满意 → 执行步骤6.3发布
   - 继续提出修改意见 → 再次执行步骤6.2

**重试限制**：
- 最多允许3次修改迭代
- 如果3次后用户仍不满意，建议：
  ```
  经过3次修改迭代，建议您直接编辑Skill文件进行精细调整：
  
  📁 Skill位置：[当前工作目录]/workflow-skills/[skill-name]/
  
  主要文件：
  - SKILL.md：主要执行逻辑和参数说明
  - workflow.json：底层工作流定义（如需修改步骤）
  ```

---

#### 步骤6.3：发布Skill到服务端（如果tool可用）

<mandatory-rule>
此步骤**仅在用户明确确认发布后执行**（如用户回复"确认发布"、"可以发布"等）。
如果检测到用于发布Skill的 create_workflow tool可用，询问用户是否发布到服务端；
否则跳过此步骤，Skill保留在本地目录即可。
</mandatory-rule>

##### 检测与决策

**检测方法**：
检查当前环境中是否存在 `create_workflow` tool。

**探索方式**：

- 方法1：查看当前可用的工具列表
- 方法2：直接尝试调用tool，捕获"tool not found"异常

**决策逻辑**：
- Tool可用 → 阅读 [references/PUBLISH_SKILL.md](references/PUBLISH_SKILL.md) 并执行发布流程
- Tool不可用 → 跳过发布，展示提示："服务端发布功能不可用，Skill已保存在本地"

## 质量检查清单

在完成Skill生成前，确认以下事项：

### 结构规范
- 目录结构符合标准
- 所有必需文件已创建
- 文件命名规范

### 内容质量
- SKILL.md简洁清晰（<500行）
- 参数说明完整准确
- 步骤指令可执行
- 故障排查实用

### 可用性验证
- 前置阶段（LOG/DATASAVER录制工作流转换）执行成功
- 内容与workflow.json一致
- 参数引用正确

### 可维护性
- 代码注释充分
- 文档说明清晰
- 版本信息完整

