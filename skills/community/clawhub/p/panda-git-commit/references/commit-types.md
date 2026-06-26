# Commit Types 定义

## 内置 Types

| Type       | Emoji | 中文说明 | English                             | SemVer 影响 |
| ---------- | ----- | -------- | ----------------------------------- | ----------- |
| `feat`     | ✨    | 新功能   | A new feature                       | MINOR       |
| `fix`      | 🐛    | Bug 修复 | A bug fix                           | PATCH       |
| `docs`     | 📝    | 文档变更 | Documentation only                  | -           |
| `style`    | 💄    | 代码格式 | Code style (formatting, whitespace) | -           |
| `refactor` | ♻️    | 代码重构 | Code refactoring (no feat, no fix)  | -           |
| `perf`     | ⚡    | 性能优化 | Performance improvement             | PATCH       |
| `test`     | ✅    | 测试相关 | Adding or updating tests            | -           |
| `chore`    | 🔧    | 杂项维护 | Maintenance, dependencies           | -           |
| `ci`       | 👷    | CI/CD    | CI/CD configuration                 | -           |
| `build`    | 📦    | 构建系统 | Build system, external deps         | -           |

## Type 推断规则

根据变更文件的特征自动推断 type：

| 文件特征                                                                               | 推断 Type                                      |
| -------------------------------------------------------------------------------------- | ---------------------------------------------- |
| 全部是 `.test.ts` / `.spec.ts` / `__tests__/`                                          | `test`                                         |
| 全部是 `.md` / `.txt` / `docs/`                                                        | `docs`                                         |
| 全部是 `.github/` / `.gitlab-ci` / `Jenkinsfile`                                       | `ci`                                           |
| 全部是 `package.json` / `tsconfig.json` / `Dockerfile` / `webpack.*` / `vite.config.*` | `build`                                        |
| 全部是 `.css` / `.scss` / `.less` / `.styled.ts`                                       | `style`                                        |
| 包含新增文件（status = added）                                                         | `feat`                                         |
| 其他情况                                                                               | `feat`（由 AI agent 根据 diff 内容进一步判断） |

## 自定义 Types

通过 EXTEND.md 添加自定义 type：

```markdown
## Custom Types

- deploy: 部署相关变更
- i18n: 国际化相关
- release: 版本发布
- wip: 开发中（work in progress）
```

自定义 type 与内置 type 合并使用，不会覆盖内置类型。

## Emoji 模式

启用 `--emoji` 或在 EXTEND.md 设置 `emoji: true` 后，commit message 格式变为：

```text
✨ feat(auth): 添加 JWT 刷新 token 功能
```

Emoji 放在 type 之前。可通过 EXTEND.md 自定义 emoji 映射。
