---
name: github-repo-browser-read-only
description: "GitHub Repo Browser - Read Only: Read-only GitHub access for agents. Use when an agent needs github repo browser read only, github repo browser read only, browse your private github repositories from a chat agent, explore any public repository's folder structure and source files, read readme files and documentation from any repo, search for code patterns across your repositories or any public project, download repo to storage, owner through AgentPMT-hosted remote tool calls."
version: 1.0.0
homepage: https://www.agentpmt.com/marketplace/github-repo-browser-read-only
compatibility: "Agent instructions for AgentPMT-hosted remote tool calls. Follow this skill body for supported account, wallet, and setup routes. No local command runtime is declared."
metadata: {"author":"agentpmt","openclaw":{"homepage":"https://www.agentpmt.com/marketplace/github-repo-browser-read-only"}}
---
# GitHub Repo Browser - Read Only

## Freshness
Last updated: `2026-06-24`.

If the current date is more than 7 days after the last updated date, reinstall this skill from skills.sh or ClawHub before relying on endpoints, schemas, setup steps, or examples.

## What This Tool Does
Give your AI agent secure, read-only access to your GitHub repositories. Browse your personal repos, organization repos, and any public project on GitHub. Explore folder structures, read source files and READMEs, view branches and commit history, and search across repositories or code. Download individual files or entire repository archives directly to file storage with integrity verification — perfect for downstream processing, attestation, or analysis. No risk of accidental writes, pushes, or deletions. Connects to your GitHub account so agents can access your private repos alongside any public repository on GitHub.

## Product Instructions
### GitHub Repo Browser

Read-only GitHub repository navigation for agents. Use it to browse accessible repositories, inspect repo structure, read files, fetch READMEs, search repositories or code, and download files or entire repo archives to file storage.

#### Actions

##### `list_my_repos`
List repositories the connected GitHub account can access.

Optional fields:
- `visibility`: `all`, `public`, or `private`
- `affiliation`: comma-separated GitHub affiliation filter such as `owner,collaborator,organization_member`
- `sort`: `created`, `updated`, `pushed`, or `full_name`
- `direction`: `asc` or `desc`
- `per_page`: 1-100
- `page`: 1+

```json
{"action":"list_my_repos","visibility":"private","per_page":20,"page":1}
```

##### `list_org_repos`
List repositories in an organization the connected account can access.

Required fields:
- `org`

Optional fields:
- `type_filter`: `all`, `public`, `private`, `forks`, `sources`, or `member`
- `sort`, `direction`, `per_page`, `page`

```json
{"action":"list_org_repos","org":"acme","type_filter":"private","per_page":25}
```

##### `get_repo`
Fetch repository metadata including default branch, permissions, visibility, and URLs.

Required fields:
- `owner`
- `repo`

```json
{"action":"get_repo","owner":"acme","repo":"platform"}
```

##### `list_branches`
List repository branches with pagination.

Required fields:
- `owner`
- `repo`

Optional fields:
- `protected_only`
- `per_page`
- `page`

```json
{"action":"list_branches","owner":"acme","repo":"platform","protected_only":true}
```

##### `list_commits`
List commits for a repository. You can scope the list to a branch, tag, or commit ancestry using `ref`, and filter to commits from the last `N` hours using `since_hours`. Results come back newest first.

Required fields:
- `owner`
- `repo`

Optional fields:
- `ref`
- `path`
- `since_hours`
- `per_page`
- `page`

```json
{"action":"list_commits","owner":"acme","repo":"platform","ref":"release/2026.03","since_hours":24,"per_page":20}
```

##### `get_commit`
Fetch a specific commit by SHA, including commit metadata, stats, and changed files.

Required fields:
- `owner`
- `repo`
- `commit_sha`

```json
{"action":"get_commit","owner":"acme","repo":"platform","commit_sha":"abc123def4567890abc123def4567890abc12345"}
```

##### `list_directory`
List the contents of a repository directory.

Required fields:
- `owner`
- `repo`

Optional fields:
- `path`: omit for repository root
- `ref`: branch, tag, or commit SHA

```json
{"action":"list_directory","owner":"acme","repo":"platform","path":"src","ref":"main"}
```

##### `get_file`
Read a text file from a repository. Binary files and files larger than 1 MB are rejected.

Required fields:
- `owner`
- `repo`
- `path`

Optional fields:
- `ref`

```json
{"action":"get_file","owner":"acme","repo":"platform","path":"src/app.py","ref":"main"}
```

##### `get_readme`
Fetch the repository README content and metadata.

Required fields:
- `owner`
- `repo`

Optional fields:
- `ref`

```json
{"action":"get_readme","owner":"acme","repo":"platform"}
```

##### `search_repositories`
Search repositories visible to the connected account.

Required fields:
- `query`

Optional fields:
- `sort`: `stars`, `forks`, `help-wanted-issues`, or `updated`
- `order`: `asc` or `desc`
- `per_page`
- `page`

```json
{"action":"search_repositories","query":"terraform language:hcl org:acme","sort":"updated","per_page":10}
```

##### `search_code`
Search code visible to the connected account. You can scope the search to a repository by providing `owner` and `repo`, or by including qualifiers directly in `query`.

Required fields:
- `query`

Optional fields:
- `owner`
- `repo`
- `sort`: `indexed`
- `order`: `asc` or `desc`
- `per_page`
- `page`

```json
{"action":"search_code","query":"OpenAI apiKey path:src language:typescript","owner":"acme","repo":"platform"}
```

##### `download_to_storage`
Download a file from a GitHub repository and save it to file storage. Returns a `file_id` and `signed_url` for downstream tools to access the exact bytes. Files up to 100 MB are supported. Downloaded bytes are integrity-verified against GitHub's git SHA before storage.

Required fields:
- `owner`
- `repo`
- `path`

Optional fields:
- `ref`

```json
{"action":"download_to_storage","owner":"acme","repo":"platform","path":"assets/logo.png","ref":"main"}
```

##### `download_repo_to_storage`
Download a repository archive as a `.tar.gz` file and save it to file storage. Returns a `file_id` and `signed_url`. Use `ref` to select a specific branch, tag, or commit SHA. Use `path` to optionally filter the archive to a subdirectory.

Required fields:
- `owner`
- `repo`

Optional fields:
- `ref`: branch, tag, or commit SHA (defaults to the repository's default branch)
- `path`: subdirectory to filter the archive to

Download an entire repository:
```json
{"action":"download_repo_to_storage","owner":"acme","repo":"platform","ref":"main"}
```

Download only a subdirectory:
```json
{"action":"download_repo_to_storage","owner":"acme","repo":"platform","ref":"v2.1.0","path":"service"}
```

#### Notes

- This tool is intentionally read-only. It does not support issue creation, pull request edits, pushes, or generic passthrough requests.
- All actions require a connected GitHub account via the existing `github_token` software connection.
- Pagination metadata includes `page`, `per_page`, `next_page`, `prev_page`, `has_next_page`, and `has_prev_page` when applicable.
- `list_commits` uses GitHub's commit listing endpoint and applies the `since_hours` filter by converting it to a GitHub `since` timestamp.
- `get_file` and `get_readme` return UTF-8 decoded text content for files up to 1 MB.
- `download_to_storage` downloads raw bytes (any file type) up to 100 MB and verifies integrity via git SHA1 before uploading to file storage.
- `download_repo_to_storage` downloads a full repository archive (or a filtered subdirectory) as a `.tar.gz` file up to 100 MB and uploads it to file storage.

## When To Use
- Use this skill for `GitHub Repo Browser - Read Only` on AgentPMT.
- Use it when an agent needs this specific tool's behavior, schema, inputs, outputs, and invocation shape.
- Search and activation keywords: github repo browser   read only, github repo browser read only, browse your private github repositories from a chat agent, explore any public repository's folder structure and source files, read readme files and documentation from any repo, search for code patterns across your repositories or any public project, download repo to storage, owner.
- Supported action names: `download_repo_to_storage`, `download_to_storage`, `get_commit`, `get_file`, `get_readme`, `get_repo`, `list_branches`, `list_commits`, `list_directory`, `list_my_repos`, `list_org_repos`, `search_code`, `search_repositories`.

## Use Cases
- Browse your private GitHub repositories from a chat agent
- Explore any public repository's folder structure and source files
- Read README files and documentation from any repo
- Search for code patterns across your repositories or any public project
- Review recent commit history and see what changed in each commit
- List branches and compare code across different branches
- Audit dependencies by reading package.json or requirements.txt files
- Gather code context for debugging without leaving your workflow
- Onboard to unfamiliar codebases by exploring structure and reading key files
- Research how open source projects implement specific features
- Download individual files with integrity verification for processing or attestation
- Download entire repository archives or specific subdirectories as .tar.gz files
- Pull code snapshots from specific branches or tags for analysis

## Related Product Skills
- File Management: ../file-management (ClawHub: `file-management`, page: https://clawhub.ai/agentpmt/file-management; skills.sh: `npx skills add AgentPMT/agent-skills --skill file-management`)

## Categories And Industries
No categories or industry tags are published for this tool.

## Actions And Schema
Complete generated action schema: `./schema.md`.
Supported action count: `13`.
x402 availability: not enabled for this product.

- `download_repo_to_storage` (action slug: `download-repo-to-storage`): Download a repository archive as a .tar.gz file and save it to file storage. Use ref to select a branch, tag, or commit. Use path to optionally filter to a specific subdirectory. Archives up to 100 MB are supported. Price: `5` credits. Parameters: `owner`, `path`, `ref`, `repo`, `timeout_seconds`.
- `download_to_storage` (action slug: `download-to-storage`): Download a single file from a GitHub repository and save it to file storage with SHA1 integrity verification. Returns a file_id and signed_url. Supports files up to 100 MB including binary files. Price: `5` credits. Parameters: `owner`, `path`, `ref`, `repo`, `timeout_seconds`.
- `get_commit` (action slug: `get-commit`): Fetch a specific commit by SHA, including changed files and commit stats. Price: `5` credits. Parameters: `commit_sha`, `owner`, `repo`, `timeout_seconds`.
- `get_file` (action slug: `get-file`): Read a text file from a repository at a branch, tag, or commit. Binary and oversized files are rejected. Price: `5` credits. Parameters: `owner`, `path`, `ref`, `repo`, `timeout_seconds`.
- `get_readme` (action slug: `get-readme`): Fetch the repository README content and metadata. Price: `5` credits. Parameters: `owner`, `ref`, `repo`, `timeout_seconds`.
- `get_repo` (action slug: `get-repo`): Fetch repository metadata, default branch, permissions, and URLs. Price: `5` credits. Parameters: `owner`, `repo`, `timeout_seconds`.
- `list_branches` (action slug: `list-branches`): List repository branches with pagination. Price: `5` credits. Parameters: `owner`, `page`, `per_page`, `protected_only`, `repo`, `timeout_seconds`.
- `list_commits` (action slug: `list-commits`): List commits for a repository, optionally scoped to a branch and filtered to the last N hours. Results are returned newest first. Price: `5` credits. Parameters: `owner`, `page`, `path`, `per_page`, `ref`, `repo`, `since_hours`, `timeout_seconds`.
- `list_directory` (action slug: `list-directory`): List the contents of a repository directory at a branch, tag, or commit. Price: `5` credits. Parameters: `owner`, `path`, `ref`, `repo`, `timeout_seconds`.
- `list_my_repos` (action slug: `list-my-repos`): List repositories the connected GitHub account can access, with pagination and sorting. Price: `5` credits. Parameters: `affiliation`, `direction`, `page`, `per_page`, `sort`, `timeout_seconds`, `visibility`.
- `list_org_repos` (action slug: `list-org-repos`): List repositories for an organization the connected account can access. Price: `5` credits. Parameters: `direction`, `org`, `page`, `per_page`, `sort`, `timeout_seconds`, `type_filter`.
- `search_code` (action slug: `search-code`): Search code visible to the connected account, optionally scoped to a specific repository. Price: `5` credits. Parameters: `order`, `owner`, `page`, `per_page`, `query`, `repo`, `sort`, `timeout_seconds`.
- `search_repositories` (action slug: `search-repositories`): Search repositories visible to the connected account. Price: `5` credits. Parameters: `order`, `page`, `per_page`, `query`, `sort`, `timeout_seconds`.

## Live Schema And Examples
Use the compact schema above for ordinary calls. Before a new production integration, or whenever parameters, enum values, nested objects, outputs, or examples are unclear, fetch live details first.

- Exact schema: call `agentpmt-tool-search-and-execution` with `action: "get_schema"`, and `tool_id: "github-repo-browser-read-only"`.
- Detailed examples: call `agentpmt-tool-search-and-execution` with `action: "get_instructions"` and `tool_id: "github-repo-browser-read-only"`, or call this product with `action: "get_instructions"` when the product tool is already selected.
- Treat returned live schema and instructions as more specific than this generated summary.

MCP schema lookup through the main AgentPMT MCP server:

```json
{
  "method": "tools/call",
  "params": {
    "name": "AgentPMT-Tool-Search-and-Execution",
    "arguments": {
      "action": "get_schema",
      "tool_id": "github-repo-browser-read-only"
    }
  }
}
```

For live examples, keep the same MCP tool and use these arguments:

```json
{
  "action": "get_instructions",
  "tool_id": "github-repo-browser-read-only"
}
```

Authenticated AgentPMT REST schema lookup body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_schema",
    "tool_id": "github-repo-browser-read-only"
  }
}
```

Authenticated AgentPMT REST live examples body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_instructions",
    "tool_id": "github-repo-browser-read-only"
  }
}
```

## Call This Tool
Product slug: `github-repo-browser-read-only`

Marketplace page: https://www.agentpmt.com/marketplace/github-repo-browser-read-only

- AgentPMT account route: first use `../agentpmt-account-mcp-rest-api-setup` to connect the main MCP server or REST API for an Agent Group where this tool is enabled.
- x402 route: not enabled for this product.
- AgentPMT overview: use `../what-is-agentpmt` for marketplace, Agent Group, workflow, MCP, REST, and payment concepts.

If those setup skills are not installed beside this product skill, use the downloads below.

Core AgentPMT setup skills:
- What AgentPMT is: ../what-is-agentpmt
  - ClawHub page: https://clawhub.ai/agentpmt/what-is-agentpmt
  - OpenClaw install: `openclaw skills install what-is-agentpmt`
  - skills.sh install: `npx skills add AgentPMT/agent-skills --skill what-is-agentpmt`
- AgentPMT account MCP/REST setup: ../agentpmt-account-mcp-rest-api-setup
  - ClawHub page: https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup
  - OpenClaw install: `openclaw skills install agentpmt-account-mcp-rest-api-setup`
  - skills.sh install: `npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup`

skills.sh install script:

```bash
npx skills add AgentPMT/agent-skills --skill what-is-agentpmt
npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup
```

MCP call shape after the main AgentPMT MCP server is connected:

```json
{
  "method": "tools/call",
  "params": {
    "name": "GitHub-Repo-Browser---Read-Only",
    "arguments": {
      "action": "download_repo_to_storage",
      "owner": "example owner",
      "path": "example path",
      "ref": "example ref",
      "repo": "example repo",
      "timeout_seconds": 5
    }
  }
}
```

Use the exact tool name returned by `tools/list`; the name above is the expected readable form.

Authenticated AgentPMT REST call body:

```json
{
  "name": "github-repo-browser-read-only",
  "parameters": {
    "action": "download_repo_to_storage",
    "owner": "example owner",
    "path": "example path",
    "ref": "example ref",
    "repo": "example repo",
    "timeout_seconds": 5
  }
}
```

Use the setup skill for the account connection details before making REST calls.

## Response Handling
- Treat the returned JSON as the source of truth for this tool call.
- If the response includes warnings or correction targets, apply them before retrying.
- If the response includes a `passed` or success-style boolean, use it as the workflow gate.
- If validation fails or the response shape is unclear, call `get_schema` or `get_instructions` before retrying.
- If `download_repo_to_storage` fails, preserve the request parameters and retry only after fixing schema, auth, or payment errors.

## Security
- Do not place account secrets, wallet private keys, mnemonics, signatures, or payment headers in prompts or logs.
- Keep tool inputs scoped to the minimum content needed for the task.
- Use the setup skills for credential handling; this product skill only defines product-specific behavior.

## AgentPMT Reference
- What AgentPMT is: ../what-is-agentpmt (ClawHub: `what-is-agentpmt`, page: https://clawhub.ai/agentpmt/what-is-agentpmt; skills.sh: `npx skills add AgentPMT/agent-skills --skill what-is-agentpmt`)
- AgentPMT account MCP/REST setup: ../agentpmt-account-mcp-rest-api-setup (ClawHub: `agentpmt-account-mcp-rest-api-setup`, page: https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup; skills.sh: `npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup`)
- Marketplace product: https://www.agentpmt.com/marketplace/github-repo-browser-read-only
- AgentPMT main MCP server: https://api.agentpmt.com/mcp/
- AgentPMT REST invoke endpoint: https://api.agentpmt.com/products/purchase
