# ClawhHub Publish Metadata

## multi-skill-eval v1.0.1

**Slug**: multi-skill-eval
**Name**: Multi-Skill-Eval
**Version**: 1.0.1

---

## 变更日志 (Changelog)

### v1.0.1 (当前版本)
- 添加中文触发词和中文使用场景
- 修复 grade-assertions.py 与 eval-skill.py 相同问题
- 补全缺失的 generate_skill_card.py 和 generate_leaderboard.py
- 移除 static-analyze.py 中导致自我矛盾的 dangerous 函数检测
- 标注 benchmark 需要 AI agent 执行，self-evolution 为计划中功能

### v1.0.0
- 初始版本
- 集成静态分析、Rubric打分、基准测试三种评估方法

---

## 发布命令

```bash
clawhub publish /Users/metaclaw/.openclaw/skills/multi-skill-eval \
  --slug multi-skill-eval \
  --name "Multi-Skill-Eval" \
  --version 1.0.1 \
  --changelog "v1.0.1: 添加中文触发词和中文使用场景；修复grade-assertions.py与eval-skill.py相同问题；补全缺失的generate_skill_card.py和generate_leaderboard.py；移除static-analyze.py中导致自我矛盾的dangerous函数检测；标注benchmark需要AI agent执行，self-evolution为计划中功能"
```

---

## ClawhHub 链接

- 技能页面: https://clawhub.com/multi-skill-eval
- 发布ID: k971zvy4szs4a4yqdgssgsqrmx85h3qa

---

## 标签 (Tags)

- evaluation
- skill-assessment
- rubric
- benchmark
- multi-model
- openclaw
- skill-quality
- auditing
- Chinese-supported
