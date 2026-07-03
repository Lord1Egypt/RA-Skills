## Description: <br>
Audits an entire repository for over-engineering and returns a ranked list of what to delete, simplify, or replace with standard library or native features. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dietrichgebert](https://clawhub.ai/user/dietrichgebert) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to inspect a repository for unnecessary abstraction, dead flexibility, hand-rolled standard library behavior, and other simplification opportunities. It reports ranked findings only and does not apply changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill needs broad read access to inspect a repository for simplification opportunities. <br>
Mitigation: Use it only in workspaces where repository-wide read access is appropriate, and review the reported findings before acting on them. <br>
Risk: The skill explicitly excludes correctness, security, and performance review from its scope. <br>
Mitigation: Route correctness bugs, security issues, and performance concerns to a normal review pass instead of relying on this audit. <br>


## Reference(s): <br>
- [Project homepage](https://github.com/DietrichGebert/ponytail) <br>
- [ClawHub skill page](https://clawhub.ai/dietrichgebert/skills/ponytail-audit) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown text with one ranked finding per line and a final net reduction summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports simplification findings only; it does not edit files.] <br>

## Skill Version(s): <br>
4.8.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
