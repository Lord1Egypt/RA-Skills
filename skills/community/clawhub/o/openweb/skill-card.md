## Description: <br>
OpenWeb gives agents typed JSON access to 90+ real websites through the openweb CLI for reading, searching, posting, commenting, messaging, and other site interactions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[imoonkey](https://clawhub.ai/user/imoonkey) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and agents use OpenWeb to inspect available website operations, execute JSON-parameterized site actions, and expand site coverage by capturing and curating additional site packages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: OpenWeb can reuse browser-authenticated sessions and tokens to act on many real website accounts. <br>
Mitigation: Install only when that account access is acceptable; keep write and delete prompts enabled, avoid transact actions, and use test or low-risk accounts for author-mode capture. <br>
Risk: Capture bundles and local OpenWeb data can contain cookies, tokens, HAR traffic, or other sensitive account data. <br>
Mitigation: Treat capture bundles, cookies, tokens, HARs, and OPENWEB_HOME data as sensitive, and restrict sharing or retention of those files. <br>


## Reference(s): <br>
- [OpenWeb homepage](https://getopenweb.com) <br>
- [OpenWeb repository](https://github.com/openweb-org/openweb) <br>
- [ClawHub OpenWeb release](https://clawhub.ai/imoonkey/openweb) <br>
- [CLI Reference](references/cli.md) <br>
- [x-openweb Field Schema](references/x-openweb.md) <br>
- [Troubleshooting](references/troubleshooting.md) <br>
- [Add Site Guide](add-site/guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, JSON, Configuration, Code, Markdown] <br>
**Output Format:** [Markdown guidance with shell commands and JSON CLI input/output; author-mode workflows may produce OpenAPI YAML, TypeScript adapters, examples, and documentation.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [CLI responses over 4096 bytes spill to a temp file; write and delete actions require prompts by default, and transact actions are denied by default.] <br>

## Skill Version(s): <br>
0.1.5 (source: server release metadata, artifact metadata, and target metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
