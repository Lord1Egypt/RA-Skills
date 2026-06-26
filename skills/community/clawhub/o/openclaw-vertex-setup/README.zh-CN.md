# OpenClaw Vertex Setup Skill

**中文版** | [English](./README.md)

这个仓库提供一个 Codex/OpenClaw skill，用来把 OpenClaw 配置成通过正常启动路径使用 Google Vertex AI Gemini 模型。

它重点覆盖这些链路，让它们都能稳定工作：

- `openclaw models status`
- `openclaw gateway start` / `openclaw gateway restart`
- `openclaw tui`
- macOS 上由 `launchd` 管理的 Gateway 服务

它也专门记录了一个常见坑：全局 npm 安装的 `openclaw` CLI 和已经安装的 Gateway 服务如果不是同一个版本，TUI 和 Gateway 很容易冲突。

## 这个 Skill 解决什么问题

- Google Cloud `gcloud` ADC 登录
- `GOOGLE_CLOUD_PROJECT` 和 `GOOGLE_CLOUD_LOCATION`
- 通过 `~/.openclaw/.env` 共享 OpenClaw 环境变量
- 在 `~/.openclaw/openclaw.json` 里设置默认模型
- `google-vertex` 认证资料缺失时的实用修复
- Gateway 服务安装、重启和验证
- 本地 agent 模式和 Gateway/TUI 模式的端到端验证

## 当前模型建议

这个仓库当前采用的 OpenClaw 配置模型 ID 是：

- `google-vertex/gemini-3.1-pro-preview`

这里有一个很重要的区分：

- `gemini-3.1-pro-preview` 是更新的预览线
- `gemini-2.5-pro` 仍然是当前 Vertex Pro 的最新稳定线

所以如果你追求最新预览能力，可以用 `3.1-pro-preview`。
如果你更在意稳定性或生产可用性，优先回退到 `2.5-pro`。

## 快速开始

### 1. 完成 ADC 登录

```bash
gcloud auth application-default login
gcloud config set project <project-id>
gcloud auth application-default set-quota-project <project-id>
```

### 2. 把共享 Vertex 环境写进 `~/.openclaw/.env`

```dotenv
GOOGLE_CLOUD_PROJECT=<project-id>
GOOGLE_CLOUD_LOCATION=global
GOOGLE_APPLICATION_CREDENTIALS=/Users/<user>/.config/gcloud/application_default_credentials.json
```

### 3. 在 `~/.openclaw/openclaw.json` 里设置默认模型

```json
{
  "agents": {
    "defaults": {
      "model": {
        "primary": "google-vertex/gemini-3.1-pro-preview"
      }
    }
  }
}
```

### 4. 用当前 CLI 重新安装 Gateway 服务

```bash
openclaw gateway install --force
openclaw gateway restart
openclaw gateway status --deep
```

### 5. 验证 Gateway 路径

```bash
openclaw agent --agent main --message "Reply with exactly: OPENCLAW_VERTEX_OK" --json
openclaw tui
```

## 升级规则

每次执行完：

```bash
npm install -g openclaw@latest
```

都建议立刻执行：

```bash
openclaw gateway install --force
openclaw gateway restart
openclaw gateway status --deep
```

原因很简单：

- CLI 可能已经升级了
- 旧的 LaunchAgent 可能还指向以前的安装路径
- 版本混用时，很容易出现 `invalid connect params` 这类 TUI/Gateway 协议错误

## 已知限制

按 2026-04-19 的实测结果，即使认证、环境变量和 Gateway 服务都配置正确，`google-vertex/gemini-3.1-pro-preview` 在当前 OpenClaw 执行路径下仍然可能出现不完整轮次。

如果你遇到这种情况，保留现有的环境和 Gateway 修复，只把默认模型暂时切回：

```json
"google-vertex/gemini-2.5-pro"
```

这样可以继续使用稳定的 Vertex 集成，同时保留整套接入流程。

## 仓库结构

- [SKILL.md](./SKILL.md): 给模型看的 skill 指令
- [agents/openai.yaml](./agents/openai.yaml): skill 的 UI 元数据
- [README.md](./README.md): English documentation

## 仓库地址

- GitHub: [bhrum/openclaw-vertex-setup-skill](https://github.com/bhrum/openclaw-vertex-setup-skill)
