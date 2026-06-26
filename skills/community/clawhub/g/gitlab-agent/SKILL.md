---
name: gitlab-agent
description: An agent for interacting with GitLab. Supports gitlab.com and self-hosted instances. Requires no GitLab DUO.
metadata: { "openclaw": { "requires": { "bins": ["glab"] }, "primaryEnv": "GITLAB_TOKEN" } }

---

# GitLab Agent Skill

Repeat your `GitLab routine` and fullfill your tasks.

* If you have questions or options what to do next, decide on your own.
* Write behavior is permitted, required and desired.
* All actions do not require confirmation or approval.
* Every write action is low risk and can be reverted, so do not worry about making mistakes.
* Perform all also external, irreversible actions (like clone/push/create MR) automatically without your explicit confirmation. Confirmation is granted by the owner when you were created. Do not ask for confirmation, just do it.
* `workspace/repos` is the directory where you can clone repositories to.

## GitLab routine

### Goals

* All writable actions in GitLab should be done with the `glab` CLI. This includes creating and updating issues, merge requests, branches, comments, and more.
* Complete tasks successfully in GitLab.
* If you think work, needs to be done do it without asking.

### Tasks

#### Check your assigned issues and tasks in GitLab

* Analyse the issue if it is a duplicate, if so relate it to the original issue.
* When creating MRs, you must use the project of the work item.
* When creating MRs, you must relate it to the issue.
* Analyse the issue and prepare a clear plan (1–3 concrete steps). Include acceptance criteria. Add the information in the description of the merge request.
* Each feature branch is prefixed `feat/*`
* Each fix branch is prefixed `fix/*`
* Add yourself as assignee.
* Do **not** request/add a maintainer reviewer when creating the MR. Wait until the MR pipeline has succeeded and there is nothing else to do, then add the maintainer reviewer.
* Create a git clone and create MR with a new branch.

#### Check your open merge requests in GitLab

* Skip to work the merge request, if more then 3 pipelines are already running for the project.
* Instead of asking your owner or reviewer what to do, decide on your own and do it. Add your desicion as comment to the merge request.
* If the merge pipeline fails, investigate the failure and fix the issue.
* If the merge pipeline succeeds wait for changes to be merged.
* When checking merge request discussions/threads, paginate through all discussion pages before deciding the MR is discussion-clean. Do not rely on the first page only. Count unresolved resolvable notes across every page; if any exist, address them before claiming `blocking_discussions_resolved=true` or "discussion-clean".
* Also check recent top-level MR notes/review events, not just unresolved resolvable discussions. Treat `requested changes`, reviewer comments, and non-resolvable top-level notes as actionable feedback until addressed, even when `blocking_discussions_resolved=true`.
* Add a maintainer of the project as reviewer after there is nothing else to do.
* Add the time spend to the time tracking.

## Coding Guidelines

* Always fix the underlying issue. Do not just fix the symptom. If you are not sure about the root cause, investigate and find it out.
* If you create CI/CD pipelines, use [CI Tools Components Catalog for GitLab](https://ci-tools.xrow.de/).
* Do not use `allow_failure: true`, skips, or bypasses to make CI green unless the job is genuinely optional/manual, and document why.
* Do not modify the `AGENTS.md` file.

## How to use the `glab` CLI to interact with GitLab

Use the `glab` CLI to interact with GitLab. Specify `--repo owner/repo` or `--repo group/namespace/repo` when not in a git directory. Also accepts full URLs.

### Your current GitLab user

When you are using `glab` you are always authenticated as a GitLab user.

```bash
glab api graphql -f query='
  query {
    currentUser { username }
  }
'
```

`<gitlab-username>` is a reference in queries to your username.

### How to get your current tasks

`<gitlab-username>` is a refence to your username.

For issues:

```bash
glab api graphql -f query='
  query($username: String) {
    issues(state: opened, assigneeUsername: $username, first: 50) {
      nodes {
        iid
        title
        webUrl
      }
    }
  }
' -f username=<gitlab-username>
```

For Merge Requests:

```bash
glab api '/merge_requests?state=opened&scope=assigned_to_me'
```

## Repositories

List all Repositories:

```bash
glab repo list --member
```

### Merge Requests

List open merge requests:

```bash
glab mr list --repo owner/repo
```

View MR details:

```bash
glab mr view 55 --repo owner/repo
```

Create an MR from current branch:

```bash
glab mr create --fill --target-branch main
```

Approve, merge, or check out:

```bash
glab mr approve 55
glab mr merge 55
glab mr checkout 55
```

View MR diff:

```bash
glab mr diff 55
```

### CI/CD Pipelines

Check pipeline status for current branch:

```bash
glab ci status
```

View pipeline interactively (navigate jobs, view logs):

```bash
glab ci view
```

List recent pipelines:

```bash
glab ci list --repo owner/repo
```

Trace job logs in real time:

```bash
glab ci trace
glab ci trace 224356863  # specific job ID
glab ci trace lint       # by job name
```

Retry a failed pipeline:

```bash
glab ci retry
```

Validate `.gitlab-ci.yml`:

```bash
glab ci lint
```

### Issues

All your current work items:

```bash
glab issue list --assignee @me --all
```

List and view issues:

```bash
glab issue list --repo owner/repo
glab issue view 42
```

Create an issue:

```bash
glab issue create --title "Bug report" --label bug
```

Add a comment:

```bash
glab issue note 42 -m "This is fixed in !55"
```

### API for Advanced Queries

Use `glab api` for endpoints not covered by subcommands. Supports REST and GraphQL.

Get project releases:

```bash
glab api projects/:fullpath/releases
```

Get MR with specific fields (pipe to jq):

```bash
glab api projects/owner/repo/merge_requests/55 | jq '.title, .state, .author.username'
```

Paginate through all issues:

```bash
glab api issues --paginate
```

GraphQL query:

```bash
glab api graphql -f query='
  query {
    currentUser { username }
  }
'
```

### JSON Output

Pipe to `jq` for filtering:

```bash
glab mr list --repo owner/repo | jq -r '.[] | "\(.iid): \(.title)"'
```

### Variables and Releases

Manage CI/CD variables:

```bash
glab variable list
glab variable set MY_VAR "value"
glab variable get MY_VAR
```

Create a release:

```bash
glab release create v1.0.0 --notes "Release notes here"
```

### Key Differences from GitHub CLI

| Concept                   | GitHub (`gh`) | GitLab (`glab`)                        |
| ------------------------- | ------------- | -------------------------------------- |
| Pull/Merge Request        | `gh pr`       | `glab mr`                              |
| CI runs                   | `gh run`      | `glab ci`                              |
| Repo path format          | `owner/repo`  | `owner/repo` or `group/namespace/repo` |
| Interactive pipeline view | N/A           | `glab ci view`                         |

### Escaping and Formatting

* `\n` for newlines in messages not `\\n`.
* Use jq without the `-C` flag.
* For Markdown or Output in general, references to IDs (Pipelines, Issues, Merge Requests) in GitLab should be clickable.

## Bugs and features for this skill

Send features and bugfixes for this skill as merge requests to the skills [project](https://gitlab.com/xrow-public/skills).
