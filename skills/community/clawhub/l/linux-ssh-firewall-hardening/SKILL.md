---
author: peterliu-512
name: linux-ssh-firewall-hardening
description: Use when 排查SSH连不上/改端口/加固SSH与firewalld。
---

# Linux SSH 服务诊断与防火墙加固

## 触发场景
- SSH 远程连不上（某入口通、某入口不通）
- 改 SSH 端口 / 加固 root 登录 / 收紧防火墙

## 权威配置核对：`sshd -T`
```bash
sudo sshd -T | grep -iE '^(port|permitrootlogin|passwordauthentication|pubkeyauthentication)'
```
直接输出 sshd **实际生效值**，比肉眼读 sshd_config 可靠。

## 关键坑：OpenSSH 重复指令取「第一个值」
sshd_config 中对同一关键字重复出现时，**第一个获得的值生效**（后续重复被忽略）。
例：第71行 `PasswordAuthentication yes` + 第150行 `PasswordAuthentication no` → 实际生效 **yes**，不是 no。
判断前先 `sshd -T` 核实，勿凭"最后一行"臆断。

## firewalld 端口同步坑
改 sshd `Port 22→50022` 后，firewalld 的 `ssh` 服务仍指向 22，不会自动跟随。后果：新端口被默认 reject，远程连不上。
修复（最小暴露面，仅放行 LAN 网段）：
```bash
sudo firewall-cmd --permanent --add-rich-rule='rule family="ipv4" source address="192.168.1.0/24" port port="50022" protocol="tcp" accept'
sudo firewall-cmd --reload
```

## 多入口表现不一致的根因
- 物理网卡入口（192.168.x）走 firewalld → 新端口未放行即被拒。
- Tailscale 入口（100.x）走 `ts-input` 链对 `tailscale0` 接口直接 `-j ACCEPT`，**绕过 firewalld**，所以一直通。
定位法：`iptables -S ts-input`、`nft list ruleset | grep <port>`、`firewall-cmd --list-all`。

## 加固动作
```bash
# 改前备份
sudo cp -a /etc/ssh/sshd_config /etc/ssh/sshd_config.bak.$(date +%Y%m%d)
# root 禁密码登录（仅密钥）
sudo sed -i 's/^PermitRootLogin yes$/PermitRootLogin prohibit-password/' /etc/ssh/sshd_config
# 移除已无监听的旧端口服务（收紧假放行）
sudo firewall-cmd --permanent --remove-service=ssh && sudo firewall-cmd --reload
# reload 保持已有连接（勿 restart 断会话）
sudo systemctl reload sshd
```

## 验证闭环
```bash
sudo sshd -T | grep -iE 'permitrootlogin|passwordauthentication'
sudo firewall-cmd --list-rich-rules   # 确认新端口规则在位、未误伤
sudo ss -tlnp | grep -E ':(22|50022)' # 新端口监听、旧端口无
```

## 注意
- `PasswordAuthentication` 收紧为 `no` 前，务必确认用户当前是密钥登录（否则把自己锁门外），且改完立即用密钥复测。
- `systemctl reload sshd` 对 Port/ListenAddress 等需 restart 才生效；PermitRootLogin/PasswordAuthentication 属 per-connection，reload 即可。
