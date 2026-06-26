# KooCLI 命令参考

## 通用选项

```bash
hcloud [OPTIONS] <SERVICE> <COMMAND> [ARGS]

OPTIONS:
  --help              显示帮助信息
  --version           显示版本信息
  --debug             启用调试模式
  --output=FORMAT     输出格式（json/table）
  --query=EXPRESSION  JMESPath 查询表达式
  --profile=NAME      使用指定配置文件
```

---

## 云服务器（ECS）

### 查询云服务器列表

```bash
hcloud ecs list-servers
```

**参数**:

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| --limit | integer | 否 | 每页数量 |
| --marker | string | 否 | 分页标记 |

**示例**:

```bash
hcloud ecs list-servers --limit=10
```

---

### 查询云服务器详情

```bash
hcloud ecs show-server --server-id=xxx
```

**参数**:

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| --server-id | string | 是 | 服务器ID |

---

### 启动云服务器

```bash
hcloud ecs start-server --server-id=xxx
```

---

### 停止云服务器

```bash
hcloud ecs stop-server --server-id=xxx
```

**参数**:

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| --type | string | 否 | 类型（SOFT/HARD） |

---

### 重启云服务器

```bash
hcloud ecs reboot-server --server-id=xxx
```

---

## 对象存储（OBS）

### 查询桶列表

```bash
hcloud obs list-buckets
```

---

### 创建桶

```bash
hcloud obs create-bucket --bucket=my-bucket
```

**参数**:

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| --bucket | string | 是 | 桶名称 |
| --location | string | 否 | 区域 |

---

### 上传文件

```bash
hcloud obs upload-object --bucket=my-bucket --key=example.txt --file=example.txt
```

**参数**:

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| --bucket | string | 是 | 桶名称 |
| --key | string | 是 | 对象键 |
| --file | string | 是 | 本地文件路径 |

---

### 下载文件

```bash
hcloud obs download-object --bucket=my-bucket --key=example.txt --file=example.txt
```

---

### 删除文件

```bash
hcloud obs delete-object --bucket=my-bucket --key=example.txt
```

---

## 云数据库（RDS）

### 查询实例列表

```bash
hcloud rds list-instances
```

**参数**:

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| --instance-id | string | 否 | 实例ID |
| --name | string | 否 | 实例名称 |

---

### 查询实例详情

```bash
hcloud rds show-instance --instance-id=xxx
```

---

### 重启实例

```bash
hcloud rds restart-instance --instance-id=xxx
```

---

## 函数计算（FunctionGraph）

### 查询函数列表

```bash
hcloud functiongraph list-functions
```

---

### 调用函数

```bash
hcloud functiongraph invoke-function --function-urn=xxx
```

**参数**:

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| --function-urn | string | 是 | 函数URN |
| --event | string | 否 | 事件数据 |

---

## 云监控（CES）

### 查询指标数据

```bash
hcloud ces list-metric-data \
    --metric-name=SYS.ECS.CPUUtilization \
    --namespace=SYS.ECS \
    --dimensions.0.name=instance_id \
    --dimensions.0.value=i-xxx
```

**参数**:

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| --metric-name | string | 是 | 指标名称 |
| --namespace | string | 是 | 命名空间 |
| --dimensions | array | 是 | 维度列表 |

---

## 应用运维管理（AOM）

### 查询事件告警

```bash
hcloud aom list-events
```

---

## 更多服务

KooCLI 支持华为云所有服务，使用以下命令查看完整列表：

```bash
hcloud --help
```

---

## 输出格式

### JSON 格式

```bash
hcloud ecs list-servers --output=json
```

---

### Table 格式

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
```

---

## 配置文件

### 查看配置列表

```bash
hcloud configure list
```

---

### 切换配置

```bash
hcloud --profile=prod ecs list-servers
```

---

## 参考文档

- [KooCLI 命令参考](https://support.huaweicloud.com/api-hcli/hcli_01_0001.html)
- [华为云服务文档](https://support.huaweicloud.com/)

---

🎯
