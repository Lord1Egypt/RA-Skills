# 高级用法

**适用场景**: 掌握基础监控后，学习远程监控、数据导出、告警配置、API 集成等高级功能

---

## 一、客户端-服务端模式（远程监控）

### 为什么使用服务端模式？

- 在一台机器上集中查看多台服务器的资源状态
- 通过 SSH 安全隧道传输监控数据
- 适合运维团队监控生产服务器集群

### 启动服务端

**AI执行说明**: AI 可以在远程服务器上启动服务端

```bash
# 在被监控的服务器上启动服务端（默认端口 61209）
glances -s

# 指定监听地址和端口
glances -s --bind 0.0.0.0 --port 61209

# 设置访问密码（推荐在生产环境使用）
glances -s --password

# 后台运行（使用 nohup 或 systemd）
nohup glances -s &
```

### 连接到服务端

**AI执行说明**: AI 可以建立客户端连接并解读远程系统状态

```bash
# 连接到远程服务端（XML-RPC 协议）
glances -c 192.168.1.100

# 指定端口连接
glances -c 192.168.1.100 --port 61209

# 使用密码连接
glances -c 192.168.1.100 --password

# 通过 SSH 隧道安全连接（推荐生产环境）
ssh -f -L 61209:localhost:61209 user@remote-server -N
glances -c localhost --port 61209
```

---

## 二、REST API 模式

### 启动 API 服务

Glances 内置了 REST API，支持通过 HTTP 获取实时系统数据。

**AI执行说明**: AI 可以启动 API 服务并帮助查询数据

```bash
# 启动 Web 服务器（同时提供 Web UI 和 REST API）
glances -w

# 仅启动 API（禁用 Web UI，减少资源占用）
glances -w --disable-webui

# 指定端口和绑定地址
glances -w --bind 0.0.0.0 --port 61208
```

### 常用 API 端点

```bash
# 获取所有插件列表
curl http://localhost:61208/api/3/pluginslist

# 获取 CPU 信息
curl http://localhost:61208/api/3/cpu

# 获取内存信息
curl http://localhost:61208/api/3/mem

# 获取系统负载
curl http://localhost:61208/api/3/load

# 获取磁盘 I/O
curl http://localhost:61208/api/3/diskio

# 获取网络接口信息
curl http://localhost:61208/api/3/network

# 获取进程列表（TOP 进程）
curl http://localhost:61208/api/3/processlist

# 获取 Docker 容器状态
curl http://localhost:61208/api/3/docker

# 获取所有数据（完整快照）
curl http://localhost:61208/api/3/all

# 获取特定字段的值
curl "http://localhost:61208/api/3/cpu/total"
```

**期望输出示例**（CPU 信息）:
```json
{
  "total": 23.4,
  "user": 18.2,
  "system": 3.1,
  "idle": 76.6,
  "nice": 0.0,
  "iowait": 1.8,
  "irq": 0.2,
  "softirq": 0.1
}
```

---

## 三、配置告警阈值

### 创建自定义配置文件

**AI执行说明**: AI 可以根据你的需求生成配置文件

```bash
# 创建配置目录（如不存在）
mkdir -p ~/.config/glances

# 创建配置文件
cat > ~/.config/glances/glances.conf << 'EOF'
[global]
# 刷新间隔（秒）
refresh=2
# 进程列表最大显示数量
process_max=50

[cpu]
# CPU 告警阈值（百分比）
careful=60
warning=80
critical=95

[mem]
# 内存告警阈值（百分比）
careful=60
warning=80
critical=90

[memswap]
# Swap 告警阈值（百分比）
careful=40
warning=60
critical=80

[load]
# 负载告警阈值（CPU 核数的倍数）
careful=0.7
warning=1.0
critical=5.0

[network]
# 网络带宽告警（单位: bit/s）
# 对特定网卡设置阈值
[network_eth0]
rx_careful=10000000
rx_warning=100000000
rx_critical=1000000000
tx_careful=10000000
tx_warning=100000000
tx_critical=1000000000

[fs]
# 磁盘使用率告警（百分比）
careful=60
warning=80
critical=90

[diskio]
# 磁盘 I/O 告警（字节/秒）
# hide=sda1,sdb

[docker]
# Docker 监控配置
max_name_size=20
EOF
```

### 使用自定义配置启动

```bash
# 使用默认配置路径（~/.config/glances/glances.conf）
glances

# 指定配置文件路径
glances --config /path/to/my-glances.conf
```

---

## 四、数据导出

### 导出到 CSV 文件

**AI执行说明**: AI 可以配置数据导出，用于离线分析

```bash
# 持续导出到 CSV 文件（每次刷新追加一行）
glances --export csv --export-csv-file /tmp/glances_metrics.csv

# 仅导出特定指标
glances --export csv --export-csv-file /tmp/cpu_mem.csv \
    --stdout cpu.total,mem.percent

# 静默模式导出（无界面，后台记录）
glances -q --export csv --export-csv-file /var/log/glances/metrics.csv
```

### 导出到 InfluxDB

```bash
# 安装 InfluxDB 客户端
pip3 install influxdb  # InfluxDB v1
pip3 install influxdb-client  # InfluxDB v2

# 配置 InfluxDB 导出（在 glances.conf 中添加）
cat >> ~/.config/glances/glances.conf << 'EOF'

[influxdb]
host=localhost
port=8086
user=root
password=root
db=glances
prefix=localhost
# 每 N 次刷新导出一次（减少写入频率）
interval=1

[influxdb2]
host=localhost
port=8086
org=myorg
bucket=glances
token=mytoken
interval=1
EOF

# 启动并导出到 InfluxDB v1
glances --export influxdb

# 启动并导出到 InfluxDB v2
glances --export influxdb2
```

### 导出到 Prometheus

```bash
# 安装 Prometheus 客户端
pip3 install prometheus_client

# 配置 Prometheus 导出
cat >> ~/.config/glances/glances.conf << 'EOF'

[prometheus]
host=localhost
port=9091
prefix=glances
labels=localhost
interval=1
EOF

# 启动并暴露 Prometheus 指标端点
glances --export prometheus
# 访问: http://localhost:9091/metrics
```

### 导出到 Elasticsearch

```bash
pip3 install elasticsearch

cat >> ~/.config/glances/glances.conf << 'EOF'

[elasticsearch]
host=localhost
port=9200
index=glances
interval=1
EOF

glances --export elasticsearch
```

---

## 五、Docker 容器监控

### 监控 Docker 容器

**AI执行说明**: AI 可以帮助配置 Docker 监控

```bash
# 确保 Docker SDK 已安装
pip3 install docker

# 启动 Glances（会自动检测 Docker）
glances

# 在界面中按 D 键切换 Docker 容器列表显示

# Docker 模式下运行 Glances 监控宿主机（含容器）
docker run -d --restart="always" \
    --name=glances \
    -p 61208-61209:61208-61209 \
    -e GLANCES_OPT="-w" \
    -v /var/run/docker.sock:/var/run/docker.sock:ro \
    --pid host \
    nicolargo/glances:latest
```

---

## 六、以 systemd 服务运行

### 创建 systemd 服务

```bash
# 创建服务文件
sudo tee /etc/systemd/system/glances.service << 'EOF'
[Unit]
Description=Glances system monitor
After=network.target

[Service]
ExecStart=/usr/local/bin/glances -w --disable-webui
Restart=on-failure
RestartSec=10s
User=nobody

[Install]
WantedBy=multi-user.target
EOF

# 重新加载 systemd 配置
sudo systemctl daemon-reload

# 启用并启动服务
sudo systemctl enable glances
sudo systemctl start glances

# 查看服务状态
sudo systemctl status glances

# 查看服务日志
sudo journalctl -u glances -f
```

---

## 七、使用 Python API 集成

### 在 Python 脚本中使用 Glances

**AI执行说明**: AI 可以帮助编写 Glances API 集成脚本

```python
# 通过 REST API 获取数据（无需额外安装）
import requests
import json

BASE_URL = "http://localhost:61208/api/3"

def get_cpu():
    """获取 CPU 使用率"""
    resp = requests.get(f"{BASE_URL}/cpu")
    return resp.json()

def get_mem():
    """获取内存使用率"""
    resp = requests.get(f"{BASE_URL}/mem")
    return resp.json()

def get_top_processes(n=5):
    """获取资源占用最高的 N 个进程"""
    resp = requests.get(f"{BASE_URL}/processlist")
    processes = resp.json()
    # 按 CPU 使用率排序
    return sorted(processes, key=lambda p: p.get('cpu_percent', 0), reverse=True)[:n]

if __name__ == "__main__":
    cpu = get_cpu()
    mem = get_mem()
    print(f"CPU: {cpu['total']:.1f}%")
    print(f"Memory: {mem['percent']:.1f}%")
    print("\nTop 5 Processes (by CPU):")
    for proc in get_top_processes():
        print(f"  {proc['name']:20s}  CPU: {proc['cpu_percent']:.1f}%  MEM: {proc['memory_percent']:.1f}%")
```

---

## 八、告警通知配置

### 配置邮件告警

```bash
cat >> ~/.config/glances/glances.conf << 'EOF'

[alert]
# 启用告警通知
# 注意：需要安装 SNMP 或配置外部脚本

[smtp]
host=smtp.example.com
port=587
user=your@email.com
password=your_password
to=admin@example.com
EOF
```

### 使用 Glances 告警脚本

```bash
# 通过 API 轮询并在超阈值时发出通知（自定义脚本）
cat > /usr/local/bin/glances-alert.sh << 'EOF'
#!/bin/bash
CPU=$(curl -s http://localhost:61208/api/3/cpu/total)
if (( $(echo "$CPU > 90" | bc -l) )); then
    echo "ALERT: CPU usage is ${CPU}%" | mail -s "Server Alert" admin@example.com
fi
EOF
chmod +x /usr/local/bin/glances-alert.sh

# 通过 cron 每分钟检查一次
echo "* * * * * /usr/local/bin/glances-alert.sh" | crontab -
```

---

## 九、常用参数速查表

| 参数 | 说明 | 示例 |
|------|------|------|
| `-w` | 启动 Web 服务器模式 | `glances -w` |
| `-s` | 启动服务端模式 | `glances -s` |
| `-c` | 连接到服务端 | `glances -c 192.168.1.1` |
| `-t N` | 刷新间隔（秒） | `glances -t 5` |
| `-q` | 静默模式（无界面） | `glances -q` |
| `--export` | 启用数据导出 | `glances --export csv` |
| `--stdout` | 输出到标准输出 | `glances --stdout cpu.total` |
| `--count N` | 刷新 N 次后退出 | `glances --count 10` |
| `--config` | 指定配置文件 | `glances --config /path/to/conf` |
| `--disable-plugin` | 禁用指定插件 | `glances --disable-plugin docker` |
| `--process-filter` | 进程名过滤（正则） | `glances --process-filter nginx` |
| `--list-plugins` | 列出所有插件 | `glances --list-plugins` |
| `--bind` | 绑定地址 | `glances -w --bind 0.0.0.0` |
| `--port` | 监听端口 | `glances -w --port 8080` |
| `--username` | 启用用户名认证 | `glances -w --username` |
| `--password` | 启用密码认证 | `glances -w --password` |
| `--disable-webui` | 仅 API，禁用 Web UI | `glances -w --disable-webui` |

---

## 完成确认

### 检查清单

- [ ] 学会启动服务端和客户端模式监控远程主机
- [ ] 成功调用 REST API 获取系统指标
- [ ] 配置了自定义告警阈值
- [ ] 掌握数据导出（CSV / InfluxDB / Prometheus）
- [ ] （可选）配置了 systemd 服务实现开机自启

### 下一步

如遇到问题，查看 [常见问题](../troubleshooting.md)
