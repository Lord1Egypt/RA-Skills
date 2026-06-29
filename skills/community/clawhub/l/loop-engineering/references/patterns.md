# Common Loop Patterns

> Reusable loop patterns in Loop Engineering, each with applicable scenarios, workflow, and key points.

---

## 1. Patrol Loop

**Applicable scenarios:** System health monitoring, periodic data validation, scheduled patrols

**Core idea:** Wake up at fixed intervals, check a batch of conditions, execute actions only when conditions are met, stay silent otherwise.

```
loop patrol:
    sleep(interval)
    for each checkpoint in checkpoints:
        state = check(checkpoint)
        if state != healthy:
            trigger_alert(checkpoint, state)
            take_action(checkpoint, state)
        else:
            log("OK: " + checkpoint)
```

**Key points:**

* Interval should not be too short (waste resources) or too long (miss alerts)
* Checkpoints should cover critical metrics, avoid excessive monitoring that creates noise
* Recommend using a state machine: healthy -> degraded -> critical, with tiered responses
* Health baselines must be clearly defined; vague conditions cause false positives/negatives

---

## 2. Collect-Transform-Archive

**Applicable scenarios:** Data collection pipelines, log aggregation, ETL tasks, information source aggregation

**Core idea:** Three loosely-coupled phases, each independently replaceable, with localized retry on failure.

```
loop pipeline:
    raw = collect(sources)
    if raw is empty: sleep(backoff); continue

    processed = transform(raw)
    for each item in processed:
        if validate(item):
            archive(item)
        else:
            dead_letter_queue.push(item)
```

**Key points:**

* The three phases have clear responsibilities and should not be coupled (collector does not care how data is stored)
* Archive must use idempotent writes to avoid redundant data from duplicate collection
* dead_letter_queue is a required component; abnormal data must not be silently discarded
* Backoff strategy prevents excessive requests to collection sources

---

## 3. Observe-Alert-Remediate

**Applicable scenarios:** Operations automation, self-healing systems, service reliability assurance

**Core idea:** Complete feedback loop -- detect anomalies -> auto-remediate -> verify -> escalate if irreparable.

```
loop observe_alert_remediate:
    anomaly = detect(metrics)
    if anomaly is None: sleep(interval); continue

    alert(anomaly)
    result = remediate(anomaly)

    if result == SUCCESS:
        verify_result = recheck(anomaly)
        if verify_result == OK:
            log("Fixed: " + anomaly)
        else:
            escalate(anomaly, "verification failed")
    else:
        escalate(anomaly, "remediation returned " + result)
```

**Key points:**

* Remediation actions must include a verification step; fixing without verifying is equivalent to not fixing
* Automated remediation should have boundaries (whitelist operations) to avoid making things worse
* Escalate paths should be tiered: log -> notify -> human intervention
* Record the full context of each remediation for post-mortem analysis

---

## 4. Batch Processing Queue

**Applicable scenarios:** Task queue consumption, Worktree-driven batch processing, async workflows

**Core idea:** Enqueue and consume are decoupled, supporting multiple concurrent Workers with centralized result aggregation.

```
loop batch_queue:
    # Enqueue
    for each task in discover_tasks(source):
        queue.enqueue(task)

    # Consume
    workers = spawn_workers(N)
    results = []
    while queue.not_empty() or workers.any_busy():
        for each worker in workers:
            if worker.idle() and queue.not_empty():
                worker.assign(queue.dequeue())
            if worker.done():
                results.append(worker.collect())
                worker.reset()

    # Aggregate
    report = aggregate(results)
    cleanup(workers)
```

**Key points:**

* Task idempotency -- the same task may be consumed multiple times
* Set task timeouts to prevent a single task from blocking the entire queue
* Classify results during aggregation: success / failure / timeout
* Queue must be persistent to prevent task loss on process crash

---

## 5. Goal-Driven Exploration

**Applicable scenarios:** Typical /goal scenarios, autonomous Agent tasks, open-ended problem solving

**Core idea:** plan-act-observe loop, continuing until a verifiable completion condition is met or max iterations reached.

```
loop goal_driven:
    while not goal_met and iterations < max_iterations:
        plan = decompose(goal, context)
        action = select_next_action(plan, context)
        result = execute(action)
        observation = observe(result)

        context = update_context(observation)
        if observation.indicates_goal_met():
            goal_met = True
        elif observation.indicates_dead_end():
            backtrack(context)

    if goal_met:
        report_success(context)
    else:
        report_partial(context, "max iterations reached")
```

**Key points:**

* Goal must be verifiable -- with clear judgment criteria, not a vague "do well"
* A backtrack mechanism is needed; not all paths lead to the goal
* Set max_iterations to prevent infinite loops; return the best result so far on timeout
* Each iteration's observation should be recorded, forming a traceable execution trail

---

## 6. Multi-Agent Deliberation

**Applicable scenarios:** Code review, proposal evaluation, creative generation and filtering, quality assurance

**Core idea:** Multiple Agents play different roles, generate -> cross-review -> iterate and improve -> converge.

```
loop deliberation:
    # Generate
    proposals = []
    for each role in roles:
        proposals.append(role.generate(topic, constraints))

    # Cross-review + iterate
    for round in 1..max_rounds:
        feedbacks = []
        for each role in roles:
            for each proposal in proposals:
                if proposal.author != role:
                    feedbacks.append(role.review(proposal, criteria))

        if all_feedbacks_approved(feedbacks): break

        for each proposal in proposals:
            proposal.revise(feedbacks.for(proposal))

    return select_best(proposals, criteria)
```

**Key points:**

* Role design should be differentiated (radical, conservative, user perspective, security audit)
* Review criteria should be defined upfront to avoid endless debate
* Set max_rounds to prevent infinite iteration; typically 2-3 rounds is enough to converge
* select_best can use voting, weighted scoring, or chairperson adjudication

---

## 7. Incremental Build

**Applicable scenarios:** Code change awareness, incremental processing, hot reload, continuous integration

**Core idea:** Detect changes -> compute impact scope -> process only affected parts -> verify.

```
loop incremental_build:
    changed = detect_changes(since_last_build)
    if changed is empty: sleep(poll_interval); continue

    scope = compute_impact(changed, dependency_graph)
    if scope is empty: continue

    build_order = topo_sort(scope)
    for each module in build_order:
        result = build(module)
        if result != SUCCESS:
            rollback(module)
            notify_failure(module, result)
            break

    if all_built:
        verify(scope)
        deploy(scope)
```

**Key points:**

* dependency_graph is the core data structure that determines the accuracy of incremental computation
* Change detection granularity determines efficiency: file-level < function-level < module-level
* Build failures must have a clear rollback/recovery strategy
* since_last_build state must be persisted; it must not be lost after restart

---

## 8. Self-Healing

**Applicable scenarios:** Service self-recovery, automatic fault handling, degradation and circuit breaking

**Core idea:** Detect faults -> attempt recovery by escalating strategies -> escalate on each failure -> verify after recovery.

```
loop self_healing:
    fault = detect_fault(system)
    if fault is None: sleep(health_check_interval); continue

    recovery_plan = [
        {level: "retry",     action: restart_service},
        {level: "degrade",   action: enable_fallback},
        {level: "rollback",  action: revert_last_change},
        {level: "escalate",  action: notify_human},
    ]

    for step in recovery_plan:
        if fault.resolved(): break
        result = step.action(fault)
        if result == SUCCESS:
            fault.check_resolved()
        if step.level == "escalate": break

    if not fault.resolved():
        critical_alert(fault)
    else:
        log("Self-healed: " + fault)
        record_incident(fault, recovery_plan)
```

**Key points:**

* Recovery strategies are ordered by risk from low to high: retry -> degrade -> rollback -> notify
* Each recovery level must be verified; do not assume "executed = fixed"
* Record a complete incident report for post-mortem root cause analysis
* circuit breaker is a common prerequisite component for self-healing

---

## Pattern Selection Guide

| Scenario | Recommended Pattern | Rationale |
|----------|----------|------|
| Scheduled health checks, monitoring alerts | Patrol Loop | Timer-triggered + conditional checks, low overhead, suitable for routine monitoring |
| Data collection, log aggregation | Collect-Transform-Archive | Loosely-coupled pipeline, each phase independently replaceable |
| Operations automation, service self-healing | Observe-Alert-Remediate | Complete feedback loop, auto-remediation + escalation path |
| Async tasks, batch processing | Batch Processing Queue | Decoupled enqueue and consume, horizontally scalable Workers |
| Open-ended exploration, autonomous Agent | Goal-Driven Exploration | plan-act-observe loop, supports backtrack |
| Code review, proposal evaluation | Multi-Agent Deliberation | Multi-role cross-review, eliminates single-perspective blind spots |
| CI/CD, hot reload, incremental processing | Incremental Build | Process only changed parts, avoid full rebuild |
| Auto fault recovery, circuit breaking, degradation | Self-Healing | Tiered recovery strategy, verify at each level |
| Complex systems (multi-pattern combination) | Combined use | Patrol detects anomaly -> Self-Healing remediates -> Pipeline processes |

**Combination suggestions:**

* Patrol Loop + Self-Healing: Patrol detects anomalies and directly triggers the self-healing process
* Collect-Transform-Archive + Incremental Build: After collection, determine processing scope based on incremental impact
* Goal-Driven Exploration + Multi-Agent Deliberation: Multi-role review of key decisions during exploration
* Batch Processing Queue + Observe-Alert-Remediate: Queue consumption anomalies trigger the monitoring alert loop