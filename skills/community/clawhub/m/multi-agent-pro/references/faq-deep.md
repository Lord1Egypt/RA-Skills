# 深度 FAQ

## Q1: 如何处理超大型输出数据？

**A**: 当单个节点的输出超过 10MB 时，建议将数据写入独立文件，`output_data` 中只存文件路径：

```json
{
  "output_data": {
    "raw_data_file": "./output/collector_raw_data_20260701.json",
    "row_count": 150000,
    "summary": "共采集15万条记录"
  }
}
```

这样状态文件保持精简，大数据通过文件传递。AI 执行下游节点时读取文件即可。

---

## Q2: 如何实现并行执行？

**A**: 当前版本（1.0）的脚本仅支持串行执行。但 AI 编排器可以自行管理并行：

1. 运行 `python orchestrator.py plan pipeline.json` 获取拓扑排序
2. 识别同层节点（入度同时为 0 的节点）
3. AI 同时 spawn 多个子任务处理同层节点
4. 各子任务完成后分别调用 `state_store.py complete` 保存输出
5. 所有同层节点完成后，继续下一层

---

## Q3: 如何在流水线中传递文件路径？

**A**: 在 `output_data` 中传递路径字符串即可：

```bash
python state_store.py complete state.json collector '{"output_file": "/data/raw_data.json"}'
```

下游节点从 `output_data` 中读取路径，然后读取文件内容。建议使用绝对路径避免歧义。

---

## Q4: 多个流水线可以共享状态文件吗？

**A**: 不建议。每个流水线应有独立的 `pipeline_state.json`。如果需要跨流水线共享数据，建议：

1. 在 DAG 的 `state_store.path` 中指定不同的状态文件名
2. 通过文件系统共享中间结果（写入约定路径）
3. 在新流水线的节点中读取上一个流水线的输出文件

---

## Q5: 如何回滚到某个节点的执行前状态？

**A**: 当前版本不支持自动回滚。建议做法：

1. 在关键节点执行前手动备份 `pipeline_state.json`
2. 需要回滚时恢复备份文件
3. 将该节点状态手动改为 `pending`

未来版本计划支持自动快照功能。

---

## Q6: 如何处理节点间数据格式不匹配？

**A**: 建议在 DAG 定义中明确每个节点的 `inputs` 和 `outputs`，并在节点角色描述中注明数据格式：

```json
{
  "id": "analyzer",
  "role": "输入：JSON数组格式的清洗数据。输出：包含analysis_result和key_metrics的对象",
  "inputs": ["cleaned_data"],
  "outputs": ["analysis_result", "key_metrics"]
}
```

AI 编排器在执行时会参考这些描述进行格式转换。

---

## Q7: 如何监控长时间运行的流水线？

**A**: 定期运行状态查询：

```bash
python orchestrator.py status state.json
```

或查看状态文件中的时间戳，判断节点是否卡住。如果节点 `started_at` 距当前时间超过 `timeout` 设定，说明可能卡住，需要手动干预。

---

## Q8: 如何在敏感数据处理场景中使用？

**A**:
1. 不要将真实密钥、密码写入 `output_data`
2. 在节点角色描述中注明需要脱敏的字段
3. AI 执行任务时自动对敏感字段进行掩码处理
4. 状态文件存储在本地，不上传到任何服务器
5. 使用完毕后可安全删除 `pipeline_state.json`

---

## Q9: 支持 Windows / macOS / Linux 吗？

**A**: 全部支持。脚本仅使用 Python 标准库，无平台依赖。文件路径使用 `/` 分隔符，在 Windows 上 Python 会自动处理。

---

## Q10: 如何自定义重试间隔？

**A**: 当前版本使用固定的指数退避（2^n 秒）。如需自定义，修改 `error_recovery.py` 中的 `delay = 2 ** retry_num` 行即可。
