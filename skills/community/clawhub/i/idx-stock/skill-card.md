## Description: <br>
Scrapes and returns a translated company profile from the Indonesia Stock Exchange website using a supplied IDX stock code. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zororaka00](https://clawhub.ai/user/zororaka00) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and analysts use this skill to retrieve public listed-company profile data from IDX by stock code and receive normalized English field names for downstream analysis or reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts idx.co.id and depends on third-party Python packages. <br>
Mitigation: Install in a managed environment and review dependency provenance before deployment. <br>
Risk: Live scraping can fail or return incomplete data if the IDX page structure changes. <br>
Mitigation: Validate outputs with representative stock codes and handle unsuccessful responses before relying on the data. <br>
Risk: The artifact includes broad security claims that are not a formal guarantee. <br>
Mitigation: Use the server security evidence as the authority and review the skill in the target environment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/zororaka00/idx-stock) <br>
- [Publisher Profile](https://clawhub.ai/user/zororaka00) <br>
- [Indonesia Stock Exchange Listed Company Profiles](https://www.idx.co.id/id/perusahaan-tercatat/profil-perusahaan-tercatat/) <br>


## Skill Output: <br>
**Output Type(s):** [json, text] <br>
**Output Format:** [JSON object with success, data, and message fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The data object contains translated company profile fields plus stock_code, source, and scraped_at metadata.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact SKILL.md metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
