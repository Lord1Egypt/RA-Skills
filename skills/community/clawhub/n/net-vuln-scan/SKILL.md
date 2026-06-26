---
name: net-vuln-scan
description: |
  网络安全漏洞检测工具。用于检测本地网络和主机的常见安全漏洞，包括：
  (1) 开放端口检测与风险评估 (2) 弱密码和默认凭证检测 (3) SSL/TLS 证书问题 (4) 
  常见服务漏洞检测 (5) 网络配置安全检查 (6) 敏感端口暴露检测。
  适用于：安全审计、渗透测试前自查、系统加固、服务器上线检查。
  注意：仅用于授权的安全检测，禁止未授权扫描他人系统。
---

# 网络安全漏洞检测

## 概述

本技能提供主机和网络服务的安全漏洞检测能力。采用被动检测和指纹识别方式，发现潜在安全问题并提供修复建议。

## 检测项目

### 1. 端口扫描与风险评估

检测目标主机的开放端口，识别高风险服务。

**检测内容：**
- 常见高风险端口：21(FTP)、23(Telnet)、3389(RDP)、3306(MySQL)、5432(PostgreSQL)、6379(Redis)
- 敏感服务端口
- 建议关闭的端口

### 2. 弱密码与默认凭证检测

检测常见服务的默认或弱密码。

**检测内容：**
- SSH 弱密码检测（限制尝试次数）
- FTP 默认凭证
- 数据库默认端口检测
- 常见管理后台

### 3. SSL/TLS 证书检测

检测 HTTPS 服务的证书问题。

**检测内容：**
- 证书过期检测
- 证书链完整性
- 弱加密算法（SSLv3、TLS 1.0/1.1）
- 缺失 HSTS 头

### 4. 网络配置检测

检测主机的网络配置安全隐患。

**检测内容：**
- 防火墙状态
- 共享目录检测
- 本地管理员账户
- 来宾账户状态

### 5. 敏感信息泄露检测

检测常见配置文件的敏感信息泄露。

**检测内容：**
- 硬编码密码检测
- API Key 泄露
- 配置文件权限

## 使用方式

### 本地安全检测（推荐）

检测本机或内网主机的安全状况：

```
检测本机开放端口：scan ports localhost
检测远程主机：scan ports 192.168.1.1
SSL 证书检测：check ssl example.com
全面安全扫描：scan full 192.168.1.1
```

### 快速命令参考

| 命令 | 说明 |
|------|------|
| `scan ports <target>` | 端口扫描 |
| `check ssl <domain>` | SSL 证书检测 |
| `scan weakpass <target>` | 弱密码检测 |
| `scan network` | 内网主机发现 |
| `scan full <target>` | 全面扫描 |
| `report` | 生成安全报告 |

## 检测结果解读

### 风险等级

- **🔴 高危**：立即修复，可能导致被入侵
- **🟡 中危**：建议修复，存在一定风险
- **🟢 低危**：可选修复，安全性增强

### 常见漏洞修复

| 漏洞 | 修复建议 |
|------|----------|
| 开放 23 端口 | 关闭 Telnet，使用 SSH |
| 开放 3389 端口 | 仅内网访问，启用 NLA |
| MySQL 弱密码 | 修改强密码，限制远程访问 |
| SSL 证书过期 | 续期证书，配置自动更新 |
| 开放 6379(Redis) | 绑定 127.0.0.1，设置密码 |

## 输出格式

检测结果以结构化报告呈现，包含：
- 漏洞列表（按风险等级排序）
- 详细描述和影响
- 修复建议
- 参考链接

## 使用限制

- 仅用于授权系统检测
- 扫描频率限制：每秒 10 个端口
- 禁止对未授权目标进行检测
- 敏感操作需要管理员权限

## 新增功能：CVE 漏洞检测 (2026年3月更新)

### 检测最新高危漏洞

| CVE ID | 漏洞名称 | 严重程度 | CVSS |
|--------|----------|----------|------|
| CVE-2026-21514 | Microsoft Word OLE 绕过 | HIGH | 7.8 |
| CVE-2026-21262 | SQL Server 权限提升 | HIGH | 8.8 |
| CVE-2026-26110 | Office 远程代码执行 | CRITICAL | 8.4 |
| CVE-2026-26127 | .NET 拒绝服务 | HIGH | 7.5 |

### CVE 检测命令

```bash
# 检测所有高危 CVE
python scripts/cve_check.py all

# 检测指定 CVE
python scripts/cve_check.py CVE-2026-21514

# 检测 Office 漏洞
python scripts/cve_check.py CVE-2026-26110
```

## 新增功能：综合平台漏洞检测 (2026年3月更新)

### 各平台漏洞检测

支持检测以下平台的安全漏洞：

| 平台类别 | 检测内容 |
|----------|----------|
| **数据库** | MySQL, PostgreSQL, Redis, MongoDB, MSSQL |
| **网络服务** | SSH, Telnet, RDP, VPN |
| **Web 服务** | Apache, Nginx, IIS |
| **云服务** | AWS/Azure/GCP 元数据服务 |
| **容器/虚拟化** | Docker, Kubernetes, VMware |

### 平台检测命令

```bash
# 检测所有平台
python scripts/platform_check.py all

# 按平台检测
python scripts/platform_check.py 1    # 数据库平台
python scripts/platform_check.py 2    # 网络服务
python scripts/platform_check.py 3    # Web 服务
python scripts/platform_check.py 4    # 云服务
python scripts/platform_check.py 5    # 容器/虚拟化
```

### CVE 检测命令

```bash
# 检测所有高危 CVE
python scripts/cve_check.py all

# 检测指定 CVE
python scripts/cve_check.py CVE-2026-21514
```

## 相关脚本

- `scripts/port_scan.py` - 端口扫描
- `scripts/ssl_check.py` - SSL 证书检测
- `scripts/weakpass_check.py` - 弱密码检测
- `scripts/cve_check.py` - CVE 漏洞检测
- `scripts/platform_check.py` - 综合平台漏洞检测 (新增)
- `scripts/report_gen.py` - 报告生成

详细使用见 references/ 目录。
