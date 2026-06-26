# OpenClaw Gateway Manager

🦞 统一管理多平台、多发行版 OpenClaw 网关实例

---

## 简介

`openclaw-gateway-manager` 是一个用于管理 OpenClaw 网关实例的脚本仓库。

它会自动识别常见实例目录，例如：

- `~/.openclaw/`
- `~/.jvs/.openclaw/`
- `~/.qclaw/`
- `~/.config/openclaw/`
- `~/.openclaw-<name>/`

支持查看状态、扫描端口、修改端口、重启网关、验证配置、创建实例、删除实例。

---

## 先说清楚一件事

这个仓库本身不是 OpenClaw 实例目录。

- `~/.jvs/.openclaw/`、`~/.openclaw/`、`~/.qclaw/` 这些目录是实例配置目录
- `openclaw-gateway-manager` 是独立的管理脚本仓库
- 正常安装时，建议交给技能系统或模型运行时放到它认为合适的技能目录
- 如果是手动克隆做开发或调试，再放到你自己的普通工作目录即可
- 无论哪种方式，都不要把实例配置目录误当成这个仓库目录

手动开发/调试时可这样克隆：

```bash
git clone https://github.com/seastaradmin/openclaw-gateway-manager.git ~/openclaw-gateway-manager
cd ~/openclaw-gateway-manager
```

---

## 支持情况

| 系统 | 支持情况 | 服务管理 |
|------|----------|----------|
| macOS | ✅ 完整支持 | LaunchAgent |
| Linux | ✅ 完整支持 | `systemd --user`，无可用时回退手动模式 |
| Windows | ⚠️ 部分支持 | 以手动模式为主 |

---

## 依赖

必需依赖：

- `jq`
- `curl`
- `node`

可选依赖：

- `lsof` / `ss` / `netstat`，任一可用于端口检测
- macOS 下建议有 `launchctl`、`plutil`
- Linux 下建议有 `systemctl`

检查依赖：

```bash
./scripts/check-dependencies.sh
```

---

## 常用命令

查看所有实例状态：

```bash
./scripts/gateway-status.sh
```

扫描端口：

```bash
./scripts/gateway-scan-ports.sh
```

修改端口：

```bash
./scripts/gateway-set-port.sh local-shrimp 18888
```

重启所有网关：

```bash
./scripts/gateway-restart.sh all
```

验证实例配置：

```bash
./scripts/gateway-verify.sh local-shrimp
```

创建新实例：

```bash
./scripts/gateway-create.sh test-bot 18899 openim
```

删除实例：

```bash
./scripts/gateway-delete.sh test-bot
```

---

## 实例别名

| 别名 | 对应目录 |
|------|----------|
| `local-shrimp` / `本地虾` / `18789` | `~/.jvs/.openclaw/` |
| `feishu` / `飞书` / `18790` | `~/.openclaw/` |
| `qclaw` / `腾讯` / `28789` | `~/.qclaw/` |

自定义实例默认使用：

```bash
~/.openclaw-<name>/
```

---

## 安全说明

- 删除实例需要三重确认
- 删除前会自动备份到 `~/.openclaw-deleted-backups/`
- 只创建用户级服务，不需要 `sudo`
- 脚本会读写你的本地 OpenClaw 配置，请在执行前确认目标实例

---

## 相关文件

- 英文说明：[README.en.md](/Users/ping/Desktop/openclaw-gateway-manager/README.en.md)
- 技能文档：[SKILL.md](/Users/ping/Desktop/openclaw-gateway-manager/SKILL.md)
- 安全说明：[SECURITY_RESPONSE.md](/Users/ping/Desktop/openclaw-gateway-manager/SECURITY_RESPONSE.md)

---

## 仓库

GitHub：
[https://github.com/seastaradmin/openclaw-gateway-manager](https://github.com/seastaradmin/openclaw-gateway-manager)
