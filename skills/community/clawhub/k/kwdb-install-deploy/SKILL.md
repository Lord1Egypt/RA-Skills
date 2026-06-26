---
name: kwdb-install-deploy
description: Triggered when the user wants to install or deploy KaiwuDB (kwdb, kaiwudb). Helps users complete script-based deployment of KaiwuDB clusters, including configuration file modification, installation command execution, cluster initialization, and status checks.
---

# KWDB Install

## Overview

This skill provides script-based deployment for KaiwuDB, suitable for bare-metal or container deployment in Linux environments. Supports single-replica and multi-replica cluster deployments with complete deployment workflow guidance.

## Mandatory Rules

**The following three rules must be strictly followed:**

### 1. Prohibit Guessing Installation Parameters

**Do not guess or assume any installation parameters and proceed with installation unless explicitly specified by the user.**

- All configuration parameters (ports, IPs, data directories, security modes, etc.) must be confirmed with the user one by one
- Even if the user says "use defaults", the default values must be explicitly listed and confirmed with the user
- The installation package path must be explicitly provided by the user and must not be guessed

### 2. Must Read Logs on Installation Failure

**When the installation command fails, you must read the log files in the `log/` directory under the same path as the installation script to obtain detailed failure information.**

Log file path: `/opt/kaiwudb/<package-name>/log/` or `kaiwudb_install/log/`

```bash
# After installation failure, first read the logs
ls -la log/
cat log/install.log  # or the latest generated log file
```

### 3. Exit After Reporting Failure, Prohibit Arbitrary Retries

**After installation failure, you must:**
1. Clearly display the error information obtained from the logs to the user
2. Explain possible causes
3. Exit the installation process, **do not retry on your own**
4. Wait for user instructions before deciding on the next step

**Exception**: Only when the user explicitly requests "retry", you may execute the installation command again.

## Prerequisites

### System Requirements

- **Hardware**:
  - Memory: At least 8 GB RAM (16 GB recommended)
  - CPU: At least 2 cores (4 cores recommended)
  - Disk: At least 50 GB available space (SSD recommended)
- **Operating System**:
  - CentOS 7/8
  - Ubuntu 18.04/20.04/22.04
- **Network**: All nodes must have network connectivity

### User Permissions

- SSH passwordless login configured between nodes
- User must be `root` or have `sudo` privileges
- For container deployment, non-root users must be in the `docker` group

## Deployment Steps

### Step 1: Confirm Deployment Mode

First, I need to confirm the deployment mode you need:

**Ask**:
"Please select the deployment mode: single-node deployment (single) or cluster deployment (cluster)?"

### Step 1.1: Confirm Cluster Replica Count - Cluster Mode Only

If cluster deployment is selected, I need to further confirm the number of replicas:

**Ask**:
"Please select the cluster deployment type: single-replica cluster (single-replica) or multi-replica cluster (multi-replica)?"

### Step 2: Confirm Installation Package Location

Next, I need to confirm the location of the KaiwuDB installation package with you. The installation package should be a `.tar.gz` file with `KaiwuDB` as the prefix, for example: `KaiwuDB-1.0.0.tar.gz`.

**Ask**:
"Please provide the full path (including filename) of the KaiwuDB installation package. The installation package should be a tar.gz file with KaiwuDB as the prefix, for example /path/to/KaiwuDB-1.0.0.tar.gz."

**Note**: You must wait for the user to provide the exact path and must not guess on your own.

### Step 3: Verify Installation Package

After confirming the installation package location, verify that the file exists and has the correct format:

```bash
# Check if the installation package exists
if [ ! -f "$INSTALL_PACKAGE_PATH" ]; then
    echo "Error: Installation package does not exist, please check if the path is correct"
    exit 1
fi

# Check filename format
if [[ "$(basename $INSTALL_PACKAGE_PATH)" != KaiwuDB*.tar.gz ]]; then
    echo "Error: Installation package filename is incorrect. It should be a tar.gz file with KaiwuDB as the prefix"
    exit 1
fi
```

### Step 4: Extract Installation Package and Configure

```bash
# Create installation directory
sudo mkdir -p /opt/kaiwudb

# Extract installation package
tar -xzf "$INSTALL_PACKAGE_PATH" -C /opt/kaiwudb

# Enter installation directory
cd /opt/kaiwudb/kaiwudb_install
```

### Step 5: Configure deploy.cfg File

I will ask you about each configuration item step by step according to the deployment mode you selected, and then modify the `deploy.cfg` configuration file based on your answers.

**Mandatory**: Unless the user voluntarily says "all defaults" or explicitly specifies parameter values, each item must be confirmed one by one. Even if the user selects default values, the defaults must be displayed and confirmed.

#### Global Configuration (global) - Common to All Modes

1. **Security Mode (secure_mode)**:
   - Ask: "Please select the security mode: insecure (non-secure mode), tls (TLS secure mode, default), tlcp (TLCP secure mode)"

2. **Management User (management_user)**:
   - Ask: "Please enter the KaiwuDB management username (default: kaiwudb)"

3. **RESTful Port (rest_port)**:
   - Ask: "Please enter the KaiwuDB Web service port (default: 8080)"

4. **KaiwuDB Service Port (kaiwudb_port)**:
   - Ask: "Please enter the KaiwuDB service port (default: 26257)"

5. **BRPC Port (brpc_port)**:
   - Ask: "Please enter the KaiwuDB time-series engine communication port (default: 27257)"

6. **Data Directory (data_root)**:
   - Ask: "Please enter the KaiwuDB data storage directory (default: /var/lib/kaiwudb)"

7. **CPU Resource Usage (cpu)**:
   - Ask: "Please enter the proportion of CPU resources occupied by KaiwuDB service (0-1, default: unlimited)"

#### Local Node Configuration (local) - Common to All Modes

8. **Local Node IP Address (local_node_ip)**:
   - Ask: "Please enter the IP address of the local node (used for external services)"
   - **Note**: This parameter has no default value and must be provided by the user

#### Cluster Configuration (cluster) - Cluster Mode Only

9. **Other Cluster Node IP Addresses (cluster_node_ips)**:
   - Ask: "Please enter the IP addresses of other cluster nodes (multiple addresses separated by commas)"

10. **SSH Port (ssh_port)**:
    - Ask: "Please enter the SSH service port of the remote node (default: 22)"

11. **SSH Username (ssh_user)**:
    - Ask: "Please enter the SSH login username for the remote node"

Based on your answers, I will automatically generate the corresponding `deploy.cfg` configuration file. The cluster configuration section will be automatically omitted for single-node deployment.

### Step 6: Execute Installation Command

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

**Important**: Before execution, all configuration parameters must be displayed to the user and confirmed before proceeding.

### Step 7: Confirm Installation Information

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

### Step 8: Handle Installation Failure

**If the installation command execution fails (returns a non-zero exit code), the following operations must be performed:**

```bash
# 1. Enter the log directory
cd log/

# 2. List log files
ls -la

# 3. Read the latest log file (usually install.log or a file with a timestamp)
cat install.log
# or
tail -100 <latest log file>
```

**Report failure information to the user:**

1. Clearly display the error information extracted from the logs
2. Explain possible causes (refer to references/troubleshooting.md)
3. **Exit the installation process, do not retry on your own**
4. Wait for further user instructions

Example report format:
```
Installation failed!

Error information (from logs):
[Specific error content extracted from log/install.log]

Possible causes:
- [Possible causes analyzed based on the error information]

Please check the above issues and let me know if you need to retry or have other instructions.
```

### Step 9: Initialize and Start Cluster - Cluster Mode Only

After successful installation, execute:

```bash
./deploy.sh cluster -i
# or
./deploy.sh cluster --init
```

### Step 10: Check Status

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

### Step 11: Configure Auto-start on Boot (Optional)

```bash
systemctl enable kaiwudb
```

## Resources

### references/
Contains KaiwuDB related documents:

- `installation_guide.md` - Detailed installation guide
- `troubleshooting.md` - Common issues and solutions

### assets/
Contains KaiwuDB configuration file templates and resources:

- `deploy.cfg` - Deployment configuration file template
