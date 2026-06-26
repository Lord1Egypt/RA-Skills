---
name: hive-commander
description: 1+5 Distributed Production Swarm with Session Inheritance.
permissions:
  fs:
    read: ["~/.openclaw/skills/**", "~/.openclaw/swarm_tmp/**"]
    write: ["~/.openclaw/swarm_tmp/**"]
  exec: ["python3"]
---

# Skill: Hive-Commander-Kernel (Harness-V2)

## 1. Execution Pipeline

### Phase 1: Sub-task Matrix Generation
Identify the operational mode and map user intent into a 5-node matrix. Assign specialized identities to each node via metadata-driven prompting.

### Phase 2: Session Extraction Protocol
Mandatory extraction of `api_key`, `base_url`, and `model_id`. These parameters **MUST** be injected into the worker configuration to ensure parity with the master session.

### Phase 3: Configuration Serialization
Construct `~/.openclaw/swarm_tmp/task_config.json` adhering to the following Schema:
{
  "session": {"api_key": "str", "base_url": "str", "model": "str"},
  "workers": [{"id": "int", "role": "str", "prompt": "str", "query": "str"}]
}

### Phase 4: Hardware-Accelerated Dispatch
Invoke `python3 ~/.openclaw/skills/hive-commander/executor.py` for parallel execution.
* **Timeout Handling:** 120s per node.
* **Failure Policy:** Revert to synchronous serial execution on error.

### Phase 5: Synthesis & Conflict Audit
Final aggregation of `worker_*.md` outputs. Perform logical de-confliction to ensure the final report is devoid of internal contradictions.

## 2. Hard Constraints
* **Parallelism:** Fixed at 5 Workers.
* **Context Isolation:** Workers **SHALL NOT** share context during the execution phase.
* **Pathing:** Strictly enforced absolute paths within `~/.openclaw/`.