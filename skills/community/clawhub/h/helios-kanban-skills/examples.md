# Examples

## Setup

```bash
export HELIOS_KANBAN_URL="http://100.64.0.5:7964"
export HELIOS_KANBAN_PROJECT_ID="a1b2c3d4-e5f6-7890-abcd-ef1234567890"
export HELIOS_KANBAN_REPO_ID="bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb"
export HELIOS_KANBAN_ITERATION="260717"
HK="bash scripts/hk.sh"
```

## Pick the right project

```bash
$HK projects
# read description + repos, then:
export HELIOS_KANBAN_PROJECT_ID="<chosen>"
# or set description for agents:
$HK projects update "$HELIOS_KANBAN_PROJECT_ID" --description "Kanban product — UI/API work only"
```

## Full remote loop

**User**: 260717 新建「修复登录」，基于 develop 跑起来

```bash
$HK branches "$HELIOS_KANBAN_REPO_ID" --query develop
$HK create-and-start "修复登录" --branch develop --desc "登录页 500 @coding-standards"
# or multi-repo:
# $HK start "<task_id>" --repo "$REPO_A" --repo "$REPO_B:main"
```

**User**: 怎么样了？

```bash
$HK status "<task_id>"
# running, last_attempt_failed, workspace summaries (files/lines, pending approval)
```

**User**: 再跟它说加单测

```bash
$HK follow-up "<task_id>" 请补充单元测试并保持 API 兼容
# mode=follow_up | queued
```

**User**: 有审批卡着

```bash
$HK approvals
$HK approve "<approval_id>" --process "<execution_process_id>"
# or: $HK deny "<approval_id>" --process "<ep_id>" --reason "too risky"
```

**User**: 停掉 / 取消

```bash
$HK workspaces --task "<task_id>"
$HK stop "<workspace_id>"
$HK tasks cancel "<task_id>"   # also stops workspaces
```

**User**: 找一下登录相关的 todo

```bash
$HK tasks list --status todo --query 登录
```

**User**: 建个紧急任务修线上 500，修完降到中

```bash
$HK tasks create "修复线上 500" --priority urgent
$HK tasks list --priority urgent
$HK tasks update "<task_id>" --priority medium
```

## curl snippets

```bash
curl -s "$HELIOS_KANBAN_URL/api/health" | jq .
curl -s "$HELIOS_KANBAN_URL/api/info" | jq '.data.config.executor_profile'
curl -s "$HELIOS_KANBAN_URL/api/approvals" | jq '.data'
curl -s "$HELIOS_KANBAN_URL/api/repos/$HELIOS_KANBAN_REPO_ID/branches" | jq '.data[].name'
```
