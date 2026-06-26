## Description: <br>
Verify academic citations against CrossRef, Semantic Scholar, and OpenAlex, detecting AI-hallucinated references, chimeric citations, and suspicious patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PHY041](https://clawhub.ai/user/PHY041) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, students, and editors use this skill to verify BibTeX bibliographies before submission or CI release. It checks citations against public academic databases and reports verified, suspicious, and not-found references. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends citation titles, DOIs, and related bibliography metadata to CrossRef, Semantic Scholar, and OpenAlex. <br>
Mitigation: Use it only when sending that bibliography metadata to public academic APIs is allowed; avoid unpublished, embargoed, client-confidential, or internal bibliographies unless approved. <br>
Risk: Database coverage and free-tier rate limits can produce suspicious or not-found results for legitimate papers, especially grey literature, book chapters, unpublished reports, and records without DOIs. <br>
Mitigation: Manually review suspicious or not-found citations, include DOIs when available, and treat API results as triage rather than final publication authority. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/PHY041/phy-citation-checker) <br>
- [Publisher profile](https://clawhub.ai/user/PHY041) <br>
- [Project homepage](https://github.com/PHY041/claude-skill-citation-checker) <br>
- [Referenced citation-hallucination paper](https://arxiv.org/abs/2501.04181) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Terminal report or JSON summary with citation status, confidence, source matches, red flags, and notes.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Exit codes indicate all verified, not-found citations, or suspicious citations requiring manual review.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
