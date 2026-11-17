---
name: interaction-design-sop
version: "0.1.0"
license: Apache-2.0
description: "Frontend interaction resilience & defense SOP for engineering implementation. Covers 7-step pre-coding interaction checklist: user intent & task friction reduction, P0/P1/P2 information hierarchy triage, 4-state resilience (empty, loading, error, destructive confirmation), perceived performance (optimistic UI, skeletons), power user shortcuts, and layout resilience trade-offs. Use when: implementing UI views/forms/dashboards in code, designing component interaction logic, handling edge cases and states, or conducting frontend UX resilience reviews. Keywords: 交互细节, 状态设计, 边界情况, 异常处理, 交互审查, 骨架屏, 乐观更新, 防错设计, interaction design, edge cases, error state, empty state, loading state, UI review, UI resilience."
metadata:
  openclaw:
    emoji: ⚡
---

# Interaction Design SOP — Frontend Engineering Resilience Framework

A rigorous pre-coding interaction resilience & defense SOP for frontend engineers and interaction designers. Focuses on interface completeness, error resilience, and edge-case handling before writing code.

> [!NOTE]
> **System Collaboration Guidelines**:
> - **Product UX Lifecycle**: For end-to-end product design (user scenarios, business metrics, journey maps, and wireframe prototypes), refer to `product-ux-workflow`.
> - **Component Implementation**: For code implementations, consult `custom-ui-spec` (for headless components like shadcn/ui and Radix) or `ui-framework-spec` (for pre-built libraries like Ant Design and Element Plus).



When designing a UI, work through these 7 steps before writing code. Each step constrains the next — decisions compound, so get the early steps right.

## Step 1: Intent & Context

Define **who** is using this and **what** they're trying to accomplish. If you can't state the primary goal in one sentence, you don't understand the task yet.

- What specific scenario brings the user to this interface?
- What is the single most important action they need to complete?

Output: a clear user scenario and the one primary goal. Reject feature creep at this stage — secondary goals come later.

## Step 2: Task Flow Optimization (Friction Reduction)

Map the happy path from entry to completion. Then cut it.

- List every click, decision, and input the user must make
- Eliminate steps: smart defaults, pre-fill from context, merge multi-step forms into one
- A step that can be automated should be automated

Target: the minimum number of actions to complete the primary goal. Each remaining step must justify its existence.

## Step 3: Information Architecture

Triage every piece of information into three tiers:

**P0 — Vital.** The content users spend 80% of their time on. Gets the best screen real estate, largest visual weight, and appears without any user action. If you had only one screenful to show, this is what stays.

**P1 — Secondary.** Supporting context and actions. Available without hunting, but never competes with P0 for attention. Smaller, lower contrast, positioned around P0.

**P2 — Progressive.** Edge-case settings, advanced options, low-frequency data. Hidden behind disclosure: collapsible sections, hover tooltips, "advanced" toggles, or secondary tabs. Default: hidden.

For each piece of data on the screen, assign a tier. If you can't decide, it's P2.

## Step 4: Resilience & Edge Cases

Design for three states every view must handle:

**Empty state.** What shows when there's no data? A blank screen is a dead end. Show a clear next action — a create button, sample data, or an inline prompt. The user should know exactly what to do next.

**Error state.** What shows when the network drops or the API fails? Never show a raw error. Provide a human-readable message, a retry action, and preserve any user input so they don't lose work. Consider offline fallback.

**Loading state.** What shows while data fetches? Skeleton screens for content areas, spinner for short actions, progress bar for uploads. Never flash a blank screen then suddenly populate — that feels broken.

**Destructive actions.** Identify every action that can't be undone (delete, overwrite, bulk operations). Each needs at minimum a confirmation step. For truly catastrophic actions, require the user to type the entity name to confirm.

## Step 5: Perceived Performance & Power Users

Speed is a feature, not a metric. Optimize for perceived speed even when actual latency exists:

- **Optimistic UI:** Show the expected result immediately, then reconcile. Works for likes, toggles, quick edits. Roll back on failure.
- **Skeleton screens:** Show layout structure instantly while data loads. Beats a spinner — gives users something to scan.
- **Prefetching:** Load data the user will likely need next (hover-triggered prefetch, route-based prefetch).

For power users, add keyboard shortcuts for the top 3-5 actions. Consider whether a Cmd+K command palette is warranted for discoverability.

## Step 6: Trade-off Critique

Before writing code, stress-test the design against three perspectives:

- **Layout resilience:** Does it break with very long text? 320px-wide viewport? Right-to-left languages? High-contrast mode? 200% font size?
- **Power user experience:** Can an expert drive this entirely by keyboard? Can they batch-operate? Is there a shortcut for the thing they do 50 times a day?
- **Novice experience:** Would a first-time user know what to do within 5 seconds? Is complexity unnecessarily exposed? Is there a guided path?

Then make a deliberate trade-off: what did you sacrifice and why? Document it. "It's simple because we dropped bulk-edit" is a decision; "it's complex because we added everything" is an abdication.

## Step 7: Output

Produce the actual UI implementation. The format depends on the task:

- **Standalone page/component:** working React/Vue/HTML code with proper states
- **System design:** component tree, data flow diagram, route structure
- **Design review:** annotated screenshots or a written audit against the 6 steps above

Whatever the format, it must handle the empty, loading, error, and destructive-action states defined in Step 4.

## Execution Rules

1. Work through all 7 steps in order. Skipping steps produces fragile designs.
2. Every step must produce a concrete artifact — not just agreement, but specific decisions.
3. P0 content gets the best real estate. P2 content starts hidden. This is non-negotiable.
4. Every view must define its empty, loading, and error states. A view without all three is incomplete.
