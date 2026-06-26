## Description: <br>
Add a Historical Figures Advisory Board to AI agent personalities with 10 pre-configured personas inspired by public-domain historical figures for strategic advice. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jcrowan3](https://clawhub.ai/user/jcrowan3) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent builders use this skill to define, validate, and compile PersonaNexus identity YAML files with advisory-board personas into prompts and agent configuration formats. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad or poorly scoped board engagement rules can introduce misleading or inappropriate guidance into an agent prompt. <br>
Mitigation: Review and narrow engagement rules before compiling them into agents, especially for sensitive domains. <br>
Risk: Personality-role mappings may be misapplied to consequential human decisions. <br>
Mitigation: Do not use these mappings for hiring, compliance authority, or other consequential decisions about people. <br>
Risk: Unpinned runtime dependencies can change behavior in production. <br>
Mitigation: Use locked dependency versions when deploying this skill in production environments. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/jcrowan3/personanexus-bod) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/jcrowan3) <br>
- [PersonaNexus project homepage](https://github.com/PersonaNexus/personanexus) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration] <br>
**Output Format:** [PersonaNexus YAML validation results, system prompt text, Markdown, JSON/OpenClaw configuration, Anthropic XML-style prompt sections, and CLI command output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [All processing is local; compiled prompts may include advisory-board context, disclaimers, and engagement rules from the input YAML.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
