# EXTEND.md 配置格式

EXTEND.md 文件用于自定义 panda-git-commit 的行为。使用 Markdown 格式，按 `##` 标题分区。

## 配置文件路径

| 路径                                                       | 作用域   | 说明                       |
| ---------------------------------------------------------- | -------- | -------------------------- |
| `.panda-skills/panda-git-commit/EXTEND.md`                 | 项目级   | 团队共享配置，可提交到 git |
| `$XDG_CONFIG_HOME/panda-skills/panda-git-commit/EXTEND.md` | XDG 配置 | 遵循 XDG 规范              |
| `$HOME/.panda-skills/panda-git-commit/EXTEND.md`           | 用户级   | 个人偏好                   |

优先级：项目级 > XDG > 用户级。

## 自动生成

运行 `/panda-git-commit --init` 可自动检测项目信息并生成 EXTEND.md，后续运行将直接读取缓存，跳过重复检测。使用 `--refresh` 可强制重新检测并覆盖。

自动生成的内容包括：Settings（语言）、Convention（规范检测结果）、Scope Mapping（monorepo 子包映射）。用户手动编辑的区块在 `--init` 时不会被覆盖（仅补充缺失区块）。

## 完整示例

```markdown
## Settings

- language: auto
- max_subject_length: 72
- body_wrap: 80
- emoji: false

## Convention

- source: commitlint
- format: conventional-commits
- types: feat, fix, docs, style, refactor, perf, test, chore, ci, build
- scope_required: false
- subject_max_length: 100

## Custom Types

- deploy: 部署相关变更
- i18n: 国际化相关
- release: 版本发布

## Scope Mapping

- packages/ui -> ui
- packages/core -> core
- packages/sdk -> sdk
- apps/admin -> admin
- apps/web -> web
- shared/ -> shared

## Scope Aliases

- frontend: web, ui
- backend: api, core

## Templates

### feat

feat({scope}): {emoji}{description}

{body}

### fix

fix({scope}): {emoji}{description}

原因：{cause}
影响：{impact}
```

## 各区块说明

### Settings

基础配置项，格式为 `- key: value`。

| Key                  | Type    | Default | Description                                                                           |
| -------------------- | ------- | ------- | ------------------------------------------------------------------------------------- |
| `language`           | string  | `auto`  | commit message 语言。`auto` 从 git log 自动检测，或显式设置 `zh` / `en` / `ja` / `ko` |
| `max_subject_length` | number  | `72`    | subject 行最大字符数                                                                  |
| `body_wrap`          | number  | `80`    | body 自动换行宽度                                                                     |
| `emoji`              | boolean | `false` | 是否在 type 前添加 emoji                                                              |

### Convention

项目 commit 规范缓存，格式为 `- key: value`。通常由 `--init` 自动生成，也可手动编写。

当此区块存在时，运行 `/panda-git-commit` 将跳过 `convention-detector.ts` 和 `scope-detector.ts` 的执行，直接使用缓存值。

| Key                   | Type    | Description                                                                  |
| --------------------- | ------- | ---------------------------------------------------------------------------- |
| `source`              | string  | 规范来源：`commitlint` / `commitizen` / `git-hooks` / `git-history` / `default` |
| `format`              | string  | 格式：`conventional-commits` / `angular` / `emoji-prefix` / `jira-prefix` / `free-form` |
| `types`               | string  | 允许的 type 列表，逗号分隔                                                  |
| `scope_required`      | boolean | scope 是否必填                                                               |
| `scope_enum`          | string  | 允许的 scope 列表，逗号分隔                                                 |
| `subject_max_length`  | number  | subject 行最大字符数                                                         |
| `subject_case`        | string  | subject 大小写规则（如 `lower-case`）                                        |
| `body_max_line_length`| number  | body 每行最大字符数                                                          |

### Custom Types

自定义 commit type，格式为 `- type_name: 描述`。

与内置 type 合并使用，不会覆盖内置类型。AI agent 在推断 type 时会考虑自定义类型。

### Scope Mapping

自定义路径 → scope 映射，格式为 `- path -> scope`。

优先级高于自动推导。路径使用前缀匹配：`packages/ui` 匹配 `packages/ui/src/Button.tsx`。

### Scope Aliases

scope 分组别名，格式为 `- alias: scope1, scope2`。

当变更涉及同一别名下的多个 scope 时，可以使用别名作为 scope，避免拆分。

### Templates

自定义 commit message 模板，按 `### type_name` 分组。

支持的变量：

| 变量            | 说明                       |
| --------------- | -------------------------- |
| `{type}`        | commit type                |
| `{scope}`       | scope 名称                 |
| `{emoji}`       | emoji 字符（未启用时为空） |
| `{description}` | 简短描述                   |
| `{body}`        | 正文内容                   |
| `{cause}`       | 变更原因（fix 类型）       |
| `{impact}`      | 影响范围（fix 类型）       |

未定义模板的 type 使用默认格式 `{type}({scope}): {description}`。
