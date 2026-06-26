## Description: <br>
Query Philippines customs HS codes for products exported to the Philippines using product descriptions and the official Tariff Commission tariff book. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wumaohua233](https://clawhub.ai/user/wumaohua233) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, exporters, and trade-support developers use this skill to identify likely Philippines HS classifications for products, download chapter PDFs, and search the tariff text for candidate codes with source pages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts the Philippines Tariff Commission and Google Drive, opens Chromium, and saves downloaded PDFs locally. <br>
Mitigation: Run it only in environments where browser automation, outbound access to those services, and local PDF storage are acceptable. <br>
Risk: A fallback download path may weaken TLS verification when retrieving large Google Drive files. <br>
Mitigation: Prefer verified downloads and review the downloaded PDF source URL before relying on results. <br>
Risk: HS code results are search candidates from tariff PDFs and may not be a final customs classification. <br>
Mitigation: Review the returned source URL, page number, and product description before using the code for trade or customs decisions. <br>


## Reference(s): <br>
- [Philippines Tariff Commission 2022 Tariff Book](https://www.tariffcommission.gov.ph/tariff-book-2022) <br>
- [ClawHub Skill Page](https://clawhub.ai/wumaohua233/ph-hs-code-finder) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, code, guidance] <br>
**Output Format:** [Markdown and terminal text with HS code tables, source URLs, page numbers, and recommended candidate codes.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May download public chapter PDFs locally and may open Chromium through Playwright to resolve Google Drive-hosted tariff files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
