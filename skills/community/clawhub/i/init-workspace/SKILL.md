---
name: init_workspace
description: Initialize personal and team knowledge bases, create or join teams, create team project spaces, configure Gitea repository permissions, and maintain the AIFusionBot/system-config control repository.
---

# Skill: init_workspace - 初始化个人/团队知识库

## 用途

paper-kb v3 的入口初始化模块，负责：

- 第一次使用时创建用户个人知识库
- 创建团队知识库
- 通过邀请码加入团队
- 创建团队项目空间
- 初始化 Gitea 仓库目录结构
- 给用户授予对应 Gitea 仓库权限
- 维护 `AIFusionBot/system-config` 控制仓库

本 skill 自包含，脚本只依赖本目录 `scripts/` 下的模块和 `.env`。

## 触发条件

Activate when:

- 用户第一次使用知识库相关功能
- 用户说“注册 / 初始化 / 创建个人知识库”
- 用户说“创建团队”
- 用户说“加入团队”
- 用户说“创建团队项目”
- 团队管理员在群里说“绑定本群 / 解除本群绑定 / 查看本群绑定”
- 其他 skill 发现用户未注册，需要先初始化

Do NOT activate when:

- 用户已注册且正在存资料、查询、批量编译，交给对应 skill
- 用户的问题与知识库系统无关

## 关键规则

- 每个用户第一次注册时，自动创建个人知识库。
- 一个用户只能加入一个团队。
- 团队知识库归 `AIFusionBot` 所有。
- 个人知识库归用户自己的 Gitea 账号所有。
- `AIFusionBot` 对个人知识库获得 `admin` 权限。
- 团队管理员在团队知识库获得 `write` 权限。
- 普通团队成员在团队知识库获得 `read` 权限。
- 团队创建后自动创建 `general` 项目。
- 团队邀请码写入团队知识库根目录 `TEAM_INFO.md`。
- 第一次注册引导必须包含真实 Gitea 地址，地址来自环境变量 `GITEA_URL`。
- 私聊身份使用 OpenClaw `SenderId`，群聊身份使用 `GroupSubject`。
- 群聊必须先绑定到团队；群绑定 key 是 `GroupSubject`（chat_id），不是群名。
- 群里发消息的人 `SenderId` 只用于权限校验和审计，不用于决定这个群属于哪个团队。
- 只有团队管理员可以绑定或解绑团队群，且必须两步确认。
- 注册成功后必须写入 `active_tasks.json` 的 `post_init_choice:<SenderId>`，用于承接用户下一条“1/2/3”回复。
- 用户在初始化后回复 `1/2/3` 时，必须先调用 `resolve_pending_action.py` 判断含义，不得自行解释短数字。
- 如果脚本返回 `interactive_card`，OpenClaw 优先发送飞书互动卡片；卡片按钮回调映射为 `CardActionValue`，表单回调映射为 `CardFormValues`。
- 用户选择 `2. 创建新团队` 时，必须继续收集团队名称和团队研究方向；拿到这两个字段后才能调用 `init_team.py`。
- 创建团队时，团队知识库仓库名使用 `<团队名称slug>-team-kb`，不得使用 `<team_id>-team-kb` 或自动编号替代团队名称。

## 脚本

### 1. 检查用户是否注册

```bash
python3 scripts/init_user.py --check --open_id <SenderId>
```

未注册时回复用户：

```text
你好，我是科研知识库助手。第一次使用需要先创建你的个人知识库。
请先打开 Gitea 注册账号：{GITEA_URL}

注册完成后，回复以下信息：
Gitea用户名：
姓名：
研究方向：
```

### 2. 注册用户并创建个人知识库

```bash
python3 scripts/init_user.py --register --open_id <SenderId> \
  --gitea_username <username> \
  --name "<姓名>" \
  --research_direction "<研究方向>"
```

成功后回复：

```text
个人知识库已创建：<personal_repo_url>

接下来你可以：
1. 加入已有团队
2. 创建新团队
3. 暂时不加入团队
```

用户下一条回复如果是 `1`、`2`、`3` 或对应文本，先调用：

```bash
python3 scripts/resolve_pending_action.py --open_id <SenderId> \
  --message "<用户回复>"
```

如果来自卡片按钮或表单回调，调用：

```bash
python3 scripts/resolve_card_action.py --action_value "<CardActionValue>"

python3 scripts/resolve_pending_action.py --open_id <SenderId> \
  --action_value "<CardActionValue>" \
  --form_values_json '<CardFormValues>'
```

处理规则：

- 返回 `action=join_team`：继续向用户收集团队名称和邀请码，再调用 `join_team.py`。
- 返回 `action=create_team`：继续向用户收集团队名称和团队研究方向，再调用 `init_team.py`。
- 返回 `ready_to_execute=true`：按返回的 `command` 和 `args` 调用 `join_team.py` 或 `init_team.py`。
- 返回 `action=personal_only`：结束初始化后选择，不创建团队。
- 如果没有 `post_init_choice:<SenderId>`，不要把单独的 `1/2/3` 当成初始化选择。

### 3. 创建团队

```bash
python3 scripts/init_team.py --open_id <SenderId> \
  --team_name "<团队名称>" \
  --research_direction "<团队研究方向>"
```

成功后：

- 创建 `AIFusionBot/<团队名称slug>-team-kb`
- 写入 `TEAM_INFO.md`
- 当前用户成为团队管理员
- 当前用户 Gitea 账号获得团队库 `write` 权限

### 4. 加入团队

```bash
python3 scripts/join_team.py --open_id <SenderId> \
  --team_name "<团队名称>" \
  --invite_code "<邀请码>"
```

成功后：

- 用户加入 `teams.json.members`
- 用户 `role=member`
- 用户 Gitea 账号获得团队库 `read` 权限

### 5. 创建团队项目

只有团队管理员可以创建：

```bash
python3 scripts/create_project.py --open_id <SenderId> \
  --project_name "<项目名称>" \
  --brief "<项目说明>"
```

脚本会：

- 创建 `projects/<project_id>/`
- 初始化 `index.md`、`timeline.md`、`decisions.md`、`open_questions.md`、`people.md`、`sources.md`
- 更新团队知识库 `catalog.json`
- 更新 `system-config/teams.json`

### 6. 绑定团队群

群聊绑定只允许在群里触发。OpenClaw 字段映射：

- `SenderId`：发起绑定的用户 open_id
- `ChatType`：必须是 `group`
- `GroupSubject`：群聊 chat_id
- `MessageSid`：消息 id，用于审计

第一步，管理员在团队群里 @bot 说“绑定本群”后调用：

```bash
python3 scripts/bind_chat.py --action request_bind \
  --sender_id <SenderId> \
  --chat_type <ChatType> \
  --chat_id <GroupSubject> \
  --chat_name "<可选，feishu_chat(action=get) 取到的群名>"
```

脚本会检查：

- 当前上下文必须是群聊。
- 当前群必须有 `GroupSubject`。
- `SenderId` 必须已注册。
- `SenderId` 必须已加入团队。
- `SenderId` 必须是该团队管理员。
- 如果该群已绑定其他团队，直接拒绝。

脚本返回 `confirm_code` 后，在群里回复：

```text
将把本群绑定到团队【<team_name>】。
绑定后，本群 @我 的查询、入库、批量导入和扫描默认进入该团队知识库。

请团队管理员在 10 分钟内回复：
@AIFusionBot 确认绑定 <confirm_code>
```

如果脚本返回 `interactive_card`，优先发送确认卡片。卡片按钮值 `confirm_bind:<confirm_code>` 对应调用 `bind_chat.py --action confirm_bind`；`cancel_bind:<confirm_code>` 对应调用 `bind_chat.py --action cancel_pending`。

第二步，确认绑定：

```bash
python3 scripts/bind_chat.py --action confirm_bind \
  --sender_id <SenderId> \
  --chat_type <ChatType> \
  --chat_id <GroupSubject> \
  --chat_name "<可选群名>" \
  --confirm_code <confirm_code>
```

确认成功后会写入：

- `system-config/chat_bindings.json`
- `system-config/chat_binding_events.json`
- 团队知识库 `identity/group-bindings.md`

查看当前群绑定：

```bash
python3 scripts/bind_chat.py --action status \
  --sender_id <SenderId> \
  --chat_type <ChatType> \
  --chat_id <GroupSubject>
```

解绑同样必须两步确认：

```bash
python3 scripts/bind_chat.py --action request_unbind \
  --sender_id <SenderId> \
  --chat_type <ChatType> \
  --chat_id <GroupSubject>
```

```bash
python3 scripts/bind_chat.py --action confirm_unbind \
  --sender_id <SenderId> \
  --chat_type <ChatType> \
  --chat_id <GroupSubject> \
  --confirm_code <confirm_code>
```

如果脚本返回解绑确认卡片，按钮值 `confirm_unbind:<confirm_code>` 对应调用 `bind_chat.py --action confirm_unbind`；`cancel_unbind:<confirm_code>` 对应调用 `bind_chat.py --action cancel_pending`。

解绑后该群不能再查询或写入团队知识库，直到重新绑定。

### 7. 修复半初始化状态

如果 Gitea 仓库已经创建，但写 `system-config` 失败，初始化脚本会记录 `provisioning_errors.json`。
如果连恢复记录也写入失败，脚本仍会返回已创建的仓库 URL，并设置 `recovery_failed=true` 和 `recovery_error`，方便人工定位。

查看待修复记录：

```bash
python3 scripts/repair_provisioning.py
```

修复单条：

```bash
python3 scripts/repair_provisioning.py --error_id <recovery_id>
```

修复全部：

```bash
python3 scripts/repair_provisioning.py --all
```

## system-config

本 skill 自动维护：

```text
AIFusionBot/system-config/
├── users.json
├── teams.json
├── chat_bindings.json
├── pending_chat_bindings.json
├── chat_binding_events.json
├── sources.json
├── jobs.json
├── active_tasks.json
├── permissions.json
└── provisioning_errors.json（按需创建）
```

`system-config` 是系统控制平面，不存知识正文。

## 错误处理

- Gitea 用户不存在：提示用户先注册 Gitea。
- 用户已注册：不要重复创建个人库。
- 用户已加入团队：拒绝加入第二个团队。
- 团队名称重复：提示加入已有团队或换名。
- 邀请码错误：拒绝加入。
- Gitea 授权失败：不要静默成功，必须告诉用户。
- 初始化写配置失败：返回 `recoverable=true` 和 `recovery_id`，后续用 `repair_provisioning.py` 修复。
