# 选择项目示例

## 输入

```
用户：帮我生成一个"任务管理"模块，包含选择项目功能

字段明细：
| 字段名(简体中文) | 字段名(英文) | 类型 | 必填 | 列表显示 | 关联类型 |
| 任务名称 | taskName | String | ✓ | ✓ | |
| 所属项目 | projectId | Long | ✓ | ✓ | project |
| 任务描述 | description | String | | | |
```

**AI自动判断**：无parentId字段 → 表类型为Page
**关联关系**：projectId → relationType = "project" → 选择项目控件

---

## 处理流程

### 1. 模块标识生成

- buildBizName = task
- buildClassName = Task
- buildPackage = {microservice.package}
- buildTableName = wsd_task

### 2. 字段集合构建

- buildColumns = [taskName, projectId]
- buildAddforms = [taskName, projectId]
- buildUpdateforms = [taskName, projectId, description]
- buildSearchForms = [taskName]

### 3. 关联关系处理

- projectId → relationType = "project"
  - 前端组件：`FormSelect`
  - API：`projectList` from `@/api/api`
  - 列表渲染：`getProjectName()` 通过 projectId 查找项目名称

### 4. 代码生成

- 后端：PO、Form、VO、Service、Controller、Mapper
- 前端：index、TopTags、AddForm、UpdateForm、SearchForm（projectId 渲染为选择项目控件）

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
├── AddForm.jsx      # projectId → FormSelect + projectList
├── UpdateForm.jsx   # projectId → FormSelect + projectList
└── SearchForm.jsx
```

### projectId 选择项目控件示例

**AddForm.jsx 中的 projectId 字段**

```jsx
import {projectList} from '@/api/api'

// projectId 字段配置
{
  id: 'projectId',
  label: '所属项目',
  type: 'select',
  url: projectList,  // 选择项目控件：url 指定远程数据源
  allowClear: true,
}
```

**TaskVo.java 中的 projectId 字段**

```java
/**
 * 所属项目
 */
@ApiModelProperty(value = "所属项目")
private GeneralVo projectId;
```

---

## check 检查清单

**示例类型**：example-project.md（选择项目示例）

### 专项检查：project关联

| 序号 | 检查项 | 文件/位置 | 结果 | 说明 |
|----|-------|---------|------|------|
| 1  | project关联-VO类型 | TaskVo.java | ✅ 通过 | projectId 类型必须为 `GeneralVo` |
| 2  | project关联-前端组件 | AddForm.jsx/UpdateForm.jsx | ✅ 通过 | projectId 必须使用 `FormSelect` |
| 3  | project关联-数据加载 | AddForm.jsx/UpdateForm.jsx | ✅ 通过 | 必须有 `url: projectList` |

---

### 通用检查项

通用检查全部通过 ✅
