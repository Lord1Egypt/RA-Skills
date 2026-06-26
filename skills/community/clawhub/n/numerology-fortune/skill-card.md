## Description: <br>
Analyzes numerology profiles using the Pythagorean system, calculating core numbers and personal cycles from a birth date and full legal name with calculation steps shown for verification. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[eamanc-lab](https://clawhub.ai/user/eamanc-lab) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to request Pythagorean numerology readings, including Life Path, Expression, Soul Urge, Personality, Birthday, and personal cycle numbers. The skill is intended for entertainment and personal reflection, not professional advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may save and silently reuse a user's full legal name, birth date, and derived numerology profile. <br>
Mitigation: Ask for explicit consent before writing or reusing MEMORY.md; for one-time readings, instruct the agent not to write memory and delete any existing saved profile data. <br>
Risk: Users could treat numerology interpretations as professional advice. <br>
Mitigation: Present readings as entertainment and personal reflection only, and direct users to qualified professionals for medical, legal, financial, or other major decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/eamanc-lab/numerology-fortune) <br>
- [Publisher profile](https://clawhub.ai/user/eamanc-lab) <br>
- [Project homepage](https://github.com/eamanc-lab/fortune-telling-skills) <br>
- [Numerology Calculation Rules](references/calculation-rules.md) <br>
- [Number Meanings Reference](references/number-meanings.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, files] <br>
**Output Format:** [Markdown numerology report with calculation steps; optional local MEMORY.md profile cache] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires birth date for Life Path and cycle numbers; requires full legal name in English for name-based core numbers.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
