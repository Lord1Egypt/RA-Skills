# Li Base Scan - 老李安全扫描工具

一款集成于 OpenClaw 的综合安全扫描工具，支持多种扫描模式和安全评估功能。

## 作者

**北京老李 (Beijing Lao Li)**

## 功能特性

- 🔍 **网络扫描**: 集成 Nmap 进行端口和服务发现
- 🛡️ **漏洞扫描**: Nikto 用于 Web 漏洞检测
- 🗄️ **SQL注入检测**: SQLMap 集成
- 📦 **容器安全**: Trivy 用于镜像扫描
- 🔒 **系统合规**: Lynis 用于系统审计
- 🤖 **AI智能分析**: 基于 LLM 的安全报告分析
- 📊 **报告生成**: 支持 Markdown、JSON 和 HTML 格式
- 📜 **扫描历史**: 基于 SQLite 的历史记录管理

## 安装

### 前置要求

确保系统已安装以下工具：

- `nmap` - 网络扫描器
- `nikto` - Web 漏洞扫描器
- `sqlmap` - SQL 注入工具
- `trivy` - 容器镜像扫描器
- `lynis` - 系统审计工具

### 通过 ClawHub 安装

```bash
clawhub skills install li-base-scan
```

## 使用方法

### 基础扫描

```bash
# 快速扫描 (30秒)
li-base-scan 192.168.1.1 --mode quick

# 标准扫描 (2-5分钟)
li-base-scan 192.168.1.1 --mode standard

# 完整扫描 (5-10分钟)
li-base-scan 192.168.1.1 --mode full
```

### Web 应用扫描

```bash
# Web 漏洞扫描
li-base-scan http://example.com --mode web

# Web + SQL 注入扫描
li-base-scan http://example.com --mode web_sql
```

### 合规与隐蔽扫描

```bash
# 合规审计
li-base-scan 192.168.1.1 --mode compliance

# 隐蔽扫描
li-base-scan 192.168.1.1 --mode stealth
```

### LLM 智能分析

```bash
# 启用 AI 智能分析 (需要 LLM_API_KEY)
li-base-scan 192.168.1.1 --mode full --llm
```

## 安全特性

- ✅ 目标地址哈希存储 (SHA-256) - 不存储敏感数据
- ✅ 文件权限限制 (敏感文件 0o600)
- ✅ 审计日志与隐私保护
- ✅ 使用 `shlex.quote()` 防止命令注入
- ✅ 单主机限制 (禁止 CIDR/范围扫描)
- ✅ 超时保护 (每个命令 5-30 分钟)

## 扫描模式

| 模式 | 时长 | 描述 |
|------|------|------|
| `quick` | ~30秒 | 快速端口扫描 |
| `standard` | 2-5分钟 | 标准安全扫描 |
| `full` | 5-10分钟 | 全面扫描 |
| `web` | 2-3分钟 | Web 漏洞扫描 |
| `web_sql` | 3-5分钟 | Web + SQL 注入扫描 |
| `compliance` | 可变 | 系统合规审计 |
| `stealth` | 可变 | 隐蔽模式扫描 |

## 报告输出

报告保存在 `reports/` 目录：
- `security-report-{timestamp}.md` - Markdown 报告
- `security-report-{timestamp}.json` - JSON 报告
- `security-report-{timestamp}.html` - HTML 报告

## 历史与日志

- **扫描历史**: 存储在 `history.db` (SQLite)
- **日志文件**: `~/.openclaw/logs/li-base-scan.log`

## 环境变量

- `LLM_API_KEY` - LLM 智能分析的 API 密钥
- `LLM_API_URL` - 自定义 LLM API 端点

## 许可证

MIT 许可证

## 安全声明

⚠️ **重要**: 本工具仅用于授权的安全测试。请确保您有权扫描目标系统。未经授权的扫描可能违反法律法规。
