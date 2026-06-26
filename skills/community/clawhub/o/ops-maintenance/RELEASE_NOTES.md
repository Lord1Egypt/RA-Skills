# ops-maintenance v2.1.0 发布说明

## 🎉 安全增强版本

ops-maintenance v2.1.0 是一个重要的安全更新版本，针对 ClawHub 安全扫描发现的问题进行了全面修复。

## 📋 主要改进

### 🔒 安全性提升

1. **移除默认 root 用户**
   - 必须显式指定 SSH 用户
   - 防止权限过大导致的安全风险

2. **密码加密存储**
   - 使用 AES-256-GCM 加密算法
   - 自动生成并管理加密密钥
   - 密钥文件权限设置为 600

3. **命令白名单验证**
   - 只允许执行安全的只读命令
   - 拒绝危险操作（删除、修改、系统控制等）
   - 检测管道、重定向、命令替换等绕过方式

4. **移除 shell 执行**
   - `runCommand` 不再使用 shell
   - 防止命令注入攻击

5. **增强安全检查**
   - 检测特殊字符和绕过方式
   - 严格的文件权限控制

## 📦 新增功能

### 加密工具模块 (`crypto.ts`)
- AES-256-GCM 加密/解密
- 自动密钥管理
- 配置文件加密存储

### 命令验证模块 (`command-validator.ts`)
- 命令白名单验证
- 危险命令检测
- 绕过方式检测

## 🚨 破坏性变更

### 1. 必须显式指定 SSH 用户
**之前**：
```json
{
  "host": "192.168.1.100",
  "port": 22
}
```

**现在**：
```json
{
  "host": "192.168.1.100",
  "port": 22,
  "user": "admin"
}
```

### 2. 命令白名单限制
**之前**：可以执行任意命令

**现在**：只能执行白名单中的命令
- ✅ 允许：`uptime`, `free`, `df`, `ps`, `tail`, `grep` 等
- ❌ 禁止：`rm`, `mv`, `shutdown`, `systemctl start` 等

### 3. 配置文件加密
**之前**：密码明文存储

**现在**：密码自动加密存储

## 📝 文档更新

- ✅ 更新 SKILL.md（版本 2.1）
- ✅ 添加安全改进说明
- ✅ 添加命令白名单文档
- ✅ 创建 SECURITY_IMPROVEMENTS.md
- ✅ 创建 CHANGELOG.md

## 🔧 技术细节

### 加密技术
- 算法：AES-256-GCM
- 密钥长度：256 位
- IV：16 字节（随机生成）
- 认证标签：16 字节

### 文件权限
- 配置目录：700
- 配置文件：600
- 密钥文件：600

## 📊 允许的命令类型

### 系统信息
- `uptime`, `free`, `df`, `top`, `ps`, `uname`, `hostname`, `whoami`, `id`

### 日志查看
- `tail`, `grep`, `cat`, `less`, `journalctl`

### 网络检查
- `netstat`, `ss`, `lsof`, `curl`, `wget`, `ping`

### 进程和服务
- `systemctl status`, `docker ps`, `kubectl get`

### 文件和磁盘
- `ls`, `du`, `find`, `stat`

## 🚫 禁止的命令类型

### 文件操作
- `rm`, `rmdir`, `mv`, `cp`, `touch`, `chmod`, `chown`

### 系统控制
- `shutdown`, `reboot`, `poweroff`, `halt`

### 用户管理
- `useradd`, `userdel`, `usermod`, `passwd`

### 包管理
- `apt-get`, `apt`, `yum`, `dnf`, `pacman`, `npm`, `pip`

### 服务控制
- `systemctl start/stop/restart/reload`

### 危险操作
- `dd`, `mkfs`, `fdisk`, `parted`
- 任何包含管道、重定向、命令替换的命令

## 🔄 迁移指南

### 1. 更新服务器配置
为每个服务器添加 `user` 字段：
```json
{
  "host": "192.168.1.100",
  "port": 22,
  "user": "admin",
  "keyFile": "~/.ssh/id_rsa",
  "name": "web-1",
  "tags": ["production", "web"]
}
```

### 2. 检查命令白名单
确保使用的命令在白名单中，如果不在，请：
- 使用只读命令替代
- 联系管理员添加到白名单

### 3. 密码自动加密
首次加载时，未加密的密码会自动加密，无需手动操作。

## 🧪 测试建议

### 安全测试
1. 测试密码加密/解密
2. 测试命令白名单验证
3. 测试危险命令拒绝
4. 测试绕过方式检测

### 功能测试
1. 测试 SSH 连接（非 root 用户）
2. 测试允许的命令
3. 测试批量操作
4. 测试文件传输

## 📦 安装

```bash
cd /Users/a1234/.openclaw/workspace/skills/ops-maintenance
npm install
npm run build
```

## 🚀 使用

### 健康检查
```bash
/ops-maintenance health
/ops-maintenance admin@192.168.1.100 health
```

### 日志分析
```bash
/ops-maintenance logs error
/ops-maintenance admin@192.168.1.100 logs error
```

### 集群管理
```bash
/ops-maintenance cluster
/ops-maintenance cluster @production
```

## 📄 许可证

MIT

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📞 支持

如有问题，请提交 Issue 或联系维护者。

---

**注意**：这是一个重要的安全更新，建议所有用户尽快升级。
