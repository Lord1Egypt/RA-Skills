# 脚本参数手册

## 1. gongwen_format.py — 国标排版

```bash
python scripts/gongwen_format.py [参数] --output 输出.docx
```

### 基本

| 参数 | 说明 |
|---|---|
| `--config PATH` | JSON 配置文件，字段名与下列参数同名（下划线形式）。与命令行混用时**命令行优先** |
| `--title TEXT` | 公文标题，2 号小标宋体居中 |
| `--input PATH` | 正文来源 `.md` / `.txt` / `.docx` |
| `--output PATH` / `--out` | 输出 `.docx` 路径 |
| `--demo` | 生成内置示例公文，用于验证环境与字体映射 |

### 版头要素

| 参数 | 说明 |
|---|---|
| `--redhead TEXT` | 发文机关标志（红头）。联合行文用 `;` 分隔多个机关 |
| `--doc-number TEXT` | 发文字号，如 `×政发〔2026〕12号`。脚本会规范化括号与虚位 |
| `--copies NNNNNN` | 份号，6 位阿拉伯数字，首页版心左上角顶格 |
| `--secret-level TEXT` | 密级和保密期限，如 `机密★20年` |
| `--urgency {特急,加急,平急}` | 紧急程度 |
| `--signer TEXT` | 签发人，**上报的公文必备**。多人用 `、` 分隔。指定后红头位置自动下移至 80mm |

### 主体要素

| 参数 | 说明 |
|---|---|
| `--recipient TEXT` | 主送机关，顶格，自动补全角冒号 |
| `--attachment TEXT` | 附件说明条目，**可重复**多次 |
| `--attachment-doc PATH` | 附件正文文件，另面编排。格式 `path` 或 `path::附件标题` |
| `--author TEXT` | 发文机关署名，联合行文用 `;` 分隔 |
| `--date TEXT` | 成文日期，支持 `2026-08-06` / `2026年8月6日` / `today` |
| `--seal` | 加盖印章版式：署名与日期右空四字 |
| `--seal-image PATH` | 印章图片，嵌入并下压署名 |
| `--notes TEXT [TEXT...]` | 附注，如 `此件公开发布`，自动加圆括号 |

### 版记与页面

| 参数 | 说明 |
|---|---|
| `--cc TEXT` | 抄送机关 |
| `--print-author TEXT` | 印发机关 |
| `--print-date TEXT` | 印发日期 |
| `--no-page-num` | 不编页码 |
| `--no-first-page-num` | 首页不显示页码。**国标未作此要求**，仅供个别单位惯例 |
| `--minutes` | 会议纪要版式：无版记、无印章 |
| `--strict-font` | 强制写入国标字体名，不做本机可用性回退 |

### JSON 配置示例

```json
{
  "redhead": "××市人民政府",
  "doc_number": "×政发〔2026〕12号",
  "title": "××市人民政府关于进一步加强城市排水防涝工作的通知",
  "recipient": "各区县人民政府，市政府各部门、各直属机构",
  "body_text": "一、提高思想认识\n\n近年来……",
  "author": "××市人民政府",
  "date": "2026-08-06",
  "seal": true,
  "notes": ["此件公开发布"],
  "cc": "市委办公室，市人大常委会办公室",
  "print_author": "××市人民政府办公室",
  "print_date": "2026-08-07"
}
```

`body_text` 与 `--input` 二选一；同时存在时 `--input` 优先。

---

## 2. gongwen_check.py — 格式质检

```bash
python scripts/gongwen_check.py --input 待检.docx [--report 报告.md] [--json]
```

| 参数 | 说明 |
|---|---|
| `--input PATH` | 待检 `.docx`（必填），不限于本技能生成的文件 |
| `--report PATH` | Markdown 报告输出路径。不指定则只打印到终端 |
| `--json` | 输出 JSON 结构化结果 |

退出结论：**合规**（无高级别问题）/ **不通过**（存在高级别问题）。检查项见 `qc-checklist.md`。

---

## 3. style_clean.py — 文风净化与校对

```bash
python scripts/style_clean.py --input draft.md [--output clean.md] [--report 文风报告.md]
```

| 参数 | 说明 |
|---|---|
| `--input PATH` | 输入 `.md` / `.txt` / `.docx`（必填） |
| `--output PATH` | 净化后文本输出路径 |
| `--report PATH` | 处理报告输出路径 |
| `--dry-run` | 只出报告，不写净化文本 |
| `--keep-markdown` | 保留 Markdown 标记。**串联排版时建议加**，否则层级信息丢失 |
| `--no-punct` | 跳过标点规范化 |
| `--json` | 输出 JSON |

---

## 4. 串联脚本模板

```bash
#!/usr/bin/env bash
set -e
SRC=draft.md
CFG=my.json

python scripts/style_clean.py   --input "$SRC" --output out/clean.md \
                                --report out/文风报告.md --keep-markdown
python scripts/gongwen_format.py --config "$CFG" --input out/clean.md \
                                --output out/正式文件.docx
python scripts/gongwen_check.py --input out/正式文件.docx --report out/质检报告.md
```

## 5. 常见报错

| 现象 | 原因 | 处理 |
|---|---|---|
| `ModuleNotFoundError: No module named 'docx'` | 未装依赖 | `pip install python-docx`（注意不是 `pip install docx`） |
| 生成的文档字体不对 | 本机缺公文字库，已自动回退 | 看运行日志的字体映射行；装字库后重跑，或加 `--strict-font` |
| 需要 PDF 版 | 本技能只产出标准 `.docx` | 用 Word/WPS「另存为 PDF」即可获得 PDF 版 |
| 质检报「未识别到正文段落」 | 输入不是公文正文，或正文字号异常 | 确认文件内容；检查是否整篇都是标题级字号 |
| 层级字体全部报错 | 正文用了 `#` 而未经排版脚本处理 | 先跑排版脚本，不要直接检查 Markdown 转存的 docx |
