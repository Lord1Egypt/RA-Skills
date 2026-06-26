# OCP CE Deployment and Takeover

## Terminology

- **OCP CE** (`ocp-ce`): OceanBase Cloud Platform Community Edition — full management platform.
- **`ocp-express`**: Legacy lightweight web console. **Replaced by `obshell dashboard`** (port 2886). Do not deploy `ocp-express` for new setups.
- When users say "deploy OCP" without qualification, always use `ocp-ce`.

## OCP CE Deployment

OCP CE is deployed as a component in the obd config file:

```yaml
ocp-ce:
  servers:
    - <ocp_server_ip>
  global:
    # OCP CE specific parameters
    home_path: /home/admin/ocp-ce
    # ... other parameters per official OCP CE documentation
```

**Important**: `ocp-ce` packages are **not** in the public community mirror by default. Use `obd mirror list` to verify package availability before planning deployment. An internal or separately provided mirror may be required.

## OCP Express Redirect

When users explicitly request `ocp-express`:

> `ocp-express` has been replaced by `obshell dashboard`. Deploy OceanBase CE directly and access the dashboard on port `2886`. There is no need to deploy `ocp-express` separately.

## OCP Takeover

Prepare an OBD-deployed cluster to be managed by a running OCP CE (or enterprise OCP) instance.

### Step 1: Check Conditions
```bash
obd cluster check4ocp <deploy_name> -V <ocp_version>
```

Validates that the cluster meets OCP requirements.

### Step 2: Export to OCP
```bash
obd cluster export-to-ocp <deploy_name> -a <ocp_address> -u <user> -p <password>
```

Registers the cluster with the OCP instance for centralized management.

**Note**: `check4ocp` and `export-to-ocp` target a running OCP CE (or enterprise OCP) control plane, not `ocp-express`.
