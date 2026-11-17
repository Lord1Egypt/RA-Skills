# 复核协议

每次校验最多返回 100 个待复核任务。完成当前批次后继续处理下一批，直到校验结束。

每个任务包含任务 ID、源行 ID、字段、原因、观察值、来源位置和是否阻断。

每个任务只能选择一个动作：

- `confirmed`：来源明确支持观察值，主要用于 OCR 或低置信度任务。
- `corrected`：来源显示其他值；用字段原始类型提交 `corrected_value`。
- `unreadable`：经过页面图像检查后仍无法辨认。
- `not_found`：检查指定位置后确认不存在该行或字段。

```json
{
  "job_id": "任务 UUID",
  "resolutions": [
    {
      "task_id": "复核任务 UUID",
      "action": "corrected",
      "corrected_value": "AA11",
      "evidence_ref": "权重表.xlsx / 病组权重 / row 18"
    }
  ]
}
```

不得为了清除任务而确认结构无效的编码或负数。遇到重复键冲突时必须对照两处来源，修正误读编码或数值，不能在没有证据时自行选取。

提交复核后：

1. 仍有开放任务时继续检查返回的下一批。
2. 修正行产生新任务时回到原始来源处理根因。
3. 只在 `report_ready`、`report_ready_with_warnings` 或 `blocked` 时停止。
4. 最终只返回质量摘要、警告和报告地址。
