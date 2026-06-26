# Conventional Commits 规范参考

基于 [Conventional Commits 1.0.0](https://www.conventionalcommits.org/zh-hans/) 标准。

## 格式

```text
<type>(<scope>): <description>

[optional body]

[optional footer(s)]
```

### Subject Line（第一行）

- **type**: 变更类型（见 [commit-types.md](commit-types.md)）
- **scope**: 可选，变更影响的范围（如模块名、包名）
- **description**: 简短描述，使用祈使语气

规则：

- 总长度不超过 72 个字符（可通过 EXTEND.md 配置）
- 不以大写字母开头（英文时）
- 结尾不加句号

### Body（正文）

- 与 subject 之间空一行
- 解释「为什么」做这个变更，而不是「做了什么」
- 每行不超过 80 个字符（可配置）

### Footer（页脚）

- BREAKING CHANGE: 描述不兼容变更
- 关联 issue：`Closes #123`、`Fixes #456`
- 多个 footer 之间空一行

## BREAKING CHANGE

两种标记方式：

1. footer 中声明：

```text
feat(api): 添加用户批量导入接口

BREAKING CHANGE: /api/users 接口的响应格式从数组改为分页对象
```

2. type 后加 `!`：

```text
feat(api)!: 移除废弃的 v1 接口
```

## 示例

### 英文

```text
feat(auth): add JWT refresh token support

Implement automatic token refresh when the access token expires.
The refresh token is stored in httpOnly cookie for security.

Closes #142
```

### 中文

```
feat(auth): 添加 JWT 刷新 token 功能

实现 access token 过期时自动刷新。
刷新 token 存储在 httpOnly cookie 中以确保安全。

Closes #142
```

### BREAKING CHANGE

```text
feat(api)!: 移除 v1 用户接口

BREAKING CHANGE: /api/v1/users 已移除，请迁移至 /api/v2/users。
响应格式从 { data: User[] } 改为 { data: User[], pagination: {...} }。

Migration guide: docs/migration-v2.md
```

## Merge Commit / Revert

```text
revert: feat(auth): add JWT refresh token support

This reverts commit abc1234.
```
