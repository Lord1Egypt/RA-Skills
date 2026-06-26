## Description: <br>
Draws a four-card Tarot spread using local cryptographic randomness and maps the result to a concrete next-step recommendation for ambiguous or low-stakes planning decisions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kc0bfv](https://clawhub.ai/user/kc0bfv) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents use this skill to break ties when a user gives an ambiguous, nonchalant, or explicitly fate-based request and multiple reasonable approaches exist. It is intended as a creative nudge for low-stakes planning, not as a substitute for clear requirements, safety review, or production judgment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Tarot-style randomness can produce misleading confidence if used for security, data integrity, production, financial, or other high-stakes decisions. <br>
Mitigation: Use the reading only for low-stakes ambiguous choices; for consequential decisions, ask for requirements, apply domain review, and rely on explicit user control. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/kc0bfv/let-fate-decide) <br>
- [Interpretation Guide](references/INTERPRETATION_GUIDE.md) <br>
- [Major Arcana Card Meanings](cards/major.md) <br>
- [Wands Card Meanings](cards/wands.md) <br>
- [Cups Card Meanings](cards/cups.md) <br>
- [Swords Card Meanings](cards/swords.md) <br>
- [Pentacles Card Meanings](cards/pentacles.md) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Text, Guidance] <br>
**Output Format:** [JSON from the draw script followed by Markdown or plain-text interpretation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Draws four cards by default; output is nondeterministic and intended for low-stakes tie-breaking.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
