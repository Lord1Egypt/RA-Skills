# Function — Ontology 的原生计算层

## 4种函数类型

| 类型 | 触发方式 | 典型用途 | 性能要求 |
|------|---------|---------|---------|
| Object Function | 针对单个对象自动调用 | 派生属性、AI 推理 | < 1s |
| Object Set Function | 针对对象集合 | 批量计算、聚合分析 | < 10s |
| Action Validation Function | Action 提交时 | 业务规则校验 | < 2s |
| Query Function | 前端显式调用 | 复杂计算、自定义 API | 最长 30s |

**运行时规格：** TypeScript（ES2020+）、最大 30s（超时终止，不回滚）、内存 512MB、网络默认禁止。

## 性能优化

```typescript
// ❌ 反模式：N 次请求
for (const emp of await employees.fetchAll()) {
  const projects = await emp.$link.projects.fetchAll();
}

// ✅ 正确：1 次请求
const allProjects = await employees.$link.projects.fetchAll();
```

1. 用 ObjectSet 批量获取，避免循环
2. 多个独立查询用 `Promise.all`
3. 高频计算配置 TTL 缓存
4. 百万行级聚合在 Pipeline 层预计算

## TTL 缓存选择

| 场景 | TTL |
|------|-----|
| 实时性要求高（库存状态） | 1-5 分钟 |
| 统计类指标（月度汇总） | 1 小时 |
| 不变的计算结果（历史归档） | 永久缓存 |

## 设计原则

- Object Function 必须是纯函数——可能被并发调用，有副作用会导致不可预期状态
- 不要在 Object Function 中修改 Ontology 数据
- Query Function 超时后用户看到错误，不会回滚，需设计降级策略
