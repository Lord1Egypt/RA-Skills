## Description: <br>
Creates a local HTML slide deck from user-provided presentation content by splitting text into slides and applying a minimalist presentation style. <br>

This skill is for demonstration purposes and not for production usage. <br>

## Publisher: <br>
[qidong](https://clawhub.ai/user/qidong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill authors use this template to prototype PPT-to-HTML generation and create browser-ready slide decks from supplied speech or presentation content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated HTML files can preserve user-provided presentation content on local disk. <br>
Mitigation: Use the skill only with content appropriate for local storage and manage generated files according to the user's retention requirements. <br>
Risk: Untrusted HTML or JavaScript in slide text may be rendered because the skill does not sanitize slide content before writing the presentation. <br>
Mitigation: Avoid untrusted markup and review generated HTML before opening, presenting, or sharing it. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/qidong/ppt-generator-template) <br>
- [Skill Documentation](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Code, Guidance] <br>
**Output Format:** [Browser-ready HTML file and generated file path] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates presentation-<timestamp>.html in the agent's current working directory; slide text is not sanitized before rendering.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
