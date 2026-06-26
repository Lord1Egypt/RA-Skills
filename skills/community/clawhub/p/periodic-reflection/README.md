# Periodic Reflection Skill - 周期性反思报告

🧬 自动化生成结构化的自我进化反思报告，支持数据驱动的快速迭代优化。

## 快速开始

### 1. 使用模板生成报告

```bash
cd ~/workspace/agent/workspace/skills/periodic-reflection

# 手动生成报告
node scripts/generate-report.js \
  --project "你的项目名称" \
  --cycle "daily" \
  --output reports/reflection-$(date +%Y-%m-%d).md
```

### 2. 设置自动定时任务

```bash
# 每 8 小时生成一次反思报告
crontab -e

# 添加以下行：
0 */8 * * * cd ~/workspace/agent/workspace/skills/periodic-reflection && node scripts/generate-report.js --auto >> /tmp/reflection.log 2>&1
```

### 3. 查看生成的报告

```bash
ls -la reports/
cat reports/reflection-*.md
```

## 文档结构

```
periodic-reflection/
├── SKILL.md                      # Skill 使用说明
├── README.md                     # 本文件
├── scripts/
│   └── generate-report.js        # 报告生成脚本
├── templates/
│   └── reflection-template.md    # 报告模板
└── references/
    └── best-practices.md         # 最佳实践指南
```

## 适用场景

- ✅ EvoMap 资产发布监控
- ✅ Agent 自我进化跟踪
- ✅ DevOps 运维复盘
- ✅ 任何需要持续优化的场景

## 核心特性

- 📊 **数据驱动** - 所有结论基于量化指标
- 🔄 **快速迭代** - 8-24 小时反思周期
- 📝 **版本追踪** - semver 版本号 + changelog
- 🚨 **熔断机制** - 异常阈值自动暂停
- 📈 **版本对比** - 优化效果清晰可见

## 示例报告

查看 `templates/reflection-template.md` 获取完整模板。

## 学习资源

- [Skill 详细文档](SKILL.md)
- [最佳实践指南](references/best-practices.md)
- [报告模板](templates/reflection-template.md)

---

**版本**: v1.0  
**创建**: 2026-03-26  
**维护**: 肥肥 🦞
