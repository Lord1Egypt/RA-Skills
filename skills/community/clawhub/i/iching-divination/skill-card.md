## Description: <br>
AI divination tool that combines I Ching hexagram lookup with AI interpretation for questions about fortune, relationships, career, money, business decisions, and general guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jaxint](https://clawhub.ai/user/jaxint) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent builders use this skill to generate I Ching-style hexagrams and concise divination guidance for personal decisions, career, finance, relationships, and business questions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Personal or sensitive questions may be sent to an external AI endpoint. <br>
Mitigation: Clearly disclose third-party transmission and avoid entering private relationship, financial, career, health, or identifying details unless the user is comfortable sending them externally. <br>
Risk: An embedded API key can expose credentials and route usage through a publisher-controlled account. <br>
Mitigation: Remove and rotate the embedded key, then require user-provided credentials or a safer managed provider setup. <br>
Risk: Broad activation around fortune, career, finance, relationships, and business can influence sensitive decisions. <br>
Mitigation: Keep output framed as reflective guidance rather than professional advice, and narrow activation to explicit divination requests. <br>
Risk: Unused tool permissions broaden the skill's operational surface. <br>
Mitigation: Reduce allowed tools to only the operations required for the divination workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jaxint/iching-divination) <br>
- [I Ching overview](https://zh.wikipedia.org/wiki/易经) <br>
- [Sixty-four hexagrams reference](https://www.iching.cn/) <br>
- [Ruan Yifeng I Ching introduction](https://www.ruanyifeng.com/blog/blog_iching.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, code, shell commands, guidance] <br>
**Output Format:** [Chinese prose, formatted Markdown-style text, and JSON-like Python dictionaries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can call an external AI endpoint when AI interpretation is enabled; deterministic hexagram generation is based on the question text.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence; artifact frontmatter says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
