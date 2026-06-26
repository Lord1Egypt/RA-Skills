# 数据源接入指南

各类数据源的接入配置说明。

## 关系型数据库

### MySQL / MariaDB

```yaml
data_source:
  type: mysql
  host: "localhost"
  port: 3306
  database: "your_db"
  user: "monitor_user"
  password: "${MYSQL_PASSWORD}"  # 从环境变量读取
  query_timeout: 10  # 秒
```

建议为监控账号只授予 SELECT 权限：
```sql
CREATE USER 'monitor_user'@'%' IDENTIFIED BY 'password';
GRANT SELECT ON your_db.* TO 'monitor_user'@'%';
```

### PostgreSQL

```yaml
data_source:
  type: postgresql
  host: "localhost"
  port: 5432
  database: "your_db"
  user: "monitor_user"
  password: "${PG_PASSWORD}"
  sslmode: "require"
```

### SQL Server

```yaml
data_source:
  type: sqlserver
  host: "localhost"
  port: 1433
  database: "your_db"
  user: "monitor_user"
  password: "${MSSQL_PASSWORD}"
```

## NoSQL 数据库

### MongoDB

```yaml
data_source:
  type: mongodb
  uri: "mongodb://monitor_user:${MONGO_PASSWORD}@localhost:27017/your_db"
  collection: "orders"
  # metric 字段使用 MongoDB aggregation pipeline（JSON 格式）
```

### Redis

```yaml
data_source:
  type: redis
  host: "localhost"
  port: 6379
  password: "${REDIS_PASSWORD}"
  db: 0
  # metric 字段使用 Redis 命令，如 "LLEN queue:orders"
```

### Elasticsearch

```yaml
data_source:
  type: elasticsearch
  hosts: ["https://localhost:9200"]
  api_key: "${ES_API_KEY}"
  index: "logs-*"
  # metric 字段使用 ES Query DSL（JSON 格式）
```

## REST API

```yaml
data_source:
  type: api
  url: "https://api.example.com/metrics"
  method: "GET"
  headers:
    Authorization: "Bearer ${API_TOKEN}"
    Content-Type: "application/json"
  # 支持 JSONPath 提取指标值
  # metric 字段使用 JSONPath，如 "$.data.payment_success_rate"
  timeout: 10
```

### 带请求体的 POST 接口

```yaml
data_source:
  type: api
  url: "https://api.example.com/query"
  method: "POST"
  headers:
    Authorization: "Bearer ${API_TOKEN}"
  body: |
    {
      "metric": "payment_success_rate",
      "start": "now-5m",
      "end": "now"
    }
  metric: "$.result.value"
```

## 消息队列

### Kafka

```yaml
data_source:
  type: kafka
  brokers: ["localhost:9092"]
  topic: "order-events"
  group_id: "monitor-consumer"
  sasl:
    mechanism: "PLAIN"
    username: "${KAFKA_USER}"
    password: "${KAFKA_PASSWORD}"
  # 监控消息积压量（lag）
  metric: "consumer_lag"
```

### RabbitMQ

```yaml
data_source:
  type: rabbitmq
  management_url: "http://localhost:15672"
  user: "${RABBITMQ_USER}"
  password: "${RABBITMQ_PASSWORD}"
  vhost: "/"
  queue: "order-queue"
  # 可监控：messages_ready / messages_unacknowledged / consumers
  metric: "messages_ready"
```

## 日志文件

```yaml
data_source:
  type: log
  path: "/var/log/nginx/access.log"
  format: "combined"  # combined / json / custom
  # metric 字段使用正则表达式或关键词
  metric: "ERROR"  # 统计包含 ERROR 的行数
  window: 300  # 统计最近 N 秒的日志
```

### JSON 格式日志

```yaml
data_source:
  type: log
  path: "/var/log/app/app.log"
  format: "json"
  metric: "$.level == 'error'"  # JSONPath 过滤条件
  window: 300
```

## 云服务监控 API

### 阿里云

```yaml
data_source:
  type: aliyun
  access_key_id: "${ALIYUN_AK}"
  access_key_secret: "${ALIYUN_SK}"
  region: "cn-hangzhou"
  namespace: "acs_rds_dashboard"
  metric_name: "CpuUsage"
  dimensions:
    instanceId: "rm-xxxxxxxx"
```

### 腾讯云

```yaml
data_source:
  type: tencentcloud
  secret_id: "${TENCENT_SECRET_ID}"
  secret_key: "${TENCENT_SECRET_KEY}"
  region: "ap-guangzhou"
  namespace: "QCE/CDB"
  metric_name: "CPUUseRate"
  dimensions:
    InstanceId: "cdb-xxxxxxxx"
```

## 安全建议

- 所有密码和密钥通过环境变量传入，不要硬编码在配置文件中
- 监控账号只授予最小必要权限（只读）
- 生产环境建议使用 SSL/TLS 加密连接
- 定期轮换监控账号密码
