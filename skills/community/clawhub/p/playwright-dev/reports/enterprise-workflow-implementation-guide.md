# 企业级工作流解决方案实施指南

**推荐方案：Dify + Temporal 组合**  
**版本：** 1.0  
**更新日期：** 2026-03-12

---

## 📋 目录

1. [环境准备](#1-环境准备)
2. [Dify 部署](#2-dify-部署)
3. [Temporal 部署](#3-temporal-部署)
4. [流程定义](#4-流程定义)
5. [Agent 集成](#5-agent-集成)
6. [测试验证](#6-测试验证)
7. [监控运维](#7-监控运维)

---

## 1. 环境准备

### 1.1 硬件要求

| 组件 | 最低配置 | 推荐配置 |
|------|---------|---------|
| **Dify** | 2 核 4GB | 4 核 8GB |
| **Temporal** | 2 核 4GB | 4 核 8GB |
| **数据库** | 2 核 4GB | 4 核 8GB |
| **总计** | 6 核 12GB | 12 核 24GB |

### 1.2 软件要求

- Docker 20.10+
- Docker Compose 2.0+
- Node.js 18+（可选，用于自定义开发）
- Python 3.10+（用于 Temporal Worker）

### 1.3 网络要求

- 开放端口：Dify(3000, 5001), Temporal(7233, 8233)
- 域名（可选）：dify.yourcompany.com, temporal.yourcompany.com
- SSL 证书（生产环境必需）

---

## 2. Dify 部署

### 2.1 Docker Compose 部署（推荐）

```bash
# 创建部署目录
mkdir -p ~/dify-deploy && cd ~/dify-deploy

# 下载 Docker Compose 配置
curl -o docker-compose.yml https://raw.githubusercontent.com/langgenius/dify/main/docker/docker-compose.yaml

# 修改配置（可选）
vim .env

# 启动服务
docker compose up -d

# 查看日志
docker compose logs -f
```

### 2.2 配置文件示例

```yaml
# .env 配置
# Dify 配置
CONSOLE_API_URL=http://localhost:5001
CONSOLE_WEB_URL=http://localhost:3000
SERVICE_API_URL=http://localhost:5001
APP_API_URL=http://localhost:5001

# 数据库配置
DB_USERNAME=postgres
DB_PASSWORD=dify123456
DB_HOST=db
DB_PORT=5432
DB_DATABASE=dify

# Redis 配置
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_PASSWORD=dify123456

# 存储配置
STORAGE_TYPE=local
S3_ENDPOINT=
S3_BUCKET_NAME=
```

### 2.3 访问 Dify

- 控制台：http://localhost:3000
- API：http://localhost:5001
- 默认账号：admin@dify.ai / 首次登录设置密码

### 2.4 配置模型提供商

```bash
# 登录 Dify 控制台
# 设置 → 模型提供商 → 添加模型

# 推荐配置（国产优先）：
1. 阿里云百炼（优先）
   - API Key: 从阿里云获取
   - 模型：qwen-max, qwen-plus

2. 硅基流动
   - API Key: 从硅基流动获取
   - 模型：Qwen2.5-Coder, Qwen2.5

3. OpenAI（备选）
   - API Key: 从 OpenAI 获取
   - 模型：gpt-4, gpt-3.5-turbo
```

---

## 3. Temporal 部署

### 3.1 Docker Compose 部署

```bash
# 创建部署目录
mkdir -p ~/temporal-deploy && cd ~/temporal-deploy

# 创建 docker-compose.yml
cat > docker-compose.yml << 'EOF'
version: '3.8'
services:
  temporal:
    image: temporalio/auto-setup:1.22
    ports:
      - "7233:7233"
    environment:
      - DB=postgresql
      - DB_PORT=5432
      - POSTGRES_USER=temporal
      - POSTGRES_PWD=temporal123
      - POSTGRES_SEEDS=db
    depends_on:
      db:
        condition: service_healthy

  temporal-ui:
    image: temporalio/ui:2.21.0
    ports:
      - "8233:8080"
    environment:
      - TEMPORAL_ADDRESS=temporal:7233
      - TEMPORAL_CORS_ORIGINS=http://localhost:3000

  db:
    image: postgres:14
    environment:
      POSTGRES_USER: temporal
      POSTGRES_PASSWORD: temporal123
      POSTGRES_DB: temporal
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U temporal"]
      interval: 5s
      timeout: 5s
      retries: 5

volumes:
  postgres_data:
EOF

# 启动服务
docker compose up -d

# 查看日志
docker compose logs -f
```

### 3.2 访问 Temporal UI

- UI 地址：http://localhost:8233
- gRPC 地址：localhost:7233

### 3.3 安装 Temporal CLI

```bash
# macOS
brew install temporal

# Linux
curl -sLO https://temporal.download/cli.sh && bash cli.sh

# 验证安装
temporal --version
```

### 3.4 配置 Temporal CLI

```bash
# 配置连接
temporal operator namespace create default

# 查看工作流
temporal workflow list --namespace default
```

---

## 4. 流程定义

### 4.1 Dify 工作流设计

**步骤：**

1. **登录 Dify 控制台**
   - 访问 http://localhost:3000
   - 创建新应用 → 选择"工作流"

2. **设计工作流**
   ```
   开始 → 数据验证 → AI 处理 → 人工审核 → 结果输出 → 结束
   ```

3. **配置节点**

   **节点 1：开始**
   - 输入变量：order_data (JSON)

   **节点 2：数据验证（代码节点）**
   ```python
   def main(order_data: dict) -> dict:
       # 验证订单数据
       if not order_data.get('order_id'):
           return {'valid': False, 'error': '缺少订单 ID'}
       if not order_data.get('amount'):
           return {'valid': False, 'error': '缺少金额'}
       return {'valid': True, 'data': order_data}
   ```

   **节点 3：AI 处理（LLM 节点）**
   - 模型：qwen-max
   - Prompt：分析订单数据，提取关键信息

   **节点 4：人工审核（人工节点）**
   - 配置审核人员
   - 审核通过 → 下一节点
   - 审核拒绝 → 返回 AI 处理

   **节点 5：结果输出（HTTP 请求节点）**
   - 调用 Temporal API 触发后端工作流
   - URL: http://temporal:8233/api/v1/namespaces/default/workflows

4. **发布工作流**
   - 点击"发布"
   - 获取 API 端点

### 4.2 Temporal 工作流定义

**安装 Python SDK：**

```bash
pip install temporalio
```

**创建工作流定义：**

```python
# workflows/order_workflow.py
from temporalio import workflow
from datetime import timedelta

@workflow.defn
class OrderProcessingWorkflow:
    @workflow.run
    async def run(self, order_data: dict) -> dict:
        # 步骤 1：验证订单
        validation_result = await workflow.execute_activity(
            validate_order,
            order_data,
            start_to_close_timeout=timedelta(seconds=30)
        )
        
        if not validation_result['valid']:
            return {'status': 'failed', 'reason': validation_result['error']}
        
        # 步骤 2：处理支付
        payment_result = await workflow.execute_activity(
            process_payment,
            order_data,
            start_to_close_timeout=timedelta(seconds=60)
        )
        
        # 步骤 3：发货
        shipping_result = await workflow.execute_activity(
            ship_order,
            order_data,
            start_to_close_timeout=timedelta(seconds=120)
        )
        
        return {
            'status': 'success',
            'payment': payment_result,
            'shipping': shipping_result
        }

@workflow.defn
class ValidateOrderActivity:
    @workflow.activity
    async def validate_order(self, order_data: dict) -> dict:
        # 实现验证逻辑
        pass

@workflow.defn
class ProcessPaymentActivity:
    @workflow.activity
    async def process_payment(self, order_data: dict) -> dict:
        # 实现支付逻辑
        pass

@workflow.defn
class ShipOrderActivity:
    @workflow.activity
    async def ship_order(self, order_data: dict) -> dict:
        # 实现发货逻辑
        pass
```

**创建 Worker：**

```python
# workers/order_worker.py
from temporalio.client import Client
from temporalio.worker import Worker
from workflows.order_workflow import OrderProcessingWorkflow, ValidateOrderActivity

async def main():
    # 连接 Temporal
    client = await Client.connect('localhost:7233')
    
    # 创建 Worker
    worker = Worker(
        client,
        task_queue='order-processing',
        workflows=[OrderProcessingWorkflow],
        activities=[ValidateOrderActivity, ProcessPaymentActivity, ShipOrderActivity]
    )
    
    # 启动 Worker
    await worker.run()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
```

---

## 5. Agent 集成

### 5.1 Dify 集成 AI Agent

**配置 AI Agent 节点：**

1. **添加 LLM 节点**
   - 选择模型：qwen-max（阿里云）
   - 配置系统提示词

2. **配置 RAG 知识库（可选）**
   - 上传文档
   - 配置向量数据库
   - 设置检索参数

3. **配置 Agent 工具（可选）**
   - 添加搜索工具
   - 添加计算器工具
   - 添加自定义 API 工具

### 5.2 Temporal 集成 AI Agent

**创建 AI Agent Activity：**

```python
# activities/ai_agent.py
import httpx

async def ai_agent_activity(task: str, context: dict) -> dict:
    """调用 Dify API 执行 AI 任务"""
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            'http://dify:5001/v1/workflows/run',
            json={
                'inputs': {
                    'task': task,
                    'context': context
                },
                'response_mode': 'blocking'
            },
            headers={
                'Authorization': 'Bearer YOUR_DIFY_API_KEY'
            }
        )
        
        return response.json()
```

**在工作流中使用：**

```python
@workflow.defn
class OrderProcessingWorkflow:
    @workflow.run
    async def run(self, order_data: dict) -> dict:
        # ... 其他步骤
        
        # AI 风险分析
        risk_analysis = await workflow.execute_activity(
            ai_agent_activity,
            '分析订单风险',
            order_data,
            start_to_close_timeout=timedelta(seconds=60)
        )
        
        # ... 继续流程
```

---

## 6. 测试验证

### 6.1 单元测试

**测试 Temporal 工作流：**

```python
# tests/test_order_workflow.py
import pytest
from temporalio.testing import WorkflowEnvironment
from temporalio.worker import Worker

async def test_order_workflow():
    async with WorkflowEnvironment() as env:
        async with Worker(
            env.client,
            task_queue='test',
            workflows=[OrderProcessingWorkflow],
            activities=[validate_order, process_payment, ship_order]
        ):
            result = await env.client.execute_workflow(
                OrderProcessingWorkflow.run,
                {'order_id': '123', 'amount': 100},
                id='test-workflow',
                task_queue='test'
            )
            
            assert result['status'] == 'success'
```

### 6.2 端到端测试

**测试流程：**

1. **创建测试订单**
   ```bash
   curl -X POST http://dify:5001/v1/workflows/run \
     -H "Authorization: Bearer YOUR_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{
       "inputs": {
         "order_data": {
           "order_id": "TEST-001",
           "amount": 100,
           "product": "Test Product"
         }
       }
     }'
   ```

2. **查看 Temporal 执行**
   ```bash
   temporal workflow show --workflow-id test-workflow
   ```

3. **验证结果**
   - 检查订单状态
   - 检查支付记录
   - 检查发货信息

### 6.3 性能测试

**使用 Temporal Bench：**

```bash
# 安装
go install go.temporal.io/sdk/cmd/temporal-bench@latest

# 运行压力测试
temporal-bench workflow \
  --qps 100 \
  --duration 5m \
  --workflow OrderProcessingWorkflow
```

---

## 7. 监控运维

### 7.1 Dify 监控

**监控指标：**
- API 响应时间
- LLM 调用次数
- 工作流执行成功率
- 用户活跃度

**查看日志：**
```bash
docker compose logs -f dify-api
docker compose logs -f dify-worker
```

### 7.2 Temporal 监控

**监控指标：**
- 工作流执行数
- 活动执行数
- 失败率
- 延迟

**使用 Temporal UI：**
- 访问 http://localhost:8233
- 查看工作流列表
- 查看执行详情
- 重试失败的工作流

**配置告警：**
```yaml
# prometheus.yml
scrape_configs:
  - job_name: 'temporal'
    static_configs:
      - targets: ['temporal:9090']
```

### 7.3 备份策略

**数据库备份：**

```bash
# PostgreSQL 备份
pg_dump -h db -U difify difify > difify_backup.sql

# Temporal 数据库备份
pg_dump -h db -U temporal temporal > temporal_backup.sql
```

**配置文件备份：**

```bash
# 备份 Docker Compose 配置
cp docker-compose.yml docker-compose.yml.backup
cp .env .env.backup
```

### 7.4 故障恢复

**Dify 故障恢复：**

```bash
# 重启服务
docker compose restart

# 查看错误日志
docker compose logs dify-api | grep ERROR

# 回滚版本
git checkout <previous-version>
docker compose up -d
```

**Temporal 故障恢复：**

```bash
# 重启服务
docker compose restart temporal

# 查看工作流状态
temporal workflow list --query "ExecutionStatus = 'Running'"

# 重试失败的工作流
temporal workflow update --workflow-id <workflow-id>
```

---

## 📞 技术支持

- **Dify 文档：** https://docs.dify.ai
- **Temporal 文档：** https://docs.temporal.io
- **GitHub Issues：** 
  - Dify: https://github.com/langgenius/dify/issues
  - Temporal: https://github.com/temporalio/temporal/issues

---

**实施指南版本：** 1.0  
**最后更新：** 2026-03-12  
**维护团队：** 企业工作流实施小组
