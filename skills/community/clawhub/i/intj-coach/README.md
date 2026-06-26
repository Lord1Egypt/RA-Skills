# INTJ Coach Skill 套件

**INTJ 成长伙伴 — 双模式教练系统**

---

## 📁 目录结构

```
intj-coach/
├── SKILL.md                      # 主技能文档（含记录机制）
├── README.md                     # 本文件
├── references/                   # 参考资料
│   ├── intj-insights.md          # INTJ 专属洞察
│   ├── question-bank.md          # 问题库
│   └── advisor-templates.md      # 顾问模式建议模板
├── examples/                     # 对话示例
│   ├── coach-mode.md             # 教练模式完整示例
│   └── advisor-mode.md           # 顾问模式完整示例
└── scripts/                      # 工具脚本
    └── init-user-profile.py      # 用户档案初始化
```

---

## 🎯 核心功能

### 1. 双模式对话
- **教练模式**（默认）：提问帮用户自己想清楚
- **顾问模式**（补充）：给具体建议和方案

### 2. Per-User 档案系统
- 每个用户独立档案
- 自动加载历史
- 自动保存对话
- 主动追踪行动

### 3. 心跳追踪
- 每周检查未完成行动
- 主动发消息提醒
- 每月生成复盘报告

---

## 🚀 快速开始

### 触发方式
```
- "我是 INTJ，最近有点迷茫"
- "INTJ 成长"
- "给我建议"
- "/intj-coach"
```

### 首次使用
自动创建用户档案：
```
~/.openclaw/workspace/memory/intj-users/
├── {user_id}-profile.md
├── {user_id}-sessions.md
└── {user_id}-actions.md
```

### 手动初始化（可选）
```bash
python3 scripts/init-user-profile.py <user_id> [user_name]
```

---

## 📋 使用指南

### 教练模式流程
1. 加载用户档案
2. 检查未完成行动 → 先问进展
3. 开场："今天想聊点啥？"
4. 倾听 → 提问 → 觉察 → 行动
5. 保存对话记录

### 顾问模式流程
1. 加载用户档案
2. 确认问题
3. 给 2-3 个方案
4. 说优劣 + 给第一步
5. 保存对话记录

### 心跳追踪流程
1. 扫描所有用户档案
2. 找出超过 7 天未完成的行动
3. 主动发消息提醒
4. 记录提醒历史

---

## 🔧 配置说明

### 档案位置
```bash
~/.openclaw/workspace/memory/intj-users/
```

### 文件格式
- **profile.md**: 用户基本信息 + 目标 + 历史决策
- **sessions.md**: 每次对话记录
- **actions.md**: 行动追踪（进行中/已完成/已放弃）

### 心跳配置
添加到 `HEARTBEAT.md`：
```markdown
## INTJ Coach 追踪（每周一 10:00）
- [ ] 扫描 intj-users/ 下所有 actions.md
- [ ] 找出超过 7 天未完成的行动
- [ ] 主动发消息提醒
```

---

## 📊 效果评估

### 成功指标
- 用户完成行动数 / 总行动数 > 50%
- 用户月度留存率 > 70%
- 用户满意度评分 > 4/5

### 失败信号
- 用户连续 3 次对话无行动
- 用户放弃行动数 > 完成行动数
- 用户明确表示"没用"

### 改进流程
1. 每次对话后记录：哪里卡住了？
2. 每周复盘：哪个问题最有效？
3. 每月更新：补充新模板和示例

---

## 🔗 相关资源

### 内部文档
- `references/intj-insights.md` - INTJ 专属洞察
- `references/question-bank.md` - 完整问题库
- `references/advisor-templates.md` - 建议模板
- `examples/coach-mode.md` - 教练模式示例
- `examples/advisor-mode.md` - 顾问模式示例

### 外部资源
- 《MBTI 进阶指南》
- 《越过山丘》- 教练哲学
- 《原则》- 系统思考
- 《卓有成效的管理者》- 时间管理

---

## 📈 版本历史

| 版本 | 日期 | 更新内容 |
|------|------|---------|
| v2.0.0 | 2026-04-16 | 新增 per-user 档案系统 + 心跳追踪 |
| v1.0.0 | 2026-04-15 | 初始版本（双模式设计） |

---

## 🎯 Skill 类型

**归类**：业务流程与团队自动化（通用技能 🟡）

**说明**：将 INTJ 成长对话流程自动化，包含教练模式和顾问模式两种路径，内建 per-user 档案系统。

---

*本技能持续改进，基于实际咨询案例更新模板和示例。*
