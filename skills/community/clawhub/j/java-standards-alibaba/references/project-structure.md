# 工程结构

> 来源: Java开发手册（嵩山版）— 六、工程结构

## (一) 应用分层

### 【推荐】分层结构

| 层 | 说明 |
|---|------|
| **开放 API 层** | 封装 Service 为 RPC/http 接口，网关控制 |
| **终端显示层** | velocity/JS/JSP/移动端模板渲染 |
| **Web 层** | 访问控制转发，参数校验，简单业务处理 |
| **Service 层** | 具体业务逻辑 |
| **Manager 层** | 第三方平台封装、Service 能力下沉、多 DAO 组合 |
| **DAO 层** | 与 MySQL/Oracle/Hbase 等数据交互 |
| **第三方服务** | 其它部门 RPC、基础平台、外部 HTTP 接口 |
| **外部数据接口** | 数据迁移场景中的外部存储服务 |

### 【参考】分层异常处理

- **DAO 层**: `catch(Exception e)` → `throw new DAOException(e)`，不打印日志
- **Service 层**: 必须记录出错日志到磁盘，带参数信息
- **Manager 层**: 与 Service 同机部署则同 DAO，单独部署同 Service
- **Web 层**: 不往上抛异常，跳转到友好错误页面
- **开放接口层**: 处理成错误码和错误信息返回

### 【参考】分层领域模型

| 模型 | 说明 |
|------|------|
| **DO** | 与数据库表一一对应，DAO 层上传 |
| **DTO** | Service/Manager 向外传输 |
| **BO** | Service 层输出的业务逻辑封装 |
| **Query** | 数据查询对象，超过 2 参数禁止用 Map 传输 |
| **VO** | Web 向模板渲染引擎传输 |

---

## (二) 二方库依赖

### 【强制】规则

### 1. GAV 规则

- **GroupID**: `com.{公司/BU}.业务线[.子业务线]`，最多 4 级
- **ArtifactID**: `产品线名-模块名`
- **Version**: 主版本号.次版本号.修订号

### 2. 版本号语义

| 版本段 | 含义 |
|--------|------|
| 主版本号 | 产品方向改变，大规模 API 不兼容 |
| 次版本号 | 增加主要功能，极小 API 不兼容 |
| 修订号 | 修复 BUG、新增次要功能 |

> **说明**: 起始版本号必须为 `1.0.0`，不是 `0.0.1`。

### 3. 线上不依赖 SNAPSHOT

安全包除外。RELEASE 版本号有延续性，不允许覆盖升级。

### 4. 依赖升级仲裁不变

升级时进行 `dependency:resolve` 前后比对，不一致时用 `dependency:tree` 找出差异点。

### 5. 接口返回值不用枚举

参数可以使用枚举，但返回值不允许使用枚举或包含枚举的 POJO。

### 6. 统一定义版本变量

> **正例**: `${spring.version}` 统一版本。

### 7. 禁止相同 GAV 不同 Version

子项目 pom 中出现相同 GroupId+ArtifactId 但不同 Version，线下正确线上故障。

### 【推荐】

### 8. 谨慎引入第三方

底层基础技术框架、核心数据管理平台谨慎引入。

### 9. dependencies vs dependencyManagement

- `<dependencies>`: 自动引入，被子项目继承
- `<dependencyManagement>`: 仅声明版本，子项目需显式声明

### 10. 二方库无配置项

### 11. 不用不稳定工具包

### 【参考】

### 12. 二方库发布原则

- 精简可控: 移除不必要 API 和依赖
- 稳定可追溯: 版本变化可记录，维护者可追溯

---

## (三) 服务器

### 【推荐】规则

### 1. 调小 time_wait

> **正例**: `net.ipv4.tcp_fin_timeout = 30`

### 2. 调大最大文件句柄数

并发连接数大时 fd 不足会报 "open too many files"。

### 3. JVM OOM Dump

`-XX:+HeapDumpOnOutOfMemoryError`

### 4. JVM Xms = Xmx

避免 GC 后调整堆大小带来的压力。

### 【参考】

### 5. 重定向

内部用 `forward`，外部用 URL Broker 生成。
