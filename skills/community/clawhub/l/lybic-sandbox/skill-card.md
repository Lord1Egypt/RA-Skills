## Description:

Lybic Sandbox is a cloud sandbox built for agents and automation workflows, providing disposable cloud computers for GUI automation, code execution, file operations, network port mapping, and sandbox management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aenjoy](https://clawhub.ai/user/aenjoy)

### License/Terms of Use:

MIT

## Use Case:

Developers and automation engineers use this skill to create and operate Lybic cloud sandboxes, run code or shell commands, automate desktop and Android GUIs, move files, and expose sandbox services through HTTP port mappings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An agent can create, operate, and delete cloud sandboxes, projects, files, and processes through the user's Lybic account.

Mitigation: Use a least-privileged API key, supervise destructive actions, and review commands before deleting projects or sandboxes.

Risk: HTTP port mappings can expose sandbox services to the internet.

Mitigation: Create mappings only for intended services, avoid exposing sensitive local endpoints, and delete mappings when they are no longer needed.

Risk: Credential handling is required through Lybic organization and API key settings.

Mitigation: Provide credentials through environment variables or a managed secret store, avoid hardcoding them in examples or scripts, and prefer a dedicated pinned SDK environment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/aenjoy/skills/lybic-sandbox)
- [Lybic Homepage](https://lybic.ai)
- [Lybic Documentation](https://docs.lybic.cn)
- [Python SDK Reference](https://docs.lybic.cn/en/sdk/python)
- [Sandbox Actions](https://docs.lybic.cn/en/sandbox/action)
- [Code Execution Docs](https://docs.lybic.cn/en/sandbox/code)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown with Python and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include async Python SDK examples, sandbox action JSON snippets, environment variable setup, and operational cleanup guidance.]

## Skill Version(s):

0.1.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
