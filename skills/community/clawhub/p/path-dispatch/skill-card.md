## Description:

Discrete Hamiltonian task dispatch for multi-hop workflows that maps task dependencies as a graph, precomputes reachability matrices, and solves constrained path queries under budget.

This skill is ready for commercial/non-commercial use.

## Publisher:

[turinfohlen](https://clawhub.ai/user/turinfohlen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to model multi-step task workflows as dependency graphs, query valid next tasks under a remaining budget, and avoid dead-end execution paths. It is suited to agent workflows with long dependency chains or parallel fan-out and fan-in.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Default cache loading can execute code if a malicious adjacent .cache file is present.

Mitigation: Use the skill only in controlled local project directories, do not accept .cache files from untrusted archives or shared folders, and set PATH_DISPATCH_NO_CACHE=1 when processing untrusted inputs.

Risk: The dependency manifest may need correction before broad use.

Mitigation: Review and fix the package dependency manifest before deployment in shared or production environments.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/turinfohlen/skills/path-dispatch)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell command examples, plus command output from matrix, path, query, and deps operations.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are local workflow-dispatch results derived from user-provided triples files.]

## Skill Version(s):

1.0.4 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
