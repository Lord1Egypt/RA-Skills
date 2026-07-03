## Description: <br>
Extracts business contact details from Google Maps search results and place detail pages, then visits listed business websites to collect public emails, phone numbers, and social media profile links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[browseract-cli](https://clawhub.ai/user/browseract-cli) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to build browser-assisted lead lists from Google Maps business listings and public business websites. It is intended for visible business data and should be run in small, compliant batches. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bulk contact extraction can violate site terms, privacy expectations, or applicable laws when used beyond public business data. <br>
Mitigation: Use only on public business information, keep runs small, respect site terms and applicable privacy laws, and review outputs before use. <br>
Risk: Parallel or stealth browser sessions can increase abuse and compliance risk. <br>
Mitigation: Avoid stealth, anti-throttling tactics, and high-volume automation; test with a few businesses before any broader run. <br>
Risk: The workflow may collect personal or sensitive contact information from business websites. <br>
Mitigation: Filter results to public business contacts only and remove personal or sensitive contact details before storage or outreach. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/browseract-cli/skills/google-maps-contact-extract) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Code, Guidance] <br>
**Output Format:** [Markdown guidance with shell command snippets and JSON extraction results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs can include per-business records with names, addresses, phones, websites, ratings, hours, emails, and social media profile links.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
