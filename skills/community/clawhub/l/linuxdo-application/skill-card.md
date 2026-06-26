## Description: <br>
Crafts de-AI-ed Chinese registration applications for Linux.do by interviewing the applicant, checking the draft against Linux.do-specific rules, and producing natural plain text for review before submission. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[clarezoe](https://clawhub.ai/user/clarezoe) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and Chinese-speaking applicants use this skill to prepare a Linux.do registration application by answering a short adaptive survey and receiving a concise, natural draft they can review before submission. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is designed to make a platform registration application look self-written and less AI-generated even though the referenced platform rules discourage AI-generated applications. <br>
Mitigation: Use it only as drafting support for truthful, user-provided details; review and edit the final application so it complies with the destination site's rules and does not misrepresent authorship. <br>
Risk: The workflow asks for personal background, discovery path, registration reasons, and planned account use. <br>
Mitigation: Provide only minimal, truthful details needed for the application and avoid sensitive personal information. <br>
Risk: The artifact suggests loading additional related skills before starting, which could broaden behavior beyond this markdown-only workflow. <br>
Mitigation: Do not load extra skills unless the user explicitly chooses them and has reviewed what they do. <br>


## Reference(s): <br>
- [Linux.do Rules & Signals](references/linuxdo-rules.md) <br>
- [De-AI Checklist](references/de-ai-checklist.md) <br>
- [Skill Genie Homepage](https://github.com/Fei2-Labs/skill-genie) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Guidance] <br>
**Output Format:** [Markdown with a plain-text Chinese application in a code block] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Final application targets roughly 80-150 Chinese characters after survey, rule checks, and de-AI polishing.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
