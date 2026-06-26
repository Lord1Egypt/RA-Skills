# ops-maintenance v2.1.0 快速迁移指南

## ⚠️ 重要提示

v2.1.0 包含破坏性变更，升级前请仔细阅读本指南。

## 📋 升级前检查清单

- [ ] 备份当前配置文件 `~/.config/ops-maintenance/servers.json`
- [ ] 记录当前使用的命令列表
- [ ] 确认所有 SSH 用户名（不再默认使用 root）
- [ ] 测试环境先升级验证

## 🔧 升级步骤

### 1. 备份配置

```bash
cp ~/.config/ops-maintenance/servers.json ~/.config/ops-maintenance/servers.json.backup
```

### 2. 更新代码

```bash
cd /Users/a1234/.openclaw/workspace/skills/ops-maintenance
git pull  # 或重新下载 v2.1.0
npm install
npm run build
```

### 3. 更新服务器配置

编辑 `~/.config/ops-maintenance/servers.json`，为每个服务器添加 `user` 字段：

**之前**：
```json
[
  {
    "host": "192.168.1.100",
    "port": 22,
    "keyFile": "~/.ssh/id_rsa",
    "name": "web-1",
    "tags": ["production", "web"]
  }
]
```

**现在**：
```json
[
  {
    "host": "192.168.1.100",
    "port": 22,
    "user": "admin",
    "keyFile": "~/.ssh/id_rsa",
    "name": "web-1",
    "tags": ["production", "web"]
  }
]
```

### 4. 验证命令白名单

检查你使用的命令是否在白名单中：

#### ✅ 允许的命令

**系统信息**：
- `uptime`, `free`, `df`, `top`, `ps`, `uname`, `hostname`, `whoami`, `id`

**日志查看**：
- `tail`, `grep`, `cat`, `less`, `journalctl`

**网络检查**：
- `netstat`, `ss`, `lsof`, `curl`, `wget`, `ping`

**进程和服务**：
- `systemctl status`, `docker ps`, `kubectl get`

**文件和磁盘**：
- `ls`, `du`, `find`, `stat`

#### ❌ 禁止的命令

**文件操作**：
- `rm`, `rmdir`, `mv`, `cp`, `touch`, `chmod`, `chown`

**系统控制**：
- `shutdown`, `reboot`, `poweroff`, `halt`

**用户管理**：
- `useradd`, `userdel`, `usermod`, `passwd`

**包管理**：
- `apt-get`, `apt`, `yum`, `dnf`, `pacman`, `npm`, `pip`

**服务控制**：
- `systemctl start/stop/restart/reload`

**危险操作**：
- `dd`, `mkfs`, `fdisk`, `parted`
- 任何包含管道、重定向、命令替换的命令

### 5. 测试连接

```bash
# 测试本地健康检查
/ops-maintenance health

# 测试远程连接
/ops-maintenance admin@192.168.1.100 health

# 测试集群状态
/ops-maintenance cluster
```

### 6. 验证密码加密

首次加载时，未加密的密码会自动加密。检查配置文件：

```bash
cat ~/.config/ops-maintenance/servers.json
```

如果密码字段是加密格式（类似 `abc123:def456:ghi789`），说明加密成功。

## 🔄 常见迁移问题

### Q1: 升级后连接失败，提示"SSH用户必须显式指定"

**原因**：配置文件中缺少 `user` 字段

**解决**：为每个服务器添加 `user` 字段

### Q2: 命令执行失败，提示"安全检查失败"

**原因**：命令不在白名单中

**解决**：
1. 检查命令是否在白名单中
2. 使用只读命令替代修改操作
3. 如需添加命令，联系管理员

### Q3: 密码无法连接

**原因**：密码格式可能不兼容

**解决**：
1. 检查密码是否为加密格式
2. 如果是明文，会自动加密
3. 如果加密后仍无法连接，重新配置密码

### Q4: 旧版本配置文件能否使用？

**原因**：配置文件格式兼容性

**解决**：
- v2.1.0 会自动迁移旧配置
- 明文密码会自动加密
- 但必须添加 `user` 字段

## 📝 配置示例

### 完整配置示例

```json
[
  {
    "host": "192.168.1.100",
    "port": 22,
    "user": "admin",
    "keyFile": "~/.ssh/id_rsa",
    "name": "web-1",
    "tags": ["production", "web"]
  },
  {
    "host": "192.168.1.101",
    "port": 22,
    "user": "ops",
    "password": "encrypted_password_here",
    "name": "db-1",
    "tags": ["production", "database"]
  },
  {
    "host": "192.168.1.102",
    "port": 2222,
    "user": "deploy",
    "keyFile": "~/.ssh/deploy_key",
    "name": "app-1",
    "tags": ["staging", "app"]
  }
]
```

## 🧪 测试清单

升级完成后，请测试以下功能：

- [ ] 本地健康检查
- [ ] 远程 SSH 连接
- [ ] 日志查看
- [ ] 端口检查
- [ ] 进程检查
- [ ] 磁盘使用检查
- [ ] 集群状态查看
- [ ] 批量操作
- [ ] 文件传输
- [ ] 审计日志

## 🆘 回滚方案

如果升级后遇到严重问题，可以回滚到旧版本：

```bash
# 1. 恢复配置文件
cp ~/.config/ops-maintenance/servers.json.backup ~/.config/ops-maintenance/servers.json

# 2. 删除加密密钥（如果需要）
rm ~/.config/ops-maintenance/.key

# 3. 回滚代码
git checkout v2.0.0
npm install
npm run build
```

## 📞 获取帮助

如果遇到问题：

1. 查看 [SECURITY_IMPROVEMENTS.md](./SECURITY_IMPROVEMENTS.md)
2. 查看 [RELEASE_NOTES.md](./RELEASE_NOTES.md)
3. 提交 Issue
4. 联系维护者

## ✅ 升级完成

升级完成后，你将获得：

- ✅ 更高的安全性
- ✅ 密码加密存储
- ✅ 命令白名单保护
- ✅ 防止命令注入
- ✅ 严格的权限控制

---

**祝升级顺利！** 🎉
