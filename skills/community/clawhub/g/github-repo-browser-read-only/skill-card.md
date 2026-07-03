## Description: <br>
Provides read-only GitHub repository browsing for agents, including repository listing, file and README inspection, code search, commit and branch review, and optional file or archive downloads to storage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agentpmt](https://clawhub.ai/user/agentpmt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to inspect GitHub repositories they can access, gather code context, review documentation and commits, search code, and retrieve selected files or repository archives for analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The connected GitHub token can expose private repositories available to that account. <br>
Mitigation: Install only when read access to those repositories is intended, and keep requests scoped to the minimum repositories, paths, and refs needed for the task. <br>
Risk: Download actions can copy private repository files or archives into AgentPMT-managed storage and return signed URLs. <br>
Mitigation: Prefer read-only inspection actions such as get_file, get_readme, list_directory, and search_code; use download_to_storage or download_repo_to_storage only when copying repository content and sharing a signed URL is intentional. <br>
Risk: External storage retention and access controls are not clearly documented in the evidence. <br>
Mitigation: Avoid downloading sensitive source or secrets unless downstream storage handling, retention, and sharing expectations are acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/agentpmt/skills/github-repo-browser-read-only) <br>
- [AgentPMT marketplace page](https://www.agentpmt.com/marketplace/github-repo-browser-read-only) <br>
- [Generated action schema](artifact/schema.md) <br>
- [File Management related skill](https://clawhub.ai/agentpmt/file-management) <br>
- [AgentPMT account MCP/REST setup](https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, API calls, JSON, files] <br>
**Output Format:** [Markdown instructions with JSON action examples and JSON tool responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Some download actions return file identifiers and signed URLs for copied repository files or archives.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
