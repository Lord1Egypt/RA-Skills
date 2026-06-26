## Description: <br>
Search Jerusalem specialty coffee shops by name, amenities, ratings, opening hours, reviews, and locations using a public community-curated data source. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alexpolonsky](https://clawhub.ai/user/alexpolonsky) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and agents use this skill to find Jerusalem specialty coffee shops, check amenities such as WiFi or kosher status, inspect ratings and reviews, and identify shops that may be open now. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Venue hours, amenities, and ratings may be stale because the skill relies on a public community data export and cached upstream place data. <br>
Mitigation: Verify hours and important venue details directly before travel or time-sensitive decisions. <br>
Risk: The skill contacts a public Google Docs export and writes a short-lived cache under the system temporary directory. <br>
Mitigation: Use it only in environments where that outbound request and temporary local cache are acceptable. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/alexpolonsky/jlm-coffee) <br>
- [Skill Homepage](https://github.com/alexpolonsky/agent-skill-jlm-coffee) <br>
- [Jerusalem Coffee Finder Data Site](https://coffee.amsterdamski.com) <br>
- [Public Google Docs Data Export](https://docs.google.com/document/d/1BfsXKQLbKjogfSebRr0Ixt4L4VJHqPqTfnWxkosvcuM/export?format=txt) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, guidance] <br>
**Output Format:** [Terminal text or JSON command output with optional shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports colorized terminal output, a --json mode, and a 15-minute local cache in the system temporary directory.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release metadata; artifact frontmatter: 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
