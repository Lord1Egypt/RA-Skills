# Onboarding Playbook（仅供参考 / For Reference Only）

> ⚠️ 本文档为 AI onboarding 提供参考映射和建议。AI 必须根据实际项目扫描结果调整，
> 不得机械套用。以下维度推荐和命令候选仅为起点，最终方案需结合项目实况和用户确认。
>
> ⚠️ This document provides reference mappings for AI onboarding. The AI MUST adjust
> based on actual project scan results and must not apply them mechanically.
> The dimension recommendations and command candidates below are starting points only;
> the final plan must reflect the actual project state and user confirmation.

---

## 1. 扫描清单 / Scan Checklist

AI onboarding 时应并行检查以下内容（均为只读操作）：

| 检查项 / Check | 目标文件 / Target | 用途 / Purpose |
|---|---|---|
| Manifest 文件 | `package.json`, `pyproject.toml`, `setup.py`, `requirements.txt`, `Package.swift`, `go.mod`, `Cargo.toml`, `pom.xml`, `build.gradle`, `build.gradle.kts`, `Gemfile`, `composer.json`, `mix.exs`, `pubspec.yaml`, `tsconfig.json` | 识别技术栈和包管理器 |
| 目录结构 | 项目根目录下 2-3 层目录树 | 生成模块地图，识别前后端边界 |
| specs 目录 | `specs/`, `spec/`, `docs/specs/` | 判断是否启用 spec-compliance 维度 |
| 测试目录 | `tests/`, `test/`, `__tests__/`, `spec/` | 判断测试覆盖情况 |
| CI 配置 | `.github/workflows/`, `.gitlab-ci.yml`, `Jenkinsfile`, `.circleci/` | 了解已有验证流程 |
| 上下文文件 | `README.md`, `CLAUDE.md`, `PROJECT.md`, `CONTRIBUTING.md` | 提取已有项目描述和约定 |
| 源码目录 | `src/`, `lib/`, `app/`, `cmd/`, `internal/` | 识别主代码位置 |

**禁止扫描 / Never Scan:**
`.env`, `.env.*`, `*.key`, `*.pem`, `*.p12`, `*.crt`, `*.cer`,
`credentials.json`, `.aws/`, `.ssh/`, `secrets/`, `node_modules/`, `__pycache__/`

---

## 2. 技术栈 → 审查维度映射 / Tech Stack → Dimension Mapping

以下为默认推荐，AI 应根据项目实际模块结构调整。

### 通用基础维度（所有项目推荐启用）

| 维度 / Dimension | 优先级 / Priority | 理由 / Reason |
|---|---|---|
| correctness | critical | 任何项目都需要 |
| security | critical | 任何项目都需要 |
| performance | high | 任何项目都需要 |
| architecture | high | 任何项目都需要 |
| style-tests | medium | 任何项目都需要 |
| tech-debt | medium | 任何项目都需要 |

### 按技术栈追加维度

| 技术栈 / Tech Stack | 追加维度 / Additional Dimensions | 理由 / Reason |
|---|---|---|
| JavaScript / TypeScript（含前端） | `frontend-backend`, `ui-ux` | 有前端 UI 层 |
| Swift（iOS/macOS app） | `ui-ux` | 有 UI 层 |
| Dart/Flutter | `frontend-backend`, `ui-ux` | 有前端 UI 层 |
| Kotlin/Java（Android） | `ui-ux` | 有 UI 层 |
| 纯后端 API（任何语言） | `frontend-backend` | 有 API 契约 |
| 有 specs/ 目录（任何语言） | `spec-compliance` | 有规范文档可对照 |
| 无前端（CLI 工具、库、服务） | 无追加 | 不需要 ui-ux |

### 维度禁用建议

| 场景 / Scenario | 建议禁用 / Suggest Disable | 理由 / Reason |
|---|---|---|
| 无 specs/ 目录 | spec-compliance | 无规范可对照，空转浪费算力 |
| 无前端 UI | ui-ux | 不适用 |
| 纯库项目（无 API 层） | frontend-backend | 不适用 |

---

## 3. 技术栈 → 验证命令候选 / Tech Stack → Validation Command Candidates

以下命令为常见候选，**必须根据项目实际配置（package.json scripts、Makefile 等）调整**。

### Python

| 类型 / Type | 命令候选 / Command Candidate | 备注 / Note |
|---|---|---|
| Lint | `ruff check src/` | 若项目使用 ruff |
| Lint | `flake8 src/` | 若项目使用 flake8 |
| Type check | `mypy src/ --ignore-missing-imports` | 若项目使用 mypy |
| Test | `pytest tests/ -x -q` | 常见 pytest 命令 |
| Test | `python -m unittest discover -s tests` | 若使用 unittest |

### JavaScript / TypeScript

| 类型 / Type | 命令候选 / Command Candidate | 备注 / Note |
|---|---|---|
| Lint | `npm run lint` | 检查 package.json scripts |
| Type check | `npm run typecheck` 或 `tsc --noEmit` | TypeScript 项目 |
| Build | `npm run build` | 编译检查 |
| Test | `npm test` 或 `npm run test` | 检查 package.json scripts |
| Test | `yarn test` / `pnpm test` | 若使用 yarn/pnpm |

### Swift

| 类型 / Type | 命令候选 / Command Candidate | 备注 / Note |
|---|---|---|
| Build | `swift build -c debug` | SwiftPM |
| Test | `swift test` | SwiftPM |
| Lint | `swiftlint lint --path Sources/` | 若安装了 SwiftLint |

### Go

| 类型 / Type | 命令候选 / Command Candidate | 备注 / Note |
|---|---|---|
| Vet | `go vet ./...` | 标准工具 |
| Build | `go build ./...` | 编译检查 |
| Test | `go test ./...` | 标准测试 |

### Rust

| 类型 / Type | 命令候选 / Command Candidate | 备注 / Note |
|---|---|---|
| Lint | `cargo clippy` | 标准工具 |
| Build | `cargo build` | 编译检查 |
| Test | `cargo test` | 标准测试 |

### Java / Kotlin

| 类型 / Type | 命令候选 / Command Candidate | 备注 / Note |
|---|---|---|
| Build | `mvn compile` 或 `gradle compileJava` | 取决于构建工具 |
| Test | `mvn test` 或 `gradle test` | 取决于构建工具 |

---

## 4. 常见 Iterate 注意点 / Common Iterate Notes

以下注意点应写入 ITERATE.md 的"Iterate 注意点"区，AI 根据项目实况筛选和调整。

### 通用注意点

- 审查时跳过自动生成文件（`*.generated.*`, `dist/`, `build/`）。
- 不要修改锁文件（`package-lock.json`, `poetry.lock`, `Cargo.lock` 等）的内容，除非有明确依赖变更。
- 每轮修复后运行项目配置的验证命令，验证失败即回滚。

### Python 项目

- 注意 `__init__.py` 的导出变更可能影响下游模块。
- 类型注解缺失不应视为原子问题（可能需要跨文件补充）。
- 若使用 dataclass / pydantic，字段变更属于架构问题。

### JavaScript / TypeScript 项目

- API 路由变更属于架构问题（影响前后端契约）。
- React/Vue 组件 props 变更属于架构问题。
- `any` 类型的修复应结合上下文，不可盲目收窄。

### Swift 项目

- `Sendable` / `@MainActor` 标注变更属于架构问题。
- SwiftUI View 的属性变更可能破坏调用方。
- 避免修改 `*.xcodeproj` 文件（二进制/复杂格式）。

### Go 项目

- 接口方法变更属于架构问题。
- goroutine 泄漏检查是 correctness 维度的重点。
- `init()` 函数的副作用变更需要特别关注。

### Rust 项目

- `unsafe` 块的变更属于架构问题。
- trait 实现变更属于架构问题。
- 所有权/生命周期变更属于架构问题。

---

## 5. Onboarding 产物质量检查 / Output Quality Checklist

AI onboarding 完成后应自检：

- [ ] ITERATE.md 的 AI 维护区和用户维护区分区标记完整。
- [ ] iterate.config.yaml 的 `onboarding.fingerprints` 包含所有检测到的 manifest 文件。
- [ ] `validation.commands` 中的命令均经过用户确认（涉及自动执行）。
- [ ] 每条 `validation.commands` 命令都能通过 `iterate guard pre-check`——guard 只放行它认识的安全工具前缀，`validation.command_whitelist` **没有任何运行时效果**，登记在那里并不会让 guard 放行；确需执行其它工具时，请用环境变量 `ITERATE_EXTRA_SAFE_COMMAND_PREFIXES` 登记该工具前缀。
- [ ] 推荐的维度列表与项目实际模块结构一致（无空转维度）。
- [ ] ITERATE.md 中的项目概述、技术栈、模块地图均基于扫描结果，非凭空生成。
