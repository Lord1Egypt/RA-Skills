## Description: <br>
Search, mark, rate, review, and manage books, movies, music, games, podcasts, performances, collections, and tags in NeoDB through its API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gitnapp](https://clawhub.ai/user/gitnapp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to search NeoDB catalog items and update a user's NeoDB shelves, ratings, reviews, notes, collections, and tags after user confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup flow can display and store NeoDB account credentials. <br>
Mitigation: Treat generated tokens and scripts/.credentials.json as secrets; remove the file or restrict its permissions after configuring NEODB_TOKEN. <br>
Risk: Write operations can update shelves, ratings, reviews, notes, collections, tags, visibility, and federation posting behavior. <br>
Mitigation: Require explicit user confirmation before each write request, including review of visibility and post_to_fediverse values. <br>


## Reference(s): <br>
- [NeoDB Skill Page](https://clawhub.ai/gitnapp/neodb) <br>
- [Catalog API Reference](references/catalog.md) <br>
- [Shelf and Journal API Reference](references/shelf-and-journal.md) <br>
- [Collection and Tag API Reference](references/collection-and-tag.md) <br>
- [NeoDB OpenAPI Specification](references/openapi.json) <br>
- [NeoDB](https://neodb.social) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands, API request examples, and JSON snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill should request user confirmation before write operations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
