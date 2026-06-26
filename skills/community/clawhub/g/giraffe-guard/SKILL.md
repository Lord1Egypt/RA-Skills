# 🦒 Giraffe Guard — 长颈鹿卫士

Scan OpenClaw skill directories for supply chain attacks and malicious code.
扫描 OpenClaw skill 目录，检测潜在的供应链投毒和恶意代码。

## Features / 功能

- 22 security detection rules covering the full supply chain attack surface / 22 条检测规则，覆盖供应链攻击全链路
- **Context-aware**: distinguishes documentation from executable code, reducing false positives / **上下文感知**：区分文档描述和实际可执行代码，降低误报
- Colored terminal output + JSON report output / 彩色终端输出 + JSON 格式报告
- `--verbose` mode shows matching line context / `--verbose` 模式显示匹配行上下文
- `--skip-dir` to exclude directories / `--skip-dir` 跳过指定目录
- Whitelist support / 白名单机制
- Compatible with macOS and Linux, zero external dependencies / 兼容 macOS 和 Linux，零外部依赖

## Usage / 使用方法

### Scan a skill directory / 扫描目录

```bash
{baseDir}/scripts/audit.sh /path/to/skills
```

### Verbose mode / 详细模式

```bash
{baseDir}/scripts/audit.sh --verbose /path/to/skills
```

### JSON report / JSON 报告

```bash
{baseDir}/scripts/audit.sh --json /path/to/skills
```

### With whitelist / 使用白名单

```bash
{baseDir}/scripts/audit.sh --whitelist whitelist.txt /path/to/skills
```

### Skip directories / 跳过目录

```bash
{baseDir}/scripts/audit.sh --skip-dir node_modules --skip-dir vendor /path/to/skills
```

### Combined / 组合使用

```bash
{baseDir}/scripts/audit.sh --verbose --context 3 --whitelist whitelist.txt --skip-dir node_modules /path/to/skills
```

## Detection Rules (22) / 检测规则

### 🔴 Critical / 严重级别
| # | Rule | EN | 中文 |
|---|------|----|------|
| 1 | pipe-execution | Pipe execution (curl/wget to bash) | 管道执行 |
| 2 | base64-decode-pipe | Base64 decoded and piped | Base64 解码管道执行 |
| 3 | security-bypass | macOS Gatekeeper/SIP bypass | 安全机制绕过 |
| 5 | tor-onion-address | Tor hidden service | 暗网地址 |
| 5 | reverse-shell | Reverse shell patterns | 反向 shell |
| 7 | file-type-disguise | Binary disguised as text | 文件类型伪装 |
| 8 | ssh-key-exfiltration | SSH key theft | SSH 密钥窃取 |
| 8 | cloud-credential-access | Cloud credential access | 云凭证访问 |
| 8 | env-exfiltration | Env vars sent over network | 环境变量外传 |
| 9 | anti-sandbox | Anti-debug/anti-sandbox | 反沙盒/反调试 |
| 10 | covert-downloader | One-liner downloaders | 单行下载器 |
| 11 | persistence-launchagent | macOS LaunchAgent | 持久化 |
| 13 | string-concat-bypass | String concatenation bypass | 字符串拼接绕过 |
| 15 | env-file-leak | .env with real secrets | .env 密钥泄露 |
| 16 | typosquat-npm/pip | Typosquatting packages | 包名仿冒 |
| 17 | malicious-postinstall | Malicious lifecycle scripts | 恶意生命周期脚本 |
| 18 | git-hooks | Active git hooks | 活跃 git hooks |
| 19 | sensitive-file-leak | Private keys/credentials | 私钥/凭证泄露 |
| 20 | skillmd-prompt-injection | Prompt injection in SKILL.md | SKILL.md prompt 注入 |
| 21 | dockerfile-privileged | Docker privileged mode | Docker 特权模式 |
| 22 | zero-width-chars | Zero-width Unicode chars | 零宽 Unicode 字符 |

### 🟡 Warning / 警告级别
| # | Rule | EN | 中文 |
|---|------|----|------|
| 2 | long-base64-string | Long Base64 strings | 超长 Base64 字符串 |
| 4 | dangerous-permissions | Dangerous permissions | 危险权限修改 |
| 5 | suspicious-network-ip | Non-local IP connections | 非本地 IP 直连 |
| 5 | netcat-listener | Netcat listeners | netcat 监听 |
| 6 | covert-exec-eval | Suspicious eval() (JS/TS) | 可疑 eval 调用 |
| 6 | covert-exec-python | os.system/subprocess in .py | Python 危险调用 |
| 11 | cron-injection | Cron/launchctl injection | 定时任务注入 |
| 12 | hidden-executable | Hidden executable files | 隐藏可执行文件 |
| 13 | hex/unicode-obfuscation | Hex/Unicode obfuscation | hex/Unicode 混淆 |
| 14 | symlink-sensitive | Symlinks to sensitive paths | 敏感符号链接 |
| 16 | custom-registry | Non-official registries | 非官方包源 |
| 20 | skillmd-privilege-escalation | Privilege escalation | 权限提升 |
| 21 | dockerfile-sensitive-mount | Sensitive mounts | 敏感目录挂载 |
| 21 | dockerfile-host-network | Host network mode | 主机网络模式 |

## Exit Codes / 退出码

- `0` — ✅ Clean / 安全
- `1` — 🟡 Warnings / 有警告
- `2` — 🔴 Critical / 有严重发现

## Dependencies / 依赖

No external dependencies. Uses: bash, grep, sed, find, file, awk, readlink, perl
零外部依赖，仅使用系统自带工具。
