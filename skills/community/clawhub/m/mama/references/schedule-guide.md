# 定时检查

默认检查时间：工作日 `08:00-18:00`，每 2 小时一次。

推荐 cron：

```cron
0 8-18/2 * * 1-5
```

对应检查点：周一至周五 `08:00、10:00、12:00、14:00、16:00、18:00`。

## 手动检查

```bash
python scripts/process_digest.py --since-hours 2
```

## 自定义

通过 `scripts/digest_config.py` 修改：

```python
CHECK_WINDOW = {
    "enabled": True,
    "workdays": [1, 2, 3, 4, 5],
    "start": "08:00",
    "end": "18:00",
    "interval_hours": 2,
}
```
