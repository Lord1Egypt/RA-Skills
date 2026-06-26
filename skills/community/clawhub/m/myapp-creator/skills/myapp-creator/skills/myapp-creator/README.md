# myapp-creator

让小度用户用一句话造一个 HTML 小应用，落库到 fe-service。

- 包名：ClawHub 页面 URL 为 `https://clawhub.ai/<发布者>/myapp-creator`；**`clawhub install / inspect` 只允许裸 slug `myapp-creator`**（参数里含 `/` 会报 `Invalid slug`）。fe-service `MYAPP_SKILL_NAME` 可仍写全路径，下发 install_prompt 时会自动剥成裸 slug。
- 当前版本：见 `version.txt`
- License：MIT-0

## 用户视角是什么

用户在小度 Swan 端的"我的应用"页输入一句话（如"做一个五子棋"），fe-service 通过对话深链触发龙虾 OpenClaw 的 LLM agent；agent 在本 skill 的 prompt 约束下生成单文件 HTML 与功能列表，再调本 skill 的 `myapp_register` 工具把数据落到 fe-service。

整个流程对用户透明：用户只看见一个进度条和最终的应用卡片。

## 安装方式

### A. 自动安装（推荐）

用户首次进入"我的应用"页时，fe-service 会下发一段 install_prompt，由龙虾 agent 自动执行：

```
clawhub install myapp-creator --version <VERSION>
```

页面路径里虽有 `zhang6714268/`，**安装时不要带前缀**，否则 `Invalid slug`。

若本机无 `clawhub`，agent 需先 `npm i -g clawhub`（或 `npx clawhub@latest install ...`）。**不要用 `openclaw skills install`**，新版 OpenClaw 的 `skills` 子命令会报 `too many arguments`。

并写入 `~/.mcporter/mcporter.json` 中的环境变量。**用户无需手动操作。**

### B. 手动安装（兜底/调试）

```bash
clawhub install myapp-creator --version 1.0.0
# 或：npx --yes clawhub@latest install myapp-creator --version 1.0.0
```

然后在 `~/.mcporter/mcporter.json` 的 `skills.myapp-creator.env` 写入：

```json
{
  "MYAPP_API_BASE": "http://group.dumi-SwanSSRNode12-env.dumi.all",
  "MYAPP_API_TOKEN": "<由 fe-service 团队下发>"
}
```

最后重新加载（任选其一，以本机 CLI 为准）：

```bash
openclaw gateway restart
# 若无 gateway 子命令：重启 OpenClaw 应用
```

## 工具清单

| 工具 | 入参 | 用途 |
|---|---|---|
| `myapp_register` | dumi_id, cuid, query, app_name, html_content, features | 创建新应用 |
| `myapp_update`   | app_id, query, html_content, features | 更新已有应用 |
| `myapp_get`      | app_id | 读应用详情（更新前用） |
| `myapp_ping`     | session_id, dumi_id, cuid, skill_version | 安装自检 |

详细约束与触发条件见 `SKILL.md`。

## 故障排查

| 现象 | 排查 |
|---|---|
| 调 register/update 返回 401 | 检查 `MYAPP_API_TOKEN` 是否与 fe-service 配置一致 |
| 调 register/update 返回 502 (BOS upload failed) | fe-service 端 BOS_UPLOAD_AK/SK 未配置或权限不足 |
| 调 register/update 返回 400 | 入参超长或缺字段；检查 `app_name`/`features`/`html_content` 是否符合 SKILL.md 约束 |
| 调 register/update 返回 timeout | fe-service 不可达；检查 `MYAPP_API_BASE` 与本机网络 |
| `myapp_get` 404 | app 已被软删，或 app_id 写错 |
| 安装自检 60s 仍未完成 | 检查 mcporter env 中 token / base 是否正确写入；重启 openclaw |
| `./publish.sh` 报 `too many arguments for 'skills'` | **openclaw** 不再支持 `skills publish/install`；发布用 `clawhub`，安装用 `clawhub install <裸slug> --version …`（不要 `owner/skill`） |

## 发版

```bash
# 0) 安装并登录 ClawHub CLI（发布走 clawhub，不要用已弃用的 openclaw skills publish）
npm i -g clawhub
clawhub login

# 1) 改 version.txt 和 clawhub.yaml 中的 version
# 2) 跑发布（内部: clawhub skill publish . --version <x.y.z>）
./publish.sh

# 3) 同步更新 fe-service 中的 MYAPP_SKILL_REQUIRED_VERSION
```

## 安全说明

- 本 skill 代码为公开包，**不包含任何 token**。
- 所有调用都需要 `MYAPP_API_TOKEN`，token 由 fe-service 在用户首次安装时通过 install_prompt 下发，落到用户本机 mcporter.json env。
- 没有合法 dumi_id + token 的用户即使装上 skill，调用 fe-service 也会被 401 拒绝。
- 安全模型与 [`dueros-mcp/xiaodu-control-official`](https://clawhub.ai/dueros-mcp/xiaodu-control-official) 一致。
