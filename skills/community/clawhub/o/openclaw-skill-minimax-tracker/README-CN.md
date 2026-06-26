# openclaw-skill-minimax-tracker

<p align="center">
  <img src="https://raw.githubusercontent.com/QiaoTuCodes/openclaw-skill-whisper-stt/main/assets/openclaw-skill-logo.png" alt="MiniMax Tracker" width="500" style="visibility: visible; max-width: 100%;">
</p>

<p align="center">
  <strong>📊 MiniMax API 用量追踪技能 for OpenClaw</strong>
</p>

<p align="center">
  <a href="https://github.com/QiaoTuCodes/openclaw-skill-minimax-tracker/releases"><img src="https://img.shields.io/github/v/release/QiaoTuCodes/openclaw-skill-minimax-tracker?include_prereleases&style=for-the-badge" alt="GitHub release"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge" alt="MIT License"></a>
</p>

> 实时追踪和监控 MiniMax API 用量，带有进度条显示和自动提醒功能，专为 OpenClaw agents 设计。

## ✨ 功能特性

- 📊 **实时用量追踪** - 实时追踪 prompts 使用情况
- 📈 **进度条显示** - 可视化进度条 + 关键指标
- ⏰ **自动重置计算** - 基于 MiniMax 规则计算重置时间
- 🔔 **定时提醒** - Cron 定时用量检查提醒
- 💾 **持久化存储** - JSON 用量历史记录
- 🔄 **Agent 集成** - 轻松集成到 OpenClaw agents

## 📦 安装

```bash
# 克隆到你的 OpenClaw 工作区
cd ~/openclaw-workspace/skills
git clone https://github.com/QiaoTuCodes/openclaw-skill-minimax-tracker.git

# 或手动复制
cp -r openclaw-skill-minimax-tracker ~/openclaw-workspace/skills/
```

## 🚀 快速开始

```bash
# 查看当前状态
python3 openclaw-skill-minimax-tracker/minimax_tracker.py status

# 记录用量（每次 API 调用后）
python3 openclaw-skill-minimax-tracker/minimax_tracker.py add

# 查看简洁进度条
python3 openclaw-skill-minimax-tracker/minimax_tracker.py compact
```

## 📊 进度条格式

```
[████████████████████] 98% RST:18:00 TTL:1h40m PKG:Starter USE:2/40 REM:38 NXT:19:19
```

**图例：**
| 缩写 | 含义 |
|------|------|
| RST | 重置时间 |
| TTL | 距重置时间 |
| PKG | 套餐名称 |
| USE | 已用 prompts |
| REM | 剩余 prompts |
| NXT | 下次提醒时间 |

## ⚙️ 配置

修改 `minimax_tracker.py` 中的配置：

```python
CONFIG = {
    "max_prompts": 40,           # 每月最大 prompts 数
    "reset_hour_start": 15,      # 重置窗口开始 (15:00 UTC+8)
    "reset_hour_end": 20,        # 重置窗口结束 (20:00 UTC+8)
    "check_interval_hours": 3,  # 提醒间隔
}
```

## 🤖 OpenClaw 集成

### Agent 代码集成

```python
import subprocess

# API 调用后追踪用量
result = subprocess.run(
    ["python3", "~/openclaw-workspace/skills/openclaw-skill-minimax-tracker/minimax_tracker.py", "add", "1"],
    capture_output=True, text=True
)
print(result.stdout)
```

### Cron 设置（每3小时）

```json
{
  "name": "minimax-usage-check",
  "schedule": "0 */3 * * *",
  "payload": {
    "kind": "agentTurn",
    "message": "Run: python3 ~/openclaw-workspace/skills/openclaw-skill-minimax-tracker/minimax_tracker.py compact"
  }
}
```

## 📖 文档

- [English README](README.md)
- [中文文档](README-CN.md)
- [技能定义](SKILL.md)

## 🔨 环境要求

- Python 3.8+
- 无需外部依赖（纯标准库）

## 📂 项目结构

```
openclaw-skill-minimax-tracker/
├── SKILL.md                    # OpenClaw 技能定义
├── minimax_tracker.py          # Python 主脚本
├── README.md                   # 英文文档
├── README-CN.md               # 中文文档
├── LICENSE                    # MIT 许可证
├── .gitignore                 # Git 忽略规则
└── assets/                    # 图标和资源
    └── icon.png
```

## 🤝 贡献

欢迎提交 Pull Request！

## 📜 许可证

MIT License - 详见 [LICENSE](LICENSE)

## 👥 作者

- **魏然 (Weiran)** - [GitHub](https://github.com/QiaoTuCodes)
- **焱焱 (Yanyan)** - AI 助手

## 🔗 相关链接

- [OpenClaw 文档](https://docs.openclaw.ai)
- [技能市场](https://clawhub.com)
- [MiniMax 平台](https://platform.minimaxi.com)

---

<p align="center">
  <sub>用 ❤️ 为 OpenClaw 社区打造</sub>
</p>
