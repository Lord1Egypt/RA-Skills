# GitHub Personal Repo Publisher

This skill turns a local Git project plus your own-account GitHub publishing request into a verified repo-creation, remote-wiring, and push workflow.
这个 skill 会把“本地 Git 项目 + 发布到自己 GitHub 账户”的请求，转成一条已验证的建仓库、接 remote 和推送流程。

## What This Skill Is For | 适用场景

Use it when:
适用于：

- a local project repo should be published under your own GitHub account
- the target repository may not exist yet
- `gh` may be unavailable
- account access is managed through SSH and a 1Password-stored GitHub PAT

## Validated Defaults | 已验证默认值

- GitHub owner: `grey0758`
- SSH host alias: `github-grey0758`
- PAT item: `GitHub Fine-Grained PAT - Repo Admin - grey0758`
- new repo visibility: `private`

## Important Decision Rules | 关键判断规则

- verify SSH auth before changing remotes
- create the GitHub repo first when it does not already exist
- push only committed history
- explicitly call out any remaining local-only changes

## Included Files | 包含文件

- `SKILL.md`
- `README.md`
- `WORKFLOW.md`
- `FAQ.md`
- `CHANGELOG.md`
- `agents/openai.yaml`

## ClawHub Publish Shape | ClawHub 发布方式

This folder is self-contained so it can be published to ClawHub as a single bundle.
这个目录是自包含的，可以直接作为一个 skill 包发布到 ClawHub。

```bash
clawhub publish ./skills/shared/github-personal-repo-publisher \
  --slug github-personal-repo-publisher \
  --name "GitHub Personal Repo Publisher" \
  --version 1.0.0 \
  --tags latest,github,git,repository,publish
```
