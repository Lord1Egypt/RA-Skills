# Workflow

## Goal | 目标

Create a new repository under your own GitHub account and safely wire a local project repo to it.

在你自己的 GitHub 账户下创建新仓库，并把本地项目仓库安全接过去。

## Build Order | 构建顺序

1. inspect local repo state
2. verify SSH auth
3. check remote repo existence
4. create the repo if missing
5. add or update `origin`
6. push and set upstream
7. verify remote state
8. report what remains local-only

## Core Rule | 核心规则

Repository creation success does not mean the local project is fully published. Only committed history that was actually pushed counts as published.

仓库创建成功不代表本地项目已经完整发布。只有真正 push 出去的已提交历史，才算已发布。
