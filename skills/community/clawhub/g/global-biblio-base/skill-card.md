## Description: <br>
Global Biblio Base lets an agent search Chinese and global scholarly literature, inspect article metadata and source links, and retrieve authorized Chinese or open-access PDFs when available. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[j-levee](https://clawhub.ai/user/j-levee) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, researchers, students, and developers use this skill to find academic papers, patents, standards, theses, supporting citations, and literature-review material through natural-language requests. It is especially useful when an agent needs structured search results, article details, citation/source links, quota-aware access, and user-triggered full-text retrieval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill collects and stores an email address for registration, quota tracking, and some open-access lookups. <br>
Mitigation: Ask for an email only when needed, explain its use before registration, and avoid using sensitive personal or institutional addresses unless the user accepts that exposure. <br>
Risk: Research topics and download requests are sent to SmartLib Gateway and open-access services. <br>
Mitigation: Do not use the skill for confidential, unpublished, or institutionally sensitive research topics without prior review. <br>
Risk: Successful SmartLib API calls consume quota and the skill can present paid WeChat recharge flows. <br>
Mitigation: Show quota status and expected billable actions before continuing, require explicit user action for recharge, and keep user email out of payment display pages. <br>
Risk: The skill can create local PDF files and includes automated download guidance with incomplete boundaries. <br>
Mitigation: Download only user-requested items, validate returned files before presenting them, and avoid attempting to bypass paywalls or access restrictions. <br>
Risk: The artifact includes gateway configuration values used to contact the service. <br>
Mitigation: Review installed configuration before sharing or publishing derived files, and avoid exposing service credentials in user-visible responses. <br>


## Reference(s): <br>
- [ClawHub Skill Listing](https://clawhub.ai/j-levee/skills/global-biblio-base) <br>
- [README](artifact/README.md) <br>
- [Pipeline Optimization Guide](artifact/PIPELINE.md) <br>
- [Skill Definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown responses with structured literature results, links, status labels, optional code or shell snippets, and local PDF files when downloads are requested and available.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call external SmartLib Gateway and open-access services, track quota consumption, request an email address for account/quota management, and create local PDF files during user-requested downloads.] <br>

## Skill Version(s): <br>
3.6.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
