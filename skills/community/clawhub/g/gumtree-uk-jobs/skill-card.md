## Description: <br>
Search Gumtree UK jobs and part-time listings with bb-browser from a user's role, location, and hours, returning structured JSON plus first-image Markdown for scanning vacancies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[salamankakit](https://clawhub.ai/user/salamankakit) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to search UK employment listings on Gumtree for full-time, part-time, temporary, and casual roles, then fetch listing details for closer review. It is intended for jobs-only workflows and excludes non-employment categories such as pets, motors, property sales, and collectibles. <br>

### Deployment Geography for Use: <br>
United Kingdom <br>

## Known Risks and Mitigations: <br>
Risk: Search terms and locations are sent to Gumtree when the bb-browser commands run. <br>
Mitigation: Avoid entering sensitive personal data in search queries or locations unless the user explicitly accepts sharing that data with Gumtree. <br>
Risk: The helper scripts are installed by copying JavaScript into the local bb-browser sites directory. <br>
Mitigation: Install only from the verified release artifact, review the copied scripts before use, and replace them only when updating this skill. <br>
Risk: Scope drift can occur if a command searches broad Gumtree categories instead of jobs. <br>
Mitigation: Use the documented jobs category or a job subcategory for every search and pass only Gumtree listing URLs to the listing command. <br>
Risk: Job adverts can contain inaccurate employer, right-to-work, or pay information. <br>
Mitigation: Verify employer identity, right-to-work requirements, and pay through official channels before acting on a listing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/salamankakit/gumtree-uk-jobs) <br>
- [Publisher profile](https://clawhub.ai/user/salamankakit) <br>
- [Gumtree UK](https://www.gumtree.com/) <br>
- [bb-browser package](https://www.npmjs.com/package/bb-browser) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash command examples; helper commands return JSON records and optional first-image Markdown.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search output includes query, location, category, page, result count, listing URLs, snippets, prices, locations, image URLs, and first-image Markdown when available.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
