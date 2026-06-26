# Authentication and Repository Context

Verified against `glab 1.90.0`.

## Basic Checks

```bash
glab --version
glab auth status
git remote -v
glab repo view
```

If `glab repo view` fails outside a Git repository, switch to an explicit repository target:

```bash
glab repo view group/project
glab mr list -R group/project
glab issue list -R group/project
```

## Authentication

```bash
# Interactive login
glab auth login

# Self-hosted GitLab
glab auth login --hostname gitlab.example.org

# Non-interactive login from stdin
glab auth login --stdin < myaccesstoken.txt
glab auth login --hostname gitlab.example.org --stdin < myaccesstoken.txt

# Non-interactive login with explicit token
glab auth login --hostname gitlab.example.org --token glpat-xxxx

# Log out from one host
glab auth logout --hostname gitlab.example.org
```

`glab auth login --help` documents `api` and `write_repository` as the minimum token scopes. If a command still fails after login, verify the token and the project permissions in GitLab.

## Self-Hosted GitLab

Use an explicit host whenever the current Git remote is not enough:

```bash
GITLAB_HOST=gitlab.example.org glab repo view group/project
glab api --hostname gitlab.example.org projects/:id
glab repo view https://gitlab.example.org/group/project.git
```

## Common Failures

### `401 Unauthorized`

1. Check the current auth state:

   ```bash
   glab auth status
   ```

2. Re-authenticate against the correct host:

   ```bash
   glab auth login
   glab auth login --hostname gitlab.example.org
   ```

3. If `auth status` still shows no token, stop and ask the user to log in instead of retrying more API calls.

### `403 Forbidden`

- Verify the token belongs to the correct user.
- Verify the user has project permissions for the action.
- Re-check whether the command targets the correct GitLab instance.

### `404 Project Not Found`

1. Confirm the repository identifier:

   ```bash
   glab repo view group/project
   ```

2. If outside a repository, use `-R group/project` or a full GitLab URL instead of relying on auto-detection.

3. For self-hosted instances, set the host explicitly:

   ```bash
   GITLAB_HOST=gitlab.example.org glab repo view group/project
   ```

### `fatal: not a git repository`

Either change into the correct repository, or use an explicit target:

```bash
glab mr list -R group/project
glab issue list -R group/project
glab repo view group/project
```

### Wrong Repository or Host

Check the current Git remote before mutating anything:

```bash
git remote -v
glab repo view --output json
```

If the remote points to the wrong instance or project, do not continue until the target is explicit.
