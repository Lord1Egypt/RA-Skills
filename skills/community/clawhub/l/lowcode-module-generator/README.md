---
name: lowcode-module-generator
description: 低代码模块生成器 - 人读概览
---

# 低代码模块生成器

基于低代码平台的Velocity模板，自动生成新模块的完整前后端代码。

## 功能说明

当用户需要开发新模块时，调用本技能生成代码框架。用户只需提供简体中文模块名 + 字段明细表。

AI自动推断表类型：有parentId → Tree，否则 → Data

## 核心能力

- **自动命名转换**：简体中文名称 → 英文标识、类名前缀
- **后端代码生成**：PO、Form、VO、Service、Controller、Mapper、Feign
- **前端代码生成**：主页、工具栏、表单、标签页、工作流
- **模板引擎**：基于Velocity语法，支持复杂模板替换

## 用户输入格式

### 必需信息

1. **新模块简体中文名称**（如：设备管理）
2. **字段明细表**

AI自动推断表类型：
- 字段中有 `parentId` 或 `parent_id` → **Tree**（树形表）
- 否则 → **Page**（分页数据表）

### 字段明细格式
| 字段名(简体中文) | 字段名(英文) | 类型 | 必填 | 列表显示 | 关联类型 | 关联配置 |
|------------|------------|------|-----|---------|---------|---------|
| 设备名称 | equipmentName | String | ✓ | ✓ | | |
| 设备编号 | equipmentCode | String | | ✓ | | |
| 责任部门 | orgId | Long | ✓ | ✓ | org | |
| 设备状态 | status | String | ✓ | ✓ | dict | equipment_status |
| 供应商 | supplierId | Long | | | relevancy | type:2,url:/api/base/supplier |

3. **表类型**：Tree / Data / 普通
4. **外键配置**（可选）：epsId（关联EPS项目）

### 关联类型

| 关联类型 | 说明 | 渲染方式 |
|---------|------|---------|
| dict | 数据字典 | getDictNameByProject |
| org | 组织架构 | 显示name |
| user | 用户 | 显示name |
| project | 项目 | 显示name |
| relevancy | 数据关联 | 弹窗选择 |

### relevancyType 三种模式

| type值 | 说明 | 前端组件 |
|-------|------|---------|
| 1 | 枚举类型 | FormSelect + customDicts |
| 2 | 远程搜索 | FormSelect + URL |
| 3 | 弹窗选择 | FormDataModel + Modal |

## 输出内容

| 类型 | 生成内容 |
|-----|---------|
| 后端-PO | 数据库实体类 |
| 后端-Form | 新增/修改/查询表单 |
| 后端-VO | 视图对象/树形VO/分页VO |
| 后端-Service | 服务接口+实现 |
| 后端-Controller | REST控制器+工作流控制器 |
| 后端-Mapper | Mapper接口+XML |
| 前端-主页 | 列表+工具栏+右侧标签 |
| 前端-工具栏 | 操作按钮 |
| 前端-表单 | 新增/修改/搜索/信息表单 |
| 前端-标签页 | 标签页索引+工具栏 |
| 前端-工作流 | 审批主页+审批表单 |

## 默认功能

新模块默认包含：
- 列表查询（分页/树形/普通）
- 新增
- 修改
- 删除
- 工作流审批（可选配置）

## 命名规则

| 项目 | 规则               | 示例                    |
|-----|------------------|-----------------------|
| 模块英文标识 | 模块中名的英文翻译        | 设备管理 → equipment （驼峰） |
| 类名前缀 | 首字母大写            | equipment → Equipment |
| 表名 | {database.tablePrefix}{模块}    | wsd_plan_equipment    |
| API路径 | api/{服务名}/{模块标识} | api/plan/equipment    |

## 使用流程

```
1. 用户提供新模块简体中文名称和字段明细
2. Agent调用本技能
3. 分析字段明细，构建模板变量
4. 生成完整代码框架
5. 输出给用户确认/调整
```

## 代码存放位置

- 后端：`{microservice.path}/`
- 前端：`{frontend.path}/{模块名}/`

## 模板来源

模板来源于 `wsd-adp/src/main/resources/codebuilder/` 目录，共 **30个** .vm 模板文件：
- java/ - 后端Java模板（12个）
- web/ - 前端React模板（18个）

**重要**：模板文件禁止修改，如需调整功能请新建模板或使用配置参数。

---

## 详细文档

详细说明请参考 [SKILL.md](SKILL.md)，包含：
- 核心概念：[src/documents/core-concepts/core-concepts.md](src/documents/core-concepts/core-concepts.md)
- 布局类型：[src/documents/layout-types/](src/documents/layout-types/)
- 表单控件：[src/documents/form-controls/form-controls.md](src/documents/form-controls/form-controls.md)
- 模板变量：[src/documents/velocity-variables/velocity-variables.md](src/documents/velocity-variables/velocity-variables.md)
- 使用示例：[src/documents/examples/](src/documents/examples/)

---

本技能基于低代码平台的Velocity模板的代码结构生成。
