---
name: pattern-subworkflows
description: Calling one workflow from another via Execute Workflow nodes — tier ordering, ID resolution.
user-invocable: false
---

# Pattern: subworkflows

A "subworkflow" is a workflow called by another workflow via the `n8n-nodes-base.executeWorkflow` node. The callee uses `n8n-nodes-base.executeWorkflowTrigger` as its entry point.

## ID resolution

The caller references the callee by **n8n workflow ID** (not by name). Use the placeholder:

```json
{
  "type": "n8n-nodes-base.executeWorkflow",
  "parameters": {
    "source": "database",
    "workflowId": {
      "__rl": true,
      "value": "{{@env:workflows.<callee-key>.id}}",
      "mode": "id"
    }
  }
}
```

This way the caller hydrates to the correct ID per env (dev/staging/prod).

## Input passing

The callee's Execute Workflow Trigger must declare its expected inputs **OR** use `inputSource: "passthrough"` to accept arbitrary data. The lock primitives ship with `inputSource: "passthrough"`.

## Tier ordering

Sub-workflows must be deployed before their callers. Use `<workspace>/n8n-config/deployment_order.yml`:

```yaml
tiers:
  "Tier 0a: leaves":
    - lock_acquisition
    - lock_release
  "Tier 1":
    - foo  # references lock_acquisition / lock_release
```

`deploy_all.py` walks tiers in alphabetical key order, so name them with leading numbers.

## Publish dependency

In recent n8n versions, activating (publishing) a workflow that uses `executeWorkflow` requires the referenced sub-workflows to be activated/published first. Errors look like:

> Cannot publish workflow: Node "X" references workflow Y which is not published. Please publish all referenced sub-workflows first.

`deploy_all.py` handles this by deploying tiers in order; sub-workflows go in earlier tiers and stay active in dev.
