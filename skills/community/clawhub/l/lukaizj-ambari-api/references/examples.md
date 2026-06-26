# Common Usage Examples

## Multi-Cluster Configuration

```bash
# Configure development cluster
python ambari_api.py config --add \
  --name dev \
  --url https://ambari-dev.example.com:8080 \
  --username admin \
  --password admin123

# Configure production cluster
python ambari_api.py config --add \
  --name prod \
  --url https://ambari-prod.example.com:8080 \
  --username admin \
  --password prodPass456

# List all configurations
python ambari_api.py config --list
```

## Service Operations

### Stop a Service
```bash
python ambari_api.py services --config prod --cluster mycluster \
  --service HDFS --action STOP
```

### Start Multiple Services
```bash
# Start HDFS
python ambari_api.py services --config prod --cluster mycluster \
  --service HDFS --action START

# Start YARN
python ambari_api.py services --config prod --cluster mycluster \
  --service YARN --action START
```

### Restart All DataNodes (Rolling)

```bash
# Get all hosts
python ambari_api.py hosts --config prod --cluster mycluster

# Restart DataNode on each host one by one
for host in node01 node02 node03; do
  python ambari_api.py components --config prod --cluster mycluster \
    --host $host --service HDFS --component DATANODE --action STOP
  # Wait for stopped
  sleep 30
  python ambari_api.py components --config prod --cluster mycluster \
    --host $host --service HDFS --component DATANODE --action START
  # Wait for started
  sleep 30
done
```

## Health Check Script

```bash
#!/bin/bash
# Check all services status

CLUSTER="mycluster"
CONFIG="prod"

echo "=== Service Status ==="
python ambari_api.py services --config $CONFIG --cluster $CLUSTER

echo ""
echo "=== Host Status ==="
python ambari_api.py hosts --config $CONFIG --cluster $CLUSTER
```

## Common Service Restart Order

When restarting multiple services, follow dependency order:

```bash
# 1. ZooKeeper (foundation)
python ambari_api.py services --config prod --cluster mycluster \
  --service ZOOKEEPER --action RESTART

# 2. HDFS
python ambari_api.py services --config prod --cluster mycluster \
  --service HDFS --action RESTART

# 3. YARN
python ambari_api.py services --config prod --cluster mycluster \
  --service YARN --action RESTART

# 4. Hive
python ambari_api.py services --config prod --cluster mycluster \
  --service HIVE --action RESTART

# 5. HBase (if used)
python ambari_api.py services --config prod --cluster mycluster \
  --service HBASE --action RESTART
```

## Component-Level Operations

### Restart a Single DataNode

```bash
# Stop DataNode on specific host
python ambari_api.py components --config prod --cluster mycluster \
  --host node03 --service HDFS --component DATANODE --action STOP

# Verify stopped
python ambari_api.py status --config prod --cluster mycluster --service HDFS

# Start DataNode
python ambari_api.py components --config prod --cluster mycluster \
  --host node03 --service HDFS --component DATANODE --action START
```

### Restart NodeManager

```bash
python ambari_api.py components --config prod --cluster mycluster \
  --host node03 --service YARN --component NODEMANAGER --action STOP

sleep 20

python ambari_api.py components --config prod --cluster mycluster \
  --host node03 --service YARN --component NODEMANAGER --action START
```

## Python API Usage

```python
from ambari_api import AmbariClient

# Create client
client = AmbariClient(
    base_url="https://ambari.example.com:8080",
    username="admin",
    password="admin"
)

# Get services
services = client.get_services("mycluster")
for svc in services:
    print(f"{svc['service_name']}: {svc['state']}")

# Restart a service
result = client.service_action("mycluster", "HDFS", "RESTART")
print(f"Request ID: {result.get('Requests', {}).get('id')}")

# Get components on a host
components = client.get_host_components("mycluster", "node01")
for comp in components:
    print(f"{comp['component_name']}: {comp['state']}")
```