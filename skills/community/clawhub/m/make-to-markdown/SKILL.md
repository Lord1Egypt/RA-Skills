---
name: make-to-markdown
description: 工业级RAG Markdown物料生成技能，使用 markitdown 将各类文档和文件转换为 Markdown 格式。支持 .doc/.ppt 老格式自动预处理（Word/PowerPoint COM / LibreOffice）。启动时自动检测 OS/版本/能力，按平台选择最佳执行路径。触发词：转 Markdown / 转换文档 / markitdown / 文档转 md / 批量转换。当需要将 PDF、Word (.docx/.doc)、PowerPoint (.pptx/.ppt)、Excel (.xlsx, .xls)、HTML、CSV、JSON、XML、图片（含 EXIF/OCR）、音频（含语音转写）、ZIP 压缩包、YouTube 链接或 EPub 电子书转换为 Markdown 格式，为知识库提供统一的"通用语言"时触发此技能。
version: "3.6"
metadata:
  domain: "make-to-markdown"
  author: "智慧半岛"
  platform:
    windows: full
    linux: full
    macos: full
  openclaw:
    requires:
      bins:
        - uv
        - python
    emoji: "📚"
---

> 文档结构：SKILL.md = 核心运行时指令（Agent 执行必读），REFERENCE.md = 扩展参考与运维细节。非核心内容不得写入本文件。

## ⛔ 核心红线 (Critical Constraints)
1. **源文件零修改原则**：转换过程对源文件实行只读操作。严禁以任何理由修改、删除、移动或重命名用户提供的原始文档。所有中间产物写入系统临时目录或技能工作区，转换完成后不保留任何可关联回源文件的痕迹。
2. **输出覆盖二次确认**：`-o` 指定的输出文件若已存在，convert.py 启动前必须暂停并告知用户路径及已有内容来源，获得明确授权后方可覆盖。禁止自动跳过或静默覆写。
3. **加密文档不重试**：检测到文档加密（`File is encrypted` / 密码保护提示）时，首次失败即终止该文件转换，提示用户解密后重试。禁止反复尝试、猜测密码或绕过保护。
4. **旧格式无预处理环境时阻断**：`.doc` / `.ppt` 旧格式且在 COM 和 LibreOffice 均不可用的环境下，必须暂停并告知用户安装 Office 或 LibreOffice。禁止静默跳过该文件或输出空结果。
5. **禁止绕过 convert.py 裸调 CLI**：不得直接调用 `markitdown` / `uvx markitdown` / 原生库进行转换。所有转换必须经由 `scripts/convert.py` 统一入口，以确保依赖补全、降级兜底和后置清洗管线完整执行。
6. **禁止外部 API 泄露文档内容**：转换过程全程本地执行，禁止将文档内容上传至任何外部 API（包括 OpenAI、Ollama 远程、云端 OCR 等）。仅允许本地安装的 markitdown / python-docx / openpyxl / python-pptx 等库。
7. **网络驱动器路径约束（平台自适应）**：涉及网络驱动器（如 X: 盘、E:\Marvis_Data 等）上的文件读写操作时：
   - **Windows 网络驱动器**：优先使用 `python_executor`，避免 `shell_executor`（PowerShell/cmd 可能因 WinError 2 找不到网络驱动器路径）
   - **Linux/macOS NFS/CIFS 挂载**：`shell_executor` 通常可用，但路径中含空格或特殊字符时回退到 `python_executor`
   - **自动检测**：脚本内部使用 `pathlib.Path` 处理路径，无需硬编码平台判断
8. **系统破坏操作禁令 (HARB)**：以下高风险行动黑名单中的命令，Agent 在任何阶段均不得自动执行，必须输出完整命令预览并等待用户显式确认：
   - **文件系统破坏**：`rm -rf` / `del /f /s` / `Remove-Item -Recurse -Force` 等递归强制删除 | 格式化（`format` / `mkfs`） | 对工作目录外任意路径的批量写操作
   - **数据不可逆丢失**：`git reset --hard` / `git clean -fdx` | 数据库 `DROP TABLE` / `TRUNCATE` / `DROP DATABASE` | 清空回收站 | `shred` / `wipe` 等安全擦除
   - **系统级破坏**：`diskpart clean` | 注册表 `reg delete` 批量删除 | `sc delete` 删除系统服务 | `bcdedit` 修改引导配置
   - **批量不可逆操作**：对 >50 个文件或目录的单次删除/覆盖 | 对 >10 个 Git 仓库的单次 `push --force` / `reset --hard`
   违反本禁令的脚本或流水线必须被拒绝执行并告知用户原因
9. **输出编码完整性**：所有输出文件必须为 UTF-8 编码。convert.py 写盘后须验证文件可被 UTF-8 解码且无乱码（检查项 V2）。非 UTF-8 源文件需先检测编码再转码，禁止直接写入可能导致乱码的编码。
10. **批量操作确认前置**：批量转换前必须确认源目录路径、目标输出路径、待转换文件数量（预估）、限定格式。禁止不经确认即递归遍历整个目录。
11. **禁止循环清洗**：`post_clean.py` 的输出不得再次作为 `convert.py` 的输入；`convert.py` 的输出不得再次调 `post_clean.py`。二次清洗会导致摘要叠加、噪声模式重复匹配、标题层级二次修复误触发。


# make-to-markdown Markdown物料智能转换器 (v3.6)

核心入口：`scripts/convert.py`。依赖检测 → `uv tool install markitdown --with=...` 安装完整 extras → 转换 → 失败降级 → 后置清洗。零人工干预。

> 🟢 **最小可用示例**：`python scripts/convert.py input.docx`。全选项见 §3，异常处理见 §5。

## 1. 核心执行流程

当用户要求转换文件时，**只需调用一次** `scripts/convert.py`，脚本内部自动完成以下全部步骤：

```
(.doc/.ppt?)→预处理为 .docx/.pptx → 依赖检测 → 自动安装 → markitdown extras → markitdown 转换 → (失败则) 原生降级 → 后置清洗 → 输出
```

1. **.doc/.ppt 预处理**（v2.3+）：自动将老格式转为 `.docx`/`.pptx`，详见 [§2.5 旧格式预处理](#25-旧格式预处理v2-3)。
2. **依赖检测**：根据文件扩展名自动检查所需 Python 模块是否已安装。
3. **自动安装**：缺失模块自动 `pip install` 安装，120 秒超时。
3.5. **markitdown extras**（v2.4）：自动检测 pip 和 uv 两侧的 markitdown 可选依赖完整性；缺失时自动安装，避免 `MissingDependencyException`。pypdf 已就绪则跳过全部安装。
4. **markitdown 转换**：调用 markitdown CLI 转换文件。
5. **降级兜底**：markitdown 失败时，使用 python-docx / openpyxl / python-pptx 等原生库转换。
6. **后置清洗**：去水印 / 页码 / 空白压缩 + 标题层级修复（多 H1 降级、越级补过渡） + 表格分隔符补全 + 注入文档摘要（内联执行，无需单独调用 post_clean.py）。
7. **结果反馈**：输出路径 + H1/H2/H3 标题统计 + 表格计数 + 转换方式（markitdown / 原生降级）。

## 2. 依赖映射

markitdown 对非纯文本格式采用可选依赖策略：`pip install markitdown` 仅装核心，以下格式需额外包。`convert.py` 会在转换前**自动检测并安装**缺失依赖。

| 扩展名 | pip 包 | import 模块 | markitdown extra 名 |
|--------|--------|-------------|---------------------|
| .docx | python-docx | docx | docx |
| .doc | python-docx | docx | docx |
| .xlsx | openpyxl | openpyxl | xlsx |
| .xls | xlrd | xlrd | xls |
| .pptx | python-pptx | pptx | pptx |
| .ppt | python-pptx | pptx | pptx |
| .pdf | pypdf | pypdf | pdf |
| .epub | ebooklib | ebooklib | epub |

以下格式无需额外依赖，标记为完整安装时可省略 `--with`：
`.html` `.htm` `.csv` `.json` `.xml` `.png` `.jpg` `.jpeg` `.gif` `.bmp` `.tiff` `.webp` `.mp3` `.wav` `.m4a` `.ogg` `.flac` `.zip`

**uv 环境等效命令**（手动安装参考，脚本自动处理）：
```bash
# 安装 markitdown 及全部可选依赖（一次性）
uv tool install markitdown --with python-docx --with openpyxl --with python-pptx --with pypdf --with xlrd --with ebooklib

# 或仅安装当前文件所需依赖
uvx --with python-docx markitdown input.docx -o output.md
```

## 2.5 旧格式预处理（v2.3+）

`.doc` 和 `.ppt`（Office 97-2003 二进制格式）不被 markitdown 直接支持。`convert.py` 在转换前自动尝试两种方式转为新版格式，其中 LibreOffice 按四级优先级链定位 `soffice` 可执行文件：

| 旧格式 | 目标格式 | 方式 1 | 方式 2 |
|--------|---------|--------|--------|
| `.doc` | `.docx` | Word COM (仅 Windows, `Documents.Open` → `SaveAs2`) | `soffice --headless --convert-to docx` |
| `.ppt` | `.pptx` | PowerPoint COM (仅 Windows, `Presentations.Open` → `SaveAs`) | `soffice --headless --convert-to pptx` |

**LibreOffice 定位优先级链（v2.8）**：
1. `shutil.which("soffice")` — PATH 中的 soffice
2. `$SOFFICE_PATH` 环境变量
3. 按平台分叉的常见安装路径（`os.path.exists` 校验）
4. 裸名 `"soffice"` 兜底

> 🔴 **CHECKPOINT**：若 .doc/.ppt 旧格式且 COM 和 LibreOffice 均不可用，**必须立即暂停**，明确告知用户需安装 Microsoft Office（含 Word/PowerPoint）或 LibreOffice，等待用户确认后再继续。禁止静默跳过旧格式文件。

`.xls` 则由 markitdown 原生支持（`[xls]` 可选依赖组，底层 `xlrd`），无需预处理。

## 3. 命令参考

### 3.1 智能转换（推荐）

```bash
# 单文件转换（自动检测依赖 + 清洗）
python scripts/convert.py input.docx -o output.md

# 使用默认输出名（同目录下 input.md）
python scripts/convert.py input.pdf

# 跳过文档摘要
python scripts/convert.py data.xlsx --no-summary

# 静默模式
python scripts/convert.py report.pptx -q
```

> 🔴 **CHECKPOINT**：若 `-o` 指定的输出文件已存在，convert.py 会直接覆盖。覆盖前**必须**暂停并告知用户输出路径已存在已有内容（如上次转换结果、手动修正后的版本），等待用户确认是否覆盖。若用户拒绝，改用 `-o <新文件名>` 或先备份。

### 3.2 降级转换器

当 markitdown 无法处理（依赖缺失且自动安装失败、超时、加密文档等），`convert.py` 自动启用原生降级：

| 格式 | 降级方案 | 能力 |
|------|---------|------|
| .docx / .doc | python-docx | 提取段落样式→标题层级、表格→Markdown 表格、粗体短文本→内嵌标题 |
| .xlsx / .xls | openpyxl | 每个 Sheet → H2 章节，数据行→ Markdown 表格 |
| .pptx | python-pptx | 每页幻灯片→ H2 章节，文本层级保留，表格自动转换 |

降级转换器的输出同样经过后置清洗流程，质量标准与 markitdown 一致。

### 3.3 批量转换

> 🔴 **CHECKPOINT**：批量转换前**必须**向用户确认：源目录路径、目标输出路径、待转换文件数量（预估）、限定格式（如有 `--ext`）。等待用户确认后再启动。禁止不经确认即递归遍历整个目录。

```bash
# 递归转换整个目录
python scripts/batch_convert.py <源目录> <输出目录>

# 仅转换指定格式
python scripts/batch_convert.py docs/ output/ --ext .pdf .docx --clean
```

### 3.4 单独后置清洗

```bash
# 清洗单个文件
python scripts/post_clean.py output.md

# 注入摘要后输出到新文件
python scripts/post_clean.py output.md --summary-file summary.txt -o cleaned.md

# 仅检查结构不修改
python scripts/post_clean.py output.md --check-only
```

## 4. 后置清洗与 RAG 优化

`convert.py` 内联了后置清洗逻辑，无需单独调用 `post_clean.py`。清洗流程：

**噪声模式去除**（6 类 15+ 正则）：

| 类别 | 匹配模式 |
|:---|:---|
| 工具水印 | `[Generated by ...]` / `Converted by markitdown` / `[Created with ...]` / `Powered by ... markitdown` |
| 页码标记 | `Page X of Y` / `[PAGE X]` / `--- Page X ---` |
| 机密标记 | `Confidential` / `DRAFT` / `Internal Use Only` / `For Review Only` |
| 版权声明 | `© YYYY` / `All Rights Reserved` |
| 空白压缩 | 连续 3+ 空行 → 2 行 |
| 行尾空格 | 移除空行末无用空格 |

**标题层级修复**：
- 多 H1 → 仅保留首个，其余降为 H2
- 层级跳跃（如 H1→H3 无 H2）→ 补过渡标题
- 无 H1 → 从文件名推断后注入

**表格分隔符补全**：检测 `|---|` 缺失行并补全。

**文档摘要注入**：提取首段或首个 H1 后段落作为摘要。

完整清洗项及正则模式详见 [REFERENCE.md §1](REFERENCE.md)。

## 5. 异常处理

### 5.1 错误分类与处理

| 错误类型 | 典型症状 | 原因 | 处理方式 |
|:---|:---|:---|:---|
| 依赖安装失败 | `pip install` 超时或报错，转换终止 | Python 包索引不可达 / 权限不足 / 包版本冲突 | 终止转换，输出具体缺失的包名，提示用户手动 `pip install <pkg>` |
| markitdown 失败 | markitdown CLI 返回非零退出码 | 文件格式损坏 / markitdown extras 缺失 / 未知格式 | 自动切换到原生降级转换器（python-docx/openpyxl/python-pptx），降级后仍经后置清洗 |
| 原生降级也失败 | 降级转换器报错或输出空内容 | 加密文档 / 文档严重损坏 / 格式不兼容 | 终止转换，输出"文档可能已加密或格式不受支持" |
| 加密文档 | markitdown + 原生库均提示 `File is encrypted` 或类似信息 | 文档受密码保护 | 终止转换，提示"文档已加密，请解密后重试"。**禁止反复重试** |
| 旧格式无预处理环境 | .doc/.ppt 文件但 COM 和 LibreOffice 均不可用 | Windows 未装 Office `pywin32`；Linux/macOS 未装 LibreOffice | 🔴 CHECKPOINT：暂停，告知用户安装 Office 或 LibreOffice |
| 批量场景单文件失败 | 个别文件转换报错，其余正常 | 该文件格式异常 / 权限不足 / 正在被其他程序占用 | 跳过该文件，在 `_conversion_errors.log` 记录文件名+错误原因，其余文件继续 |
| 输出路径不可写 | convert.py 写文件时报 PermissionError | 目标目录不存在且无创建权限 / 磁盘满 | 终止，提示检查输出路径权限和磁盘空间 |
| uv 不在 PATH | `ensure_markitdown_extras()` 检测不到 uv | uv 未安装或未加入 PATH | 跳过 markitdown extras 安装，转换仍可进行（仅限内置支持格式） |
| 网络驱动器不可达 | `[WinError 2]` 或 `FileNotFoundError` | 网络驱动器断连（E:\Marvis_Data 等） | 提示用户检查网络驱动器连接状态 |

> 🔴 **CHECKPOINT**（参见 §2.5 预处理流程）：以下两类情况必须立即暂停，等待用户介入，禁止自动跳过或反复重试：
> - **加密文档**（`File is encrypted`）：首次检测到即终止该文件转换，提示用户解密后重试
> - **旧格式无预处理环境**（.doc/.ppt 且 COM 和 LibreOffice 均不可用）：告知用户安装 Office 或 LibreOffice

### 5.2 静默失败防护

| 静默失败形态 | 检测机制 |
|:---|:---|
| 清洗跳过某些噪声模式 | §4 噪声模式库覆盖 15+ 正则 |
| 降级转换器输出格式不一致 | 降级输出同样经过后置清洗 |
| 批量转换某文件失败未记录 | `_conversion_errors.log` 自动汇总 |
| 标题层级修复误触发（二次修复） | v2.6+ 标题修复仅执行一次，有状态标记 |
| markitdown extras 缺失但转换仍"成功" | `convert.py` 启动时检测全部可选依赖 |

详见 [REFERENCE.md §7](REFERENCE.md)。

## 6. 输出与反馈规范

转换成功后反馈示例：

> 成功将 `report.pdf` 转换为 Markdown [markitdown] | H1=1 H2=5 H3=12 | 表格=3 | 48,256 bytes
> 输出: E:\output\report.md

**反馈格式固定模板**（所有转换结果必须统一使用）：

```
{状态}将 `{源文件名}` 转换为 Markdown [{转换方式}] | H1={n} H2={n} H3={n} | 表格={n} | {文件大小}
输出: {绝对路径}
```

| 字段 | 说明 | 取值 |
|:---|:---|:---|
| 状态 | 转换结果 | `成功` / `失败` / `部分成功`（批量场景） |
| 转换方式 | 所用引擎 | `markitdown` / `原生降级(python-docx)` / `原生降级(openpyxl)` / `原生降级(python-pptx)` |
| H1/H2/H3 | 标题层级统计 | 整数，无标题时写 0 |
| 表格 | Markdown 表格数量 | 整数 |

**批量转换反馈**：
```
批量转换完成 | 总计=12 | 成功=10 | 失败=2
失败详情: _conversion_errors.log
输出: E:\output\markdown\
```

> 输出质量自检清单（7 项）已移至 [REFERENCE.md §2](REFERENCE.md)。

## 7. 脚本清单

**前置校验**：执行转换前，Agent 应通过 `python -c "from pathlib import Path; import sys; sys.path.insert(0,'scripts'); assert Path('scripts/convert.py').exists(), 'convert.py missing'"` 确认核心脚本存在。

| 脚本 | 用途 |
|------|------|
| `scripts/convert.py` | 智能转换引擎（推荐）：依赖自动补全 + markitdown + 降级兜底 + 内联清洗 |
| `scripts/batch_convert.py` | 批量转换：递归遍历目录、保持结构、异常收集 |
| `scripts/post_clean.py` | 后置清洗：去水印、注入摘要（含标题修复、面包屑注入、质量评分） |
| `scripts/platform_detect.py` | 平台检测模块（v2.8）：启动时检测 OS/版本/能力，`best_office_tool()` 返回最优办公软件路由 |

## 8. 平台兼容性与更新记录 (Platform & Changelog)

Windows / Linux / macOS 三平台完全支持。关键约束：`convert.py` 启动时自动检测平台能力；网络驱动器路径使用 `python_executor` 执行；全部脚本使用 `pathlib.Path` 适配路径分隔符。详见 [REFERENCE.md §3](REFERENCE.md)。更新记录见 [REFERENCE.md §6](REFERENCE.md)。

## 9. 反模式与禁止清单 (Anti-Patterns & Blacklist)

**核心禁令**（完整版见 [REFERENCE.md §4](REFERENCE.md)）：

1. **绕过 convert.py 直接裸调 markitdown** → 跳过依赖补全+清洗管线，输出含残留水印。必须使用 `python scripts/convert.py`
2. **用 shell_executor 执行网络驱动器脚本** → PowerShell WinError 2。使用 `python_executor`
3. **对加密文档反复重试** → 首次失败即终止，提示解密后重试
4. **.doc/.ppt 无预处理环境时强行转换** → 告知用户安装 Office 或 LibreOffice
5. **批量转换不设 --ext 过滤** → 产出 .jpg.md/.zip.md。必须 `--ext .pdf .docx .pptx`
6. **重复清洗已清洗过的输出** → 摘要叠加。不要对 convert.py 输出再调 post_clean.py

**禁止操作**：`post_clean.py` 输出→ `convert.py` 输入（循环清洗）；`.xls` 用 COM 预处理；空 `--ext` 参数；二次 convert 已成功输出。

## 10. 可验证性检查表 (Verification Checklist)

### 10.1 验收标准

每次转换完成后，Agent 必须对输出文件执行以下逐项检查。任一未通过 = 转换失败，需进入 §5 异常处理流程。

| # | 检查项 | 通过标准 | 验证命令 |
|:---|:---|:---|:---|
| V1 | 文件存在且非空 | 输出文件大小 > 0 字节 | `python -c "import os; s=os.stat('<输出.md>'); assert s.st_size>0, '空文件'"` |
| V2 | 编码正确 | 文件可被 UTF-8 解码且无乱码 | `python -c "open('<输出.md>',encoding='utf-8').read()"` |
| V3 | 无残留水印 | 不含 `Generated by markitdown` / `Confidential` / `Page X of Y` | `python -c "import re; t=open('<输出.md>').read(); assert not re.search(r'Generated by|Page \d+ of \d+',t), '有水印'"` |
| V4 | 标题层级正常 | 至少存在 1 个 H1，且 H 层级无跳跃（H1→H3 无 H2 报错） | `python -c "import re; t=open('<输出.md>',encoding='utf-8').read(); hs=re.findall(r'^(#{1,6})\s',t,re.M); levels=[len(h) for h in hs]; jumps=[i for i in range(1,len(levels)) if levels[i]-levels[i-1]>1]; assert len(hs)>0 and levels[0]==1, f'无H1' if not hs else f'H{levels[0]}打头'; assert not jumps, f'层级跳跃: {jumps}'; print('PASS')"` |
| V5 | 表格完整性 | 无 `|---|` 分隔符缺失、无空表格、无 `||` 异常分隔符 | `python -c "import re; t=open('<输出.md>').read(); pipes=[l for l in t.split(chr(10)) if l.startswith('|')]; assert len(pipes)>0 or '无表格', '表格可能损坏'"` |
| V6 | 源文件对应 | 每 1 个源文件产生 1 个输出文件（批量模式无漏转） | `python -c "print(len(os.listdir('<输出目录>')))"` 对比源文件数 |

### 11.2 自检清单 (Agent 执行后必查)

Agent 在完成转换并写盘后，必须在最终回复中逐项确认以下内容（直接输出结果，不展开过程）：

- [ ] 输出文件路径已确认存在且非空（V1）
- [ ] 输出内容已抽检前 3 段，无乱码/水印/页码残留（V2+V3）
- [ ] 标题层级已检查，无跳跃（V4）
- [ ] 表格（如有）分隔符完整（V5）
- [ ] 批量转换时：源文件数与输出文件数一致（V6）

### 11.3 回归测试与快速验证

回归测试用例（RT1-RT3）和 Python 一键验证 oneliner 已移至 [REFERENCE.md §5](REFERENCE.md)。
