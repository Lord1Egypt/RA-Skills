# meta-skill-weaver | ClawHub 上架材料 (v2.4.0)

---

## 📝 技能描述（200 字）

**meta-skill-weaver（技能编织器）** 是一款 AI 技能编排引擎，专为复杂多步骤任务设计。它通过第一性原理任务分解器将宏大目标拆解为原子任务，利用 EventBus 事件系统实现多技能松耦合协作，支持并行执行、超时控制、中断恢复。v2.4.0 新增 MetricsMiddleware 自优化触发机制（失败率超阈值自动触发优化建议 + 自适应重试策略）和 FeedbackMiddleware 用户反馈收集（评分/评论/统计）。核心价值：让 AI 从"单点响应"升级为"系统协作"，轻松驾驭研究→分析→报告等长程任务，是构建企业级 AI 工作流的必备基础设施。

---

## 🆕 v2.4.0 新增功能

### MetricsMiddleware — 自优化触发机制

- **失败率自动分析**：当任务失败率 > 25% 或连续失败 > 3 次时，自动触发优化建议
- **自适应重试策略**：根据历史失败模式动态调整重试次数和退避倍数
- **指标持久化与趋势分析**：时间序列指标存储，支持趋势查询

```javascript
const { MetricsMiddleware } = require('meta-skill-weaver/src/middleware/metrics-middleware');

const metrics = new MetricsMiddleware({
  failureRateThreshold: 0.25,
  onOptimizationTriggered: (analysis) => {
    console.log('优化触发:', analysis.suggestions);
  },
});

// 在中间件链中使用
chain.use(metrics);

// 查询指标报告
const report = metrics.getReport();
```

### FeedbackMiddleware — 用户反馈收集

- **评分系统**：1-5 星评分 + 文字评论 + 标签
- **自动分类**：praise / issue / bug / suggestion
- **统计与排名**：按任务/技能维度统计，技能评分排名
- **趋势分析**：按日/周/小时聚合

```javascript
const { FeedbackMiddleware } = require('meta-skill-weaver/src/middleware/feedback-middleware');

const feedback = new FeedbackMiddleware();

// 提交反馈
feedback.submit({
  taskId: 'report-123',
  skillName: 'weather',
  rating: 5,
  comment: '非常好用',
  tags: ['fast', 'reliable'],
});

// 查询统计
const stats = feedback.getStats();
const rankings = feedback.getSkillRankings();
```

---

## 📊 六维评分（v2.4.0）

| 维度 | 评分 | 说明 |
|------|------|------|
| T 技术深度 | 0.75 | +0.05，新增中间件实现、指标分析、自适应重试 |
| C 认知增强 | 0.65 | 保持不变 |
| O 编排能力 | 0.80 | 保持不变 |
| E 进化能力 | 0.75 | +0.13，自优化触发 + 用户反馈收集 + 趋势分析 |
| M 市场验证 | 0.70 | +0.15，真实代码 + 测试覆盖，ClawHub 上架准备就绪 |
| U 用户体验 | 0.58 | 保持不变 |
| **平均** | **0.71** | **+0.06** |

---

## 📁 v2.4.0 新增文件

```
src/middleware/
├── metrics-middleware.js     # 自优化触发机制 + 自适应重试
└── feedback-middleware.js    # 用户反馈收集 + 统计分析
tests/
├── metrics-middleware.test.js  # 28 个测试用例
└── feedback-middleware.test.js # 26 个测试用例
```

---

**更新时间**：2026-04-25  
**版本**：v2.4.0  
**维护者**：pagoda111king
