# Config File Deployment

Detailed steps for deploying OceanBase CE clusters using configuration files.

## Deploy with Config File

```bash
obd cluster deploy <deploy_name> -c <config_file>
obd cluster start <deploy_name>
```

The config file (YAML) defines components, server addresses, ports, and parameters.

## Interactive Deploy

```bash
obd cluster deploy <deploy_name> -i
```

Guides through configuration interactively. Use when users want step-by-step setup.

## Component Selection

Common components for config files:

| Component | Purpose |
|-----------|---------|
| `oceanbase-ce` | OceanBase database server |
| `obproxy-ce` | OceanBase proxy for load balancing |
| `obagent` | Monitoring agent |
| `ocp-ce` | OCP Community Edition (full management platform) |
| `prometheus` | Metrics collection |
| `grafana` | Metrics visualization |

For OCP, always use `ocp-ce` by default. See [ocp-ce.md](ocp-ce.md) for details.

## Cluster Operations After Deployment

### Edit Config
```bash
obd cluster edit-config <deploy_name>
```
Opens the config in an editor. Changes take effect after `reload`.

### Reload Config
```bash
obd cluster reload <deploy_name>
```
Applies config changes to a running cluster without full restart.

### Upgrade Component
```bash
obd cluster upgrade <deploy_name> -c <component_name> -V <version>
```

### Scale Out
```bash
obd cluster scale_out <deploy_name> -c <config_file>
```
The config file describes the new nodes to add.

### Add / Delete Component
```bash
obd cluster component add <deploy_name> -c <config_file>
obd cluster component del <deploy_name> <component_name>
```

**Deletion order matters**: Components with dependants must be deleted after their dependants. Delete `grafana` and `prometheus` before `obagent`.
