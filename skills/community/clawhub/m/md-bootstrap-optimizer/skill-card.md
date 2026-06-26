## Description: <br>
Guides agents and developers in keeping OpenClaw bootstrap Markdown files lean by splitting oversized files, assigning clear rule ownership, and loading detailed procedures only when needed. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[warren2008-2020-spec](https://clawhub.ai/user/warren2008-2020-spec) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent maintainers use this skill to audit and reorganize OpenClaw bootstrap files so permanent rules stay small, detailed procedures load on demand, and archival content does not consume session context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may run sample shell commands without reviewing their local paths. <br>
Mitigation: Review commands before execution; the bundled examples are local read-only audits for Markdown file sizes and counts. <br>
Risk: Misapplying the architecture could move important rules out of always-loaded bootstrap context. <br>
Mitigation: Treat the layer model and size thresholds as guidance, then verify critical rules remain available where the agent needs them. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/warren2008-2020-spec/md-bootstrap-optimizer) <br>
- [Publisher Profile](https://clawhub.ai/user/warren2008-2020-spec) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with bash audit snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes local read-only audit examples, file-size thresholds, and bootstrap organization rules.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
