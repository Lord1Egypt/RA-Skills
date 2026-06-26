# OpenClaw Tailscale Remote Access

[English](./README.md)

这是一个给 Codex/OpenClaw 用的技能仓库，用来把 OpenClaw 控制面通过 Tailscale 可靠地暴露出来，并且支持按步骤排查常见故障。

## 链接

- ClawHub: https://clawhub.ai/skills/openclaw-tailscale-remote-access
- GitHub: https://github.com/JiangAgentLabs/openclaw-tailscale-remote-access

## 这个 Skill 能做什么

- 在修改前统一检查 OpenClaw、Tailscale 和 Tailscale Serve 状态。
- 把 OpenClaw 网关改成推荐配置，适配 `Tailscale Serve + HTTPS`。
- 配置 `https://<machine>.<tailnet>.ts.net/ -> http://127.0.0.1:18789/`。
- 提供从配置、TLS、MagicDNS、origin 到 pairing 的标准排障路径。

## 快速开始

先从 ClawHub 安装到 OpenClaw workspace：

```bash
clawhub install openclaw-tailscale-remote-access
```

或者把仓库克隆到本地 Codex skills 目录：

```bash
git clone git@github.com:JiangAgentLabs/openclaw-tailscale-remote-access.git \
  "${CODEX_HOME:-$HOME/.codex}/skills/openclaw-tailscale-remote-access"
```

常见安装位置：

- OpenClaw workspace：`~/.openclaw/workspace/skills/openclaw-tailscale-remote-access`
- Codex 用户技能目录：`~/.codex/skills/openclaw-tailscale-remote-access`

设置运行所需变量：

```bash
export SKILL_DIR="${CODEX_HOME:-$HOME/.codex}/skills/openclaw-tailscale-remote-access"
export OPENCLAW_CONFIG="${OPENCLAW_CONFIG:-$HOME/.openclaw/openclaw.json}"
export GATEWAY_PORT="${GATEWAY_PORT:-18789}"
export TS_HOSTNAME="<machine>.<tailnet>.ts.net"
export GATEWAY_TOKEN="<gateway-token>"
```

执行标准流程：

```bash
bash "$SKILL_DIR/scripts/inspect_remote_access.sh" "$OPENCLAW_CONFIG"
python3 "$SKILL_DIR/scripts/apply_gateway_config.py" \
  --config "$OPENCLAW_CONFIG" \
  --ts-hostname "$TS_HOSTNAME" \
  --token "$GATEWAY_TOKEN" \
  --port "$GATEWAY_PORT"
systemctl --user restart openclaw-gateway
tailscale up --accept-dns=false --accept-routes=false --ssh=false
bash "$SKILL_DIR/scripts/configure_tailscale_serve.sh" --port "$GATEWAY_PORT"
```

## 仓库结构

```text
.
├── SKILL.md
├── README.md
├── README.zh-CN.md
├── CHANGELOG.md
├── agents/
│   └── openai.yaml
├── references/
│   ├── remote-setup.md
│   └── troubleshooting.md
└── scripts/
    ├── apply_gateway_config.py
    ├── configure_tailscale_serve.sh
    └── inspect_remote_access.sh
```

## 内置脚本

- `scripts/inspect_remote_access.sh`：检查主机身份、Tailscale 状态、Serve 状态、OpenClaw 服务、配置文件和待审批设备。
- `scripts/apply_gateway_config.py`：备份并修改 `openclaw.json`，写入推荐的网关配置。
- `scripts/configure_tailscale_serve.sh`：创建或重建 Tailscale HTTPS Serve 映射。

## 推荐执行顺序

1. 先确认当前 shell 不是通过 Tailscale SSH 连进去的。
2. 用 `inspect_remote_access.sh` 看现状。
3. 用 `apply_gateway_config.py` 落配置。
4. 重启 `openclaw-gateway`。
5. 在安全会话里执行 `tailscale up --accept-dns=false --accept-routes=false --ssh=false`。
6. 用 `configure_tailscale_serve.sh` 建好 Serve。
7. 验证 `https://<machine>.<tailnet>.ts.net/` 是否可访问。

## 兼容性

- 服务端：Linux + `systemd` + `tailscale` + `python3` + `bash` + `curl`
- 客户端：文档里包含 macOS 的 MagicDNS 修复说明
- 主要配置文件：`~/.openclaw/openclaw.json`

## 文档入口

- 主技能说明：[SKILL.md](./SKILL.md)
- 主机配置流程：[references/remote-setup.md](./references/remote-setup.md)
- 排障说明：[references/troubleshooting.md](./references/troubleshooting.md)

## 版本记录

见 [CHANGELOG.md](./CHANGELOG.md)。

## 参考了什么写法

这份仓库结构参考了公开 skill 项目和 ClawHub 示例里常见的组织方式：

- 首页先讲清一句话定位
- 提供可直接复制的 Quick Start
- 明确列出目录结构
- 把脚本和文档职责拆开
- 用单独的 changelog 和 `agents/openai.yaml` 管理发布信息
