---
name: kingdee-dev
version: 1.1.0
description: >
  金蝶二次开发全栈技能。覆盖金蝶云星空（K3 Cloud）和金蝶云苍穹（Cosmic）的二次开发，
  重点聚焦插件开发。触发场景：金蝶、K3、星空、苍穹、BOS、BOS IDE、单据、插件开发、
  表单插件、列表插件、操作插件、报表插件、单据转换插件、服务插件、审批流插件、
  WebAPI、DynamicObject、BusinessInfo、IIS、SQL Server、KingScript、动态表单、
  金蝶二开、金蝶开发、金蝶接口、金蝶单据、金蝶报表、金蝶审批流、金蝶工作流、
  金蝶数据库、金蝶打包部署、金蝶补丁、金蝶自定义WebAPI、金蝶插件注册、金蝶字段操作、
  金蝶菜单发布、金蝶权限配置、金蝶数据迁移、金蝶多组织、金蝶性能优化、金蝶苍穹低代码、
  金蝶苍穹Java开发。当用户提到任何与金蝶ERP系统开发相关的需求时使用此技能。
---

# 金蝶二次开发技能

## 产品线识别

收到需求后先识别目标产品：

| 关键词 | 产品 | 技术栈 | 参考 |
|--------|------|--------|------|
| 星空、K3 Cloud、K/3 Cloud、BOS IDE、C#插件、K3Cloud | 金蝶云星空 | C# / .NET / SQL Server / IIS | `references/xingkong-plugin-dev.md` |
| 苍穹、Cosmic、AI苍穹、低代码、KingScript、Java插件 | 金蝶云苍穹 | Java / Spring Cloud / PostgreSQL | `references/cangqiong-dev.md` |

无法判断时，先问用户："是金蝶云星空（K3 Cloud）还是金蝶云苍穹（Cosmic）？"

## 需求决策树

拿到一个二开需求，按以下决策树快速定位：

### 1. 识别需求类型

| 用户说 | 处理方向 | 推荐文档 |
|--------|----------|----------|
| "界面按钮点击/字段联动/表单加载后控制" | 星空表单插件 | `references/xingkong-plugin-dev.md` §表单插件 |
| "列表过滤/行着色/批量操作" | 星空列表插件 | `references/xingkong-plugin-dev.md` §列表插件 |
| "保存前校验/提交前校验/审核后处理" | 星空操作插件 | `references/xingkong-plugin-dev.md` §操作插件 |
| "下推时改字段/转单逻辑" | 星空单据转换插件 | `references/xingkong-plugin-dev.md` §单据转换插件 |
| "自定义报表/账表" | 星空报表插件 | `references/xingkong-plugin-dev.md` §报表插件 |
| "自定义接口/定时任务/后台服务" | 星空服务插件 | `references/xingkong-plugin-dev.md` §服务插件 |
| "审批人动态设置/审批流扩展/跳过审批" | 星空审批流插件 | `references/workflow-plugin-dev.md` |
| "多组织/数据权限/字段权限" | 星空多组织与权限 | `references/multi-org-security.md` |
| "慢/卡/大数据量/性能优化" | 星空性能优化 | `references/performance-debugging.md` |
| "查表/SQL/上下游关联" | 星空数据库参考 | `references/database-reference.md` |
| "部署/打包/调试/运维" | 星空部署运维 | `references/deployment-ops.md` |
| "第三方系统对接/外部接口" | 星空WebAPI | `references/xingkong-webapi.md` |
| "BOS建模/字段扩展/菜单发布" | BOS IDE 操作 | `references/xingkong-bos-ide.md` |
| "苍穹表单/操作/列表/报表/Java" | 苍穹开发 | `references/cangqiong-dev.md` |

### 2. 星空开发完整流程

1. **明确产品线**：星空 / 苍穹
2. **确定需求类型**：插件 / BOS建模 / 接口 / 报表 / 数据迁移
3. **选择插件类型**：见下方插件选择矩阵
4. **编码实现**：使用 `references/plugin-templates.md` 对应模板
5. **处理边界**：空值判断、异常处理、事务安全、权限控制
6. **本地测试**：BOS IDE 注册插件，IIS 回收，浏览器验证
7. **部署上线**：BOS IDE 打包 → 测试环境验证 → 生产环境部署

## 插件选择矩阵（星空）

| 需求场景 | 插件类型 | 基类 | 参考 |
|----------|----------|------|------|
| 单据界面交互（按钮点击、字段变更、数据联动） | 表单插件 | `AbstractFormPlugin` | `references/xingkong-plugin-dev.md` §表单插件 |
| 列表界面过滤、工具栏操作、行着色 | 列表插件 | `AbstractListPlugin` | `references/xingkong-plugin-dev.md` §列表插件 |
| 保存/提交/审核/反审核时校验或干预 | 操作插件 | `AbstractOperationServicePlugIn` | `references/xingkong-plugin-dev.md` §操作插件 |
| 报表数据查询与展示 | 报表插件 | `AbstractSysReportServicePlugIn` | `references/xingkong-plugin-dev.md` §报表插件 |
| 下推转单时干预转换逻辑 | 单据转换插件 | `AbstractConvertPlugIn` | `references/xingkong-plugin-dev.md` §单据转换插件 |
| 自定义WebAPI / 定时任务 / 后台服务 | 服务插件 | `AbstractServiceHandler` / `IScheduleService` | `references/xingkong-plugin-dev.md` §服务插件 |
| 审批流节点控制、动态审批人 | 审批流插件 | `AbstractWorkflowPlugin` | `references/workflow-plugin-dev.md` |

## 核心参考文件

| 文件 | 内容 | 何时读取 |
|------|------|----------|
| `references/xingkong-plugin-dev.md` | 星空6大类插件完整开发指南 | 星空插件开发需求 |
| `references/plugin-templates.md` | 各类插件完整代码模板 + 复杂案例 | 编码阶段直接套用 |
| `references/workflow-plugin-dev.md` | 审批流插件开发与节点控制 | 审批流扩展需求 |
| `references/multi-org-security.md` | 多组织、权限、SQL安全 | 多组织/权限相关需求 |
| `references/performance-debugging.md` | 性能优化、日志分析、死锁排查 | 性能问题/调试排错 |
| `references/xingkong-bos-ide.md` | BOS IDE 操作手册 | 需要BOS建模/配置时 |
| `references/xingkong-webapi.md` | WebAPI 接口开发 | 第三方对接需求 |
| `references/database-reference.md` | 数据库核心表/SQL/多语言/LK表 | 写SQL/查数据时 |
| `references/cangqiong-dev.md` | 苍穹二次开发 | 苍穹相关需求 |
| `references/common-patterns.md` | 常见开发模式 + 社区FAQ | 遇到典型问题/报错时 |
| `references/deployment-ops.md` | 打包部署/调试/运维 | 部署阶段 |

## 编码规范

- **命名**：插件类名 = `{业务对象}{功能}PlugIn`，如 `SaleOrderValidatePlugIn`
- **防御式编程**：所有字段取值都做空判断，避免 `NullReferenceException`
- **多语言**：涉及中文名称的字段必须关联 `_L` 表，`FLOCALEID=2052`
- **上下游关联**：使用 `_LK` 关联表，`FSID` → 上游明细 `FENTRYID`
- **SQL安全**：所有 SQL 查询使用参数化，禁止字符串拼接用户输入
- **性能**：操作插件在 `OnPreparePropertys` 中只声明必要字段，避免全量加载
- **单据操作**：系统自带单据先"扩展"再修改，修改前必须"签出"，改完"保存→签入→发布"
- **异常处理**：表单插件使用 try-catch；操作插件异常会阻止单据操作，需谨慎使用
- **日志**：关键节点写日志，便于生产排查

## 版本兼容性

星空不同版本的 BOS API 可能存在差异。开发时需注意：
- 从对应版本 `K3Cloud\WebSite\bin` 目录复制引用 DLL
- 升级后重新编译并注册所有自定义插件
- 公有云与私有云的部分 API 行为可能不同

## 官方资源索引

| 资源 | 链接 |
|------|------|
| 星空知识地图 | https://vip.kingdee.com/article/392699482837824512 |
| 星空社区 | https://vip.kingdee.com/search?productId=1&productLineId=1 |
| 星空环境下载 | https://open.kingdee.com/K3Cloud/Open/Products.aspx |
| 星空开发入门视频 | https://vip.kingdee.com/school/learnPath/193463482326019584 |
| WebAPI接口说明书 | https://vip.kingdee.com/knowledge/2569 |
| 苍穹开发者门户 | https://dev.kingdee.com/dev |
| 苍穹开发文档 | https://demo.kdcloud.com/devdoc/wf |
| 苍穹开发认证 | https://kone.kingdee.com/certcenter |
| 星空开放平台 | https://open.kingdee.com/k3cloud/open/home |
