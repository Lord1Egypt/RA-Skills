# MQL 查询语法参考

## 基本格式

```bash
npx @lark-project/meego-mcporter call meego search_by_mql --args '{"project_key":"你的project_key","mql":"<MQL语句>"}' --config /workspace/meego-config.json
```

## 重要提示

⚠️ **MQL 语法严格，字段名必须与 API 字段名完全一致。** 建议先通过 `list_workitem_field_config` 确认实际字段 key 再填入查询。

已知问题：
- MQL 语法报错通常提示 `syntax error at position X`，说明字段名或运算符不被识别
- 部分字段在 MQL 层不支持（建议用 `list_todo` + URL 解析代替）
- 最可靠的查询方式还是 `list_todo`（无需知道字段名）和直接传 `url` 参数

## 可用运算符

| 运算符 | 示例 | 说明 |
|--------|------|------|
| `=` | `status = "OPEN"` | 相等比较 |
| `!=` | `priority != "0"` | 不等比较 |
| `in` | `status in ("OPEN","IN PROGRESS")` | 枚举匹配 |
| `not in` | `type not in ("story")` | 排除 |
| `contains` | `name contains "缺陷"` | 模糊包含（字符串字段） |
| `and` / `or` | `status = "OPEN" and priority = "0"` | 逻辑组合 |

## 常用字段速查（你的项目名称 issue 类型）

| 字段含义 | 字段 key | 示例值 |
|---------|---------|--------|
| 缺陷名称 | `name` | 字符串 |
| 缺陷状态 | `work_item_status` | `OPEN`/`IN PROGRESS`/`REPAIRING`/`IN REPAIRING`/`RESOLVED`/`VERIFYING`/`REOPENED`/`CLOSED`/`REJECTED`/`ABONDONED` |
| 优先级 | `priority` | `0`（最高）/ `1`（高）/ `2`（中）/ `99`（低） |
| 严重程度 | `severity` | `1`（致命）/ `2`（严重）/ `3`（一般）/ `4`（轻微） |
| 当前负责人 | `current_status_operator` | open_id 字符串 |
| 创建者 | `owner` | open_id 字符串 |
| 发现阶段 | `issue_stage` | `stage_test`/`stage_online` 等 |
| 缺陷类型 | `field_f76015` | `rrq3w4u7s`（代码问题）等 |
| 规划版本 | `planning_version` | 工作项关联ID |
| 规划迭代 | `planning_sprint` | 工作项关联ID |
| 工作项类型 | `work_item_type_key` | `issue`/`story`/`sub_task` 等 |
| 所属空间 | `owned_project` | project_key |

## 状态值参考

### issue（缺陷）状态
```
OPEN          → 开始
IN PROGRESS   → 待确认
REPAIRING     → 待修复
IN REPAIRING  → 修复中
RESOLVED      → 已修复
VERIFYING     → 验证中
REOPENED      → 重新打开
CLOSED        → 已关闭
REJECTED      → 拒绝
ABONDONED     → 废弃
ugugjneny     → 挂起
systemEnded   → 已终止
```

### sub_task（任务）状态
```
unfinished → 未完成
done       → 已完成
```

## 示例查询

```mql
-- 查所有 OPEN 状态的缺陷
name contains "登录" and work_item_status = "OPEN"

-- 查负责人是某人的所有在途工作项
current_status_operator = "ou_xxx" and work_item_status != "CLOSED"

-- 查高优先级缺陷
priority = "0" and work_item_status not in ("CLOSED","REJECTED","ABONDONED")

-- 查所有未关闭的 issue
work_item_type_key = "issue" and work_item_status not in ("CLOSED","REJECTED")
```

## 分页查询

```bash
# 第一次查询
npx @lark-project/meego-mcporter call meego search_by_mql --args '{"project_key":"你的project_key","mql":"work_item_status not in (\"CLOSED\")"}' --config /workspace/meego-config.json

# 第二次查询（取上次返回的 session_id）
npx @lark-project/meego-mcporter call meego search_by_mql --args '{"project_key":"你的project_key","mql":"work_item_status not in (\"CLOSED\")","session_id":"上次返回的session_id"}' --config /workspace/meego-config.json
```

## 推荐替代方案

MQL 语法复杂且易错，以下场景推荐用更简单的替代方式：

| 场景 | 推荐替代 | 原因 |
|------|---------|------|
| 查我的在途工作项 | `list_todo --args '{}'` | 无需字段名，自动过滤当前用户 |
| 查任意工作项详情 | 传 `url` 参数 | 自动解析所有参数 |
| 查某类型所有工作项 | `list_todo` + 过滤 | 稳定可靠 |
| 查团队成员 | `list_project_team` + `list_team_members` | 直接返回列表 |
