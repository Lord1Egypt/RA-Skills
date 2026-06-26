## Description: <br>
Complete the first-time setup wizard for a new Mobazha store. Use after deployment to configure admin password, store name, currencies, and profile. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fengzie](https://clawhub.ai/user/fengzie) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Store operators, developers, and deployment agents use this skill after a Mobazha deployment to complete first-time onboarding, including admin password setup, store profile configuration, region and currency settings, and next-step guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive admin passwords and bearer tokens during first-time setup. <br>
Mitigation: Ask for explicit user consent before setting passwords or making API calls, and do not store, log, or display credentials beyond the immediate setup step. <br>
Risk: The security evidence reports a suspicious verdict and warns about broad full-access defaults in a bundled review helper. <br>
Mitigation: Review the bundle before installation and follow the scanner guidance for safer review-helper settings when private code could be involved. <br>


## Reference(s): <br>
- [Mobazha Access Modes](references/access-modes.md) <br>
- [ClawHub listing](https://clawhub.ai/fengzie/mobazha-store-onboarding) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Configuration instructions, API calls, Shell commands] <br>
**Output Format:** [Markdown with inline HTTP examples, JSON bodies, and shell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires explicit user consent before handling admin passwords, bearer tokens, or setup API calls.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
