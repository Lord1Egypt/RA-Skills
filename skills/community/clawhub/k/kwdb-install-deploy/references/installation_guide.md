# KaiwuDB Script Deployment Guide

## Prerequisites

### System Requirements

- Hardware, operating system, and software dependencies of all nodes to be deployed must meet the installation and deployment requirements.
- **Network Settings**:
  - Network connectivity between all nodes.
  - Nodes are located within the same data center.
  - Network latency between physical machines is no higher than 50 ms.
  - Clock difference between nodes is no greater than 500 ms.
  - Required ports for KaiwuDB service have been reserved on each node.
- KaiwuDB bare-metal or container installation package for the corresponding system version has been obtained.

### User Permissions

- SSH passwordless login is configured between the current node and other nodes in the cluster.
- The installation user is the `root` user or a regular user with `sudo` privileges.
- When deploying with the container installation package, if the installation user is a non-`root` user, add the user to the `docker` group by running `sudo usermod -aG docker $USER`.

## Deployment Steps

### Step 1: Confirm Deployment Mode

First, confirm the deployment mode:

**Ask**:
"Please select the deployment mode: single-node deployment (single) or cluster deployment (cluster)?"

### Step 1.1: Confirm Cluster Replica Count - Cluster Mode Only

If cluster deployment is selected, further confirm the number of replicas:

**Ask**:
"Please select the cluster deployment type: single-replica cluster (single-replica) or multi-replica cluster (multi-replica)?"

### Step 2: Confirm Installation Package Location

Provide the full path of the installation package, including the filename, for example:
```
/path/to/KaiwuDB-1.0.0.tar.gz
```

### Step 3: Extract Installation Package

```bash
# Create installation directory
sudo mkdir -p /opt/kaiwudb

# Extract installation package
tar -xzf "$INSTALL_PACKAGE_PATH" -C /opt/kaiwudb

# Enter installation directory
cd /opt/kaiwudb/$(basename "$INSTALL_PACKAGE_PATH" .tar.gz)
```

### Step 4: Configure deploy.cfg File

I will ask you about each configuration item step by step according to the deployment mode you selected, and then modify the `deploy.cfg` configuration file based on your answers.

#### Global Configuration (global) - Common to All Modes

1. **Security Mode (secure_mode)**:
   - Select the security mode: insecure (non-secure mode), tls (TLS secure mode, default), tlcp (TLCP secure mode)

2. **Management User (management_user)**:
   - Enter the KaiwuDB management username (default: kaiwudb)

3. **RESTful Port (rest_port)**:
   - Enter the KaiwuDB Web service port (default: 8080)

4. **KaiwuDB Service Port (kaiwudb_port)**:
   - Enter the KaiwuDB service port (default: 26257)

5. **BRPC Port (brpc_port)**:
   - Enter the KaiwuDB time-series engine communication port (default: 27257)

6. **Data Directory (data_root)**:
   - Enter the KaiwuDB data storage directory (default: /var/lib/kaiwudb)

7. **CPU Resource Usage (cpu)**:
   - Enter the proportion of CPU resources occupied by KaiwuDB service (0-1, default: unlimited)

#### Local Node Configuration (local) - Common to All Modes

8. **Local Node IP Address (local_node_ip)**:
   - Enter the IP address of the local node (used for external services)

#### Cluster Configuration (cluster) - Cluster Mode Only

9. **Other Cluster Node IP Addresses (cluster_node_ips)**:
   - Enter the IP addresses of other cluster nodes (multiple addresses separated by commas)

10. **SSH Port (ssh_port)**:
    - Enter the SSH service port of the remote node (default: 22)

11. **SSH Username (ssh_user)**:
    - Enter the SSH login username for the remote node

Based on your answers, I will automatically generate the corresponding `deploy.cfg` configuration file. The cluster configuration section will be automatically omitted for single-node deployment.

### Step 5: Execute Installation Command

Execute the corresponding installation command based on your selection:

**Single-node deployment**:
```bash
./deploy.sh install --single
```

**Single-replica cluster deployment**:
```bash
./deploy.sh install --single-replica
```

**Multi-replica cluster deployment**:
```bash
./deploy.sh install --multi-replica
```

### Step 6: Confirm Installation Information

After checking that the configuration is correct, enter `Y` or `y`. If you need to return to modify the configuration file, enter `N` or `n`.

```shell
================= KaiwuDB Basic Info =================
Deploy Mode: bare-metal
Management User: kaiwudb
Start Mode: single
RESTful Port: 8080
KaiwuDB Port: 26257
BRPC Port: 27257
Data Root: /var/lib/kaiwudb
Secure Mode: tls
CPU Usage Limit: 1
Local Node Address: 192.168.122.221
=========================================================
Please confirm the installation information above(Y/n):
```

### Step 7: Initialize and Start Cluster - Cluster Mode Only

```bash
./deploy.sh cluster -i
# or
./deploy.sh cluster --init
```

### Step 8: Check Status

**Check service status**:
```bash
systemctl status kaiwudb
```

**Check cluster status (cluster mode only)**:
```bash
./deploy.sh cluster -s
# or
./deploy.sh cluster --status
# or use the convenience script
kw-status
```

### Step 9: Configure Auto-start on Boot (Optional)

```bash
systemctl enable kaiwudb
```

## Status Check Description

Field descriptions returned by the `kw-status` command:

| Field | Description |
|-------|-------------|
| `id` | Node ID |
| `address` | Node address |
| `sql_address` | SQL address |
| `build` | KaiwuDB version |
| `started_at` | Start time |
| `updated_at` | Update time |
| `is_available`/`is_live` | Node status, both `true` indicates normal |

## Deployment Modes

### Bare-metal Deployment

Use the `KaiwuDB-baremetal-*.tar.gz` installation package for deployment.

### Container Deployment

Use the `KaiwuDB-container-*.tar.gz` installation package for deployment. Ensure Docker is installed and configured.
