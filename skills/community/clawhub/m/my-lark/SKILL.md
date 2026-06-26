---
name: my-lark
version: 3.0.0
description: 飞书全能力技能。基于飞书官方工具服务，支持消息、群组、云文档、云盘、知识库、日历、审批、多维表格、电子表格、画板、通讯录全部模块。面向小白：安装即用，每一步都有操作指引；面向AI：每个接口均有调用示例、参数说明、权限要求和异常处理。触发词：发消息、搜索文档、查日历、查审批、建日程、拉群列表等。
---

# My Lark（飞书全能力技能）

> 凭证统一存放在 `/workspace/.lark_tokens.json`，技能本身不含任何凭证。

---

## 一、完整功能索引

| # | 功能场景 | 核心工具 | 凭证要求 |
|---|---------|---------|---------|
| 1 | 发消息到群 | `im_v1_message_create` | app_id + app_secret |
| 2 | 获取群聊列表 | `im_v1_chat_list` | app_id + app_secret |
| 3 | 创建群聊 | `im_v1_chat_create` | app_id + app_secret |
| 4 | 搜索云文档 | `docx_builtin_search` | user_access_token |
| 5 | 读取文档内容 | `docx_v1_document_rawContent` | user_access_token |
| 6 | 读写电子表格 | `sheets_v2_spreadsheets_values_*` | app_id + app_secret |
| 7 | 搜索知识库 | `wiki_v1_node_search` | user_access_token |
| 8 | 查询多维表格 | `bitable_v1_appTableRecord_*` | app_id + app_secret |
| 9 | 查日历/建日程 | `calendar_v4_events` | app_id + app_secret |
| 10 | 查询通讯录 | `contact_v3_user_batchGetId` | app_id + app_secret |
| 11 | 提交/查审批 | `approval_v4_instances_*` | app_id + app_secret |
| 12 | 云盘文件管理 | `drive_explorer_v2_fileList` | app_id + app_secret |
| 13 | 下载画板图片 | `board/v1/whiteboards/:id/download_as_image` | app_id + app_secret |
| 14 | 解析 PlantUML/Mermaid | `board/v1/whiteboards/:id/nodes/plantuml` | app_id + app_secret |

---

## 二、前置条件（逐项检查）

| 依赖 | 最低要求 | 检查命令 | 检查失败怎么做 |
|------|---------|---------|-------------|
| Python | ≥ 3.8（建议 ≥ 3.10） | `python3 --version` | 升级 Python：`apt update && apt install python3.11` |
| Node.js | ≥ 16 | `node --version` | 升级 Node.js |
| npm | 任意版本 | `npm --version` | 随 Node.js 自动安装 |
| lark-mcp | 已安装并可用 | `lark-mcp --help` | 见安装步骤第三步 |
| 飞书应用 | 已创建并发布 | 飞书开放平台控制台 | 见安装步骤第一步 |
| 凭证文件 | 已配置 | `cat /workspace/.lark_tokens.json` | 见安装步骤第二步 |

**一键检查脚本（复制运行）：**
```bash
python3 --version && node --version && lark-mcp --help && cat /workspace/.lark_tokens.json | python3 -m json.tool && echo "✅ 全部就绪"
```

---

## 三、完整安装步骤

### 第一步：创建飞书应用（账号要求：飞书管理员）

**操作路径：**
1. 打开 [飞书开放平台](https://open.feishu.cn/app) → 用管理员账号登录
2. 点击「创建企业自建应用」→ 填写应用名称（如"MyLark Bot"）→ 点击创建
3. 进入应用 → 左侧「应用功能」→「机器人」→ 点击「开启」
4. 左侧「凭证与基础信息」→ 复制 **App ID** 和 **App Secret**（备用）
5. 左侧「权限管理」→ 按需申请以下权限（见下方权限速查表）
6. 左侧「版本管理与发布」→ 创建版本 → 申请发布 → 管理员审批

**必须申请的权限（消息/群组/日历/通讯录/审批/多维表格）：**
| 权限名 | 用途 |
|--------|------|
| `im:message` | 发/查消息 |
| `im:chat` | 群管理 |
| `im:chat:read` | 读取群信息 |
| `calendar` | 日历读写 |
| `calendar:calendar:read` | 读日历 |
| `contact` | 通讯录读写 |
| `approval` | 审批读写 |

**知识库/云文档额外权限（需 User Token）：**
| 权限名 | 用途 |
|--------|------|
| `wiki` | 知识库读写 |
| `docx` | 云文档读写 |

> 💡 权限申请后需重新发布版本才能生效。

---

### 第二步：配置凭证文件

在 `/workspace/.lark_tokens.json`（注意是 `/workspace/` 不是 `~`）创建文件：

```json
{
  "app_id": "cli_xxxxxxxxxxxxxxxx",
  "app_secret": "your_app_secret_here",
  "user_access_token": "your_user_access_token_here"
}
```

**如何获取 user_access_token（仅知识库/云文档需要）：**

方式 A（简单）：在飞书开放平台 → 应用 → 权限管理 → 开通「以应用身份获取用户授权」

方式 B（标准 OAuth）：
1. 构造授权 URL：
```
https://open.feishu.cn/open-apis/authen/v1/authorize?app_id=cli_xxx&redirect_uri=http%3A%2F%2Flocalhost%3A8080%2Fcallback&state=randomstring
```
2. 浏览器打开 → 扫码授权 → 回调获取 `code`
3. 用 code 换取 token：
```bash
curl -X POST 'https://open.feishu.cn/open-apis/authen/v1/oidc/access_token' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer USER_ACCESS_TOKEN' \
  -d '{"grant_type": "authorization_code", "code": "获取的code"}'
```

---

### 第三步：安装 lark-mcp CLI

```bash
npm install -g @larksuite/lark-mcp
```

验证安装成功：
```bash
lark-mcp --help
# 出现帮助信息即表示安装成功
```

---

### 第四步：验证配置（逐项测试）

```bash
# 1. 确认凭证文件存在且格式正确
cat /workspace/.lark_tokens.json | python3 -m json.tool
# 应该输出格式化的 JSON，无报错

# 2. 测试 App Token（查询群列表）
python3 /workspace/skills/lark-skill/lark_mcp.py call im_v1_chat_list '{"page_size": 5}'
# 预期：返回群聊列表 JSON

# 3. 测试发消息（需要先把机器人拉入群）
python3 /workspace/skills/lark-skill/lark_mcp.py send oc_xxxxxxxxxxxxxxxx "机器人连通测试"
# 预期：飞书群收到消息

# 4. 测试通讯录查询
python3 /workspace/skills/lark-skill/lark_mcp.py call contact_v3_user_batchGetId '{}'
# 预期：返回用户信息
```

全部通过 → 配置完成 ✅

---

## 四、调用方式详解

### 标准格式

```bash
python3 /workspace/skills/lark-skill/lark_mcp.py <命令> [参数]
```

### 命令分类

#### A. 便捷命令（简化操作，无需记工具名）

| 命令 | 示例 | 说明 |
|------|------|------|
| `send <chat_id> <消息>` | `send oc_xxx "你好"` | 发文本消息到群 |
| `chats` | `chats` | 获取群聊列表（返回 chat_id） |
| `search <关键词>` | `search 项目报告` | 搜索云文档（需 User Token）|
| `doc <doc_token>` | `doc W7FOdr5aQo9F1` | 读取云文档全文（需 User Token）|
| `user <open_id>` | `user ou_xxx` | 查询单个用户信息 |
| `call <工具名> <json>` | `call im_v1_chat_list '{}'` | 调用任意底层工具 |

#### B. 底层工具调用格式

```bash
python3 /workspace/skills/lark-skill/lark_mcp.py call <工具名> '<JSON参数>'
```

> ⚠️ JSON 参数必须用**单引号**包裹，外层用双引号，这是 shell 转义要求。

---

## 五、每个场景的完整调用示例

### 场景 1：发文本消息到群

```bash
python3 /workspace/skills/lark-skill/lark_mcp.py send oc_xxxxxxxxxxxxxxxx "各位同事，明天上午10点开会，请准时参加。"
```

**前置**：机器人已在群里（未被禁言）

---

### 场景 2：获取群聊列表（找到 chat_id）

```bash
python3 /workspace/skills/lark-skill/lark_mcp.py call im_v1_chat_list '{"page_size": 20}'
```

返回示例：
```json
{
  "data": {
    "items": [
      {"chat_id": "oc_xxx", "name": "技术部群"},
      {"chat_id": "oc_yyy", "name": "项目协同群"}
    ]
  }
}
```
取 `chat_id` 填入 `send` 命令即可发消息。

---

### 场景 3：发送富文本消息

```bash
python3 /workspace/skills/lark-skill/lark_mcp.py call im_v1_message_create '{
  "receive_id": "oc_xxxxxxxxxxxxxxxx",
  "msg_type": "post",
  "content": "{\"zh_cn\":{\"title\":\"会议通知\",\"content\":[[{\"tag\":\"text\",\"text\":\"时间：明天上午10点\"},{\"tag\":\"text\",\"text\":\"地点：会议室A\"}]]}}"
}'
```

---

### 场景 4：搜索云文档

```bash
python3 /workspace/skills/lark-skill/lark_mcp.py search 项目报告
```

返回文档名称、token、链接等列表。

---

### 场景 5：读取云文档内容

```bash
# 先用 search 拿到 document_id，再读取内容
python3 /workspace/skills/lark-skill/lark_mcp.py doc W7FOdr5aQo9F1OxapR8cQkPpnNg
```

⚠️ 需要 `user_access_token` 配置正确。

---

### 场景 6：读写电子表格

```bash
# 读取单元格（A1:D5）
python3 /workspace/skills/lark-skill/lark_mcp.py call sheets_v2_spreadsheets_values_get '{
  "spreadsheetToken": "Shtxxxxxx",
  "range": "Sheet1!A1:D5"
}'

# 写入单元格
python3 /workspace/skills/lark-skill/lark_mcp.py call sheets_v2_spreadsheets_values_put '{
  "spreadsheetToken": "Shtxxxxxx",
  "range": "Sheet1!A1",
  "values": [["姓名", "部门", "状态"], ["张三", "技术部", "在职"]]
}'
```

---

### 场景 7：操作多维表格（增删改查记录）

```bash
# 列出所有多维表格
python3 /workspace/skills/lark-skill/lark_mcp.py call bitable_v1_app_list '{}'

# 列出某个多维表格的所有记录
python3 /workspace/skills/lark-skill/lark_mcp.py call bitable_v1_appTableRecord_list '{
  "table_id": "tblxxxxxx",
  "page_size": 100
}'

# 新增一条记录
python3 /workspace/skills/lark-skill/lark_mcp.py call bitable_v1_appTableRecord_create '{
  "table_id": "tblxxxxxx",
  "fields": {"姓名": "李四", "部门": "产品部"}
}'
```

---

### 场景 8：日历管理

```bash
# 查询日历列表
python3 /workspace/skills/lark-skill/lark_mcp.py call calendar_v4_calendars '{}'

# 创建日程
python3 /workspace/skills/lark-skill/lark_mcp.py call calendar_v4_events '{
  "summary": "产品评审会",
  "start_time": {"timestamp": "1743225600", "timezone": "Asia/Shanghai"},
  "end_time": {"timestamp": "1743229200", "timezone": "Asia/Shanghai"},
  "description": "Q2产品评审，需要各位负责人参加"
}'

# 查询某人在某时段的忙闲
python3 /workspace/skills/lark-skill/lark_mcp.py call calendar_v4_freebusy_query '{
  "time_min": "2026-03-30T00:00:00+08:00",
  "time_max": "2026-03-31T00:00:00+08:00",
  "user_ids": ["ou_xxxxxxxxxxxxxxxx"]
}'
```

---

### 场景 9：通讯录查询

```bash
# 查询已知用户的信息
python3 /workspace/skills/lark-skill/lark_mcp.py call contact_v3_user_batchGetId '{
  "user_id_type": "open_id",
  "open_ids": ["ou_032ca29de8829b1a71272844465a4df3"]
}'

# 查询部门下所有用户
python3 /workspace/skills/lark-skill/lark_mcp.py call contact_v3_users '{
  "user_id_type": "open_id",
  "department_id_type": "open_department_id",
  "department_ids": ["od_xxxxxxxxxxxxxxxx"]
}'
```

---

### 场景 10：提交审批

```bash
python3 /workspace/skills/lark-skill/lark_mcp.py call approval_v4_instances_create '{
  "approval_code": "APPROVAL_CODE_xxx",
  "form": [
    {"id": "field1", "value": ["张三的报销申请"]},
    {"id": "field2", "value": ["998.50"]}
  ]
}'
```

---

### 场景 11：知识库操作

```bash
# 搜索知识库
python3 /workspace/skills/lark-skill/lark_mcp.py call wiki_v1_node_search '{
  "query": "技术文档",
  "count": 10
}'

# 获取知识库节点详情（需要 space_id 和 node_token）
python3 /workspace/skills/lark-skill/lark_mcp.py call wiki_v2_space_getNode '{
  "space_id": "7241909889038073859",
  "node_token": "xxxxxxxxxx"
}'
```

⚠️ 知识库相关接口需要 `user_access_token`。

---

### 场景 12：云盘文件管理

```bash
# 获取云盘根目录
python3 /workspace/skills/lark-skill/lark_mcp.py call drive_explorer_v2_root_folder_meta '{}'

# 列出文件夹内容
python3 /workspace/skills/lark-skill/lark_mcp.py call drive_explorer_v2_fileList '{
  "order_by": 3,
  "direction": "DESC"
}'

# 创建文件夹
python3 /workspace/skills/lark-skill/lark_mcp.py call drive_v1_files_create_folder '{
  "name": "新文件夹",
  "folder_token": "根目录token"
}'
```

---

### 场景 13：下载画板为图片

```bash
# 获取画板ID（从文档块中提取 white_board_token）
python3 /workspace/skills/lark-skill/lark_mcp.py call board/v1/whiteboards/{whiteboard_id}/download_as_image '{
  "format": "png",
  "quality": "high"
}'
```

---

### 场景 14：解析 PlantUML / Mermaid 语法

```bash
# 解析 PlantUML
python3 /workspace/skills/lark-skill/lark_mcp.py call board/v1/whiteboards/{whiteboard_id}/nodes/plantuml '{
  "plant_uml_code": "@startuml\nAlice -> Bob: 你好\nBob --> Alice: 你好！\n@enduml",
  "syntax_type": 1
}'

# 解析 Mermaid
python3 /workspace/skills/lark-skill/lark_mcp.py call board/v1/whiteboards/{whiteboard_id}/nodes/plantuml '{
  "mermaid_code": "graph TD;\n    A[开始] --> B{判断}\n    B -->|是| C[执行]\n    B -->|否| D[退出}",
  "syntax_type": 2
}'
```

---

## 六、异常处理（完整版）

### 运行时错误速查

| 错误现象 | 第一步排查 | 解决方案 |
|---------|----------|---------|
| 报 `FileNotFoundError` | `ls /workspace/.lark_tokens.json` | 创建凭证文件，见第二步 |
| 报 `JSONDecodeError` | `cat /workspace/.lark_tokens.json \| python3 -m json.tool` | JSON 格式错误，用 [json.cn](https://json.cn) 校验 |
| 报 `app_id` 或 `app_secret` 错误 | 飞书开放平台 → 凭证与基础信息 | 重新复制 App ID / App Secret |
| 报 `permission denied` | 飞书开放平台 → 权限管理 | 申请对应权限 → 重新发布版本 |
| 报 `99991403` | 「权限不足」含义广 | 见下方分类排查 |
| 报 `99991700` | 机器人不在群里 | 手动把机器人拉入群聊 |
| 报 `99991140` | 接口频率超限 | 等 1-2 秒再试，勿频繁轮询 |
| 报 `99991663` | Token 无效或过期 | App Secret 可能变更，重新获取 |
| 报 `lark-mcp: command not found` | `npm list -g @larksuite/lark-mcp` | 重新安装：`npm install -g @larksuite/lark-mcp` |
| 工具调用后无输出/超时报错 | `lark-mcp --help` 确认可用 | 重启终端或重新安装 lark-mcp |
| 知识库/云文档报权限错误 | `user_access_token` 是否配置 | 确认凭证中有 `user_access_token` 字段 |

### 99991403 权限不足——分类诊断

| 伴随信息 | 真正原因 | 解决方法 |
|---------|---------|---------|
| "无 im:message 权限" | 应用未申请消息权限 | 飞书后台 → 权限管理 → 申请 `im:message` → 重新发版 |
| "无 calendar 权限" | 日历权限未开 | 同上，申请 `calendar` → 重新发版 |
| "无 docx 权限" | 云文档权限未开 | 同上，申请 `docx` → 重新发版 |
| "文档不存在" | 文档 token 错误或应用无访问权 | 文档 → 右上角「分享」→ 添加应用 |
| "节点不存在" | 知识库节点 token 错误 | 确认 node_token 正确 |

### 网络与连接错误

| 错误信息 | 原因 | 解决方法 |
|---------|------|---------|
| `Connection timeout` | 网络超时 | 确认服务器可访问 `open.feishu.cn` |
| `HTTP 403` | IP 白名单限制 | 飞书后台 → 安全设置 → 关闭 IP 白名单 |
| `HTTP 429` | 请求过快被限流 | 添加延时：`sleep 1` 后重试 |
| `SSL error` | 证书问题 | 确认服务器时间正确：`date` |

---

## 七、凭证与权限体系详解

### 凭证种类

| 凭证 | 有效期 | 获取方式 | 用途 |
|------|-------|---------|------|
| App Token（tenant_access_token）| 2小时，自动续期 | app_id + app_secret 自动换取 | 消息/日历/通讯录/审批/多维表格/云盘 |
| User Access Token | 2小时 | OAuth 用户授权 | 知识库/云文档搜索和读取 |

### 权限申请自查表（按功能）

| 需要的功能 | 必须申请的权限 | 是否需重新发版 |
|---------|-------------|-------------|
| 发消息到群 | `im:message` | ✅ |
| 获取群列表 | `im:chat:read` | ✅ |
| 创建群聊 | `im:chat` | ✅ |
| 日历读写 | `calendar` | ✅ |
| 通讯录查询 | `contact` | ✅ |
| 提交审批 | `approval` | ✅ |
| 多维表格读写 | `bitable:app` | ✅ |
| 电子表格读写 | `sheets` | ✅ |
| 云盘文件管理 | `drive` | ✅ |
| 知识库搜索/读取 | `wiki` | ✅ + User Token |
| 云文档搜索/读取 | `docx` | ✅ + User Token |
| 获取用户信息 | `contact:user.id:readonly` | ✅ |

---

## 八、调试与排障流程图

```
工具调用报错
  │
  ├─ FileNotFoundError / JSONDecodeError
  │     → 检查 /workspace/.lark_tokens.json 是否存在、格式是否正确
  │
  ├─ lark-mcp: command not found
  │     → npm install -g @larksuite/lark-mcp
  │
  ├─ 99991663（Token 无效）
  │     → 重新确认 app_id 和 app_secret 是否正确
  │
  ├─ 99991403（权限不足）
  │     ├─ 应用权限未申请 → 飞书后台申请 + 发版
  │     └─ 文档未分享给应用 → 文档右上角「分享」添加应用
  │
  ├─ 99991700（不在群里）
  │     → 手动把机器人拉入目标群
  │
  ├─ 99991140（频率超限）
  │     → 降低调用频率
  │
  └─ 无输出 / 超时
        → lark-mcp --help 确认可用性，重试
```

---

## 九、频率限制参考

| 接口类型 | 限制 | 超过后 |
|---------|------|-------|
| 大多数 API | 50次/秒 | 收到 99991140，等待后重试 |
| 知识库搜索 | 5次/秒 | 等待 1 秒再试 |
| 发送消息 | 50次/秒 | 加 sleep(0.1) 控制频率 |
| 创建日程 | 10次/秒 | 降低频率 |
| 创建电子表格 | 5次/分 | 控制调用节奏 |
| 批量发消息 | 受单发限制叠加 | 建议间隔发送 |

---

## 十、参考文件索引

| 文件 | 内容 |
|------|------|
| references/start-here.md | 快速入门，三分钟上手 |
| references/tools-index.md | 全部工具完整索引（60+ 接口）|
| references/auth.md | 认证体系、双层权限模型详解 |
| references/errors.md | 完整错误码速查 |
| references/im.md | 消息与群组 API 详解 |
| references/drive.md | 云盘与文件 API 详解 |
| references/wiki.md | 知识库 API 详解 |
| references/docx.md | 云文档 API 详解 |
| references/sheets.md | 电子表格 API 详解 |
| references/bitable.md | 多维表格 API 详解 |
| references/board.md | 画板 API 详解 |
| references/contact.md | 通讯录 API 详解 |
| references/calendar.md | 日历 API 详解 |
| references/approval.md | 审批 API 详解 |
