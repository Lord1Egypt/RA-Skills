# 🕐 PingCode TimeLogger

> OpenClaw Skill：自动化 PingCode 工时填报，支持手动任务清单和 Git 提交自动生成。

## ✨ 功能

- **创建子任务**：在指定父工作项下批量创建子任务
- **自动登记工时**：设置日期、状态、工时，自动分配到工作日
- **Git 提交转工时**：读取 GitHub / GitLab 提交记录，自动生成任务并填报
- **双通道认证**：API 直连优先，浏览器自动化兜底
- **通用脱敏**：所有敏感信息从配置文件读取，skill 本身不含任何硬编码

## 📦 安装

### 方式一：ClawHub（推荐）

```bash
clawhub install pingcode-timelogger
```

### 方式二：手动

将 `SKILL.md` 和 `references/` 目录放入你的 OpenClaw workspace 的 `skills/pingcode-timelogger/` 下。

## ⚙️ 配置

### 1. 创建配置目录

```bash
mkdir -p ~/.openclaw/skills/pingcode-timelogger
```

### 2. 复制配置模板

将 `references/config-template.yaml` 复制到配置目录：

```bash
cp <skill-dir>/references/config-template.yaml ~/.openclaw/skills/pingcode-timelogger/config.yaml
```

### 3. 填写配置

编辑 `~/.openclaw/skills/pingcode-timelogger/config.yaml`：

```yaml
pingcode:
  url: https://your-company.pingcode.com   # 你的 PingCode 地址
  cookie_file: ./cookies.txt                # Cookie 文件路径
  project_id: "xxxxxxxxxxxxxxxxxxxxxxxx"    # 项目 ID（24位hex）
  default_parent_id: ""                     # 默认父工作项 ID（可选）
  user_id: "xxxxxxxxxxxxxxxxxxxxxxxx"       # 你的用户 ID
  task_type_id: ""                          # "任务"类型 ID
  completed_state_id: ""                    # "已完成"状态 ID
  open_state_id: ""                         # "打开"状态 ID
```

### 4. 导出 PingCode Cookie

1. 用浏览器登录你的 PingCode
2. 打开开发者工具（F12）→ Application → Cookies
3. 复制 PingCode 域名下的所有 Cookie
4. 保存到 `~/.openclaw/skills/pingcode-timelogger/cookies.txt`

> 💡 也可以让 OpenClaw 通过浏览器自动操作（兜底方案），此时不需要 Cookie 文件，但需要你在浏览器中已登录 PingCode。

### 5. 查找 ID（如果不知道的话）

在 PingCode 中打开开发者工具的 Network 面板，操作时观察 API 请求：

| 需要的 ID | 怎么找 |
|-----------|--------|
| `project_id` | 打开项目，看 URL 或 API 请求中的 project 参数 |
| `user_id` | 查看个人信息相关的 API 返回 |
| `task_type_id` | 创建一个任务，看请求中的 type 字段 |
| `completed_state_id` | 修改任务状态为"已完成"，看请求中的 state_id |

> 💡 首次使用时，直接告诉 OpenClaw "帮我配置 PingCode TimeLogger"，它会引导你一步步完成。

### 6. 配置 Git 集成（可选）

如果你想从 Git 提交记录自动生成工时：

```yaml
git:
  provider: github          # github 或 gitlab
  url: https://api.github.com
  token_file: ./git-token.txt
  username: your-username
  repos: ["owner/repo1", "owner/repo2"]
```

创建 token 文件：
```bash
echo "your-github-token" > ~/.openclaw/skills/pingcode-timelogger/git-token.txt
```

## 🚀 使用

### 手动填报

直接告诉 OpenClaw：

```
帮我在 SMA-348 下填这周的工时：
- 周一：修复用户认证超时问题 3h
- 周二：数据同步接口开发 4h
- 周三：代码审查 + 部署 2h
```

或者给一个 PingCode 链接：

```
帮我在这里填工时：https://your-company.pingcode.com/pjm/projects/SMA/work-items/SMA-348
任务清单如下：...
```

### Git 提交自动填报

```
根据今天的 Git 提交帮我填 PingCode，今天工作了 8 小时
```

OpenClaw 会：
1. 读取你配置的 Git 仓库的提交记录
2. 按日期分组，自动生成任务标题
3. 按提交数量比例分配工时
4. 确认后自动创建子任务并登记工时

## 📁 文件结构

```
pingcode-timelogger/
├── SKILL.md                          # Agent 指令文件
└── references/
    ├── config-template.yaml          # 配置模板
    ├── category-ids.md               # 工作类别 ID 映射
    └── git-integration.md            # Git 集成说明
```

## ⚠️ 注意事项

- PingCode 认证使用 Cookie，不支持 Bearer Token
- 工时会自动分配到工作日（周一~周五），不会堆在一天
- 首次使用会有引导流程，帮你找到各种 ID
- **不会自动删除或修改已有工作项**，除非你明确要求

## 📄 License

MIT
