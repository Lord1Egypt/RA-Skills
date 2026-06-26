---
name: lowcode-module-generator
description: 低代码模块生成器。低代码平台出码（完整前后端代码），支持ACM系统的普通主页、左右布局等模块开发。用户只需提供中文模块名和字段明细表，即可生成 PO、Form、VO、Service、Controller、Mapper 等后端代码，以及前端 React 页面组件。
metadata:
  type: generator
  version: 2.3.0
  author: wisdom hejian
  created: 2026-05-15
  updated: 2026-05-17
---

# 低代码模块生成器 技能

低代码平台出码（完整前后端代码），支持ACM系统的普通主页、左右布局等模块开发。用户只需提供中文模块名和字段明细表，即可生成 PO、Form、VO、Service、Controller、Mapper 等后端代码，以及前端 React 页面组件。

---

## 目录结构

```
lowcode-module-generator/
├── SKILL.md                               # 技能定义文档（Agent 必读）
├── README.md                              # 本文件（人读概览）
├── CHANGES.md                             # 变更记录
└── src/
    ├── config.json                         # 配置文件（microservice、frontend、database）
    ├── documents/                          # 详细说明文档
    │   ├── template/                       # 模板约束与变量说明
    │   │   ├── velocity-variables.md       # Velocity 模板变量说明
    │   │   └── template-constraints.md     # 模板约束规则说明
    │   ├── form-controls/                  # 表单控件说明
    │   ├── layout-types/                   # 布局类型说明
    │   │   ├── layout-labels.md            # 标签页说明
    │   │   └── layout-leftright.md         # 左右布局说明
    │   ├── examples/                       # 使用示例（按需加载）
    │   │   ├── example-common.md           # 普通主页示例
    │   │   ├── example-org.md              # 组织下拉框示例
    │   │   ├── example-user.md             # 用户下拉框示例
    │   │   ├── example-fileupload.md       # 附件上传示例
    │   │   ├── example-project.md          # 选择项目示例
    │   │   ├── example-leftright-action.md # 左右布局-普通列表
    │   │   └── example-leftright-folder.md # 左右布局-树形列表
    │   └── sql-generator.md                # SQL生成说明
    └── template/                           # Velocity 模板文件（原始模板，禁止修改）
        ├── 说明.txt                         # 模板说明文档
        ├── java/                           # 后端Java模板
        │   ├── po/                         # PO实体模板
        │   │   └── po.java.vm
        │   ├── vo/                         # VO视图模板
        │   │   ├── vo.java.vm
        │   │   ├── treevo.java.vm
        │   │   └── datavo.java.vm
        │   ├── form/                       # Form模板
        │   │   ├── addform.java.vm
        │   │   ├── updateform.java.vm
        │   │   └── searchform.java.vm
        │   ├── service/                    # Service模板
        │   │   ├── service.java.vm
        │   │   └── serviceimpl.java.vm
        │   ├── controller/                 # Controller模板
        │   │   ├── controller.java.vm
        │   │   └── controller-wf.java.vm
        │   ├── mapper/                     # Mapper模板
        │   │   ├── mapper.java.vm
        │   │   └── mapper.xml.vm
        │   └── feign/                      # Feign模板
        │       └── relevancyApiFeign.java.vm
        └── web/                            # 前端React模板
            ├── index/                      # 主页模板
            │   ├── web-index.jsx.vm
            │   └── web-toptags.jsx.vm
            ├── form/                       # 表单模板
            │   ├── web-addform.jsx.vm
            │   ├── web-updateform.jsx.vm
            │   ├── web-searchform.jsx.vm
            │   └── web-infoform.jsx.vm
            ├── labels/                     # 标签页模板
            │   ├── web-label-index.jsx.vm
            │   └── web-label-toptags.jsx.vm
            ├── wf/                         # 工作流模板
            │   ├── web-wf-index.jsx.vm
            │   └── web-wf-approval.jsx.vm
            ├── leftRight/                  # 左右布局模板
            │   ├── web-left-index.jsx.vm
            │   ├── web-left-toptags.jsx.vm
            │   └── web-index-right.jsx.vm
            └── upDown/                     # 上下布局模板
                ├── web-top-index.jsx.vm
                ├── web-index-top.jsx.vm
                └── web-top-toptags.jsx.vm
```

## 核心能力

- **严格遵循模板**：所有代码生成严格遵守 `src/template/` 目录下的 Velocity 模板，按模板变量填充，不得篡改
- **自动命名转换**：简体中文名称 → 英文标识、类名前缀
- **后端代码生成**：PO、Form、VO、Service、Controller、Mapper、Feign
- **前端代码生成**：主页、工具栏、表单、标签页、工作流
- **模板引擎**：基于Velocity语法，支持复杂模板替换
- **工作流程强制执行**：所有任务必须按工作流程的8个步骤顺序执行，不得跳过任何步骤
- **简体中文优先**：所有生成内容必须使用简体中文

## 用户输入要求

用户只需提供：
1. **新模块简体中文名称**（如：设备管理）
2. **字段明细表**

AI自动推断：
- 字段中有 `parentId` 或 `parent_id` → **Tree**（树形表）
- 否则 → **Page**（分页数据表）

外键配置（可选）：如关联EPS项目可额外说明

### 字段明细格式

| 字段名(简体中文) | 字段名(英文) | 类型 | 必填 | 列表显示 | 关联类型 | 控件说明 |
|------------|------------|------|-----|---------|---------|---------|
| 项目名称 | projectName | String | ✓ | ✓ | dict | project_status |
| 项目编号 | projectCode | String | | ✓ | | |
| 责任主体 | orgId | TreeSelect | ✓ | ✓ | org | 组织控件(OBS) |
| 责任人 | userId | Select | | ✓ | user | 用户控件(责任人) |
| 附件 | fileIds | FileUpload | | | | 上传附件 |
| 开始日期 | startDate | Date | | ✓ | | 日期筛选 |
| 结束日期 | endDate | DateTime | | | | 日期时间筛选 |
| 设备名称 | equipmentName | String | ✓ | ✓ | | |
| 设备编号 | equipmentCode | String | | ✓ | | |
| 供应商 | supplierId | Long | | | relevancy | type:2,url:/api/base/supplier |
| 采购合同 | contractId | Long | | | relevancy | type:3,url:/api/contract/select |

### 关联类型配置

| 关联类型 | 说明 | 关联配置格式 |
|---------|------|-------------|
| dict | 数据字典 | `dict:{dictType}` |
| org | 组织架构 | `org` |
| user | 用户 | `user` |
| project | 项目 | `project` |
| relevancy | 数据关联 | `relevancy:type:{1/2/3},url:{接口URL}` |

#### relevancyType 三种模式

| type值 | 说明 | 前端组件 |
|-------|------|---------|
| 1 | 枚举类型 | FormSelect + customDicts内嵌选项 |
| 2 | 远程搜索 | FormSelect + relevancySelectUrl远程数据 |
| 3 | 弹窗选择 | FormDataModel + SelectSingleModal弹窗 |

### 表类型

| 类型 | 说明 | 特征 |
|-----|------|------|
| Tree | 树形表 | 有parentId，支持父子结构 |
| Page | 分页数据表 | 支持分页查询 |
| 普通 | 普通列表 | 无分页，支持搜索 |
| **左右结构** | 左右联动布局 | 左边表格/树形 + 右边表格/树形联动 |

### 页面布局类型

| 布局类型 | 说明 | 生成文件 |
|---------|------|---------|
| **普通主页** | 单表格页面（默认） | index.jsx, TopTags/index.jsx |
| **左右布局** | 左右联动 | LeftIndex.jsx, RightIndex.jsx, TopTags/index.jsx |
| **标签页** | 多标签页 | LabelIndex.jsx, LabelTopTags/index.jsx, Labels/{tab}/index.jsx |
| **工作流** | 审批流程 | WfIndex.jsx, WfApproval.jsx |

### 布局类型自动判断

**判断规则**：

| 用户输入关键词 | 自动判断为 |
|--------------|-----------|
| 未提及"左右布局" | 普通主页 |
| 提及"左右布局"（含左边描述 + 右边描述） | 左右布局 |
| 提及"标签页"或"页签" | 标签页 |

### 标签页（页签）说明

> 详细说明请参见：[src/documents/layout-types/layout-labels.md](src/documents/layout-types/layout-labels.md)

内容包括：
- 标签页与布局的组合
- 普通主页 + 标签页图示
- 左右布局 + 标签页图示
- 联动原理
- 标签页结构
- 标签页识别特征
- 模板文件说明
- 代码组织
- SKILL 自动识别页签
- 标签页自动判断流程

### 左右结构说明

> 详细说明请参见：[src/documents/layout-types/layout-leftright.md](src/documents/layout-types/layout-leftright.md)

内容包括：
- 左右结构特点
- 联动原理
- API 设计
- 模板文件说明
- 代码组织
- 左右布局自动判断流程

## 输出结果

| 类型 | 生成文件                                                     |
|-----|----------------------------------------------------------|
| 后端-PO | XxxPo.java                                               |
| 后端-Form | XxxAddForm.java, XxxUpdateForm.java, XxxSearchForm.java  |
| 后端-VO | XxxVo.java, XxxTreeVo.java, XxxDataVo.java               |
| 后端-Service | XxxService.java, XxxServiceImpl.java                     |
| 后端-Controller | XxxController.java, XxxControllerWf.java                 |
| 后端-Mapper | XxxMapper.java, XxxMapper.xml                            |
| 前端-主页 | index.jsx                                                |
| 前端-工具栏 | TopTags/index.jsx                                        |
| 前端-表单 | AddForm.jsx, UpdateForm.jsx, SearchForm.jsx              |
| 前端-标签页 | LabelIndex.jsx, LabelTopTags.jsx, Labels/{tab}/index.jsx |
| 前端-工作流 | WfIndex.jsx, WfApproval.jsx                              |
| 前端-左右布局 | LeftIndex.jsx, RightIndex.jsx                            | 同一模块目录 |
| **数据库-初始化SQL** | db/init.sql                                       | 根据实际数据库类型生成 |

### 左右布局详细说明

> 详细内容请参见：[src/documents/layout-types/layout-leftright.md](src/documents/layout-types/layout-leftright.md)

内容包括：
- 左右结构特点
- 联动原理
- API 设计
- 模板文件说明
- 代码组织
- 左右布局自动判断流程


---

## ⚠️ 铁律：工作流程必须严格执行

**所有代码生成任务必须严格按照以下工作流程执行，不得跳过任何步骤：**

```
用户输入新模块信息
    ↓
步骤1：生成模块标识（简体中文→英文）[ ]
    ↓
步骤2：自动判断页面布局类型 [ ]
    ↓
步骤3：解析字段明细，构建模板变量 [ ]
    ↓
步骤4：替换Velocity模板变量 [ ]
    ↓
步骤5：生成后端代码（PO→Form→VO→Service→Controller→Mapper） [ ]
    ↓
步骤6：生成前端代码（根据布局类型生成对应页面） [ ]
    ↓
步骤7：生成数据库初始化SQL（根据配置的数据库类型，只生成一个SQL） [ ]
    ↓
步骤8：输出完整代码清单 [ ]
    ↓
步骤9：执行 check 检查，全部通过才能结束 [ ]
```

### TODO执行要求（强制）

**完整步骤清单**：

| 步骤 | 内容 | 状态 |
|-----|------|------|
| 步骤1 | 生成模块标识（简体中文→英文） | [ ] |
| 步骤2 | 自动判断页面布局类型 | [ ] |
| 步骤3 | 解析字段明细，构建模板变量 | [ ] |
| 步骤4 | 替换Velocity模板变量 | [ ] |
| 步骤5 | 生成后端代码（PO→Form→VO→Service→Controller→Mapper） | [ ] |
| 步骤6 | 生成前端代码（根据布局类型生成对应页面） | [ ] |
| 步骤7 | 生成数据库初始化SQL（根据配置的数据库类型） | [ ] |
| 步骤8 | 输出完整代码清单 | [ ] |
| 步骤9 | 执行 check 检查，全部通过才能结束 | [ ] |

**执行要求**：
- 每个步骤完成后标记 `[x]` 表示已执行
- 显示完整清单让用户了解全局进度
- **步骤1-3为准备阶段**，必须先完成才能进入生成阶段
- **步骤4-7为生成阶段**，必须按顺序执行，不得跳过
- **步骤8为输出阶段**，最后必须输出完整代码清单
- **步骤9为检查阶段**，必须执行 check 清单检查，全部通过才能结束
- **如步骤7未执行，SQL不会生成，必须完成所有步骤**
- **任意步骤失败，必须停止并报告错误，不得继续下一步**
- **步骤1必须将模块标识清单打印输出后，才能继续执行步骤2**
- **步骤9 check 检查必须全部通过，才能完成工作流程**

### 配置优先级

**配置来源优先级**：自然语言 > config.json

- **微服务工程**：用户可在自然语言中指定，如"在{microservice.name}中生成"
- **前端模块生成路径**：用户可在自然语言中指定，如"前端放到{frontend.path}目录下"
- **数据库类型**：用户可在自然语言中指定，如"使用Oracle数据库"
- 若用户未指定，则读取 `src/config.json` 中的默认配置

### 步骤详细说明

| 步骤 | 内容 | 输出 |
|-----|------|------|
| 步骤1 | 生成模块标识 | buildBizName, buildClassName, buildPackage, buildTableName |
| 步骤2 | 判断布局类型 | 普通主页 / 左右布局 / 标签页 / 工作流 |
| 步骤3 | 解析字段构建变量 | buildColumns, buildAddforms, buildUpdateforms, buildSearchForms |
| 步骤4 | Velocity模板替换 | 处理所有 .vm 模板文件 |
| 步骤5 | 生成后端代码 | PO, Form, VO, Service, Controller, Mapper |
| 步骤6 | 生成前端代码 | index.jsx, TopTags, AddForm, UpdateForm |
| 步骤7 | 生成SQL | 根据数据库类型生成一个SQL（init.sql） |
| 步骤8 | 输出代码清单 | 完整文件列表 + 存放路径 |
| 步骤9 | 执行 check 检查 | 全部通过才能完成工作流程 |

### 步骤1详细说明

**读取环境变量（config.json）**：
- 后台微服务名称：`{microservice.name}`
- 后台微服务工程JAVA包路径：`{microservice.package}`
- 后台微服务代码生成路径：`{microservice.path}`
- 前端模块代码生成路径：`{frontend.path}`
- 数据库类型：`{database.type}`

**生成模块标识清单**：

| 变量 | 值 | 说明 |
|-----|---|------|
| buildBizName | {模块英文名} | 模块英文名（驼峰） |
| buildClassName | {ClassName} | 类名前缀（首字母大写） |
| buildPackage | {microservice.package} | JAVA包路径 |
| buildTableName | {database.tablePrefix}{模块名} | 表名 |
| frontend | {frontend.path} | 前端模块生成路径 |
| microservice | {microservice.path} | 后端微服务生成路径 |
| databaseType | {database.type} | 数据库类型 |

**生成路径对照**：

| 类型 | 路径                                                                                                                                 |
|-----|------------------------------------------------------------------------------------------------------------------------------------|
| 后端代码 | `{microservice.path}/`                                                                                                             |
| 前端代码 | `{frontend.path}/`                                                                                                                 |
| SQL文件 | 以`{microservice.path}`中`{microservice.name}`的位置为基准，即`{microservice.path}中{microservice.name}之前的路径/{microservice.name}/db/init.sql` |

**路径计算示例**：
若`{microservice.path}` = `/Users/hadoop/.../adp-modules/wsd-aiagent/src/main/java/com/wisdom/acm/aiagent`
则`{microservice.name}` = `wsd-aiagent`出现在路径中
SQL文件 = `/Users/hadoop/.../adp-modules/wsd-aiagent/db/init.sql`

**⚠️ 重要**：步骤1必须将模块标识清单打印输出后，才能按工作流程继续执行。

**⚠️ 强制要求**：若用户输入包含繁体中文，AI必须先将其转换为简体中文，再生成代码。禁止直接使用繁体中文。

---

## 步骤9：CHECK 检查清单

**执行时机**：步骤8（输出完整代码清单）完成后，必须执行 check 检查，全部通过才能结束工作流程。

**check 检查是强制步骤**：若有任何检查项未通过，必须修复后重新检查，直到全部通过才能完成工作流程。

**检查清单来源**：根据当前生成模块的布局类型，加载对应的检查清单。不同布局类型对应不同的检查点组合。

### 示例类型与检查清单对应关系

| 示例文件 | 说明 |
|---------|------|
| example-common.md | 普通主页示例 |
| example-org.md | 组织下拉框示例 |
| example-user.md | 用户下拉框示例 |
| example-project.md | 选择项目示例 |
| example-fileupload.md | 附件上传示例 |
| example-leftright-action.md | 左右布局-普通列表 |
| example-leftright-folder.md | 左右布局-树形列表 |

### check 检查清单

| 序号 | 检查项 | 检查内容 | 标准 |
|-----|-------|---------|------|
| 1 | 包名路径 | `${buildPackage}` 是否正确 | 必须与微服务 package 一致，如 `com.wisdom.acm.aiagent` |
| 2 | 类名命名 | 所有类名是否遵循驼峰命名 | 首字母大写，如 `EquipmentPo`，方法名首字母小写如 `equipmentName` |
| 3 | 继承关系-PO | PO 是否继承 `BasePo` 或 `BaseCustomPo` | 根据 `buildEnableCustomField` 判断 |
| 4 | 继承关系-Form | Form 是否继承 `BaseForm` / `BaseSearchForm` | AddForm/UpdateForm 继承 BaseForm，SearchForm 继承 BaseSearchForm |
| 5 | 继承关系-VO | VO 是否继承 `BaseInfoVo` / `BaseVo` | Vo 继承 BaseInfoVo，DataVo 继承 BaseVo |
| 6 | 继承关系-Service | Service 是否继承 `CommService<Po>` | 类型参数只有1个（Po） |
| 7 | 继承关系-ServiceImpl | ServiceImpl 是否继承 `BaseService<Mapper, Po>` | 类型参数只有2个（Mapper, Po），不是5个 |
| 8 | 继承关系-Controller | Controller 是否继承 `BaseController` | 必须继承 BaseController |
| 9 | 关联类型-org | org 类型字段 VO 中是否为 `GeneralVo` | 如 `private GeneralVo orgId;` |
| 10 | 关联类型-user | user 类型字段 VO 中是否为 `GeneralVo` | 如 `private GeneralVo userId;` |
| 11 | 关联类型-dict | dict 类型字段 VO 中是否为 `DictionaryVo` | 如 `private DictionaryVo status;` |
| 12 | 关联类型-status | status 字段 DataVo 中是否为 `StatusVo` | 如 `private StatusVo status;` |
| 13 | 日期类型格式化 | Date 类型字段是否有 `@JsonFormat` | 必须有 `@JsonFormat(pattern = "yyyy-MM-dd")` 或 `"yyyy-MM-dd HH:mm:ss"` |
| 14 | 表名注解 | PO 类是否有 `@Table(name = "...")` | 表名必须与 `buildTableName` 一致 |
| 15 | Column注解 | PO 字段是否有 `@Column(name = "...")` | 字段名必须大写，如 `equipment_name` |
| 16 | ApiModel注解 | Form/VO 类是否有 `@ApiModel` | 值必须为中文描述，如 `设备管理` |
| 17 | ApiModelProperty注解 | 字段是否有 `@ApiModelProperty` | 值必须为中文描述 |
| 18 | Required属性 | 必填字段 `required = true` | 根据字段明细中是否必填来判断 |
| 19 | Service方法签名 | 方法签名是否符合模板 | `addXxx(AddForm)`、`updateXxx(UpdateForm)`、`deleteXxx(List<Long>)` |
| 20 | Controller注解 | 是否有 `@Api(tags = "...")` | tags 必须为中文描述 |
| 21 | Controller注入 | Service 是否用 `@Autowired` 注入 | 必须有 `@Autowired private XxxService xxxService;` |
| 22 | Mapper继承 | Mapper 是否继承 `CommMapper<Po>` | 类型参数只有1个（Po） |
| 23 | Mapper.xml | XML 声明和 DOCTYPE 是否正确 | 必须有 `<?xml version="1.0" encoding="UTF-8" ?>` 和对应 DOCTYPE |
| 24 | Mapper.xml命名空间 | namespace 是否正确 | 必须为 `${buildPackage}.mapper.${buildClassName}Mapper` |
| 25 | Mapper.xml中间为空 | mapper 标签内是否为空 | `<mapper>` 和 `</mapper>` 之间不能有内容 |
| 26 | buildColumns完整性 | 列表显示字段是否完整 | 只包含标记为"列表显示"的字段 |
| 27 | buildAddforms完整性 | 增加表单字段是否完整 | 只包含增加时需要的字段 |
| 28 | buildUpdateforms完整性 | 修改表单字段是否完整 | 包含所有可修改字段，status 字段已排除 |
| 29 | buildSearchForms完整性 | 搜索表单字段是否完整 | 只包含需要搜索的字段 |
| 30 | buildPos完整性 | PO字段是否完整 | 包含所有数据库字段 |
| 31 | Tree表类型 | Tree表是否有 parentId 字段 | 必须有 `private Long parentId;` |
| 32 | Page表类型 | Page表无 parentId | 不生成 parentId 字段 |
| 33 | ForeignKey处理 | 有外键时是否正确处理 | 有 `buildForeignKey` 时需在 Form/VO 中生成对应字段 |
| 34 | 前端import-关联 | 前端关联字段 import 是否正确 | org/user 导入 `GeneralVo`，dict 导入 `DictionaryVo` |
| 35 | 前端formType映射 | 前端组件类型是否正确 | input→FormInput，select→FormSelect，date→FormDate 等 |
| 36 | ServiceImpl-Override注解 | ServiceImpl中带有@Override注解的方法是否在Service接口中声明 | ServiceImpl中每个带有@Override注解的方法，必须在Service接口中有对应的方法声明 |

### 关联类型专项检查

| 序号 | 检查项 | 关联类型 | 检查内容 |
|----|-------|---------|---------|
| 1  | org关联-VO类型 | org | VO中org类型字段必须为 `GeneralVo` |
| 2  | org关联-前端组件 | org | 前端org类型字段必须使用 `FormTreeSelect` + `getOrgSelectTree` |
| 3  | org关联-数据加载 | org | 前端org字段必须有 `loadDatas` 加载树形数据 |
| 4  | user关联-VO类型 | user | VO中user类型字段必须为 `GeneralVo` |
| 5  | user关联-前端组件 | user | 前端user类型字段必须使用 `FormSelect` + `allSelectGeneralUser` |
| 6  | user关联-数据加载 | user | 前端user字段必须有 `url` 指定远程数据源 |
| 7  | project关联-VO类型 | project | VO中project类型字段必须为 `GeneralVo` |
| 8  | project关联-前端组件 | project | 前端project类型字段必须使用 `FormSelect` + `projectList` |
| 9  | project关联-数据加载 | project | 前端project字段必须有 `url` 指定远程数据源 |
| 10 | fileUpload关联-VO类型 | fileUpload | VO中fileUpload类型字段必须为 `String` |
| 11 | fileUpload关联-前端组件 | fileUpload | 前端fileUpload字段必须使用 `FormInputUpload` |
| 12  | fileUpload关联-import | fileUpload | 前端必须导入 `FormInputUpload` 组件 |

### 左右布局专项检查

| 序号 | 检查项 | 检查内容 |
|----|-------|---------|
| 1  | 左右布局-整体模块名 | 模块名为整体名称，如 `actionManagement`、`folderManage` |
| 2  | 左右布局-左边业务对象 | 左边业务对象独立生成，如 `ActionGroup`、`Folder` |
| 3  | 左右布局-右边业务对象 | 右边业务对象独立生成，如 `ActionInfo`、`Document` |
| 4  | 左右布局-前端同目录 | 前端代码生成到同一模块目录，如 `{frontend.path}/actionManagement/` |
| 5  | 左右布局-外键配置 | foreignKey 和 foreignTitle 必须正确配置 |
| 6  | 左右布局-左右联动 | 左边选择后，右边根据 foreignKey 过滤数据 |

### Tree表类型专项检查

| 序号 | 检查项 | 检查内容 |
|----|-------|---------|
| 1  | Tree表-parentId字段 | Tree表PO必须有 `private Long parentId;` |
| 2  | Tree表-VO-parentId | Tree表VO必须有parentId字段 |
| 3  | Tree表-树形查询方法 | Tree表Service必须有 `queryXxxTreeList` 方法 |

### check 执行流程

```
步骤8完成 → 识别示例类型 → 加载对应检查清单 → 逐项核对 → 如有未通过项 → 修复问题 → 重新 check → 全部通过 → 工作流程结束
```

### check 输出格式

**执行时机**：步骤8完成后，逐条列出检查项，每项记录文件名和检查结果。

**⚠️ 铁律**：不得少报、漏报任何检查不通过的事项，必须如实汇报给用户。

**输出结构**：按检查分类逐条检查项输出，每个分类显示检查项数统计

```markdown
## check 检查结果

### 示例类型：example-leftright-action.md（左右布局-普通列表）

### 一、基础检查

| 序号 | 检查项 | 文件 | 结果 | 说明 |
|-----|-------|------|------|------|
| 1 | 包名路径 | ActionGroupPo.java | ✅ | buildPackage=com.wisdom.acm.aiagent |
| ... | ... | ... | ... | ... |

**基础检查：36项（23项相关，13项N/A）**

### 二、关联类型专项检查

| 序号 | 检查项 | 文件 | 结果 | 说明 |
|----|-------|---------|------|------|
| 1 | project关联-VO类型 | ActionInfoVo.java | ✅ | private GeneralVo projectId; |
| ... | ... | ... | ... | ... |

**关联类型专项：3项（全部通过）**

### 三、左右布局专项检查

| 序号 | 检查项 | 文件 | 结果 | 说明 |
|----|-------|---------|------|------|
| 1 | 左右布局-整体模块名 | 前端目录 | ✅ | actionManagement |
| ... | ... | ... | ... | ... |

**左右布局专项：6项（全部通过）**
```

**重要**：
- 检查结果必须**按分类逐条检查项输出**，每个分类独立成节
- 每个分类标题后必须显示检查项数统计，格式：`{分类名}：{总项数}项（{相关项数}项相关，{N/A项数}项N/A）` 或 `（全部通过）`
- 表格中每条检查结果必须**单独一行**，便于用户事后复查
- **不得少报、漏报任何未通过的检查项**，必须如实完整列出
- 未通过项用 ❌ 标记，必须列出**问题详情**和**修复建议**
- 全部通过（100% ✅）后才能结束工作流程

### check 未通过处理

若有任何检查项未通过：
1. 列出未通过项及原因
2. 修复问题
3. 重新执行 check 检查
4. 直到全部通过才能完成工作流程

### check 参考示例

各示例文件的检查项数统计：

| 示例文件 | 说明 | 检查项数 |
|---------|------|--------|
| [example-common.md](src/documents/examples/example-common.md) | 普通主页示例 | 基础36项 |
| [example-org.md](src/documents/examples/example-org.md) | 组织下拉框示例 | 基础36项 + org关联3项 = 39项 |
| [example-user.md](src/documents/examples/example-user.md) | 用户下拉框示例 | 基础36项 + user关联3项 = 39项 |
| [example-project.md](src/documents/examples/example-project.md) | 选择项目示例 | 基础36项 + project关联3项 = 39项 |
| [example-fileupload.md](src/documents/examples/example-fileupload.md) | 附件上传示例 | 基础36项 + fileUpload关联3项 = 39项 |
| [example-leftright-action.md](src/documents/examples/example-leftright-action.md) | 左右布局-普通列表 | 基础36项 + 左右布局专项6项 = 42项 |
| [example-leftright-folder.md](src/documents/examples/example-leftright-folder.md) | 左右布局-树形列表 | 基础36项 + 左右布局专项6项 + Tree专项3项 = 45项 |

---

## Velocity模板变量详解

详细内容请参见：[src/documents/template/velocity-variables.md](src/documents/template/velocity-variables.md)

内容包括：
- 一、后端核心变量
- 二、字段集合变量（buildColumns/buildAddforms/buildPos）
- 三、关联关系变量（buildRelationList/buildRelevancyFields）
- 四、搜索相关变量（buildTextSearchForms）
- 五、前端变量
- 六、关联字段变量（rl.relation/relationName/voClassName）
- 七、前端特殊变量（codeBuilderId/column.fieldType）
- 八、功能开关变量
- 九、formType 表单控件类型

## 字段类型映射

### Java类型映射

| 表单类型 | Java类型 |
|---------|---------|
| Input | String |
| InputNumber | Integer / Long |
| TreeSelect | Long |
| Select | String |
| Date | Date |
| DateTime | Date |
| TextArea | String |
| Checkbox | String |
| Radio | String |
| FileUpload | String |

### 前端组件映射

| 表单类型 | 前端组件 |
|---------|---------|
| Input | FormInput |
| InputNumber | FormNumber |
| TreeSelect | FormTreeSelect |
| Select | FormSelect |
| Date | FormDate |
| DateTime | FormDate |
| TextArea | FormTextArea |
| Checkbox | FormCheckGroup |
| Radio | FormRadioGroup |
| FileUpload | FormInputUpload |

### 关联类型渲染

| 关联类型 | 列表渲染 | 表单渲染 |
|---------|---------|---------|
| dict | getDictNameByProject() | FormSelect |
| org | name字段 | FormTreeSelect |
| user | name字段 | FormSelect |
| project | name字段 | FormSelect |
| relevancy:1 | customDicts查找 | FormSelect |
| relevancy:2 | name字段 | FormSelect远程 |
| relevancy:3 | name字段 | FormDataModel弹窗 |

### 控件实现说明

> 详细说明请参见：[src/documents/form-controls/form-controls.md](src/documents/form-controls/form-controls.md)

内容包括：
- 控件类型映射
- Java类型映射
- 前端组件映射
- 6种控件实现说明（项目选择、用户控件、组织控件、上传附件、日期筛选）
- 通用控件导入
- 关联类型渲染

### SQL生成

> 详细说明请参见：[src/documents/sql-generator.md](src/documents/sql-generator.md)

内容包括：
- 数据库类型识别（MySQL/Oracle/达梦）
- Java类型到数据库类型映射
- 三种数据库的CREATE TABLE语句模板
- 通用字段说明
- 生成流程

## 模板约束规则

> 详细内容请参见：[src/documents/template/template-constraints.md](src/documents/template/template-constraints.md)

内容包括：
- 铁律：生成代码前必须先读取模板文件
- 约束说明（模板文件只读、槽位填充原则等）
- 常见错误：BaseService 类型参数说明
- 槽位填充要求
- mapper.xml 模板约束
- 违反约束的处理


### ⚠️ 绝对禁止：凭记忆生成代码

| 禁止行为 | 正确做法 |
|---------|---------|
| 凭记忆写import语句 | 必须读取模板文件，复制模板中的import |
| 凭经验猜测变量类型 | 必须查看模板中的变量定义 |
| 凭直觉写代码逻辑 | 必须按照模板的Velocity语法填充 |
| 跳过模板直接写代码 | 必须先读取模板，再基于模板生成 |

**错误示例**：
```java
// ❌ 错误：凭记忆写import
import com.wisdom.base.common.vo.base.GeneralVo;  // 记错了路径

// ✅ 正确：复制模板中的import
import com.wisdom.base.common.vo.GeneralVo;
```

**核心原则**：
1. **生成代码前必须先读取模板文件**，禁止根据经验生成
2. 所有import、变量、方法调用都必须来自模板
3. 若模板中有 `#if`、`#foreach` 等Velocity指令，必须正确处理
4. 不确定时必须重新读取模板确认


---

## 代码存放位置

### 普通主页/标签页/工作流

| 类型      | 路径                             | 说明         |
|---------|--------------------------------|------------|
| 后端微服务工程 | {microservice.name}/           | 后台微服务工程    |
| 后端代码    | {microservice.path}            | 后台工程代码生成路径 |
| 前端页面    | {frontend.path}/{模块英文名}/ | 前端工程代码生成路径 |

### 左右布局

详细内容请参见：[src/documents/layout-types/layout-leftright.md](src/documents/layout-types/layout-leftright.md)

### SQL输出位置

| 类型 | 路径 | 说明 |
|-----|------|------|
| SQL文件 | 以`{microservice.path}`中`{microservice.name}`的位置为基准 | 只生成一个SQL文件，根据微服务实际连接的数据库类型 |

```
# 以microservice.name在microservice.path中的位置为基准
wsd-aiagent/                      # microservice.name所在目录
├── db/
│   └── init.sql                  # Oracle初始化SQL（默认）
```

**路径计算示例**：
- 若`{microservice.path}` = `/Users/hadoop/.../adp-modules/wsd-aiagent/src/main/java/com/wisdom/acm/aiagent`
- 在`{microservice.path}`中找到`{microservice.name}` = `wsd-aiagent`的位置
- SQL文件 = `/Users/hadoop/.../adp-modules/wsd-aiagent/db/init.sql`

## 使用示例

> 详细内容请参见：[src/documents/examples/](src/documents/examples/)

SKILL 根据用户输入**自动按需加载**对应示例文件：

### 示例加载规则

| 用户输入关键词 | 加载示例文件 | 说明 |
|--------------|------------|------|
| "左右布局" + 有parentId/树形 | example-leftright-folder.md | 树形+普通列表左右布局 |
| "左右布局" + 无parentId | example-leftright-action.md | 普通列表左右布局 |
| "组织"、"责任主体"、"项目团队"、"协作团队" | example-org.md | 组织下拉框示例 |
| "用户"、"责任人"、"负责人"、"创建人"、"修改人" | example-user.md | 用户下拉框示例 |
| "附件"、"上传"、"fileUpload" | example-fileupload.md | 附件上传示例 |
| "项目"、projectId | example-project.md | 选择项目示例 |
| 默认（无上述关键词） | example-common.md | 普通主页示例 |

### 加载时机

- **步骤1完成后**（生成模块标识），根据用户输入的字段明细判断需要加载的示例
- 将示例文件内容作为上下文参考，帮助理解该类型模块的处理流程
- **不是所有示例都加载**，只加载与用户需求匹配的那一个

### 示例文件列表

```
src/documents/examples/
├── example-common.md              # 普通主页示例
├── example-org.md                 # 组织下拉框示例
├── example-user.md                # 用户下拉框示例
├── example-fileupload.md          # 附件上传示例
├── example-project.md             # 选择项目示例
├── example-leftright-action.md    # 左右布局-普通列表
└── example-leftright-folder.md    # 左右布局-树形列表
```

## 模板来源

模板来源于 `wsd-adp/src/main/resources/codebuilder/` 目录，共 **30个** .vm 模板文件：
- java/ - 后端Java模板（12个）
- web/ - 前端React模板（18个）

**重要**：模板文件禁止修改，如需调整功能请新建模板或使用配置参数。

## 变更记录

### v2.1.0 - 2026-05-16
- **新增铁律**：生成代码前必须先读取模板文件，禁止根据经验生成
- **新增说明**：明确 BaseService 类型参数为2个（Mapper, Po），不是5个
- **警告示例**：添加错误示例和正确示例对比

### v2.0.0 - 2026-05-16
- 完善 Velocity 模板变量填充规则文档
- 新增关联类型（relevancyType 1/2/3）配置说明
- 新增自定义字段、工作流开关等变量说明
- 补充字段明细表扩展字段定义
- 统一前端路径为 `{frontend.path}`
- 增加 SKILL 标准头部信息

---

### v1.0.0 - 2026-05-15
- 初始版本
- 支持生成后端 PO、Form、VO、Service、Controller、Mapper
- 支持生成前端主页、工具栏、表单

