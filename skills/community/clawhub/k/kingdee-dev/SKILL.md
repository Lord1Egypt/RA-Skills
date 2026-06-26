---
name: kingdee-dev
version: 1.0.0
description: >
  金蝶二次开发全栈技能。覆盖金蝶云星空（K3 Cloud）和金蝶云苍穹（Cosmic）的二次开发，
  重点聚焦插件开发。触发场景：金蝶、K3、星空、苍穹、BOS、BOS IDE、单据、插件开发、
  表单插件、列表插件、操作插件、报表插件、单据转换插件、服务插件、WebAPI、
  DynamicObject、BusinessInfo、IIS、SQL Server、KingScript、动态表单、
  金蝶二开、金蝶开发、金蝶接口、金蝶单据、金蝶报表、金蝶审批流、金蝶数据库、
  金蝶打包部署、金蝶补丁、金蝶自定义WebAPI、金蝶插件注册、金蝶字段操作、
  金蝶菜单发布、金蝶权限配置、金蝶数据迁移、金蝶苍穹低代码、金蝶苍穹Java开发。
  当用户提到任何与金蝶ERP系统开发相关的需求时使用此技能。
---

# 金蝶二次开发技能

## 产品线识别

收到需求后先识别目标产品：

| 关键词 | 产品 | 技术栈 | 参考 |
|--------|------|--------|------|
| 星空、K3 Cloud、K/3 Cloud、BOS IDE、C#插件 | 金蝶云星空 | C# / .NET / SQL Server / IIS | `references/xingkong-plugin-dev.md` |
| 苍穹、Cosmic、AI苍穹、低代码、KingScript | 金蝶云苍穹 | Java / Spring Cloud / PostgreSQL | `references/cangqiong-dev.md` |

无法判断时，问用户。

## 需求分析流程

拿到一个二开需求，按以下步骤拆解：

1. **明确产品线** → 星空 or 苍穹
2. **需求分类** → 属于哪类开发：
   - **插件开发**（重点）：表单交互 / 列表过滤 / 操作校验 / 报表数据 / 单据转换 / 服务扩展
   - **BOS建模**：新建或扩展单据、字段、菜单
   - **接口开发**：WebAPI 对接第三方系统
   - **报表开发**：直接SQL账表 / 简单账表
   - **数据层**：SQL查询 / 数据迁移
3. **选择插件类型** → 见下方插件选择矩阵
4. **编码** → 使用 `references/plugin-templates.md` 中对应模板
5. **测试调试** → 参 `references/deployment-ops.md`
6. **打包部署** → 参 `references/deployment-ops.md`

## 插件选择矩阵（星空）

| 需求场景 | 插件类型 | 基类 | 参考 |
|----------|----------|------|------|
| 单据界面交互（按钮点击、字段变更、数据联动） | 表单插件 | AbstractFormPlugin | `references/xingkong-plugin-dev.md` §表单插件 |
| 列表界面过滤、工具栏操作 | 列表插件 | AbstractListPlugin | `references/xingkong-plugin-dev.md` §列表插件 |
| 保存/提交/审核时校验或干预 | 操作插件 | AbstractOperationServicePlugIn | `references/xingkong-plugin-dev.md` §操作插件 |
| 报表数据查询与展示 | 报表插件 | AbstractSysReportServicePlugIn | `references/xingkong-plugin-dev.md` §报表插件 |
| 下推转单时干预转换逻辑 | 单据转换插件 | AbstractConvertPlugIn | `references/xingkong-plugin-dev.md` §单据转换插件 |
| 自定义WebAPI / 定时任务 / 后台服务 | 服务插件 | ISysReportService / IDOService | `references/xingkong-plugin-dev.md` §服务插件 |

## 核心参考文件

| 文件 | 内容 | 何时读取 |
|------|------|----------|
| `references/xingkong-plugin-dev.md` | 星空6大类插件完整开发指南（重点） | 星空插件开发需求 |
| `references/plugin-templates.md` | 各类插件完整代码模板 | 编码阶段直接套用 |
| `references/xingkong-bos-ide.md` | BOS IDE 操作手册 | 需要BOS建模/配置时 |
| `references/xingkong-webapi.md` | WebAPI 接口开发 | 第三方对接需求 |
| `references/database-reference.md` | 数据库核心表/SQL/多语言/LK表 | 写SQL/查数据时 |
| `references/cangqiong-dev.md` | 苍穹二次开发 | 苍穹相关需求 |
| `references/common-patterns.md` | 常见开发模式 + 社区FAQ | 遇到典型问题/报错时 |
| `references/deployment-ops.md` | 打包部署/调试/运维 | 部署阶段 |

## 编码规范

- **命名**：插件类名 = `{业务对象}{功能}PlugIn`，如 `SaleOrderValidatePlugIn`
- **多语言**：涉及中文名称的字段必须关联 `_L` 表，`FLOCALEID=2052`
- **上下游关联**：使用 `_LK` 关联表，`FSID` → 上游明细 `FENTRYID`
- **单据操作**：系统自带单据先"扩展"再修改，修改前必须"签出"，改完"保存→签入"
- **发布**：单据修改后必须"发布到主控台"才能在前台看到

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
