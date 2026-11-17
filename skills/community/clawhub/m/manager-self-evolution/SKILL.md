# Self-Evolution Skill - 自我进化技能

## 功能定位

使Manager具备自我诊断、自我改进的机制，不依赖外部提醒持续优化。

**v1.1.0 更新（2026-07-12）**:
- 集成 OpenClaw secrets audit 检查
- 增强心跳期自我诊断（识别误报 pattern）
- 新增 agent health score 输出
- 集成 MEMORY.md 教训匹配（最近 30 天）
- 三层走（必看 / 必查 / 必引）任务前自检

## 核心功能

### 1. 自我诊断 (self-diagnose)
- 检查最近对话记录，识别理解错误模式
- 检查 MEMORY.md 中的教训是否被遵守
- 检查 SOUL.md 原则是否在行为中体现
- **v1.1.0**: 匹配最近 30 天失败经验，标记潜在风险

### 2. 缺陷发现 (defect-discovery)
- 在 heartbeat 时主动扫描最近对话
- 发现问题立即记录到 evolution-log.md
- 不等用户提醒
- **v1.1.0**: 反误报硬规则（识别 `ls | head -N` 截断类推断为"缺"，必须 `find` disprove）

### 3. 改进追踪 (improvement-tracking)
- 记录每次自我发现的问题
- 追踪改进是否落实
- 评估改进效果

### 4. 技能健康 (skill-health)
- 定期检查 skill 文件完整性
- 检查 skill 中的承诺是否兑现
- 确保 skill 不成为空壳

### 5. v1.1.0 安全审计 (secrets-audit)
- 集成 OpenClaw secrets audit（只读，不直接调用）
- 检查 5 个应清 env var 是否真正清空
- 检查 plaintext / unresolved / shadowed / legacy 标记
- 失败立即报告并写入 evolution-log.md

### 6. v1.1.0 三层走验证 (three-layer-check)
- 任何任务前必走 #84 三层走：必看 / 必查 / 必引
- 必看 MEMORY.md 失败经验段（最近 30 天）
- 必查 memory_search 关键词（即使 0 hits 也要 rg FTS 兜底）
- 必引带路径引用给主人

### 7. v1.1.0 健康评分 (health-score)
- 输出 0-100 agent health score
- 维度：诊断覆盖率 / 教训匹配度 / 误报率 / secrets audit 状态 / skill 健康度
- 每次 heartbeat 自动输出

## 触发机制

| 触发条件 | 执行内容 |
|----------|----------|
| 每次 heartbeat | 运行自我诊断 + 健康评分 |
| 任何任务前 | #84 三层走验证 |
| 发现重大失误后 | 立即记录并提醒 |
| 每周五 | 汇总进化日志 |
| v1.1.0 每日 | secrets audit + 健康评分 |

## 文件结构

```
self-evolution/
├── SKILL.md              # 本文件
├── self-check.py         # 自我检查脚本
└── evolution-log.md      # 进化日志（自动创建）
```

## 注意事项

- **只读优先**：尽可能减少写入
- **不影响现有系统**：不修改 MEMORY.md/SOUL.md/AGENTS.md
- **用户确认**：重大改进需用户确认才执行
- **透明记录**：所有自我发现都记录在 evolution-log
- **v1.1.0 集成**：不直接调 secrets audit 命令，只读审计报告

## 使用方式

```bash
# 手动运行自我检查
python3 skills/self-evolution/self-check.py diagnose

# 健康评分（v1.1.0）
python3 skills/self-evolution/self-check.py health-score

# 查看进化日志
cat memory/evolution-log.md
```

## v1.1.0 变更日志

### 新增
- 安全审计集成（secrets-audit）
- 三层走验证（three-layer-check）
- 健康评分输出（health-score）
- 反误报硬规则（disprove pattern detection）

### 改进
- 自我诊断精度（匹配最近 30 天 MEMORY.md 教训）
- 缺陷发现智能化（识别 `ls | head -N` 类截断误报）
- 触发机制增加每日 secrets audit

### 兼容性
- 完全向后兼容 v1.0.0
- 现有 self-check.py 接口不变
- evolution-log.md 格式向后兼容

## License

MIT-0