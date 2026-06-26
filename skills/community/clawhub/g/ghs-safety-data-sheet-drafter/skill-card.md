## Description: <br>
Helps SDS authors, EHS managers, industrial hygienists, product stewards, and regulatory-affairs specialists draft a 16-section Safety Data Sheet aligned with OSHA HCS 2024 for a substance or mixture. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[archlab-space](https://clawhub.ai/user/archlab-space) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External SDS authors, EHS managers, industrial hygienists, product stewards, and regulatory-affairs specialists use this skill to assemble a draft OSHA HCS 2024 SDS packet, including label content, trade-secret concentration worksheets, authoring gaps, evidence indexing, and open questions for qualified review. <br>

### Deployment Geography for Use: <br>
United States <br>

## Known Risks and Mitigations: <br>
Risk: The workflow may handle sensitive product formulas, CBI percentages, supplier records, and hazard data. <br>
Mitigation: Use it only in agent environments approved for that information and avoid entering sensitive formulation data into untrusted sessions. <br>
Risk: A generated SDS packet could be mistaken for a final regulatory document. <br>
Mitigation: Treat every output as a draft and require approval by a qualified SDS author, EHS manager, industrial hygienist, or regulatory-affairs reviewer before use or distribution. <br>
Risk: Regulatory deadlines, allowed CBI ranges, and jurisdiction-specific requirements can change. <br>
Mitigation: Verify current OSHA HCS 2024 requirements, deadlines, CBI constraints, and any non-U.S. jurisdictional requirements before relying on the draft. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/archlab-space/ghs-safety-data-sheet-drafter) <br>
- [Skill README](README.md) <br>
- [Skill definition](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown draft packet with structured SDS sections, tables, worksheets, gap lists, and review prompts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are marked as draft material for qualified SDS author, EHS, industrial hygiene, or regulatory-affairs review before use or distribution.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
