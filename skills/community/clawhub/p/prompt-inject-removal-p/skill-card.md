## Description: <br>
Prompt Inject Removal helps agents summarize untrusted external content through a hardened prompt that treats embedded instructions as inert data and emits a sanitized factual summary. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[subaru0573](https://clawhub.ai/user/subaru0573) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users can use this skill as a defense-in-depth step before passing web pages, articles, blogs, emails, or files into an agent workflow. It is intended to produce a sanitized summary for review, not to serve as a complete security boundary. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompt-only sanitization can reduce exposure to indirect prompt injection but is not a complete security boundary. <br>
Mitigation: Use it as defense-in-depth and review sanitized summaries before allowing an agent to send messages, edit files, delete data, or take other consequential actions. <br>
Risk: Sanitized output may still contain factual content that leads a downstream agent toward unsafe actions. <br>
Mitigation: Keep downstream tools constrained and require human review before state-changing actions based on untrusted source material. <br>
Risk: The setup script writes files into the selected target directory. <br>
Mitigation: Inspect setup.sh and choose the target directory deliberately before running it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/subaru0573/prompt-inject-removal-p) <br>
- [Metadata homepage](https://clawhub.ai/Quarantiine/prompt-inject-removal) <br>
- [Hardened system prompt](PROMPT.md) <br>
- [Security documentation](references/security.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Concise sanitized summary text, optionally including the marker [INJECTION_ATTEMPT_REMOVED]] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No external API keys are required; summaries should be reviewed before consequential agent actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
