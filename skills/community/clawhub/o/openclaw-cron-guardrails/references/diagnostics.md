# Diagnostics and Repair

Use this reference when the user asks why a cron job failed, delivered to the wrong place, or should be repaired without changing its whole shape.

## Triage order

Always inspect in this order:

1. read the existing job
2. inspect recent runs
3. classify the failure
4. fix one dimension at a time
5. verify again

Suggested commands:

```bash
openclaw cron list
openclaw cron runs --id <jobId> --limit 10
```

If safe:

```bash
openclaw cron run <jobId>
```

## Failure buckets

### 1) Delivery-target ambiguity
Signals:
- job ran but nothing showed up where expected
- errors mention missing channel or target
- visible isolated job depended on implicit `last`

Typical fix:
- make delivery explicit
- set `delivery.channel`
- set `delivery.to`
- set `accountId` if the workspace uses multiple accounts

### 2) Auth / permission / provider issue
Signals:
- route looks correct but provider still rejects or fails
- channel/account mismatch
- target exists but is not writable

Typical fix:
- verify target/account pair
- verify channel/provider auth separately

### 3) Timeout too short
Signals:
- runs die at roughly the same short duration
- prompt is clearly heavier than the timeout budget

Typical fix:
- raise `timeoutSeconds` before changing the prompt

### 4) Schedule / timezone issue
Signals:
- job fires at the wrong wall-clock time
- recurring job has no explicit timezone

Typical fix:
- set `tz` explicitly
- verify the intended wall-clock schedule

### 5) Prompt / content issue
Signals:
- the job runs, but the actual content/task is wrong
- delivery is correct, but behavior is not what the user asked for

Typical fix:
- keep routing stable
- edit only the prompt/content side

## Repair rules

### Modify, do not recreate, when:
- only one dimension is broken
- the schedule is right
- the target is right except for one missing field
- the timeout is obviously too short

### Recreate only when:
- the original job shape is fundamentally wrong
- multiple dimensions are inconsistent
- the user wants a different task type entirely

### Refuse unsafe assumptions when:
- the target destination is ambiguous
- current-thread vs explicit external target is unclear
- the user mixes reminder semantics with research/worker semantics without saying which behavior they want

## User-facing explanation style

Prefer short, concrete wording:
- `The timer is fine; the failure is in delivery routing.`
- `This job is visible output, so it should not rely on implicit last-channel resolution.`
- `The task looks heavier than a 60-second timeout.`
- `The schedule is recurring, but timezone is missing, so wall-clock behavior is unstable.`

Avoid vague wording like:
- `The cron seems broken somehow.`
- `Maybe the system didn't understand it.`

## Goal

Diagnosis should reduce uncertainty, not just suggest random edits.
Fix the root cause, then verify.
