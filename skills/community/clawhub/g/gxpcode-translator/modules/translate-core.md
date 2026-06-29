# 翻译核心模块

>  **加载触发器**：输入解析完成后 MANDATORY 加载。text 和 PDF 路径共用本模块。

---

## 输入数据（来自上游）

| 数据 | text 路径 | PDF 路径（按页并行） |
|---|---|---|
| 原文 | 用户粘贴的原文 | 逐页 `*_pXXX.md` 文件 |
| en→cn 映射 | —（步骤 2 产出） | —（步骤 2 产出，全页合并去重） |
| elements_json_path | — | `recognition_json/<file>.json` |
| 输出目录 | — | `translation-output/{ts}-{slug}` |

---

## 步骤 2：术语扫描

### text 路径 — 单次扫描

**2.1** 调用 `term_match.py` 扫描全文。

### PDF 路径 — 按页并行扫描（带进度）

**2.1** 遍历所有逐页 md，对每页单独调用 `term_match.py`。必须向用户展示进度：

```
🔍 术语扫描中... 1/10  3_p001.md → 86 matches
🔍 术语扫描中... 2/10  3_p002.md → 41 matches
...
✅ 术语扫描完成: 10 页, 79 个唯一术语
```

```powershell
$tempJson = "$outDir/_term_scan.json"
$pageFiles = Get-ChildItem "$paddleDir/markdown" -Filter "*_p*.md" | Sort-Object Name
$allMatches = @()
$totalPages = $pageFiles.Count
$pageNum = 0
foreach ($page in $pageFiles) {
    $pageNum++
    Write-Output "🔍 术语扫描中... $pageNum/$totalPages"  # 进度输出
    $text = Get-Content $page.FullName -Raw -Encoding UTF8
    & $pyExe $termPy --output "$tempJson" $text
    $data = Get-Content $tempJson -Raw -Encoding UTF8 | ConvertFrom-Json
    Write-Output "   $($page.Name): $($data.match_count) 个术语命中"
    $allMatches += $data.matches
}
```

**2.2** 合并所有页的 matches，去重后提取 `en→cn` 映射。向用户输出最终统计。

---

## 步骤 3：AI 翻译

### 模式一：Agent 自扫自译（默认，5 页/Agent）

每个 Agent 独立完成：术语扫描 → 翻译 → 输出。主流程只做切页分发。

**Agent Prompt 模板**：

```
你是{domain}领域({subdomain})专业翻译 Agent。你的任务：翻译 {page_count} 页 PDF 原文。

## 执行步骤

### 第一步：术语扫描
对每一页原文，用以下命令扫描本页命中的术语：

& $PythonExe ^
  "$SkillDir\\term_match.py" ^
  --output "{temp_json}" ^
  (Get-Content "{page_md_path}" -Raw -Encoding UTF8)

从输出的 JSON 中提取 matches 数组，收集所有 en→cn 映射。

### 第二步：翻译
将每页原文逐页翻译为中文。使用第一步扫描到的术语映射。

## 翻译规则
1. 禁用"待XX"机械直译
2. 禁用"被XX"被动结构，中文尽量用主动语态
3. 术语必须使用第一步扫描到的译法
4. 保持原文段落结构，段落数量严格一致
5. 段落间必须有空行
6. 公式（$...$）和 HTML 表格标签保持不变，仅翻译表格内文本
7. 图片链接（!\[\](...)）保持不变
8. 译文使用中文标点符号
9. **原文完整保证**：原文已经过系统预处理，保证内容完整无截断。必须翻译每一行、每一个 `<tr>`，不得省略。

### 第三步：输出
每页译文写入对应文件：

{page_list_with_paths}

## 输出规则
- 仅汇报进度：每完成一页输出 "pXXX ✅"
- 全部完成后输出总页数
- 译文内容禁止出现在对话中，仅写入文件
```

### 模式二：集中术语扫描（旧版，保留兼容）

主流程预先扫描全部术语，Agent 直接翻译（无需自扫）。

```
你是{domain}领域({subdomain})专业翻译。将以下{source_lang}翻译为{target_lang}。

## 术语映射（必须使用以下译法）

{en_cn_map}

## 翻译规则

1. 禁用"待XX"机械直译（如 "to be steamed" ≠ "待蒸汽灭菌"，应为"需蒸汽灭菌"）
2. 禁用"被XX"被动结构，中文尽量用主动语态
3. 术语必须使用上方映射表中的指定译法
4. 保持原文段落结构，段落数量严格一致
5. **段落间必须有空行**：每个段落和标题（##）之间必须以空行分隔（`\n\n`），禁止 `## 标题\n正文` 无空行拼接
6. 公式（$...$）和 HTML 表格标签保持不变，仅翻译表格内文本内容
7. 图片链接（!\[\](...)）保持不变
8. 译文使用中文标点符号
9. **原文完整保证**：原文文件已经过系统预处理，保证内容完整无截断。你必须翻译原文中的每一行、每一个表格行（`<tr>`），不得自行判断内容是否截断或省略任何内容。

## 原文

{source_text}

## 译文（仅输出译文，不要任何解释）
```

### text 路径 — 单次翻译

注入原文 + 术语映射 → LLM → 译文。

### PDF 路径 — 按页翻译（静默输出 + 进度）

> 🛑 **加载时先读本段**：以下所有翻译步骤中，译文**仅写入文件**。对话框只能出现进度行、状态行、校验行。**任何情况下不得展示译文字符**。

对每页逐页注入该页的原文 + 全局术语映射 → LLM → 该页译文。

>  **输出铁律**：翻译内容仅写入 `*_trans.md` 文件。对话框**仅显示进度**，不得输出译文内容。

**进度格式**：仅输出一行状态，包含页号 + 页数 + 文件名。

```
🔍 术语扫描中... 1/10
🔍 术语扫描中... 2/10
✅ 术语扫描完成: 10 页, 79 个术语

🌐 翻译中... 1/10  3_p001.md → 已保存
🌐 翻译中... 2/10  3_p002.md → 已保存
...
✅ 翻译完成: 10/10 页
```

**实现方式**：

1. 每页的 AI 翻译在内部执行（Prompt 模板 → LLM），译文不向用户展示
2. 译文直接写入 `pages/<file>_pXXX_trans.md`
3. 对话框仅输出进度行

```powershell
# 创建 pages 目录
New-Item -ItemType Directory -Force -Path "$outDir/pages" | Out-Null

# 逐页翻译（静默）+ 保存
$pageNum = 0
foreach ($page in $pageFiles) {
    $pageNum++
    Write-Output "🌐 翻译中... $pageNum/$totalPages  $($page.Name)"  # 仅进度
    
    $sourceText = Get-Content $page.FullName -Raw -Encoding UTF8
    # [内部] 构建 Prompt → LLM 翻译 → $translatedText
    
    # 保存该页译文 【立即落盘，不展示】
    $outName = ($page.BaseName -replace '\.md$', '') + "_trans.md"
    [System.IO.File]::WriteAllText("$outDir/pages/$outName", $translatedText, [System.Text.UTF8Encoding]::new($false))
}
Write-Output "✅ 翻译完成: $totalPages/$totalPages 页"
```

>  **强制规则**：
> 1. 翻译内容永不输出到对话框
> 2. 每翻完一页，立即落盘
> 3. 对话框仅输出进度行（每页一行 + 完结一行）

#### 表格拆行翻译（防截断）

>  **触发条件**：处理某一页时，检测到 element `label == "tab"` 且 `<tr>` 行数 > 2。

大 HTML 表格（3000+ 字符）直接送 LLM 会截断。拆 `<tr>` 逐行翻译 → 校验 → 拼回。每行注入全局术语映射。

```powershell
# 该页某个 element 是 tab，拆行处理
$tableText = $el.text
$rows = [regex]::Matches($tableText, '<tr>.*?</tr>', 'Singleline') | % { $_.Value }
$rowCount = $rows.Count

# 表头行翻译列名（带术语映射）
$transHeader = <LLM: "翻译表格列名，仅翻译<td>内文本。术语：${en_cn_map}`n`n${rows[0]}">

# 数据行逐行翻译（每行注入术语映射）
$transRows = @($transHeader)
for ($j = 1; $j -lt $rows.Count; $j++) {
    $rowPrompt = "你是{domain}领域({subdomain})专业翻译。仅翻译<td>内文本。术语：`n${en_cn_map}`n`n${rows[$j]}"
    $transRows += <LLM>
}

# 校验行数
if ($transRows.Count -ne $rowCount) { Write-Output "⚠️ 表格行数不匹配"; 回退重译 }

# 拼回（保留原 <table...> 外壳）
$before = $tableText.Substring(0, $tableText.IndexOf('<tr>'))
$el.translatedText = $before + ($transRows -join "")
```

---

## 步骤 4：自检

| # | 检查项 | 内容 |
|---|---|---|
| 4.1 | 朗读感 | 译文是否通顺自然 |
| 4.2 | 拆长句 | 英文长句拆分后中文是否合理 |
| 4.3 | "待XX"排查 | 如 `to be steamed` ≠ "待蒸汽灭菌" |
| 4.4 | "被XX"排查 | 中文尽量用主动语态 |
| 4.5 | 语境匹配 | 术语译法是否符合段落上下文 |
| 4.6 | 不通过 → 修正后重检，最多 2 轮 | |

PDF 路径：每页独立自检。某页不通过 → 该页单独回退翻译。

---

## 步骤 5：输出

**5.1 text 路径**：**仅输出纯译文，一行，无任何装饰。** 禁止输出术语表、匹配统计、自检表格、解释说明、翻译备注、日志路径等任何非译文内容。唯一例外：术语库中找不到对应译法、需要向用户确认时。

**5.2 PDF 路径**：合并所有逐页译文 → 交付 `modules/Gxpcode-export.md` 生成 HTML + MD。

---

## 步骤 6：表格行数校验（merge 后必检）

>  **触发**：`merge_translations.py` 完成后、导出 HTML/MD 前，必须执行。

对 translated.json 中所有 `label=tab` 的元素，对比 EN 和 ZH 的 `<tr>` 数量：

```python
import json
with open("translated.json") as f:
    data = json.load(f)
for el in data["elements"]:
    if el.get("label") == "tab":
        en_tr = el["en"].count("<tr>")
        zh_tr = el["zh"].count("<tr>")
        if en_tr != zh_tr:
            print(f"⚠️  elem[{el['index']}] page={el['page']} TR mismatch: EN={en_tr} ZH={zh_tr}")
```

| 结果 | 处理 |
|---|---|
| 全部一致 | ✅ 通过，继续导出 |
| 存在不一致 | ⚠️ 输出差异列表，暂停导出，等待人工确认 |



---

## 故障排查

### F01: term_match.py 输出 JSON 解析失败

**症状**：PowerShell `ConvertFrom-Json` 报错 "传入的对象无效"，部分页的 `match_count` 为空。

**根因**：Windows 控制台默认 GBK 编码无法处理 ™、®、†、• 等 Unicode 字符，`&` 管道捕获时二次污染。

**诊断**：
```powershell
# 检查某页是否有 UnicodeEncodeError
& $pyExe $termPy (Get-Content "page.md" -Raw) 2>&1 | Select-String "UnicodeEncodeError"
```

**修复步骤**：

| 优先级 | 动作 | 说明 |
|---|---|---|
| P0 | 确认 `term_match.py` 版本 ≥ 当前（含 `--output` 支持） | 源头 UTF-8 输出 |
| P1 | 调用侧使用 `--output <path>` 传文件，而非 `&` 管道 | `& $pyExe $termPy --output "$json" $text` |
| P2 | 读回时指定 UTF-8 | `Get-Content $json -Raw -Encoding UTF8 \| ConvertFrom-Json` |

**验证**：重扫失败页后 `$data.match_count` 应为正整数，无编码异常。

### F02: 段落对齐错位（HTML 中部分段落单栏显示）

**症状**：HTML 中某些段落只有英文列（EN），中文列为空或缺失。打开 HTML 在页面顶部显示红色警告卡片。

**根因**：
- `translated.txt` 中段落数与 paddleocr elements 数不一致。常见原因：
  - 标题 `## ...` 与正文之间无空行 → `split_paragraphs()` 合并
  - paddleocr 将长文本跨页拆为多个 element，翻译合为一段 → 数量减 1

**诊断**：打开 HTML，页面顶部自动显示红色 `⚠ 段落对齐警告` 卡片，列出所有缺译文的元素及其文本开头。

**修复步骤**：

| 优先级 | 动作 | 说明 |
|---|---|---|
| P0 | 看 HTML 顶部警告卡片 | 直接知道哪些元素缺译文 |
| P1 | 检查对应位置 `translated.txt` 有无空行缺失 | `\n## ` 应为 `\n\n## ` |
| P2 | 补齐空行或补翻译 → 重生成 HTML | 段落数 = 元素数 = 警告消失 |

**预防**：
1. 翻译 Prompt 规则 5：段落/标题间必须有空行
2. HTML 自动诊断：`split_paragraphs()` 发现不匹配时注入可见警告卡片
3. 每次生成后检查 HTML 顶部是否出现红色卡片
