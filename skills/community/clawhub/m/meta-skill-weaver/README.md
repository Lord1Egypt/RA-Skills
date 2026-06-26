# Meta-Skill Weaver - 元技能编织器

**版本**: v0.4.1  
**定位**: L2 编排层 - AI 技能编排引擎  
**状态**: ✅ 已上架 ClawHub

---

## 🎯 适用场景

✅ 多步骤任务（研究→分析→报告）  
✅ 多技能协作（需要 3+ 技能）  
✅ 需要进度追踪的长程任务  
✅ 需要中断恢复的长时任务  
✅ 需要事件驱动的松耦合协作

---

## 🔧 核心功能

**v0.4.1 新增**（2026-04-06）:
- ✅ EventBus 事件系统
- ✅ Jest 单元测试框架（35 个用例）
- ✅ 第一性原理任务分解器

**v0.3.0 功能**:
- ✅ Middleware 链（7 个内置中间件）
- ✅ 虚拟路径系统（线程隔离）
- ✅ 并发执行（限制 3 个并发）
- ✅ 超时控制（默认 15 分钟）

**原有功能**:
- ✅ 任务分解与编排
- ✅ 技能分配与调度
- ✅ 状态追踪（6 种状态）
- ✅ 中断恢复
- ✅ 数据收集

---

## 🏗️ 技术架构

### 模块结构
```
src/
├── task-tracker.js          # 核心任务追踪器
├── event-bus.js             # 事件总线（v0.4.1 新增）
├── first-principle-decomposer.js  # 任务分解器（v0.4.1 新增）
├── middleware-chain.js      # 中间件链
├── parallel-execution.js    # 并行执行
└── virtual-path-system.js   # 虚拟路径
```

### 测试覆盖
```
tests/
├── task-tracker.test.js     # 任务追踪测试
├── event-bus.test.js        # 事件系统测试（12 个用例）
└── first-principle-decomposer.test.js  # 分解器测试（15 个用例）
```

**总测试用例**: 35 个  
**覆盖率**: 73.72%（语句）/ 60.08%（分支）/ 73.41%（函数）

---

## 📋 工作流程

```
1. 接收复杂任务
   ↓
2. 第一性原理分解（识别假设→5Why 分析→重构任务）
   ↓
3. 分解为原子任务
   ↓
4. 通过 EventBus 分配合适技能
   ↓
5. 并行/串行执行（Middleware 链处理）
   ↓
6. 事件追踪与状态更新
   ↓
7. 合成最终结果
   ↓
8. 交付报告
```

---

## 🔌 EventBus API

### 基本用法
```javascript
const { EventBus } = require('./src/event-bus');

const bus = new EventBus({ historySize: 1000 });

// 订阅事件
bus.on('task-started', (payload, context) => {
  console.log('任务开始:', payload);
});

// 发布事件
await bus.emit('task-started', { taskId: '123' }, { userId: 456 });

// 添加拦截器
bus.addBeforeInterceptor(async ({ event, payload }) => {
  console.log('事件前拦截:', event);
});
```

### 内置拦截器
- `loggingInterceptor()` - 日志记录
- `performanceInterceptor()` - 性能监控
- `errorTrackingInterceptor(handler)` - 错误追踪

---

## 🧪 测试

```bash
# 运行测试
npm test

# 带覆盖率报告
npm run test:coverage

# 监视模式
npm run test:watch
```

**测试命令**: `npx jest --coverage`

---

## 📊 六维评估

| 维度 | v0.3.0 | v0.4.1 | 改进 | 目标 |
|------|--------|--------|------|------|
| T（技术深度） | 0.70 | 0.75 | +0.05 | 0.80 |
| C（认知增强） | 0.65 | 0.70 | +0.05 | 0.80 |
| O（编排能力） | 0.80 | 0.85 | +0.05 | 0.90 |
| E（进化能力） | 0.62 | 0.70 | +0.08 | 0.80 |
| M（商业化） | 0.55 | 0.68 | +0.13 | 0.70 |
| U（用户体验） | 0.58 | 0.65 | +0.07 | 0.80 |
| **平均** | **0.65** | **0.72** | **+0.07** | **0.80** |

---

## 💼 服务定价

| 版本 | 价格 | 包含 |
|------|------|------|
| 个人版 | $99.9 | 永久使用 +1 年更新 |
| 商业版 | $299.9 | 商业用途 + 优先支持 |
| 企业版 | $999.9 | 定制 + 部署 + 培训 |

---

## 🏆 头部技能对标

**对标**: writing-assistant（3.641 分）

**我们的优势**:
- ✅ 更强大的编排能力（O 维度 0.85）
- ✅ 支持并发执行
- ✅ 完整的状态追踪
- ✅ 事件驱动架构（v0.4.1）
- ✅ 单元测试覆盖（v0.4.1）

---

## 📞 支持

- 📧 support@cloud-shrimp.com
- 💬 微信：CloudShrimpSupport

**响应**: 24 小时内

---

## 📝 版本历史

**v0.4.1**（2026-04-06）- O 维度提升
- EventBus 事件系统完善
- Jest 单元测试框架
- 第一性原理任务分解器
- 六维评分 0.65→0.72

**v0.3.0**（2026-03-31）- 重大升级
- EventBus 事件系统
- Jest 单元测试框架（35 个用例）
- 第一性原理任务分解器
- 六维评分 0.58→0.65

**v0.2.0**（2026-03-28）
- Middleware 链
- 虚拟路径系统
- 并发执行

**v0.1.0**（2026-03-27）- 初始版本

---

**版本**: v0.4.1 | **更新**: 2026-04-06 | **维护者**: 王的奴隶 · 严谨专业版

---

## ❓ FAQ

### Q1: 如何编排多个技能协作？

**A**: 使用 meta-skill-weaver 的编排功能，描述复杂任务，它会自动分解并分配合适的技能。

```
请编排以下任务：分析竞品并生成报告
```

### Q2: 事件系统如何使用？

**A**: EventBus 支持订阅/发布模式，可以监听任务执行的各种事件。

```javascript
const { EventBus } = require('./src/event-bus');
const bus = new EventBus();
bus.on('task-completed', (data) => console.log(data));
```

### Q3: 如何追踪长程任务进度？

**A**: meta-skill-weaver 提供状态追踪功能，可以查询任务的当前状态和历史。

```
查询任务 [任务 ID] 的进度
```

### Q4: 支持中断恢复吗？

**A**: 是的，支持中断恢复。任务状态会持久化，可以随时恢复。

```
恢复任务 [任务 ID]
```

### Q5: 如何自定义 Middleware？

**A**: 可以创建自定义 Middleware，实现特定功能。

```javascript
const myMiddleware = {
  name: 'my-middleware',
  priority: 5,
  execute: async (context, next) => {
    // 自定义逻辑
    await next();
  }
};
```

---

## 📁 项目结构

```
meta-skill-weaver/
├── SKILL.md                 # 技能定义
├── README.md                # 本文档
├── package.json             # 项目配置
├── src/
│   ├── task-tracker.js      # 任务追踪
│   ├── event-bus.js         # 事件总线
│   └── ...
├── tests/
│   ├── task-tracker.test.js
│   ├── event-bus.test.js
│   └── ...
└── examples/
    └── usage-examples.md    # 使用示例
```

---

## 💰 购买与授权

**个人版**: $99.9（永久使用 + 1 年更新）  
**商业版**: $299.9（商业用途 + 优先支持）  
**企业版**: $999.9（定制部署 + 培训）

**购买方式**: 访问 ClawHub 技能页面

**ClawHub ID**: k971w2r2jxpvzjhnw6xaqwzbeh84a0hc
