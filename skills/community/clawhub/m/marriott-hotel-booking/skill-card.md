## Description: <br>
Searches Marriott-family hotels by destination, brand keyword, and budget, then returns hotel prices, details, package offers, and booking links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[travel-skills](https://clawhub.ai/user/travel-skills) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External travelers and travel planners use this skill to find Marriott-family hotels, compare prices and amenities, review hotel or package details, and open booking links. It does not complete bookings directly. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses an environment-configured proxy URL and auth token for hotel search, and the release evidence says external network use is under-disclosed. <br>
Mitigation: Review before installing, use it only with a trusted proxy service, control PROXY_URL and PROXY_TOKEN, and verify the proxy URL is fixed to the intended HTTPS host. <br>
Risk: Travel queries and booking details may be sent through the configured proxy service. <br>
Mitigation: Avoid entering sensitive travel or booking details until the skill declares its network requirements and validates the proxy destination. <br>
Risk: Hotel prices and availability can change, and the skill provides booking links rather than completing reservations. <br>
Mitigation: Confirm final pricing, policies, availability, and payment terms on the booking page before acting on the result. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/travel-skills/skills/marriott-hotel-booking) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown-formatted text with hotel search results, details, package offers, and booking links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Results may include hotel IDs, prices, addresses, nearby points of interest, facilities, policies, package benefits, and external booking links.] <br>

## Skill Version(s): <br>
1.1.3 (source: server release evidence; artifact frontmatter reports 1.1.2) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
