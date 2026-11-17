# Kinema TDD Injector Onboarding

> 本文档指导 AI Agent 完成 Claude Code 与 Codex 共用渲染环境的首次检查。

## Prerequisites | 前置条件

- `uv` 包管理器
- 目标仓库为 Python 或 TypeScript/JavaScript 项目

## Step 1: 检测 Jinja2

```bash
uv run --with jinja2 python -c "import jinja2; print(jinja2.__version__)"
```

无需手动安装 jinja2，`uv run --with` 会自动处理依赖。

## Step 2: 验证共享模板

确认插件根目录存在 `assets/claude_md.j2`。该文件是 Claude/Codex 共用模板，渲染器会按
`--target` 注入平台名称、指令文件名和 co-author 身份。

```bash
uv run --with jinja2 python -c "
from jinja2 import FileSystemLoader, Environment
env = Environment(loader=FileSystemLoader('<plugin_root>/assets'))
template = env.get_template('claude_md.j2')
print('template loaded:', template.name)
"
```

## Step 3: 验证渲染器

```bash
uv run --with jinja2 python <plugin_root>/scripts/render.py --help
```

渲染目标：

```bash
# Claude Code（默认 target，显式写出便于审计）
uv run --with jinja2 python <plugin_root>/scripts/render.py \
  --target claude \
  --params <repo>/.kinema-params.tmp.json \
  --out <repo>/.kinema-claude.draft.md

# Codex
uv run --with jinja2 python <plugin_root>/scripts/render.py \
  --target codex \
  --params <repo>/.kinema-params.tmp.json \
  --out <repo>/.kinema-agents.draft.md
```

参数 JSON 支持 UTF-8 与带 BOM 的 UTF-8；最终输出统一为无 BOM UTF-8。

## Step 4: 目标仓库语言检测

使用本 skill 时，Agent 会自动扫描目标仓库：

- 含 `pyproject.toml` → Python 包
- 含 `package.json` + `tsconfig.json` → TypeScript 包
- 含 `package.json` 无 TS → JavaScript 包

若发现 `Cargo.toml` / `go.mod` / `pom.xml` → **拒绝执行**（规范仅支持 Python + TS/JS）。

## Troubleshooting | 故障排除

| 错误 | 原因 | 解决方案 |
|------|------|----------|
| `ModuleNotFoundError: No module named 'jinja2'` | uv 未正确调用 | 确认使用 `uv run --with jinja2` |
| `TemplateNotFound: claude_md.j2` | 模板路径错误 | 从插件根目录定位 `assets/`，不要从 Codex skill 子目录猜测路径 |
| `JSONDecodeError` | 参数文件不是有效 JSON | 确认文件为 UTF-8/UTF-8 BOM 且没有尾随逗号 |
| `SyntaxError` in render.py | Python 版本过低 | 升级 Python 或通过 `uv python install` 管理 |
| 目标仓库含 Go/Rust | 规范不支持 | 告知用户本规范仅支持 Python + TS/JS |
