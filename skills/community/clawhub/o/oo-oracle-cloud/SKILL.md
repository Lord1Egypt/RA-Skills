---
name: oo-oracle-cloud
description: "Oracle Cloud Infrastructure (oracle.com). Use this skill for ANY Oracle Cloud Infrastructure request — reading, creating, updating, and deleting data. Whenever a task involves Oracle Cloud Infrastructure, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Oracle Cloud Infrastructure"
  author: "OOMOL"
  version: "1.0.5"
  services: ["oracle_cloud"]
  icon: "https://static.oomol.com/logo/third-party/oracle_cloud.png"
---

# Oracle Cloud Infrastructure

Operate **Oracle Cloud Infrastructure** through your OOMOL-connected account. This skill calls the `oracle_cloud` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Oracle Cloud Infrastructure. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "oracle_cloud" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "oracle_cloud" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `create_subnet` — Create a subnet in a VCN. [write]
- `create_vcn` — Create a virtual cloud network. [write]
- `delete_vcn` — Permanently delete an empty VCN. This is destructive. [destructive]
- `get_compartment_by_name` — Find a direct child compartment by exact name.
- `get_current_tenancy` — Get the tenancy configured on this connection.
- `get_current_user` — Get the IAM user configured on this connection.
- `get_image` — Get a compute image by OCID.
- `get_instance` — Get a compute instance by OCID.
- `get_metrics_data` — Retrieve aggregated OCI Monitoring metric data using an MQL expression.
- `get_network_security_group` — Get a network security group by OCID.
- `get_security_list` — Get a security list by OCID.
- `get_subnet` — Get a subnet by OCID.
- `get_tenancy` — Get a tenancy by OCID.
- `get_vcn` — Get a virtual cloud network by OCID.
- `get_vnic` — Get a VNIC and its assigned IP addresses by OCID.
- `get_vnic_attachment` — Get a VNIC attachment by OCID.
- `instance_action` — Perform one of the instance actions exposed by Oracle's official Compute MCP server.
- `launch_instance` — Launch a compute instance from an image in a subnet. [write]
- `list_alarms` — List Monitoring alarms in a compartment.
- `list_availability_domains` — List availability domains accessible from a compartment or tenancy.
- `list_compartments` — List child compartments, optionally traversing the tenancy subtree.
- `list_images` — List compute images, optionally filtered by operating system.
- `list_instance_agent_command_executions` — List Oracle Cloud Agent command executions for a compute instance.
- `list_instances` — List OCI compute instances in a compartment.
- `list_metric_definitions` — List available OCI Monitoring metric definitions.
- `list_network_security_groups` — List network security groups, optionally filtered by VCN or VLAN.
- `list_security_lists` — List security lists in a compartment, optionally filtered by VCN.
- `list_subnets` — List subnets in a compartment, optionally filtered by VCN.
- `list_subscribed_regions` — List regions to which a tenancy is subscribed.
- `list_vcns` — List virtual cloud networks in a compartment.
- `list_vnic_attachments` — List VNIC attachments in a compartment, optionally for one instance.
- `run_instance_agent_command` — Run a shell or batch script through Oracle Cloud Agent. The script executes on the target host with the agent service account's privileges. [write]
- `terminate_instance` — Permanently terminate a compute instance. This destructive operation cannot be undone. [destructive]
- `update_instance` — Update flexible shape resources for an instance; OCI may restart the instance. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Oracle Cloud Infrastructure state — confirm the exact payload and effect with the user before running.**
- **Actions tagged `[destructive]` remove or overwrite data — always confirm the target and get explicit approval first.**

## First-time setup

These are **one-time** steps — do not repeat them on every call. Run a step only when a command fails for the matching reason.

- **`oo: command not found`** — install the oo CLI (other platforms: <https://cli.oomol.com/install-guide.md>):

  ```bash
  curl -fsSL https://cli.oomol.com/install.sh | bash    # macOS / Linux
  ```

  ```powershell
  irm https://cli.oomol.com/install.ps1 | iex           # Windows PowerShell
  ```

- **Not signed in / authentication error** — sign in to your OOMOL account once:

  ```bash
  oo auth login
  ```

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Oracle Cloud Infrastructure is not connected, or the connection expired or lacks a scope. Connect once (auth type: custom credential) at:

  ```text
  https://console.oomol.com/connections/oracle_cloud
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Oracle Cloud Infrastructure homepage: https://www.oracle.com/cloud/
- API documentation: https://docs.oracle.com/en-us/iaas/Content/API/Concepts/usingapi.htm
