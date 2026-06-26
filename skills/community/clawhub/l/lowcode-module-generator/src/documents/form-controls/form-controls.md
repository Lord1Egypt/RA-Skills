# 表单控件类型

formType 决定前端表单组件渲染方式，来源于字段的 widgetType 或 fieldType。

## 控件类型映射

| widgetType | formType | 前端组件 | 说明 |
|-----------|----------|---------|------|
| input | input | FormInput | 文本输入 |
| select | select | FormSelect | 下拉选择 |
| treeSelect | treeSelect | FormTreeSelect | 树形选择 |
| date | date | FormDate | 日期选择 |
| dateTime | dateTime | FormDate | 日期时间选择 |
| fileUpload | fileUpload | FormInputUpload | 文件上传 |
| number | number | FormNumber | 数字输入 |
| textArea | textArea | FormTextArea | 多行文本 |
| checkbox | checkbox | FormCheckGroup | 多选 |
| radio | radio | FormRadioGroup | 单选 |

## Java类型映射

| formType | Java类型 |
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

## 前端组件映射

| formType | 前端组件 |
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

---

## 控件实现说明

### 1. 选择项目控件（relationType=project）

| 项目 | 说明 |
|-----|------|
| 后端API | `GET /api/plan/project/list` |
| 前端API | `projectList` from `@/api/api` |
| 组件 | FormSelect |
| 返回格式 | `[{id, name}, ...]` |

```velocity
#elseif(${column.relationType} == 'project')
    url = {projectList}
```

### 2. 用户控件（relationType=user/wf2User）

| 项目 | 说明 |
|-----|------|
| 别名 | 责任人、负责人 |
| 后端API | `GET /api/sys/user/general/select/list` |
| 前端API | `allSelectGeneralUser` from `@/api/api` |
| 组件 | FormSelect |
| 返回格式 | `[{id, name}, ...]` |

```velocity
#elseif(${column.relationType} == 'user' || ${column.relationType} == 'wf2User')
    url = {allSelectGeneralUser}
```

### 3. 组织控件（relationType=org）

| 项目 | 说明 |
|-----|------|
| 别名 | 责任主体、OBS、协作团队、项目团队 |
| 后端API | `GET /api/sys/org/select/tree` |
| 前端调用 | `homeExt.getOrgSelectTree(callback)` |
| 组件 | FormTreeSelect |
| 返回格式 | `[{id, name, children: [...]}, ...]` |

```velocity
#elseif(${column.relationType} == 'org')
    loadDatas={(callback) => { homeExt.getOrgSelectTree(callback) }}
```

### 4. 上传附件控件（formType=FileUpload）

| 项目 | 说明 |
|-----|------|
| 后端API | `POST /api/doc/file/upload` |
| 组件 | FormInputUpload |
| 参数 | multipartFile |
| 返回格式 | `{id, fileName, fileUrl}` |

```velocity
#elseif(${column.formType} == 'FileUpload')
    #set($vmFormItemType = "FormInputUpload")
```

### 5. 日期筛选控件（formType=Date/DateTime）

| 项目 | 说明 |
|-----|------|
| 后端处理 | Date类型直接接收 |
| 组件 | FormDate |
| 格式化 | `dataUtil.Dates().formatTimeString()` |

```velocity
#elseif(${column.formType} == 'Date')
    #set($vmFormItemType = "FormDate")
#elseif($column.formType == 'DateTime')
    #set($vmFormItemType = "FormDate")
```

---

## 通用控件导入

所有表单组件统一从 `@/components` 导入：

```jsx
import {SubmitButton,ModelLayout,ModelContent,ModelFooter,FormInput,
    FormSelect,FormTreeSelect,FormDate,FormCheckGroup,FormRadioGroup,
    FormNumber,FormTextArea,FormInputUpload,FormDataModel,SelectSingleModal,BaseForm} from "@/components"
```

API方法从 `@/api/api` 导入：

```jsx
import {allSelectGeneralUser,projectList} from '@/api/api'
```

---

## 关联类型渲染

| 关联类型 | 列表渲染 | 表单渲染 |
|---------|---------|---------|
| dict | getDictNameByProject() | FormSelect |
| org | name字段 | FormTreeSelect |
| user | name字段 | FormSelect |
| project | name字段 | FormSelect |
| relevancy:1 | customDicts查找 | FormSelect |
| relevancy:2 | name字段 | FormSelect远程 |
| relevancy:3 | name字段 | FormDataModel弹窗 |