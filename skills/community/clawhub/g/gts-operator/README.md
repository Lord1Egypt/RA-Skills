# gts-operator（AI 原生对话式操作员 · 动态发现版）

让 AI Agent 以纯对话方式完成 GTS 多租户平台的全部操作：
**注册租户/管理员 → 维护组织架构与人员 → 配置表单与工作流 → 配置审批代理人与超时自动处理
→ 发起单据 → 流程审批 → 表单复用与模板共享（复制/导出/导入/发布到市场/一键安装）**，
全部通过调用系统真实 HTTP API 完成，不写业务代码、不改库。

## 动态发现模式（v2）
Skill 不再内置端点表。Agent 每次会话先拉取系统自带的机器可读契约，再按契约执行：

- `GET /discovery/routes` — 从 Router 注册表**动态导出**全部端点（method/path/参数），后端增删路由自动反映，零维护。
- `GET /discovery/contract` — 配置域契约：12 种字段类型白名单与附加属性、流程节点属性（含 `field_permissions` 与 `timeout`）/审批人规则/condition、biz_data 状态机与 data_json/subforms 组装规则、审批 action 枚举、字典用法、**模板包（gts-template）结构与市场语义**、**代理人语义**。

后端演进（新增字段类型/端点/状态）只需更新契约源，Skill 无需手改。

## 系统侧新增（v2.3.0 超时自动处理 + 审批代理人）
- `core/Validator.php`：新增 `TIMEOUT_ACTIONS`（`remind`/`transfer`/`approve`/`reject`）、
  `TIMEOUT_ACTIONS_TARGETED`、`TIMEOUT_ACTIONS_UNSAFE`、`DELEGATION_SCOPES`、
  `TIMEOUT_MIN_HOURS=1`/`TIMEOUT_MAX_HOURS=744`，以及节点 `timeout` 校验
  （cc 节点拒绝携带、`after_hours` 范围、`transfer` 必带 `transfer_to`、
  `approve`/`reject` 必须 `acknowledged:true`）。
- `controllers/DelegationController.php`（新）：
  - `GET /delegations`（`?mine=1`；管理员看全租户，其他用户只看自己的）
  - `POST /delegations`（`user_id` 仅管理员可指定，默认本人）
  - `PUT /delegations/{id}`、`DELETE /delegations/{id}`（撤销为软删除）
  - 服务端挡下：自代理、跨租户用户、时间窗倒置、**同一被代理人生效期重叠的代理**
  - 列表响应附服务端计算的 `state`（`active`/`scheduled`/`expired`/`revoked`）与 `is_active_now`
- `controllers/BizDataController.php`：
  - 新增 `advanceAfterNode()` —— 人工 `complete()` 与超时引擎**共用同一状态机**，避免两份实现漂移
  - 新增 `runTimeoutActions()` —— **惰性触发**（在 `GET /biz-data`、`GET /biz-data/{id}`、
    `POST /biz-data/{id}/escalate` 时求值），靠 `node_tasks.timeout_action_at` 条件 UPDATE
    保证**同一任务只执行一次**，无需 cron
  - `escalate()` 改为执行节点配置的 timeout 动作；未配置时退回原"记录一次升级"
  - **修复既有缺陷**：`node_tasks.deadline_at` 此前从未被任何代码写入（`deadline_hours` 可配可读，
    但无代码写该列），导致逾期红标不亮、`escalate()` 永远找不到过期任务。现由 `createNodeTasks()` 写入
- `user_delegations` 表 + `node_tasks` 三个新列（`timeout_action_at`/`timeout_action`/`delegated_from_id`）
  + `idx_task_timeout` 索引。**零迁移**：不写 `timeout` 键的流程行为与改前完全一致。
- 前端：`WorkflowDesigner.jsx` 节点编辑器加超时处理 UI（含自动同意/驳回的确认勾选）、
  `Delegations.jsx`（新）代理人管理页、`SideNav.jsx` 主导航入口（**所有用户**都可能需代理自己）。
- `/discovery/contract` 新增 `delegation` 域 + `workflows.node.timeout` 说明
  （含 `when_it_runs` 与 `audit` 两条治理说明）。

## 系统侧新增（v2.2.0 节点级字段权限）
- 节点 `field_permissions`：`{字段键: editable|readonly|hidden|required}`，服务端强制——
  读时把 `hidden` 从 data_json **和** schema_json 双删；写时只接受 `editable`/`required`
  并校验 `required` 非空。零迁移；老流程无此键行为不变。

## 系统侧新增（v2.0.0 / v2.1.0 / v2.1.1 模板能力）
- `controllers/TemplateController.php`：
  - v2.0.0 **模板包**：`GET /templates/export`、`POST /templates/inspect`、`POST /templates/import`
    —— 脱敏（无 tenant_id/user id/内部 id），引用按 code 重映射（`ref_form_code`/`subform_form_code`），
    用户型审批人降级为 placeholder，缺依赖入 warnings 不阻断，导入单事务。
  - v2.1.0 **共享市场**：`POST /templates/publish`、`GET /templates/market`、
    `GET /templates/market/{id}/preview`、`POST /templates/market/{id}/install`、
    `DELETE /templates/market/{id}` —— 无审核公共目录，任一租户 admin 可发布、
    发布者可下架（非属主 404）；`template_market` 表（软删除）。
  - v2.1.1 **子表自动包含**：`buildPackage()` 递归拉入被引用子表（含多层嵌套），
    因此分享/导出/发布**只需传主表 id**，明细表随包自动带上。
- 端点重构：`export/inspect/import` 与市场发布/安装共用 `buildPackage()` /
  `installPackage()` / `inspectPackage()` 三个核心，市场安装与文件导入行为不会分叉。
- `/discovery/contract` 新增 `templates` 域（含 `market` 子段）。
- `POST /forms/{id}/clone`（v1.9.0）：同租户复制表单（可选连带复制审批流）。

## 系统侧新增（v1.4.0 发现层）
- `core/Router.php`：公开 `Router::routes()` 导出注册表。
- `controllers/DiscoveryController.php`（新）：两个只读公开端点。
- `api.php`：注册两条 discovery 路由。

## 系统侧新增（v1.8.0 OAuth 设备授权）
- `controllers/OauthController.php`（新）：`/oauth/device`（Agent 发起）、`/oauth/status`（Agent 轮询）、`/oauth/approve`（授权页登录后确认）、`/oauth/me`（验证 token）、`/oauth/revoke`。
- `oauth_sessions` 表 + 30 天 token（`config/app.php` `oauth_token_expiry`）。
- 前端 `OauthAuthorize.jsx`（`#/oauth/authorize?user_code=XXX` 授权页，复用平台账号登录）。
- `/discovery/contract` `api` 域新增 `oauth_device_flow` / `token_lifetime` 说明。

## 使用（对最终用户）
- **API 地址已内置**（`https://www.geeyo.com/s/gts/api.php`），用户**无需提供地址**。
- **认证方式**：
  - **① OAuth 设备授权（推荐，v1.8.0 起）**：AI Agent 会引导你在浏览器打开授权链接并登录你的平台账号确认。授权一次 **30 天有效**，跨对话免重复登录，无需把密码告诉 Agent。凭证由 Agent 持久化在本机 `~/.gts-operator.json`。
  - **② 账号密码（临时）**：直接提供手机号+密码+租户 slug（或让 Agent `POST /auth/register` 开新租户）。
- 例："帮我在 geeyo 搭一个设备申购流程，1 万以下自动过、以上 Ken 审批"——Agent 会先完成 OAuth 认证（若无有效授权），再自动执行全部 API 调用。
- 例（v2.3.0）："这个节点超过 24 小时没人审就转给小李，超过 3 天就自动驳回"；"我 9/20–9/27 休假，报销审批转给小李"。
- 授权页会显示请求方与有效期；中途可对 Agent 说"撤销授权"立即生效。

## 已验证（2026-09）
- discovery 输出正确：端点自动列出、contract 各域（含 `templates`、`delegation`、`workflows.node.timeout`）与代码一致。
- 动态发现 + 全链路 E2E（注册租户→组织→表单→流程→发起→审批含条件分支）此前已实测通过。
- AI Agent 验收：对话式搭"设备申购"（坏 schema→400→Agent 自愈）+ 双条件发起 + 审批 + 审计留痕全通过（v1.5.0）。
- OAuth UX（v1.8.1）：授权页展示请求方 client_label、授权码状态引导、租户 slug 化标识、成功摘要与撤销提示。
- 模板能力（v2.0.0–v2.1.1）：导出/导入脱敏包 + 引用 code 重映射（冒烟 21/21）；共享市场发布/浏览/预览/安装/下架 + 跨租户隔离（冒烟 11/11）；**子表自动包含**（单元 8/8、端到端 11/11：只传主表 id 即产出含子表的完整包，安装后子表引用正确重绑）。
- 字段权限（v2.2.0）：隐藏字段双向不可见、发起人与管理员不受限、`required` 空值 400、写入过滤丢弃 hidden、跨租户 404、老流程无键回归。
- **超时 + 代理人（v2.3.0）**：Validator 行为探针 15/15（cc 节点拒绝、范围、必填、`acknowledged` 门禁）；
  HTTP 冒烟 **38/38（连跑两次幂等）**——remind 不改状态、**once-only**（重复读只执行一次）、
  transfer 改派且原责任人保留、**转交目标失效时中止且不丢任务**、approve 跨节点自动推进 + `Auto-approve` 留痕、
  reject 关闭单据、代理人改派新任务 + `delegated_from_id`、跨租户代理不可见/不可改（404）/跨租户用户不可当代理人、
  自代理/时间窗倒置/重叠窗口全部拒绝、人工 `complete()` 与 `escalate()` 回归通过、`deadline_at` 现已写入。
  生产发布后已复验：路由上线、鉴权隔离正常、代理人 CRUD 全 200。

## 已知边界
- 注册接口当前完全开放（无邀请码）；如担心滥用可加"注册邀请码/人工审批"。
- 表单 schema / 流程 nodes 已由服务端校验（v1.5.0）：非法配置返回 400 + 精确定位，Agent 据此自愈；契约字段枚举见 `/discovery/contract`。
- `/discovery/contract` 的枚举（字段类型/状态/action/模板语义/超时与代理人语义）由 DiscoveryController 维护，引擎变更时需同步该文件。
- **模板市场无审核**：公共目录，任一租户管理员可发布；发布者只能下架自己的条目，无平台级全局管理员（治理能力见 BACKLOG）。
- **子表公式不参与计算**：`SubFormEditor` 仅渲染 schema，子表内的 `formula` 字段不会自动算（主表字段正常）。
- **超时处理是惰性触发**：无后台调度器，只在 `GET /biz-data`、`GET /biz-data/{id}` 或
  `POST /biz-data/{id}/escalate` 时求值。因此"到点了但没人打开单据"就不会执行——这是设计如此。
  没有 cron/定时任务；如需严格按时执行需平台侧另加调度（见 BACKLOG）。
- **超时只支持小时维度**：`after_hours` 为 1..744 连续计时。竞品（钉钉宜搭）的
  法定工作日 / 免打扰时段 / 多次提醒尚未实现（见 BACKLOG）。
- **未实现 `goto`（超时跳转到其他节点）**：宜搭有五种动作，本平台只做了四种
  （`remind`/`transfer`/`approve`/`reject`）。跳转需要节点跳过语义，与 v2.2.0 的
  `field_permissions`（按节点绑定处理人）存在语义冲突，故未实现。
- **自动同意/驳回是机器判定**：默认关闭、需显式 `acknowledged`、执行留痕（`Auto-*`，
  actor 记原处理人）。它能改变审批结论而无人参与——用户问治理问题时如实说明。
- **代理人只影响新建任务**：不追改代理生效前已存在的任务；撤销也不回收已在代理人待办里的任务。
