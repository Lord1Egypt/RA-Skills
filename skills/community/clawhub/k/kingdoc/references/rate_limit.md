# 限流 / 性能 / 硬件自适应策略

> 设计红线：**再快也不能拖累用户电脑**。所有并发与批量参数均由本机硬件自动决定。

## 1. API 限流（429）退避

`engine/rate_limiter.py` 实现指数退避 + 随机抖动：

```
delay = min(2^retry + random(0,1), 300s)   # 最多重试 5 次
```

`engine/client.py` 读取 `Retry-After` 头，结合退避，避免雪崩。

## 2. 硬件自适应并发（v3.0.0 新增）

`engine/hardware.py` 在首次运行时采集本机 CPU/内存，并缓存到
`.kingdoc_hardware_profile.json`（30 分钟内复用），计算出：

| 参数 | 低端机 (≤2核/<4GB) | 普通机 | 高端机 (≥8核/≥16GB) |
|------|-------------------|--------|---------------------|
| 并发子进程数 `workers` | 1 | min(核数,4) | min(核数,8) |
| 批量写入分块 `batch_chunk` | 50 | 200 | 500 |
| 大文件阈值 | 50MB | 100MB | 100MB |
| 本地渲染并行 | 否 | 视核数 | 是 |

调用方式：

```python
from engine.hardware import get_recommended_settings
s = get_recommended_settings()
print(s["workers"], s["batch_chunk"], s["note"])
```

AI 在批量生成思维导图/流程图、批量写表时，应读取该参数控制并行度，
**绝不**超过 `workers`，保证用户电脑不卡顿。

## 3. 会话级配额保护

| 限制项 | 阈值 | 说明 |
|--------|------|------|
| 写入次数 | 100 次/会话 | 防止 AI 失控循环 |
| 文件总大小 | 1GB/会话 | 防止批量大文件撑爆配额 |
| API 调用 | 1000 次/会话 | 综合限制 |

## 4. 批量合并

50ms 窗口内连续写入自动合并为一次请求，进一步降低 API 压力。

*最后更新：2026-07-12 | v3.0.0*
