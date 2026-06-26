# 组织下拉框示例

## 输入

```
用户：帮我生成一个"任务管理"模块，包含组织控件

字段明细：
| 字段名(简体中文) | 字段名(英文) | 类型 | 必填 | 列表显示 | 关联类型 |
| 任务名称 | taskName | String | ✓ | ✓ | |
| 责任主体 | orgId | Long | ✓ | ✓ | org |
| 任务描述 | description | String | | | |
```

**AI自动判断**：无parentId字段 → 表类型为Page
**关联关系**：orgId → relationType = "org" → 组织下拉框控件
**别名说明**：组织控件也称为"责任主体"、"项目团队"、"协作团队"等

---

## 处理流程

### 1. 模块标识生成

- buildBizName = task
- buildClassName = Task
- buildPackage = {microservice.package}
- buildTableName = wsd_task

### 2. 字段集合构建

- buildColumns = [taskName, orgId]
- buildAddforms = [taskName, orgId]
- buildUpdateforms = [taskName, orgId, description]
- buildSearchForms = [taskName]

### 3. 关联关系处理

- orgId → relationType = "org"
  - 前端组件：`FormTreeSelect`
  - API：`homeExt.getOrgSelectTree(callback)`
  - 列表渲染：组织名称字段

### 4. 代码生成

- 后端：PO、Form、VO、Service、Controller、Mapper
- 前端：index、TopTags、AddForm、UpdateForm、SearchForm（orgId 渲染为组织下拉框控件）

---

## 输出

### 后端代码目录结构（完整层次）

```
wsd-aiagent/  (微服务工程)
└── src/main/java/com/wisdom/acm/aiagent/
    ├── po/
    │   └── TaskPo.java
    ├── form/
    │   └── task/
    │       ├── TaskAddForm.java
    │       ├── TaskUpdateForm.java
    │       └── TaskSearchForm.java
    ├── vo/
    │   └── task/
    │       ├── TaskVo.java
    │       ├── TaskDataVo.java
    │       └── TaskTreeVo.java
    ├── service/
    │   ├── TaskService.java
    │   └── impl/
    │       └── TaskServiceImpl.java
    ├── controller/
    │   └── TaskController.java
    └── mapper/
        ├── TaskMapper.java
        └── TaskMapper.xml
```

### 前端代码结构

```
{frontend.path}/task/
├── index.jsx
├── TopTags/
│   └── index.jsx
├── AddForm.jsx      # orgId → FormTreeSelect + getOrgSelectTree
├── UpdateForm.jsx    # orgId → FormTreeSelect + getOrgSelectTree
└── SearchForm.jsx
```

### orgId 组织下拉框控件示例

**AddForm.jsx 中的 orgId 字段**

```jsx
// orgId 字段配置
{
  id: 'orgId',
  label: '责任主体',
  type: 'treeSelect',
  loadDatas: (callback) => { homeExt.getOrgSelectTree(callback) },  // 组织控件：loadDatas 指定树形数据源
  allowClear: true,
}
```

**TaskVo.java 中的 orgId 字段**

```java
/**
 * 责任主体
 */
@ApiModelProperty(value = "责任主体")
private GeneralVo orgId;
```

---

## check 检查清单

**示例类型**：example-org.md（组织下拉框示例）

### 专项检查：org关联

| 序号 | 检查项 | 文件/位置 | 结果 | 说明 |
|----|-------|---------|------|------|
| 1  | org关联-VO类型 | TaskVo.java | ✅ 通过 | orgId 类型必须为 `GeneralVo` |
| 2  | org关联-前端组件 | AddForm.jsx/UpdateForm.jsx | ✅ 通过 | orgId 必须使用 `FormTreeSelect` |
| 3  | org关联-数据加载 | AddForm.jsx/UpdateForm.jsx | ✅ 通过 | 必须有 `loadDatas: (callback) => { homeExt.getOrgSelectTree(callback) }` |

---

### 通用检查项

通用检查全部通过 ✅
