"""
跨工作区任务分发系统 - 部署配置

本文件定义了如何在不同工作区部署任务监听器和分发器

============================================================
架构概览
============================================================

[主工作区]                    [目标工作区A]           [目标工作区B]
┌─────────────┐            ┌─────────────┐         ┌─────────────┐
│             │            │             │         │             │
│ TaskDistributor     ←→   TaskListener    ←→    TaskListener
│ (分发+聚合)         │  (接收+执行)   │  (接收+执行)   │
│             │            │             │         │             │
│ 通知你       │            └─────────────┘         └─────────────┘
└─────────────┘
       ↑
       你

============================================================
部署步骤
============================================================

【步骤1: 在目标工作区部署 TaskListener】

1. 复制以下文件到目标工作区:
   - pao-system/task_listener.py
   - pao-system/src/protocols/task_protocol.py

2. 启动监听器:
   python task_listener.py --ws-id ws_xxx --ws-name "工作区名称" --port 8765

3. 守进程运行（可选）:
   python -m pip install gunicorn
   gunicorn -k uvicorn.workers.UvicornWorker task_listener:app

【步骤2: 在主工作区部署 TaskDistributor】

1. 复制以下文件到主工作区:
   - pao-system/task_distributor.py
   - pao-system/src/protocols/task_protocol.py

2. 配置目标工作区地址:
   编辑配置文件 workers.json

3. 启动分发器:
   python -c "from task_distributor import get_distributor; import asyncio; asyncio.run(get_distributor())"

【步骤3: 测试】

1. 启动目标工作区的监听器:
   python task_listener.py --ws-id ws_finance --ws-name "金融分析区" --port 8765

2. 在主工作区测试:
   python -c "
   from task_distributor import TaskDistributor, WorkerInfo
   import asyncio
   
   async def test():
       dist = TaskDistributor('main')
       dist.register_worker(WorkerInfo(
           ws_id='ws_finance',
           ws_name='金融分析区',
           host='localhost',
           port=8765,
           status='online',
           capabilities=['data_query']
       ))
       result = await dist.dispatch('测试', {'msg': 'hello'}, workers=['ws_finance'])
       print(result.aggregated_result)
   
   asyncio.run(test())
   "

============================================================
配置文件示例
============================================================

workers.json:
```json
{
    "workers": [
        {
            "ws_id": "ws_finance",
            "ws_name": "金融分析区",
            "host": "192.168.1.100",
            "port": 8765,
            "capabilities": ["data_query", "stock_analysis", "fund_query"]
        },
        {
            "ws_id": "ws_code",
            "ws_name": "代码分析区", 
            "host": "192.168.1.101",
            "port": 8765,
            "capabilities": ["code_analysis", "file_search"]
        },
        {
            "ws_id": "ws_research",
            "ws_name": "研究专区",
            "host": "192.168.1.102",
            "port": 8765,
            "capabilities": ["web_search", "research"]
        }
    ],
    "settings": {
        "timeout": 300,
        "max_retries": 2,
        "heartbeat_interval": 30
    }
}
```

============================================================
使用示例
============================================================

【示例1: 分发到指定工作区】

from task_distributor import TaskDistributor, WorkerInfo
import asyncio

async def main():
    dist = TaskDistributor("main")
    
    # 注册工作区
    dist.register_worker(WorkerInfo(
        ws_id="ws_finance",
        ws_name="金融分析区", 
        host="192.168.1.100",
        port=8765,
        status="online",
        capabilities=["data_query"]
    ))
    
    # 分发任务
    result = await dist.dispatch(
        "查股价",
        {"stock": "600519"},
        workers=["ws_finance"]
    )
    
    print(result.aggregated_result)

asyncio.run(main())

【示例2: 自动选择工作区】

# 根据 capabilities 自动选择
result = await dist.dispatch(
    "查股票数据",
    {"stock": "000001"},
    workers=["auto"]  # 自动选择所有在线的
)

【示例3: 并行分发到多个工作区】

result = await dist.dispatch(
    "全面分析",
    {"stock": "600519"},
    workers=["ws_finance", "ws_research"]  # 同时发到多个
)

============================================================
常见问题
============================================================

Q: 目标工作区没有公网IP怎么办？
A: 可以用内网穿透（如 ngrok、frp）或 VPN 连接

Q: 如何保证任务不丢失？
A: TaskListener 有本地队列，失败会自动重试

Q: 可以分发多少任务？
A: 目前无限制，受网络和目标工作区处理能力影响

============================================================
扩展开发
============================================================

1. 添加新任务类型:
   在 TaskListener.executor 注册新的 handler

2. 添加认证:
   在消息中添加 token 验证

3. 添加加密:
   使用 TLS/SSL 加密通信

4. 添加监控:
   接入 Prometheus/Grafana
"""

# 配置文件模板
CONFIG_TEMPLATE = {
    "workers": [],
    "settings": {
        "timeout": 300,
        "max_retries": 2,
        "heartbeat_interval": 30
    }
}

# 使用说明
USAGE = """
# 快速开始

## 1. 在目标工作区启动监听器
python task_listener.py --ws-id ws_finance --ws-name "金融分析区" --port 8765

## 2. 在主工作区使用分发器
from task_distributor import dispatch_task
import asyncio

result = asyncio.run(dispatch_task("测试", {"msg": "hello"}, workers=["ws_finance"]))
print(result)
"""