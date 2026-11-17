# Stateful user flow

Read this reference when the user requests a user flow, task flow, wireflow, product flowchart, responsibility-oriented swimlane, or review of a bounded goal-directed interaction.

## Purpose and boundary

A user flow explains how an actor pursues a goal through actions, system responses, decisions, states, permissions, alternatives, failures, and recovery. It is not merely a sequence of screens. Use a journey map for a longitudinal experience across touchpoints and time; use a service blueprint when frontstage and backstage operations are the decision focus.

If no accepted IA exists, create only the minimum semantic substrate required for the flow: relevant actor, goal, objects/content, states, permissions, business rules, and success condition. Mark reversible assumptions and proceed; do not force a complete IA project.

## Flow contract

Define the decision purpose, scope, actor, goal, trigger, entry, preconditions, source version/readiness, and success condition before choosing a visual notation.

Model relevant steps with stable IDs and explicit types:

- user or operator action;
- system response;
- decision;
- object or system state;
- success;
- failure;
- recovery;
- cancellation or exit;
- handoff between actors or systems.

For each consequential transition, preserve the condition, responsible actor, required permission, affected canonical item, state change, and evidence status when relevant. Distinguish the main path, alternatives, errors, recovery, and cancellation. Do not invent backend calls, HTTP methods, screens, or implementation details unless the requested artifact needs them.

An action belongs to a person or operator; a system response belongs to the product or an identified system. Give every decision two or more distinct, plainly labeled outcomes. Model authentication, persistence, synchronization, payment, or onboarding only when the current goal or evidence requires them—never as automatic conversion steps. Cover failure and recovery in proportion to consequence: critical and likely failures need explicit treatment; low-impact edge cases can remain documented risks rather than bloating the main flow.

## Interaction depth

Match depth to the decision:

- task flow: actor goal, actions, decisions, outcomes;
- user flow: task flow plus system responses, states, branches, failure, and recovery;
- wireflow: user flow plus necessary screen context;
- swimlane: responsibility and handoffs across actors or systems;
- state diagram: lifecycle or system-state transitions;
- sequence diagram: time-ordered technical interaction, only when explicitly useful.

These are related views, not mandatory phases. Produce only the requested or decision-useful representation.

## Review

Check:

- the goal, trigger, entry, preconditions, and success condition agree;
- every referenced actor, item, state, and permission exists in the source or is marked Proposed;
- every decision has meaningful outcomes;
- decision outcomes are distinct and their labels explain the condition rather than repeating generic “yes/no” when the meaning would be ambiguous;
- important failures have recovery, safe termination, or a visible unresolved decision;
- cancellation and backtracking preserve state correctly where relevant;
- no unexplained dead ends, unreachable steps, or accidental loops remain;
- system responses make consequences and progress legible;
- role changes and handoffs preserve ownership and access;
- downstream screen choices do not silently rewrite the semantic model;
- changes from the source are classified as allowed adaptation, proposal, semantic drift, or implementation defect.

Do not call a flow validated merely because it is complete or visually polished. Use scenario walkthroughs, expert review, usability testing, operational evidence, or another method matched to the claim. Record which validity layers remain unmeasured.

## Diagram and output

Choose direction and notation for the audience and task. Persian flows may use RTL or vertical direction when clearer. Use distinguishable action, decision, state, failure, recovery, and success nodes; concise labels; labeled decision branches; controlled crossings; and a textual equivalent. Do not allow labels, nodes, arrows, or branch annotations to overlap. Mermaid, a native diagram, table, or structured JSON are delivery formats, not sources of truth. Create a file only when the current conversation requests or accepts one.
