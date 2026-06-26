# Velocity 模板变量详解

## 一、后端核心变量

| 变量 | 说明 | 示例                     |
|-----|------|------------------------|
| ${buildPackage} | 包名 | {microservice.package} |
| ${buildBizName} | 业务名(英文) | equipment              |
| ${buildBizCnName} | 业务名(简体中文) | 设备管理                   |
| ${buildClassName} | 类名 | Equipment              |
| ${buildUpperCaseBizName} | 大写类名 | EQUIPMENT              |
| ${buildTableName} | 表名 | wsd_equipment          |
| ${buildTableType} | 表类型 | Tree / Page / 普通       |
| ${buildForeignKey} | 外键字段名 | epsId                  |
| ${buildForeignTitle} | 外键名称 | EPS                    |

## 二、字段集合变量

### buildColumns（列表显示字段）

```java
// 每个字段包含：
title        // 字段简体中文名
className     // 驼峰字段名
classType     // Java类型(String/Integer/Long/Date/BigDecimal)
fieldName     // 数据库字段名(大写)
formType      // 表单类型(Input/InputNumber/Select/TreeSelect/Date/DateTime/TextArea/Checkbox/Radio/FileUpload)
relationType  // 关联类型(dict/org/user/relevancy)
relationValue // 关联值(字典类型/表名等)
required      // 是否必填
width         // 列宽
align         // 对齐方式
voClassName   // VO中字段名(通常去掉Id后缀)
```

### buildAddforms / buildUpdateforms / buildSearchForms

结构同 buildColumns，增加以下属性：
```java
paramEnum      // 日志参数枚举(1=普通,2=DICT枚举)
paramEnumCode  // 枚举代码
log            // 是否记录日志
defaultSearch  // 默认搜索(1)
colspan        // 表单跨列
```

### buildPos（PO实体字段）

```java
title       // 字段简体中文名
fieldName    // 数据库字段名(大写)
classType    // Java类型
className    // 驼峰字段名
```

## 三、关联关系变量

### buildRelationList（关联字段列表）

```java
relationType   // 关联类型(dict/org/user/relevancy)
relationValue   // 关联值
title          // 字段简体中文名
className      // 驼峰字段名
```

### buildRelevancyFields（数据关联字段）

当 associationType == "TABLE" 且 widgetType in ("MODEL", "SELECT") 时填充：

```java
searchFields       // 搜索字段列表 [fieldName]
searchFieldJson    // JSON数组格式 ["fieldName"]
searchFieldArrStr  // JSON字符串 "[\"fieldName\"]"
labelFormatter     // 格式化字符串 {name}
upperVoClassName   // 首字母大写
lowerVoClassName   // 首字母小写
title             // 字段简体中文名
voClassName       // 去掉Id后缀(如 userId → user)
relevancyType      // 关联类型(1/2/3)
```

### buildRelevancyServices / buildRelevancyFeigns

```java
// 服务列表（去重）
buildRelevancyServices   // ["EquipmentService"]
// Feign服务列表
buildRelevancyFeigns     // ["RelevancyApiFeign"]
```

## 四、搜索相关变量

### buildTextSearchForms / buildTextSearchFormArr

当 searchType == "LIKE" 时填充：

```java
className         // 字段名
title            // 字段简体中文名
searchValueIndex // 搜索值索引
```

## 五、前端变量

| 变量 | 说明 | 示例 |
|-----|------|------|
| ${baseUrl} | API基础路径 | api/plan/equipment |
| ${buildBizUrlName} | URL名称 | equipment |
| ${buildServiceName} | 服务名 | plan |
| ${buildBizType} | 业务类型 | equipment |
| ${addRank} | 表单列数 | 3 |
| ${addWidth} | 弹窗宽度 | 850 |

## 六、关联字段变量（buildRelationList）

关联字段是具有特殊关联类型（org/user/project/relevancy）的字段，用于生成关联 VO 对象。

### rl.relation（是否关联）

判断是否需要生成关联 VO 对象：

| 条件 | rl.relation | 说明 |
|-----|------------|------|
| widgetType = org/user/project/fileUpload/TABLE | "1" | 需要关联 VO |
| widgetType = dict | 无此字段 | 字典类型不生成关联对象 |
| 其他 | 无此字段 | 普通字段无关联 |

### rl.relationName（关联类名）

关联 VO 类的类名部分：

| widgetType | relationName | 关联VO类 |
|-----------|-------------|---------|
| org | Org | OrgVo |
| user | User | UserVo |
| project | Project | ProjectVo |
| fileUpload | File | FileVo |
| other | Xxx | XxxVo |
| TABLE关联 | General | GeneralVo |
| dict | Dictionary | DictionaryVo |

### rl.voClassName / rl.upperVoClassName（字段名）

从字段名推断的 VO 属性名（去掉 Id 后缀）：

| 字段名 | voClassName | upperVoClassName |
|-------|------------|-----------------|
| userId | user | User |
| orgId | org | Org |
| projectId | project | Project |

### rl.paramEnumCode（日志枚举）

用于 `@LogParam` 注解的日志参数枚举：

| relationType | paramEnumCode |
|-------------|---------------|
| org | ORG |
| user | USER |
| dict | DICT |
| project | 无（不记录日志） |

## 七、前端特殊变量

### ${codeBuilderId}（CRP组件标识）

**用途**：前端组件的 `tkey` 唯一标识，用于 CRP 平台识别组件

**说明**：ADP 代码生成器自动生成，AI 调用 SKILL 时可留空，CRP 平台会自动填充

**模板位置**：
- `tkey = {"index-main-${buildClassName}-${codeBuilderId}"}`
- `tkey = {"add-form-${buildClassName}-${codeBuilderId}"}`
- `tkey = {"update-form-${buildClassName}-${codeBuilderId}"}`

### ${column.fieldType}（列表日期类型）

**用途**：列表中日期类型字段判断，小写 `date` 用于前端条件渲染

**来源**：DevPropertyPo.getFieldType() 转为小写

**模板用法**：
```velocity
#elseif(${column.fieldType} == 'date')
    // 日期格式化处理
```

## 八、功能开关变量

| 变量 | 说明 | 填充条件 |
|-----|------|---------|
| ${buildEnableCustomField} | 启用自定义字段 | customField == 1 |
| ${buildEnableWf} | 启用工作流 | enableWf != "none" 且有status字段 |
| ${buildHasEnableWorkflow} | 工作流开关 | 同上 |
| ${buildWfType} | 工作流类型 | pagePo.getWfType() |
| ${showClassifyGroup} | 分类码分组 | 页面配置 |

## 九、formType 表单控件类型

formType 决定前端表单组件渲染方式，来源于字段的 widgetType 或 fieldType。

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

**模板用途**：vo.java.vm 用于判断日期类型字段

```velocity
#elseif(${column.formType} == 'Date')
    #set($vmFormItemType = "FormDate")
#elseif(${column.formType} == 'DateTime')
    #set($vmFormItemType = "FormDate")
```
