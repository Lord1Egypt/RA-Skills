## Description: <br>
Build and review JLCFA/JiaLiChuang FA aluminum alloy enclosure modeling attributes for manufacturable aluminum enclosure designs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhoushoujianwork](https://clawhub.ai/user/zhoushoujianwork) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers, CAD users, and enclosure designers use this skill to turn JLCFA aluminum enclosure requirements into structured modeling attributes and to check openings, holes, finishes, machining choices, and marking details against documented process limits. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Manufacturing values or available JLCFA designer options may change after the referenced material was reviewed. <br>
Mitigation: Verify current JLCFA requirements for expensive, order-critical, or production-critical designs before relying on the generated attributes. <br>
Risk: Generated enclosure attributes may contain inferred dimensions, coordinate assumptions, or process choices when the user request is incomplete. <br>
Mitigation: Review the assumptions, conflicts, fixes, and open questions before converting the guidance into CAD changes or production orders. <br>


## Reference(s): <br>
- [JLCFA Aluminum Alloy Enclosure Reference](references/jlcfa-standards.md) <br>
- [JLCFA help manual](https://www.jlcfa.com/help/44006) <br>
- [JLCFA process parameters](https://ke.jlcfa.com/housing/11) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance] <br>
**Output Format:** [Markdown with JSON-like attribute blocks and concise review notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include assumptions, constraint conflicts, proposed fixes, and open questions for missing production details.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
