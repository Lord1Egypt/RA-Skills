# 左右布局示例（树形 + 普通列表）

## 输入

```
用户：帮我生成一个"文件夹管理"模块，采用左右布局

左边：文件夹树形列表
字段：folderName（文件夹名称）, parentId（父文件夹）, sortNum（排序号）

右边：文件夹下的文档列表
字段：docName（文档名称）, folderId（所属文件夹）, docType（文档类型）, createTime（创建时间）
```

**判断逻辑**：左边字段中有 parentId → 左侧为树形结构（Tree）

---

## 处理流程

### 1. 读取环境变量（config.json）

- 后台微服务名称：`{microservice.name}`
- 后台微服务工程JAVA包路径：`{microservice.package}`
- 后台微服务工程代码生成路径：`{microservice.path}`
- 前端模块代码生成路径：`{frontend.path}`
- 数据库类型：`{database.type}`

### 2. 模块标识生成清单

| 变量 | 值 | 说明 |
|-----|---|------|
| buildBizName | folderManage | 模块英文名 |
| buildClassName | FolderManage | 类名前缀（首字母大写） |
| buildPackage | {microservice.package} | JAVA包路径 |
| buildTableName | wsd_folder_manage | 表名 |
| microservice | {microservice.name} | 后台微服务名称 |
| frontend | {frontend.path} | 前端模块生成路径 |
| databaseType | {database.type} | 数据库类型 |

### 3. 业务对象拆分

- 整体模块名：folderManage
- 左边业务对象：folder（文件夹）
  - buildBizName = folder
  - buildClassName = Folder
  - buildTableName = wsd_folder
  - 表类型：Tree（有parentId）
- 右边业务对象：document（文档）
  - buildBizName = document
  - buildClassName = Document
  - buildTableName = wsd_document
  - 表类型：Page

### 4. 布局类型判断

- 用户输入包含"左右布局" → 自动判断为**左右布局**
- 左边：树形结构（有parentId）→ Tree
- 右边：列表结构 → Page

### 5. 外键配置

- foreignKey = folderId
- foreignTitle = 文件夹

### 6. 代码生成

**前端**（同一模块目录）：
- index.jsx（主页面）
- LeftIndex.jsx（左边树形）
- RightIndex.jsx（右边列表）
- TopTags/index.jsx（工具栏）

**后端**（同一个微服务）：
- folder模块：FolderPo, FolderAddForm, FolderUpdateForm, FolderVo, FolderTreeVo, FolderService, FolderServiceImpl, FolderController, FolderMapper, FolderMapper.xml
- document模块：DocumentPo, DocumentAddForm, DocumentUpdateForm, DocumentVo, DocumentService, DocumentServiceImpl, DocumentController, DocumentMapper, DocumentMapper.xml

---

## 输出

### 后端代码目录结构（完整层次）

```
wsd-aiagent/  (微服务工程)
└── src/main/java/com/wisdom/acm/aiagent/
    ├── po/
    │   ├── FolderPo.java
    │   └── DocumentPo.java
    ├── form/
    │   └── folderManage/
    │       ├── folder/
    │       │   ├── FolderAddForm.java
    │       │   ├── FolderUpdateForm.java
    │       │   └── FolderSearchForm.java
    │       └── document/
    │           ├── DocumentAddForm.java
    │           ├── DocumentUpdateForm.java
    │           └── DocumentSearchForm.java
    ├── vo/
    │   └── folderManage/
    │       ├── folder/
    │       │   ├── FolderVo.java
    │       │   ├── FolderTreeVo.java
    │       │   └── FolderDataVo.java
    │       └── document/
    │           ├── DocumentVo.java
    │           └── DocumentDataVo.java
    ├── service/
    │   ├── FolderService.java
    │   ├── FolderServiceImpl.java
    │   ├── DocumentService.java
    │   └── DocumentServiceImpl.java
    ├── controller/
    │   ├── FolderController.java
    │   └── DocumentController.java
    └── mapper/
        ├── FolderMapper.java
        ├── FolderMapper.xml
        ├── DocumentMapper.java
        └── DocumentMapper.xml
```

### 前端代码目录结构（同一模块目录）

```
{frontend.path}/folderManage/
├── index.jsx           # 主页面（引入左右组件）
├── LeftIndex.jsx       # 左边树形组件
├── RightIndex.jsx      # 右边列表组件
├── TopTags/
│   └── index.jsx       # 工具栏
├── Folder/
│   ├── AddForm.jsx
│   └── UpdateForm.jsx
└── Document/
    ├── AddForm.jsx
    └── UpdateForm.jsx
```

### 数据库初始化SQL

```sql
-- Oracle数据库
CREATE TABLE wsd_folder (
    id NUMBER(20) NOT NULL,
    folder_name VARCHAR2(200) NOT NULL,
    parent_id NUMBER(20),
    sort_num NUMBER(20),
    tenant_id NUMBER(20),
    create_time DATE,
    create_user_id NUMBER(20),
    update_time DATE,
    update_user_id NUMBER(20),
    CONSTRAINT pk_wsd_folder PRIMARY KEY (id)
);

CREATE TABLE wsd_document (
    id NUMBER(20) NOT NULL,
    doc_name VARCHAR2(200) NOT NULL,
    folder_id NUMBER(20),
    doc_type VARCHAR2(50),
    create_time DATE,
    sort_num NUMBER(20),
    tenant_id NUMBER(20),
    create_user_id NUMBER(20),
    update_time DATE,
    update_user_id NUMBER(20),
    CONSTRAINT pk_wsd_document PRIMARY KEY (id)
);
```

---

## check 检查清单

**示例类型**：example-leftright-folder.md（左右布局-树形列表）

### 专项检查：左右布局

| 序号 | 检查项 | 文件/位置 | 结果 | 说明 |
|----|-------|---------|------|------|
| 1  | 左右布局-整体模块名 | 模块名 | ✅ 通过 | folderManage（整体模块名） |
| 2  | 左右布局-左边业务对象 | FolderPo等 | ✅ 通过 | Folder（左边业务对象，树形） |
| 3  | 左右布局-右边业务对象 | DocumentPo等 | ✅ 通过 | Document（右边业务对象） |
| 4  | 左右布局-前端同目录 | 前端代码 | ✅ 通过 | 生成到 `{frontend.path}/folderManage/` |
| 5  | 左右布局-外键配置 | buildForeignKey | ✅ 通过 | foreignKey=folderId, foreignTitle=文件夹 |
| 6  | 左右布局-左右联动 | RightIndex.jsx | ✅ 通过 | 左边选择后，右边根据 folderId 过滤 |

### 专项检查：Tree表类型

| 序号 | 检查项 | 文件/位置 | 结果 | 说明 |
|----|-------|---------|------|------|
| 1  | Tree表-parentId字段 | FolderPo.java | ✅ 通过 | 必须有 `private Long parentId;` |
| 2  | Tree表-VO-parentId | FolderVo.java | ✅ 通过 | VO中必须包含parentId字段 |
| 3  | Tree表-树形查询方法 | FolderService.java | ✅ 通过 | 必须有 `queryFolderTreeList` 方法 |

---

### 通用检查项

通用检查全部通过 ✅
