## Description:

Diagnoses enterprise business-process efficiency constraints with the IDC COMPASS framework, identifies priority Agent entry points, and maps supplier directions using IDC MarketGlance categories.

This skill is ready for commercial/non-commercial use.

## Publisher:

[seanlandtop](https://clawhub.ai/user/seanlandtop)

### License/Terms of Use:

MIT-0 distribution; IDC methodology, MarketGlance mappings, and vendor data licensed under CC-BY-SA-4.0

## Use Case:

Business, strategy, and transformation teams use this skill to diagnose where enterprise Agent initiatives should start, prioritize COMPASS dimensions, assess system readiness, and choose supplier direction categories before implementation planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reference names and packaged filenames do not fully align, which can lead an agent to look for guidance in the wrong file.

Mitigation: Review the package structure before deployment and verify that each referenced diagnostic, supplier, readiness, and boundary file is available at the expected path.

Risk: Supplier and licensing claims affect procurement and reuse decisions.

Mitigation: Verify vendor information against IDC MarketGlance materials or vendor official websites, and confirm licensing obligations before relying on the content commercially.

Risk: Agent planning recommendations may overreach if business baselines or human approval gates are missing.

Mitigation: Require baseline data for ROI claims and keep human approval for exceptions, critical decisions, and vendor evaluation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/seanlandtop/skills/idc-enterprise-agent-compass)
- [COMPASS workflow and rules](artifact/human-agent-boundary.md)
- [System readiness framework](artifact/vendor-enterprise.md)
- [Supplier direction mapping](artifact/vendor-platform.md)
- [Human-Agent boundary checklist](artifact/vendor-industry.md)
- [China AI Agent industry application and development platform market overview](https://my.idc.com/getdoc.jsp?containerId=CHC54462426&pageType=PRINTFRIENDLY)
- [China enterprise AI Agent application market overview](https://my.idc.com/getdoc.jsp?containerId=CHC54371726&pageType=PRINTFRIENDLY)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown guidance with structured diagnostic sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Bilingual Chinese and English business-strategy guidance; no executable code or hidden runtime behavior identified in security evidence.]

## Skill Version(s):

1.0.3 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
