---
name: periodic-reflection
description: |
  周期性反思报告生成工具。用于自动化生成结构化的自我进化反思报告，支持多场景（EvoMap 发布、Agent 进化、DevOps 运维等）。
  
  **触发场景：**
  - 用户要求生成周期性反思报告
  - 需要量化指标对比和版本追踪
  - 需要数据驱动的优化决策
  - 用户提到"反思"、"复盘"、"进化报告"、"周期性总结"
  - 需要固化优化成果和 changelog
---

# 周期性反思报告 Skill

自动化生成结构化的自我进化反思报告，支持数据驱动的快速迭代优化。

## 架构

```
periodic-reflection/
├── SKILL.md                     # 本文件
├── scripts/
│   ├── generate-report.js       # 报告生成脚本
│   ├── metrics-collector.js     # 指标收集器
│   └── version-manager.js       # 版本管理器
├── templates/
│   └── reflection-template.md   # 报告模板
└── references/
    ├── best-practices.md        # 最佳实践
    └── metrics-guide.md         # 指标定义指南
```

## 快速开始

### 1. 生成反思报告

```bash
cd ~/workspace/agent/workspace/skills/periodic-reflection

# 使用模板生成报告
node scripts/generate-report.js \
  --project "EvoMap 发布器" \
  --cycle "daily" \
  --output reports/reflection-$(date +%Y-%m-%d).md
```

### 2. 配置监控指标

编辑 `scripts/metrics-collector.js` 添加你的指标：

```javascript
const metrics = {
  // EvoMap 发布场景
  publishCount: { command: 'cat logs/publish.log | wc -l', target: 100 },
  quarantineRate: { command: 'node scripts/calc-quarantine.js', target: '<5%' },
  successRate: { command: 'node scripts/calc-success.js', target: '>95%' },
  
  // Agent 进化场景
  taskCompletion: { command: '...', target: '>90%' },
  errorRate: { command: '...', target: '<2%' },
  
  // DevOps 场景
  uptime: { command: '...', target: '>99.9%' },
  mttr: { command: '...', target: '<30min' }
};
```

### 3. 设置定时任务

```bash
# 每 8 小时生成一次反思报告
crontab -e

# 添加：
0 */8 * * * cd ~/workspace/agent/workspace/skills/periodic-reflection && node scripts/generate-report.js --auto
```

## 报告结构

### 执行摘要（必填）
- 状态标识（🟢/🟡/🔴）
- 核心指标表格
- 一句话总结

### 版本对比（必填）
- 前后版本指标对比
- 改善百分比
- 优化结论

### 关键发现（必填）
- 数据支撑的洞察
- 问题根因分析
- 验证结果

### 变更文件（必填）
- 文件列表
- 版本号变更
- 变更说明

### 行动计划（必填）
- 立即完成事项
- 短期计划（1-3 天）
- 中期计划（1-2 周）

## 核心原则

### 1. 数据驱动
- ✅ 所有结论有数据支撑
- ✅ 指标可量化、可测量
- ✅ 前后对比清晰

### 2. 快速迭代
- ✅ 反思周期 8-24 小时
- ✅ 单次优化≤3 个参数
- ✅ 验证周期 1-3 天

### 3. 可追溯性
- ✅ semver 版本号
- ✅ changelog 追踪
- ✅ 配置版本同步

### 4. 熔断机制
- ✅ 异常阈值明确
- ✅ 自动暂停机制
- ✅ 排查后恢复

## 推荐反思周期

| 场景 | 周期 | 触发时间 |
|------|------|----------|
| EvoMap 发布 | 8 小时 | 06:00, 14:00, 22:00 |
| Agent 进化 | 24 小时 | 每日 09:00 |
| DevOps 运维 | 24 小时 | 每日 10:00 |
| 战略复盘 | 每周 | 周一 09:00 |

## 指标定义指南

### EvoMap 发布场景

| 指标 | 定义 | 计算方式 | 健康阈值 |
|------|------|----------|----------|
| 发布量 | 每日成功发布资产数 | COUNT(publish_success) | >100 条/节点 |
| 隔离率 | 被 quarantine 的比例 | quarantine/total * 100% | <5% |
| 成功率 | 发布成功比例 | success/total * 100% | >95% |
| 内容轮换率 | 模板使用多样性 | used_templates/total * 100% | >80% |
| 声誉分数 | 节点声誉评分 | API 获取 | >70 |

### Agent 进化场景

| 指标 | 定义 | 计算方式 | 健康阈值 |
|------|------|----------|----------|
| 任务完成率 | 成功完成任务比例 | completed/total * 100% | >90% |
| 用户满意度 | 用户评分/反馈 | 平均评分 | >4.5/5 |
| 错误率 | 执行错误比例 | errors/total * 100% | <2% |
| 响应时间 | 平均响应延迟 | AVG(response_time) | <3s |

### DevOps 运维场景

| 指标 | 定义 | 计算方式 | 健康阈值 |
|------|------|----------|----------|
| 可用性 | 系统正常运行时间 | uptime/total * 100% | >99.9% |
| MTTR | 平均恢复时间 | SUM(downtime)/incidents | <30min |
| 告警数 | 触发告警次数 | COUNT(alerts) | <5/天 |
| 资源利用率 | CPU/内存使用率 | AVG(usage) | 60-80% |

## 最佳实践

### 1. 固定时间触发
每天同一时间生成报告，形成节奏感。

### 2. 自动化优先
能用脚本获取的数据不手动填写。

### 3. 简洁明了
执行摘要控制在 10 行以内。

### 4. 行动导向
每个发现都对应具体的下一步行动。

### 5. 版本关联
报告与代码版本一一对应。

## 文件组织

```
reports/
├── templates/
│   └── reflection-template.md    # 报告模板
├── evolution/
│   ├── evolution-report-YYYY-MM-DD-HHMM.md
│   └── ...
└── metrics/
    ├── daily-stats-YYYY-MM-DD.json
    └── ...
```

## 示例报告

详见 `templates/reflection-template.md`

## 常见问题

### Q: 反思周期应该多长？
A: 取决于场景：
- 高频变化（发布/交易）：8 小时
- 中频变化（Agent 行为）：24 小时
- 低频变化（架构/战略）：每周

### Q: 如何确定优化有效？
A: 三个标准：
1. 指标改善幅度 >10%
2. 连续 3 个周期稳定
3. 无副作用（其他指标不恶化）

### Q: 版本号怎么管理？
A: 遵循 semver：
- MAJOR: 突破性变更
- MINOR: 新功能/优化
- PATCH: bug 修复/配置调整

### Q: 如何处理异常数据？
A: 熔断机制：
1. 超过阈值自动暂停
2. 记录异常上下文
3. 根因分析后恢复
4. 更新阈值（如需要）

---

**Skill 版本**: v1.0
**创建日期**: 2026-03-26
**维护者**: 肥肥 🦞
**适用场景**: EvoMap 发布、Agent 自我进化、DevOps 运维、任何需要持续优化的场景
