# Verify: Confirm the Layer That Has Actually Happened

Verification keeps wishes, commands, and logs distinct from results. Every effect has at least five possible states:

1. **Proposed**: a request, recommendation, or command exists;
2. **Accepted**: the executing party explicitly accepted it;
3. **Executed**: a tool, person, or external system performed the operation;
4. **State changed**: an observable change appeared in the target object;
5. **Effect appeared**: that change produced the result originally sought.

Claim each layer with evidence from that layer. A saved file proves the file exists; an API response proves the request completed; one successful sample proves a candidate implementation can work. Understanding, business effect, and stable capability each need their own evidence.

## Choose evidence by object

- documents, pages, and images: open or render them and inspect critical sizes and reading paths;
- code and tools: run relevant tests, boundary samples, and failure paths;
- external systems: read authoritative state or a checkable receipt;
- understanding: seek counterexamples, alternative explanations, and new observations that could overturn it;
- capability: reproduce the intended result on real work and record conditions and failure signals;
- human gain: the person can understand, judge, use, take over, or correct it.

A failed verification can return the system to observation, reorganize capability, change a relation, narrow a claim, or change the goal. Verification enters [update](update.md); work quality is defined in [works](../experience/works.md).
