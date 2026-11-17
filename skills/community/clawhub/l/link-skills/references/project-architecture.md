# Link 项目架构参考

## 总体架构

Link 是一套 CRM + AI 助手企业级微服务系统，基于 Java 8 + Spring Boot 2.1.2 + Spring Cloud Greenwich 构建。采用 Monorepo 管理，包含 8 个独立 Maven 模块（无聚合父 pom，各模块独立构建）。

## 模块清单

| 模块 | 路径 | 职责 | 端口 |
|------|------|------|------|
| link-ai | `link-ai/` | AI 助手服务（核心） | 8888（服务）/ 9235（容器） |
| link-base | `link-base/` | 基础业务服务（CRM 核心，最大模块） | - |
| link-auth | `link-auth/` | 认证授权服务 | - |
| link-gateway | `link-gateway/` | API 网关 | 8888 |
| link-config | `link-config/` | Spring Cloud Config 配置中心 | - |
| link-log | `link-log/` | 日志服务 | - |
| link-login | `link-login/` | 登录服务 | - |
| link-register | `link-register/` | Eureka 注册中心 | - |

## 服务间关系

```
                    ┌─────────────┐
                    │ link-register│ (Eureka)
                    │  注册中心     │
                    └──────┬──────┘
                           │ 注册/发现
           ┌───────────────┼───────────────┐
           │               │               │
    ┌──────┴──────┐ ┌──────┴──────┐ ┌──────┴──────┐
    │ link-gateway│ │  link-ai    │ │  link-base  │
    │  API 网关   │ │  AI 助手    │ │  CRM 核心   │
    └──────┬──────┘ └──────┬──────┘ └──────┬──────┘
           │               │               │
           │     ┌─────────┴─────────┐     │
           │     │                   │     │
    ┌──────┴──────┐         ┌────────┴──────┴────┐
    │  link-auth  │         │   link-config      │
    │  认证授权   │         │   配置中心          │
    └─────────────┘         └────────────────────┘
```

## 技术栈详情

### 核心框架

| 技术 | 版本 | 说明 |
|------|------|------|
| Java | 1.8 | 编译目标版本（禁止使用 Java 9+ 语法） |
| Spring Boot | 2.1.2.RELEASE | 所有模块统一 |
| Spring Cloud | Greenwich.RELEASE | 微服务套件 |
| Spring Cloud Gateway | Greenwich | 网关（link-gateway） |
| Spring Cloud Config | Greenwich | 配置中心（link-config） |
| Eureka | Greenwich | 服务注册发现（link-register） |
| OpenFeign | Greenwich | 服务间调用 |
| Hystrix | Greenwich | 熔断降级 |

### 数据与中间件

| 技术 | 版本 | 用途 |
|------|------|------|
| MySQL | 8.0.30 | 主数据库（linkbase + linkadmin 库） |
| ClickHouse | - | 分析型数据库（linkloyalty 库） |
| Redis | Jedis 2.9.1 | 缓存（支持单机/集群） |
| Kafka | Spring Kafka | 消息队列（审计追踪） |
| Elasticsearch | 7.16.3 | 全文检索 |
| MyBatis | 2.0.0 (spring-boot-starter) | ORM |
| Druid | 1.2.13 | 数据库连接池（gateway） |
| Apollo | 1.9.2 | 配置中心 |

### AI 相关依赖（link-ai 专属）

| 依赖 | 版本 | 用途 |
|------|------|------|
| coze-api | 0.2.8 | Coze AI 对话平台 SDK |
| volc-sdk-java | 1.0.49 | 火山引擎 SDK（HiAgent、ASR） |
| link-websocket-starter | 1.0.0-RELEASE | Netty WebSocket 支持 |
| Java-WebSocket | 1.5.3 | WebSocket 客户端 |
| spring-boot-starter-webflux | - | 响应式流（Coze 流式对话） |

### 工具库

| 依赖 | 版本 |
|------|------|
| Lombok | provided |
| Fastjson | 1.2.83 |
| Jackson | 2.10.5 |
| Guava | 27.0-jre |
| OkHttp | 3.12.0 |
| commons-lang3 | 3.0 |
| XXL-JOB | 2.0.1 |
| Log4j2 | 2.17.0 |
| Graylog GELF | 1.3.1 |
| Knife4j | 2.0.5 |
| Springfox Swagger UI | 2.9.2 |
| jasypt-spring-boot-starter | 2.0.0（加密） |

### 内部私有依赖

来自内部 Nexus 仓库 `http://nexus.saas.hand-china.com/repository/link-maven-repository-proxy/`：

| 依赖 | 版本 | 说明 |
|------|------|------|
| link-core | 1.5.95-RELEASE | 核心框架（BasicController/BasicModel/BasicService/BasicMapper） |
| link-mvc | - | MVC 框架（含安全过滤器） |
| link-mvc-aigc | - | AIGC 相关 MVC 扩展 |

## link-ai 模块源码结构

路径：`link-ai/src/main/java/com/link/`

| 子包 | 职责 |
|------|------|
| `autoconfigure/` | 自动配置（@EnableLinkAi、AiAutoConfiguration） |
| `base/agentconf/` | AI Agent 配置管理 |
| `base/application/` | 应用管理 |
| `base/conversation/` | 对话管理（含历史记录） |
| `base/guidedpurchase/` | 导购训练 |
| `base/knowledge/` | 知识库模块（文档/版本/文件，数据中转模式） |
| `base/organization/` | 组织架构 |
| `core/config/` | AOP/Swagger/Bean 配置 |
| `core/feignclients/` | Feign 客户端 |
| `core/websocket/` | Netty WebSocket 支持 |
| `coze/` | Coze AI 对话集成 |
| `hiagent/chat/` | 火山引擎 HiAgent 集成（含 ASR 语音识别） |

### 知识库模块结构（三层分包规范示例）

```
base/knowledge/
├── config/              # KnowledgeProperties, KnowledgeApiConstants, KnowledgeHttpHelper
├── kbdocument/          # 知识库文档
│   ├── controller/
│   ├── service/
│   ├── dao/mybatis/{mapper,sqlMap}/
│   └── model/
├── kbdocumentfile/      # 文档文件上传（分片）
└── kbdocumentversion/   # 文档版本管理
```

## link-base 模块结构

路径：`link-base/src/main/java/com/link/base/`

| 子包 | 职责 |
|------|------|
| `base/` | 核心 CRM（accnt 账户、activity 活动、approval 审批、attendance 考勤等数十个子域） |
| `core/` | 核心工具 |
| `dmp/` | 数据管理平台 |
| `ext/` | 扩展 |
| `loyalty/` | 会员忠诚度 |
| `microinterface/` | 微服务接口 |
| `task/` | 定时任务（XXL-JOB） |
| `tencent/corpwx/` | 企业微信集成（通讯录同步、外部联系人、应用消息等） |
| `wechat/` | 微信公众号集成 |

## 网关路由配置

link-gateway `application.yml` 路由规则：

| 路由前缀 | 目标服务 | 说明 |
|----------|----------|------|
| `/linkcrm/ai/**` | link-ai | AI 助手服务 |
| `/linkcrm/action/**` | link-base | CRM 基础业务 |
| `/linkcrm/login/**` | link-login | 登录服务 |
| `/linkcrm/ai/websocket/**` | ai-websocket | WebSocket |

- 统一前缀：`/${LINK_PREFIX:linkcrm}/{module}/**`
- StripPrefix=1（去掉第一段前缀）

## 多环境 Profile

link-ai 支持多个 bootstrap profile：

| Profile | 用途 |
|---------|------|
| `eurekasingle` | 单节点 Eureka（开发环境） |
| `eurekamulti` | 多节点 Eureka（生产环境） |
| `runtime` | 运行时 |
| `choerodon` | Choerodon 平台 |
| `devmix` | 混合开发环境 |

## 构建工具

- **Maven**（各模块独立 pom.xml，无聚合父 pom）
- `maven-compiler-plugin`：source/target 1.8，UTF-8
- `maven-checkstyle-plugin` 3.0.0（validate 阶段执行，违反即构建失败）
- `maven-surefire-plugin`：skip=true（测试默认跳过）
- `spring-boot-maven-plugin` 1.3.7.RELEASE

## Maven settings.xml

路径：`link-ai/settings.xml`（其他模块类似）

- 阿里云镜像加速
- 内部 Nexus 仓库认证（用户：linkcrm）
- 私有依赖仓库代理
