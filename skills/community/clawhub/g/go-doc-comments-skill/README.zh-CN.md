# go-doc-comments-skill

一个用于为 Go 代码编写和补充注释的 [Claude](https://claude.com/claude-code) / Agent **skill**，遵循 Go 官方文档注释标准（[go.dev/doc/comment](https://go.dev/doc/comment)）。

> English docs: [README.md](./README.md)

## 它做什么

当你让 agent 为 Go 代码添加、修复或补充注释时，这个 skill 会引导它写出符合 Go 生态习惯、对工具友好、地道的文档注释。它融合了两条看似矛盾、实则互补的原则：

- **函数体内的注释要克制** —— 解释「为什么」，而不是「做了什么」；能用清晰命名说明的，就不写注释。
- **但每个导出标识符都必须有文档注释** —— 这是 Go 的硬性约定。`go doc`、`gopls`、`pkg.go.dev` 都会提取文档注释，因此每个导出的 package、func、type、const、var 都要有一条。

skill 把这两条规则明确分开，因此 agent 不会以「代码自解释」为由跳过导出 API 的文档注释。

## 特点

- **「要不要写注释」的决策框架。** 一个分步判断门（是否导出？→ 代码是否自解释？→ 改名/重构能否消除？→ 是 WHY 还是 WHAT？），同时决定「是否加注释」和「加哪种注释」—— 这是良好注释判断力的核心。
- **内置官方标准。** 涵盖注释位置规则、首词为标识符名的句式、布尔函数用 `reports whether`、零值/并发安全/复杂度的文档化、`Deprecated:` 标记，以及完整的 gofmt 友好语法（标题、doc link `[pkg.Name]`、列表、代码块、note、编译指令）—— 详尽语法规则见按需加载的 [`references/doc-comment-syntax.md`](references/doc-comment-syntax.md)。
- **语言自适应。** 自动检测文件/包中已有注释的语言并保持一致（无已有注释时默认英文），同时让 Go 的机器标记（`Deprecated:`、`TODO(...)`、`//go:...`、doc link 方括号）和「首词为标识符名」的结构保持规范形式。
- **gofmt 稳定输出。** 注释按 `gofmt` 不会改动的方式书写 —— 列表和代码块的缩进正确、`#` 标题、doc link 语法规范。
- **先审计后修改。** 在批量编辑前先清点「已导出但缺少文档」的声明，确保不遗漏。
- **反模式清单 + 检查表。** 捕获 Go 文档常见缺陷：缺失文档注释、句首不是标识符名、空行导致文档注释失效、缩进误产生代码块、冗余/失效代码注释等。
- **准确性护栏。** 只描述从代码中确认的行为；绝不臆断未经核实的版本号、RFC 或性能界。

## 安装

把它放到 agent 能发现 skill 的目录即可。skill 由 `SKILL.md` 加一个按需加载的 `references/` 目录组成。

### 让 agent 帮你安装（最简单）

直接给你的 agent 发一条消息：

```
帮我安装这个 skill：https://github.com/rroy233/go-doc-comments-skill
```

agent 会把仓库克隆到合适的 skills 目录（项目级 `.claude/skills/` 或用户级 `~/.claude/skills/`），并确认 skill 已可用。

### Claude Code

克隆到项目或用户级 skills 目录：

```bash
# 项目级（仅当前仓库）
git clone https://github.com/rroy233/go-doc-comments-skill .claude/skills/go-doc-comments

# 或用户级（对所有项目生效）
git clone https://github.com/rroy233/go-doc-comments-skill ~/.claude/skills/go-doc-comments
```

skill 目录只需包含 `SKILL.md`。安装后，当你提到「给 Go 代码写注释」时它会自动激活，也可以用 `/go-doc-comments` 显式调用。

### 手动安装

下载本仓库内容（`SKILL.md` 和 `references/`），放到：

```
<你的-skills-目录>/go-doc-comments/
├── SKILL.md
└── references/
    └── doc-comment-syntax.md
```

## 使用

在包含 Go 代码的项目里直接提出需求即可：

```
给 server.go 里的导出函数写文档注释
为这个包补充注释
把 handler.go 的注释改成符合 Go 标准
```

skill 会先读代码、检测注释语言、清点未文档化的导出符号，然后写出符合标准的文档注释。

## 参考

- [Go Doc Comments](https://go.dev/doc/comment)
- [Effective Go: Commentary](https://go.dev/doc/effective_go#commentary)

## 许可

MIT
