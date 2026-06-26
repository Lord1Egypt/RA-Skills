# Cron 脚本设计规范

> ⚠️ **强制约束**：每次开发新 cron 脚本前，必须先读取本文件。

---

## 核心设计原则

**定时脚本必须完全自动化，不依赖人工介入。**

```
launchd 定时触发
    ↓
Python 脚本直接执行：
  1. 加载 master_task.json（goal_web + core_goal）
  2. 采集数据（API / web_fetch 等）
  3. 生成分析报告
  4. 通过 openclaw message send 把结果发给用户
    ↓
用户收到完整报告，无需任何回复
```

**严禁以下模式（已废弃）：**
```
❌ cron → 发触发消息 → 等用户回复 → AI 才执行
```
这个模式依赖人工介入，不是定时自动化。

---

## 1. 架构分层

| 层 | 职责 | 文件 |
|---|------|------|
| **调度层** | 定时触发，仅负责启动 Python 脚本 | launchd plist |
| **编排层** | 加载上下文、调用各功能模块、汇总结果、发送报告 | `scripts/auto_{平台名}.py` |
| **数据层** | 采集原始数据（API/抓取） | `scripts/fetch_{平台名}_data.py`（可选独立） |
| **输出层** | 格式化报告 + openclaw message send 发送给用户 | 编排层内调用 |

---

## 2. 编排脚本规范（`auto_{平台名}.py`）

### 2.1 标准结构

```python
#!/usr/bin/env python3
"""
auto_{platform}.py — {平台名} 全自动数据采集 + 报告生成 + 发送

职责：
  1. 加载 tasks/master_task.json（或直接使用硬编码参数）
  2. 采集数据（调用 API / subprocess web_fetch 等）
  3. 分析数据，生成 Markdown 报告
  4. 写入 run/{date}/{batch_seq}/report.md
  5. 调用 openclaw --profile <OPENCLAW_PROFILE> message send 把报告发给用户
  6. 更新 tasks/{goal_web}_tasks_{batch_seq}.json（task_state = done）
"""

import subprocess, json, os
from datetime import datetime
from pathlib import Path

SKILL_ROOT = Path(__file__).parent.parent
OPENCLAW_BIN = "<OPENCLAW_BIN_PATH>"
MESSAGE_TARGET = "<MESSAGE_TARGET>"
OPENCLAW_PROFILE = "<OPENCLAW_PROFILE>"

def send_feishu(message: str):
    """发送飞书消息给用户"""
    result = subprocess.run([
        OPENCLAW_BIN, "--profile", OPENCLAW_PROFILE,
        "message", "send",
        "--channel", "feishu",
        "--target", MESSAGE_TARGET,
        "--message", message
    ], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"[warn] Feishu 发送失败: {result.stderr}")
    else:
        print(f"[ok] Feishu 发送成功")

def fetch_data() -> list:
    """采集数据，返回结构化列表"""
    # 实现数据采集逻辑
    pass

def generate_report(data: list) -> str:
    """生成 Markdown 报告"""
    # 实现报告生成逻辑
    pass

def main():
    date_str = datetime.now().strftime("%Y-%m-%d")
    print(f"[{datetime.now()}] 开始执行 {平台名} 自动任务")

    # 1. 采集数据
    data = fetch_data()

    # 2. 生成报告
    report = generate_report(data)

    # 3. 写入文件
    run_dir = SKILL_ROOT / "run" / date_str / "auto"
    run_dir.mkdir(parents=True, exist_ok=True)
    report_path = run_dir / f"{平台名}_report_{date_str}.md"
    report_path.write_text(report, encoding="utf-8")
    print(f"[ok] 报告已写入: {report_path}")

    # 4. 发送给用户
    send_feishu(report)

if __name__ == "__main__":
    main()
```

### 2.2 数据采集方式

由于 Python `urllib` 直接请求部分外部 API 会被 403 拦截，采集方式按优先级：

| 优先级 | 方式 | 适用场景 |
|--------|------|---------|
| 1 | `subprocess` 调用 `curl -A "Mozilla/5.0 ..."` | **Reddit 等有 UA 检测的 API（✅ 已验证）** |
| 2 | 直接 `urllib/requests`（无需特殊 UA） | 简单开放 API |

> ⚠️ `urllib.request` 直接请求 Reddit 会返回 `403 Blocked`，**必须用 curl**。

Reddit 采集示例：
```python
import urllib.request, json

def fetch_reddit(query: str, limit=5) -> list:
    url = f"https://www.reddit.com/search.json?q={query}&sort=hot&limit={limit}&t=week"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (compatible; ReportBot/1.0)"})
    with urllib.request.urlopen(req, timeout=10) as r:
        data = json.load(r)
    return [
        {
            "title": p["data"]["title"],
            "score": p["data"]["score"],
            "subreddit": p["data"]["subreddit"],
            "num_comments": p["data"]["num_comments"],
            "url": f"https://reddit.com{p['data']['permalink']}",
            "selftext": p["data"].get("selftext", "")[:200]
        }
        for p in data["data"]["children"]
        if p["data"].get("score", 0) > 0
    ]
```

---

## 3. 定时注册规范（macOS launchd）

### 3.1 Plist 命名与位置
```
~/Library/LaunchAgents/<LAUNCH_AGENT_NAME>.plist
```

### 3.2 Plist 标准模板

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
  <dict>
    <key>Label</key>
    <string><LAUNCH_AGENT_NAME></string>

    <key>ProgramArguments</key>
    <array>
      <string>/usr/bin/python3</string>
      <string><PYTHON_SCRIPT_PATH></string>
    </array>

    <key>WorkingDirectory</key>
    <string><WORKING_DIRECTORY></string>

    <key>StartCalendarInterval</key>
    <dict>
      <key>Hour</key>
      <integer>9</integer>
      <key>Minute</key>
      <integer>0</integer>
    </dict>

    <key>RunAtLoad</key>
    <false/>

    <key>StandardOutPath</key>
    <string><STDOUT_LOG_PATH></string>

    <key>StandardErrorPath</key>
    <string><STDERR_LOG_PATH></string>

    <key>EnvironmentVariables</key>
    <dict>
      <key>PATH</key>
      <string><PATH_ENV></string>
      <key>HOME</key>
      <string><HOME_DIR></string>
      <key>PYTHONUNBUFFERED</key>
      <string>1</string>
    </dict>

    <key>ProcessType</key>
    <string>Background</string>
  </dict>
</plist>
```

**直接运行 Python**，不经过 bash 包装层，更简洁稳定。

### 3.3 注册 / 卸载 / 验证
```bash
launchctl load ~/Library/LaunchAgents/<LAUNCH_AGENT_NAME>.plist
launchctl list | grep <LAUNCH_AGENT_NAME>
launchctl start <LAUNCH_AGENT_NAME>   # 手动触发
launchctl unload ~/Library/LaunchAgents/<LAUNCH_AGENT_NAME>.plist
```

---

## 4. 测试规范

### 4.1 开发完成后先直接运行 Python 脚本
```bash
python3 scripts/auto_{平台名}.py
```
检查：
- [ ] 数据采集是否成功（无报错）
- [ ] 报告是否生成到 `run/{date}/auto/`
- [ ] Feishu 是否收到完整报告（不是触发消息，是真正的报告内容）
- [ ] 报告内容是否完整（数据 + 分析 + 洞察）

### 4.2 launchd 触发测试
```bash
launchctl start <LAUNCH_AGENT_NAME>
sleep 15
tail -20 logs/{任务名}.out.log
```

---

## 5. 禁止事项

| 禁止 | 原因 |
|------|------|
| cron 脚本发触发消息、等待用户回复 | 不是自动化，破坏定时任务的完整性 |
| 在 Python 里直接用 `urllib` 访问有 UA 拦截的 API | 会被 403，加 User-Agent header 或用 curl |
| `--target "user:<ID>"` 这类包装格式 | 某些消息通道下可能无法识别，优先使用系统要求的原始目标标识 |
| 不显式指定 profile | 多实例环境下可能读错消息通道配置 |
| 使用相对路径 | launchd 工作目录不确定 |

---

## 6. 已有脚本清单

| 脚本 | Plist | 平台 | 触发时间 | 模式 | 状态 |
|------|-------|------|---------|------|------|
| `auto_{platform}.py` | `<LAUNCH_AGENT_NAME>.plist` | `{平台名}` | `{计划时间}` | 全自动或消息触发 | 由接入平台时填写 |
| `cron_{platform}.sh` | — | `{平台名}` | `{计划时间}` | 已废弃示例 | 仅历史兼容说明，不推荐使用 |

---

## 7. 开发新自动脚本的完整流程

```
1. 读取本文件（必须）
2. 新建 scripts/auto_{平台名}.py，按第 2 节标准结构实现
3. 实现 fetch_data() 和 generate_report() 两个核心函数
4. 直接运行测试：python3 scripts/auto_{平台名}.py
5. 验证 Feishu 收到完整报告（非触发消息）
6. 创建 plist，直接调用 python3 脚本（非 bash 包装）
7. launchctl load + launchctl start 验证
8. 更新本文件「已有脚本清单」
9. 在 script_registry.json 中注册（target_web = 对应平台）
```
