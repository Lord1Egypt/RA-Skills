---
name: litellm-attack-detector
description: "Detect the LiteLLM supply chain attack (v1.82.7/1.82.8). Scans for compromised packages, malicious .pth files, backdoor persistence, suspicious network connections, and Kubernetes IoCs. No dependencies, read-only, safe to run."
metadata:
  {
    "openclaw":
      {
        "emoji": "🛡️",
        "requires": { "bins": ["bash"] },
        "tags": ["security", "supply-chain", "litellm", "malware", "incident-response", "安全", "供应链攻击"],
      },
  }
---

# LiteLLM Supply Chain Attack Detector

检测 LiteLLM 供应链攻击（v1.82.7 / v1.82.8，TeamPCP）的入侵指标。纯只读脚本，不修改任何文件，不发送任何数据，安全可靠。

Detect indicators of compromise (IoCs) from the LiteLLM supply chain attack (versions 1.82.7 / 1.82.8). Read-only script — no files modified, no data exfiltrated.

**Reference**: https://github.com/BerriAI/litellm/issues/24512

**Original script**: https://gist.github.com/sorrycc/30a765b9a82d0d8958e756b251828a19#file-check-litellm-sh (by [@sorrycc](https://github.com/sorrycc), adapted with bug fix: `set -euo pipefail` → `set -u`)

## Overview

2026 年 3 月，LiteLLM PyPI 包的 1.82.7 和 1.82.8 版本被植入恶意代码（供应链攻击）。攻击者通过 `.pth` 文件持久化后门，窃取环境变量中的凭据，并在 Kubernetes 环境中部署特权 Pod。

本 skill 提供一键检测脚本，覆盖 7 个检测维度：

| # | 检测项 | 说明 |
|---|--------|------|
| 1 | 版本检测 | 检查 pip/pip3/uv 中是否安装了受影响版本 |
| 2 | .pth 文件扫描 | 搜索 site-packages 和缓存目录中的恶意 `litellm_init.pth` |
| 3 | 后门持久化 | 检查 `~/.config/sysmon/`、`sysmon.service`、`/tmp/.pg_state` 等已知后门路径 |
| 4 | 网络连接 | 检查是否有到 `litellm.cloud` / `checkmarx.zone` 的活跃连接 |
| 5 | DNS 解析 | 确认恶意域名的 DNS 可达性 |
| 6 | Kubernetes | 检查 kube-system 中的可疑 Pod 和特权容器 |
| 7 | 依赖链 | 检查哪些包间接依赖了 litellm |

## When to Use

当用户的请求涉及以下场景时触发此技能：

- 检测 LiteLLM 供应链攻击："检查一下有没有中招"
- 安全扫描："扫描一下 litellm 是否被篡改"
- 事件响应："litellm 后门检测"
- 关键词触发："litellm attack"、"litellm 1.82.7"、"litellm 1.82.8"、"TeamPCP"、"supply chain"、"供应链攻击"

## How to Use

### 运行检测脚本

```bash
bash {{SKILL_DIR}}/scripts/detect.sh
```

脚本无需任何参数，无需 root 权限，自动检测当前环境。

### 输出说明

脚本使用彩色输出标识检测结果：

- 🟢 `[+]` 绿色 — 该项安全
- 🔴 `[!]` 红色 — 发现入侵指标（IoC）
- 🟡 `[*]` 黄色 — 信息提示

### 输出示例（安全环境）

```
============================================
 LiteLLM Supply Chain Attack Detector
 Target: litellm 1.82.7 / 1.82.8 (TeamPCP)
============================================

[*] Checking installed litellm version...
[+] litellm not installed via pip
[*] Searching for litellm_init.pth in Python site-packages...
[+] No litellm_init.pth found
[*] Checking for persistence artifacts...
[+] No persistence artifacts found
[*] Checking for suspicious network connections...
[+] No suspicious connections to known C2 domains
[*] Checking DNS resolution...
[*] Checking Kubernetes environment...
[*] kubectl not found, skipping Kubernetes checks
[*] Checking if litellm is a transitive dependency...

============================================
 CLEAN — No indicators of compromise found.
============================================
```

### 输出示例（受感染环境）

```
============================================
 ALERT — Indicators of compromise detected!

 Recommended actions:
   1. Uninstall litellm and delete litellm_init.pth manually
   2. Remove backdoor: ~/.config/sysmon/ and sysmon.service
   3. Purge caches: pip cache purge / rm -rf ~/.cache/uv
   4. ROTATE ALL CREDENTIALS:
      - SSH keys
      - AWS / GCP / Azure credentials
      - Kubernetes configs and service account tokens
      - All API keys in .env files
      - Database passwords
      - Git credentials
      - CI/CD secrets
   5. Audit cloud IAM logs for unauthorized access
   6. If in K8s: delete node-setup-* pods, audit secrets
============================================
```

### 退出码

- `0` — 未发现入侵指标
- `1` — 发现入侵指标，需要立即处理

## Edge Cases

- **无 pip/pip3**：自动跳过版本检测，继续其他检查项
- **无 python3**：`.pth` 文件搜索会使用备用路径（`~/.cache/pip`、`~/.cache/uv` 等）
- **无 kubectl**：自动跳过 Kubernetes 检查
- **无 lsof/ss**：跳过网络连接检测
- **虚拟环境**：自动检测 `$VIRTUAL_ENV` 路径
- **macOS / Linux 均支持**：脚本兼容两个平台
- **只读操作**：整个脚本不修改任何文件、不安装任何东西、不向外发送任何数据
