## Description: <br>
Guides developers through spec-driven CLI workflows with kiro-spec-engine, including project initialization, spec creation, document enhancement, environment checks, and project adoption. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sougannkyou](https://clawhub.ai/user/sougannkyou) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers use this skill to run a KSE CLI workflow for spec-driven development: initializing projects, creating specs, improving requirements and design documents, checking the environment, and validating implementation against acceptance criteria. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow asks users to install an npm CLI globally and run commands that can create or change project files. <br>
Mitigation: Confirm that `kiro-spec-engine` is the intended package, prefer a pinned or project-local install when appropriate, run `kse` only in the intended project, and review files it creates or modifies. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sougannkyou/kse-dev) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and file-path guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose npm and kse CLI commands that modify project files.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
