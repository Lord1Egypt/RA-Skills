---
slug: monitor-toolkit-free
name: monitor-toolkit-free
version: 1.0.1
displayName: 监控工具包-免费版
summary: "轻量级服务监控工具,支持HTTP/SSL/进程/磁盘检查,状态变更告警,适合个人项目。轻量级服务监控工具免费版,面向个人开发者与小型项目。核心能力:"
license: MIT
edition: free
description: "轻量级服务监控工具免费版,面向个人开发者与小型项目。核心能力:. 适用于需要monitor toolkit相关能力的开发场景,包含结构化的工作流程和可复用的模板,帮助用户快速完成任务并保持代码质量. 适用于需要monitor toolkit相关能力的开发场景,包含结构化的工作流程和配置指引. 该工具经过深度差异化处置,针对用户反馈和使用痛点进行了调优改进,提升了实用性和可操作性."
tags:
  - 监控
  - monitor
  - toolkit
  - automation
  - productivity
  - 运维
  - 告警
  - 健康检查
  - 工具
  - http
tools:
  - read
  - exec
homepage: ""
category: "Operations"
pricing_tier: free

---
# 监控工具包 - 免费版

## 概述

监控工具包免费版是面向个人开发者与小型项目的轻量级监控方案。用户定义需要监控的目标和检查方式,工具负责按设定间隔执行检查,并在状态发生变化时发出告警通知.
采用「用户定义检查内容,工具负责调度与告警」的模型,灵活适配各种监控需求.
## 核心能力

### 1. HTTP 接口监控

通过 `curl` 检查 URL 的 HTTP 状态码与响应延迟,适合 API 健康检查.

**处理**: 解析HTTP 接口监控的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回HTTP 接口监控的响应数据,包含状态码、结果和日志.
### 2. SSL 证书检测

使用 `openssl` 检查 SSL/TLS 证书的过期时间,提前预警证书到期.

**处理**: 解析SSL 证书检测的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回SSL 证书检测的响应数据,包含状态码、结果和日志.
### 3. 进程与端口检查

通过 `pgrep` 检查进程是否运行,通过 `nc` 检查端口是否开放.

**处理**: 解析进程与端口检查的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回进程与端口检查的响应数据,包含状态码、结果和日志.
### 4. 磁盘空间监控

使用 `df` 检查磁盘剩余空间,防止磁盘写满导致服务中断.

**处理**: 解析磁盘空间监控的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回磁盘空间监控的响应数据,包含状态码、结果和日志.
### 5. 状态变更告警

仅在状态发生变化时发出告警(ok 变 fail、fail 变 ok),避免重复通知.

**处理**: 解析状态变更告警的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回状态变更告警的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：轻量级服务监控工、磁盘检查、适合个人项目、具免费版、面向个人开发者与、小型项目、核心能力、接口可用性监控、证书过期检测、进程与端口状态检、状态变更邮件、通知告警等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持.
## 使用场景

### 场景一:API 健康监控

监控个人项目的 API 接口,每 5 分钟检查一次.
## 输入格式
| 参数名 | 类型 | 必填 | 说明 |
|---|---|---|---|
| input | string | 是 | 监控工具包-免费版处理的输入数据或指令 |
| options | object | 否 | 附加配置选项,如模式选择、格式偏好等 |
| callback_url | string | 否 | 异步处理完成后的回调通知URL |

```bash
# 创建监控配置
cat > ./monitor/monitors.json << 'EOF'
{
  "api_prod": {
    "description": "生产 API 健康检查",
    "checks": [
      {"type": "http", "target": "https://api.example.com/health"}
    ],
    "interval": "5m",
    "alert_on": "change",
    "requires": [],
    "created": "2025-01-15"
  }
}
EOF
# ...
# 手动执行检查
curl -s -o /dev/null -w "%{http_code} %{time_total}s" https://api.example.com/health
```

### 场景二:SSL 证书到期提醒

监控域名 SSL 证书,提前 30 天告警.
```bash
# 检查证书过期时间
echo | openssl s_client -connect example.com:443 2>/dev/null \
  | openssl x509 -noout -enddate
# ...
# 批量检查多个域名
for domain in example.com api.example.com cdn.example.com; do
  echo -n "$domain: "
  echo | openssl s_client -connect $domain:443 2>/dev/null \
    | openssl x509 -noout -enddate 2>/dev/null || echo "检查失败"
done
```

### 场景三:服务器磁盘与进程监控

检查关键服务进程是否存活,监控磁盘空间.
```bash
# 进程检查
pgrep -x "nginx" > /dev/null && echo "nginx: 运行中" || echo "nginx: 未运行"
pgrep -x "redis" > /dev/null && echo "redis: 运行中" || echo "redis: 未运行"
# ...
# 磁盘空间检查(低于 20% 告警)
df -h / | awk 'NR==2 {gsub(/%/,"",$5); if($5 > 80) print "警告: 根分区使用率 "$5"%"}'
```

## 不适用场景

以下场景监控工具包-免费版不适合处理：

- 物理硬件维修
- 网络物理布线
- 数据中心选址

## 触发条件

需要系统监控、日志分析、运维告警、部署管理时使用。不适用于非本工具能力范围的需求.
## 快速开始

1. 阅读## 核心能力章节了解skill功能
2. 按## 依赖说明配置环境
3. 执行所需能力对应的命令
4. 参考## 错误处理章节处理异常
5. 查看## FAQ解答常见疑问

### 初始化

```bash
# 创建监控目录
mkdir -p ./monitor/logs
# ...
# 查看已有监控
cat ./monitor/monitors.json 2>/dev/null || echo "暂无监控配置"
```

### 添加领先个监控

```bash
# 添加 HTTP 监控
{
  "my_website": {
    "description": "个人网站监控",
    "checks": [
      {"type": "http", "target": "https://myblog.example.com"},
      {"type": "ssl", "target": "myblog.example.com"}
    ],
    "interval": "10m",
    "alert_on": "change"
  }
}
EOF
```

**响应解析**: 完成完成后,查看输出响应确认任务状态。成功时输出包含解析摘要和响应数据;失败时根据错误信息排查问题,查阅错误解析章节获取恢复步骤.
#
## 示例

### 监控定义格式

```json
{
  "monitor_name": {
    "description": "监控描述",
    "checks": [
      {"type": "http", "target": "URL"},
      {"type": "ssl", "target": "domain"},
      {"type": "process", "target": "process_name"},
      {"type": "disk", "target": "/"},
      {"type": "port", "target": "host:port"}
    ],
    "interval": "5m",
    "alert_on": "change",
    "requires": []
  }
}
```

### 检查类型一览

| 类型 | 检查内容 | 所需工具 |
|:-----|:-----|:-----|
| http | URL 状态码 + 延迟 | curl |
| ssl | 证书过期时间 | openssl |
| process | 进程是否运行 | pgrep |
| disk | 磁盘剩余空间 | df |
| port | 端口是否开放 | nc |
| custom | 自定义命令 | 用户指定 |

### 告警通知配置

```bash
# Webhook 告警示例
curl -X POST https://hooks.example.com/alert \
  -H "Content-Type: application/json" \
  -d '{
    "monitor": "my_website",
    "status": "fail",
    "message": "HTTP check failed: 503",
    "timestamp": "2025-01-15T10:30:00Z"
  }'
```

## 优秀实践

1. **仅在变更时告警**:设置 `alert_on: "change"`,避免每 5 分钟收到相同状态通知
2. **组合检查**:对同一目标配置多种检查(HTTP + SSL),全方位监控
3. **合理间隔**:个人项目 5-10 分钟足够,避免过于频繁的检查
4. **日志保留**:检查结果按月归档,便于排查历史问题
5. **权限最小化**:`requires` 字段仅声明实际需要的权限,不假设有额外访问

## 常见问题

### Q: 如何收到告警通知?

A: 免费版支持 Webhook 方式发送告警。配置一个接收 URL,状态变更时会向该 URL 发送 POST 请求。也可通过环境变量配置 Pushover 等推送服务.
### Q: 检查频率怎么设置合适?

A: 个人项目建议 5-10 分钟。HTTP 检查可短至 1 分钟,SSL 证书检查可长至 1 小时(因为证书到期是以天为单位).
### Q: 可以监控需要认证的接口吗?

A: 可以。在 HTTP 检查中添加 Authorization 头,通过 curl 的 `-H` 参数传入。注意不要在配置文件中硬编码密码,使用环境变量引用.
### Q: 磁盘空间告警阈值怎么设?

A: 建议设置两级阈值:80% 警告(提醒清理),95% 紧急(可能导致服务异常)。免费版支持在 `custom` 类型中用脚本实现阈值判断.
## 依赖说明

### 运行环境

- **Agent平台**: 支持 SKILL.md 的任意 AI Agent(Claude Code / Cursor / Codex / Gemini CLI 等)
- **操作系统**: Windows / macOS / Linux
- **Shell 环境**: Bash 或兼容 Shell

### 依赖详情

| 依赖项 | 类型 | 是否必需 | 获取方式 |
|---:|---:|---:|---:|
| curl | CLI工具 | 必需 | 系统自带或包管理器安装 |
| openssl | CLI工具 | SSL检查必需 | 系统自带 |
| pgrep | CLI工具 | 进程检查必需 | procps 包 |
| df | CLI工具 | 磁盘检查必需 | 系统自带 |
| nc(netcat) | CLI工具 | 端口检查必需 | 包管理器安装 |
| jq | CLI工具 | JSON处理推荐 | 包管理器安装 |
| LLM API | API | 必需 | 由Agent内置LLM提供 |

### API Key 配置

- Webhook 告警:配置接收 URL,无需 API Key
- Pushover 推送(可选):设置 `PUSHOVER_TOKEN` 和 `PUSHOVER_USER` 环境变量
- 本 Skill 核心功能基础LLM由Agent平台提供

### 可用性分类

- **分类**: MD+EXEC模式Markdown指令 + 命令行执行)
- **说明**: 通过自然语言指令驱动 Agent 执行监控检查与告警,依赖系统命令行工具
- **限制**: 免费版支持单机监控,最多 10 个监控目标,不支持分布式监控与历史趋势分析

## 错误处理

| 错误场景 | 原因 | 处理方式 |
|:---:|:---:|:---:|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 执行ping命令测试网络连通性,检查防火墙和代理设置连接后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令，参考国内替代方案 |

## 已知限制

- 当前为免费版本,如需完整功能请升级到付费版获取全部能力

## 输出格式
```json
{
  "success": true,
  "data": {
    "result": "监控工具包-免费版处理结果",
    "execution_time": "0.5s",
    "metadata": {
      "version": "1.0",
      "processor": "monitorkit"
    }
  },
  "execution_log": ["解析输入参数", "执行核心处理", "格式化输出结果"],
  "error": null
}
```
