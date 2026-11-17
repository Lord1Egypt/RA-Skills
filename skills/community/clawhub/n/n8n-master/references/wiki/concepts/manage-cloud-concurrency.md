# Cloud concurrency

## 何时读取

当用户的问题涉及 n8n 文档 `manage-cloud/concurrency.md` 的主题、配置、概念或操作步骤时读取。

## 核心要点

- Too many concurrent executions can cause performance degradation and unresponsiveness. To prevent this and improve instance stability, n8n sets concurrency limits for production executions in regular mode. Any executions beyond the limits queue for later processing. These executions remain in the queue until concurrency capacity frees up, and are then processed in FIFO order.

## 快速定位

- Concurrency limits
- Details
- Comparison to queue mode

