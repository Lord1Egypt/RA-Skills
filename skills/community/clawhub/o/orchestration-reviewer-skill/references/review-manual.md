# Review Manual

## 评审流程总览

```
business_goal + existing_plan_ir + skills_manifest
    │
    ▼
[阶段一] 输入规范化 → 解析/合并/补全
    │
    ▼
[阶段二] 静态校验 → Schema / DAG / Scope / Skills
    │ 校验失败 → 记录为 critical issue
    ▼
[阶段三] 语义评审（LLM）→ 7 维度逐项评审
    │
    ▼
[阶段四] 结论生成 → overall_decision + scorecard + issues
    │
    ▼
[阶段五] 可选修订 → revised_plan_ir + diff_report → 再校验
```

## 常见问题模式（Anti-Patterns）

### 1. 过度串行
```
N1 → N2 → N3 → N4 → N5
```
问题：N2 和 N3 无依赖却串行。建议并行。

### 2. 不可达节点
```
N1 → N2
N3 → N4  (N3 无任何入边，且不在 entry_nodes 中)
```
问题：N3 永远不会被执行。

### 3. 孤儿出口
```
N1 → N2 → N3
N4 (无任何入边/出边)
```
问题：N4 完全孤立。

### 4. 扇入扇出不匹配
入口/出口节点数量与实际流程不符。

### 5. 技能错配
节点的 target_skill 与 purpose 描述不匹配。

### 6. 作用域越权
节点声明了超出其职责范围的 state_keys。

### 7. 缺少补偿路径
高风险节点没有 on_failure_route。

## 评审 checklist

- [ ] Schema 校验通过
- [ ] DAG 无环
- [ ] 所有节点可达
- [ ] 入口/出口节点正确
- [ ] 技能绑定在白名单内
- [ ] scoped_state_keys 非空且最小权限
- [ ] 目标覆盖度 ≥ 80%
- [ ] 无过度串行（可并行未并行）
- [ ] 高风险节点有补偿路径
