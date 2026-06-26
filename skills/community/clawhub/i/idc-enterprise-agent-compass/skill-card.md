## Description: <br>
Based on the IDC COMPASS model, this skill diagnoses enterprise business process efficiency constraints, identifies suitable Agent entry points, and maps supplier directions using the IDC MarketGlance taxonomy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[seanlandtop](https://clawhub.ai/user/seanlandtop) <br>

### License/Terms of Use: <br>
MIT-0 distribution; CC-BY-SA-4.0 for IDC COMPASS methodology, MarketGlance taxonomy mappings, and vendor directory data <br>


## Use Case: <br>
Business and IT leaders use this skill to diagnose enterprise workflow bottlenecks, choose Agent pilot scenarios, and map supplier directions without ranking individual vendors. It is intended for enterprise Agent planning across process analysis, system readiness, supplier category selection, and human-agent boundary design. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Vendor lists and vendor claims may be incomplete or outdated. <br>
Mitigation: Treat vendor lists as informational, verify current vendor claims independently, and consult IDC MarketGlance vendor product evaluation reports and vendor official websites before selection. <br>
Risk: Redistribution or derivative use may miss attribution or share-alike requirements for IDC methodology and data. <br>
Mitigation: Check the IDC attribution and CC-BY-SA-4.0 terms before redistributing derived materials. <br>
Risk: Recommendations may be misleading if the user skips diagnosis or lacks baseline metrics. <br>
Mitigation: Complete the diagnostic steps, preserve human review for critical decisions, and collect baseline processing time, accuracy, and manual effort before estimating ROI. <br>
Risk: The skill is Markdown-only guidance and is not an approved production integration. <br>
Mitigation: Do not provide secrets or production system access unless a separate implementation is built and approved with human approval, audit, and permission controls. <br>


## Reference(s): <br>
- [COMPASS Dimensions Reference](artifact/IDCcopyright.md) <br>
- [Supplier Direction Mapping Reference](artifact/vendor-platform.md) <br>
- [System Readiness Framework](artifact/vendor-enterprise.md) <br>
- [Human-Agent Boundary Checklist](artifact/vendor-industry.md) <br>
- [IDC MarketGlance: China AI Agent Industry Applications and Development Platform Market Overview](https://my.idc.com/getdoc.jsp?containerId=CHC54462426&pageType=PRINTFRIENDLY) <br>
- [IDC MarketGlance: China Enterprise AI Agent Applications Market Overview](https://my.idc.com/getdoc.jsp?containerId=CHC54371726&pageType=PRINTFRIENDLY) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown with structured diagnosis and recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include vendor candidate lists only after the user asks; does not rank vendors or estimate ROI without baseline data.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata; artifact frontmatter and changelog show 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
