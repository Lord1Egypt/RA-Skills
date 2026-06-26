---
name: meego-skill
version: 2.2.0
description: 飞书项目（Meego）全能力技能。提供工作项查询、状态流转、团队管理、工时统计、评论协作等全部能力。当用户提到以下场景时激活：查询在途工作项、查缺陷/任务/需求详情、查团队成员、查工时记录、添加评论、创建工作项、修改工作项字段、查询工作项流转状态、查成员排期、查询视图和图表、查询工作项字段配置、查询项目空间信息、按条件筛选工作项。面向小白：逐项操作指引；面向AI：每个接口均有参数说明、示例和异常处理。
---

# Meego Skill（飞书项目全能力技能）

> 本技能通过飞书项目官方 MCP 接口提供全部能力。
> 底层调用工具：`meego-mcporter`（MCP over stdio 协议），凭证通过 OAuth 管理。

---

## 一、完整功能索引

| # | 功能场景 | 核心工具 | 需要 OAuth |
|---|---------|---------|-----------|
| 1 | 查我的在途工作项 | `list_todo` | ✅ |
| 2 | 查任意工作项详情 | `get_workitem_brief` | ✅ |
| 3 | 查工作项节点/子任务 | `get_node_detail` | ✅ |
| 4 | 流转工作项状态 | `get_transitable_states` + `update_field` | ✅ |
| 5 | 添加评论 | `add_comment` | ✅ |
| 6 | 创建工作项 | `create_workitem` | ✅ |
| 7 | 修改工作项字段 | `update_field` | ✅ |
| 8 | 查工时记录 | `get_workitem_man_hour_records` | ✅ |
| 9 | 查字段配置 | `list_workitem_field_config` | ✅ |
| 10 | 查工作项类型 | `list_workitem_types` | ✅ |
| 11 | 查团队成员 | `list_team_members` / `list_project_team` | ✅ |
| 12 | 查成员排期 | `list_schedule` | ✅ |
| 13 | 查项目空间信息 | `search_project_info` | ✅ |
| 14 | 按标题搜索视图 | `search_view_by_title` | ✅ |
| 15 | 查视图下图表 | `list_charts` / `get_chart_detail` | ✅ |
| 16 | MQL 自由查询 | `search_by_mql` | ✅ |
| 17 | 查工作项操作记录 | `get_workitem_op_record` | ✅ |
| 18 | 关联工作项查询 | `list_related_workitems` | ✅ |

---

## 二、前置条件（逐项检查）

| 依赖 | 要求 | 检查命令 | 检查失败怎么做 |
|------|------|---------|-------------|
| Node.js | ≥ 16 | `node --version` | 升级 Node.js |
| npm | 任意版本 | `npm --version` | 随 Node.js 自动安装 |
| mcporter | 已安装并可用 | `mcporter --help` | 见安装步骤第一步 |
| meego-mcporter | 已安装并可用 | `meego-mcporter --help` 或 `npx @lark-project/meego-mcporter --help` | 见安装步骤第二步 |
| OAuth 凭证 | 已完成授权并同步到服务器 | `meego-mcporter call meego list_todo --args '{}'` | 见安装步骤第三步 |
| 飞书项目 | 已开通企业版 | 联系管理员 | — |

**一键检查脚本：**
```bash
node --version && mcporter --help && meego-mcporter --help && echo "✅ 工具就绪"
```

---

## 三、完整安装步骤（两步完成）

> **核心原理：** `meego-mcporter` 通过 MCP over stdio 协议连接飞书项目 MCP 服务器，OAuth 授权由 `mcporter` 管理。安装只需两步：装工具 → 做授权。

### 第一步：安装工具（服务器 + 本地电脑都要装）

**服务器端（已有 Node.js 环境）：**
```bash
npm install -g mcporter
npm install -g @lark-project/meego-mcporter
```

**本地电脑（用于完成 OAuth 授权）：**
```powershell
# Windows PowerShell / 命令提示符
npm install -g mcporter
npm install -g @lark-project/meego-mcporter
```

```bash
# Mac/Linux 终端
sudo npm install -g mcporter
sudo npm install -g @lark-project/meego-mcporter
```

验证安装（服务器或本地都行）：
```bash
meego-mcporter --help
```

---

### 第二步：在本地电脑完成 OAuth 授权（关键步骤）

**第一步：创建配置文件**

在本地电脑新建 `meego-config.json`（内容固定，服务器地址不变）：

```json
{
  "mcpServers": {
    "meego": {
      "url": "https://project.feishu.cn/mcp_server/v1",
      "auth": "oauth"
    }
  }
}
```

> ⚠️ `meego` 是服务器名称，不要改。`url` 和 `auth` 字段固定，不需要填 App ID/Secret。

**第二步：触发授权**
```powershell
npx @lark-project/meego-mcporter auth meego --config meego-config.json
```
```bash
# Mac/Linux
npx @lark-project/meego-mcporter auth meego --config ./meego-config.json
```

这个命令会：
1. 启动一个本地 HTTP 服务监听 callback
2. 自动打开浏览器跳转发书授权页面
3. 用户在飞书点击"授权"后，callback 收到 code
4. 自动用 code 换取 access_token + refresh_token
5. **自动保存到** `~/.mcporter/credentials.json`（本地电脑）

**预期输出：**
```
Opening browser for OAuth authorization...
Authorization received. Exchanging for tokens...
Success! Credentials saved to ~/.mcporter/credentials.json
```

**第三步：把 credentials 上传到服务器**

授权完成后，在本地电脑执行：
```bash
type %USERPROFILE%\.mcporter\credentials.json
# Windows PowerShell:
# Get-Content $env:USERPROFILE\.mcporter\credentials.json
```

```bash
# Mac/Linux:
cat ~/.mcporter/credentials.json
```

把完整 JSON 内容发给 AI助手（粘贴到聊天里），AI会自动写入服务器的 `/root/.mcporter/credentials.json`。

> **服务器credentials路径：** `/root/.mcporter/credentials.json`（Linux服务器）
> **本地 credentials 路径：** `~/.mcporter/credentials.json`

---

### 验证连接

服务器上执行：
```bash
meego-mcporter call meego list_todo --args '{}'
```

预期：返回当前用户在飞书项目中的在途工作项列表。

✅ 全部通过 → 配置完成！

---

## 四、调用格式详解

### 标准格式（服务器上直接用）

```bash
meego-mcporter call meego <工具名> --args '<JSON参数>'
```

凭证自动从 `/root/.mcporter/credentials.json` 读取，无需每次传 `--config`。

> ⚠️ **JSON 参数必须用单引号包裹**，外层用双引号。这是 shell 转义要求。

### 传 URL 自动解析（最简单）

如果用户提供了一个 Meego 链接，直接把完整 URL 作为 `url` 参数传入，系统自动解析 project_key 和 work_item_id：

```bash
meego-mcporter call meego get_workitem_brief --args '{
  "url": "https://project.feishu.cn/more/more?workitem_id=123456&project_key=你的project_key"
}'
```

### 分页查询

所有 `list` 类工具支持分页，用 `page_num`（从1开始）：

```bash
meego-mcporter call meego list_todo --args '{"page_num": 2}'
```

---

## 五、每个场景的完整调用示例

### 场景 1：查我的在途工作项（最高频）

```bash
meego-mcporter call meego list_todo --args '{}'
```

返回：工作项ID、名称、类型、当前节点、计划开始/结束时间。
分页：每页50条。

---

### 场景 2：查任意工作项详情

```bash
meego-mcporter call meego get_workitem_brief --args '{
  "project_key": "你的project_key",
  "work_item_id": 123456
}' --config /workspace/meego-config.json
```

也支持直接传 URL：
```bash
meego-mcporter call meego get_workitem_brief --args '{
  "url": "https://project.feishu.cn/more/more?workitem_id=123456&project_key=你的project_key"
}' --config /workspace/meego-config.json
```

---

### 场景 3：查工作项节点（子任务）

```bash
meego-mcporter call meego get_node_detail --args '{
  "project_key": "你的project_key",
  "work_item_id": 123456,
  "need_sub_task": true
}' --config /workspace/meego-config.json
```

---

### 场景 4：流转工作项状态（三步完成）

**第一步：查可流转到哪些状态**
```bash
meego-mcporter call meego get_transitable_states --args '{
  "project_key": "你的project_key",
  "work_item_id": 123456,
  "work_item_type": "issue",
  "user_key": "你的user_key（从 list_todo 返回中获取）"
}' --config /workspace/meego-config.json
```

**第二步：查目标状态需要填哪些必填字段**
```bash
meego-mcporter call meego get_transition_required --args '{
  "project_key": "你的project_key",
  "work_item_id": 123456,
  "state_key": "RESOLVED"
}' --config /workspace/meego-config.json
```

**第三步：执行流转**
```bash
meego-mcporter call meego update_field --args '{
  "project_key": "你的project_key",
  "work_item_id": 123456,
  "fields": ["work_item_status:RESOLVED"]
}' --config /workspace/meego-config.json
```

---

### 场景 5：添加评论

```bash
meego-mcporter call meego add_comment --args '{
  "project_key": "你的project_key",
  "work_item_id": 123456,
  "comment_content": "## 修复方案\n\n已定位原因，正在修复中，请稍候。\n\n@负责人 请review"
}' --config /workspace/meego-config.json
```

评论内容支持 Markdown。

---

### 场景 6：创建工作项

**第一步：查该类型的必填字段（必须先做）**
```bash
meego-mcporter call meego get_workitem_field_meta --args '{
  "project_key": "你的project_key",
  "work_item_type": "issue"
}' --config /workspace/meego-config.json
```

**第二步：创建工作项**
```bash
meego-mcporter call meego create_workitem --args '{
  "project_key": "你的project_key",
  "work_item_type": "issue",
  "fields": [
    "name:缺陷标题",
    "priority:1",
    "severity:2",
    "work_item_status:OPEN"
  ]
}' --config /workspace/meego-config.json
```

> 字段 key 从第一步返回获取。常见 key：`name`（标题）、`priority`（优先级）、`severity`（严重程度）、`work_item_status`（状态）。

---

### 场景 7：修改工作项字段

```bash
# 单个字段
meego-mcporter call meego update_field --args '{
  "project_key": "你的project_key",
  "work_item_id": 123456,
  "fields": ["priority:0"]
}' --config /workspace/meego-config.json

# 多个字段
meego-mcporter call meego update_field --args '{
  "project_key": "你的project_key",
  "work_item_id": 123456,
  "fields": ["priority:1", "name:新标题"]
}' --config /workspace/meego-config.json
```

---

### 场景 8：查工时记录

```bash
meego-mcporter call meego get_workitem_man_hour_records --args '{
  "project_key": "你的project_key",
  "work_item_id": 123456,
  "work_item_type": "issue"
}' --config /workspace/meego-config.json
```

---

### 场景 9：查工作项字段配置

```bash
# 查某类型的完整字段列表（含选项值）
meego-mcporter call meego list_workitem_field_config --args '{
  "project_key": "你的project_key",
  "work_item_type": "issue",
  "page_num": 1
}' --config /workspace/meego-config.json

# 模糊搜索字段（找负责人的字段key等）
meego-mcporter call meego list_node_field_config --args '{
  "project_key": "你的project_key",
  "work_item_type": "issue",
  "query": "负责人"
}' --config /workspace/meego-config.json
```

---

### 场景 10：查工作项类型

```bash
meego-mcporter call meego list_workitem_types --args '{
  "project_key": "你的project_key"
}' --config /workspace/meego-config.json
```

返回：`type_key`（如 `issue`/`story`/`sub_task`）。

---

### 场景 11：查团队成员

```bash
# 查项目下所有团队
meego-mcporter call meego list_project_team --args '{
  "project_key": "你的project_key"
}' --config /workspace/meego-config.json

# 查某团队的成员
meego-mcporter call meego list_team_members --args '{
  "project_key": "你的project_key",
  "team_id": "team_xxx"
}' --config /workspace/meego-config.json
```

---

### 场景 12：查成员排期

```bash
meego-mcporter call meego list_schedule --args '{
  "project_key": "你的project_key",
  "user_keys": ["你的user_key"],
  "start_time": "2026-03-01",
  "end_time": "2026-03-31"
}' --config /workspace/meego-config.json
```

- 时间格式：`YYYY-MM-DD`，最大范围3个月
- `user_keys`：从 `list_team_members` 或 `list_todo` 中获取的 user_key 列表

---

### 场景 13：查项目空间信息（获取 project_key）

```bash
# 用项目中文名查询
meego-mcporter call meego search_project_info --args '{
  "project_key": "你的项目名称"
}' --config /workspace/meego-config.json

# 用 simple_name 查询
meego-mcporter call meego search_project_info --args '{
  "project_key": "your_simple_name"
}' --config /workspace/meego-config.json
```

返回：`project_key`（数字）、`simple_name`、`project_name`。

---

### 场景 14：MQL 自由查询

> ⚠️ MQL 语法严格，字段名必须与 API 字段名完全一致。先用 `list_workitem_field_config` 查实名字段 key 再填入。

```bash
# 查所有 OPEN 状态的缺陷
meego-mcporter call meego search_by_mql --args '{
  "project_key": "你的project_key",
  "mql": "work_item_status = \"OPEN\" and work_item_type_key = \"issue\""
}' --config /workspace/meego-config.json

# 查高优先级在途缺陷
meego-mcporter call meego search_by_mql --args '{
  "project_key": "你的project_key",
  "mql": "priority = \"0\" and work_item_status not in (\"CLOSED\",\"REJECTED\")"
}' --config /workspace/meego-config.json

# 分页查询
meego-mcporter call meego search_by_mql --args '{
  "project_key": "你的project_key",
  "mql": "work_item_status not in (\"CLOSED\")",
  "session_id": "上次返回的session_id"
}' --config /workspace/meego-config.json
```

**issue（缺陷）状态值：**
| 状态 key | 含义 |
|---------|------|
| `OPEN` | 开始 |
| `IN PROGRESS` | 待确认 |
| `REPAIRING` | 待修复 |
| `IN REPAIRING` | 修复中 |
| `RESOLVED` | 已修复 |
| `VERIFYING` | 验证中 |
| `REOPENED` | 重新打开 |
| `CLOSED` | 已关闭 |
| `REJECTED` | 拒绝 |
| `ABONDONED` | 废弃 |

**常用字段速查：**
| 字段 | key | 示例值 |
|------|-----|--------|
| 名称 | `name` | 字符串 |
| 状态 | `work_item_status` | 见上方状态值 |
| 优先级 | `priority` | `0`（最高）/ `1`（高）/ `2`（中）/ `99`（低）|
| 严重程度 | `severity` | `1`（致命）/ `2`（严重）/ `3`（一般）/ `4`（轻微）|
| 当前负责人 | `current_status_operator` | user_key 字符串 |
| 创建者 | `owner` | user_key 字符串 |

---

## 六、异常处理（完整版）

### 运行时错误速查

| 错误现象 | 第一步排查 | 解决方案 |
|---------|----------|---------|
| `OAuth authorization required` / `xdg-open ENOENT` | 服务器无浏览器，OAuth 授权未完成 | 见下方「授权异常」专项处理 |
| `401 Unauthorized` | token 过期 | 见下方「token 刷新」专项处理 |
| `403 Forbidden` | 应用权限不足 | 飞书开放平台 → 权限管理申请权限 → 重新发版 |
| `404 Not Found` | project_key 或 work_item_id 错误 | 确认 URL 中参数正确 |
| `MCP error -32000: Connection closed` | OAuth token 无效或已过期 | 刷新 token，见下方流程 |
| `Permission denied` | 应用未被加入项目空间 | 项目管理员 → 设置 → 成员管理 → 添加应用 |
| `workflow:invalid_state` | 流转到不合法的状态 | 先用 `get_transitable_states` 查可流转状态 |
| `Command not found: meego-mcporter` | meego-mcporter 未安装 | `npm install -g @lark-project/meego-mcporter` |
| MQL `syntax error` | 字段名拼写错误 | 用 `list_workitem_field_config` 确认字段 key |
| 工具调用无输出/超时 | token 失效 | 刷新 token |

---

### 专项一：授权异常（最常见）

**错误 1：`xdg-open ENOENT`（服务器无浏览器环境）**

服务器环境没有浏览器，无法自动打开授权页面。解决流程：

**第一步：本地完成授权**
```powershell
# 本地电脑执行（Windows）
npx @lark-project/meego-mcporter auth meego --config meego-config.json
```
```bash
# Mac/Linux
npx @lark-project/meego-mcporter auth meego --config ./meego-config.json
```

**第二步：导出 credentials**
```powershell
# 本地电脑执行
type $env:USERPROFILE\.mcporter\credentials.json
```

**第三步：发给 AI助手**，AI自动写入服务器 `/root/.mcporter/credentials.json`

---

**错误 2：`OAuth authorization required for 'meego'`（token 不存在）**

服务器上 credentials 文件缺失或内容为空。同上流程：本地完成授权 → 导出 credentials → 发给 AI。

---

### 专项二：Token 过期处理

**错误：`MCP error -32000: Connection closed` 或 `401 Unauthorized`**

**原因：** OAuth access_token 有效期 2 小时，refresh_token 有效期 30 天。

**自动刷新（推荐）：**

本地完成一次 `meego-mcporter auth meego --config meego-config.json`（会覆盖 credentials），然后重新导出 credentials 上传到服务器。

**手动刷新（无浏览器时）：**

access_token 过期后，refresh_token 还在有效期内（30天），直接替换 credentials 中的 access_token 即可：

```powershell
# 本地执行，导出最新 credentials
type $env:USERPROFILE\.mcporter\credentials.json
```

把新 credentials 发给 AI助手 更新到服务器。

---

### 专项三：权限类错误

| 错误信息 | 原因 | 解决方法 |
|---------|------|---------|
| `permission denied` | 应用未开通飞书项目权限 | 飞书开放平台 → 权限管理 → 申请 `project` 权限 → 重新发版 |
| `project:workitem:not_found` | 应用未被加入项目空间 | 项目管理员 → 设置 → 成员管理 → 添加应用 |
| `workflow:invalid_state` | 流转到不合法的状态 | 先用 `get_transitable_states` 查可流转状态 |

---

### 专项四：网络与连接错误

| 错误信息 | 原因 | 解决方法 |
|---------|------|---------|
| `Connection timeout` | 网络超时 | 确认服务器可访问 `project.feishu.cn` |
| `HTTP 403` | IP 白名单限制 | 飞书后台 → 安全设置 → 关闭 IP 白名单 |
| `HTTP 429` | 请求过快 | 降低调用频率，加 `sleep 1` 延时 |

---

## 七、调试与排障流程图

```
工具调用报错
  │
  ├─ OAuth authorization required / xdg-open ENOENT
  │     → 本地执行 auth → 导出 credentials → 发给 AI 更新服务器
  │
  ├─ MCP error -32000: Connection closed / 401 Unauthorized
  │     → token 过期
  │     → 本地执行 auth 刷新 → 新 credentials 发给 AI
  │
  ├─ 403 Forbidden / permission denied
  │     ├─ 应用权限未申请 → 飞书开放平台申请 + 发版
  │     └─ 应用未加入项目 → 项目设置 → 成员管理 → 添加应用
  │
  ├─ 404 Not Found
  │     → 检查 project_key 和 work_item_id 是否正确
  │
  ├─ MQL syntax error
  │     → 字段名拼写错误，用 list_workitem_field_config 确认 key
  │
  └─ 返回空列表
        → 可能无数据（非错误），确认查询条件是否合理
```

---

## 八、凭证与权限体系

### 凭证文件

| 环境 | 文件路径 | 用途 |
|------|---------|------|
| 服务器（Linux） | `/root/.mcporter/credentials.json` | OAuth token（AI助手写入） |
| 本地电脑 | `~/.mcporter/credentials.json` | OAuth token（auth 命令自动写入） |

> **配置格式不是** `app_id + app_secret` JSON，而是 OAuth credentials JSON（由飞书授权流程自动生成）。

### 权限申请检查表

| 需要的功能 | 必须申请的权限 | 是否需重新发版 |
|---------|-------------|-------------|
| 工作项读写 | `project:workitem` | ✅ |
| 状态流转 | `project:workflowstatus` | ✅ |
| 评论 | `project:comment` | ✅ |
| 成员查询 | `project:member` | ✅ |
| 排期查询 | `project:schedule` | ✅ |
| 视图查询 | `project:view` | ✅ |
| 基础读写 | `project` | ✅ |

---

## 九、参考文件索引

| 文件 | 内容 |
|------|------|
| references/tools.md | 所有工具完整清单（40+ 接口）|
| references/mql.md | MQL 查询语法与完整示例 |
| references/fields.md | 工作项字段配置参考 |
