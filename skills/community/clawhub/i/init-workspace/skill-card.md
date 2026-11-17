## Description:

Initialize personal and team knowledge bases, create or join teams, create team project spaces, configure Gitea repository permissions, and maintain the AIFusionBot/system-config control repository.

This skill is ready for commercial/non-commercial use.

## Publisher:

[myd2002](https://clawhub.ai/user/myd2002)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and workspace administrators use this skill to onboard users and teams into a Gitea-backed research knowledge-base system, provision private repositories, assign collaborator permissions, and manage team chat bindings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses broad Gitea administrative authority to create and modify private repositories, control-plane JSON files, and collaborator permissions.

Mitigation: Install only in a controlled Gitea instance, restrict who can invoke the skill, use the narrowest viable service token, and audit repository permissions after provisioning.

Risk: The provided environment example uses an HTTP Gitea endpoint, which can expose credentials or administrative actions in transit.

Mitigation: Replace the default endpoint with HTTPS before deployment and rotate any admin token that may have been used with the HTTP endpoint.

Risk: Runtime dependencies are not pinned in the artifact.

Mitigation: Pin and review dependencies before deployment.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash command examples and JSON-producing helper scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return interactive card payloads for supported chat clients.]

## Skill Version(s):

1.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
