# Queue mode

## 何时读取

当用户的问题涉及 n8n 文档 `hosting/scaling/queue-mode.md` 的主题、配置、概念或操作步骤时读取。

## 核心要点

- You can run n8n in different modes depending on your needs. The queue mode provides the best scalability. When running in queue mode, you have multiple n8n instances set up, with one main instance receiving workflow information (such as triggers) and the worker instances performing the executions.

## 快速定位

- How it works
- Configuring workers
- Set encryption key
- Set executions mode
- Start Redis
- Start workers
- Running n8n with queues
- Webhook processors
- Configure webhook URL
- Configure load balancer
- Disable webhook processing in the main process (optional)
- Configure worker concurrency
- Concurrency and scaling recommendations
- Multi-main setup
- Leader designation
- Configuring multi-main setup

