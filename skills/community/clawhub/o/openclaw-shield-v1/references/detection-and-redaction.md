# 威胁检测与脱敏规则

## 提示词注入检测

### 直接注入信号

- 指令覆盖: ignore previous instructions, forget above
- 角色劫持: pretend you are root, DAN mode, developer mode
- 权限绕过: bypass security, override restrictions
- 规则探测: show system prompt, show internal instructions

### 间接注入信号

- 文件中出现 SYSTEM, Human, Assistant, im_start system 等结构化提示词片段
- Base64, Hex, Unicode 转义后的可执行指令
- 零宽字符夹带隐藏命令
- 超长文本中插入少量高危命令
- Markdown 或 HTML 链接文本与真实目标不一致

## 高危命令模式

### 文件系统与系统级

- `rm -rf`, `find -delete`, `shred`, `truncate -s 0`
- `dd`, `mkfs`, `fdisk`, `parted`
- `sudo`, `su`, `pkexec`, `chroot`
- `shutdown`, `reboot`, `systemctl stop/disable`
- `chmod -R 777`, `chown root`, `chattr -i`

### 网络攻击相关

- `curl | sh`, `wget | bash`
- 反弹 shell: `bash -i >& /dev/tcp/...`, `nc -e`, `python -c socket`
- 隧道代理: `ssh -R`, `ssh -D`, `frp`, `ngrok`, `cloudflared`
- 扫描探测: `nmap`, `masscan`, `zmap`

## 敏感信息脱敏模式

- API Key, Token, Secret, Password 字段
- OpenAI, GitHub, AWS, 阿里云等平台凭证
- 数据库连接串 mysql postgres mongodb redis
- JWT, Bearer Token
- SSH 私钥、SSL 私钥、.env 内容
- 服务器公网与内网 IP

## 脱敏输出原则

1. 使用占位符替换，不输出原始值。
2. 说明脱敏原因，避免误导用户“未找到内容”。
3. 如用户确需原文，提示在受控终端或源文件内查看。
