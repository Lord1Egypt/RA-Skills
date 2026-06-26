## Description: <br>
Discrete Hamiltonian task dispatch for multi-hop workflows that maps task dependencies as a graph, precomputes reachability matrices, and solves constrained path queries under budget. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[turinfohlen](https://clawhub.ai/user/turinfohlen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to model long task workflows as triples, query valid next steps under a remaining budget, check dependencies, and avoid dead-end execution paths. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Default cache loading can execute code if a crafted .cache file is placed beside a workflow file. <br>
Mitigation: Use the skill only in directories you control, delete existing .cache files before running on downloaded or shared workflow files, and set PATH_DISPATCH_NO_CACHE=1 for untrusted, CI, or multi-user environments. <br>
Risk: The security verdict is suspicious because the cache uses pickle. <br>
Mitigation: Prefer a future version that replaces pickle with a non-executable cache format and pins dependencies. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/turinfohlen/path-dispatch) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/turinfohlen) <br>
- [Skill documentation](artifact/SKILL.md) <br>
- [Dispatch script](artifact/scripts/dispatch.py) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with command examples and plain-text CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs include path, dependency, matrix, and next-hop query results for local workflow files.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
