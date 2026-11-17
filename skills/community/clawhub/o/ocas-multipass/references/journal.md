# Journal

Multipass produces journals per spec-ocas-journal.md v1.3. Write a journal at the end of every run. Runs missing journals are invalid.

Journal path: `{agent_root}/commons/journals/ocas-multipass/YYYY-MM-DD/{run_id}.json`

Written atomically (write to `.tmp`, then rename). Never edit after writing.

## Journal types

- **Action Journal** -- written after every `multipass.run`. Records the full session lifecycle, tools resolved, and task outcome.
- **Research Journal** -- written after every `multipass.search`. Records surfaces searched and candidates found, no execution side effects.

## Action Journal structure

```json
{
  "run_identity": {
    "run_id": "r_xxxxxxx",
    "skill_name": "ocas-multipass",
    "skill_version": "4.0.0",
    "journal_type": "action",
    "journal_spec_version": "1.3",
    "timestamp_start": "2026-04-04T10:00:00-07:00",
    "timestamp_end": "2026-04-04T10:04:32-07:00",
    "normalized_input_hash": "sha256:..."
  },
  "runtime": {
    "model": "claude-sonnet-4-6",
    "provider": "anthropic",
    "node": "macstudio-01",
    "max_spawn_depth": 2,
    "parallel_mode": true,
    "mcporter_available": true
  },
  "input": {
    "command": "multipass.run",
    "task_description": "...",
    "normalized_input_hash": "sha256:..."
  },
  "decision": {
    "approach_selected": "A",
    "approach_description": "...",
    "gap_count": 2,
    "candidates_evaluated": 7,
    "reasoning_summary": "..."
  },
  "action": {
    "session_id": "mp_xxxxxxx",
    "session_dir": "{agent_root}/commons/data/ocas-multipass/sessions/mp_xxxxxxx/",
    "tools_resolved": ["skill:author/tool-name", "api:open-meteo"],
    "identity_used": false,
    "side_effect_executed": true
  },
  "artifacts": [
    {"type": "output", "path": "output/result.md"},
    {"type": "replay", "path": "replay.md"},
    {"type": "manifest", "path": "manifest.json"}
  ],
  "metrics": {
    "phases_completed": 4,
    "gaps_total": 2,
    "gaps_resolved": 2,
    "gaps_failed": 0,
    "candidates_tried": 3,
    "circuit_breakers_fired": 0,
    "approach_pivots": 0,
    "identity_used": false,
    "latency_ms": 272000
  },
  "okr_evaluation": {
    "task_status": "complete",
    "approaches_tried": 1,
    "output_produced": true,
    "replay_produced": true,
    "circuit_breakers_fired": 0
  }
}
```

## Research Journal structure

```json
{
  "run_identity": {
    "run_id": "r_xxxxxxx",
    "skill_name": "ocas-multipass",
    "skill_version": "4.0.0",
    "journal_type": "observation",
    "journal_spec_version": "1.3",
    "timestamp_start": "2026-04-04T10:00:00-07:00",
    "timestamp_end": "2026-04-04T10:01:15-07:00",
    "normalized_input_hash": "sha256:..."
  },
  "runtime": {
    "model": "claude-sonnet-4-6",
    "provider": "anthropic",
    "node": "macstudio-01",
    "max_spawn_depth": 2,
    "parallel_mode": true,
    "mcporter_available": true
  },
  "input": {
    "command": "multipass.search",
    "query": "...",
    "normalized_input_hash": "sha256:..."
  },
  "decision": {
    "surfaces_searched": ["mcp-registry", "clawhub", "github"],
    "reasoning_summary": "..."
  },
  "action": {
    "side_effect_intent": null,
    "side_effect_executed": false,
    "reason": "observation_run"
  },
  "artifacts": [
    {"type": "search_results", "path": "{agent_root}/commons/data/ocas-multipass/search_log.jsonl"}
  ],
  "metrics": {
    "surfaces_searched": 3,
    "candidates_found": 8,
    "candidates_above_threshold": 5,
    "latency_ms": 75000
  },
  "okr_evaluation": {
    "task_status": "complete",
    "candidates_found": 8,
    "surfaces_unreachable": 0
  }
}
```
