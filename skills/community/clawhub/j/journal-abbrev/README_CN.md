# Journal Abbrev — 期刊名称缩写查询技能

[English](README.md)

一个用于查询期刊/杂志名称标准缩写的 Claude Code 技能。支持 ISO 4 和 MEDLINE 两种缩写标准，覆盖 25,000+ 期刊。

## 功能特性

| 功能 | 原生 Claude Code | Journal Abbrev |
|------|-----------------|----------------|
| 期刊名缩写查询 | 需要手动猜测 | 多源级联查询，结果准确 |
| 缩写反查全名 | 不支持 | 双向查询 |
| BibTeX 批量处理 | 不支持 | 自动替换 journal 字段 |
| 模糊搜索 | 不支持 | 支持部分名称匹配 |
| 离线查询 | 不支持 | 本地缓存 25K+ 期刊 |

## 数据来源

1. **JabRef 数据库** — 25,000+ 期刊，CC0 开源，首次运行自动下载
2. **AbbrevISO API** — 基于 LTWA 的 ISO 4 算法缩写（正向查询）
3. **NLM Catalog** — 生物医学期刊双向查询（MEDLINE 标准）

## 安装

`journal-abbrev` 是通过 `SKILL.md` 分发的 skill，直接安装到任意支持
`SKILL.md` 的平台即可：

| 平台 | 安装命令 |
|---|---|
| **Claude Code**（全局） | `git clone https://github.com/Agents365-ai/journal-abbrev.git ~/.claude/skills/journal-abbrev` |
| **Claude Code**（项目） | `git clone https://github.com/Agents365-ai/journal-abbrev.git .claude/skills/journal-abbrev` |
| **OpenClaw**（全局） | `git clone https://github.com/Agents365-ai/journal-abbrev.git ~/.openclaw/skills/journal-abbrev` |
| **OpenClaw**（项目） | `git clone https://github.com/Agents365-ai/journal-abbrev.git skills/journal-abbrev` |
| **ClawHub** | `clawhub install journal-abbrev` |
| **SkillsMP** | 在 [skillsmp.com](https://skillsmp.com) 搜索 `journal-abbrev` |

也可以把仓库克隆到任意位置直接使用 CLI —— 纯 Python 3.9+ 标准库实现，
无任何第三方依赖，在 macOS、Linux、Windows 上均可运行：

```bash
git clone https://github.com/Agents365-ai/journal-abbrev.git
cd journal-abbrev
python3 jabbrv.py lookup "Nature Medicine"
python3 jabbrv.py schema              # 完整机器可读的 CLI 契约
```

## 使用方法

### 自然语言

直接向 Claude 提问：

- "Nature Medicine 的缩写是什么？"
- "J. Biol. Chem. 是哪个期刊？"
- "帮我把 refs.bib 里的期刊名都改成缩写"
- "查一下 biolog chem 相关的期刊"

### 命令行

```bash
# 自动检测方向
python3 jabbrv.py lookup "Nature Medicine"

# 全名 → 缩写
python3 jabbrv.py abbrev "Journal of Biological Chemistry"

# 缩写 → 全名
python3 jabbrv.py expand "Nat. Med."

# 模糊搜索（支持分页）
python3 jabbrv.py search "biolog chem" --limit 10 --offset 0

# 处理 BibTeX 文件（先预览再写入）
python3 jabbrv.py bib refs.bib --dry-run
python3 jabbrv.py bib refs.bib --output refs_final.bib

# 批量查询（每行一个期刊名）
python3 jabbrv.py batch journals.txt
python3 jabbrv.py batch journals.txt --stream   # NDJSON 流式输出

# 缓存管理
python3 jabbrv.py cache status     # 查看本地缓存状态
python3 jabbrv.py cache update     # 下载缺失的缓存文件
python3 jabbrv.py cache rebuild    # 删除并重新下载全部缓存

# 机器可读的命令契约（供 AI 智能体或自动化工具使用）
python3 jabbrv.py schema
python3 jabbrv.py schema lookup
```

### Agent-native 输出契约

当标准输出不是终端（例如被管道捕获、被智能体运行时读取）时，`stdout` 默认输出
稳定的 JSON 信封；在终端下则输出人类友好的表格或缩进视图。所有响应共用同一信封结构：

- 成功: `{"ok": true, "data": ..., "meta": {"schema_version", "cli_version", "cache", "latency_ms"}}`
- 部分成功（batch）: `{"ok": "partial", "data": {"succeeded": [...], "failed": [...]}}`
- 错误: `{"ok": false, "error": {"code", "message", "retryable", ...}}`

退出码按失败类别区分：`0` 成功、`1` 运行时错误、`2` 参数/输入错误、`3` 未找到。
可用 `--format json|table|human` 强制格式（`--json` 是旧版兼容别名）；
所有全局参数可以放在子命令前或后。

## 依赖

- Python 3.9+（无需安装第三方包）

## 支持作者

如果这个项目对你有帮助，欢迎支持作者：

<table>
  <tr>
    <td align="center">
      <img src="https://raw.githubusercontent.com/Agents365-ai/images_payment/main/qrcode/wechat-pay.png" width="180" alt="微信支付">
      <br>
      <b>微信支付</b>
    </td>
    <td align="center">
      <img src="https://raw.githubusercontent.com/Agents365-ai/images_payment/main/qrcode/alipay.png" width="180" alt="支付宝">
      <br>
      <b>支付宝</b>
    </td>
    <td align="center">
      <img src="https://raw.githubusercontent.com/Agents365-ai/images_payment/main/qrcode/buymeacoffee.png" width="180" alt="Buy Me a Coffee">
      <br>
      <b>Buy Me a Coffee</b>
    </td>
  </tr>
</table>

## 作者

**Agents365-ai**

- B站: https://space.bilibili.com/441831884
- GitHub: https://github.com/Agents365-ai

## 许可证

MIT
