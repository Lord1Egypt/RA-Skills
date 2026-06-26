## Description: <br>
Find, classify, and update hardcoded default-like model references in a repo. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[patrick-erichsen-2](https://clawhub.ai/user/patrick-erichsen-2) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to audit and migrate repository model defaults while avoiding broad replacement of tests, docs examples, catalogs, and compatibility references. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Changing model defaults can affect CI, tests, release workflows, or runtime behavior. <br>
Mitigation: Review the proposed checklist before approving edits, select only intended references, and run the repository's required validation after changes. <br>
Risk: Over-broad replacement could update examples, fixtures, catalogs, or compatibility references that do not control default behavior. <br>
Mitigation: Classify matches semantically and ignore documented noise unless a reference controls an actual default or fallback. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with repository-relative file references and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user review before edits and validation of changed repository surfaces.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
