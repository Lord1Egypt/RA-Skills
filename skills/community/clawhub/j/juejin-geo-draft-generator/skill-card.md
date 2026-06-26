## Description: <br>
Assists with generating Juejin-style technical article drafts from AI-GEO content assets and preparing them for manual review and publication. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ljseeking](https://clawhub.ai/user/ljseeking) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and technical operations teams use this skill to turn local AI-GEO content assets into Juejin-ready article drafts, titles, summaries, tags, and a pre-publication checklist. It supports visible-browser draft filling while keeping final save and publish actions under human control. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated public article content may be inaccurate, over-promotional, or unsuitable for publication. <br>
Mitigation: Review the generated article and publish checklist manually before saving or publishing on Juejin. <br>
Risk: Optional browser automation interacts with a logged-in Juejin draft form. <br>
Mitigation: Use only a visible local browser session, keep login and security prompts manual, and leave final save and publish actions to the user. <br>
Risk: Platform security prompts or risk controls may appear during draft preparation. <br>
Mitigation: Stop automation when CAPTCHA, secondary verification, or risk-control prompts appear and let the user take over manually. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ljseeking/juejin-geo-draft-generator) <br>
- [Publisher Profile](https://clawhub.ai/user/ljseeking) <br>
- [README](artifact/README.md) <br>
- [Automation Safety Rules](artifact/automation/safety_rules.md) <br>
- [Playwright Draft Flow](artifact/automation/playwright_draft_flow.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown files, text metadata, checklists, and optional local Playwright draft-filling guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces article body, Markdown-ready content, title candidates, summary, tags, publish checklist, and draft status for manual review.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and changelog, released 2026-05-12) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
