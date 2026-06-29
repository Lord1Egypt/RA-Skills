# hello-env

> A zero-dependency Bash health check for any dev environment — host, container, or K8s pod.
>
> 一个零依赖的开源环境自检脚本，适用于本地、容器、K8s Pod 环境。

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

Pure `bash`. No Python, no npm, no third-party packages. Works on macOS, Linux, and inside containers.

### Compatibility matrix

| Platform | Status |
|---|---|
| Linux (any distro) | ✅ Full |
| macOS (bash 3.2.57+ default) | ✅ Full |
| Windows WSL / WSL2 | ✅ Full |
| Windows Git Bash / MSYS / Cygwin | ⚠️ Partial (cgroup detection + PVC monitor skipped — Linux-only kernel) |
| Windows PowerShell / cmd | ❌ Not supported by design |

| Agent platform | Status |
|---|---|
| Claude Code, Codex, OpenClaw, Cursor, Cline | ✅ Standard SKILL.md format, drops in |

---

## English

### Why

Setting up a new machine or jumping into someone else's container/pod usually means one of:

- "What OS / arch / shell am I on?"
- "Is node / python / git / curl / jq installed? Which version?"
- "What's my IP and what subnet am I in?"
- "Am I in a container? In K8s? Which namespace?"
- "**Did the PersistentVolume silently get remounted?** All my files seem to have disappeared after the pod restarted."

`hello-env` answers all of that in one command, and **catches silent PVC remount** by snapshotting the mount device + a directory-count baseline on each run.

### Quick start

```bash
git clone https://github.com/Songhonglei/better-agent-skills.git
bash better-agent-skills/skills/hello-env/scripts/check-env.sh
```

### Common usage

```bash
# Defaults — checks current directory + standard K8s env vars
bash check-env.sh

# Custom workdir + extra env vars to probe for container/K8s
bash check-env.sh --workdir /opt/myapp --probe-env "KUBERNETES_SERVICE_HOST,K8S_NAMESPACE,MY_REGION,DEPLOY_ENV"

# Force PVC monitoring when no K8s indicators present (e.g. plain Docker)
bash check-env.sh --force-pvc

# Optional config file check
bash check-env.sh --config /etc/myapp/config.json
```

### What it checks

| # | Module | Output |
|---|---|---|
| 1 | OS | macOS / Linux distro + arch |
| 2 | Current user | `whoami`, uid, gid, HOME |
| 3 | Node.js | Path + version + npm |
| 4 | Python3 | Path + version |
| 5 | Basic tools | git, curl, jq, make, docker (version + path) |
| 6 | Network | Hostname + IP + inferred private subnet |
| 7 | Container/K8s | Probes configurable env vars, falls back to `/.dockerenv` and `/proc/1/cgroup` heuristics |
| 8 | Workdir | Path exists + git initialized + branch |
| 9 | Config file | Only if `--config <path>` passed |
| 10 | PVC persistence | Device-number + watch-dir count snapshot diff |

Output legend: ✅ ok · ℹ️ info · ⚠️ warning · ❌ failure

### CLI flags

| Flag | Default | Description |
|---|---|---|
| `--workdir <path>` | `pwd` | Working directory to check |
| `--watch-dir <path>` | `<workdir>` | Directory whose subfolder count is snapshotted |
| `--config <path>` | _(unset)_ | Optional config file to check |
| `--probe-env "A,B,C"` | `KUBERNETES_SERVICE_HOST,K8S_NAMESPACE` | Env vars to probe for K8s/container context |
| `--force-pvc` | off | Force PVC monitoring when no probe vars hit |
| `--snapshot-dir <path>` | `<workdir>/.hello-env` | Where to store snapshots |
| `-h, --help` | — | Show inline help |

### Environment variables (lower priority than flags)

`HELLO_ENV_WORKDIR`, `HELLO_ENV_WATCH_DIR`, `HELLO_ENV_CONFIG`, `HELLO_ENV_PROBE_ENV`, `HELLO_ENV_FORCE_PVC=1`, `HELLO_ENV_SNAPSHOT_DIR`

### PVC remount detection — the killer feature

K8s `PersistentVolume`s can be silently reattached to a fresh disk during pod restarts. Users see:

> "All the files I created yesterday are gone after the pod restarted."

`hello-env` catches it by writing two files per run to `<snapshot-dir>`:

- `last-device` — mount device for `<workdir>`
- `last-watch-count` — `find <watch-dir> -maxdepth 1 -mindepth 1 -type d | wc -l`

| Device | Watch-dir count | Verdict |
|---|---|---|
| changed | any | ⚠️ Likely PVC remount |
| unchanged | decreased | ℹ️ Probably manual removal |
| unchanged | not decreased | ✅ Healthy |

Activates when **any** of the `--probe-env` vars is set, OR `--force-pvc` is on.

### Exit codes

Diagnostic tool — exits `0` unless arguments are malformed. Warnings don't block.

### License

MIT © Evan Song · [github.com/Songhonglei](https://github.com/Songhonglei)

---

## 中文

### 它解决什么问题

进入一台新机器、一个新容器、或某个 K8s Pod，常见疑问：

- 系统/架构是什么？
- node / python / git / curl / jq 装了没？版本号？
- IP 多少？属于哪个网段？
- 是不是容器？是不是 K8s？属于哪个 namespace？
- **PVC 是不是被悄悄换卷了？** 重启 Pod 后昨天写的文件全没了。

`hello-env` 一条命令全部回答，并通过每次运行打**设备号+目录数量快照**来**捕捉 K8s PVC 静默换卷**。

### 快速开始

```bash
git clone https://github.com/Songhonglei/better-agent-skills.git
bash better-agent-skills/skills/hello-env/scripts/check-env.sh
```

### 常用示例

```bash
# 默认：检查当前目录 + 标准 K8s 环境变量
bash check-env.sh

# 自定义 workdir + 探测的环境变量清单
bash check-env.sh --workdir /opt/myapp --probe-env "KUBERNETES_SERVICE_HOST,K8S_NAMESPACE,MY_REGION,DEPLOY_ENV"

# 非 K8s 环境强制启用 PVC 监控（如纯 Docker）
bash check-env.sh --force-pvc

# 检查指定的配置文件是否存在
bash check-env.sh --config /etc/myapp/config.json
```

### 检查项

1. **OS** — macOS / Linux 发行版 + 架构
2. **当前用户** — whoami / uid / gid / HOME
3. **Node.js** — 路径 + 版本 + npm
4. **Python3** — 路径 + 版本
5. **基础工具** — git, curl, jq, make, docker（版本+路径）
6. **网络** — hostname + IP + 推断私有网段
7. **容器/K8s** — 探测可配置环境变量，配合 `/.dockerenv` 和 `/proc/1/cgroup` 兜底
8. **Workdir** — 路径存在性 + git 初始化检查 + 分支
9. **配置文件** — 仅当传 `--config <path>` 时检查
10. **PVC 持久化** — 设备号 + 监控目录数量快照对比

### CLI 参数 / 环境变量

CLI 参数 > 环境变量 > 默认值。详见 SKILL.md 完整表格。

### PVC 换卷检测 — 核心特性

K8s 的 PersistentVolume 在 Pod 重启时可能悄无声息地被重新挂载到一个**全新的磁盘**，导致用户重启 Pod 后发现"昨天写的文件全没了"。

`hello-env` 每次运行写两份快照到 `<snapshot-dir>`：

- `last-device` — workdir 的挂载设备号
- `last-watch-count` — 监控目录的一级子目录数

| 设备号 | 目录数量 | 判定 |
|---|---|---|
| 变化 | 任意 | ⚠️ 高度疑似 PVC 换卷 |
| 不变 | 减少 | ℹ️ 可能是手动删除 |
| 不变 | 不减 | ✅ 健康 |

启用条件：`--probe-env` 中任一变量有值 **或** 加 `--force-pvc`。

### 许可证

MIT © Evan Song · [github.com/Songhonglei](https://github.com/Songhonglei)
