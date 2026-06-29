# Node Exporter 安装说明

## 自动安装

```bash
bash os_adapters/linux/install_node_exporter.sh
```

## 默认配置

- 监听端口：9182（可通过参数修改）
- 监听地址：`0.0.0.0`（防火墙限制内网访问）
- 采集间隔：Prometheus 默认 15s

## Prometheus 采集配置

在 Prometheus 的 `prometheus.yml` 中添加：

```yaml
scrape_configs:
  - job_name: 'node'
    static_configs:
      - targets:
        - '10.x.x.x:9100'   # 服务器 1
        - '10.x.x.y:9100'   # 服务器 2
```

## 关键指标

| 指标 | 说明 |
|------|------|
| `node_cpu_seconds_total` | CPU 使用时间（按模式分类） |
| `node_memory_MemAvailable_bytes` | 可用内存 |
| `node_filesystem_free_bytes` | 文件系统可用空间 |
| `node_network_receive_bytes_total` | 网络接收字节数 |
| `node_load1` | 1 分钟负载均衡 |
