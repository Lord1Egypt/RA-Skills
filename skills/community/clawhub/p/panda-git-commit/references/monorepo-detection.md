# Monorepo 检测策略

## 检测顺序

按以下顺序检测，命中即停止：

| 优先级 | 配置文件                           | 工具                  |
| ------ | ---------------------------------- | --------------------- |
| 1      | `package.json` → `workspaces` 字段 | npm / yarn workspaces |
| 2      | `pnpm-workspace.yaml`              | pnpm workspaces       |
| 3      | `lerna.json`                       | Lerna                 |
| 4      | `nx.json`                          | Nx                    |
| 5      | `turbo.json`                       | Turborepo             |

## Workspace 目录解析

### npm / yarn workspaces

读取 `package.json` 的 `workspaces` 字段：

```json
{
  "workspaces": ["packages/*", "apps/*"]
}
```

或 yarn 格式：

```json
{
  "workspaces": {
    "packages": ["packages/*", "apps/*"]
  }
}
```

### pnpm workspaces

读取 `pnpm-workspace.yaml`：

```yaml
packages:
  - 'packages/*'
  - 'apps/*'
  - 'tools/*'
```

### Lerna

读取 `lerna.json` 的 `packages` 字段（默认 `["packages/*"]`）：

```json
{
  "packages": ["packages/*", "modules/*"]
}
```

### Nx

检测到 `nx.json` 后，扫描默认目录：`packages/*`、`apps/*`、`libs/*`。

### Turborepo

检测到 `turbo.json` 后，优先读取 `package.json` 的 workspaces 字段，否则扫描默认目录：`packages/*`、`apps/*`。

## Glob 展开

配置中的 `*` 通配符会展开为实际子目录。例如 `packages/*` 在以下结构中：

```text
packages/
├── core/
├── ui/
└── utils/
```

展开为：`packages/core`、`packages/ui`、`packages/utils`。

## Scope 推导

### Monorepo 项目

变更文件路径匹配 workspace 目录时，读取该子包的 `package.json`（Nx 项目优先读 `project.json`）中的 `name` 字段作为 scope。如果 `name` 字段不存在，才兜底使用目录名。

**各工具的包标识来源（来自官方文档）**：

| 工具 | 标识来源 |
| ---- | -------- |
| npm/yarn workspaces | 子包 `package.json` 的 `name` 字段 |
| pnpm workspaces | 子包 `package.json` 的 `name` 字段 |
| Lerna | 子包 `package.json` 的 `name` 字段 |
| Nx | `project.json` 的 `name` > `package.json` 的 `name` > 路径推断 |
| Turborepo | 子包 `package.json` 的 `name` 字段 |

**示例**：

假设以下 monorepo 结构：

```text
packages/
├── core/package.json      → { "name": "@myorg/core" }
├── ui-components/package.json → { "name": "@myorg/ui" }
└── utils/package.json     → { "name": "shared-utils" }
```

| 变更文件 | Workspace 目录 | package.json name | Scope |
| -------- | -------------- | ----------------- | ----- |
| `packages/core/src/index.ts` | `packages/core` | `@myorg/core` | `@myorg/core` |
| `packages/ui-components/src/Button.tsx` | `packages/ui-components` | `@myorg/ui` | `@myorg/ui` |
| `packages/utils/format.ts` | `packages/utils` | `shared-utils` | `shared-utils` |

### 非 Monorepo 项目

按目录结构推导：

| 变更文件                    | 推导规则            | Scope        |
| --------------------------- | ------------------- | ------------ |
| `src/components/Button.tsx` | `src/` 下取次级目录 | `components` |
| `src/utils/format.ts`       | `src/` 下取次级目录 | `utils`      |
| `server/api/users.ts`       | 取顶级目录          | `server`     |
| `README.md`                 | 根目录文件          | `null`       |

### 多 Scope 场景

当变更文件跨越多个 scope 时：

- 2 个 scope → 建议拆分，或使用逗号分隔：`feat(core,ui): ...`
- 3+ 个 scope → 强烈建议拆分为独立 commit

### EXTEND.md 自定义映射

用户可在 EXTEND.md 中定义自定义路径 → scope 映射，优先级高于自动推导：

```markdown
## Scope Mapping

- packages/ui -> ui
- packages/core -> core
- shared/ -> shared
- config/ -> config
```
