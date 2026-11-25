# CodeBuddy / Claude Code 主题与差异可读性

> [English](cli-themes.md) · **简体中文**

这份文档解释：为什么终端里 `ls` 看着没问题，到了 AI CLI 的 diff 视图里却很难受；
以及该改哪一层。CodeBuddy 和 Claude Code 共用同一套 ANSI 主题名
（`dark-ansi` / `light-ansi`）。

## 症状

它们的 ANSI 主题把差异词的背景映射到终端的**亮色** ANSI 槽：

```
diffAddedWord   → ansi:greenBright   (ANSI 10)
diffRemovedWord → ansi:redBright     (ANSI 9)
```

这两个槽是给**前景强调**用的。一旦被拿来当背景，亮度就过头了。实测 `voltage`：

| 组合 | 对比度 |
|---|---|
| 语法橙 `#f1a65a` 在亮绿 `#0dd25f` 上 | **1.01:1** |
| 正文 `#e8e8ed` 在亮绿 `#0dd25f` 上 | **1.65:1** |
| 语法橙 `#f1a65a` 在亮红 `#fa9ba8` 上 | **1.00:1** |
| 正文 `#e8e8ed` 在亮红 `#fa9ba8` 上 | **1.67:1** |

这不是色板挪一个值能解决的：ANSI 9/10 必须保持亮，才能当前景强调色用。
为了当背景而压暗它们，会把 `ls`、`git diff` 和所有用亮红/亮绿表达强调的程序一起毁掉。

## 修法

用 CLI 的非 ANSI 主题，它自带深色差异底：

| Token | 非 ANSI `dark` |
|---|---|
| `diffAdded` | `rgb(34, 92, 43)` → 正文对比 6.53 |
| `diffRemoved` | `rgb(122, 41, 54)` → 正文对比 7.82 |
| `diffAddedWord` | `rgb(56, 166, 96)` |
| `diffRemovedWord` | `rgb(179, 89, 107)` |

亮底终端用非 ANSI 的 `light` 主题：`diffAdded rgb(153, 204, 255)`、
`diffRemoved rgb(255, 204, 204)`；`setup-cli.sh` 会按当前 会勇禾口王·终端工作台 主题的底色自动选。

两种做法：

- 在你用的 AI CLI 的设置文件里把 `theme` 改成 `dark` 或 `light`——具体路径见该 CLI 官方文档，本技能不会替你去探测；
- 在 CLI 里运行 `/theme`，选 **Dark** / **Light**（不要选 ANSI 变体）；
- 或运行 `./scripts/setup-cli.sh --config <设置文件路径> --apply`（会先备份设置文件，再写入与当前终端匹配的非 ANSI 主题）。

验证：

```bash
./scripts/setup-cli.sh --config <设置文件路径> --check   # 0 = 安全，1 = ANSI 主题，2 = 没检查
./scripts/doctor.sh --status       # CLI 行报同一个检查
python3 config/themes/_preview.py --cli-diff voltage   # 复现坏组合
```

## 为什么不改色板

`setup-cli.sh` 只改 CLI 的主题，永远不动终端的 ANSI 9/10。
审计里会报告 `cli_diff` 比值，但不作为色板 gate —— 亮槽本来就该亮。
以后如果做「生成的 CLI 主题」（付费层），应该把 diff token 钉成和
非 ANSI `dark` 一样的深色底，那才是这个问题的正确落点。
