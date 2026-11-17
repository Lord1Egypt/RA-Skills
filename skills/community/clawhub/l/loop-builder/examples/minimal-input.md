# Minimal Input

```text
I want Codex to reproduce a page from a screenshot. We usually spend many
rounds changing it without getting closer. Turn this into a controlled workflow
that I can reuse, but do not edit the project yet.
```

Expected first response:

- recognize a UI visual-match scenario;
- ask only for decision-critical evidence such as the target screenshot,
  current page or code, viewport, allowed scope, and acceptance method;
- stop at `WAITING_FOR_CONTEXT` if that evidence is missing;
- after evidence is available, recommend a `Plan-Execute-Verify` workflow with
  human visual acceptance;
- synthesize a task card and workflow confirmation card;
- wait before generating an executable Prompt or Skill package.

The request does not authorize code changes, Skill installation, commit, push,
or publication.
