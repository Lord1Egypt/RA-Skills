---
name: kubernetes-encyclopedia
description: >-
  Kubernetes documentation-first workflow for Kubernetes-specific questions,
  troubleshooting, command planning, cluster operations, workload/resource
  behavior, networking, storage, scheduling, security, and diagnostics. Use
  when the request is clearly about Kubernetes itself: the `kubectl` CLI,
  Kubernetes API objects, pods, deployments, services, ingress, config maps,
  secrets, volumes, nodes, scheduling, RBAC, controllers, CRDs, Helm-free
  core Kubernetes behavior, or cluster/runtime behavior where Kubernetes-
  specific semantics matter. Do not use for generic Linux administration,
  generic container theory, generic cloud architecture, or Docker-only
  questions unless the Kubernetes layer is specifically what is being
  discussed or debugged.
metadata: {"openclaw":{"emoji":"☸️","homepage":"https://kubernetes.io/docs/home/"}}
---

# Kubernetes Encyclopedia

## Overview

Use a docs-first workflow for Kubernetes work. Prefer the official Kubernetes documentation at `https://kubernetes.io/docs/home/`, consult cached local copies under `.Kubernetes-Encyclopedia/` before re-fetching, and record useful official-doc excerpts plus environment-specific operational learnings so future work gets faster and safer.

This skill is for the **Kubernetes API/control-plane/cluster layer**. It should trigger for real Kubernetes behavior, configuration, workload/resource, and operational questions — not for generic Linux admin work, generic container theory, or Docker-only questions where Kubernetes-specific semantics are not the real issue.

## Workflow

1. **Classify the task**
   - Decide whether the task is a Kubernetes question, troubleshooting task, command-planning task, resource review, cluster review, or live operational task.
   - Use this skill when the request is specifically about Kubernetes product behavior, `kubectl` semantics, API resource behavior, workload lifecycle, cluster networking/storage/scheduling/security behavior, or Kubernetes-specific operational details.
   - Do not use this skill for generic shell work, generic Linux admin, generic container theory, or Docker-only questions unless the Kubernetes layer is specifically in play.

2. **Check local cache first**
   - Use `.Kubernetes-Encyclopedia/` as the local knowledge/cache root.
   - Check these locations first when relevant:
     - `.Kubernetes-Encyclopedia/docs/kubernetes.io/docs/...`
     - `.Kubernetes-Encyclopedia/notes/components/...`
     - `.Kubernetes-Encyclopedia/notes/patterns/...`
     - `.Kubernetes-Encyclopedia/inventory/...`
   - If a cached page or note already answers the question well enough, use it.

3. **Consult official Kubernetes docs before answering or touching the system**
   - Before answering direct or indirect Kubernetes questions that depend on command syntax, resource semantics, controller behavior, feature boundaries, configuration semantics, cluster behavior, or version-sensitive details, consult the official docs unless the answer is already well-supported by the local cache.
   - Before performing direct Kubernetes CLI or configuration work, consult the relevant docs first when:
     - the exact resource or command path matters
     - scheduling/networking/storage/security semantics are easy to misremember
     - the action could affect workloads, nodes, access, traffic, storage, policy, or cluster reachability
   - Do not improvise high-impact Kubernetes commands or manifest changes from memory when the docs are easy to check.

4. **Cache consulted docs locally**
   - When you consult a Kubernetes docs page, save a normalized markdown/text cache copy under `.Kubernetes-Encyclopedia/docs/kubernetes.io/docs/...`.
   - Mirror the official docs path structure as much as practical.
   - Cache only pages actually consulted; do not try to mirror the whole docs site eagerly.
   - Use `scripts/cache_doc.py` when appropriate.

5. **Separate official documentation from local observations**
   - Store official-doc-derived material under `.Kubernetes-Encyclopedia/docs/...`.
   - Store environment-specific operational knowledge under:
     - `.Kubernetes-Encyclopedia/notes/components/`
     - `.Kubernetes-Encyclopedia/notes/patterns/`
     - `.Kubernetes-Encyclopedia/inventory/`
   - Distinguish clearly between:
     - official documented behavior
     - observed local configuration/state
     - inferred best-practice guidance

6. **Record useful local learnings**
   - After useful live work, save durable notes such as:
     - cluster-specific topology and access conventions
     - recurring workload/debugging patterns
     - ingress/network-policy/storage-class gotchas
     - scheduling/RBAC/manifest conventions
     - safe/unsafe operational boundaries for the environment
   - Prefer concise durable notes over re-learning the same Kubernetes details later.

## Live Work Rules

- Treat official Kubernetes docs lookup as the default preflight for non-trivial Kubernetes work.
- Prefer read/inspect first when entering a Kubernetes area you have not recently reviewed.
- Treat namespace-wide changes, workload rollouts, storage changes, ingress/service exposure, RBAC/policy changes, and node/control-plane touching operations as high-sensitivity areas.
- When uncertainty remains after checking cache + docs, say so and avoid bluffing.
- When answering a question, mention when useful whether the answer comes from cached official docs, a fresh official docs lookup, or live observed environment state.

## Data Root

Use this workspace-local root for cache and notes:

- `.Kubernetes-Encyclopedia/`

Expected structure:

- `.Kubernetes-Encyclopedia/docs/kubernetes.io/docs/...`
- `.Kubernetes-Encyclopedia/notes/components/...`
- `.Kubernetes-Encyclopedia/notes/patterns/...`
- `.Kubernetes-Encyclopedia/inventory/...`

Use `scripts/init_workspace.py` to create or repair the expected directory structure.

## Note Destinations

- Component-specific observations → `.Kubernetes-Encyclopedia/notes/components/<component-name>.md`
- Reusable Kubernetes patterns/gotchas → `.Kubernetes-Encyclopedia/notes/patterns/<topic>.md`
- Environment-wide deployment/access info → `.Kubernetes-Encyclopedia/inventory/*.md`
- Cached official docs → `.Kubernetes-Encyclopedia/docs/kubernetes.io/docs/...`

## Secrets / Sensitive Data

- Do not store plaintext credentials, API keys, session tokens, private URLs, recovery codes, kubeconfigs, client certificates, bearer tokens, or other secrets in the encyclopedia notes/inventory tree.
- If a note needs to mention access details, keep it high-level and redact or omit secret material.
- Treat these workspace notes as operational memory, not as a secrets vault.

## Resources

- `scripts/init_workspace.py` — create or repair the `.Kubernetes-Encyclopedia/` directory tree.
- `scripts/cache_doc.py` — fetch and cache a consulted official Kubernetes docs page under `.Kubernetes-Encyclopedia/docs/...`.
- `references/workflow.md` — detailed operating workflow and evidence-handling rules.
- `references/cache-layout.md` — canonical `.Kubernetes-Encyclopedia/` directory structure.
- `references/topic-map.md` — useful Kubernetes topic groupings for faster doc lookup.

## Good Outcomes

- Answer a Kubernetes question using cached or freshly checked official docs instead of guesswork.
- Inspect a live Kubernetes environment after checking the relevant docs and record any new local operational knowledge.
- Build a growing local Kubernetes knowledge cache that makes later work faster, safer, and more grounded.
- Turn one-off Kubernetes discoveries into durable notes so future work does not rediscover them from scratch.

## Avoid

- Answering Kubernetes-specific questions purely from memory when docs are easy to consult.
- Treating local observed behavior as if it were guaranteed official documented behavior.
- Dumping large amounts of low-value docs into the workspace without a reason.
- Writing component-specific observations into the official-doc cache tree.
- Making high-impact live changes before checking the relevant docs when exact behavior matters.
