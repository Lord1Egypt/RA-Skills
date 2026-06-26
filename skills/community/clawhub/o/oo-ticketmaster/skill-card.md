## Description: <br>
Ticketmaster (ticketmaster.com). Use this skill for Ticketmaster requests that search, read, or retrieve Ticketmaster event, venue, attraction, classification, suggestion, image, section-map, and Season Ticketing information through an OOMOL-connected account. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to operate Ticketmaster through an OOMOL-connected account, primarily for searching and reading Ticketmaster events, venues, attractions, classifications, suggestions, images, and section maps. Season Ticketing command execution should be treated as a higher-risk workflow that needs explicit payload review before use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Season Ticketing command execution may change Ticketmaster account state even though the skill is primarily presented as read/search oriented. <br>
Mitigation: Require explicit user approval of the exact action payload and expected effect before running Season Ticketing commands. <br>
Risk: The skill depends on sensitive Ticketmaster credentials injected through an OOMOL-connected account. <br>
Mitigation: Install and run it only in environments where the OOMOL account connection, scopes, and billing state are trusted and reviewed. <br>


## Reference(s): <br>
- [ClawHub Ticketmaster skill page](https://clawhub.ai/oomol/oo-ticketmaster) <br>
- [OOMOL publisher profile](https://clawhub.ai/user/oomol) <br>
- [Ticketmaster homepage](https://www.ticketmaster.com) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live connector schemas before constructing Ticketmaster action payloads.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
