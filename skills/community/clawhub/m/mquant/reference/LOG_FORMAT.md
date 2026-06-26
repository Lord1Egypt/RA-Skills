# 日志格式规范

## 文件结构

每个策略对应一个 `.log` 文件：
```
strategy_name.py
strategy_name.log  <- 生成元数据 + 运行时日志
```

---

## 格式示例

```
===== GENERATION META =====
{
  "version": 1,
  "previous": null,
  "generated_at": "2026-03-05 18:00:00",
  "model": "moonshot/kimi-k2.5",
  "template": "Dual MA",
  "params": {"fast_ma": 5, "slow_ma": 20},
  "target_path": "D:\\Matic\\M-quant\\userA\\",
  "matic_exe_path": "D:\\Matic\\maticupdate.exe",
  "changelog": "Initial version"
}

===== RUNTIME LOG =====
[2026-03-05 22:20:01] [INFO] Strategy started
[2026-03-05 22:20:01] [INFO] Target price: 18.50, Order amount: 100
[2026-03-05 22:20:05] [INFO] Condition triggered! Current 18.45 <= Target 18.50
[2026-03-05 22:20:05] [INFO] Buy order sent: 601688.SH, Order ID 12345
```

---

## 日志级别

| 级别 | 用途 |
|------|------|
| `DEBUG` | 详细数据（tick价格、计算过程、判断条件） |
| `INFO` | 关键事件（初始化、交易触发、参数变化） |
| `WARN` | 警告（数据异常、条件不满足但仍继续） |
| `ERROR` | 错误（API调用失败、异常抛出） |

---

## 代码实现

```python
import os
from datetime import datetime

LOG_FILE = None

def write_log(level, msg):
    """Write log to .log file"""
    global LOG_FILE
    if LOG_FILE is None:
        LOG_FILE = os.path.splitext(__file__)[0] + '.log'
    
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_line = f"[{timestamp}] [{level}] {msg}\n"
    
    try:
        with open(LOG_FILE, 'a', encoding='utf-8') as f:
            f.write(log_line)
    except:
        pass
```

---

## 排查问题检查点

1. **行情数据是否接收？** → 检查 DEBUG 日志的 tick/kline 数据
2. **计算是否正确？** → 检查计算的索引、均线值等
3. **判断条件是否满足？** → 检查条件判断的 True/False
4. **交易是否执行？** → 检查 order() 调用和返回值
