## Description: <br>
Look up, search, and reference Bible verses and saved Hey Bible account data through the Hey Bible API, returning Scripture text and structured JSON. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hey-bible](https://clawhub.ai/user/hey-bible) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents use this skill when a user asks to look up, quote, search, cross-reference, or compare Bible verses, passages, chapters, and translations. With the user's Hey Bible API key, it can also retrieve saved favorites, notes, verse images, chats, and tags. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read private Hey Bible account data, including favorites, notes, verse images, chats, tags, and signed image links. <br>
Mitigation: Use only with a Hey Bible API key the user is comfortable giving to the agent, and review returned account data before sharing or storing it elsewhere. <br>
Risk: Verse searches may save lookup activity to the user's Hey Bible account. <br>
Mitigation: Tell the user before running searches when account activity matters, and keep lookups scoped to the user's request. <br>


## Reference(s): <br>
- [Hey Bible homepage](https://heybible.app) <br>
- [Hey Bible API docs](https://docs.heybible.app) <br>
- [Hey Bible CLI package](https://www.npmjs.com/package/@hey-bible/cli) <br>
- [Hey Bible MCP package](https://www.npmjs.com/package/@hey-bible/mcp) <br>
- [Hey Bible TypeScript SDK](https://www.npmjs.com/package/@hey-bible/client) <br>
- [Artifact API reference](artifact/references/api-reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, structured JSON, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON responses from the Hey Bible CLI] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires HEY_BIBLE_API_KEY, Node.js, npx, and network access to api.heybible.app.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
