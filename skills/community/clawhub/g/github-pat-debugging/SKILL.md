---
name: github-pat-debugging
slug: github-pat-debugging
displayName: GitHub PAT Debugging
description: 排查 GitHub PAT 认证失败、401、Bad credentials、推送失败、token 看起来失效等问题。先检查命令、变量传递、路径和请求参数，再用 curl、Node、Python 或 PowerShell 交叉验证，确认后才判断权限、撤销或网络原因。适用于 GitHub API、Contents API、GitHub Pages 和 Skill 镜像推送。 Diagnose GitHub Personal Access Token failures before declaring a token expired or revoked.
description_zh: GitHub PAT 认证排障
description_en: Debug GitHub PAT failures
version: "1.0.8"
disable: false
agent_created: true
---

# github-pat-debugging

## When to use
- A GitHub API or Contents API request returns `401 Bad credentials`.
- A token is shown as active or non-expiring in GitHub, or another GitHub workflow has just succeeded.
- Different runtimes or shells are being mixed, especially Bash, Node.js, Python, PowerShell, curl, or Git.

## Steps
1. Do not conclude that the token is expired or revoked from one failed request. Record the exact endpoint, HTTP status, auth scheme, and runtime.
2. Inspect the token file without printing the token: byte count, prefix, suffix, and trailing newline. Do not expose the full secret.
3. Test the same token with an independent client. In Bash, use direct expansion for curl:
   ```bash
   TOKEN=$(cat "$HOME/.workbuddy/connectors/default/tokens/github.txt")
   curl -sS -D - -o /dev/null \\
     -H "Authorization: Bearer $TOKEN" \\
     -H "User-Agent: workbuddy-probe" \\
     -H "Accept: application/vnd.github+json" \\
     https://api.github.com/user
   ```
4. When handing the token to a child process, export it explicitly. This is a critical Bash distinction:
   - Wrong for a later command: `TOKEN=$(cat file) && node script.js` (shell variable is not exported).
   - Correct: `export TOKEN="$(cat file)" && node script.js`.
   - Also correct for one process: `TOKEN="$(cat file)" node script.js`.
5. In Node.js, check `process.env.TOKEN` only as a boolean/presence signal; never print the value. Test both `Bearer` and `token` schemes if needed.
6. Compare the results. If curl is `200` with `X-OAuth-Scopes` and Node is `401`, inspect environment propagation before token state, proxy, or GitHub account hypotheses.
7. Only after independent clients using the same secret both fail, investigate GitHub-side causes: manual deletion/revocation, secret-scanning revocation, third-party credential revocation, OAuth-app token limits, organization/enterprise policy, or expiration. GitHub documents `oauth_authorization.destroy` as a possible security-log event.
8. Distinguish **repo-existence 404 from auth 404**. A private repo returns 404 (not 403) to unauthenticated or unauthorized viewers — web pages, raw file URLs, and unauthenticated API calls all show 404. This is GitHub's standard privacy behavior, NOT evidence the repo was deleted. To confirm existence: authenticated `GET /repos/{owner}/{repo}` — HTTP 200 with `private: true` means the repo exists and the 404s are permission-based hiding. Cross-validate: authenticated API 200 + unauthenticated raw 404 = private repo working as designed.
9. After fixing the auth path, fetch the current remote blob SHA, update through the Contents API with the SHA, and verify the raw file contains the intended content.

## Pitfalls
- `VAR=value command` exports the variable only to that command; `VAR=value && command` does not export it to the later command.
- A `401` from Node with `process.env.TOKEN` unset is a local process bug, not evidence of a revoked PAT.
- A 200 from `GET /user` proves the token is valid, not that it is authorized for the write: if the Contents API write returns 403, check scope and repository access (see `references/token-failure-modes.md`) before treating the token as revoked.
- `Never used` or a stale "last used" label is weaker evidence than a live authenticated `GET /user`; use the latter for runtime validation.
- Do not print, commit, or paste a full PAT. If a token has been exposed, rotate it after completing the needed deployment.
- Do not overwrite a remote file without first retrieving its current SHA. Any Contents API write changes a public or shared repository and may become visible immediately: state the target repo and file to the user and get confirmation before writing, even when the task is framed as debugging or verification.
- A 404 on a private repo's web page or raw URL (unauthenticated) is privacy hiding, not deletion. Check with an authenticated API call before concluding the repo is gone.
- `GET /users/{name}/repos` lists **public repos only**, even with a valid token. To audit the full inventory including private repos, call `GET /user/repos?visibility=all` authenticated as that user — otherwise "repo missing" conclusions are wrong by construction.
- Shell shims and wrappers may silently drop environment variables on the way to child processes. If a token read via `env` or `$VAR` arrives empty in one runtime but works in another, read the token from its file inside the script instead of relying on env propagation.
- A token file saved with Windows CRLF line endings sends a trailing `\r` as part of the token and returns 401 regardless of validity — one more reason step 2 inspects byte count and trailing bytes before concluding anything about the token itself.

## Verification
- Run an authenticated `GET /user` with the corrected runtime and confirm HTTP 200 plus the expected login, without printing the token.
- Confirm the write response is HTTP 200/201 and record only the commit SHA.
- Read the public raw file and verify the new marker is present and stale markers are absent.
- Confirm the Contents API write included the current remote blob SHA fetched immediately before the update (not a stale or omitted SHA).
- Record the precise root cause and command correction in the project daily log.
