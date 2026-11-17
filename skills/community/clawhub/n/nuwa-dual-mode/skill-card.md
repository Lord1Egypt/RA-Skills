## Description:

Nuwa Dual Mode helps an agent distill a person or theme into a runnable perspective skill with Persona, Toolkit, or single-mode behavior.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shallinta](https://clawhub.ai/user/shallinta)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill authors use this skill to create or update perspective skills that model a public figure, fictional character, historical person, or methodology as Persona and/or Toolkit modes. The workflow guides source gathering, mode selection, skill structure, checkpoints, validation, and delivery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can request private or sensitive source material and preserve it in generated skill artifacts.

Mitigation: Provide only material you are authorized to use, avoid confidential or third-party personal data, and review generated files before sharing or installing them.

Risk: Generated Persona rules may obscure that responses are AI-generated or may create emotional-companionship concerns.

Mitigation: Review identity-disclosure, attribution, emotional-support, and crisis-support rules in every generated Persona before use.

Risk: The workflow can create and install other skills and package source materials.

Mitigation: Inspect the generated skill directory, run available validation or scanning steps, and confirm uninstall behavior before deployment.

## Reference(s):

- [Checkpoint Protocol](references/checkpoint-protocol.md)
- [Dual Mode Skill Template](references/dual-mode-template.md)
- [Extraction Framework](references/extraction-framework.md)
- [Intent Inference](references/intent-inference.md)
- [Mode Detection Logic](references/mode-detection-logic.md)
- [Single Mode Skill Template](references/single-mode-template.md)
- [Update Existing Skill](references/update-existing-skill.md)
- [Validation Tests](references/validation-tests.md)
- [Workflow Phases](references/workflow-phases.md)
- [Workflow Types](references/workflow-types.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with generated skill files, code snippets, shell commands, and configuration notes.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local skill directories, research notes, templates, and validation reports when the host agent executes the workflow.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
