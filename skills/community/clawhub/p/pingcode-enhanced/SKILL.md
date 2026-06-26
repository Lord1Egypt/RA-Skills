---
name: pingcode
description: PingCode 研发管理平台 API 集成。支持查询工作项、测试库、项目进度、组织架构、知识库、DevOps 等。
metadata:
  openclaw:
    requires:
      env:
        - PINGCODE_CLIENT_ID
        - PINGCODE_CLIENT_SECRET
---

# PingCode Skill

日常用 PingCode 管项目进度和需求迭代，用这个技能让 AI 直接帮忙查工作项、看进度、生成周报。

## 前置条件

1. 在 PingCode 企业后台创建应用，获取 `Client ID` 和 `Client Secret`
2. 配置应用的数据访问范围
3. 设置环境变量：

```bash
export PINGCODE_CLIENT_ID="your_client_id"
export PINGCODE_CLIENT_SECRET="your_client_secret"
```

---

## 1️⃣ 项目管理

日常用得最多的是查迭代进度和项目概况。

```bash
# 查看所有项目
python3 scripts/query_projects.py

# 搜项目
python3 scripts/query_projects.py --name "项目名称"

# 项目详情（含负责人、时间等）
python3 scripts/query_projects.py --project_id xxx --detail

# 看迭代（Sprint）
python3 scripts/query_projects.py --project_id xxx --sprints
python3 scripts/query_projects.py --all_projects_sprints --sprints

# 看发布（Release）
python3 scripts/query_projects.py --project_id xxx --releases

# 项目成员
python3 scripts/query_projects.py --project_id xxx --members
```

---

## 2️⃣ 工作项 (Work Items)

工作项是每天最常用的——看自己的任务、查 Bug、统计进度。

### 我的工作项

```bash
python3 scripts/get_my_tasks.py
```

### 项目工作项

```bash
python3 scripts/get_project_workitems.py --project_name "项目名称"
python3 scripts/get_project_workitems.py --project_id abc123 --json
```

### 高级查询（推荐用这个，比上面的灵活）

```bash
# 项目统计
python3 scripts/query_workitems.py --project_name "项目名称"

# 只看 bug
python3 scripts/query_workitems.py --project_name "项目名称" --type bug

# 未完成
python3 scripts/query_workitems.py --project_name "项目名称" --unfinished

# 全部未完成（跨项目）
python3 scripts/query_workitems.py --all_projects --unfinished

# 按人筛选
python3 scripts/query_workitems.py --project_name "项目名称" --assignee "张三"

# 最近7天新增
python3 scripts/query_workitems.py --project_name "项目名称" --recent 7
```

### 更新工作项

```bash
# 改负责人
python3 scripts/update_workitem.py --workitem_id abc --assignee anytao

# 改时间
python3 scripts/update_workitem.py --workitem_id abc --start_date "2026-03-12" --due_date "2026-03-20"

# 改优先级
python3 scripts/update_workitem.py --workitem_id abc --priority "高"

# 改状态
python3 scripts/update_workitem.py --workitem_id abc --status "进行中"
```

### 生成周报

```bash
python3 scripts/generate_weekly_report.py
python3 scripts/generate_weekly_report.py --project_id xxx --project_name "项目名称"
python3 scripts/generate_weekly_report.py --output /tmp/weekly_report.md
```

---

## 3️⃣ 测试管理 (Test Hub)

### 测试库列表

```bash
# 全部测试库
python3 scripts/query_test_library.py

# 按名称搜
python3 scripts/query_test_library.py --library_name "项目名称"

# 含用例统计
python3 scripts/query_test_library.py --library_name "项目名称" --detail

# 按 ID
python3 scripts/query_test_library.py --library_id xxx --detail
```

输出示例：

```
📂 测试模块 (50):
   模块A: 30
   模块B: 13
   模块C: 12
   模块D: 8
   模块E: 5
   ...

📋 用例状态分布:
   设计: 260
```

### 测试执行记录

```bash
python3 scripts/query_test_runs.py                           # 最近执行
python3 scripts/query_test_runs.py --library_name "项目名称" # 按测试库
python3 scripts/query_test_runs.py --days 7                  # 最近7天
python3 scripts/query_test_runs.py --detail                  # 详细结果
```

---

## 4️⃣ 组织架构

```bash
# 所有用户
python3 scripts/query_users.py

# 按姓名搜索
python3 scripts/query_users.py --search "蔡"

# 用户详情（邮箱/手机/职位）
python3 scripts/query_users.py --user_id xxx

# 只跑某个参数
python3 scripts/query_users.py --departments   # 部门
python3 scripts/query_users.py --groups        # 团队
python3 scripts/query_users.py --roles         # 角色
python3 scripts/query_users.py --detail        # 全部详细信息
```

---

## 5️⃣ 知识管理 (Wiki)

```bash
python3 scripts/query_wiki.py                               # 空间列表
python3 scripts/query_wiki.py --space_id xxx                # 空间下页面
python3 scripts/query_wiki.py --space_id xxx --search "关键字"   # 搜页面
python3 scripts/query_wiki.py --page_id xxx                 # 页面详情
python3 scripts/query_wiki.py --page_id xxx --content       # 正文内容
```

---

## 6️⃣ 动态 & 评论 & 工时

看工作项的变更历史、评论和工时记录。

```bash
python3 scripts/query_activities.py --work_item_id xxx              # 动态
python3 scripts/query_activities.py --work_item_id xxx --comments  # 评论
python3 scripts/query_activities.py --work_item_id xxx --hours     # 工时
python3 scripts/query_activities.py --work_item_id xxx --followers # 关注人
python3 scripts/query_activities.py --work_item_id xxx --relations # 关联项
```

---

## 7️⃣ DevOps 集成

代码仓库、提交记录、PR、构建部署。

```bash
python3 scripts/query_devops.py --repos     # 代码仓库
python3 scripts/query_devops.py --commits  # 提交记录
python3 scripts/query_devops.py --pr       # Pull Request
python3 scripts/query_devops.py --builds   # 构建记录
python3 scripts/query_devops.py --deploys  # 部署记录
```

---

## 8️⃣ 全局看板

```bash
python3 scripts/pingcode_dashboard.py                    # 所有项目
python3 scripts/pingcode_dashboard.py --project "项目名称"   # 按项目
python3 scripts/pingcode_dashboard.py --test             # 含测试统计
```

---

## 脚本清单

| 脚本 | 说明 |
|------|------|
| `query_projects.py` | 项目、迭代、发布、成员 |
| `get_projects.py` | 获取项目列表（原始版本，功能少但稳定） |
| `get_my_tasks.py` | 我负责的工作项 |
| `get_project_workitems.py` | 项目工作项（原始版本） |
| `query_workitems.py` | 工作项高级查询（推荐，功能全面） |
| `update_workitem.py` | 更新工作项字段 |
| `generate_weekly_report.py` | 周报生成（我们内部每周一用） |
| `query_test_library.py` | 测试库 + 用例查询 |
| `query_test_runs.py` | 测试执行记录 |
| `query_users.py` | 用户/部门/团队/角色 |
| `query_wiki.py` | 知识库 |
| `query_activities.py` | 动态/评论/工时 |
| `query_devops.py` | DevOps 集成 |
| `pingcode_dashboard.py` | 全局看板 |
