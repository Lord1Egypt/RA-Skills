## Description: <br>
Pinecone (pinecone.io). Use this skill for ANY Pinecone request — reading, creating, updating, and deleting data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to operate Pinecone indexes and vectors through an OOMOL-connected account, including read, write, and destructive index or vector workflows. It is intended for Pinecone tasks where the agent should inspect the live connector schema before constructing a command payload. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can operate a user's Pinecone account through OOMOL and requires sensitive connected-account credentials. <br>
Mitigation: Install it only when Pinecone account access through OOMOL is intended, and ensure the user trusts the oo CLI and OOMOL connection model before setup. <br>
Risk: Write and destructive actions can create, update, delete, or overwrite Pinecone indexes and vectors. <br>
Mitigation: Review write and delete payloads carefully and obtain explicit approval before running delete_index, delete_vectors, update_vector, or upsert_vectors. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/oomol/oo-pinecone) <br>
- [Pinecone Homepage](https://www.pinecone.io/) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI Install Guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Connector responses are JSON objects containing data and meta.executionId.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
