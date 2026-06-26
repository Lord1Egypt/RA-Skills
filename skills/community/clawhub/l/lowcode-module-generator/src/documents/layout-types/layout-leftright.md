# 左右布局

左右结构是一种常见的联动布局模式：

## 特点

- 左边为列表（表格或树形），显示主数据
- 右边为详情表格/树形，根据左边选中行联动显示
- 左边点击一行后，右边显示该行关联的子数据
- 通过 `foreignKey`（外键）实现左右联动

## 联动原理

```
左边选中行 → 触发 setForeignKey(record.id) → 右边刷新数据
```

## API 设计

- 左边列表：`GET /api/{service}/{leftBizName}/list` 或 `/tree`
- 右边列表：`GET /api/{service}/{rightBizName}/{foreignKey}/{pageSize}/{pageNum}/list`
- 右边树形：`GET /api/{service}/{rightBizName}/{foreignKey}/tree`

## 模板文件

| 文件 | 说明 |
|-----|------|
| web-left-index.jsx.vm | 左边主页（表格/树形） |
| web-index-right.jsx.vm | 右边主页（联动表格/树形） |
| web-left-toptags.jsx.vm | 左边工具栏 |

## 代码组织

### 前端代码（同一模块目录）

左右布局的前端代码生成到**同一模块目录下**：
```
{frontend.path}/{模块名}/
├── index.jsx          # 主页面（引入左右组件）
├── LeftIndex.jsx       # 左边组件
├── RightIndex.jsx     # 右边组件
└── TopTags/
    └── index.jsx      # 工具栏组件
```

### 后端代码（生成到{microservice.path}）

左右布局的后端对应**两个业务对象**，生成到{microservice.path}，是两个不同的业务对象类。

**重要**：
1. 左右布局的前端代码生成到**同一模块目录**
2. 左右布局的后端代码生成到{microservice.path}，是两个不同的业务对象类
3. 不是每个业务对象创建一个新的微服务，两个业务对象都生成到{microservice.path}里，是两个不同的业务对象类
4. 如果对应的{microservice.path}不存在，报错给用户并且流程中止

```
{microservice}/           # 环境变量的微服务
    └── src/main/java/com/wisdom/acm/
        ├── po/
        │   ├── FolderPo.java          # 左边业务对象PO
        │   └── DocumentPo.java        # 右边业务对象PO
        ├── vo/
        │   ├── folder/
        │   │   ├── FolderVo.java
        │   │   └── FolderTreeVo.java
        │   └── document/
        │       └── DocumentVo.java
        ├── form/
        │   ├── folder/
        │   │   ├── FolderAddForm.java
        │   │   └── FolderUpdateForm.java
        │   └── document/
        │       ├── DocumentAddForm.java
        │       └── DocumentUpdateForm.java
        ├── service/
        │   ├── FolderService.java
        │   ├── DocumentService.java
        │   └── impl/
        │       ├── FolderServiceImpl.java
        │       └── DocumentServiceImpl.java
        ├── controller/
        │   ├── FolderController.java
        │   └── DocumentController.java
        └── mapper/
            ├── FolderMapper.java
            ├── FolderMapper.xml
            ├── DocumentMapper.java
            └── DocumentMapper.xml
```

## 左右布局自动判断流程

当用户输入包含"左右布局"描述时，自动进入此流程：

```
步骤3a：解析左右布局描述
    - 提取左边描述 → 确定左边业务对象和类型（表格/树形）
    - 提取右边描述 → 确定右边业务对象和类型（表格/树形）
    ↓
步骤3b：判断表类型（根据parentId字段）
    - 左边字段中包含parentId → 左侧为Tree（树形）
    - 左边字段中无parentId → 左侧为Page（普通列表）
    - 右边字段中包含parentId → 右侧为Tree
    - 右边字段中无parentId → 右侧为Page
    ↓
步骤3c：确认外键配置
    - foreignKey：外键字段名（如 groupId、folderId）
    - foreignTitle：外键名称（如 行动分组、文件夹）
    ↓
步骤3d：生成联动代码
    - 前端：生成到同一模块目录下（LeftIndex + RightIndex）
    - 后端：分别生成到{microservice.path}（左边业务对象 + 右边业务对象）,是两个不同的业务对象类
    - 左边模板：web-left-index.jsx.vm（调用 setForeignKey）
    - 右边模板：web-index-right.jsx.vm（接收 foreignKey 联动刷新）
    - 工具栏：TopTags/index.jsx（公共操作按钮）
```

## 表类型判断规则

| 判断条件 | 表类型 | 生成文件 |
|---------|-------|---------|
| 字段中**有**parentId | Tree | TreeVo, 树形组件 |
| 字段中**无**parentId | Page | DataVo, 分页组件 |

**重要**：左右布局的每一侧独立判断表类型，不是整个模块统一判断。
