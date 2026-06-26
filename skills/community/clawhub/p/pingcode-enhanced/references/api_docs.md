# PingCode Open API 文档

## 基础信息
- Base URL: `https://open.pingcode.com`
- 认证: OAuth2 Client Credentials
  - `GET /v1/auth/token?grant_type=client_credentials&client_id={client_id}&client_secret={client_secret}`
  - 返回: `access_token` (有效期30天), `token_type: Bearer`
- 分页: `page_size` (默认30, 最大100), `page_index` (0开始)
- 频率限制: 200次/分钟

---

## 1. 项目管理 (Agile)

### 项目
- `GET /v1/agile/projects` — 获取项目列表
- `POST /v1/agile/projects` — 创建项目
- `PATCH /v1/agile/projects/{project_id}` — 部分更新项目
- `GET /v1/agile/projects/{project_id}` — 获取项目详情
- `GET /v1/agile/projects/{project_id}/members` — 获取项目成员
- `POST /v1/agile/projects/{project_id}/members` — 添加成员
- `DELETE /v1/agile/projects/{project_id}/members/{member_id}` — 移除成员

### 工作项 (Work Items)
- `GET /v1/agile/projects/{project_id}/work_items` — 获取工作项列表
- `POST /v1/agile/projects/{project_id}/work_items` — 创建工作项
- `PATCH /v1/agile/work_items/{work_item_id}` — 更新工作项
- `DELETE /v1/agile/work_items/{work_item_id}` — 删除工作项
- `GET /v1/agile/work_items/types` — 工作项类型列表
- `GET /v1/agile/work_items/states` — 工作项状态列表
- `GET /v1/agile/work_items/priorities` — 工作项优先级列表

### 迭代 (Sprint)
- `GET /v1/agile/projects/{project_id}/sprints` — 获取迭代列表
- `POST /v1/agile/projects/{project_id}/sprints` — 创建迭代
- `PATCH /v1/agile/sprints/{sprint_id}` — 更新迭代

### 发布 (Release)
- `GET /v1/agile/projects/{project_id}/releases` — 获取发布列表
- `POST /v1/agile/projects/{project_id}/releases` — 创建发布

---

## 2. 测试管理 (Test Hub)

### 测试库 (Library)
- `GET /v1/testhub/libraries` — 获取测试库列表
- `POST /v1/testhub/libraries` — 创建测试库
- `PATCH /v1/testhub/libraries/{library_id}` — 更新测试库
- `GET /v1/testhub/libraries/{library_id}` — 获取测试库详情
- `POST /v1/testhub/libraries/{library_id}/members` — 添加成员
- `GET /v1/testhub/libraries/{library_id}/members` — 获取成员列表
- `PATCH /v1/testhub/libraries/{library_id}/members/{member_id}` — 更新成员
- `DELETE /v1/testhub/libraries/{library_id}/members/{member_id}` — 移除成员
- `POST /v1/testhub/libraries/{library_id}/suites` — 添加用例模块
- `PATCH /v1/testhub/libraries/{library_id}/suites/{suite_id}` — 更新用例模块
- `GET /v1/testhub/libraries/{library_id}/suites` — 获取用例模块列表
- `DELETE /v1/testhub/libraries/{library_id}/suites/{suite_id}` — 移除用例模块

### 用例 (Case)
- `GET /v1/testhub/cases?library_id={library_id}` — 获取用例列表
- `POST /v1/testhub/cases` — 创建用例
- `PATCH /v1/testhub/cases/{case_id}` — 更新用例
- `DELETE /v1/testhub/cases/{case_id}` — 删除用例
- `POST /v1/testhub/cases/batch` — 批量创建用例
- `PATCH /v1/testhub/cases/batch` — 批量更新用例

### 计划 (Plan/Test Run)
- `GET /v1/testhub/plans` — 获取计划列表
- `POST /v1/testhub/plans` — 创建计划
- `PATCH /v1/testhub/plans/{plan_id}` — 更新计划
- `GET /v1/testhub/plans/types` — 计划类型列表
- `POST /v1/testhub/plans/{plan_id}/test_runs` — 创建执行用例
- `POST /v1/testhub/plans/{plan_id}/test_runs/batch` — 批量创建执行用例
- `GET /v1/testhub/test_runs` — 获取执行用例列表
- `GET /v1/testhub/test_runs/{test_run_id}` — 获取执行用例详情
- `PATCH /v1/testhub/test_runs/{test_run_id}` — 更新执行用例
- `PATCH /v1/testhub/test_runs/batch` — 批量更新执行用例
- `POST /v1/testhub/test_runs/batch/operations` — 批量操作执行用例
- `GET /v1/testhub/test_runs/{test_run_id}/results` — 获取执行结果列表
- `GET /v1/testhub/test_runs/results` — 获取执行结果记录

### 测试配置中心
- `GET /v1/testhub/case_states` — 全部用例状态列表
- `GET /v1/testhub/case_types` — 全部用例类型列表
- `GET /v1/testhub/important_levels` — 全部重要程度列表
- `GET /v1/testhub/test_run_results` — 全部执行结果列表
- `GET /v1/testhub/plan_statuses` — 全部计划状态列表

---

## 3. 产品管理 (SCM)

### 产品 (Product)
- `GET /v1/scm/products` — 获取产品列表
- `POST /v1/scm/products` — 创建产品
- `PATCH /v1/scm/products/{product_id}` — 更新产品
- `GET /v1/scm/products/{product_id}/members` — 成员列表

### 工单 (Ticket)
- `GET /v1/scm/product/{product_id}/tickets` — 工单列表
- `POST /v1/scm/product/{product_id}/tickets` — 创建工单
- `GET /v1/scm/tickets/states` — 工单状态列表
- `GET /v1/scm/tickets/priorities` — 工单优先级列表

### 需求 (Idea)
- `GET /v1/scm/product/{product_id}/ideas` — 需求列表
- `POST /v1/scm/product/{product_id}/ideas` — 创建需求

---

## 4. 知识管理 (Wiki)

- `GET /v1/wiki/spaces` — 空间列表
- `POST /v1/wiki/spaces` — 创建空间
- `GET /v1/wiki/spaces/{space_id}/pages` — 页面列表
- `POST /v1/wiki/spaces/{space_id}/pages` — 创建页面
- `GET /v1/wiki/pages/{page_id}` — 获取页面详情
- `GET /v1/wiki/pages/{page_id}/content` — 获取文档正文
- `PUT /v1/wiki/pages/{page_id}/content` — 更新文档正文

---

## 5. 组织架构 (Directory)

- `GET /v1/directory/users` — 获取企业成员列表
- `GET /v1/directory/departments` — 获取部门列表
- `GET /v1/directory/groups` — 获取团队列表
- `GET /v1/directory/roles` — 获取角色列表
- `GET /v1/directory/jobs` — 获取职位列表

---

## 6. 通用

- `GET /v1/comments?principal_type={type}&principal_id={id}` — 评论列表
- `POST /v1/comments` — 创建评论
- `DELETE /v1/comments/{comment_id}?principal_type={type}&principal_id={id}` — 删除评论
- `POST /v1/attachments` — 上传文件
- `GET /v1/followers?principal_type={type}&principal_id={id}` — 关注人列表
- `POST /v1/followers` — 添加关注人
- `DELETE /v1/followers/{follower_id}?principal_type={type}&principal_id={id}` — 移除关注人
- `GET /v1/relationships?principal_type={type}&principal_id={id}` — 关联列表
- `GET /v1/activities?principal_type={type}&principal_id={id}` — 活动记录
- `GET /v1/work_hours?principal_type={type}&principal_id={id}` — 工时列表
- `POST /v1/work_hours` — 创建工时

---

## 7. DevOps/集成

- `GET /v1/review/reviews` — 评审列表
- `GET /v1/code/repositories` — 代码仓库列表
- `GET /v1/code/commits` — 提交列表
- `GET /v1/code/pull_requests` — 拉取请求列表
- `GET /v1/build/build_records` — 构建记录列表
- `GET /v1/release/environments` — 环境列表
- `GET /v1/release/deployments` — 部署列表

---

## 8. 安全

- `GET /v1/security/login_logs` — 登录日志
- `GET /v1/security/audit_logs` — 审计日志
