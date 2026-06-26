## Description: <br>
Transform raw AI output into platform-ready content with proper formatting, metadata, and cleanup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TheShadowRose](https://clawhub.ai/user/TheShadowRose) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Content creators, writers, marketers, developers, and teams use Output Forge to convert existing AI-generated or plain-text drafts into platform-ready blog posts, newsletters, social posts, Markdown, LaTeX, HTML, and plain-text files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Default cleanup can remove AI-origin statements, uncertainty caveats, browsing limits, training cutoff notes, or other disclosures that may be required by policy, academic rules, workplace rules, or law. <br>
Mitigation: Review output before publishing and disable cleanup with --no-clean when those caveats are relevant or required. <br>
Risk: Generated HTML or LaTeX from untrusted input may include unsafe or unsuitable content for sensitive systems. <br>
Mitigation: Inspect and sanitize generated HTML or LaTeX before pasting it into publishing tools, admin panels, or production workflows. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/TheShadowRose/output-forge) <br>
- [Publisher Profile](https://clawhub.ai/user/TheShadowRose) <br>
- [README](artifact/README.md) <br>
- [Limitations](artifact/LIMITATIONS.md) <br>
- [License](artifact/LICENSE.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, HTML, LaTeX, plain text, social-thread text, configuration JSON, and command-line guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports local file, stdin, stdout, and batch-directory workflows; default cleanup can be disabled with --no-clean.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
