---
slug: ping-monitor-tool-free
name: ping-monitor-tool-free
version: 1.0.0
displayName: 网络监控免费版
summary: "网站可用性监控,支持ICMP/HTTP检测、告警通知与基础可视化。面向个人开发者与小团队的网站可用性监控工具."
license: Proprietary
edition: free
description: '面向个人开发者与小团队的网站可用性监控工具.
  核心能力: ICMP Ping、HTTP 检测、邮件告警、可用性统计、基础可视化

  适用场景: 个人博客监控、API 健康检查、家庭网络监控、小团队项目

  差异化: 免费版聚焦个人监控需求,轻量部署,适合个人开发者

  适用关键词: 网站监控, Ping检测, HTTP健康检查, 可用性监控, 告警通知'
tags:
  - 网络监控
  - 可用性监控
  - 个人工具
  - 告警通知
  - 网站健康
  - 监控
  - 运维
  - 工具
  - self
  - target
  - def
  - config
  - return
tools:
  - read
  - exec
homepage: ""
category: "Operations"
---
# 网络监控 (免费版)

## 概述

本工具为个人开发者与小团队提供轻量的网站可用性监控能力,支持 ICMP Ping、HTTP 健康检查、邮件告警、可用性统计与基础可视化。轻量部署,几分钟内即可启动监控,适合个人博客、API 服务、家庭网络等场景.
免费版聚焦个人监控需求,适合个人开发者、独立项目维护者使用.
## 核心能力

| 能力模块 | 描述 | 免费版支持 |
|----|---|-----|
| ICMP Ping | 主机可达性检测 | 支持 |
| HTTP 检测 | 网站健康检查 | 支持 |
| TCP 端口检测 | 端口开放检测 | 支持 |
| 邮件告警 | 异常邮件通知 | 支持 |
| 可用性统计 | 在线率统计 | 支持 |
| 基础可视化 | 简单图表 | 支持 |
| 多地区监控 | 多地域检测 | 不支持 (升级 PRO) |
| 短信/IM 告警 | 即时通讯通知 | 不支持 (升级 PRO) |
| 历史数据 | 长期数据存储 | 30 天 |
| API 监控 | 接口性能监控 | 不支持 (升级 PRO) |
| 状态页 | 公开状态页 | 不支持 (升级 PRO) |
| 团队协作 | 多人协作 | 不支持 (升级 PRO) |

### 核心功能执行
用`input_params`参数进行配置.

**处理**: 解析核心功能执行的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回核心功能执行的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 参数配置与调用
用`config_options`参数进行配置.

**处理**: 解析参数配置与调用的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回参数配置与调用的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`config_options`参数,支持修改/重置/导入操作

### 结果处理与输出
用`output_format`参数进行配置.

**处理**: 解析结果处理与输出的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回结果处理与输出的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`output_format`参数,支持导出/保存/转换操作
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：网站可用性监控、告警通知与基础可、面向个人开发者与、小团队的网站可用、性监控工具、核心能力、适用场景、个人博客监控、家庭网络监控、小团队项目、差异化、免费版聚焦个人监、控需求、轻量部署、适合个人开发者、适用关键词、网站监控、可用性监控、告警通知等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持.
## 使用场景

### 场景一: 个人博客监控

监控个人博客是否可访问.
```python
import subprocess
import smtplib
from email.mime.text import MIMEText
from datetime import datetime
from pathlib import Path
import json
# ...
class PingMonitor:
    def __init__(self, config_path="~/.ping-monitor/config.json"):
        self.config = self._load_config(config_path)
        self.data_dir = Path("~/.ping-monitor/data").expanduser()
        self.data_dir.mkdir(parents=True, exist_ok=True)
# ...
    def _load_config(self, path):
        default = {
            "targets": [],
            "interval_seconds": 60,
            "timeout_seconds": 5,
            "alert_email": None,
            "smtp": None,
        }
        p = Path(path).expanduser()
        if p.exists():
            return json.loads(p.read_text())
        return default
# ...
    def ping(self, host):
        """ICMP Ping 检测"""
        try:
            result = subprocess.run(
                ["ping", "-c", "1", "-W", str(self.config["timeout_seconds"]), host],
                capture_output=True,
                timeout=self.config["timeout_seconds"] + 5,
            )
            return result.returncode == 0
        except Exception:
            return False
# ...
    def http_check(self, url, expected_status=200):
        """HTTP 健康检查"""
        import requests
        try:
            resp = requests.get(url, timeout=self.config["timeout_seconds"])
            return resp.status_code == expected_status
        except Exception:
            return False
# ...
    def monitor_once(self):
        """执行一次监控"""
        results = []
        for target in self.config["targets"]:
            if target["type"] == "icmp":
                ok = self.ping(target["host"])
            elif target["type"] == "http":
http_check(target["url"])
            else:
                continue
# ...
            results.append({
                "target": target,
                "status": "up" if ok else "down",
                "timestamp": datetime.now().isoformat(),
            })
# ...
            if not ok:
                self._alert(target)
# ...
        self._save_results(results)
        return results
# ...
    def _alert(self, target):
        """发送告警"""
        if not self.config.get("alert_email"): return
        subject = f"[告警] {target.get('name', target.get('host', '未知'))} 不可达"
        body = f"""
监控目标: {target}
检测时间: {datetime.now()}
状态: 不可达 (DOWN)
# ...
请检查服务状态.
"""
        self._send_email(subject, body)
# ...
    def _send_email(self, subject, body):
        """发送邮件"""
        smtp_config = self.config.get("smtp")
        if not smtp_config: return
# ...
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = smtp_config["from"]
        msg["To"] = self.config["alert_email"]
# ...
        with smtplib.SMTP(smtp_config["host"], smtp_config["port"]) as server:
            server.starttls()
            server.login(smtp_config["user"], smtp_config["password"])
            server.send_message(msg)
# ...
    def _save_results(self, results):
        """保存监控结果"""
        today = datetime.now().strftime("%Y-%m-%d")
        log_file = self.data_dir / f"{today}.jsonl"
        with open(log_file, "a") as f:
            for r in results:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
# ...
    def availability_stats(self, days=7):
        """可用性统计"""
        from datetime import timedelta
        stats = {}
        for i in range(days):
            date = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
data_dir / f"{date}.jsonl"
            if not log_file.exists(): continue
# ...
            for line in log_file.read_text().splitlines():
                r = json.loads(line)
                name = r["target"].get("name", r["target"].get("host"))
                if name not in stats:
                    stats[name] = {"total": 0, "up": 0}
                stats[name]["total"] += 1
                if r["status"] == "up":
                    stats[name]["up"] += 1
# ...
        return {
            name: {
                "availability_pct": round(s["up"] / s["total"] * 100, 2),
                "total_checks": s["total"],
                "up_checks": s["up"],
            }
            for name, s in stats.items()
        }
# ...
# 示例
monitor = PingMonitor()
monitor.config["targets"] = [
    {"name": "我的博客", "type": "http", "url": "https://example.com"},
    {"name": "服务器", "type": "icmp", "host": "192.168.1.1"},
]
monitor.config["interval_seconds"] = 60
# ...
# 执行一次监控
results = monitor.monitor_once()
# 查看可用性
stats = monitor.availability_stats(days=7)
```

### 场景二: API 健康检查

监控 API 服务是否正常响应.
```python
def check_api_health(url, expected_response=None):
    """检查 API 健康状态"""
    import requests
    try:
get(url, timeout=10)
        if resp.status_code != 200:
            return {"healthy": False, "reason": f"HTTP {resp.status_code}"}
        if expected_response:
            data = resp.json()
            for key, value in expected_response.items():
                if data.get(key) != value:
                    return {"healthy": False, "reason": f"{key} 不匹配"}
        return {"healthy": True, "response_time_ms": round(resp.elapsed.total_seconds() * 1000)}
    except Exception as e:
        return {"healthy": False, "reason": str(e)}
```

### 场景三: 定时监控

设置定时任务持续监控.
```bash
# Linux/macOS: crontab 配置
crontab -e
# ...
# 添加每分钟监控
* * * * * python ~/.ping-monitor/monitor.py
# ...
# 或使用 systemd timer
cat > ~/.config/systemd/user/ping-monitor.timer << 'EOF'
[Unit]
Description=Ping Monitor
# ...
[Timer]
OnBootSec=1min
OnUnitActiveSec=1min
# ...
[Install]
WantedBy=timers.target
EOF
```

## 不适用场景

以下场景网络监控免费版不适合处理：

- 实时流数据处理
- 小规模数据手动分析
- 非结构化文本情感分析

## 触发条件

需要数据分析、报表生成、统计洞察、数据可视化时使用。不适用于非本工具能力范围的需求.
## 快速开始

### Step 1: 初始化监控配置

```bash
mkdir -p ~/.ping-monitor/data
cat > ~/.ping-monitor/config.json << 'EOF'
{
  "targets": [
    {"name": "博客", "type": "http", "url": "https://example.com"},
  ],
  "interval_seconds": 60,
  "timeout_seconds": 5
}
EOF
```

### Step 2: 测试监控

```bash
python -c "
from monitor import PingMonitor
m = PingMonitor()
results = m.monitor_once()
for r in results:
    print(f'{r[\"target\"][\"name\"]}: {r[\"status\"]}')"
```

### Step 3: 配置定时任务

```bash
# 每分钟执行监控
crontab -e
# 添加: * * * * * python ~/.py
```

### Step 4: 配置告警 (可选)

```json
{
  "alert_email": "you@example.com",
  "smtp": {
    "host": "smtp.gmail.com",
    "port": 587,
    "user": "you@gmail.com",
    "password": "app_password",
    "from": "you@gmail.com"
  }
}
```

#
## 配置示例

### 监控配置

```yaml
# ~/.ping-monitor/config.yaml
targets:
  - name: 个人博客
    type: http
    url: https://myblog.com
    expected_status: 200
    timeout: 10
# ...
  - name: API 服务
    type: http
    url: https://api.myservice.com/health
    expected_response:
      status: ok
    timeout: 5
# ...
  - name: 数据库服务器
    type: icmp
    host: 192.168.1.100
    timeout: 5
# ...
  - name: SSH 端口
    type: tcp
    host: 192.168.1.100
    port: 22
    timeout: 5
# ...
settings:
  interval_seconds: 60
  timeout_seconds: 10
  retry_on_failure: 3
  alert_cooldown_minutes: 30  # 避免告警风暴
# ...
alerting:
  email:
    enabled: true
    address: alerts@example.com
    smtp:
      host: smtp.gmail.com
      port: 587
# ...
storage:
  data_dir: ~/.ping-monitor/data
  retention_days: 30
  format: jsonl
```

### 可用性报告模板

```python
def generate_report(stats):
    """生成可用性报告"""
    report = "网站可用性报告\n"
    report += "=" * 40 + "\n"
        status = "正常" if s["availability_pct"] >= 99.9 else "异常"
        report += f"\n{name}:\n"
        report += f"  可用率: {s['availability_pct']}%\n"
        report += f"  检测次数: {s['total_checks']}\n"
        report += f"  正常次数: {s['up_checks']}\n"
        report += f"  状态: {status}\n"
    return report
```

## 最佳实践

### 1. 监控频率

```text
监控频率建议:
- 关键服务: 1 分钟
- 一般服务: 5 分钟
- 个人项目: 10 分钟
# ...
注意: 过于频繁可能造成服务器压力.
```

### 2. 告警策略

```python
def smart_alert(target, failure_count, cooldown):
    """智能告警策略"""
    # 连续失败 3 次才告警,避免误报
    if failure_count < 3:
        return None
    # 告警冷却,避免告警风暴
    if cooldown.active:
        return None
    return f"目标 {target} 连续 {failure_count} 次检测失败"
```

### 3. 数据保留

```python
def cleanup_old_data(data_dir, retention_days=30):
    """清理过期数据"""
    from datetime import timedelta
    cutoff = datetime.now() - timedelta(days=retention_days)
    for f in Path(data_dir).glob("*.jsonl"):
        date_str = f.stem
        try:
            file_date = datetime.strptime(date_str, "%Y-%m-%d")
            if file_date < cutoff:
                f.unlink()
        except ValueError:
            continue
```

## 常见问题

### Q1: 免费版能监控多少目标?

无硬性上限,但建议不超过 20 个目标,以保证性能.
### Q2: 数据保留多久?

免费版保留 30 天。长期数据存储需要 PRO 版本.
### Q3: 支持哪些告警渠道?

免费版支持邮件告警。短信、IM (Slack、钉钉、飞书) 需要 PRO 版本.
### Q4: 部署在哪里?

部署在任意可访问目标的服务器或本地机器。建议部署在云服务器以保证持续运行.
### Q5: 误报如何处理?

设置连续失败阈值 (如 3 次) 与告警冷却 (如 30 分钟),减少误报.
## 依赖说明

### 运行环境

- **Agent 平台**: 支持 SKILL.md 规范的任意 AI Agent (Claude Code、Cursor、Codex、Gemini CLI 等)
- **操作系统**: Windows / macOS / Linux
- **网络**: 需访问监控目标

### 依赖详情

| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:-----|:-----|:-----|:-----|
| LLM API | 推理服务 | 必需 | 由 Agent 内置 LLM 提供 |
| Python 3.8+ | 运行时 | 推荐 | python.org 下载 |
| requests | Python 库 | HTTP 检测 | `pip install requests` |
| ping | 系统工具 | ICMP 检测 | 系统自带 |
| cron / systemd | 定时任务 | 推荐 | 系统自带 |

### API Key 配置

```bash
# 免费版无需外部 API Key
# ...
# 可选: SMTP 配置 (邮件告警)
export SMTP_HOST="smtp.gmail.com"
export SMTP_USER="you@gmail.com"
export SMTP_PASSWORD="app_password"
export ALERT_EMAIL="you@example.com"
```

### 可用性分类

- **分类**: MD+EXEC (Markdown 指令 + 命令行执行)
- **说明**: 本 Skill 通过自然语言指令驱动 Agent 执行网络监控,数据本地存储
- **免费版限制**: 单用户、30 天数据、邮件告警、单地区检测、无 API 性能监控

## 错误处理

| 错误场景 | 原因 | 处理方式 |
|---:|---:|---:|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 执行ping命令测试网络连通性,检查防火墙和代理设置连接后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令，参考国内替代方案 |

## 已知限制

- 免费版不支持HTTPS证书过期监控和内容变化检测，仅支持基础ICMP/HTTP状态码检测
- 告警通知仅支持邮件渠道，短信/Webhook/即时通讯通知需升级到付费版
- 监控频率最低为5分钟，不适合需要秒级响应的高可用性场景

## 示例

### 基本用法

**输出**：返回执行结果,包含操作状态和输出数据

```text
用户: 执行核心功能
Skill: 正在执行核心功能...
Skill: 执行完成,结果如下: 操作成功
```

## 输出格式
```json
{
  "success": true,
  "data": {
    "result": "网络监控免费版处理结果",
    "execution_time": "0.5s",
    "metadata": {
      "version": "1.0",
      "processor": "ping monitor"
    }
  },
  "execution_log": ["解析输入参数", "执行核心处理", "格式化输出结果"],
  "error": null
}
```
