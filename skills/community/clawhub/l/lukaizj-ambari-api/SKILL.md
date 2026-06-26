---
name: ambari-api
description: Manage Hadoop clusters via Ambari REST API. Supports service start/stop/restart, component operations, and cluster monitoring. Use when managing Ambari clusters, Hadoop services, or when user mentions Ambari, HDP, HDF, or cluster operations.
---

# Ambari API Management

Manage Hadoop clusters through Ambari REST API (supports Ambari 2.7.5 and 3.0.0).

## Quick Start

```bash
# Install dependencies
pip install -r ~/.claude/skills/ambari-api/scripts/requirements.txt

# Add cluster configuration
python ~/.claude/skills/ambari-api/scripts/ambari_api.py config --add \
  --name prod \
  --url https://ambari.example.com:8080 \
  --username admin \
  --password admin

# List clusters
python ~/.claude/skills/ambari-api/scripts/ambari_api.py clusters --config prod
```

## Core Operations

### Service Management

```bash
# List services in a cluster
python ambari_api.py services --config prod --cluster mycluster

# Start/Stop/Restart a service
python ambari_api.py services --config prod --cluster mycluster --service HDFS --action START
python ambari_api.py services --config prod --cluster mycluster --service YARN --action STOP
python ambari_api.py services --config prod --cluster mycluster --service HIVE --action RESTART
```

### Component Management (Host-Specific)

```bash
# List components on a host
python ambari_api.py components --config prod --cluster mycluster --host node01

# Start/Stop specific component on a host
python ambari_api.py components --config prod --cluster mycluster --host node01 \
  --service HDFS --component DATANODE --action START

python ambari_api.py components --config prod --cluster mycluster --host node01 \
  --service HDFS --component DATANODE --action STOP
```

### Host and Status Operations

```bash
# List all hosts
python ambari_api.py hosts --config prod --cluster mycluster

# Get service status
python ambari_api.py status --config prod --cluster mycluster --service HDFS
```

## Configuration Management

```bash
# List configured clusters
python ambari_api.py config --list

# Remove a cluster configuration
python ambari_api.py config --remove --name prod
```

## API Reference

| Command | Description |
|---------|-------------|
| `config --add` | Add cluster config with URL, username, password |
| `config --list` | List all saved configurations |
| `clusters` | List clusters in Ambari |
| `services` | List services or perform START/STOP/RESTART |
| `hosts` | List hosts in a cluster |
| `components` | List or manage components on specific host |
| `status` | Get detailed service status |

## References

- [API Endpoints](references/api-endpoints.md) - Complete API endpoint reference
- [Examples](references/examples.md) - Common usage patterns
- [Troubleshooting](references/troubleshooting.md) - Common issues and solutions