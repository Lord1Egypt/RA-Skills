# FAQ

## Does this skill require `gh`? | 这个 skill 需要 `gh` 吗？

No.

- It uses `curl` plus the GitHub API when needed
- It reads the PAT from 1Password

## Why check SSH first? | 为什么先查 SSH？

Because repo creation and repo push use different mechanisms.

- API access may work while SSH push is broken
- Early SSH validation shortens recovery time

## Why say uncommitted work is still local-only? | 为什么要强调未提交改动仍只在本地？

Because that is the actual Git boundary.

- committed history can be pushed
- uncommitted files cannot

## Should new repos default to private? | 新仓库默认私有吗？

Yes, unless the user clearly asks for public.
