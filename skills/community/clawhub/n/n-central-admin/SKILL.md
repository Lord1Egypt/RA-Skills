---
name: n-central-admin
description: Operate N-able N-central safely and efficiently through its web UI. Use when handling device administration, filters, rules, scheduled tasks, automation policies, monitoring associations, remote tools, and tenant/customer/site scoped changes in N-central.
---

# N-central Admin

Use this skill to run reliable browser-driven N-central operations.

## Operating model

Follow this sequence for almost every change:
1. Confirm scope (SO / Customer / Site).
2. Confirm targeting (filter preview or explicit devices).
3. Apply change (rule/task/template/action).
4. Validate on a small sample of devices.
5. Expand scope only after validation.

## Read references only as needed

- Read `references/ui-navigation-and-operating-model.md` for hierarchy, module navigation, and change-control flow.
- Read `references/filters-and-rules.md` for filter expression logic, rule behavior, trigger events, and troubleshooting.
- Read `references/automation-policies-and-tasks.md` for Automation Manager behavior, scheduled task execution, and offline/timing caveats.
- Read `references/device-details-tabs-and-tools.md` for per-device tabs, quick actions, and tool availability expectations.
- Read `references/browser-operator-playbooks.md` for browser execution playbooks and stability patterns.

## Guardrails

- Prefer the narrowest scope that solves the task.
- Clone and specialize shared objects instead of risky in-place edits.
- Name filters/rules/tasks with explicit scope and intent.
- Confirm target count before save and after save.
- Use pilot-first rollout for broad-impact changes.
- Verify outcome using Monitoring, Associations, and Audit Trail.

## Quick dispatch

- If you need left-nav click paths, use `references/ui-navigation-and-operating-model.md#left-navigation-path-map-common-admin-tasks`.
- If rule behavior is wrong, use `references/filters-and-rules.md#rule-not-firing-checklist`.
- If scheduled execution behavior is wrong, use `references/automation-policies-and-tasks.md#offline-and-timing-behavior`.
- If target selector arrows are confusing, use `references/automation-policies-and-tasks.md#dual-list-selector-buttons-targeting-and-similar-fields`.
- If an expected tool is missing on a device, use `references/device-details-tabs-and-tools.md#why-actions-may-be-unavailable`.
- If browser automation gets flaky, use `references/browser-operator-playbooks.md#ui-stability-patterns`.
