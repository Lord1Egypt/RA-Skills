# PDF 输入模块（按页并行）

>  **加载触发器**：检测到 PDF 输入时 MANDATORY 加载本模块。

通过 paddleocr-parser 按页解析 PDF，产出逐页 Markdown + elements JSON。随后启动并行翻译管线。

---

## 步骤 0：前置检查

| 场景 | 检查方式 | 处理 |
|---|---|---|
| 文件路径为空 | `!pdf_path` | 提示用户提供 PDF 文件 |
| 文件不存在 | `!path.exists()` | 提示用户检查路径 |
| 非 PDF 文件 | `path.suffix.lower() != ".pdf"` | 提示提供 `.pdf` 文件 |

检查通过 → 步骤 0.5。

---

### 步骤 0.5：PDF 加密检测（🛑 强制，解析前执行）

> **检测方法**：用 `pdfplumber` 尝试打开 PDF。加密文件会抛出异常。

```powershell
& $PythonExe -c @"
import sys, pdfplumber
try:
    with pdfplumber.open(r"<PDF路径>") as pdf:
        pass
    print("PASS: PDF is not encrypted")
except Exception as e:
    msg = str(e).lower()
    if 'encrypt' in msg or 'password' in msg:
        print("BLOCKED: PDF is encrypted or password-protected")
    else:
        print(f"BLOCKED: Cannot open PDF — {e}")
    sys.exit(1)
"@
```

| 结果 | 处理 |
|---|---|
| `PASS` | ✅ 继续步骤 1 |
| `BLOCKED` | 🛑 **立即终止**，提示用户：文件已加密，请提供未加密版本 |

> **前置配置**：首次配置已在 SKILL.md 入口统一处理，此处无需重复。

---

## 步骤 1：paddleocr-parser 按页解析

**1.1** 从 `config.json` 读取 token：`$config.paddleocr_token`。若为空 → 提示用户运行首次配置。

**1.2** 读取配置并创建输出目录：

```powershell
$config = Get-Content "$SkillDir\config.json" | ConvertFrom-Json
$ts = Get-Date -Format "yyyy-MM-dd_HH-mm-ss"
$slug = "<PDF文件名（去扩展名，取前20字符）>"
$outRoot = if ($config.output_dir.StartsWith(".")) { Join-Path (Get-Location) $config.output_dir } else { $config.output_dir }
# Runtime path validation
if (-not (Test-Path $outRoot)) { New-Item -ItemType Directory -Force -Path $outRoot | Out-Null }
$outDir = "$outRoot/$ts-$slug"
$paddleDir = "$outDir/paddleocr"
New-Item -ItemType Directory -Force -Path $paddleDir, "$outDir/pages" | Out-Null

& $PythonExe `
  "$SkillDir/../paddleocr-parser/scripts/paddle_parser.py" `
  --input_path "<PDF路径>" --save_dir "$paddleDir"
```

**1.3** 向用户显示进度：

```
⏳ PDF 解析中... (已提交 API)
⏳ 轮询中... 3/10 页
✅ 解析完成: 10 页, 86 个元素
```

**1.4** 确认产出：

```
paddleocr/
├── markdown/<file>.md         # 合并版（预留，不用于翻译）
├── markdown/<file>_p001.md    # 第1页 → 独立翻译
├── markdown/<file>_p002.md    # 第2页 → 独立翻译
├── markdown/<file>_p003.md    # ...
└── recognition_json/<file>.json  # 全文 elements
```

---

### 1.5 截断修复（🛑 强制关卡，不可跳过）

> **执行铁律**：paddleocr 解析完成后，必须在术语扫描和翻译开始前执行本步骤。Agent 分发翻译任务前，必须确认本步骤已执行。

> paddleocr-parser 的 markdown 输出可能截断超长表格（标注 `[truncated]`），但 `recognition_json` 中保存了完整文本。翻译开始前集中修复，Agent 读到的文件永远是完整的。

```powershell
& $PythonExe `
  "$SkillDir\scripts\fix_truncations.py" `
  --paddleocr-dir "$paddleDir" `
  --elements "$paddleDir/recognition_json/<file>.json"
```

**检测规则**：`fix_truncations.py` 自动扫描所有 `*_p*.md`：
- 含 `[truncated]` → 截断
- `<table>` / `</table>` 数量不等 → 截断

截断页调用 `build_page_text.py` 从 elements JSON 重建完整文本并**覆盖原始 md 文件**。

```
⚠️  Truncated: file_p005.md → rebuilding from JSON…
   ✅ file_p005.md fixed (423 → 1847 chars)
⚠️  Truncated: file_p069.md → rebuilding from JSON…
   ✅ file_p069.md fixed (1562 → 3120 chars)

✅ Truncation fix complete: 2/79 pages fixed
```

>  **关键**：修复后所有 `*_p*.md` 为完整文本。下游 Agent 直接翻译 md 文件，无需感知截断概念。

---

## 步骤 2：按页切组 → 分发 Agent 自扫自译

> **核心策略**：每 5 页一组，每组一个 Agent。Agent 内部自扫术语 + 翻译，组之间互不依赖。并发数建议 ≤ 8（8GB 内存机器安全上限）。

### 2.1 切页分组

```powershell
$pageFiles = Get-ChildItem "$paddleDir/markdown" -Filter "*_p*.md" | Sort-Object Name
$totalPages = $pageFiles.Count
$groupSize = 5
$numGroups = [Math]::Ceiling($totalPages / $groupSize)
# 79页 → 16组
```

### 2.2 并发分发（分批）

**并发上限 = 8**。若组数 > 8，分两批：第一批 8 组 → 等全部完成 → 第二批剩余组。

每个 Agent 收到的信息：
- 负责的页号列表（如 p001~p005）
- 源文件路径
- 输出路径（`pages/`）
- Prompt 模板（来自 translate-core.md 步骤 3 模式一）

### 2.3 完整性检测（��� Agent 全部完成后必须执行，merge 前）

> **检测方法**：对比 `pages/` 目录下实际产出的 `_trans.md` 文件数 vs elements JSON 中的总页数。
> **通过标准**：文件数 = 总页数，且每个文件非空（> 10 字节）。

```powershell
# 注意：需要使用 python 因为 PowerShell 5.1 的 ForEach-Object -Parallel 不支持
$script = @"
import json, os, glob

pages_dir = r"$outDir/pages"
elements_json = r"$paddleDir/recognition_json/<file>.json"

with open(elements_json, 'r', encoding='utf-8') as f:
    total_pages = json.load(f)['total_pages']

existing = sorted(glob.glob(os.path.join(pages_dir, '*_trans.md')))
existing_nums = set()
empty = []
for f in existing:
    num = int(os.path.basename(f).split('_p')[1].split('_')[0])
    existing_nums.add(num)
    if os.path.getsize(f) < 10:
        empty.append(num)

missing = [n for n in range(1, total_pages + 1) if n not in existing_nums]
all_bad = sorted(set(missing + empty))

if all_bad:
    print(f'FAIL: {len(all_bad)} pages need retry (missing={len(missing)}, empty={len(empty)})')
    print(f'Pages to retry: {all_bad}')
    with open(os.path.join(pages_dir, '_retry_pages.json'), 'w') as f:
        json.dump(all_bad, f)
else:
    print(f'PASS: {total_pages}/{total_pages} files, all non-empty')
"@
& $PythonExe -c $script
```

| 结果 | 处理 |
|---|---|
| `PASS` | ✅ 继续 merge |
| `FAIL` | ⚠️ 写 `_retry_pages.json` → 对缺失页重新分发 Agent（每 5 页一组，仅剩页也正常切组）→ 重跑完整性检测 → 最多 2 轮。2 轮后仍 FAIL → 报告用户，标注遗留问题，跳过缺失页继续 merge。 |

### 2.4 进度展示

```
📦 79 页 → 16 组，每 5 页/Agent
🚀 第 1 批启动: Agent×8 (p001~p040)
🌐 p001~p005: Agent-1 翻译中...  ✅
🌐 p006~p010: Agent-2 翻译中...  ✅
...
🚀 第 2 批启动: Agent×8 (p041~p079)
...

✅ 翻译完成: 79/79 页
🔍 完整性检测: 79/79 文件就位 ✅
```

---

## 步骤 3：交付下游

翻译完成后，产生：

| 数据 | 路径 | 用途 |
|---|---|---|
| elements JSON | `recognition_json/<file>.json` | HTML/MD 导出 |
| 逐页译文 | `pages/<file>_p001_trans.md` ~ `_p010_trans.md` | 合并后供导出 |
| 合并译文 | 拼接所有页面译文 | Gxpcode_html.py + Gxpcode_markdown.py |
| 全局术语映射 | 所有页 en→cn 去重 | 写日志用 |

进入 `modules/Gxpcode-export.md` 进行合并 + 导出。

---

## 注意事项

- paddleocr-parser 调用云端 API，大 PDF 需等待数分钟
- 逐页 md 文件按编号排序（`_p001, _p002...`），确保译文合并顺序正确
- 图片 figure 目录在 `markdown/figures/`，HTML 引用时注意相对路径
- elements JSON 为全文级，不按页拆分——HTML/MD 导出时从中提取每页的 elements 并对照译文
- 步骤 1.5 截断修复已覆盖原逐页检测逻辑。翻译 Agent 不会看到截断标记