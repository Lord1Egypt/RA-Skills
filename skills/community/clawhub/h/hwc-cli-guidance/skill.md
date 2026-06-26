# Huawei Cloud CLI Guidance

## 技能描述

Huawei Cloud CLI Guidance 技能帮助开发者快速安装和使用华为云命令行工具（KooCLI）。KooCLI 是华为云提供的命令行工具，用于调用和管理华为云服务。本技能提供了详细的安装指南、配置说明、常用命令示例和最佳实践。

## 最后更新日期

2026-06-04

---

## 快速开始

### 5分钟快速上手

欢迎使用华为云 KooCLI！本指南将帮助您在 14 分钟内完成安装和配置。

#### 环境准备

1. **系统要求**
   - Windows / macOS / Linux
   - 支持 Python 3.8+ 版本

2. **获取访问密钥**
   - 访问 [华为云控制台](https://console.huaweicloud.com/)
   - 进入"我的凭证"页面
   - 创建访问密钥（Access Key ID 和 Secret Access Key）

#### 安装 KooCLI

**方法一：使用 pip 安装（推荐）**

```bash
pip install huaweicloudsdkcore
pip install huaweicloudsdkkoocli
```

**方法二：使用 curl 安装（Linux/macOS）**

```bash
curl -LO https://dl.koo.cloud/cli/latest/huaweicloud-cli-linux-amd64.tar.gz
tar -xzvf huaweicloud-cli-linux-amd64.tar.gz
sudo mv huaweicloud-cli-linux-amd64 /usr/local/bin/hcloud
```

**方法三：使用 PowerShell 安装（Windows）**

```powershell
Invoke-WebRequest -Uri "https://dl.koo.cloud/cli/latest/huaweicloud-cli-windows-amd64.zip" -OutFile "huaweicloud-cli-windows-amd64.zip"
Expand-Archive -Path "huaweicloud-cli-windows-amd64.zip" -DestinationPath .
```

#### 配置认证信息

```bash
hcloud configure init
```

按提示输入：
- Access Key ID
- Secret Access Key
- Region（如：cn-north-4）

#### 第一个命令

```bash
# 查询云服务器列表
hcloud ecs list-servers

# 查询桶列表
hcloud obs list-buckets
```

---

## 认证说明

### 认证方式

KooCLI 支持多种认证方式：

1. **AK/SK 认证**（推荐）
   - 使用访问密钥（Access Key ID 和 Secret Access Key）
   - 适用于自动化脚本和CI/CD

2. **Token 认证**
   - 使用临时访问令牌
   - 适用于短期访问场景

3. **Profile 配置**
   - 支持多配置文件管理
   - 方便切换不同项目/区域

### 配置管理

**初始化配置**

```bash
hcloud configure init
```

**查看配置**

```bash
hcloud configure list
```

**切换配置**

```bash
hcloud configure set --profile=prod
```

**删除配置**

```bash
hcloud configure delete --profile=test
```

---

## 常用命令

### 云服务器（ECS）

```bash
# 查询云服务器列表
hcloud ecs list-servers

# 查询云服务器详情
hcloud ecs show-server --server-id=xxx

# 启动云服务器
hcloud ecs start-server --server-id=xxx

# 停止云服务器
hcloud ecs stop-server --server-id=xxx

# 重启云服务器
hcloud ecs reboot-server --server-id=xxx
```

### 对象存储（OBS）

```bash
# 查询桶列表
hcloud obs list-buckets

# 创建桶
hcloud obs create-bucket --bucket=my-bucket

# 上传文件
hcloud obs upload-object --bucket=my-bucket --key=example.txt --file=example.txt

# 下载文件
hcloud obs download-object --bucket=my-bucket --key=example.txt --file=example.txt

# 删除文件
hcloud obs delete-object --bucket=my-bucket --key=example.txt
```

### 云数据库（RDS）

```bash
# 查询实例列表
hcloud rds list-instances

# 查询实例详情
hcloud rds show-instance --instance-id=xxx

# 重启实例
hcloud rds restart-instance --instance-id=xxx
```

### 函数计算（FunctionGraph）

```bash
# 查询函数列表
hcloud functiongraph list-functions

# 调用函数
hcloud functiongraph invoke-function --function-urn=xxx
```

### 更多服务

KooCLI 支持华为云所有服务，使用 `hcloud --help` 查看完整列表。

---

## 使用场景

### 场景1：自动化运维

**适用命令**: `hcloud ecs`, `hcloud rds`, `hcloud functiongraph`

**实现步骤**:
1. 配置 AK/SK 认证
2. 编写脚本批量操作资源
3. 集成到 CI/CD 流程

```bash
#!/bin/bash
# 批量启动云服务器
SERVER_IDS=("server-id-1" "server-id-2" "server-id-3")

for id in "${SERVER_IDS[@]}"; do
    hcloud ecs start-server --server-id=$id
    echo "Started server: $id"
done
```

---

### 场景2：批量数据迁移

**适用命令**: `hcloud obs`

**实现步骤**:
1. 创建目标桶
2. 批量上传文件
3. 验证上传结果

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

### 场景3：监控和告警

**适用命令**: `hcloud ces`, `hcloud aom`

**实现步骤**:
1. 查询指标数据
2. 设置告警规则
3. 自动化响应

```bash
#!/bin/bash
# 查询CPU使用率
METRIC_ID="SYS.ECS.CPUUtilization"
INSTANCE_ID="i-xxx"

hcloud ces list-metric-data \
    --metric-name=$METRIC_ID \
    --namespace=SYS.ECS \
    --dimensions.0.name=instance_id \
    --dimensions.0.value=$INSTANCE_ID
```

---

## 最佳实践

### 错误处理

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
```

### 配置管理

```bash
# 多环境配置
hcloud configure init --profile=dev
hcloud configure init --profile=prod

# 使用特定配置
hcloud --profile=dev ecs list-servers
hcloud --profile=prod ecs list-servers
```

### 输出格式

```bash
# JSON 格式
hcloud ecs list-servers --output=json

# Table 格式
hcloud ecs list-servers --output=table

# 自定义字段
hcloud ecs list-servers --query='servers[*].id'
```

---

## 错误处理

### 常见错误

| 错误码 | 含义 | 处理建议 |
|-------|------|---------|
| 401 | 认证失败 | 检查 AK/SK 是否正确 |
| 403 | 权限不足 | 检查 IAM 权限配置 |
| 404 | 资源不存在 | 确认资源 ID 是否正确 |
| 429 | 请求超限 | 降低请求频率 |
| 500 | 服务端错误 | 联系华为云技术支持 |

---

## 参考文档

- [KooCLI 安装指南](https://support.huaweicloud.com/qs-hcli/hcli_02_003.html)
- [KooCLI 用户指南](https://support.huaweicloud.com/ug-hcli/hcli_02_0001.html)
- [KooCLI API 参考](https://support.huaweicloud.com/api-hcli/hcli_01_0001.html)
- [华为云服务文档](https://support.huaweicloud.com/)

---

## 总结

Huawei Cloud CLI Guidance 技能提供了完整的 KooCLI 使用指南：

- ✅ 快速开始：5分钟上手指南
- ✅ 认证说明：AK/SK、Token、Profile 多种认证方式
- ✅ 常用命令：ECS、OBS、RDS、FunctionGraph 等服务
- ✅ 使用场景：自动化运维、批量数据迁移、监控告警
- ✅ 最佳实践：错误处理、配置管理、输出格式
- ✅ 错误处理：常见错误码和处理方法

开发者可以参考本技能文档，快速安装和使用华为云 KooCLI。

---

🎯
