# 弱密码检测指南

## weakpass_check.py

### 功能说明
检测常见服务的弱密码和默认凭证。

### 使用方法

```bash
# SSH 弱密码检测（仅测试常见弱密码）
python scripts/weakpass_check.py 192.168.1.1 --service ssh

# FTP 检测
python scripts/weakpass_check.py 192.168.1.1 --service ftp

# MySQL 检测
python scripts/weakpass_check.py 192.168.1.1 --service mysql

# 检测所有服务
python scripts/weakpass_check.py 192.168.1.1 --all
```

### 输出示例

```
=== 弱密码检测结果 ===
目标: 192.168.1.1
检测时间: 2026-03-18 14:30

=== SSH 服务检测 ===
端口: 22
状态: 开放
默认账户检测:
  root:admin123 ❌ 弱密码
  admin:password ❌ 弱密码
  admin:123456 ❌ 弱密码

风险评估:
🔴 高危: 发现弱密码组合

建议:
1. 立即修改弱密码
2. 禁用 root 远程登录
3. 使用 SSH 密钥认证
4. 启用失败登录锁定

=== FTP 服务检测 ===
端口: 21
状态: 开放
匿名登录: ❌ 不允许 (安全)

风险评估: 🟢 低

=== MySQL 检测 ===
端口: 3306
状态: 开放
默认空密码: ❌ 未发现 (安全)

风险评估: 🟢 低
```

## 常见默认凭证

### SSH

| 用户名 | 弱密码 |
|--------|--------|
| root | root, admin, 123456, password |
| admin | admin, password, 123456 |
| ubuntu | ubuntu |
| user | user, 123456 |

### FTP

| 服务 | 默认账户 |
|------|----------|
| vsftpd | anonymous |
| ProFTPD | admin |
| FileZilla | admin |

### 数据库

| 数据库 | 默认账户 |
|--------|----------|
| MySQL | root:(空) |
| PostgreSQL | postgres:postgres |
| Redis | (空密码) |
| MongoDB | (空密码) |

## 弱密码特征

以下密码被认定为弱密码：

1. **简单数字**: 123456, 12345678, 123456789
2. **键盘序列**: qwerty, asdfgh, zxcvbn
3. **常用单词**: password, admin, letmein, welcome
4. **重复字符**: aaaaa, 111111
5. **生日模式**: 19900101, 01011990
6. **用户名相关**: 用户名+123, 用户名+年份

## 密码安全建议

### 强密码规则

- 长度 ≥ 12 位
- 包含大小写字母 + 数字 + 特殊字符
- 不包含用户名、生日、手机号
- 不使用字典词汇

### 推荐方案

1. **SSH**: 使用 SSH 密钥替代密码
2. **数据库**: 使用强密码 + IP 白名单
3. **管理后台**: 启用双因素认证
4. **定期轮换**: 每 90 天更换一次密码

## 安全配置示例

### SSH (sshd_config)

```
PermitRootLogin no
PasswordAuthentication no
PubkeyAuthentication yes
MaxAuthTries 3
```

### MySQL (my.cnf)

```
bind-address = 127.0.0.1
require_secure_transport = ON
```

### Redis (redis.conf)

```
bind 127.0.0.1
requirepass <强密码>
protected-mode yes
```
