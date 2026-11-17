---
name: link-skills
description: >-
  Link 产品全链路开发技能，覆盖需求分析、方案设计（技术方案/数据库设计/接口设计）、
  编码开发（基于 link 标准）、测试部署上线、后续运维的完整生命周期。
  适用于工作目录 D:\develop\code\cdfai 下的 link CRM+AI 微服务系统。
  当用户需要为 link 项目开发新功能、设计接口、修改代码、排查问题、部署上线或进行运维操作时触发此技能。
  关键词：link开发、link接口、link部署、link运维、CRM开发、AI助手开发、知识库开发、企微同步、微服务开发。
---

# Link 产品全链路开发技能

## 技能概述

本技能为 link CRM+AI 企业级微服务系统提供全生命周期开发指导。link 系统基于 Java 8 + Spring Boot 2.1 + Spring Cloud Greenwich 构建，包含 8 个微服务模块，覆盖 CRM 业务、AI 助手、认证授权、API 网关等核心能力。

## 适用场景

- 为 link 系统开发新功能模块（CRM 业务、AI 助手、知识库等）
- 设计新接口或修改现有接口
- 数据库表设计与变更
- 代码编写与审查（需遵循 link 编码规范）
- 测试验证与部署上线
- 线上问题排查与运维操作
- 企微/微信集成开发
- AI 能力集成（Coze、火山引擎 HiAgent）

## 项目快速索引

| 维度 | 内容 |
|------|------|
| 工作目录 | `D:\develop\code\cdfai` |
| 技术栈 | Java 8 + Spring Boot 2.1.2 + Spring Cloud Greenwich |
| 微服务模块 | link-ai、link-base、link-auth、link-gateway、link-config、link-log、link-login、link-register |
| 数据库 | MySQL 8.0.30（linkbase + linkadmin）、ClickHouse（linkloyalty）、Redis、ES 7.16.3 |
| ORM | MyBatis（link-core 封装 BasicMapper） |
| API 网关 | Spring Cloud Gateway，前缀 `/linkcrm/` |
| 配置中心 | Apollo（AppID: cdfai-link-ai） |
| 部署 | Docker + Kubernetes + Helm |
| 私有框架 | link-core 1.5.95-RELEASE（BasicController/BasicService/BasicModel） |

## 全链路工作流

收到 link 开发需求后，按以下五阶段顺序执行。每个阶段产出作为下一阶段输入。

### 阶段一：需求分析

**目标**：明确需求边界、验收标准和影响范围。

**执行步骤**：

1. 解析需求，确定涉及的模块（link-ai / link-base / link-gateway 等）
2. 识别需求类型：
   - 新功能开发 → 需完整走五阶段
   - 接口新增/修改 → 重点关注阶段二、三
   - Bug 修复 → 跳至阶段三（定位+修复），再走阶段四验证
   - 运维操作 → 直接走阶段五
3. 确认验收标准（功能点清单、接口契约、性能要求）
4. 评估影响范围（涉及哪些模块、表、接口、配置）
5. 识别约束条件（link-core 框架限制、Checkstyle 规范、签名过滤器等）

**产出**：需求分析摘要（需求描述 + 验收标准 + 影响范围 + 约束条件）

**参考文档**：加载 `references/project-architecture.md` 了解模块划分和技术栈

### 阶段二：方案设计

**目标**：完成技术方案、数据库设计和接口设计。

#### 2.1 技术方案设计

1. 确定功能归属模块（按业务域划分）
2. 设计分层架构：Controller → Service → DAO(MyBatis) → Model
3. 识别跨服务调用需求（Feign 客户端）
4. 评估是否需要消息队列（Kafka）、缓存（Redis）、搜索（ES）
5. 确定配置项（Apollo namespace 规划）

**参考文档**：加载 `references/project-architecture.md` 了解架构细节

#### 2.2 数据库设计

1. 表命名：`LNK_` 前缀 + 大写下划线（如 `LNK_KB_DOCUMENT`）
2. 字段命名：大写下划线（如 `DOCUMENT_NAME`、`CREATE_TIME`）
3. 必备字段：`ID`（主键）、`CREATED_BY`、`CREATION_DATE`、`LAST_UPDATED_BY`、`LAST_UPDATE_DATE`、`OBJECT_VERSION_NUMBER`（乐观锁）
4. 设计 MyBatis Mapper 接口（继承 `BasicMapper<T>`）和 XML 映射文件
5. 多数据源考量：业务数据 → linkbase，管理数据 → linkadmin，分析数据 → ClickHouse

**特殊模式 — 数据中转**：link-ai 知识库模块不落本地库，Service 层直接代理第三方 API。如需求涉及知识库，参考此模式。

**参考文档**：加载 `references/database-guide.md` 了解数据库设计规范和 MyBatis 模式

#### 2.3 接口设计

1. 路由设计：
   - 服务内：`/link/{module}/{resource}/{action}`（如 `/link/aiAssistant/kbDocument/queryPage`）
   - 网关层：`/linkcrm/{module}/{resource}/{action}`（网关 StripPrefix=1）
2. 请求方式：统一 `@RequestMapping`（不限定 method），参数用 `@JsonParam` 接收 JSON 请求体
3. 响应格式：统一信封
   ```json
   {
     "success": true,
     "code": "200",
     "result": {},
     "rows": [],
     "total": 100,
     "detailMessage": ""
   }
   ```
4. 错误码设计：参考 `references/api-design-guide.md` 中的错误码体系
5. Swagger 文档：Controller 使用 `@Api(tags={"xxx接口"})` 注解

**参考文档**：加载 `references/api-design-guide.md` 了解完整接口设计规范

**产出**：方案设计文档（技术方案 + 表结构 DDL + 接口契约 + 文件清单）

### 阶段三：编码开发

**目标**：基于 link 标准编写代码，通过 Checkstyle 校验。

#### 3.1 创建文件结构

每个业务域严格三层分包：
```
src/main/java/com/link/{module}/{domain}/
├── controller/        # XxxController extends BasicController<Xxx>
├── service/           # XxxService(接口) + XxxServiceImpl extends BasicServiceImpl<Xxx>
├── dao/mybatis/
│   ├── mapper/        # XxxMapper extends BasicMapper<Xxx>
│   └── sqlMap/        # XxxMapper.xml + XxxMapperMySql.xml
└── model/             # Xxx extends BasicModel
```

#### 3.2 代码模板

使用 `assets/templates/` 下的模板创建新文件：
- `Controller.java` → 复制为 `{Name}Controller.java`
- `Service.java` → 复制为 `{Name}Service.java`
- `ServiceImpl.java` → 复制为 `{Name}ServiceImpl.java`
- `Mapper.java` → 复制为 `{Name}Mapper.java`
- `MapperMySql.xml` → 复制为 `{Name}MapperMySql.xml`
- `Model.java` → 复制为 `{Name}.java`

模板中使用 `{Name}`、`{name}`、`{module}`、`{domain}`、`{table}` 作为占位符，替换为实际值。

#### 3.3 编码规范要点

加载 `references/coding-standards.md` 获取完整规范。关键红线：

| 规则 | 要求 |
|------|------|
| Java 版本 | 1.8（禁止使用 Java 9+ 语法） |
| 缩进 | 4 空格，**禁止 Tab** |
| 行长度 | ≤ 150 字符 |
| 大括号 | 必须使用（即使单行 if/else） |
| switch | 必须有 default 分支 |
| import | 禁止未使用的 import |
| 空 catch | 异常变量名必须为 `expected` |
| 包名 | 全小写 `com.link.{module}.{domain}.{layer}` |
| 表名 | `LNK_` 前缀 + 大写下划线 |
| Controller | 继承 `BasicController<T>`，用 `@Controller` + `@ResponseBody` |
| Service | 接口 + Impl 分离，Impl 继承 `BasicServiceImpl<T>` |
| Mapper | 继承 `BasicMapper<T>`，XML 含 MySql 变体 |
| Model | 继承 `BasicModel`，用 Lombok `@Data` |

#### 3.4 特殊开发场景

**AI 对话集成（Coze）**：
- 参考 `com.link.coze` 包结构
- 非流式：直接调用 Coze API
- 流式：使用 WebFlux + SSE

**火山引擎 HiAgent**：
- 参考 `com.link.hiagent` 包结构
- 含工作流调用、ASR 语音识别

**WebSocket 实时通信**：
- 路径：`/websocket/ai`
- 基于 Netty + link-websocket-starter

**企微集成**：
- 参考 `com.link.base.tencent.corpwx` 包结构
- 通讯录同步、外部联系人、应用消息

**知识库数据中转**：
- 参考 `com.link.base.knowledge` 包结构
- Service 层代理第三方 API，不落本地库
- Token 通过 RSA 公钥加密自动注入

**参考文档**：加载 `references/coding-standards.md` 获取完整编码规范和代码模式

#### 3.5 一致性自检

代码编写完成后执行以下检查：

1. **Checkstyle 合规**：逐条对照 `references/coding-standards.md` 中的 Checkstyle 规则
2. **分层完整性**：Controller → Service → Mapper → Model 四层是否齐全
3. **命名一致性**：类名、表名、路由路径是否对应
4. **XML 映射**：Mapper 接口方法与 XML SQL ID 是否一一对应
5. **依赖注入**：`@Resource` 注入 Service，禁止 `@Autowired`（link 约定）
6. **异常处理**：Controller 层 try-catch BasicServiceException + Exception 双层
7. **Swagger 注解**：`@Api` + `@ApiOperation` 完整

**产出**：代码文件清单 + 一致性自检报告

### 阶段四：测试部署上线

**目标**：验证功能正确性，完成部署上线。

#### 4.1 测试验证

link 项目测试现状：单元测试极少（`maven-surefire-plugin` skip=true），主要依赖手动测试。

**测试策略**：

1. **接口冒烟测试**：使用 curl 命令测试每个接口
   - 注意：link 框架入站签名过滤器会导致直接 curl 返回 475
   - 解决方案：通过网关访问，或参考 `references/testing-guide.md` 中的签名头配置
2. **数据库验证**：执行 SQL 确认数据正确性
3. **日志检查**：查看 `logs/` 目录下的应用日志
4. **Swagger 验证**：访问 `/swagger-ui.html` 确认接口注册

**参考文档**：加载 `references/testing-guide.md` 了解测试方法和签名绕过方案

#### 4.2 构建打包

```bash
# 进入对应模块目录
cd D:\develop\code\cdfai\link-ai  # 或其他模块

# Maven 打包（跳过测试）
mvn clean package -DskipTests
```

**注意**：需要配置 `settings.xml`（阿里云镜像 + 内部 Nexus 仓库认证），link-core 等私有依赖从内部 Nexus 拉取。

#### 4.3 Docker 镜像构建

```bash
# 多阶段构建
docker build -f Dockerfile -t cdfai/link-{module}:{version} .
```

Dockerfile 模式：Stage 1 Maven 构建 → Stage 2 运行时（基于 choerodon-tools/javabase:0.8.0）

#### 4.4 K8s 部署

1. 更新 Helm Chart values（`charts/link-{module}/values.yaml`）
2. 配置项：
   - 副本数、资源限制（requests/limits）
   - JVM 参数（G1GC，Xms/Xmx）
   - 数据库/Redis/Kafka 连接配置
   - Apollo 配置中心 namespace
3. 部署命令：
   ```bash
   helm upgrade --install link-{module} ./charts/link-{module} -n {namespace}
   ```
4. 健康检查：startupProbe / readinessProbe / livenessProbe（TCP 探针）

**参考文档**：加载 `references/deployment-guide.md` 了解完整部署流程

#### 4.5 上线验证

1. 服务注册确认（Eureka 注册成功）
2. 网关路由可达性验证
3. 接口功能冒烟测试
4. 日志无异常 ERROR
5. 监控告警配置确认

**产出**：测试报告 + 部署确认 + 上线验证清单

### 阶段五：运维与后续

**目标**：保障系统稳定运行，快速响应线上问题。

#### 5.1 日常运维

1. **日志监控**：Log4j2 + Graylog GELF，关注 ERROR 级别日志
2. **配置变更**：通过 Apollo 配置中心热更新（namespaces: ops / biz / stability）
3. **定时任务**：XXL-JOB 管理（端口 8025），关注任务执行状态
4. **数据库运维**：MySQL 主从同步、Redis 集群健康、ES 索引状态

#### 5.2 故障排查

加载 `references/troubleshooting.md` 获取已知问题和解决方案。

**常见问题快速索引**：

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| curl 返回 475 | link 框架入站签名校验失败 | 通过网关访问或配置签名头 |
| Maven 编译失败 | link-core 不在本地 .m2 | 配置 settings.xml 指向内部 Nexus |
| 接口返回 412 | 乐观锁冲突（OBJECT_VERSION_NUMBER） | 重试或检查并发更新 |
| MyBatis SQL 注入 | `${}` 拼接排序字段 | 改用 `#{}` 或白名单校验 |
| 大文件下载 OOM | Range 解析脆弱 | 使用流式写入 + 分片处理 |
| Fastjson 漏洞 | 1.2.83 版本历史漏洞 | 评估升级到 Fastjson2 或替换 Jackson |

#### 5.3 性能优化

1. **数据库**：EXPLAIN 分析慢查询，索引优化
2. **缓存**：Redis 缓存热点数据，注意缓存一致性
3. **JVM**：G1GC 调优，关注 GC 日志
4. **连接池**：Druid 监控（gateway），MyBatis 连接池配置
5. **K8s**：HPA 自动扩缩容，资源限制调优

#### 5.4 安全检查

1. SQL 注入：检查 MyBatis XML 中 `${}` 使用
2. 敏感信息泄露：异常信息不返回前端
3. Fastjson 漏洞：评估 AutoType 配置
4. 签名校验：确保入站请求签名有效
5. 权限控制：接口鉴权（link-auth 服务）

**产出**：运维操作记录 + 故障排查报告 + 优化建议

## 参考文档索引

| 文档 | 路径 | 用途 |
|------|------|------|
| 项目架构 | `references/project-architecture.md` | 模块划分、技术栈、服务间关系 |
| 编码规范 | `references/coding-standards.md` | Checkstyle 规则、命名约定、代码模式 |
| 接口设计 | `references/api-design-guide.md` | API 模式、响应格式、错误码、网关路由 |
| 数据库指南 | `references/database-guide.md` | 表设计、MyBatis 模式、多数据源 |
| 部署指南 | `references/deployment-guide.md` | Docker、K8s、Helm、Apollo |
| 测试指南 | `references/testing-guide.md` | 测试方法、签名绕过、冒烟测试 |
| 故障排查 | `references/troubleshooting.md` | 已知问题、环境限制、解决方案 |

## 代码模板索引

| 模板 | 路径 | 用途 |
|------|------|------|
| Controller | `assets/templates/Controller.java` | 控制器模板 |
| Service | `assets/templates/Service.java` | 服务接口模板 |
| ServiceImpl | `assets/templates/ServiceImpl.java` | 服务实现模板 |
| Mapper | `assets/templates/Mapper.java` | MyBatis Mapper 接口模板 |
| MapperMySql | `assets/templates/MapperMySql.xml` | MyBatis XML 映射模板 |
| Model | `assets/templates/Model.java` | 实体模型模板 |

## 使用建议

1. **新功能开发**：从阶段一开始，依次走完五阶段
2. **接口开发**：重点参考阶段二（接口设计）和阶段三（编码），使用代码模板
3. **Bug 修复**：直接进入阶段三（定位修复）→ 阶段四（验证）
4. **部署上线**：重点参考阶段四的构建打包和 K8s 部署
5. **运维排查**：直接进入阶段五，参考故障排查文档
6. **每次使用时**：根据当前阶段加载对应的 references/ 文档，避免一次性加载所有文档
