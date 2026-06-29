# Skill: init_user — paper-kb 用户初始化

## 用途

paper-kb 是一个科研知识库系统：用户在飞书发论文链接/PDF 即可自动入库到自己的
Gitea 私有仓库，用自然语言即可查询。本 Skill 负责其中的**用户初始化**环节：
检查当前飞书用户是否已注册，未注册则引导注册，并自动创建其专属的
Gitea 知识库仓库和飞书多维表格。

## 触发条件

**Activate when（满足任一）：**
- 用户发出任何与 paper-kb 相关的请求（存论文、查文献、发 arxiv 链接、上传 PDF
  等），且尚未确认该用户已注册 —— 此时先用本 Skill 的 check 模式查询注册状态。
- check 结果为未注册（registered=false），需要引导用户注册。
- 用户的消息中包含 Gitea 用户名和研究方向（形如「Gitea用户名：xxx」「研究方向：yyy」），
  这是注册引导后用户的回复，进入 register 流程。
- 用户明确要求初始化/注册/重置知识库。

**Do NOT activate when：**
- 用户已确认注册（本次会话中 check 已返回 registered=true），且消息是存文档或
  查询请求 —— 应交给 ingest_paper 或 query_papers Skill。
- 用户的消息与 paper-kb 完全无关（闲聊、其他任务）。

## 前置依赖

- **current_user_open_id**：当前飞书用户的 open_id（形如 `ou_xxx`）。
  由你（OpenClaw）从消息上下文的 sender 字段获取，作为 `--open_id` 参数传给脚本。
  在网页对话中测试时若拿不到 open_id，用 `webchat_test` 作为测试值。
- 本 Skill 根目录需有 `.env` 文件（从 `env-example.txt` 复制），包含
  `GITEA_URL` 和 `GITEA_ADMIN_TOKEN`。

## 脚本调用方式

工作目录：本 Skill 根目录（`~/.openclaw/workspace/skills/init_user/`）。

### 模式1：查询注册状态（任何 paper-kb 请求的第一步）

```bash
python3 scripts/init_user.py --check --open_id <open_id>
```

输出 JSON：
- `{"success": true, "registered": true, "user": {...}, "repo_url": "..."}`
  → 已注册。把 `user` 里的 `gitea_username`、`research_direction`、
    `feishu_app_token`、`feishu_table_id` 记住，供本次会话后续使用，
    然后继续处理用户的原始请求（交给对应 Skill）。
- `{"success": true, "registered": false}`
  → 未注册。进入下面的「注册引导流程」。

### 模式2：注册新用户

```bash
python3 scripts/init_user.py --register --open_id <open_id> \
    --gitea_username <用户名> --research_direction "<研究方向>"
```

输出 JSON 关键字段：
- `success: true, already_registered: false` → 注册成功，`repo_url` 是仓库地址，
  `feishu_table_pending: true` 表示飞书表格还没建（接下来执行「创建飞书表格」步骤）。
- `success: true, already_registered: true` → 用户之前已注册，直接告知即可。
- `success: false` → 看 `error` 字段：
  - `gitea_user_not_found`：Gitea 上没有这个用户名，把 `message` 转告用户，
    让其确认注册后重发。
  - `username_taken`：该 Gitea 账号已被别的飞书用户绑定，转告用户。
  - `not_admin`：机器人 token 不是站点管理员 —— 这是系统配置问题，把 `message`
    转告用户（管理员），流程终止。
  - 其他：把 `message` 转告用户。

### 模式3：回填飞书表格信息（创建表格成功后调用）

```bash
python3 scripts/init_user.py --update-feishu --open_id <open_id> \
    --feishu_app_token <app_token> --feishu_table_id <table_id>
```

## 完整执行流程

### A. 收到任何 paper-kb 相关消息时

1. 运行模式1（check）。
2. registered=true → 记住用户信息，把消息交给对应的业务 Skill，本 Skill 结束。
3. registered=false → 发送以下引导消息，本轮结束，等待用户回复：

> 你好！我是科研知识库助手 📚
> 检测到你还没有自己的知识库，先完成一次性注册（1分钟）：
>
> 1️⃣ 打开 http://43.134.182.170:3000 注册一个 Gitea 账号
> 2️⃣ 注册完成后，回复我两条信息：
>    Gitea用户名：你的用户名
>    研究方向：一句话描述（如"强化学习控制""触觉传感器""大语言模型对齐"等）
>
> 之后发资料链接或文件给我就能自动入库了！

（上面的 Gitea 地址 http://43.134.182.170:3000 是固定的，直接原样发给用户，
不要写成占位符或"你的gitea地址"。）

### B. 用户回复了用户名和研究方向

1. 从用户消息中提取 `gitea_username` 和 `research_direction`。
   提取不到完整两项时，礼貌地请用户补全缺失项，不要猜测。
2. 运行模式2（register）。
3. 注册成功且 `feishu_table_pending: true` → 执行步骤 C（创建飞书表格）。
4. 注册失败 → 按上文错误对照表回复用户。

### C. 创建飞书多维表格（可选步骤，失败不阻塞）

1. 调用你的飞书工具 `feishu_bitable_app`（action: create）创建多维表格，
   名称：`paper-kb-<gitea_username>`。
2. **复用默认数据表，不要新建表**：新建多维表格时飞书会自动附带一个默认数据表
   （通常名叫"数据表"）。**把这个默认表改名为「资料库」并在它上面加字段**，
   不要再额外新建一个表（否则会多出一个空的"数据表"）。
   - 先拿到默认表的 table_id（创建 app 的返回里有）
   - 用 `feishu_bitable_app_table`（action: update / patch）把表名改成 **资料库**
   - 在这个表上逐个加字段（见下表）
3. 字段定义（**严格按下表**）：

| 字段名 | 字段类型 | type值 | 说明 |
|--------|---------|--------|------|
| 标题 | 文本 | 1 | 主字段（默认表自带的第一个文本字段可直接改名为"标题"） |
| 类型 | **文本** | **1** | 存中文类型名（论文/行业调研/开源项目/技术文档/实验记录/会议纪要） |
| 关键词 | 文本 | 1 | |
| 相关性评分 | 数字 | 2 | |
| 存入时间 | 日期 | 5 | |
| Gitea链接 | 超链接 | 15 | **建字段时 property 必须完全省略**（传 {} 会报 URLFieldPropertyError） |
| arxiv_id | 文本 | 1 | |

**字段创建注意（避开已知坑）：**
- 「类型」务必建**文本（type=1）**，不要建单选（type=3）——单选 options 通过 API 创建
  极易报 `SingleSelectFieldPropertyError`；文本字段照样能筛选分组。
- 「Gitea链接」是超链接（type=15），**建字段时不要传 property 参数**（传 {} 都会报错）。
- 默认表可能自带"多行文本""单选"等示例字段，把用不到的删掉，只留上面 7 个。

4. 拿到 `app_token` 和「资料库」表的 `table_id`，运行模式3（update-feishu）回填。
5. **记住表格链接** `https://feishu.cn/base/<app_token>`，在步骤 D 的回复中发给用户。
6. **如果飞书工具调用失败（权限未开通等）：跳过，不要重试超过1次，不要报错
   中断**。在最终回复中注明"飞书表格暂未启用，不影响知识库使用"。

### D. 回复用户

注册全部完成后回复（按实际情况调整）：

> ✅ 知识库初始化完成！
> 📂 你的仓库：{repo_url}
> 🎯 研究方向：{research_direction}
> 📊 飞书表格：https://feishu.cn/base/{app_token}　（暂未启用时改为"暂未启用，不影响使用"）
>
> 现在可以：
> · 发资料链接、PDF/Word/Excel 文件，或直接打字，说"帮我存入知识库"
> · 直接提问，如"有没有关于……的资料"

（飞书表格链接务必带上真实的 app_token，让用户能直接点开。）

### E. 处理用户的原始请求

如果用户最初的消息里带有实际任务（例如第一条消息就是 arxiv 链接），初始化完成后
**继续处理那条原始请求**（交给 ingest_paper / query_papers),完成后再次回复结果。

## 注意事项

- 脚本所有输出都是单行 JSON，stdout 里出现非 JSON 内容时视为脚本异常，
  把原始输出转告用户并建议联系管理员。
- 不要把 token、open_id 等敏感信息展示给用户。
- 同一会话中 check 过一次后，结果可以复用，不必每条消息都重复 check。
