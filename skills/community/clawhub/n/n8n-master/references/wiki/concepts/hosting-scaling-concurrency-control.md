# Self-hosted concurrency control

## 何时读取

当用户的问题涉及 n8n 文档 `hosting/scaling/concurrency-control.md` 的主题、配置、概念或操作步骤时读取。

## 核心要点

- In regular mode, n8n doesn't limit how many production executions may run at the same time. This can lead to a scenario where too many concurrent executions thrash the event loop, causing performance degradation and unresponsiveness. To prevent this, you can set a concurrency limit for production executions in regular mode. Use this to control how many production executions run concurrently, and queue up any concurrent production executions over the limit. These executions remain in the queue until concurrency capacity frees up, and are then processed in FIFO order.

## 快速定位

- Comparison to queue mode

