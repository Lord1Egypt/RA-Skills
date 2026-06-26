# KooCLI 最佳实践

## 1. 认证管理

### 使用多配置文件

```bash
# 开发环境
hcloud configure init --profile=dev

# 生产环境
hcloud configure init --profile=prod

# 使用特定配置
hcloud --profile=dev ecs list-servers
```

---

### 安全存储 AK/SK

**推荐**: 使用环境变量

```bash
export HUAWEICLOUD_SDK_AK="your-access-key-id"
export HUAWEICLOUD_SDK_SK="your-secret-access-key"
```

**不推荐**: 硬编码在脚本中

```bash
# ❌ 不推荐
hcloud configure init
```

---

## 2. 错误处理

### Python 示例

```python
import subprocess
import json

def safe_command(cmd):
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Error: {result.stderr}")
            return None
        return json.loads(result.stdout)
    except Exception as e:
        print(f"Exception: {e}")
        return None

# 使用
servers = safe_command("hcloud ecs list-servers")
if servers:
    print(servers)
```

---

### Bash 示例

```bash
#!/bin/bash

RESULT=$(hcloud ecs list-servers 2>&1)
if [ $? -ne 0 ]; then
    echo "Error: $RESULT"
    exit 1
fi

echo "$RESULT"
```

---

## 3. 批量操作

### 批量启动云服务器

```bash
#!/bin/bash
SERVER_IDS=("server-id-1" "server-id-2" "server-id-3")

for id in "${SERVER_IDS[@]}"; do
    hcloud ecs start-server --server-id=$id
    echo "Started server: $id"
done
```

---

### 批量上传文件

```python
import subprocess
import os

BATCH_SIZE = 100

def batch_upload(bucket, local_dir):
    files = os.listdir(local_dir)
    for i in range(0, len(files), BATCH_SIZE):
        batch = files[i:i+BATCH_SIZE]
        for file in batch:
            cmd = f"hcloud obs upload-object --bucket={bucket} --key={file} --file={local_dir}/{file}"
            subprocess.run(cmd, shell=True)
        print(f"Uploaded batch {i//BATCH_SIZE + 1}")
```

---

## 4. 输出处理

### JSON 输出

```bash
hcloud ecs list-servers --output=json | jq '.servers[].id'
```

---

### Table 输出

```bash
hcloud ecs list-servers --output=table
```

---

### JMESPath 查询

```bash
# 查询所有服务器ID
hcloud ecs list-servers --query='servers[*].id'

# 查询特定字段
hcloud ecs list-servers --query='servers[?name==`test`].{id:id,name:name}'

# 过滤和排序
hcloud ecs list-servers --query='sort_by(servers,&name)[?contains(name,`test`)].name'
```

---

## 5. 限流处理

```python
import time
import random

def request_with_retry(cmd, max_retries=3):
    for attempt in range(max_retries):
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        if result.returncode != 429:
            return result
        
        retry_after = int(result.stderr.split("Retry-After:")[1].strip())
        jitter = random.uniform(0, 1)
        wait_time = retry_after + jitter
        
        print(f"Rate limited, waiting {wait_time:.1f}s...")
        time.sleep(wait_time)
    
    return result
```

---

## 6. 日志记录

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='koocli.log'
)

def log_command(cmd):
    logging.info(f"Executing: {cmd}")
    result = safe_command(cmd)
    if result:
        logging.info(f"Success: {result}")
    else:
        logging.error(f"Failed: {cmd}")
    return result
```

---

## 7. 配置管理

### 配置文件结构

```bash
~/.hcloud/configure
```

**示例**:

```ini
[default]
ak = your-access-key-id
sk = your-secret-access-key
region = cn-north-4

[dev]
ak = dev-access-key-id
sk = dev-secret-access-key
region = cn-north-4

[prod]
ak = prod-access-key-id
sk = prod-secret-access-key
region = cn-south-1
```

---

## 8. CI/CD 集成

### GitHub Actions 示例

```yaml
name: Deploy to Huawei Cloud

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Install KooCLI
        run: |
          curl -LO https://dl.koo.cloud/cli/latest/huaweicloud-cli-linux-amd64.tar.gz
          tar -xzvf huaweicloud-cli-linux-amd64.tar.gz
          sudo mv huaweicloud-cli-linux-amd64 /usr/local/bin/hcloud
          sudo chmod +x /usr/local/bin/hcloud
      
      - name: Configure KooCLI
        run: |
          hcloud configure init --ak=${{ secrets.HUAWEICLOUD_AK }} --sk=${{ secrets.HUAWEICLOUD_SK }} --region=cn-north-4
      
      - name: Deploy
        run: |
          hcloud ecs start-server --server-id=${{ secrets.SERVER_ID }}
```

---

### Jenkins Pipeline 示例

```groovy
pipeline {
    agent any
    
    environment {
        HUAWEICLOUD_AK = credentials('huaweicloud-ak')
        HUAWEICLOUD_SK = credentials('huaweicloud-sk')
    }
    
    stages {
        stage('Install KooCLI') {
            steps {
                sh '''
                    curl -LO https://dl.koo.cloud/cli/latest/huaweicloud-cli-linux-amd64.tar.gz
                    tar -xzvf huaweicloud-cli-linux-amd64.tar.gz
                    sudo mv huaweicloud-cli-linux-amd64 /usr/local/bin/hcloud
                    sudo chmod +x /usr/local/bin/hcloud
                '''
            }
        }
        
        stage('Configure') {
            steps {
                sh '''
                    hcloud configure init --ak=${HUAWEICLOUD_AK} --sk=${HUAWEICLOUD_SK} --region=cn-north-4
                '''
            }
        }
        
        stage('Deploy') {
            steps {
                sh 'hcloud ecs start-server --server-id=xxx'
            }
        }
    }
}
```

---

## 9. 监控和告警

### 查询 CPU 使用率

```bash
#!/bin/bash
METRIC_ID="SYS.ECS.CPUUtilization"
INSTANCE_ID="i-xxx"

hcloud ces list-metric-data \
    --metric-name=$METRIC_ID \
    --namespace=SYS.ECS \
    --dimensions.0.name=instance_id \
    --dimensions.0.value=$INSTANCE_ID \
    --query='datapoints[*].{timestamp:timestamp,average:average}'
```

---

### 设置告警规则

```bash
hcloud ces create-alarm-rule \
    --alarm-name=high-cpu-usage \
    --metric-name=SYS.ECS.CPUUtilization \
    --namespace=SYS.ECS \
    --alarm-action=urn:smn:cn-north-4:xxx:topic:xxx
```

---

## 10. 性能优化

### 并发请求

```python
import concurrent.futures

def start_server(server_id):
    return safe_command(f"hcloud ecs start-server --server-id={server_id}")

with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    futures = [executor.submit(start_server, sid) for sid in SERVER_IDS]
    for future in concurrent.futures.as_completed(futures):
        print(future.result())
```

---

### 缓存结果

```python
from functools import lru_cache

@lru_cache(maxsize=100)
def get_server_detail(server_id):
    return safe_command(f"hcloud ecs show-server --server-id={server_id}")
```

---

## 参考文档

- [KooCLI 用户指南](https://support.huaweicloud.com/ug-hcli/hcli_02_0001.html)
- [华为云服务文档](https://support.huaweicloud.com/)

---

🎯
