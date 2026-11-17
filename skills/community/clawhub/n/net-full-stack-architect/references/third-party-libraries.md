# 第三方插件库清单与选型

> net-full-stack-architect 技能参考文件。引入任何新依赖前必读：先查红线，再定版本，最后 NuGet 核对。

## 目录

1. [使用总则](#1-使用总则)
2. [核心四件套](#2-核心四件套)
3. [分类清单](#3-分类清单)
4. [许可证红线（2026-10 快照）](#4-许可证红线2026-10-快照)
5. [推荐组合](#5-推荐组合)
6. [包治理](#6-包治理)

---

## 1. 使用总则

1. **先内置后三方**：.NET 10 自带 OpenAPI、RateLimiter、HealthChecks、Resilience、Authentication——能内置不引包；
2. **引一个库解决一类问题**，不为“顺便”引入大而全框架；
3. **新依赖过四问**：解决什么具体问题？有没有内置/更轻替代？许可证能否商用？维护是否活跃（近半年有发布）？
4. **版本锁死 + 集中管理**（见第 6 节），升级走单独 PR；
5. 包名**必须去 NuGet 核对拼写**——AI 幻觉包名（slopsquatting 投毒）是真实供应链攻击。

## 2. 核心四件套（本框架默认自带）

| 组件 | 包 | 模板 |
|---|---|---|
| ORM | `SqlSugar`（MIT） | references/orm-sqlsugar.md |
| 文档 | `Swashbuckle.AspNetCore`（MIT）或 .NET 10 内置 `Microsoft.AspNetCore.OpenApi` | references/api-docs-versioning.md |
| 认证 | `Microsoft.AspNetCore.Authentication.JwtBearer`（微软） | references/auth-jwt.md |
| 日志 | `Serilog.AspNetCore` + sinks（Apache-2.0） | references/logging-serilog.md |

## 3. 分类清单

### 3.1 ORM / 数据访问

| 库 | 包 | 选型 |
|---|---|---|
| SqlSugar 5.x | `SqlSugar` | 默认：中文文档、20+ 数据库（含达梦/人大金仓）、分表分库、AOP |
| FreeSql 3.x | `FreeSql` | 需要 AOT/时序库（TDengine/QuestDB）时 |
| Dapper 2.x | `Dapper` | 高频只读/极限性能，手写 SQL |
| EF Core | `Microsoft.EntityFrameworkCore` | 团队已熟悉 EF、需要导航属性/LINQ 全覆盖 |

### 3.2 对象映射

| 库 | 包 | 选型 |
|---|---|---|
| Mapster | `Mapster` | **默认**：MIT、零配置、源生成、快 |
| AutoMapper | `AutoMapper` | ⚠️ 15.0+ 需商业授权，仅锁 ≤14.0.0 或已购授权时用 |

### 3.3 验证

| 库 | 包 | 选型 |
|---|---|---|
| FluentValidation | `FluentValidation` | 默认：声明式校验 + 本地化消息 |
| 内置 DataAnnotations | — | 简单场景够用，无需引包 |

### 3.4 CQRS / 中介者

| 库 | 包 | 选型 |
|---|---|---|
| Mediator（martinothamar） | `Mediator` | **默认**：源生成、AOT 友好、MIT |
| Wolverine | `Wolverine` | 需要「中介 + 消息」一体时（MIT） |
| MediatR | `MediatR` | ⚠️ 13.0+ 需商业授权；锁 12.5.0 可用 |
| 手写 Dispatcher | — | 极简场景：IRequest + Handler + 约 50 行分发器 |

### 3.5 缓存

| 库 | 包 | 选型 |
|---|---|---|
| 内置 + Redis | `Microsoft.Extensions.Caching.StackExchangeRedis` | 默认分布式缓存 |
| FusionCache | `ZiggyCreatures.FusionCache` | 多级缓存（内存+Redis）+ 防击穿，L1/L2 一站 |
| FreeRedis | `FreeRedis` | 国产 Redis 客户端，API 友好 |
| CSRedis | `CSRedisCore` | 老牌国产客户端 |

### 3.6 消息 / 事件总线

| 库 | 包 | 选型 |
|---|---|---|
| DotNetCore.CAP | `DotNetCore.CAP` | **默认**：Outbox 最终一致、本地消息表、MQ 可切换（MIT） |
| MassTransit | `MassTransit` | ⚠️ v9 商业化；锁 v8（Apache）可用至 2026 底安全维护 |
| RabbitMQ/Kafka 客户端 | `RabbitMQ.Client` / `Confluent.Kafka` | 只需裸 MQ 能力时 |

### 3.7 定时任务

| 库 | 包 | 选型 |
|---|---|---|
| Quartz.NET | `Quartz.NET` | 集群调度、Cron、持久化（Apache-2.0） |
| Hangfire | `Hangfire.AspNetCore` | Dashboard 好用；**商业项目先核对许可证** |
| Coravel | `Coravel` | 轻量任务/队列/邮件（MIT） |
| 后台服务 | 内置 `BackgroundService` | 简单常驻任务零依赖 |

### 3.8 网关 / 反向代理

| 库 | 包 | 选型 |
|---|---|---|
| YARP | `Yarp.ReverseProxy` | 微软出品网关默认（MIT） |
| Ocelot | `Ocelot` | 经典 API 网关，配置驱动（MIT） |

### 3.9 认证授权扩展

| 库 | 包 | 选型 |
|---|---|---|
| OpenIddict | `OpenIddict` | 免费 OAuth/OIDC 服务端，替代 Duende |
| Duende IdentityServer | `Duende.IdentityServer` | ⚠️ 商业授权，仅已购license用 |

### 3.10 HTTP 客户端与弹性

| 库 | 包 | 选型 |
|---|---|---|
| 内置 HttpClientFactory | `Microsoft.Extensions.Http` | 默认基座 |
| Microsoft.Extensions.Resilience | `Microsoft.Extensions.Resilience` | **默认重试/熔断**：封装 Polly v8、免费 |
| Polly | `Polly` | ⚠️ 2026-11-16 起收 Open Source Maintenance Fee；已在新项目可用上面那个替代 |
| Refit | `Refit` | 声明式 HTTP 客户端（MIT） |
| Kiota | `Microsoft.Kiota.*` | OpenAPI 生成强类型客户端 |

### 3.11 序列化

| 库 | 包 | 选型 |
|---|---|---|
| System.Text.Json | 内置 | 默认 |
| MemoryPack | `MemoryPack` | 高性能二进制序列化（缓存/MQ 场景） |
| MessagePack | `MessagePack` | 跨语言二进制协议 |
| Newtonsoft.Json | `Newtonsoft.Json` | 遗留兼容，新代码不主动引入 |

### 3.12 文档 / 版本 / UI

| 库 | 包 | 选型 |
|---|---|---|
| Asp.Versioning 家族 | `Asp.Versioning.Mvc` / `.Http` / `.Mvc.ApiExplorer` / `.OpenApi` | 版本化标准件 |
| Swashbuckle | `Swashbuckle.AspNetCore` | 控制器项目 Swagger UI |
| Scalar | `Scalar.AspNetCore` | .NET 10 内置 OpenAPI 的现代 UI |
| NSwag | `NSwag.AspNetCore` | 需要代码生成客户端时 |

### 3.13 可观测 / 健康检查

| 库 | 包 | 选型 |
|---|---|---|
| OpenTelemetry | `OpenTelemetry.Extensions.Hosting` + Instr.* | 链路/指标标准（免费） |
| HealthChecks.UI | `AspNetCore.HealthChecks.UI` | 健康检查面板（Xabaril） |
| MiniProfiler | `MiniProfiler.AspNetCore` | 接口耗时/ SQL 一眼看（MIT） |
| prometheus-net | `prometheus-net.AspNetCore` | Prometheus 指标暴露 |
| SkyAPM | `SkyAPM.Agent.AspNetCore` | 国产 APM（Apache-2.0） |

### 3.14 Excel / PDF / 图片

| 库 | 包 | 选型 |
|---|---|---|
| MiniExcel | `MiniExcel` | **默认 Excel**：流式低内存、MIT |
| Magicodes.IE | `Magicodes.IE` | 导入导出模板丰富、MIT |
| ClosedXML | `ClosedXML` | 复杂格式/图表（MIT） |
| EPPlus | `EPPlus` | ⚠️ v5+ Polyform 非商业授权 |
| QuestPDF | `QuestPDF` | PDF 生成（代码即文档，MIT） |
| SixLabors.ImageSharp | `SixLabors.ImageSharp` | 图片处理；**注意 Split License，商业闭源评估授权** |
| SkiaSharp | `SkiaSharp` | 高性能图形（MIT） |

### 3.15 工具库

| 库 | 包 | 用途 |
|---|---|---|
| FluentValidation | 见 3.3 | — |
| System.Linq.Dynamic.Core | `System.Linq.Dynamic.Core` | 动态排序/筛选字符串 |
| Hashids.net | `Hashids.net` | Id 混淆（防遍历） |
| IdGen | `IdGen` | 雪花 ID |
| IP2Region | `IP2Region` | IP 归属地离线库 |
| MailKit | `MailKit` | 邮件发送 |
| FluentFTP / SSH.NET | 同名包 | FTP / SFTP |
| Apollo 配置中心 | `Com.Ctrip.Framework.Apollo.Configuration` | 携程 Apollo 配置中心 |

### 3.16 测试

| 库 | 包 | 选型 |
|---|---|---|
| xUnit v3 | `xunit.v3` | 默认测试框架 |
| AwesomeAssertions | `AwesomeAssertions` | FluentAssertions 社区 fork（v8 已商业化的免费替代） |
| Shouldly | `Shouldly` | 另一种流式断言 |
| NSubstitute / Moq | 同名包 | Mock |
| AutoFixture | `AutoFixture` | 测试数据生成 |
| Testcontainers | `Testcontainers.*` | 集成测试用真容器（MySQL/Redis/RabbitMQ） |
| NetArchTest | `NetArchTest.Rules` | 架构依赖规则断言 |

## 4. 许可证红线（2026-10 快照）

> 以下为已确认变更授权模式的库。**采用前必须核对官网当前条款**，法务不确定时选替代品。

| 库 | 状态 | 免费线 | 替代 |
|---|---|---|---|
| MediatR | 13.0+ RPL-1.5 + 商业双授权（Lucky Penny） | ≤12.5.0 | Mediator / Wolverine / 手写 |
| AutoMapper | 15.0+ 同上 | ≤14.0.0 | Mapster / 手写 |
| MassTransit | v9 商业化（Massient） | v8（Apache，安全维护至 2026 底后评估） | CAP / 裸 MQ 客户端 |
| FluentAssertions | v8 Xceed 商业（仅 OSS/非商业免费） | ≤7.x | AwesomeAssertions / Shouldly |
| Polly | 2026-11-16 起 Open Source Maintenance Fee（许可证未变） | 当前可用 | Microsoft.Extensions.Resilience |
| EPPlus | v5+ Polyform 非商业 | v4 旧版 | MiniExcel / Magicodes.IE / ClosedXML |
| ImageSharp | Split License | OSS 免费 | 商业闭源需授权或 SkiaSharp |
| Duende IdentityServer | 商业 | — | OpenIddict |
| Hangfire | 部分组件/版本有商业授权要求 | 核对官网 | Quartz.NET / Coravel |

社区免费线（Lucky Penny）：年营收 < $5M、外部资金 < $10M、非政府/高校——**超过任一条即需付费**，别默认自己符合。

## 5. 推荐组合

**组合 A：企业级单体（控制器 API，团队 3-10 人）**
.NET 10 + SqlSugar + Swashbuckle + Asp.Versioning.Mvc + Serilog(ELK) + Mapster + FluentValidation + Mediator + FusionCache + DotNetCore.CAP + MiniProfiler + xUnit v3/Testcontainers

**组合 B：云原生 Minimal API（新服务）**
.NET 10 + Dapper/FreeSql + 内置 OpenAPI + Asp.Versioning.OpenApi + Scalar + OpenTelemetry + Microsoft.Extensions.Resilience + YARP + AwesomeAssertions

**组合 C：轻量快速交付（内部系统/ MVP）**
.NET 10 + SqlSugar + Swashbuckle + Serilog(File) + JwtBearer + FluentValidation + 内置 RateLimiter + BackgroundService（不加 mediator/消息总线）

## 6. 包治理

1. **CPM**：所有版本进 `Directory.Packages.props`（见 project-structure.md），依赖变更 PR 可审查；
2. **Package Source Mapping**：限定每个包只能从 nuget.org（或私有源）恢复，防抢注/投毒；
3. **NuGet Audit 默认开启**：net10.0+ 默认覆盖传递依赖；`NU1903`（高危）/`NU1904`（严重）设 `WarningsAsErrors`；
4. 引入新库写 ADR（架构决策记录）：问题、候选对比、许可证结论、回退方案；
5. 每季度过一遍依赖盘点：替换停更包、清理未使用包、评估许可证变更公告。
