# Knowledge Entity Self-Check Questions

For each knowledge entity, AI must run through the corresponding self-check
list and populate the ``_selfCheck`` field:

```json
{
  "_selfCheck": {
    "passed": ["check item that's confirmed"],
    "questions": ["check item still uncertain"]
  }
}
```

Entities with non-empty ``_selfCheck.questions`` are rendered with a yellow
border and a "?" badge so the user can see at a glance which entities still
need verification.

## painPoint

1. **症状还是根因**：是可观测的现象（症状），还是造成现象的机制（根因）？
2. **严重度依据**：判断 severity 的依据是什么——数据、感受，还是对标？
3. **受影响方**：哪些角色或部门直接受影响？

## strategy

1. **痛点对应**：对应哪个具体 painPoint？是否有 ``solves`` 关系？
2. **执行前提**：实施需要哪些资源、能力或时机？
3. **效果衡量**：怎么衡量它有效？是否有 ``measures`` 关系指向 metric？

## rule

1. **规则来源**：是平台政策、法规要求，还是内部约定？
2. **违反后果**：违反后会发生什么——封号、罚款、流量降级？
3. **约束目标**：约束哪些 strategy？是否有 ``enforces`` 关系？

## metric

1. **计算方式**：值或基准是怎么得来的？
2. **衡量目标**：衡量哪个 strategy？是否有 ``measures`` 关系？
3. **阈值依据**：阈值的业务依据是什么——历史数据、行业基准、目标设定？

## practice

1. **频率周期**：执行频率是多少——每日、每周、每月、按需？
2. **支撑策略**：支撑哪个 strategy？是否有 ``requires`` 反向关系？
3. **成功信号**：怎么知道实践到位了——CTR 提升、转化率改善、客户反馈？

## pitfall

1. **导致痛点**：导致什么具体 painPoint？是否有 ``causes`` 关系？
2. **避免方式**：怎么避免——规则、流程、工具？
3. **真实案例**：是否有真实案例或数据支撑？

## Output Format

For each entity, populate ``_selfCheck`` honestly:

```json
{
  "id": "pain-001",
  "name": "ROI 不稳",
  "entityType": "painPoint",
  "_selfCheck": {
    "passed": ["可观测", "受影响方明确"],
    "questions": ["是症状还是根因？— 待用户确认"]
  }
}
```

If you don't know, put it in ``questions``. Honesty about uncertainty is more
valuable than fake confidence — the user gets to decide what to verify.

If ``questions`` is an empty array ``[]``, the entity is fully self-checked
and the renderer will display it in normal style.
