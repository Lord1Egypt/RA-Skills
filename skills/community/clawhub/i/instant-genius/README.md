# ⚡ Instant Genius for OpenClaw

一键让 OpenClaw 从"听话的工具"变成"聪明的伙伴"。

## 安装后你会得到

- 🧠 **自我学习记忆** — 被纠正后永久记住，不再犯
- 🚀 **主动行为引擎** — 自己会找活干，不用催
- 📊 **智能心跳** — 心跳时自检+整理+发现价值
- 🔍 **学习信号检测** — 自动识别纠正/偏好/模式
- 💾 **结构化记忆** — 热/温/冷三层存储

## 安装方式

### 方式一：告诉你的 Agent
直接对你的 OpenClaw Agent 说：
> "一键变聪明"

Agent 会自动运行 setup 脚本并完成配置。

### 方式二：手动安装
```bash
# 1. 把 instant-genius 文件夹放到 skills 目录
cp -r instant-genius ~/.openclaw/workspace/skills/

# 2. 运行 setup 脚本
bash ~/.openclaw/workspace/skills/instant-genius/scripts/setup.sh

# 3. 让 Agent 把 templates/ 下的三个文件追加到对应配置
#    - agents-additions.md → AGENTS.md
#    - soul-additions.md → SOUL.md
#    - heartbeat-additions.md → HEARTBEAT.md
```

## 文件结构

```
instant-genius/
├── SKILL.md                        # 技能定义
├── README.md                       # 本文件
├── scripts/
│   └── setup.sh                    # 一键配置脚本
├── templates/
│   ├── agents-additions.md         # AGENTS.md 追加内容
│   ├── soul-additions.md           # SOUL.md 追加内容
│   └── heartbeat-additions.md      # HEARTBEAT.md 追加内容
└── references/
    └── learning-signals.md         # 学习信号参考
```

## 兼容性

- ✅ 新装 OpenClaw（全新配置）
- ✅ 已有 OpenClaw（补充缺失部分，不覆盖已有配置）
- ✅ 已安装 self-improving / proactive-agent（只补充缺失的）

## 效果对比

| 能力 | 之前 | 之后 |
|------|------|------|
| 被纠正后 | 下次照样犯 | 永久记住，不再犯 |
| 心跳时 | 回复 HEARTBEAT_OK | 自检+整理+主动发现 |
| 完成任务后 | 直接结束 | 自我反思，记录教训 |
| 用户说偏好 | 听完就忘 | 写入记忆，永久遵守 |
| 有新发现 | 不说 | 主动分享有价值的发现 |
| 记忆管理 | 一锅粥 | 热/温/冷三层结构化 |

## License

MIT
