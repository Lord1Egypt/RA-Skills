---
name: lowcode-module-generator
description: 低代码模块生成器 - 变更记录
---

# 变更记录

## v2.3.0 (2026-05-17)

### 修改

- **check 输出格式优化**：检查结果按分类逐类输出，每个分类显示检查项数统计
- **新增分类统计格式**：
  - 基础检查：`36项（23项相关，13项N/A）`
  - 关联类型专项：`3项（全部通过）`
  - 左右布局专项：`6项（全部通过）`
- **check 参考示例更新**：各示例文件的检查项数重新统计

---

## v2.2.0 (2026-05-16)

### 新增

- **新增步骤9：CHECK 检查机制**：工作流程最后必须执行 check 检查，全部通过才能结束
- **新增 check 检查清单**：35 项基础检查点 + 关联类型专项 + 左右布局专项 + Tree表专项
- **新增示例检查清单**：7个示例文件各自包含对应的检查点清单

### 修改

- SKILL.md 工作流程从 8 步扩展为 9 步，新增步骤9
- SKILL.md 的步骤9根据示例类型引用不同的检查清单
- 各示例文件（example-common.md等）补充完整的 check 检查清单及对应模板文件对照表

### 检查清单对应关系

| 示例文件 | 检查点数量 |
|---------|-----------|
| example-common.md | 35项（基础） |
| example-org.md | 38项（基础+org关联） |
| example-user.md | 38项（基础+user关联） |
| example-project.md | 38项（基础+project关联） |
| example-fileupload.md | 38项（基础+fileUpload关联） |
| example-leftright-action.md | 41项（基础+左右布局专项） |
| example-leftright-folder.md | 44项（基础+左右布局专项+Tree专项） |

---

## v2.1.0 (2026-05-16)

### 新增

- **新增 src/documents/template-constraints.md**：模板约束规则独立文档
- **新增铁律**：生成代码前必须先读取模板文件，禁止根据经验生成
- **新增说明**：明确 BaseService 类型参数为2个（Mapper, Po），不是5个
- **警告示例**：添加错误示例和正确示例对比

### 修改

- SKILL.md 模板约束规则章节改为引用方式，引用 src/documents/template/template-constraints.md
- **目录结构调整**：将 velocity-variables 文件夹重命名为 template，两个文档放在同一文件夹下

---

## v2.0.0 (2026-05-16)

### 新增

- 完善 Velocity 模板变量填充规则文档
- 新增关联类型（relevancyType 1/2/3）配置说明
- 新增自定义字段（buildEnableCustomField）开关说明
- 新增工作流开关（buildEnableWf/buildHasEnableWorkflow）说明
- 新增分类码分组（showClassifyGroup）变量说明
- 补充字段明细表扩展字段定义
- 完善前端关联类型渲染规则
- **新增 SQL生成器**：支持 MySQL/Oracle/达梦 三种数据库的初始化SQL生成
- **新增 src/documents/sql-generator.md**：SQL生成详细说明文档

### 完善

- 重写 README.md，用户输入格式更清晰
- 完善 SKILL.md 中的变量说明文档
- 补充 Java 类型映射表
- 补充前端组件映射表
- 补充关联类型渲染表
- **新增第6节：关联字段变量（buildRelationList）**，详解 rl.relation/relationName/voClassName/paramEnumCode
- **新增第7节：前端特殊变量**，详解 codeBuilderId 和 column.fieldType
- **新增第9节：formType 表单控件类型**，补充 widgetType 到 formType 的映射规则
- **新增页面布局类型说明**：普通主页、左右布局、标签页、工作流
- **删除上下布局类型**
- **新增布局类型自动判断**：根据用户输入关键词自动判断
- **新增左右布局自动判断流程**：解析描述→外键配置→生成联动代码
- **明确左右布局代码组织**：前端代码生成到同一模块目录，后端代码按业务对象分开到同一个微服务工程
- **新增标签页（页签）支持**：详解标签页结构、识别特征、模板文件、代码组织
- **新增标签页与布局组合说明**：普通主页+标签页 vs 左右布局+标签页
- **新增联动原理**：普通主页和左右布局的标签页联动差异

---

## v1.0.0 (2026-05-15)

### 新增

- 初始版本
- 后端代码生成器 (backendGenerator.js)
- 前端代码生成器 (frontendGenerator.js)
- 名称转换工具 (nameConverter.js)
- 模板引擎 (templateEngine.js)
- 后端模板 (po, form, vo, service, controller, mapper)
- 前端模板 (index, topTags, addModal, infoForm)
- 模块配置 (moduleConfig.js)
- 低代码平台的Velocity模板参考代码路径

### 功能

- 支持简体中文名称转英文标识
- 支持生成PO、Form、VO、Service、Controller、Mapper
- 支持生成前端主页、工具栏、新增弹窗、编辑表单
- 支持字段类型映射
- 支持自定义功能模块（增删改查发布）
