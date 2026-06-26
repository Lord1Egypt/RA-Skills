# 安全改进报告 (v2.1)

## 概述

ops-maintenance v2.1 版本针对 ClawHub 安全扫描发现的问题进行了全面修复，提升了 skill 的安全性和合规性。

## 修复的安全问题

### 1. 移除默认 root 用户

**问题描述**：
- 原代码在 `ssh-pool.ts` 中默认使用 `root` 用户连接 SSH
- 这可能导致权限过大，增加安全风险

**修复方案**：
- 移除默认用户逻辑，要求必须显式指定 SSH 用户
- 在 `ssh-pool.ts` 第 62-66 行添加安全检查
- 如果未指定用户，抛出错误提示

**代码位置**：
- `src/utils/ssh-pool.ts:62-66`

### 2. 密码加密存储

**问题描述**：
- 原代码在 `~/.config/ops-maintenance/servers.json` 中明文存储 SSH 密码
- 密码文件权限不严格，可能被其他用户读取

**修复方案**：
- 创建 `crypto.ts` 模块，使用 AES-256-GCM 加密算法
- 自动生成并保存加密密钥到 `~/.config/ops-maintenance/.key`（权限 600）
- 保存时自动加密密码，加载时自动解密
- 配置文件权限设置为 600（仅用户可读写）

**代码位置**：
- `src/utils/crypto.ts`（新文件）
- `src/index.ts:76-93`（修改 saveServers/loadServers）

### 3. 命令白名单验证

**问题描述**：
- 原代码可以执行任意命令，包括危险操作
- 批量执行命令功能可能被滥用

**修复方案**：
- 创建 `command-validator.ts` 模块，实现命令白名单验证
- 定义允许的安全命令（只读操作）
- 定义危险命令黑名单（删除、修改、系统控制等）
- 检测管道、重定向、命令替换等绕过方式
- 在 `executeOnAllServers`、`runRemoteCommand`、`runCommand` 中添加验证

**代码位置**：
- `src/utils/command-validator.ts`（新文件）
- `src/index.ts:197-202`（executeOnAllServers）
- `src/index.ts:376-381`（runRemoteCommand）
- `src/index.ts:403-408`（runCommand）

### 4. 移除 shell 执行

**问题描述**：
- 原代码在 `runCommand` 中使用 `/bin/zsh` shell 执行命令
- 可能导致命令注入攻击

**修复方案**：
- 移除 `shell: '/bin/zsh'` 参数
- 直接执行命令，不通过 shell 解释
- 配合命令白名单验证，防止命令注入

**代码位置**：
- `src/index.ts:410`（移除 shell 参数）

### 5. 增强安全检查

**问题描述**：
- 原代码缺少对特殊字符和绕过方式的检测

**修复方案**：
- 检测管道符 `|`
- 检测重定向 `>` 和 `>>`
- 检测命令替换 `$()` 和 `` ` ``
- 检测分号 `;`
- 检测逻辑运算符 `&&` 和 `||`

**代码位置**：
- `src/utils/command-validator.ts:95-115`

## 允许的命令类型

### 系统信息查看
- `uptime`, `free`, `df`, `top`, `ps`, `uname`, `hostname`, `whoami`, `id`

### 日志查看
- `tail`, `grep`, `cat`, `less`, `journalctl`

### 网络检查
- `netstat`, `ss`, `lsof`, `curl`, `wget`, `ping`

### 进程和服务状态
- `systemctl status`, `systemctl is-active`, `service status`

### 磁盘和文件查看
- `ls`, `du`, `find`, `stat`

### 容器编排（只读）
- `docker ps`, `docker images`, `docker inspect`, `docker logs`, `docker stats`
- `kubectl get`, `kubectl describe`, `kubectl logs`, `kubectl top`

## 禁止的命令类型

### 文件操作
- `rm`, `rmdir`, `mv`, `cp`, `touch`, `chmod`, `chown`

### 系统控制
- `shutdown`, `reboot`, `poweroff`, `halt`

### 用户管理
- `useradd`, `userdel`, `usermod`, `passwd`

### 包管理
- `apt-get`, `apt`, `yum`, `dnf`, `pacman`, `npm`, `pip`

### 服务控制
- `systemctl start/stop/restart/reload`, `service start/stop/restart/reload`

### 网络配置
- `iptables`, `ufw`, `firewall-cmd`, `ifconfig`, `ip`, `route`

### 危险操作
- `dd`, `mkfs`, `fdisk`, `parted`
- 任何包含管道、重定向、命令替换的命令

## 加密技术细节

### 加密算法
- 算法：AES-256-GCM
- 密钥长度：256 位（32 字节）
- 初始化向量（IV）：16 字节（随机生成）
- 认证标签：16 字节

### 密钥管理
- 密钥文件位置：`~/.config/ops-maintenance/.key`
- 密钥文件权限：600（仅用户可读写）
- 密钥生成：使用 `crypto.randomBytes(32)` 生成
- 密钥存储：首次使用时自动生成并保存

### 加密格式
```
iv:authTag:encrypted
```
- `iv`：初始化向量（hex 编码）
- `authTag`：认证标签（hex 编码）
- `encrypted`：加密后的密码（hex 编码）

## 文件权限

### 配置目录
- 位置：`~/.config/ops-maintenance/`
- 权限：700（仅用户可读写执行）

### 服务器配置文件
- 位置：`~/.config/ops-maintenance/servers.json`
- 权限：600（仅用户可读写）

### 加密密钥文件
- 位置：`~/.config/ops-maintenance/.key`
- 权限：600（仅用户可读写）

### 审计日志目录
- 位置：`~/.config/ops-maintenance/logs/`
- 权限：700（仅用户可读写执行）

## 向后兼容性

### 配置文件迁移
- 旧版本的明文密码配置会自动加密
- 首次加载时会检测并加密未加密的密码
- 加密后的配置文件与旧版本不兼容（需要 v2.1+）

### 命令兼容性
- 旧版本允许的命令在新版本中可能被拒绝
- 需要更新命令以符合白名单要求
- 建议使用只读命令替代修改操作

### 用户配置
- 必须显式指定 SSH 用户，不再默认使用 root
- 需要更新服务器配置，添加 `user` 字段

## 测试建议

### 安全测试
1. 测试密码加密/解密功能
2. 测试命令白名单验证
3. 测试危险命令拒绝
4. 测试绕过方式检测

### 功能测试
1. 测试 SSH 连接（使用非 root 用户）
2. 测试允许的命令执行
3. 测试批量操作
4. 测试文件传输

### 兼容性测试
1. 测试旧配置文件迁移
2. 测试密钥文件生成
3. 测试权限设置

## 文档更新

### SKILL.md
- 更新版本号到 v2.1
- 添加安全改进说明
- 添加命令白名单说明
- 更新认证方式说明

### package.json
- 更新版本号到 2.1.0
- 更新描述为"安全增强版"

## 后续改进建议

1. **密钥轮换**：定期更换加密密钥
2. **多因素认证**：支持 SSH 证书或 OTP
3. **审计日志加密**：加密审计日志内容
4. **命令审计**：记录所有执行的命令
5. **权限分离**：支持不同用户不同权限
6. **配置验证**：启动时验证配置完整性

## 总结

ops-maintenance v2.1 通过以下方式提升了安全性：

1. ✅ 移除默认 root 用户，要求显式指定
2. ✅ 使用 AES-256-GCM 加密存储密码
3. ✅ 实现命令白名单验证
4. ✅ 移除 shell 执行，防止命令注入
5. ✅ 增强安全检查，检测绕过方式
6. ✅ 严格设置文件权限

这些改进使得 skill 符合 ClawHub 的安全要求，降低了安全风险，提升了合规性。
