---
name: gitlab
description: GitLab operations including creating and cloning repositories, listing projects, managing issues, merge requests, branches, commits, and pipelines. Use this skill for creating/cloning GitLab repos, browsing projects, creating/updating issues and MRs, and any GitLab API interaction. Supports both API operations and git operations.
---

# GitLab Operations

This skill enables comprehensive GitLab operations including creating and cloning repositories, listing projects, managing issues, merge requests, branches, commits, pipelines, and more.

## Configuration

The GitLab skill uses a secure, layered credential management system. Credentials are loaded in the following priority order:

### 1. Environment Variables (Recommended - Most Secure) ⭐

Set GitLab credentials as environment variables:

```bash
export GITLAB_HOST="https://gitlab.example.com"
export GITLAB_TOKEN="glpat-your-token-here"
```

**Benefits:**
- Most secure approach
- Never committed to version control
- Standard practice for production systems
- Works seamlessly with CI/CD pipelines

**Generating a GitLab Access Token:**
1. Go to GitLab → User Settings → Access Tokens
2. Create a personal access token with appropriate scopes:
   - `api` - Full API access
   - `read_repository` - For repository operations
   - `write_repository` - For creating branches, commits, etc.
3. Copy the token immediately (you won't see it again)

**Persistent Configuration:**
Add to your shell profile (~/.bashrc, ~/.zshrc, etc.):
```bash
export GITLAB_HOST="https://gitlab.example.com"
export GITLAB_TOKEN="glpat-your-token-here"
```

### 2. User Configuration File

Create a configuration file in your home directory:

```bash
mkdir -p ~/.claude
cat > ~/.claude/gitlab_config.json << 'EOF'
{
  "host": "https://gitlab.example.com",
  "access_token": "glpat-your-token-here"
}
EOF

chmod 600 ~/.claude/gitlab_config.json  # Restrict file permissions
```

**Location:** `~/.claude/gitlab_config.json`

**Benefits:**
- Secure location outside skill directory
- Won't be accidentally committed
- Easy to manage multiple GitLab instances
- Supports file-based automation

### 3. Runtime Prompt (Fallback)

If credentials are not found in environment variables or config files, the skill can prompt for credentials interactively (when the `--allow-prompt` flag is used):

```bash
python3 scripts/gitlab_api.py projects --allow-prompt
```

**Note:** This is not recommended for automation or CI/CD pipelines.

### Configuration Priority

The skill loads credentials in this order (first match wins):

1. **Environment Variables** (`GITLAB_HOST`, `GITLAB_TOKEN`) - Highest Priority
2. **User Config File** (`~/.claude/gitlab_config.json`)
3. **Legacy Config** (`scripts/config.json` - deprecated, shows warning)
4. **Runtime Prompt** (only if `--allow-prompt` flag is used)

### Example Config File Template

An example configuration template is available at `scripts/config.example.json`:

```json
{
  "host": "https://gitlab.example.com",
  "access_token": "glpat-your-token-here"
}
```

### Important Security Notes

**DO:**
✅ Use environment variables for production systems
✅ Store user config in `~/.claude/gitlab_config.json`
✅ Restrict file permissions: `chmod 600 ~/.claude/gitlab_config.json`
✅ Use different tokens for different environments
✅ Rotate tokens regularly

**DON'T:**
❌ Commit credentials to version control
❌ Store real tokens in `scripts/config.json`
❌ Share access tokens in chat logs or output
❌ Use the same token across multiple environments
❌ Print or log access tokens

### SSL Certificate Issues

For internal GitLab instances with self-signed certificates, use the `--insecure` flag:

```bash
python3 scripts/gitlab_api.py projects --insecure
```

This bypasses SSL certificate verification (useful for development/testing but not recommended for production).

### Testing Credential Loading

Test that credentials are configured correctly:

```bash
# Test using credential loader directly
python3 scripts/credential_loader.py --show-source

# List projects to verify API access
python3 scripts/gitlab_api.py projects

# Check which credential source is being used
python3 scripts/gitlab_api.py projects --allow-prompt
```

### Troubleshooting

**Problem:** "GitLab credentials not configured"

**Solutions:**
1. Check environment variables: `echo $GITLAB_HOST $GITLAB_TOKEN`
2. Check user config: `cat ~/.claude/gitlab_config.json`
3. Verify token is valid and not expired
4. Ensure token has required API scopes

**Problem:** "Authentication failed (401)"

**Solutions:**
1. Verify token hasn't expired or been revoked
2. Check token has required scopes (`api`, `read_repository`, etc.)
3. Ensure token format is correct (starts with `glpat-`)
4. Test token manually:
   ```bash
   curl -H "PRIVATE-TOKEN: $GITLAB_TOKEN" "$GITLAB_HOST/api/v4/user"
   ```

**Problem:** "Resource not found (404)"

**Solutions:**
1. Verify GitLab host URL is correct
2. Check project ID or path
3. Ensure user has access to the project
4. Test with `python3 scripts/gitlab_api.py projects` to list accessible projects

### Migration from Old Configuration

If you have an existing `scripts/config.json` file:

1. **Immediate Action:** Move credentials to secure location
   ```bash
   # Export to environment variables
   export GITLAB_HOST=$(jq -r '.host' scripts/config.json)
   export GITLAB_TOKEN=$(jq -r '.access_token' scripts/config.json)

   # Or move to user config
   mkdir -p ~/.claude
   cp scripts/config.json ~/.claude/gitlab_config.json
   chmod 600 ~/.claude/gitlab_config.json
   ```

2. **Replace config.json with placeholder:**
   ```bash
   cat > scripts/config.json << 'EOF'
   {
     "_comment": "This file is deprecated",
     "host": "https://gitlab.example.com",
     "access_token": "glpat-your-token-here"
   }
   EOF
   ```

3. **Verify new configuration works:**
   ```bash
   python3 scripts/credential_loader.py --show-source
   python3 scripts/gitlab_api.py projects
   ```

## Common Operations

### Create Repository

When the user wants to create a new GitLab repository:

1. Prompt for required information:
   - Project name (required)
   - Description (optional)
   - Visibility level: public, private, or internal (optional, defaults to private)
   - Namespace/group path (optional, defaults to user's personal namespace)
   - Initialize with README (optional, defaults to false)
2. Use POST `/api/v4/projects` endpoint with the provided parameters
3. Include additional options if specified:
   - `initialize_with_readme`: Create repository with initial README
   - `default_branch`: Set default branch name (defaults to "main")
   - `wiki_enabled`: Enable wiki (defaults to true)
   - `issues_enabled`: Enable issues (defaults to true)
   - `merge_requests_enabled`: Enable merge requests (defaults to true)
   - `jobs_enabled`: Enable CI/CD pipelines (defaults to true)
4. Handle response and provide:
   - Project URL
   - Git clone URL
   - Web URL
   - Project ID
   - Confirmation with formatted Markdown output

**Example output format:**

```markdown
## ✅ Repository Created Successfully

**Project**: my-project
**Project ID**: 123
**Visibility**: Private
**URL**: [View Project](https://gitlab.example.com/username/my-project)
**Clone**: `git clone https://gitlab.example.com/username/my-project.git`
```

**Error handling:**
- Name already exists: Suggest alternative names
- Invalid namespace: List available namespaces
- Permission denied: Check user permissions and token scopes

### Clone Repository

When the user wants to clone a GitLab repository:

1. Parse the repository URL to extract the project path and host
2. Verify the host matches the configured GitLab instance in `config.json`
3. If authentication is required for private repositories, use the access token from config
4. Clone to the specified directory or current directory if not specified
5. Use git clone with appropriate authentication:
   - For HTTPS: use token as password
   - For SSH: use git@host:project-path.git format
6. Confirm successful clone with repository path and brief info

**Example workflow:**
```
User: "clone https://gitlab.example.com/group/project to ./myproject"
Action:
1. Extract host (gitlab.example.com) and project path (group/project)
2. Run git clone with authentication
3. Confirm: "✅ Cloned to ./myproject"
```

**Authentication note:** For private repos requiring HTTPS auth, embed token in URL: `https://oauth2:TOKEN@host/project.git`

### List Repositories/Projects

When the user wants to see their GitLab repositories:

1. Load configuration from `config.json`
2. Fetch all projects using the GitLab API (`/api/v4/projects`)
3. Use `membership=true` to show only projects the user is a member of
4. Sort by `updated_at` descending to show recently updated projects first
5. Handle pagination automatically to fetch all projects
6. Output results in Markdown format with:
   - Project count summary
   - Formatted table with: Name, Visibility, Last Updated, URL
   - Group/namespace information if relevant
   - Links to each project

**Example output format:**

```markdown
## Found 25 GitLab Projects

| Name | Visibility | Last Updated | URL |
|------|------------|--------------|-----|
| group/project-name | Public | 2025-04-02 | [View](https://gitlab.example.com/group/project-name) |
...
```

### Search Projects

When the user wants to search for specific projects:

1. Use the `/api/v4/projects` endpoint with `search=<query>` parameter
2. Filter by visibility if requested (`visibility=public|private|internal`)
3. Limit results to top 20 matches unless more are requested
4. Output in Markdown table format

### Project Details

When the user asks about a specific project:

1. Use `/api/v4/projects/:id` endpoint (project ID or path-encoded URL)
2. Fetch detailed information including:
   - Description, default branch, star count, forks count
   - Last activity date
   - Repository size
   - Permissions
3. Output in formatted Markdown with sections for each detail category

### Issues

**List issues:**
- Use `/api/v4/projects/:id/issues` for project-specific issues
- Use `/api/v4/issues` for all issues across projects
- Support filtering: state (opened/closed), labels, milestone, assignee
- Output in Markdown table with: ID, Title, State, Author, Assignee, Updated, Link

**Create issue:**
- Use POST `/api/v4/projects/:id/issues`
- Required: title
- Optional: description, labels, assignee_id, milestone_id
- Ask user for missing required information
- Confirm creation and show the issue URL

**Get issue details:**
- Use GET `/api/v4/projects/:id/issues/:issue_iid`
- Fetch complete issue information including description, labels, assignees
- Output formatted Markdown with all issue details
- Show state icon (🟢 opened, 🔴 closed), author, assignees, labels, milestone
- Display full description and link to issue in GitLab
- Handle missing fields gracefully with "None" or "Unassigned" placeholders

**Update issue:**
- Use PUT `/api/v4/projects/:id/issues/:issue_iid`
- Allow updating title, description, state, labels, etc.
- Confirm changes and show updated issue link

### Merge Requests

**List merge requests:**
- Use `/api/v4/projects/:id/merge_requests` for project-specific MRs
- Use `/api/v4/merge_requests` for all MRs across projects
- Support filtering: state (opened/closed/merged), author, assignee, labels
- Output in Markdown table with: IID, Title, State, Author, Target Branch, Source Branch, Link

**Create merge request:**
- Use POST `/api/v4/projects/:id/merge_requests`
- Required: source_branch, target_branch, title
- Optional: description, assignee_id, labels, remove_source_branch
- Ask user for missing required information
- Confirm creation and show MR URL

**Show MR details:**
- Fetch MR with discussions, changes, and pipeline status
- Output comprehensive Markdown with:
  - Basic info (title, state, branches, author)
  - Changes summary (files changed, additions, deletions)
  - Pipeline status if available
  - Recent discussions/comments

### Branches

**List branches:**
- Use `/api/v4/projects/:id/repository/branches`
- Show name, protected status, commit info, last commit date
- Output in Markdown table

**Create branch:**
- Use POST `/api/v4/projects/:id/repository/branches`
- Required: branch_name, ref (starting branch or commit SHA)
- Confirm creation with branch details including:
  - Branch name and protection status (🔒 protected icon)
  - Latest commit SHA, message, author, and date
  - Link to branch in GitLab
- Handle errors gracefully:
  - Branch already exists (400 error)
  - Invalid branch name or ref (400 error)
  - Invalid project or insufficient permissions (403/404 errors)

**Delete branch:**
- Use DELETE `/api/v4/projects/:id/repository/branches/:branch`
- Warn before deletion
- Confirm deletion

### Commits

**List commits:**
- Use `/api/v4/projects/:id/repository/commits`
- Support filtering: ref_name (branch), since, until, author
- Show short SHA, author, message, date
- Output in Markdown table with links to commit diffs

**Show commit details:**
- Use `/api/v4/projects/:id/repository/commits/:sha`
- Show full commit message, author, committer, file changes
- Display diff summary

### Pipelines

**List pipelines:**
- Use `/api/v4/projects/:id/pipelines`
- Show ID, status, ref, user, created date, duration
- Output in Markdown table with status indicators (✅ ✗ ⏳)

**Show pipeline details:**
- Fetch pipeline jobs and stages
- Display job status, duration, and logs URLs
- Show overall pipeline status and timing

## Error Handling

When encountering errors:

1. **Authentication failed (401/403)**: 
   - Inform user the access token may be invalid or lacks required permissions
   - Suggest checking `config.json` or generating a new token with appropriate scopes

2. **Project not found (404)**:
   - Verify project ID or path
   - Check if user has access to the project
   - Suggest listing projects to find the correct ID

3. **Rate limiting (429)**:
   - Inform user about rate limits
   - Suggest waiting before retrying

4. **Network errors**:
   - Check if GitLab host is reachable
   - Verify network connection
   - For internal GitLab instances with self-signed certificates, handle SSL verification appropriately

5. **Invalid parameters**:
   - Explain what parameter was invalid
   - Provide guidance on correct values
   - Show API documentation links if relevant

## API Pagination

For endpoints that return paginated results:
1. Check `x-total-pages` header
2. Iterate through all pages to fetch complete results
3. For large result sets (>100 items), ask user if they want all results or just the first N
4. Show progress when fetching multiple pages

## Output Formatting Principles

1. **Use Markdown for all human-readable output** - tables, lists, code blocks
2. **Include links to relevant GitLab resources** - project URLs, issue links, MR links
3. **Show counts and summaries** - total results, filtered counts
4. **Use visual indicators for status** - ✅ for success, ✗ for failure, ⏳ for pending
5. **Format dates in readable format** - YYYY-MM-DD or relative time (2 days ago)
6. **Truncate long text** - commit messages, descriptions, with option to show full text
7. **Group related information** - use headers and sections for complex outputs

## Interactive Workflows

For complex operations requiring multiple steps:

1. **Ask for confirmation** before destructive operations (delete, close, etc.)
2. **Offer choices** when there are multiple valid approaches
3. **Suggest next actions** after completing an operation (e.g., after creating an issue, ask if they want to create another)
4. **Handle ambiguous inputs** - if a project name is ambiguous, show matching projects and ask user to select

## Example Workflows

**User asks**: "Show me my open merge requests"

**Action**:
1. Fetch MRs from all projects using `/api/v4/merge_requests?state=opened`
2. Group by project
3. Output in Markdown table with project name, MR details, and links

**User asks**: "Create an issue in myproject about the login bug"

**Action**:
1. Load config.json
2. Find project ID for "myproject"
3. Ask for issue details if not provided (description, labels, assignee)
4. Create the issue via API
5. Confirm creation and show issue URL

**User asks**: "What's the status of the main branch in project-group/webapp?"

**Action**:
1. Find project by name/path
2. Fetch branch details for "main"
3. Show commit info, protection status
4. Optionally show recent commits or pipeline status

## Notes

- All API calls should include the access token in the `PRIVATE-TOKEN` header
- Use proper SSL/TLS handling for internal GitLab instances with self-signed certificates
- Respect rate limits and implement exponential backoff if needed
- Cache project ID lookups when appropriate to avoid repeated API calls
