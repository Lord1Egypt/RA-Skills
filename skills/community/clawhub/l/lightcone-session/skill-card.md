## Description:

Lightcone Session enables manual step-by-step control of Lightcone cloud browser or desktop sessions for precise automation, login workflows, screenshots, page HTML extraction, and command output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eddieogola](https://clawhub.ai/user/eddieogola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill when an agent needs fine-grained, human-supervised browser or desktop automation for multi-step workflows, login sequences, precise clicking and typing, screenshots, HTML extraction, or cloud-computer command output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credential, screenshot, or page HTML exposure during remote browser and desktop sessions.

Mitigation: Use only authorized accounts and sites, avoid entering real secrets unless necessary, and do not capture or share sensitive screenshots or page HTML.

Risk: The debug action can run shell commands inside the cloud computer.

Mitigation: Treat debug as powerful shell access and run only commands that are necessary, authorized, and reviewed before execution.

Risk: Manual remote control can perform unintended clicks, typing, navigation, or form submission.

Mitigation: Take screenshots after navigation and before sensitive actions, verify coordinates and page state, and close sessions when work is complete.

## Reference(s):

- [Lightcone Documentation](https://docs.lightcone.ai)

## Skill Output:

**Output Type(s):** [Text, API Calls, Shell commands, Guidance]

**Output Format:** [Markdown guidance with structured tool-call examples and returned screenshots, HTML, session identifiers, or command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires TZAFON_API_KEY for Lightcone session access]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
