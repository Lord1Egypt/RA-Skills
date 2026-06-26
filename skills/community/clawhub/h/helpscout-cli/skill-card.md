## Description: <br>
CLI for the HelpScout API. Manage conversations, customers, mailboxes, knowledge base articles, and more from the terminal. Covers both Inbox and Docs APIs with full CRUD, PII redaction, permissions, and multiple output formats. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rmorse](https://clawhub.ai/user/rmorse) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Support operators and developers use this skill to have an agent work with the hs CLI for Help Scout Inbox and Docs administration, including conversations, customers, mailboxes, knowledge base articles, reports, and configuration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can manage real Help Scout support data, including conversations, customers, users, knowledge base articles, and reports. <br>
Mitigation: Use least-privilege Help Scout credentials, enable the built-in command allowlist where possible, and require confirmation before destructive or publishing actions. <br>
Risk: Customer or user PII may appear in command output, especially when redaction is disabled or debug output is used. <br>
Mitigation: Configure PII redaction for agent workflows, avoid debug output in shared environments, and review any unredacted output before sharing it. <br>
Risk: The skill depends on the upstream hs CLI installed through the declared brew formula. <br>
Mitigation: Install only if the upstream CLI and distribution source are trusted for the environment. <br>


## Reference(s): <br>
- [Help Scout skill page](https://clawhub.ai/rmorse/helpscout-cli) <br>
- [hs CLI homepage](https://github.com/operator-kit/hs-cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline hs CLI commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The hs CLI supports table, json, json-full, and csv output formats.] <br>

## Skill Version(s): <br>
0.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
