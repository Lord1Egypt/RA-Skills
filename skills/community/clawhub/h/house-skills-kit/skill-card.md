## Description:

house-skills-kit is a Chinese real-estate agent skill kit with role-based skills, transaction and mortgage calculators, sales SOP guidance, and configurable templates for generating brand-specific advisor skills.

This skill is ready for commercial/non-commercial use.

## Publisher:

[danfeistar](https://clawhub.ai/user/danfeistar)

### License/Terms of Use:

Apache-2.0

## Use Case:

Real-estate sales teams, marketers, brokers, channel operators, and buyer-facing advisors use this skill kit to select role-specific workflows, calculate transaction and financing scenarios, follow sales and market-monitoring SOPs, and generate brand-specific advisor skills from configuration.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: The server security summary reports local file-boundary flaws in the generator and installer.

Mitigation: Review the package before installing, run render.py and install.sh only with trusted configurations and generated skill directories, and inspect generated SKILL.md and manifest.json before installation.

Risk: The skill can produce tax, loan, and policy guidance for real-estate decisions.

Mitigation: Verify all tax, loan, and policy outputs against current official sources before using them for real transactions.

Risk: Rendering untrusted YAML could lead to unsafe or misleading generated skill content.

Mitigation: Avoid rendering untrusted YAML and review generated content before deploying it to an agent.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/danfeistar/skills/house-skills-kit)
- [Artifact README](artifact/README.md)
- [Skill overview](artifact/SKILL.md)
- [Calculation toolkit README](artifact/skills/calc-toolkit/README.md)
- [Kunming reference plates](artifact/examples/kunming/references/plates.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with Python command examples, generated SKILL.md files, manifest JSON, and real-estate calculation outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs depend on local configuration files and city rules; transaction, loan, tax, and policy results should be checked against current official sources before real use.]

## Skill Version(s):

1.7.1 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
