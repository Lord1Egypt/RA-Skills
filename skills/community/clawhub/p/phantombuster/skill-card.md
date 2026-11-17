## Description:

Control PhantomBuster automation agents via API to list agents, launch automations, get output and results, check status, and abort running agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[capt-marbles](https://clawhub.ai/user/capt-marbles)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to control PhantomBuster automations from an agent workflow, including launching configured phantoms, checking run status, retrieving output, aborting runs, and downloading result CSV data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can launch or abort PhantomBuster automations in the user's workspace.

Mitigation: Install only when agent control of the PhantomBuster workspace is intended, and review agent IDs and arguments before launch or abort commands.

Risk: PHANTOMBUSTER_API_KEY authorizes API access to the user's PhantomBuster workspace.

Mitigation: Keep the API key private, scoped according to workspace policy, and stored only in the environment required for the agent session.

Risk: Downloaded result CSVs may contain personal or business-sensitive data.

Mitigation: Handle result files according to platform terms, privacy law, and internal retention and sharing rules.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/capt-marbles/skills/phantombuster)
- [PhantomBuster](https://phantombuster.com)
- [PhantomBuster Workspace Settings](https://phantombuster.com/workspace-settings)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and optional JSON or CSV command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires PHANTOMBUSTER_API_KEY for authenticated PhantomBuster API calls.]

## Skill Version(s):

1.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
