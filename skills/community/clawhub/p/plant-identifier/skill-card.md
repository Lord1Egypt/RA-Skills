## Description: <br>
Identify plants from photos using trait-based analysis, ranked species candidates, follow-up capture guidance, and a reusable local log. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to identify plants from user-supplied photos, compare ranked candidate species, and decide which plant part to photograph next when evidence is incomplete. Users may also save approved local observation notes for recurring plants or wild observations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Plant photos alone may not establish species-level certainty, edibility, toxicity thresholds, or medicinal safety. <br>
Mitigation: Return ranked candidates with explicit uncertainty, avoid safety-critical clearance, and ask for the next best missing plant view when evidence is incomplete. <br>
Risk: Optional observation memory could store sensitive location context if users include precise addresses or private details. <br>
Mitigation: Ask before writing local files, keep notes under ~/plant-identifier/, and avoid saving precise home addresses or unrelated personal information. <br>


## Reference(s): <br>
- [Plant Identifier on ClawHub](https://clawhub.ai/ivangdavila/plant-identifier) <br>
- [Plant Identifier homepage](https://clawic.com/skills/plant-identifier) <br>
- [Publisher profile](https://clawhub.ai/user/ivangdavila) <br>
- [evidence-guide.md](artifact/evidence-guide.md) <br>
- [memory-template.md](artifact/memory-template.md) <br>
- [setup.md](artifact/setup.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, configuration] <br>
**Output Format:** [Markdown guidance with ranked candidates, confidence bands, evidence notes, follow-up photo requests, and optional local observation note templates.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose local files under ~/plant-identifier/ only after user approval.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
