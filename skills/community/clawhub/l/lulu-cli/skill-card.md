## Description:

Manage LuLu macOS firewall rules from the command line for reviewing blocked connections and adding, deleting, enabling, disabling, or reloading firewall rules.

This skill is ready for commercial/non-commercial use.

## Publisher:

[woop](https://clawhub.ai/user/woop)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to diagnose LuLu-blocked outbound connections and manage allow or block rules for macOS firewall policy. It is most relevant when an agent or operator needs auditable command-line guidance for reviewing recent blocks, applying rule changes, and reloading LuLu.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill gives an agent broad sudo authority to make persistent LuLu firewall rule changes through an unpinned third-party CLI.

Mitigation: Install only when agent-administered firewall management is intended, verify the Homebrew tap and installed binary, and review every sudo lulu-cli command before execution.

Risk: Over-permissive global allow-all rules for agent-reachable tools can weaken LuLu as a data-exfiltration boundary.

Mitigation: Avoid global allow-all rules for node, python, curl, git, gh, browser automation, or other tools an agent can use to reach the internet; prefer domain-specific allowlists.

Risk: Reloading LuLu restarts the system extension and creates a brief gap in filtering.

Mitigation: Apply reloads deliberately after reviewing rule changes and account for the temporary filtering gap described by the artifact.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/woop/skills/lulu-cli)
- [Objective-See LuLu](https://objective-see.org/products/lulu.html)
- [Command Reference](references/commands.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include sudo lulu-cli commands that require operator review before execution.]

## Skill Version(s):

0.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
