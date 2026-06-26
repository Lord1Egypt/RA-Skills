## Description: <br>
Monitors official Vietnam NSO monthly and quarterly socio-economic releases and compares same-period trends; used when users request official macro updates and year-over-year context. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ndtchan](https://clawhub.ai/user/ndtchan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and analysts use this skill to retrieve official Vietnam NSO macro releases, compare current indicators with the same period in the prior year, and summarize sector implications for Vietnam equities. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Official NSO pages, linked reports, or PDFs may be partially unavailable, causing missing macro indicator blocks or historical comparators. <br>
Mitigation: Report retrieval coverage, list missing GDP/CPI/IIP/trade/retail/FDI/credit fields, and downgrade confidence when required blocks are incomplete. <br>
Risk: Sector-impact summaries can be mistaken for investment instructions or may rely on unverified macro figures. <br>
Mitigation: Separate NSO facts from sector inferences, cite source URLs for key claims, verify macro figures before financial use, and avoid absolute buy or sell instructions. <br>


## Reference(s): <br>
- [Vietnam NSO monthly socio-economic reports](https://www.nso.gov.vn/bao-cao-tinh-hinh-kinh-te-xa-hoi-hang-thang) <br>
- [ClawHub release page](https://clawhub.ai/ndtchan/nso-macro-monitor) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown with release metadata, indicator tables, sector implications, confidence notes, data gaps, and cited URLs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires web access to official NSO pages and linked reports or PDFs; outputs confidence levels based on retrieval coverage and missing indicator blocks.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
