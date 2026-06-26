---
name: li-base-scan
description: Linux base security scanner integrating multiple tools - nmap, lynis, nikto, sqlmap, trivy. SINGLE HOST ONLY. Features secure temp files, progress bar, scan history, report export. Comprehensive security baseline scanning with hardened implementation.
license: MIT
metadata:
  author: 北京老李 (Beijing Lao Li)
  version: "0.0.2"
  tags: [security, scanning, nmap, linux, audit]
---

# Li Base Scan v0.0.2 - Linux安全基线扫描器 / Linux Security Baseline Scanner

**作者 Author**: 北京老李 (Beijing Lao Li)  
**版本 Version**: 0.0.2  
**许可证 License**: MIT

---

## 🌐 Language / 语言

- [中文说明](#中文文档-chinese-docs)
- [English Documentation](#english-documentation)

---

<a name="中文文档-chinese-docs"></a>
## 中文文档 Chinese Docs

### ⚠️ 安全限制 - 重要

**本工具仅支持单主机扫描，出于安全考虑，以下输入会被拒绝：**
- ❌ CIDR网段 (如 192.168.1.0/24)
- ❌ IP范围 (如 192.168.1.1-254)
- ❌ 多目标 (如 192.168.1.1,192.168.1.2)

**允许的目标格式：**
- ✅ 单个IP: `192.168.1.1`
- ✅ 域名: `scanme.nmap.org`
- ✅ 本地地址: `127.0.0.1`, `localhost`

### 概述

Li Base Scan 是一个集成多种安全工具的Linux基线扫描器，v0.0.2版本包含以下增强功能：
- **网络安全** - 使用安全临时文件、完善超时处理、错误脱敏
- **进度显示** - 实时进度条显示扫描进度
- **历史记录** - SQLite数据库存储扫描历史
- **报告导出** - 支持Markdown和JSON格式导出
- **AI分析** - 自动生成AI分析请求区块

### 集成工具

| 工具 | 功能 | 扫描类型 |
|------|------|----------|
| **nmap** | 端口扫描、服务识别 | 网络层 |
| **lynis** | 系统安全审计 | 主机层 |
| **nikto** | Web漏洞扫描 | 应用层 |
| **sqlmap** | SQL注入测试 | 应用层 |
| **trivy** | 容器/文件系统漏洞 | 多层 |

### 扫描模式

#### 1. Quick Scan (快速扫描)
```
快速扫描 127.0.0.1
```
- **工具**: nmap
- **时间**: ~30秒
- **用途**: 快速了解开放端口

#### 2. Standard Scan (标准扫描)
```
标准扫描 127.0.0.1
```
- **工具**: nmap + lynis
- **时间**: 2-5分钟
- **用途**: 端口+系统配置审计

#### 3. Full Scan (完整扫描)
```
完整扫描 127.0.0.1
完整扫描 127.0.0.1 包含web
```
- **工具**: nmap + lynis + trivy
- **时间**: 5-10分钟
- **用途**: 全面安全评估

#### 4. Web Focused (Web专项)
```
web扫描 http://localhost
扫描网站 http://example.com
```
- **工具**: nmap + nikto
- **时间**: 2-3分钟
- **用途**: Web应用安全检测

#### 5. Compliance (合规检查)
```
合规扫描 127.0.0.1
基线检查 localhost
```
- **工具**: lynis + trivy
- **时间**: 3-5分钟
- **用途**: CIS基线合规检查

#### 6. Stealth (隐蔽扫描) [v0.0.2新增]
```
隐蔽扫描 192.168.1.1
慢速扫描 target.com
```
- **工具**: nmap (stealth模式)
- **时间**: 5-10分钟
- **用途**: 避免IDS/IPS检测

### 对话输入示例

#### 基础命令
```
"快速扫描 192.168.1.1"
"标准扫描 localhost"
"检查系统安全"
"扫描网站 http://localhost:8080"
"完整安全评估 127.0.0.1"
"基线扫描"
"隐蔽扫描 10.0.0.1"
```

#### LLM 交互式对话
```
"扫描 example.com 并检查SQL注入"
"发现什么漏洞？"
"给我修复建议"
"导出HTML报告"
"系统加固情况如何？"
"Web应用有什么问题？"
```

### 命令行使用

#### 基本扫描
```bash
# 快速扫描
python3 scripts/li_base_scan.py 127.0.0.1 --mode quick

# 标准扫描
python3 scripts/li_base_scan.py 127.0.0.1 --mode standard

# 完整扫描
python3 scripts/li_base_scan.py 127.0.0.1 --mode full
```

#### 对话模式
```bash
python3 scripts/li_base_scan.py -c "快速扫描 127.0.0.1"
```

#### 导出报告 [v0.0.2新增]
```bash
# 导出Markdown报告
python3 scripts/li_base_scan.py 127.0.0.1 --mode full --export markdown

# 导出JSON报告
python3 scripts/li_base_scan.py 127.0.0.1 --mode full --export json

# 生成HTML报告（通过entrypoint）
python3 scripts/entrypoint.py '{"target": "127.0.0.1", "tools": ["nmap", "lynis"], "format": "html"}'
```

#### 查看历史 [v0.0.2新增]
```bash
python3 scripts/li_base_scan.py --history
```

#### JSON输出
```bash
python3 scripts/li_base_scan.py 127.0.0.1 --mode standard --json
```

### 输出格式

#### 控制台报告
- **执行摘要** - 整体风险评级
- **网络发现** - nmap端口扫描结果
- **系统审计** - lynis合规评分和建议
- **Web安全** - nikto发现的Web漏洞
- **漏洞清单** - trivy发现的CVE
- **修复建议** - 按优先级排序的行动项
- **AI分析区块** - 供大模型分析的原始数据

#### 导出文件 [v0.0.2新增]
报告保存在: `/root/.openclaw/skills/li-base-scan/reports/`
- `scan_<hash>_<timestamp>.md` - Markdown格式
- `scan_<hash>_<timestamp>.json` - JSON格式

#### 历史记录 [v0.0.2新增]
数据库位置: `/root/.openclaw/skills/li-base-scan/history.db`

### v0.0.2 安全增强

#### 1. 安全临时文件
```python
# 使用tempfile.NamedTemporaryFile代替硬编码路径
with tempfile.NamedTemporaryFile(mode='w', suffix='.json', 
                                 delete=False, dir='/tmp') as f:
    temp_file = f.name
os.chmod(temp_file, 0o600)  # 限制权限
```

#### 2. 完善的超时处理
```python
# 子进程超时后正确终止
proc.terminate()
try:
    proc.wait(timeout=5)
except subprocess.TimeoutExpired:
    proc.kill()
```

#### 3. 错误信息脱敏
```python
# 不暴露内部实现细节
return {"error": "扫描执行失败", "tool": "nmap"}
# 详细错误记录到日志
logger.error(f"Nmap scan failed")
```

#### 4. 审计日志
日志位置: `/var/log/li-base-scan.log`
```
2024-01-01 10:00:00 - INFO - Starting scan: mode=quick, target_hash=a1b2c3d4
```

### 依赖工具

```bash
# 安装所有依赖
apt-get update
apt-get install -y nmap lynis nikto sqlmap

# trivy安装
curl -sfL https://raw.githubusercontent.com/aquasecurity/trivy/main/contrib/install.sh | sh
```

### 使用建议

#### 快速检查 (日常)
```bash
python3 scripts/li_base_scan.py -c "快速扫描 127.0.0.1"
```

#### 定期深度扫描 (每周)
```bash
python3 scripts/li_base_scan.py 127.0.0.1 --mode full --export markdown
```

#### Web应用测试
```bash
python3 scripts/li_base_scan.py http://localhost:8080 --mode web
```

#### 查看历史趋势
```bash
python3 scripts/li_base_scan.py --history
```

### 安全警告

⚠️ **仅扫描您拥有或获得明确授权的系统！**
- 未经授权的扫描可能违反法律
- sqlmap测试需谨慎，可能触发WAF/IDS
- 生产环境请使用--safe-mode避免破坏性测试

### 故障排除

#### 扫描超时
```bash
# 增加超时时间
python3 scripts/li_base_scan.py 127.0.0.1 --timeout 600
```

#### 禁用进度条
```bash
# JSON输出或禁用进度
python3 scripts/li_base_scan.py 127.0.0.1 --json
python3 scripts/li_base_scan.py 127.0.0.1 --no-progress
```

#### 查看日志
```bash
tail -f /var/log/li-base-scan.log
```

---

<a name="english-documentation"></a>
## English Documentation

### ⚠️ Security Restrictions - Important

**This tool supports SINGLE HOST scanning only. The following inputs are REJECTED for security reasons:**
- ❌ CIDR ranges (e.g., 192.168.1.0/24)
- ❌ IP ranges (e.g., 192.168.1.1-254)
- ❌ Multiple targets (e.g., 192.168.1.1,192.168.1.2)

**Allowed target formats:**
- ✅ Single IP: `192.168.1.1`
- ✅ Domain: `scanme.nmap.org`
- ✅ Local address: `127.0.0.1`, `localhost`

### Overview

Li Base Scan is a Linux security baseline scanner integrating multiple tools. Version 0.0.2 includes:
- **Security Hardening** - Secure temp files, proper timeout handling, error sanitization
- **Progress Display** - Real-time progress bar
- **Scan History** - SQLite database for scan history
- **Report Export** - Markdown and JSON export support
- **AI Analysis** - Auto-generated AI analysis blocks

### Integrated Tools

| Tool | Function | Scan Type |
|------|----------|-----------|
| **nmap** | Port scanning, service detection | Network Layer |
| **lynis** | System security audit | Host Layer |
| **nikto** | Web vulnerability scanning | Application Layer |
| **sqlmap** | SQL injection testing | Application Layer |
| **trivy** | Container/filesystem vulnerabilities | Multi-layer |

### Scan Modes

#### 1. Quick Scan
```
quick scan 127.0.0.1
```
- **Tool**: nmap
- **Time**: ~30 seconds
- **Purpose**: Quick port discovery

#### 2. Standard Scan
```
standard scan 127.0.0.1
```
- **Tools**: nmap + lynis
- **Time**: 2-5 minutes
- **Purpose**: Port + system configuration audit

#### 3. Full Scan
```
full scan 127.0.0.1
```
- **Tools**: nmap + lynis + trivy
- **Time**: 5-10 minutes
- **Purpose**: Comprehensive security assessment

#### 4. Web Focused
```
web scan http://localhost
scan website http://example.com
```
- **Tools**: nmap + nikto
- **Time**: 2-3 minutes
- **Purpose**: Web application security detection

#### 5. Compliance
```
compliance scan 127.0.0.1
baseline check localhost
```
- **Tools**: lynis + trivy
- **Time**: 3-5 minutes
- **Purpose**: CIS baseline compliance check

#### 6. Stealth [v0.0.2 New]
```
stealth scan 192.168.1.1
slow scan target.com
```
- **Tool**: nmap (stealth mode)
- **Time**: 5-10 minutes
- **Purpose**: Avoid IDS/IPS detection

### Command Line Usage

#### Basic Scanning
```bash
# Quick scan
python3 scripts/li_base_scan.py 127.0.0.1 --mode quick

# Standard scan
python3 scripts/li_base_scan.py 127.0.0.1 --mode standard

# Full scan
python3 scripts/li_base_scan.py 127.0.0.1 --mode full
```

#### Conversation Mode
```bash
python3 scripts/li_base_scan.py -c "quick scan 127.0.0.1"
```

#### Export Reports [v0.0.2 New]
```bash
# Export Markdown report
python3 scripts/li_base_scan.py 127.0.0.1 --mode full --export markdown

# Export JSON report
python3 scripts/li_base_scan.py 127.0.0.1 --mode full --export json
```

#### View History [v0.0.2 New]
```bash
python3 scripts/li_base_scan.py --history
```

#### JSON Output
```bash
python3 scripts/li_base_scan.py 127.0.0.1 --mode standard --json
```

### Output Format

#### Console Report
- **Executive Summary** - Overall risk rating
- **Network Discovery** - nmap port scan results
- **System Audit** - lynis compliance score and recommendations
- **Web Security** - Web vulnerabilities found by nikto
- **Vulnerability List** - CVEs discovered by trivy
- **Remediation** - Prioritized action items
- **AI Analysis Block** - Raw data for LLM analysis

#### Exported Files [v0.0.2 New]
Reports saved to: `/root/.openclaw/skills/li-base-scan/reports/`
- `scan_<hash>_<timestamp>.md` - Markdown format
- `scan_<hash>_<timestamp>.json` - JSON format

#### History [v0.0.2 New]
Database location: `/root/.openclaw/skills/li-base-scan/history.db`

### v0.0.2 Security Enhancements

#### 1. Secure Temp Files
```python
# Use tempfile.NamedTemporaryFile instead of hardcoded paths
with tempfile.NamedTemporaryFile(mode='w', suffix='.json', 
                                 delete=False, dir='/tmp') as f:
    temp_file = f.name
os.chmod(temp_file, 0o600)  # Restrict permissions
```

#### 2. Proper Timeout Handling
```python
# Properly terminate subprocess after timeout
proc.terminate()
try:
    proc.wait(timeout=5)
except subprocess.TimeoutExpired:
    proc.kill()
```

#### 3. Error Sanitization
```python
# Don't expose internal implementation details
return {"error": "Scan execution failed", "tool": "nmap"}
# Log detailed errors
logger.error(f"Nmap scan failed")
```

#### 4. Audit Logging
Log location: `/var/log/li-base-scan.log`
```
2024-01-01 10:00:00 - INFO - Starting scan: mode=quick, target_hash=a1b2c3d4
```

### Dependencies

```bash
# Install all dependencies
apt-get update
apt-get install -y nmap lynis nikto sqlmap

# Install trivy
curl -sfL https://raw.githubusercontent.com/aquasecurity/trivy/main/contrib/install.sh | sh
```

### Usage Recommendations

#### Quick Check (Daily)
```bash
python3 scripts/li_base_scan.py -c "quick scan 127.0.0.1"
```

#### Periodic Deep Scan (Weekly)
```bash
python3 scripts/li_base_scan.py 127.0.0.1 --mode full --export markdown
```

#### Web Application Testing
```bash
python3 scripts/li_base_scan.py http://localhost:8080 --mode web
```

#### View History Trends
```bash
python3 scripts/li_base_scan.py --history
```

### Security Warning

⚠️ **Only scan systems you own or have explicit authorization to scan!**
- Unauthorized scanning may violate laws
- sqlmap tests should be used cautiously, may trigger WAF/IDS
- Use --safe-mode in production to avoid destructive testing

### Troubleshooting

#### Scan Timeout
```bash
# Increase timeout
python3 scripts/li_base_scan.py 127.0.0.1 --timeout 600
```

#### Disable Progress Bar
```bash
# JSON output or disable progress
python3 scripts/li_base_scan.py 127.0.0.1 --json
python3 scripts/li_base_scan.py 127.0.0.1 --no-progress
```

#### View Logs
```bash
tail -f ~/.openclaw/logs/li-base-scan.log
```

---

## 📞 Contact / 联系方式

**Author**: 北京老李 (Beijing Lao Li)  
**Email**: (请添加您的邮箱)  
**GitHub**: (请添加您的GitHub链接)

---

*Made with ❤️ by 北京老李 (Beijing Lao Li)*
