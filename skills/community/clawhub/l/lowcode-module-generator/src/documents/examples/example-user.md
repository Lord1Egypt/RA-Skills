# 用户下拉框示例

## 输入

```
用户：帮我生成一个"任务管理"模块，包含选择用户功能

字段明细：
| 字段名(简体中文) | 字段名(英文) | 类型 | 必填 | 列表显示 | 关联类型 |
| 任务名称 | taskName | String | ✓ | ✓ | |
| 负责人 | userId | Long | ✓ | ✓ | user |
| 任务描述 | description | String | | | |
```

**AI自动判断**：无parentId字段 → 表类型为Page
**关联关系**：userId → relationType = "user" → 用户下拉框控件
**别名说明**：用户控件也称为"责任人"、"创建人"、"修改人"等

---

## 处理流程

### 1. 模块标识生成

- buildBizName = task
- buildClassName = Task
- buildPackage = {microservice.package}
- buildTableName = wsd_task

### 2. 字段集合构建

- buildColumns = [taskName, userId]
- buildAddforms = [taskName, userId]
- buildUpdateforms = [taskName, userId, description]
- buildSearchForms = [taskName]

### 3. 关联关系处理

- userId → relationType = "user"
  - 前端组件：`FormSelect`
  - API：`allSelectGeneralUser` from `@/api/api`
  - 列表渲染：`getUserName()` 通过 userId 查找用户名称

### 4. 代码生成

- 后端：PO、Form、VO、Service、Controller、Mapper
- 前端：index、TopTags、AddForm、UpdateForm、SearchForm（userId 渲染为用户下拉框控件）

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
├── AddForm.jsx      # userId → FormSelect + allSelectGeneralUser
├── UpdateForm.jsx    # userId → FormSelect + allSelectGeneralUser
└── SearchForm.jsx
```

### userId 用户下拉框控件示例

**AddForm.jsx 中的 userId 字段**

```jsx
import {allSelectGeneralUser} from '@/api/api'

// userId 字段配置
{
  id: 'userId',
  label: '负责人',
  type: 'select',
  url: allSelectGeneralUser,  // 用户下拉框控件：url 指定远程数据源
  allowClear: true,
}
```

**TaskVo.java 中的 userId 字段**

```java
/**
 * 负责人
 */
@ApiModelProperty(value = "负责人")
private GeneralVo userId;
```

---

## check 检查清单

**示例类型**：example-user.md（用户下拉框示例）

### 专项检查：user关联

| 序号 | 检查项 | 文件/位置 | 结果 | 说明 |
|----|-------|---------|------|------|
| 1  | user关联-VO类型 | TaskVo.java | ✅ 通过 | userId 类型必须为 `GeneralVo` |
| 2  | user关联-前端组件 | AddForm.jsx/UpdateForm.jsx | ✅ 通过 | userId 必须使用 `FormSelect` |
| 3  | user关联-数据加载 | AddForm.jsx/UpdateForm.jsx | ✅ 通过 | 必须有 `url: allSelectGeneralUser` |

---

### 通用检查项

通用检查全部通过 ✅
