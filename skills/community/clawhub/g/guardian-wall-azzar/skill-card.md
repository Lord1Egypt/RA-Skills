## Description: <br>
Mitigate prompt injection attacks, especially indirect ones from external web content or files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1999AZZAR](https://clawhub.ai/user/1999AZZAR) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to sanitize untrusted web, file, or uploaded text before an agent processes it, flagging common prompt-injection patterns and recommending isolated delimiters for external content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompt-injection detections are heuristic and may miss novel or obfuscated attacks. <br>
Mitigation: Use Guardian Wall as one defensive layer, keep untrusted content isolated with unique delimiters, and review high-stakes content before an agent acts on it. <br>
Risk: Audit sub-agents may receive sensitive external content during high-stakes review. <br>
Mitigation: Send sensitive content to an audit sub-agent only in an appropriately constrained environment. <br>


## Reference(s): <br>
- [Prompt injection pattern reference](artifact/references/patterns.md) <br>
- [Guardian Wall ClawHub release page](https://clawhub.ai/1999AZZAR/guardian-wall-azzar) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with inline command references and plain-text sanitizer output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The sanitizer reports cleaned text and warning labels for detected prompt-injection indicators.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
