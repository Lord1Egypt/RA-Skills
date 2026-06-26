---
name: zhixing-loop
description: 基于《实践论》的自我迭代系统。当需要自动整理记忆、反思改进、或创建新技能时使用。包含Heartbeat检查清单、Cron定时任务配置、和技能创建工作流。
---

# 知行迭代 (Knowledge-Action Loop)

基于毛泽东《实践论》的辩证唯物主义自我改进方法。

## 核心哲学

> "实践、认识、再实践、再认识，循环往复以至无穷"

**三层迭代:**
1. **感性认识** → 收集事实、现象
2. **理性认识** → 分析本质、规律  
3. **回到实践** → 用行动验证

## 快速启动

### 1. 配置 Heartbeat

创建 `HEARTBEAT.md`:

```markdown
# 知行检查清单

## 记忆维护
- [ ] 检查今日对话，提取关键事实
- [ ] 更新 memory/YYYY-MM-DD.md
- [ ] 标记重要内容到 MEMORY.md

## 方法反思
- [ ] 这次对话哪里可以更好？
- [ ] 用户偏好是否有变化？
- [ ] 工具使用是否高效？

## 下一步
- [ ] 确定改进点
- [ ] 安排 Cron 任务（如需要）
```

### 2. 配置 Cron 任务

```bash
# 每日记忆整理
openclaw cron add \
  --name "每日记忆整理" \
  --cron "0 23 * * *" \
  --session isolated \
  --message "回顾今日对话，整理记忆，提取改进点" \
  --announce

# 每周技能更新检查
openclaw cron add \
  --name "技能更新检查" \
  --cron "0 9 * * 1" \
  --session isolated \
  --message "检查技能更新: clawdhub update --all" \
  --announce
```

### 3. 创建新技能（按需）

当重复需求出现3次以上:

```bash
# 初始化技能
scripts/init_skill.py my-skill --path skills/ --resources scripts

# 开发技能...

# 打包
scripts/package_skill.py skills/my-skill

# 安装
clawdhub install ./my-skill.skill
```

## 工作流详情

### Heartbeat 工作流 (每30分钟)

**触发条件:** 时间触发
**执行内容:**
1. 读取 HEARTBEAT.md
2. 执行检查清单
3. 如有重要发现，通知用户
4. 否则回复 HEARTBEAT_OK

### Cron 工作流 (每日/每周)

**触发条件:** 定时触发
**执行内容:**
1. 独立会话运行
2. 深度分析记忆文件
3. 整合知识到长期记忆
4. 生成改进报告

### 技能创建工作流 (按需)

**触发条件:** 模式识别 (重复需求≥3次)
**执行内容:**
1. 分析需求模式
2. 设计技能结构
3. 编写脚本和文档
4. 测试和打包
5. 安装使用

## 文件结构

```
workspace/
├── HEARTBEAT.md              # 检查清单
├── MEMORY.md                 # 长期记忆
├── memory/
│   └── YYYY-MM-DD.md         # 每日日志
├── skills/
│   └── zhixing-loop/         # 本技能
│       ├── SKILL.md
│       └── README.md
└── .openclaw/
    └── cron/
        └── jobs.json         # Cron 配置
```

## 最佳实践

### 1. 记忆管理
- **Daily notes**: 原始记录，不过滤
- **MEMORY.md**: 精华提取，结构化
- **定期整理**: 每天23:00自动运行

### 2. 反思原则
- **具体**: 不空谈，指出现象
- **建设性**: 每个问题都要有改进方案
- **可验证**: 改进后要有验证方法

### 3. 技能创建
- **小而美**: 一个技能解决一类问题
- **可复用**: 考虑多次使用场景
- **文档齐全**: SKILL.md 要写清楚用法

## 参考

- 《实践论》- 毛泽东
- 《矛盾论》- 毛泽东
- OpenClaw 文档: https://docs.openclaw.ai

---

*知行合一 — 理论与实践的统一*
