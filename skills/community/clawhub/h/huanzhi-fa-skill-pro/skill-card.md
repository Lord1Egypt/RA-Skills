## Description: <br>
A Chinese-first fundraising advisor for founders that diagnoses financing readiness, analyzes term-sheet risks, and provides Capital EQ negotiation and emotional-support guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ai-innopower](https://clawhub.ai/user/ai-innopower) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External founders and startup operators use this skill to assess fundraising readiness, interpret investor terms, prepare negotiation responses, and track financing progress. It is oriented toward Chinese-language startup fundraising scenarios and should not replace professional legal, accounting, investment, or financial advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks users to provide sensitive founder profiles, BP materials, diagnosis history, and term-sheet context that may be stored locally under data/users/. <br>
Mitigation: Use redacted materials when possible, confirm how locally stored files are deleted, and avoid confidential uploads until storage and deletion expectations are clear. <br>
Risk: Fundraising, investment, legal, and financial guidance may be incomplete, stale, or unsuitable for a user's specific deal. <br>
Mitigation: Treat outputs as decision support only and review important financing, term-sheet, legal, tax, or accounting decisions with qualified professionals. <br>
Risk: The security evidence notes broad triggers, scheduled follow-ups, and inconsistent audit claims in the artifact. <br>
Mitigation: Review reminder and follow-up behavior before use, disable it where inappropriate, and rely on the marketplace security status rather than artifact audit claims. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/ai-innopower/huanzhi-fa-skill-pro) <br>
- [Xiaping Coze distribution page](https://xiaping.coze.com/skill/b8e65963-a64b-4ffe-87ab-f85a31c615a4) <br>
- [Output schemas](references/outputs-schema.md) <br>
- [Configuration guide](references/config-guide.md) <br>
- [Known limitations](references/known-limitations.md) <br>
- [Failure handling](references/failure-handling.md) <br>
- [Knowledge base](references/knowledge-base.md) <br>
- [Response templates](references/response-templates.md) <br>
- [Determinism details](references/determinism-details.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown-style Chinese responses with structured sections, plus JSON payloads for fundraising diagnosis and term-sheet analysis.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes local profile and progress configuration, deterministic scoring paths, output validation with one retry, and fallback guidance for failure cases.] <br>

## Skill Version(s): <br>
2.9.4 (source: server release evidence; artifact frontmatter and skill.json show 2.9.3) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
