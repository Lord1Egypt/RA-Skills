# Workflow

## Goal | 目标

Update Mihomo route behavior from a user request and republish the subscription safely.

根据用户请求更新 Mihomo 路由行为，并安全地重新发布订阅。

## Build Order | 构建顺序

1. normalize the user request
2. resolve the target group
3. edit the canonical source file
4. regenerate worker artifacts
5. validate locally
6. deploy worker
7. trigger subscription sync
8. verify live output
9. optionally restart local Mihomo
10. optionally commit and push

## Core Rule | 核心规则

The workflow is not complete until the live subscription endpoint shows the new content.

只有当线上订阅端点已经返回新内容时，这个流程才算完成。
