# GitCode 版本发布公告（Release Notes）

根据 GitCode API 拉取仓库在指定区间内的提交，按 **新特性 / 修复 / 文档 / 其他更改** 分组，输出标准 Markdown，可直接用于 GitCode Release 页面。

## 依赖

- Python 3.7+
- 仅标准库（无 pip 依赖）
- 环境变量 **GITCODE_TOKEN**（GitCode 个人访问令牌，需 `read_api`、`read_repository`）

## 参数

| 参数 | 必填 | 说明 |
|------|------|------|
| `--repo` | 是 | 仓库，格式 `owner/repo` |
| `--branch` | 否 | 分支；未传时自动尝试 master → develop → main |
| `--since-date` | 否 | 从该日 00:00（Asia/Shanghai）至今的提交，格式 YYYY-MM-DD |
| `--from` | 否 | 起始 tag（到当前 HEAD 或到 `--to`） |
| `--to` | 否 | 结束 tag，与 `--from` 一起表示区间 |

## 示例

```bash
# 从 v1.0.0 到当前
python scripts/release_notes.py --repo owner/repo --from v1.0.0

# 从 v1.0.0 到 v1.1.0
python scripts/release_notes.py --repo owner/repo --from v1.0.0 --to v1.1.0

# 从指定日期至今（上海时间 00:00）
python scripts/release_notes.py --repo owner/repo --since-date 2026-01-08
```

## 输出格式

- **语言**：默认中文（小节标题等）；缩写、专有名称保持原文。
- 有 `--to` 时：`## v1.1.0 (YYYY-MM-DD)`，然后四组（🚀 新特性、🐛 修复、📚 文档、🔧 其他更改），每条为 `- 短描述 ([sha](commit_url))`。
- **数量**：每类最多 10 条（可 `--max-per-category N` 指定，建议 5–10）。
- **过滤**：不展示空描述、单词无意义项（如 log、label）；去掉 `!数字`、`[模块]` 等前缀，突出可读说明。
- **合并**：多条「merge xxx into master」合并为一条「合并多项分支与依赖更新（共 N 条）」。
- 无结束版本时标题留空，仅输出分组列表。

## API 与错误

- 使用 [获取仓库所有提交](https://docs.gitcode.com/docs/apis/get-api-v-5-repos-owner-repo-commits)，支持 `since` 时用于 `--since-date`。
- 请求间隔与重试、429 处理已内置；失败时输出详细错误（HTTP 状态码、路径、响应片段）。
