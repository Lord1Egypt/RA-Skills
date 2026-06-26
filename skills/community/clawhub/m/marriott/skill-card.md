## Description: <br>
Searches Marriott Bonvoy hotels on marriott.com.cn, compares available rooms and rates, and helps a user confirm a booking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qianjunye](https://clawhub.ai/user/qianjunye) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and travel planners use this skill to search Marriott China hotels, review room and rate options, and proceed through a reservation flow after explicit confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can act through a logged-in Marriott browser session and submit real hotel reservations. <br>
Mitigation: Require explicit user confirmation before final booking and independently verify hotel, dates, cancellation terms, total price, and payment details before submission. <br>
Risk: The skill stores or reuses browser login state, including cookies and generated booking artifacts. <br>
Mitigation: Use a dedicated disposable Chrome profile for Marriott only, avoid copying normal browser cookies, and delete cookies.json plus generated result files after use. <br>
Risk: The workflow includes behavior intended to avoid bot protections and may trigger access blocks or site policy issues. <br>
Mitigation: Review whether use is permitted for the account and site, stop on access-denied or interception events, and do not retry in ways that obscure user intent. <br>


## Reference(s): <br>
- [Marriott skill release page](https://clawhub.ai/qianjunye/marriott) <br>
- [Usage guide](artifact/使用指南.md) <br>
- [Marriott China](https://www.marriott.com.cn) <br>
- [OpenStreetMap Nominatim search](https://nominatim.openstreetmap.org/search) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown summaries and tables backed by JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local booking workflow artifacts such as search results, selections, room results, cookies, screenshots, and confirmation JSON.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
