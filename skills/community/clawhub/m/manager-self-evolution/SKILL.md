# Self-Evolution Skill - 自我进化技能

## 功能定位

使Manager具备自我诊断、自我改进的机制，不依赖外部提醒持续优化。

## 核心功能

### 1. 自我诊断 (self-diagnose)
- 检查最近对话记录，识别理解错误模式
- 检查MEMORY.md中的教训是否被遵守
- 检查SOUL.md原则是否在行为中体现

### 2. 缺陷发现 (defect-discovery)
- 在heartbeat时主动扫描最近对话
- 发现问题立即记录到evolution-log.md
- 不等用户提醒

### 3. 改进追踪 (improvement-tracking)
- 记录每次自我发现的问题
- 追踪改进是否落实
- 评估改进效果

### 4. 技能健康 (skill-health)
- 定期检查skill文件完整性
- 检查skill中的承诺是否兑现
- 确保skill不成为空壳

## 触发机制

| 触发条件 | 执行内容 |
|----------|----------|
| 每次heartbeat | 运行自我诊断 |
| 发现重大失误后 | 立即记录并提醒 |
| 每周五 | 汇总进化日志 |

## 文件结构

```
self-evolution/
├── SKILL.md           # 本文件
├── self-check.py      # 自我检查脚本
└── evolution-log.md   # 进化日志（自动创建）
```

## 注意事项

- **只读优先**：尽可能减少写入
- **不影响现有系统**：不修改MEMORY.md/SOUL.md/AGENTS.md
- **用户确认**：重大改进需用户确认才执行
- **透明记录**：所有自我发现都记录在evolution-log

## 使用方式

```bash
# 手动运行自我检查
python3 skills/self-evolution/self-check.py diagnose

# 查看进化日志
cat memory/evolution-log.md
```
