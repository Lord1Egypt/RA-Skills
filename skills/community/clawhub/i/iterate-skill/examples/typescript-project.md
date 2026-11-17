# 示例：TypeScript 项目配置 / Example: TypeScript Project

适用于 Node.js / VS Code 插件 / Web 前端项目。

```yaml
# iterate.config.yaml
goal: "消除 TypeScript 类型错误并提升测试覆盖率"
max_rounds: 5
language: zh

dimensions:
  - correctness
  - security
  - performance
  - architecture
  - style-tests
  - tech-debt
  - frontend-backend
  - ui-ux

atomic:
  max_lines: 20
  max_adjacent_methods: 3

git:
  target_branch: main
  use_worktree: false

validation:
  command_whitelist:
    - "npm"
    - "npm run"
  commands:
    typescript:
      - "npm run lint"
      - "npm run compile"
      - "npm test"
```

触发方式：

```text
/iterate "消除 TypeScript 类型错误并提升测试覆盖率"
```

## 预期行为

1. correctness 维度检查 `any` 滥用、未处理的 Promise、错误的类型断言。
2. security 维度检查 `eval`、`dangerouslySetInnerHTML`、硬编码密钥。
3. 原子问题直接修复；架构问题（如大组件拆分、API 层重构）经你批准后执行。
4. 每轮跑 `npm run lint`、`npm run compile`、`npm test` 验证。
5. 每轮验证通过后，是否合并回 `main` 并推送由你决定：`git.auto_merge` / `git.push_per_round` 默认均为 `false`（安全默认），不会自动合并或推送。若需自动合并推送，请在 `iterate.config.yaml` 中显式开启这两个选项，并承担改动直接进入主分支/远程的风险。
