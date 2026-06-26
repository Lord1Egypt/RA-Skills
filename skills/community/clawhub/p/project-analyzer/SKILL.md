---
name: project-analyzer
version: 5.0.0
description: |
  SDD 软件设计文档生成器 - 基于 Harness Engineering 模式构建受控环境。
  核心理念：通过架构约束、上下文工程、反馈循环、熵管理，让 AI 在约束下高效可靠地生成文档。
  使用场景：(1) 新项目接入时生成 SDD 文档 (2) 生成开发规范 (3) 分析数据库结构 (4) 对接 Apifox 自动测试。
  支持技术栈：Java/Spring Boot、Node.js、Python、Go、React/Vue 前端项目。
metadata:
  openclaw:
    emoji: "📊"
    requires:
      bins:
        - python3
---

# Project Analyzer - SDD 软件设计文档生成器

> **Harness Engineering 核心理念**：AI 是一匹拥有神力的独角兽，力量强大但难以预测。我们不是去拔掉它的角，而是为它打造"黄金缰绳"和"水晶马车"。

## ⚠️ 关键原则：先读取，后生成（所有文档类型）

```
┌────────────────────────────────────────────────────────────────────┐
│                        文档生成流程（强制）                             │
├────────────────────────────────────────────────────────────────────┤
│                                                                    │
│  第1步: 扫描相关文件                                                │
│      ↓                                                           │
│  第2步: 【必须】逐个读取文件完整内容  ← 禁止跳过任何文件            │
│      ↓                                                           │
│  第3步: 整理提取的关键信息                                         │
│      ↓                                                           │
│  第4步: 生成文档（基于实际内容）                                     │
│      ↓                                                           │
│  第5步: 自检：对照原始文件验证文档准确性                             │
│      ↓                                                           │
│  第6步: 输出文档                                                   │
│                                                                    │
│  ⚠️ 禁止在未读取文件内容的情况下生成文档                            │
│  ⚠️ 禁止假设任何技术细节                                           │
│  ⚠️ 生成后必须对照原始文件进行自检                                 │
│                                                                    │
└────────────────────────────────────────────────────────────────────┘
```

---

## 📋 SDD 文档体系

```
docs/
├── sdd/
│   ├── 01-srs.md      # 软件需求规格说明书
│   ├── 02-sad.md      # 软件架构文档
│   ├── 03-sdd.md      # 详细设计文档
│   ├── 04-dbd.md      # 数据库设计文档
│   ├── 05-apid.md     # API 接口文档
│   └── 06-tsd.md      # 测试设计文档
└── standards/         # 开发规范
```

---

## 🔍 各文档类型的扫描规范

### 📋 SRS - 软件需求规格说明书

**必须读取的文件**：

| 文件类型 | 扫描目标 |
|----------|----------|
| README.md | 项目简介、功能概述 |
| 需求文档 | 业务需求、功能列表 |
| 接口文档 | API 列表、功能模块 |
| 用户故事 | User Story、验收标准 |

**扫描命令**：

```bash
# 1. 读取 README
cat /path/to/project/README.md

# 2. 查找需求文档
find /path/to/project -name "*.md" -path "*/docs/*" -o -name "*需求*" -o -name "*requirement*"

# 3. 查找接口定义（用于识别功能模块）
find /path/to/project -path "*/controller/*.java" -name "*Controller.java"
```

---

### 🏗️ SAD - 软件架构文档

**必须读取的文件**：

| 文件类型 | 扫描目标 |
|----------|----------|
| pom.xml / go.mod | 技术栈、依赖版本 |
| application.yml | 数据库、缓存、消息队列配置 |
| Dockerfile | 部署方式、基础镜像 |
| k8s/*.yaml | Kubernetes 部署配置 |
| README.md | 架构说明 |
| 模块目录结构 | 层级架构 |

**扫描命令**：

```bash
# 1. 读取构建配置
cat /path/to/project/pom.xml
cat /path/to/project/Dockerfile

# 2. 读取应用配置
cat /path/to/project/*/src/main/resources/application.yml
cat /path/to/project/application.yml

# 3. 读取 K8s 配置
ls -la /path/to/project/k8s/
cat /path/to/project/k8s/*.yaml

# 4. 扫描模块结构
find /path/to/project -maxdepth 3 -type d | head -50
```

**技术栈判断依据**：

| 判断依据 | 技术栈结论 |
|----------|------------|
| `<parent><artifactId>spring-boot-starter-parent</artifactId>` | Spring Boot |
| `<artifactId>spring-boot-starter-parent</artifactId><version>3.x</version>` | Spring Boot 3.x + Java 17+ |
| `<artifactId>spring-boot-starter-parent</artifactId><version>2.x</version>` | Spring Boot 2.x + Java 8/11 |
| 基础镜像 `openjdk:` | Java |
| `FROM node:` | Node.js |
| `FROM python:` | Python |
| `<artifactId>mybatis-spring-boot-starter</artifactId>` | MyBatis |
| `<artifactId>spring-boot-starter-data-jpa</artifactId>` | JPA/Hibernate |

---

### 📝 SDD - 详细设计文档

**必须读取的文件**：

| 文件类型 | 扫描目标 |
|----------|----------|
| 所有 Controller.java | 接口列表、请求参数 |
| 所有 Service.java | 业务逻辑、方法签名 |
| 所有 VO/DTO/BO.java | 数据结构 |
| 所有 Entity.java / DO.java | 数据库实体 |
| Mapper XML | SQL 语句 |
| 枚举类 | 状态码、业务常量 |

**扫描命令**：

```bash
# 1. 扫描所有 Java 源文件
find /path/to/project -name "*.java" -path "*/src/main/java/*" | wc -l

# 2. 按层级扫描
find /path/to/project -path "*/controller/*.java" -name "*.java"
find /path/to/project -path "*/service/*.java" -name "*.java"
find /path/to/project -path "*/dao/*.java" -o -path "*/mapper/*.java" | grep -i java

# 3. 读取核心类（不能只读类名，要读完整内容）
cat /path/to/project/*/service/impl/*ServiceImpl.java

# 4. 扫描枚举和常量
find /path/to/project -name "*Enum*.java" -o -name "*Constant*.java" -o -name "*Status*.java"
```

**SDD 自检清单**：

```
□ 所有 Controller 接口已读取
□ 所有 Service 实现类已读取
□ 类图中的方法签名与实际代码一致
□ 时序图中的调用关系与实际代码一致
□ 枚举值与实际代码一致
□ 没有臆造的方法或类
```

---

### 🗄️ DBD - 数据库设计文档

**必须读取的文件**：

| 文件类型 | 扫描目标 |
|----------|----------|
| 所有 *.sql 文件 | CREATE TABLE、索引、约束 |
| 所有 Entity.java / DO.java | 实体映射、字段类型 |
| 所有 Mapper.xml | SQL 语句 |
| 迁移记录 | 版本历史 |

**扫描命令**：

```bash
# 1. 查找所有 SQL 文件
find /path/to/project -name "*.sql" -type f

# 2. 查找迁移脚本目录（常见名称）
ls -la /path/to/project/db-migration/
ls -la /path/to/project/migrations/
ls -la /path/to/project/sql/
ls -la /path/to/project/scripts/

# 3. 【必须】逐个读取 SQL 文件
cat /path/to/project/db-migration/*.sql

# 4. 查找 DO/Entity 类
find /path/to/project -name "*DO.java" -o -name "*Entity.java" -o -name "*PO.java"
```

**【必须】对照验证**：

```
SQL 文件 CREATE TABLE  ←→  DO/Entity 类注解

| SQL 字段 | SQL 类型 | DO 字段 | DO 类型 |
|----------|----------|----------|---------|
| id | bigint | @TableId | Long |
| name | varchar(255) | @TableField | String |
| status | smallint | @TableField | Short |
| create_time | timestamp | @TableField | LocalDateTime |
```

**数据库类型判断**：

| 判断依据 | 数据库类型 |
|----------|----------|
| `AUTO_INCREMENT`, `ENGINE=InnoDB`, `CHARSET=` | MySQL |
| `SERIAL`, `GENERATED ALWAYS AS IDENTITY`, `::regclass` | PostgreSQL |
| `NUMBER GENERATED BY DEFAULT AS IDENTITY`, `CLOB` | Oracle |
| `IDENTITY(1,1)`, `nvarchar`, `GETDATE()` | SQL Server |

---

### 📡 APID - API 接口文档

**必须读取的文件**：

| 文件类型 | 扫描目标 |
|----------|----------|
| 所有 @RestController / @Controller | 接口定义 |
| 所有 @RequestMapping / @GetMapping / @PostMapping 等 | HTTP 方法、路径 |
| 所有 @RequestBody DTO | 请求参数 |
| 所有返回值类型 | 响应结构 |
| @Valid / @NotNull 等注解 | 参数校验规则 |
| Swagger/OpenAPI 注解 | 接口描述 |

**扫描命令**：

```bash
# 1. 扫描所有 Controller
find /path/to/project -path "*/controller/*.java" -name "*.java"

# 2. 读取所有 Controller 内容（不能只读类名）
for f in $(find /path/to/project -path "*/controller/*.java"); do
    echo "=== $f ==="
    cat "$f"
done

# 3. 扫描 DTO/请求/响应类
find /path/to/project -name "*DTO.java" -o -name "*Request.java" -o -name "*Response.java"

# 4. 扫描 Feign Client（如果有）
find /path/to/project -name "*Feign*.java" -o -name "*Client.java" | grep -i feign
```

**APID 自检清单**：

```
□ 所有 Controller 方法已读取
□ 请求参数类型与实际代码一致
□ 响应类型与实际代码一致
□ HTTP 方法（GET/POST/PUT/DELETE）与实际一致
□ 接口路径与实际代码一致
□ 参数校验注解与描述一致
□ 没有遗漏的接口
```

---

### 🧪 TSD - 测试设计文档

**必须读取的文件**：

| 文件类型 | 扫描目标 |
|----------|----------|
| pom.xml | 测试框架（JUnit 4/5/TestNG） |
| src/test/**/*.java | 现有测试用例 |
| 测试配置文件 | 测试环境配置 |
| coverage 配置 | 覆盖率要求 |

**扫描命令**：

```bash
# 1. 检查测试框架
grep -A5 "junit" /path/to/project/pom.xml
grep -A5 "testng" /path/to/project/pom.xml

# 2. 扫描测试类
find /path/to/project -path "*/test/*.java" -name "*Test.java"
find /path/to/project -path "*/test/*.java" -name "*IT.java"

# 3. 读取测试类内容
cat /path/to/project/*/src/test/java/*/*Test.java

# 4. 检查覆盖率配置
find /path/to/project -name "jacoco.xml" -o -name "coverage.xml"
```

---

## 📄 文档生成流程

### 完整流程（强制执行）

```
┌─────────────────────────────────────────────────────────────────────┐
│                          文档生成完整流程                              │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  步骤1: 接收任务                                                    │
│         "生成 xxx 项目的 SDD 文档"                                  │
│              ↓                                                       │
│  步骤2: 确定需要生成的文档类型                                       │
│         □ SRS  □ SAD  □ SDD  □ DBD  □ APID  □ TSD                │
│              ↓                                                       │
│  步骤3: 根据文档类型确定必须扫描的文件清单                            │
│              ↓                                                       │
│  步骤4: 执行扫描（必须逐个文件读取内容）                             │
│         □ 文件1 已读取                                              │
│         □ 文件2 已读取                                              │
│         □ 文件3 已读取                                              │
│              ↓                                                       │
│  步骤5: 整理提取的信息                                               │
│              ↓                                                       │
│  步骤6: 生成文档                                                    │
│              ↓                                                       │
│  步骤7: 自检（对照原始文件）                                         │
│         □ 数据准确性验证                                            │
│         □ 没有遗漏的关键信息                                         │
│         □ 没有假设或推测的内容                                       │
│              ↓                                                       │
│  步骤8: 输出文档                                                    │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### 自检验证

**每生成一个文档后，必须执行以下验证**：

```
┌─────────────────────────────────────────────────────────────────────┐
│                           自检验证清单                                │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  □ 文档中引用的所有类名、方法名、字段名与源代码一致                  │
│  □ 文档中引用的所有配置值与配置文件一致                            │
│  □ 文档中引用的所有 SQL 语句与实际 SQL 文件一致                      │
│  □ 文档中引用的所有接口路径与 Controller 一致                        │
│  □ 文档中引用的所有枚举值与枚举类一致                                │
│  □ 没有"根据经验"、"通常"、"一般"等推测性表述                       │
│  □ 所有技术版本号与实际依赖一致                                      │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## ⚙️ 扫描工具参考

### 通用扫描命令

```bash
# 统计项目规模
find /path -name "*.java" | wc -l  # Java 文件数
find /path -name "*.js" | wc -l    # JS 文件数
find /path -name "*.py" | wc -l    # Python 文件数

# 查看项目结构（深度限制）
find /path -maxdepth 4 -type d | head -100

# 查找关键配置文件
find /path -name "pom.xml" -o -name "package.json" -o -name "go.mod" -o -name "requirements.txt"
```

### Java 项目扫描

```bash
# 扫描包结构
find /path -path "*/src/main/java/*" -name "*.java" | sed 's|/[^/]*$||' | sort -u

# 统计各层文件数
echo "Controller: $(find /path -path '*/controller/*.java' | wc -l)"
echo "Service: $(find /path -path '*/service/*.java' | wc -l)"
echo "DAO/Mapper: $(find /path -path '*/dao/*.java' -o -path '*/mapper/*.java' | wc -l)"
echo "Entity/DO: $(find /path -name '*DO.java' -o -name '*Entity.java' | wc -l)"
```

### 数据库扫描

```bash
# 查找 SQL 文件
find /path -name "*.sql" -type f

# 读取 SQL 文件（批量）
for f in $(find /path -name "*.sql"); do
    echo "=== $f ==="
    cat "$f"
done
```

---

## 🎯 核心优势

| 传统方式 | 本 Skill |
|---------|---------|
| 可能跳过文件读取 | ✅ 强制读取所有文件 |
| 可能假设技术栈 | ✅ 基于文件内容判断 |
| 可能遗漏关键信息 | ✅ 完整扫描清单 |
| 无校验机制 | ✅ 自检验证 |
| 各文档标准不一 | ✅ 统一规范 |

---

## ⚠️ 错误案例及纠正

### ❌ 错误做法

```
1. 扫描到 pom.xml 就假设是 Spring Boot + MySQL
2. 看到 SQL 文件名是 init.sql 就假设是 MySQL 语法
3. 只读类名不读内容就生成类图
4. 假设某个字段是 varchar 类型
5. 根据"常见做法"推测技术选型
```

### ✅ 正确做法

```
1. 读取 pom.xml parent 标签确认 Spring Boot 版本
2. 读取 SQL 文件的 CREATE TABLE 语法确认数据库类型
3. 读取每个 Java 类的完整内容生成类图
4. 读取 DO/Entity 类的 @TableField 注解确认字段类型
5. 读取 application.yml 的 spring.datasource.url 确认数据库
```

---

## 📊 使用示例

### 完整 SDD 文档生成

```
用户: "为 D:\projects\myapp 项目生成完整 SDD 文档"

AI 执行:
1. 扫描项目结构
2. 确定需要生成：SRS + SAD + SDD + DBD + APID + TSD
3. 按类型执行扫描（见上方各文档扫描规范）
4. 对每个文档执行自检
5. 输出文档
```

### 单文档生成

```
用户: "生成数据库设计文档 DBD"

AI 执行:
1. 扫描 SQL 文件（必须逐个读取）
2. 扫描 DO/Entity 类（必须逐个读取）
3. SQL 与 DO 对照验证
4. 生成 DBD 文档
5. 自检验证
6. 输出文档
```

---

*让文档生成更可靠，每一个细节都基于实际代码 📊✨*
