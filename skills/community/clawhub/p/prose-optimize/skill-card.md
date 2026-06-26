## Description: <br>
Optimizes OpenProse workflows by reducing unnecessary LLM API calls when writing or modifying .prose files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[norci](https://clawhub.ai/user/norci) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenProse workflow authors use this skill to audit .prose files, replace simple LLM-mediated steps with Python or native control flow, and merge LLM calls only when context dependencies allow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Running local Python command examples without review could execute project-specific code with unintended behavior. <br>
Mitigation: Review local scripts before execution and run examples in an appropriate workspace. <br>
Risk: Merging or replacing LLM steps can remove intermediate context, validation, or safeguards from an OpenProse workflow. <br>
Mitigation: Check context dependencies and validate workflow outputs after optimization. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/norci/prose-optimize) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code] <br>
**Output Format:** [Markdown guidance with inline prose and bash/prose code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and grep for the command examples shown by the skill.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
