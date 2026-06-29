## Description: <br>
Global Biblio Base helps agents search Chinese and global scholarly literature, inspect article metadata and source links, and retrieve authorized Chinese journal PDFs or open-access PDFs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[j-levee](https://clawhub.ai/user/j-levee) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, students, analysts, and writing agents use this skill to find academic papers, patents, standards, theses, and supporting citations, then review metadata or retrieve available full text. It is especially oriented toward Chinese journal full-text access and global literature discovery through natural-language queries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts external literature and publisher services and may download PDFs locally. <br>
Mitigation: Use explicit search and download requests, set practical result and download limits, and avoid retrieving restricted or non-open-access content. <br>
Risk: The skill can create or use a service account and stores an email address for quota management. <br>
Mitigation: Provide only an email address suitable for the service, review the generated configuration before reuse, and avoid sharing sensitive personal or institutional credentials in chat. <br>
Risk: The skill includes quota, recharge, and payment flows. <br>
Mitigation: Review any recharge prompt, plan, amount, and payment page carefully before authorizing payment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/j-levee/global-biblio-base) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown responses with search plans, literature result summaries, citation details, quota status, download guidance, and occasional command or configuration snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include links to source records or downloadable PDFs, quota and billing prompts, and locally saved PDF references when downloads are requested.] <br>

## Skill Version(s): <br>
3.6.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
