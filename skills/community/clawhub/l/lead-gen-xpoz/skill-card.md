## Description: <br>
Lead Generation finds high-intent buyers in live Twitter, Instagram, and Reddit conversations, researches a product, generates targeted search queries, and discovers people actively looking for related solutions through Xpoz MCP. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qq63523555](https://clawhub.ai/user/qq63523555) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Sales, growth, marketing, and customer-discovery users use this skill to research a product, find social posts and users showing buyer intent, score leads, and draft outreach for human review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow sends generated search queries to Xpoz and may include sensitive product, customer, or prospecting details. <br>
Mitigation: Keep confidential details out of search queries and validate the product profile with the user before running discovery. <br>
Risk: The skill depends on Xpoz, mcporter, and the xpoz-setup OAuth flow. <br>
Mitigation: Install and authorize only when those dependencies are trusted, and verify access with the documented checkAccessKeyStatus command. <br>
Risk: Local lead-generation files can retain product profiles, queries, and sent-lead history. <br>
Mitigation: Periodically review or delete files under data/lead-generation according to the user's retention needs. <br>
Risk: Generated outreach drafts may be inaccurate, noncompliant, or omit required context for a specific campaign. <br>
Mitigation: Require human review and editing before any outreach is sent, including disclosure of affiliations. <br>


## Reference(s): <br>
- [Lead Generation ClawHub page](https://clawhub.ai/qq63523555/lead-gen-xpoz) <br>
- [Publisher profile](https://clawhub.ai/user/qq63523555) <br>
- [Xpoz](https://xpoz.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash commands, JSON file paths, lead scoring notes, and outreach draft text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates or updates product profile, search query, and sent-lead tracking files under data/lead-generation; final lead records include username, quote, URL, score, fit rationale, outreach draft, engagement, and timestamp.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata, SKILL.md frontmatter, changelog released 2026-04-13) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
