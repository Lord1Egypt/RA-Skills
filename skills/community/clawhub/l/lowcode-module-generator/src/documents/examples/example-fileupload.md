# 附件上传示例

## 输入

```
用户：帮我生成一个"任务管理"模块，包含附件上传功能

字段明细：
| 字段名(简体中文) | 字段名(英文) | 类型 | 必填 | 列表显示 | 关联类型 |
| 任务名称 | taskName | String | ✓ | ✓ | |
| 附件 | fileIds | String | | | | fileUpload |
| 任务描述 | description | String | | | |
```

**AI自动判断**：无parentId字段 → 表类型为Page
**关联关系**：fileIds → formType = "fileUpload" → 附件上传控件

---

## 处理流程

### 1. 模块标识生成

- buildBizName = task
- buildClassName = Task
- buildPackage = {microservice.package}
- buildTableName = wsd_task

### 2. 字段集合构建

- buildColumns = [taskName, fileIds]
- buildAddforms = [taskName, fileIds]
- buildUpdateforms = [taskName, fileIds, description]
- buildSearchForms = [taskName]

### 3. 关联关系处理

- fileIds → formType = "fileUpload"
  - 前端组件：`FormInputUpload`
  - API：`POST /api/doc/file/upload`
  - 返回格式：`{id, fileName, fileUrl}`

### 4. 代码生成

- 后端：PO、Form、VO、Service、Controller、Mapper
- 前端：index、TopTags、AddForm、UpdateForm、SearchForm（fileIds 渲染为附件上传控件）

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
├── AddForm.jsx      # fileIds → FormInputUpload
├── UpdateForm.jsx    # fileIds → FormInputUpload
└── SearchForm.jsx
```

### fileIds 附件上传控件示例

**AddForm.jsx 中的 fileIds 字段**

```jsx
import {SubmitButton, ModelLayout, FormInput, FormInputUpload} from "@/components"

// fileIds 字段配置
{
  id: 'fileIds',
  label: '附件',
  type: 'fileUpload',
  allowClear: true,
}
```

**TaskVo.java 中的 fileIds 字段**

```java
/**
 * 附件
 */
@ApiModelProperty(value = "附件")
private String fileIds;
```

---

## check 检查清单

**示例类型**：example-fileupload.md（附件上传示例）

### 专项检查：fileUpload关联

| 序号 | 检查项 | 文件/位置 | 结果 | 说明 |
|----|-------|---------|------|------|
| 1  | fileUpload关联-VO类型 | TaskVo.java | ✅ 通过 | fileIds 类型必须为 `String` |
| 2  | fileUpload关联-前端组件 | AddForm.jsx/UpdateForm.jsx | ✅ 通过 | fileIds 必须使用 `FormInputUpload` |
| 3  | fileUpload关联-import | AddForm.jsx/UpdateForm.jsx | ✅ 通过 | 必须导入 `FormInputUpload` 组件 |

---

### 通用检查项

通用检查全部通过 ✅
