---
name: pingcode
description: PingCode 研发管理平台 API 集成。支持查询工作项、生成周报、管理项目进度等。使用场景：研发管理自动化、团队协作、数据分析。
metadata:
  openclaw:
    requires:
      env:
        - PINGCODE_CLIENT_ID
        - PINGCODE_CLIENT_SECRET
  credential_source: |
    凭证优先从 skill 根目录的 .env 文件加载（已配置），环境变量可覆盖。
    CLIENT_ID: xmoboFefrZmg
    CLIENT_SECRET: wmeVsjWKFrtxxiRFgzVuVBna
---

# PingCode Skill

通过 PingCode Open API 操作研发管理平台数据。

## 前置条件

1. 在 PingCode 企业后台创建应用，获取 `Client ID` 和 `Client Secret`
2. 配置应用的数据访问范围
3. 凭证已在 `.env` 文件中配置，脚本自动加载；也可通过环境变量覆盖：
   ```bash
   export PINGCODE_CLIENT_ID="your_client_id"
   export PINGCODE_CLIENT_SECRET="your_client_secret"
   ```

## 功能脚本

### 获取我的工作项

```bash
python3 scripts/get_my_tasks.py
```

输出示例：
```
📋 你的工作项列表 (共 15 条，显示前 20 条)

⬜ [5e05d844] 优化登录页面性能
   项目: Web端重构 | 状态: 待处理 | 优先级: 高
   负责人: 张三

🔄 [5e05d845] API 接口文档更新
   项目: 开放平台 | 状态: 进行中 | 优先级: 中
   负责人: 李四
```

### 获取项目列表

```bash
# 列出所有项目
python3 scripts/get_projects.py

# 以 JSON 格式输出
python3 scripts/get_projects.py --json

# 限制返回数量
python3 scripts/get_projects.py --limit 50
```

输出示例：
```
📁 项目列表 (共 3 个)

1. 🟢 [5fb277c1] 敏捷示例项目
   类型: 软件开发 | 状态: 进行中 | 负责人: anytao
   描述: 示例项目用于演示敏捷开发流程...

2. 🟢 [5fb277c2] 产品官网重构
   类型: 软件开发 | 状态: 进行中 | 负责人: 张三
   描述: 官网前端重构项目...
```

### 获取指定项目的全部工作项

```bash
# 通过项目名称查询
python3 scripts/get_project_workitems.py --project_name "敏捷示例"

# 通过项目 ID 查询
python3 scripts/get_project_workitems.py --project_id 62ded365

# 以 JSON 格式输出
python3 scripts/get_project_workitems.py --project_name "敏捷示例" --json
```

输出示例：
```
📋 项目工作项 - 敏捷示例 (共 82 条)

⬜ [5fb277c1] 申请售后
   类型: 需求 | 状态: 待处理 | 优先级: 普通
   负责人: anytao

⬜ [5fb277c1] 支付宝支付
   类型: 需求 | 状态: 待处理 | 优先级: 普通
   负责人: anytao
```

### 生成项目周报

```bash
# 生成周报并输出到控制台
python3 scripts/generate_weekly_report.py

# 指定项目和名称
python3 scripts/generate_weekly_report.py --project_id xxx --project_name "PingCode 重构"

# 输出到文件
python3 scripts/generate_weekly_report.py --output /tmp/weekly_report.md
```

输出示例：
```markdown
# 📊 项目周报
生成时间：2024-03-01 14:30

## 📈 数据概览
- 工作项总数：45
- 本周完成：12 (26.7%)
- 进行中：15
- 待处理：18
- 延期风险：3

## ⚠️ 延期风险
发现 3 个工作项已延期，建议优先处理：
- 优化登录性能 (截止：2024-02-28)
```

### 更新工作项

```bash
# 分配负责人
python3 scripts/update_workitem.py --workitem_id 5fb277c1 --assignee anytao

# 设置开始和截止时间
python3 scripts/update_workitem.py --workitem_id 5fb277c1 --start_date "2026-03-12" --due_date "2026-03-20"

# 同时更新多个字段
python3 scripts/update_workitem.py --workitem_id 5fb277c1 --assignee anytao --start_date "2026-03-12" --due_date "2026-03-20" --priority "高"

# 更新状态
python3 scripts/update_workitem.py --workitem_id 5fb277c1 --status "进行中"
```

### 创建工作项

```bash
# 基本用法（项目 ID + 标题必填，type_id 默认 task）
python3 scripts/create_workitem.py --project_id <id> --title "修复登录bug" --type_id bug

# 完整参数示例
python3 scripts/create_workitem.py \
  --project_id <id> \
  --title "修复登录bug" \
  --type_id bug \
  --description "登录页面在 Safari 下白屏" \
  --assignee_id <user_id> \
  --priority_id <priority_id> \
  --sprint_id <sprint_id> \
  --start_at "2026-06-18" \
  --end_at "2026-06-25" \
  --story_points 3

# type_id 固定类型：epic / feature / story / task / bug / issue
```

### 获取/删除单个工作项

```bash
# 获取详情
python3 scripts/get_workitem.py <workitem_id>

# 输出 JSON
python3 scripts/get_workitem.py <workitem_id> --json

# 删除工作项
python3 scripts/get_workitem.py <workitem_id> --delete
```

### 获取企业成员列表

```bash
# 获取所有成员（拿 user_id 用于 assignee_id 等字段）
python3 scripts/get_members.py

# 按名称搜索
python3 scripts/get_members.py --keyword "张三"

# 以 JSON 格式输出
python3 scripts/get_members.py --json
```

输出示例：
```
👥 企业成员列表 (共 12 人，显示 12 条)

🟢 张三 (@zhangsan)
   ID: a0417f68e846aae315c85d24643678a9
   邮箱: zhangsan@company.com
```

### 迭代管理

```bash
# 获取项目迭代列表
python3 scripts/sprints.py list --project_id <id>

# 按状态过滤 (pending / in_progress / completed)
python3 scripts/sprints.py list --project_id <id> --status in_progress

# 创建迭代
python3 scripts/sprints.py create \
  --project_id <id> \
  --name "Sprint 3" \
  --start_at "2026-07-01" \
  --end_at "2026-07-14" \
  --assignee_id <user_id>

# 更新迭代状态
python3 scripts/sprints.py update \
  --project_id <id> \
  --sprint_id <sprint_id> \
  --status in_progress
```

### 评论管理

```bash
# 为工作项添加评论
python3 scripts/comments.py create \
  --type work_item \
  --id <workitem_id> \
  --content "已复现，优先处理"

# 获取评论列表
python3 scripts/comments.py list --type work_item --id <workitem_id>

# 删除评论
python3 scripts/comments.py delete <comment_id>

# principal_type 允许值: work_item / test_run / test_case / ticket / idea / page
```

### 工时管理

```bash
# 获取工时类型列表（先拿到 type_id）
python3 scripts/workloads.py types

# 登记工时
python3 scripts/workloads.py create \
  --principal_id <workitem_id> \
  --type_id <type_id> \
  --duration 4 \
  --report_at "2026-06-18" \
  --report_by_id <user_id>

# 查询工时列表
python3 scripts/workloads.py list --principal_id <workitem_id>

# 按日期范围查询
python3 scripts/workloads.py list --start_at "2026-06-01" --end_at "2026-06-30"

# 更新工时
python3 scripts/workloads.py update <workload_id> --duration 6

# 删除工时
python3 scripts/workloads.py delete <workload_id>
```

## API 参考

详见 `references/api_docs.md` 或访问 https://open.pingcode.com/

## 已实现的 API 端点

| 功能 | 脚本 | 端点 |
|------|------|------|
| 获取我的工作项 | get_my_tasks.py | `GET /v1/project/work_items` |
| 获取项目列表 | get_projects.py | `GET /v1/project/projects` |
| 获取项目工作项 | get_project_workitems.py | `GET /v1/project/work_items` |
| 创建工作项 | create_workitem.py | `POST /v1/project/work_items` |
| 更新工作项 | update_workitem.py | `PATCH /v1/project/work_items/{id}` |
| 获取/删除工作项 | get_workitem.py | `GET/DELETE /v1/project/work_items/{id}` |
| 获取企业成员 | get_members.py | `GET /v1/directory/users` |
| 迭代列表/创建/更新 | sprints.py | `GET/POST/PATCH /v1/project/projects/{id}/sprints` |
| 评论 CRUD | comments.py | `POST/GET/DELETE /v1/comments` |
| 工时 CRUD | workloads.py | `POST/GET/PATCH/DELETE /v1/workloads` |
| 生成周报 | generate_weekly_report.py | 综合接口 |

## 注意事项

1. **凭证安全**：凭证存储在 skill 根目录 `.env` 文件中，脚本通过 `_config.py` 自动加载。环境变量 `PINGCODE_CLIENT_ID` / `PINGCODE_CLIENT_SECRET` 可覆盖 `.env` 中的值
2. **频率限制**：每分钟最多 200 次请求
3. **Token 有效期**：30 天
4. **分页**：默认每页 30 条，最大 100 条
5. **工作项类型**：固定类型 `epic/feature/story/task/bug/issue` 用于 scrum/kanban 项目；瀑布项目使用自定义类型（通过获取工作项类型列表查询）
