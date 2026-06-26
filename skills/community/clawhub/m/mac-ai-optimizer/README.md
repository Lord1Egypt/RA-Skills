# Mac AI Optimizer

Optimize macOS for AI workloads. Turn an 8GB Mac into a lean AI server node with near-16GB performance.

8GB Mac 极限优化工具。把小内存 Mac 变成 AI 服务器节点，接近 16GB 的运行体验。

---

## What it does / 功能说明

Reduces macOS idle memory from ~6GB to ~2.5GB:

将 macOS 闲置内存从 ~6GB 降到 ~2.5GB：

- Disable Spotlight, Siri, photo analysis, analytics / 关闭 Spotlight、Siri、照片分析、系统分析
- Reduce UI animations, transparency, GPU overhead / 减少动画、透明度、GPU 占用
- Configure Docker Desktop resource limits / 配置 Docker 资源限制
- Enable SSH for remote node management / 开启 SSH 远程管理
- Clean unused Docker resources / 清理 Docker 无用资源
- One-click revert to defaults / 一键恢复默认设置

---

## Installation / 安装

### 1. Claude Code Skill

```bash
npx skills add dongsheng123132/mac-ai-optimizer
```

Then tell Claude / 然后对 Claude 说：

```
Optimize this Mac for AI workloads
帮我优化这台 Mac 来跑 AI
```

### 2. OpenClaw / ClawHub Plugin

Local install / 本地安装：

```bash
openclaw plugins install -l /path/to/mac-ai-optimizer
```

Or copy to extensions dir / 或复制到扩展目录：

```bash
cp -r mac-ai-optimizer ~/.openclaw/extensions/mac-ai-optimizer
```

Then configure `openclaw.json` / 然后配置 `openclaw.json`：

```json
{
  "plugins": {
    "entries": {
      "mac-ai-optimizer": {
        "enabled": true,
        "config": {
          "optimizeLevel": "moderate"
        }
      }
    }
  },
  "tools": {
    "allow": [
      "mac_system_report",
      "mac_optimize_memory",
      "mac_reduce_ui",
      "mac_docker_optimize",
      "mac_enable_ssh",
      "mac_full_optimize",
      "mac_revert_optimizations"
    ]
  }
}
```

OpenClaw Agent can then call these tools directly in conversation:

OpenClaw Agent 可以在对话中直接调用这些工具：

```
"Help me optimize this Mac for running OpenClaw"
"优化这台 Mac 来跑 OpenClaw"
```

### 3. Standalone / 独立运行

```bash
chmod +x tools/*.sh

# Full optimization / 一键全部优化
./tools/full_optimize.sh

# Individual tools / 单独运行
./tools/system_report.sh      # View resources / 查看资源
./tools/optimize_memory.sh    # Optimize memory / 优化内存
./tools/reduce_ui.sh          # Reduce UI / 减少 UI
./tools/docker_optimize.sh    # Optimize Docker / 优化 Docker
./tools/enable_ssh.sh         # Enable SSH / 开启 SSH

# Revert all changes / 恢复所有修改
./tools/revert_all.sh
```

---

## Tools / 工具列表

| Tool | Description / 描述 | Savings / 节省 |
|------|---------------------|----------------|
| `system_report` | Show resource usage / 查看资源占用 | - |
| `optimize_memory` | Disable background services / 关闭后台服务 | ~1-2GB RAM |
| `reduce_ui` | Minimize UI overhead / 最小化 UI 开销 | ~300-500MB RAM |
| `docker_optimize` | Set Docker limits / 设置 Docker 限制 | Prevents OOM |
| `enable_ssh` | Enable remote access / 开启远程访问 | - |
| `full_optimize` | Run all above / 运行以上全部 | ~2-3GB RAM |
| `revert_all` | Undo all changes / 撤销所有优化 | - |

---

## Expected Results / 预期效果

### 8GB Mac

| State / 状态 | Memory Used / 内存占用 | Available / 可用 |
|---------------|------------------------|-------------------|
| Default macOS / 默认 | ~6GB | ~2GB |
| After optimization / 优化后 | ~2.5GB | ~5.5GB |
| Headless mode / 无头模式 | ~1.8GB | ~6.2GB |

Optimized 8GB Mac can comfortably run:

优化后 8GB Mac 可以流畅运行：

- OpenClaw (Docker)
- Ollama (7B models)
- Redis + PostgreSQL
- AI Agent / Crawler

---

## AI Cluster Setup / AI 集群搭建

Use multiple optimized Macs as compute nodes:

用多台优化后的 Mac 组成 AI 计算集群：

```
Control Machine / 主控电脑
     |
     | SSH
     v
Mac mini node 1 (OpenClaw)
Mac mini node 2 (Ollama)
Mac mini node 3 (Crawler)
```

After running `enable_ssh`, add to `~/.ssh/config`:

运行 `enable_ssh` 后，添加到 `~/.ssh/config`：

```
Host ai-node-1
    HostName 192.168.1.x
    User your-username
    ForwardAgent yes

Host ai-node-2
    HostName 192.168.1.y
    User your-username
    ForwardAgent yes
```

---

## Compatibility / 兼容性

| Platform | Support |
|----------|---------|
| Claude Code Skill | npx skills add |
| OpenClaw / ClawHub | openclaw plugins install |
| Standalone shell | bash tools/*.sh |

---

## Requirements / 要求

- macOS 12+ (Monterey or later)
- Admin access (sudo) for some operations / 部分操作需要管理员权限
- Docker Desktop (optional / 可选)

## Reverting / 恢复

Run `./tools/revert_all.sh` or restart Mac.

运行 `./tools/revert_all.sh` 或重启 Mac 即可恢复。

## License

MIT
