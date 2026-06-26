# 左右布局示例（普通列表）

## 输入

```
用户：帮我生成一个"行动管理"模块，采用左右布局

左边：行动分组（普通列表，非树形）
字段：groupName（分组名称）, sortNum（排序号）

右边：行动详情（普通分页）
字段：actionName（行动名称）, businessSystem（业务系统）, conceptCount（概念统计）, valueAttrCount（值属性统计）, relationAttrCount（关系属性统计）, groupId（所属分组）
```

**判断逻辑**：左边字段中没有 parentId → 左侧为普通列表（Page）

---

## 处理流程

### 1. 读取环境变量（config.json）

- 后台微服务名称：`{microservice.name}`
- 后台微服务工程JAVA包路径：`{microservice.package}`
- 后台微服务工程代码生成路径：`{microservice.path}`
- 前端模块代码生成路径：`{frontend.path}`
- 数据库类型：`{database.type}`

### 2. 模块标识生成

| 变量 | 值 | 说明 |
|-----|---|------|
| buildBizName | actionManagement | 模块英文名 |
| buildClassName | ActionManagement | 类名前缀 |
| buildPackage | {microservice.package} | JAVA包路径 |
| buildTableName | wsd_action_management | 表名 |
| microservice | {microservice.name} | 后台微服务名称 |
| frontend | {frontend.path} | 前端模块生成路径 |
| databaseType | {database.type} | 数据库类型 |

### 3. 业务对象拆分

- 整体模块名：actionManagement
- 左边业务对象：actionGroup（行动分组）
  - buildBizName = actionGroup
  - buildClassName = ActionGroup
  - buildTableName = wsd_action_group
  - 表类型：Page（无parentId，普通列表）
- 右边业务对象：actionInfo（行动详情）
  - buildBizName = actionInfo
  - buildClassName = ActionInfo
  - buildTableName = wsd_action_info
  - 表类型：Page（无parentId，普通分页）

### 4. 布局类型判断

- 用户输入包含"左右布局" → 自动判断为**左右布局**
- 左边：普通列表（无parentId）→ Page
- 右边：普通分页（无parentId）→ Page

### 5. 外键配置

- foreignKey = groupId（关联到左边的actionGroup.id）
- foreignTitle = 行动分组

### 6. 代码生成

**前端**（同一模块目录）：
- index.jsx（主页面）
- LeftIndex.jsx（左边列表）
- RightIndex.jsx（右边列表）
- TopTags/index.jsx（工具栏）
- ActionGroup/AddForm.jsx（新增表单）
- ActionGroup/UpdateForm.jsx（修改表单）
- ActionInfo/AddForm.jsx
- ActionInfo/UpdateForm.jsx

**后端**（同一个微服务）：
- actionGroup模块：ActionGroupPo, ActionGroupAddForm, ActionGroupUpdateForm, ActionGroupVo, ActionGroupService, ActionGroupController, ActionGroupMapper
- actionInfo模块：ActionInfoPo, ActionInfoAddForm, ActionInfoUpdateForm, ActionInfoVo, ActionInfoService, ActionInfoController, ActionInfoMapper

---

## 输出

### 后端代码目录结构（完整层次）

```
wsd-aiagent/  (微服务工程)
└── src/main/java/com/wisdom/acm/aiagent/
    ├── po/
    │   ├── ActionGroupPo.java
    │   └── ActionInfoPo.java
    ├── form/
    │   └── actionManagement/
    │       ├── actionGroup/
    │       │   ├── ActionGroupAddForm.java
    │       │   ├── ActionGroupUpdateForm.java
    │       │   └── ActionGroupSearchForm.java
    │       └── actionInfo/
    │           ├── ActionInfoAddForm.java
    │           ├── ActionInfoUpdateForm.java
    │           └── ActionInfoSearchForm.java
    ├── vo/
    │   └── actionManagement/
    │       ├── actionGroup/
    │       │   ├── ActionGroupVo.java
    │       │   └── ActionGroupDataVo.java
    │       └── actionInfo/
    │           ├── ActionInfoVo.java
    │           └── ActionInfoDataVo.java
    ├── service/
    │   ├── ActionGroupService.java
    │   ├── ActionGroupServiceImpl.java
    │   ├── ActionInfoService.java
    │   └── ActionInfoServiceImpl.java
    ├── controller/
    │   ├── ActionGroupController.java
    │   └── ActionInfoController.java
    └── mapper/
        ├── ActionGroupMapper.java
        ├── ActionGroupMapper.xml
        ├── ActionInfoMapper.java
        └── ActionInfoMapper.xml
```

### 前端代码目录结构（同一模块目录）

```
{frontend.path}/actionManagement/
├── index.jsx           # 主页面（引入左右组件）
├── LeftIndex.jsx       # 左边列表组件
├── RightIndex.jsx      # 右边列表组件
├── TopTags/
│   └── index.jsx       # 工具栏
├── ActionGroup/
│   ├── AddForm.jsx
│   └── UpdateForm.jsx
└── ActionInfo/
    ├── AddForm.jsx
    └── UpdateForm.jsx
```

### 数据库初始化SQL

```sql
-- Oracle数据库
CREATE TABLE wsd_action_group (
    id NUMBER(20) NOT NULL,
    group_name VARCHAR2(200) NOT NULL,
    sort_num NUMBER(20),
    tenant_id NUMBER(20),
    create_time DATE,
    create_user_id NUMBER(20),
    update_time DATE,
    update_user_id NUMBER(20),
    CONSTRAINT pk_wsd_action_group PRIMARY KEY (id)
);

CREATE TABLE wsd_action_info (
    id NUMBER(20) NOT NULL,
    action_name VARCHAR2(200) NOT NULL,
    business_system VARCHAR2(200),
    concept_count NUMBER(20),
    value_attr_count NUMBER(20),
    relation_attr_count NUMBER(20),
    group_id NUMBER(20),
    sort_num NUMBER(20),
    tenant_id NUMBER(20),
    create_time DATE,
    create_user_id NUMBER(20),
    update_time DATE,
    update_user_id NUMBER(20),
    CONSTRAINT pk_wsd_action_info PRIMARY KEY (id)
);
```

---

## check 检查清单

**示例类型**：example-leftright-action.md（左右布局-普通列表）

### 专项检查：左右布局

| 序号 | 检查项 | 文件/位置 | 结果 | 说明 |
|----|-------|---------|------|------|
| 1  | 左右布局-整体模块名 | 模块名 | ✅ 通过 | actionManagement（整体模块名） |
| 2  | 左右布局-左边业务对象 | ActionGroupPo等 | ✅ 通过 | ActionGroup（左边业务对象） |
| 3  | 左右布局-右边业务对象 | ActionInfoPo等 | ✅ 通过 | ActionInfo（右边业务对象） |
| 4  | 左右布局-前端同目录 | 前端代码 | ✅ 通过 | 生成到 `{frontend.path}/actionManagement/` |
| 5  | 左右布局-外键配置 | buildForeignKey | ✅ 通过 | foreignKey=groupId, foreignTitle=行动分组 |
| 6  | 左右布局-左右联动 | RightIndex.jsx | ✅ 通过 | 左边选择后，右边根据 groupId 过滤 |

---

### 通用检查项

通用检查全部通过 ✅
