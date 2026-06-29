# Configuration Examples

> Configuration and orchestration examples for common components in Loop Engineering, using pseudo-code style without binding to any specific platform or language.

---

## 1. Automation - Scheduled Trigger

Trigger automation tasks by time cycle, including start conditions, interval strategy, and error handling.

```
automation "daily-health-check" {
    trigger {
        type: "cron"
        schedule: "0 */6 * * *"          # or interval: "6h"
    }
    preconditions: [
        "system.status == 'active'", "last_run.elapsed > 5h",
        "maintenance_mode == false",
    ]
    execution {
        timeout: "10m"
        retry: {
            max_attempts: 3
            backoff: "exponential"       # 1m, 2m, 4m
            on: ["timeout", "network_error"]
        }
    }
    on_failure: {
        log_level: "error"
        notify: ["ops-channel"]
        fallback: "skip"           # skip | retry | halt
    }
    task: "health-check-pipeline"
}
```

* preconditions gate against invalid triggers; backoff prevents cascading failures; fallback controls skip/stop behavior

---

## 2. Worktree - State Management

State structure, read/write, and cleanup strategy for cross-cycle loops.

```
worktree "loop-state" {
    schema: {
        cycle: {
            id: string
            number: integer             # Auto-incrementing sequence number
            status: "running" | "paused" | "completed" | "failed"
        }
        context: {
            cursor: string              # Cursor (last processed position)
            accumulated: []
            checkpoints: {
                "collect": "done" | "pending"
                "transform": "done" | "pending"
                "archive": "done" | "pending"
            }
        }
        metrics: {
            items_processed: integer
            errors_count: integer
            last_error: string | null
        }
    }
    storage: {
        type: "file"
        path: "./worktrees/loop-state.json"
        sync: "on_write"
    }
    cleanup: { max_age: "30d", max_count: 1000, action: "archive" }
}

# Usage pattern
state = worktree.load("loop-state")
state.cycle.number += 1
state.cycle.status = "running"
state.context.cursor = "item-42"
state.context.checkpoints.collect = "done"
state.metrics.items_processed += 1
worktree.save(state)
state.cycle.status = "completed"; worktree.save(state)
```

* cursor supports resume from breakpoint; checkpoints mark completed stages to skip on restart; cleanup prevents unbounded growth

---

## 3. Skills - Module Registration and Orchestration

Define skill interface patterns, registration mechanism, and dynamic invocation.

```
# Skill interface
skill "skill-interface" {
    required: {
        metadata: { name, version, description }
        activate: (context) -> bool
        execute: (input, context) -> result
        validate: (result) -> bool
    }
    optional: {
        setup: () -> void
        teardown: () -> void
        rollback: (context) -> void
    }
}

# Registration
registry "skill-registry" {
    skills: [
        { name: "code-reviewer", priority: 10, path: "./skills/code-reviewer/" },
        { name: "test-runner",   priority: 5,  path: "./skills/test-runner/",
          dependencies: ["code-reviewer"] },
        { name: "deployer",      priority: 20, path: "./skills/deployer/",
          requires_approval: true },
    ]
}

# Dynamic orchestration
pipeline "skill-orchestration" {
    for each skill in registry.skills:
        if skill.activate(context):
            result = skill.execute(input, context)
            if skill.validate(result):
                context.update(result)
                log("[OK] " + skill.name)
            else:
                if skill.rollback: skill.rollback(context)
                log("[X] " + skill.name + " validation failed")
                handle_failure(skill, result)
        else:
            log("[~] " + skill.name + " skipped")
}
```

* priority controls execution order; activate hook lets skills self-determine participation; rollback reverses side effects

---

## 4. Sub-agents - Task Decomposition and Result Aggregation

Master Agent dispatches subtasks, collects results, merges output.

```
master "orchestrator" {
    decompose: (task) -> subtasks[] {
        if task.type == "code-review":
            return [
                {role: "syntax-checker",   input: task.code},
                {role: "style-checker",    input: task.code},
                {role: "security-auditor", input: task.code},
            ]
    }
    dispatch: {
        mode: "parallel"          # parallel | sequential | pipeline
        max_concurrent: 4
        timeout_per_subtask: "5m"
    }
    aggregate: (subtasks, results) -> output {
        merged = initialize_output()
        for each (subtask, result) in zip(subtasks, results):
            if result.status == "success":
                merged.add(subtask.role, result.data)
            elif result.status == "timeout":
                merged.add_warning(subtask.role, "timeout")
            else:
                merged.add_error(subtask.role, result.error)
        merged.status = "failed" if merged.has_critical_errors() else "success"
        return merged
    }
}
subagent "syntax-checker" {
    model: "default"
    toolset: ["read", "exec", "grep"]
    prompt: "Check the given code for syntax errors only."
    output_format: {
        errors: [{line: int, message: string, severity: "error" | "warning"}]
        summary: string
    }
}
subagent "security-auditor" {
    model: "security-specialized"
    toolset: ["read", "grep", "web_search"]
    prompt: "Find vulnerabilities in the given code."
    output_format: {
        vulnerabilities: [{type, severity, location}]
        recommendations: string[]
    }
}
```

* dispatch mode: parallel / sequential / pipeline; output_format constrains structured output; aggregation distinguishes success/timeout/error

---

## 5. Complete Loop System Skeleton

End-to-end example integrating Automation, Worktree, Skills, and Sub-agents.

```
system "code-review-pipeline" {
    loop: {
        type: "persistent"               # persistent | once | count(N)
        max_iterations: 1000
        idle_sleep: "30s"
        error_sleep: "5m"
    }
    logging: {
        level: "info"
        output: ["stdout", "file://./logs/pipeline.log"]
        rotation: "daily"
    }
}

automation "trigger" {
    cron: "*/10 * * * *"
    preconditions: ["worktree.status == 'idle'", "git.repo.has_new_commits()"]
    on_trigger: "pipeline.run()"
}

worktree "state" {
    schema: {
        cycle: { id, number, status }
        git: { last_commit, current_branch }
        queue: { pending: [], processing: [], completed: [] }
    }
    storage: "file://./worktrees/state.json"
}

registry "skills" {
    skills: [
        {name: "git-diff",    priority: 1, path: "./skills/git-diff/"},
        {name: "code-review", priority: 2, path: "./skills/code-review/"},
        {name: "test-runner", priority: 3, path: "./skills/test-runner/"},
        {name: "auto-fix",    priority: 4, path: "./skills/auto-fix/"},
        {name: "deploy",      priority: 5, path: "./skills/deploy/",
         requires_approval: true},
    ]
}

subagents "reviewers" {
    agents: [
        {name: "syntax",   model: "fast",  toolset: ["read", "exec"]},
        {name: "security", model: "smart", toolset: ["read", "web_search"]},
        {name: "style",    model: "fast",  toolset: ["read"]},
    ]
    dispatch: { mode: "parallel", max_concurrent: 3, timeout: "3m" }
}

pipeline "main" {
    steps: [
        { name: "detect-changes", skill: "git-diff", on_failure: "skip_cycle" },
        { name: "review", subagents: "reviewers", input: state.git.diff,
          aggregate: "merge_reviews" },
        { name: "test", skill: "test-runner", depends_on: ["review"] },
        { name: "auto-fix", skill: "auto-fix",
          condition: "review.has_fixable_issues()", on_success: "goto: review" },
        { name: "deploy", skill: "deploy",
          condition: "review.is_approved() AND test.all_passed()",
          requires_approval: true },
    ]
}

error_handling {
    retry: { max_retries: 3, backoff: "exponential" }
    fallback: { on_persistent_error: "escalate", notify: ["ops-channel"] }
    recovery: { on_restart: "resume_from_checkpoint", checkpoint_interval: "every_step" }
}

main {
    load_config("code-review-pipeline")
    worktree.initialize()
    registry.load_all()
    subagents.warm_up()

    while system.loop.should_continue():
        state = worktree.load()
        result = pipeline.run(state)
        worktree.save(state)

        mark = "[OK]" if result.status == "completed" else "[-]" if result.status == "skipped" else "[X]"
        log(mark + " Cycle " + state.cycle.id + " " + result.status)
        sleep(system.loop.idle_sleep)
}
```

---

## Configuration Quick Reference

| Component | Core Responsibility | Key Configuration Items |
|------|----------|-----------|
| Automation | When to trigger the loop | trigger, preconditions, retry, on_failure |
| Worktree | Cross-cycle state storage | schema, storage, cleanup |
| Skills | Reusable capability modules | metadata, activate, execute, validate, rollback |
| Sub-agents | Parallel subtask execution | decompose, dispatch, aggregate, output_format |
| System/Pipeline | Global orchestration and integration | loop, steps, error_handling, logging |