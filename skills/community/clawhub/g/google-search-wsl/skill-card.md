## Description:

Perform Google web and news searches through a Chrome browser running in WSL and controlled through Chrome DevTools Protocol.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jesson-hh](https://clawhub.ai/user/jesson-hh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and agents use this skill to perform Google search, news lookup, and general web research from a WSL environment. It provides setup and browser-control steps for launching Chrome with remote debugging and retrieving page content through snapshots.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Chrome remote debugging exposes broad local browser-control access while the debug browser is running.

Mitigation: Review the skill before installing, use a dedicated throwaway Chrome profile, restrict or change the debugging port and allowed origins where possible, and close Chrome after searches are complete.

Risk: Sensitive browsing data or accounts could be exposed if a shared or signed-in Chrome profile is used for debugging.

Mitigation: Avoid signing into sensitive accounts in the debug browser and keep the debug profile separate from normal browsing profiles.

Risk: The default search language may not match the intended locale.

Mitigation: Override the default zh-CN language setting when a different search locale is needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jesson-hh/skills/google-search-wsl)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command snippets and browser-tool command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Chrome or Chromium in WSL, local Chrome DevTools Protocol access, and an OpenClaw browser tool.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
