---
name: pdf-font-fixer
display_name: pdf字体乱码修复神器
display_name_en: PDF Fonts Fixer
description: PDF 中文字体乱码与「能显示但打印不出来」的体检与修复工具。导出前检测字体风险，交付前逐字符审计并做交付门禁，也能直接修复已有 PDF 的方块字、缺字、文字消失。支持 PDF 字体检测、字体字典结构校验、字体修复、PPT 转 PDF 递进导出、缺字兜底；不内嵌任何字体，自动发现本机可用的 TrueType 中文字体。其它 skill 导出 PDF 后必须调用 gate.py 作为交付门禁。当用户提到 PDF 乱码、方块字、问号、字体缺失、打印异常、打印机报错（如佳能「未导入太大的图像或格式不受支持的文件」）、手机预览异常、PPT 导出 PDF、PDF 字体检查时使用。
description_zh: 专治「本机看着正常、别人打开全是方块」的 PDF 字体问题。一条命令完成字体体检、逐字符审计与交付门禁，也能直接修复已有 PDF 的乱码、缺字与文字消失，无需重做排版。
description_en: Diagnose and repair broken Chinese fonts in PDFs. Detect risky font outlines before delivery, audit every glyph, gate releases, and fix existing PDFs with tofu boxes, missing glyphs, or dropped text — without redoing the layout.
examples_zh:
  - "帮我检查这份 PDF 发到手机上会不会中文乱码"
  - "这份 PDF 在别的电脑上显示成方块，帮我修好"
  - "PPT 导出的 PDF 有字显示不出来，给我一份到处都能正常打开的版本"
examples_en:
  - "Check whether this PDF will display Chinese correctly on other devices"
  - "This PDF shows tofu boxes on another computer — fix it for me"
  - "The PDF exported from my slides has missing text; give me a version that renders everywhere"
version: 1.1.1
author: "多裴港格"
---

# pdf字体乱码修复神器

**专治 PDF 的「字体分裂症」：你在自己电脑上看一切正常，发出去却变成方块、问号、乱码，甚至整段文字凭空消失——但复制出来的文字又是对的。**

问题不在内容，而在 PDF 内嵌字体的轮廓格式。本技能在**交付前**把风险查出来，也能把**已经出问题的 PDF** 救回来，无需重做排版。

## 0. 铁律（不得让步）

1. **任何要交付的 PDF，导出后第一件事就是 `gate.py`**。退出码非 0 一律不许交付。
2. **不内嵌任何字体**。字体靠 `discover.py` 扫本机已有的 TrueType 中文字体
   （Windows→微软雅黑/宋体，macOS→Heiti SC，Linux→文泉驿/Droid/Noto Sans SC）。
   本机没有就在 SKILL 里给**官方获取方式**，绝不打包字体进 skill。
3. **不自动安装 ghostscript**，也不从任何非官方来源取二进制。缺了就打印官方获取方式，
   然后**直接回退到扫描版**。
4. **修不动的兜底产物必须双份**：一份**原生直接导出**（可复制），一份带前缀
   **`【轮廓版】`** 或 **`【扫描版】`**。让用户自己拿手机对比——
   **原生版能正常显示，就不要用轮廓/扫描版**。
5. 修复按代价递进：能无损就不转轮廓，能转轮廓就不出位图。

## 1. 为什么会乱码

PDF 里文字靠「字体程序」画字形，轮廓格式决定能不能显示：

| 轮廓格式 | PDF 内部 | 实测结果（华为真机） |
|---|---|---|
| **TrueType**（glyf） | `FontFile2` / `CIDFontType2` | ✅ 正常 |
| **CFF（OpenType 包装）** | `FontFile3` / `/OpenType` | ❌ 画不出字形 → 中文乱码（weasyprint、Chrome 类产物） |
| **CFF（裸 CIDFontType0C）** | `FontFile3` / `/CIDFontType0C` | ⚠️ 能显示；但 charset 错位就乱码（WPS 类产物）→ 修 charset 可无损修好 |
| 未嵌入 | 无字体流 | ❌ 换设备就缺字 |

⚠️ **两种 CFF 不能混为一谈**（「CFF 一律不支持」的说法已被真机推翻）：
`/OpenType` 包装是真渲染不出；裸 `/CIDFontType0C` 能渲染，乱码通常只是 charset 映射错位。

## 1.5 第二类病：字体字典结构畸形（能显示，但打不出来）

上面的表回答的是「**能不能画出字形**」。还有一类病，字形完全画得出来、电脑和手机预览都正常，
**打印机却直接拒收整个文件**——报错常是佳能那句
「未导入太大的图像或格式不受支持的文件」。这句是通用兜底文案，**跟图像大小无关**：
实测触发它的 PDF 只有 65 KB、2 页，`pdfimages` 列表里一张图都没有。

真凶是字体的**字典结构**：

```
/Subtype /TrueType          ← 简单字体（不是 Type0）
/Flags 4                    ← Symbolic（符号字体）
/FirstChar 0                ← 字符码从 0 起，落入保留区
/Widths [0 1000 1000 1000]  ← 占位假宽度
（无 /Encoding）
正文：<010203> Tj           ← 单字节伪编码，全靠 /ToUnicode 才认得出是汉字
```

后果是分层的：

| 解析方 | 表现 |
|---|---|
| Adobe / 系统预览 / WPS / pymupdf | 靠 `/ToUnicode` 容错 → **看着完全正常** |
| 佳能 PRINT、惠普老固件等精简 RIP | 解析字体字典失败 → **整个文件拒收** |

典型来源：**python-docx 生成的 docx → LibreOffice 导出 PDF**（docx 里中文 run 没写
`w:eastAsia`，LibreOffice 就把中文字体当符号字体导出）。

⚠️ **不能只看 `/Flags` 就判死**：CID 字体（`/Type0` + `CIDFontType2/0`）标 Symbolic
是**正常做法**，中文 PDF 大量如此（Chrome 导出即是）。只有**简单字体**（`/Subtype /TrueType`
或 `/Type1`）的 Symbolic + ToUnicode 里出现 CJK，才是伪符号化。

判定由 `scripts/structcheck.py` 完成，`detect.py`/`gate.py` 已自动带上这一关。

## 2. 字体怎么来（不内嵌，靠发现）

```bash
python3 scripts/discover.py            # 列出本机所有中文字体：✅TrueType / ❌CFF
python3 scripts/discover.py --best     # 只输出最优的 Regular / Bold 两行路径
python3 scripts/discover.py --json
```

判定逻辑：**扫各平台字体目录 → 读文件头判轮廓（`OTTO`=CFF，其余=TrueType）→ 抽查常用汉字判是否中文正体 → TrueType 优先、字形数降序**。结果缓存复用。

### 本机没有 TrueType 中文字体时，给这些**官方**渠道

| 平台 | 官方来源 |
|---|---|
| Windows | 微软雅黑 / 宋体 / 黑体**系统自带**，一般无需安装 |
| macOS | Heiti SC **系统自带**；PingFang SC 是 CFF，不适合嵌 PDF |
| Linux | 文泉驿：https://wenq.org/wqy2/index.cgi?ZenHei |
| 通用 | Noto Sans SC（选 **.ttf**，不要 .otf）：https://fonts.google.com/noto/specimen/Noto+Sans+SC |
| 通用 | noto-cjk 官方发布：https://github.com/notofonts/noto-cjk/releases |

装完跑一次 `python3 scripts/discover.py --no-cache` 确认扫到 ✅。

## 3. 依赖与官方获取方式

| 依赖 | 用途 | 缺失后果 | 官方获取 |
|---|---|---|---|
| `pymupdf` | 读字体 / 渲染位图 / 无 gs 时转轮廓 | 无法工作 | `pip install pymupdf` |
| `fontTools` | CFF 解析 / OTF→TTF | `--deep` 与 to-ttf 不可用 | `pip install fonttools` |
| `pikepdf` | 改字体内嵌流（charset 修复）、字体字典结构校验、去 Symbolic 标记 | 跳过结构校验与第 1a/1b 级修复 | `pip install pikepdf` |
| `cairosvg` | 无 ghostscript 时把 SVG 转 PDF（转轮廓的第二条路） | 无 gs 时无法转轮廓 → 回退扫描版 | `pip install cairosvg` |
| `ghostscript` | 转矢量轮廓（首选，质量略好） | 自动改用 pymupdf + cairosvg；两者都无才回退扫描版 | 见下 |
| `soffice` | PPT→PDF | `pptx.py` 不可用 | LibreOffice 官网 https://www.libreoffice.org/download/ |

**ghostscript 官方获取**（脚本检测不到时会自动打印这段，且不会擅自安装）：

```
Debian/Ubuntu : sudo apt-get install ghostscript
Fedora        : sudo dnf install ghostscript
macOS         : brew install ghostscript
Windows       : winget install ArtifexSoftware.GhostScript
官方下载页     : https://ghostscript.com/releases/gsdnld.html
装不上也没关系：自动跳过「转轮廓」，直接出【扫描版】。
```

一条命令看全：`python3 scripts/locate.py --check`

## 4. 命令

```bash
S="<skill>/scripts"

# ① 体检（整体：有哪些字体、轮廓类型）
python3 $S/detect.py 产物.pdf              # 退出码 0/2；--deep 加查 charset 错位
# ①b 结构体检（字体字典：Symbolic、FirstChar、编码、码位复用 + RIP 兼容性）
python3 $S/structcheck.py 产物.pdf         # 退出码 0/2；单独排查"能显示却打不出来"
# ② 逐字符审计（每个字落在哪个字体、有没有豆腐块）
python3 $S/verify.py 产物.pdf --list-chars
# ③ 交付门禁（= ① + ①b + ②，**交付前必跑这条**）
python3 $S/gate.py 产物.pdf                # 退出码 0=可交付 / 2=不合格
python3 $S/gate.py 产物.pdf --auto-fix     # 不合格时自动产出「无损版+轮廓版」兜底，修出可用件则退 0

# ④ 修复已有 PDF（递进：去 Symbolic → charset 重写 → 转轮廓 → 扫描版）
python3 $S/fix.py 坏.pdf                   # 自动
python3 $S/fix.py 坏.pdf --keep-copy       # 只接受无损修复，做不到就报错并给替换建议
python3 $S/fix.py 坏.pdf --charset-only    # 只修 charset（保留复制，需真机确认）

# ⑤ PPT → PDF（递进三步，前一步成就不再走后面）
python3 $S/pptx.py 演示.pptx
python3 $S/pptx.py 演示.pptx --keep-copy   # 只接受第 1 步（保留复制）

# ⑥ 字体工具
python3 $S/fontkit.py list                 # 本机中文 TrueType
python3 $S/fontkit.py find "Noto Sans SC"
python3 $S/fontkit.py to-ttf x.otf -o x.ttf --text "用到的字"    # OTF→TTF（先子集，快）
python3 $S/fontkit.py lint x.ttf --text "文本"                   # 查缺字（豆腐块预警）

# ⑦ 缺字兜底（主字体覆盖不全时，造一个 TrueType 兜底字体并给 CSS 片段）
python3 $S/autofallback.py --from-json cards.json \
        --main <主字体.ttf> -o fallback.ttf --css fb.css
#    退出码 0 = 主字体够用（不产生文件）；3 = 已生成兜底
```

## 5. 修复策略（fix.py 内部递进）

| 级 | 病因 | 手段 | 复制能力 | 产物命名 |
|---|---|---|---|---|
| 0 | 字体没问题 | 什么都不做 | 保留 | — |
| 1a | 伪 Symbolic（简单 TrueType 标符号字体） | 改 `/Flags` 为 Nonsymbolic + 清 Tagged 结构树与私有 trailer 键 | **保留** | `原名_无损修复.pdf` |
| 1b | charset 错位（WPS 型裸 CFF） | 重写 charset 为 Identity | **保留** | 原文件名 |
| 2 | CFF 轮廓 / 未嵌入 / 1a 没治好 | 转矢量轮廓（ghostscript 优先，无则 pymupdf+cairosvg） | 失去 | **`【轮廓版】原名.pdf`** |
| 3 | 上一步不可用 / 需要绝对保险 | 300dpi 位图 | 失去 | **`【扫描版】原名.pdf`** |

⚠️ **第 1a 级只摘标记，不保证打印机认账** —— 结构畸形可能还在（FirstChar 0、缺 /Encoding
改不了）。所以走到这一级时 `fix.py` **会同时输出无损版和轮廓版两份**，并明确告诉用户：
先试无损版，打不了再换轮廓版。

**第 2/3 级必须同时保留「原生直接导出」的那份**（fix 的输入文件、pptx 第 1 步的导出结果），
并在输出里明确提示：**先拿手机预览原生版，能正常显示就不需要轮廓/扫描版**。

## 5.5 docx → soffice → PDF：产物必然带结构病（实测结论）

2026-11 实测：用 python-docx 生成 docx（`w:rFonts` 的 ascii/hAnsi/eastAsia/cs 四属性
全部写对、`w:hint="eastAsia"` 也在），再 `soffice --convert-to pdf`：

| docx 里写的字体 | 转出来的 PDF 字体 |
|---|---|
| `Noto Sans SC`（TTF，cmap 含 3,1 Unicode 表） | `simple TrueType` + `/Flags 4` + `/FirstChar 0` + 无 `/Encoding` |
| `Noto Sans CJK SC`（系统 ttc） | `Type 1` + `Builtin` 编码（更糟） |

也就是说：**这不是 docx 写错了，是 LibreOffice 嵌入 CJK 字体的方式**——它用
「code = 字形索引」的简化字体，而不是 `/Type0` + `Identity-H`。电脑上能显示，
打印机 RIP 不认。

**所以凡走 docx → soffice → PDF 的链路，产物必然过不了结构关。**
对策不是「每次都手工转曲」，而是让门禁自己兜住：

```bash
python3 "$FIXER/scripts/gate_hook.py" 产物.pdf --min-version 1.1.0
```

`gate_hook.py` **默认带 `--auto-fix`**：不通过时自动把「可打印的轮廓版」写回原路径、
原件另存为 `xxx_原生.pdf`，并返回 0，调用方流程不中断、拿到的就是可交付文件。
要纯报告就加 `--no-auto-fix`。

⚠️ **auto-fix 的代价**：原路径那份变成轮廓版后**文字不可复制/搜索**。需要复制检索时用
`xxx_原生.pdf`。这条必须在交付时告诉用户，不能静默替换。

> 想彻底不产生结构病，只能避开 LibreOffice 导出（换 weasyprint/reportlab 直接生成
> `/Type0` 字体，或直接用轮廓 PDF）。这属于各 skill 自己的架构选择，不在本 skill 强制范围。

## 6. PPT 三步法（递进，不是三份并列）

```
① 本机有全部字体的 TrueType 款 → soffice 导出 → gate 通过 → 结束（单份，可复制，字形 100%）
   ↓ 做不到（缺字体 / 只有 CFF）
② 导出原生 + 【轮廓版】两份 → 结束（轮廓版 100% 能显示，不可复制）
   ↓ 连转轮廓也不可用（无 ghostscript）
③ 导出原生 + 【扫描版】两份 → 结束
```

## 7. 自动兜底（主字体缺字时）

**不要依赖排版引擎自动回退**。实测：用 Noto Sans SC 排版时，`𠮷`、`한국어` 被自动退到
`Noto Sans CJK`（CFF）——字显示出来了，PDF 里混进 CFF，手机上照样乱码。

正确做法：显式造兜底字体并挂链

```bash
python3 $S/autofallback.py --from-json cards.json --main <主字体> -o fb.ttf --css fb.css
# CSS: font-family: "主字体", "CJKFALLBACK", sans-serif;   ← 兜底放第二位
```
实测：4 个缺字 → 0.9 秒 / 2 KB。`gate.py` 会逐字符确认这些字确实落在 TrueType 兜底字体上。

**优先级**：能换一个覆盖全的 TrueType 主字体就别用兜底（混排会出现两种字面）。

## 8. 跨环境定位

不假设安装位置。`locate.py` 的优先级：

| 优先级 | 依据 |
|---|---|
| 0 | **脚本自身位置**（`__file__` 往上两级）—— 能跑脚本就说明找对了 |
| 1 | 环境变量 `PDF_FONT_FIXER` |
| 2 | 多平台约定目录：`~/.skills`、`~/.claude/skills`、`~/.workbuddy/skills`、`~/.codebuddy/skills`、`~/.config/ima/skills`、`AppData/Roaming/*`、项目内 `./skills` |
| 3 | 用户目录限深搜索（≤4 层） |

调用方（其它 skill）一行候选链，跨 bash/zsh：

```bash
for c in "$PDF_FONT_FIXER" "$HOME/.skills/pdf-font-fixer" "$HOME/.claude/skills/pdf-font-fixer" \
         "$HOME/.workbuddy/skills/pdf-font-fixer" \
         "$HOME/.codebuddy/skills/pdf-font-fixer" "./skills/pdf-font-fixer"; do
  [ -f "$c/scripts/gate.py" ] && FIXER="$c" && break
done
[ -z "$FIXER" ] && { echo "❌ 未找到 pdf-font-fixer，请设置 PDF_FONT_FIXER"; exit 2; }
python3 "$FIXER/scripts/gate.py" 产物.pdf
```

## 9. 踩坑速查

1. **CFF 无法在 PDF 层"转换"成 TrueType** —— 轮廓格式转换必须回到字体文件层面（三次→二次贝塞尔）。已有坏 PDF 只有两条路：转轮廓（牺牲复制）或换字体重出。
2. **同样是 CFF，`/OpenType` 包装和裸 `/CIDFontType0C` 是两种病**。WPS 修复工具只认后者。
3. **排版引擎的自动回退会把字退到 CFF 字体** → 必须显式挂兜底链 + 逐字符验收。
4. **pymupdf 对 CIDFontType0 返回 `ext='cid'`**，别只认 `otf`/`cff`，否则会误判通过（本项目已修）。
5. **fontTools 4.6x 的 `maxp.recalc()` 不填 v1.0 扩展字段**，手工拼 glyf 后会 `KeyError: 'maxZones'`，必须自己补。
6. **`.ttc` 不要直接嵌 PDF**（多字面取哪个不可控），先提取面存 `.ttf`。
7. **转轮廓后文字不可搜索**（`get_text()` 长度 = 0），交付时要说明。
8. **「能渲染」不等于「能打印」**（2026-11 实测补）。pymupdf 的容错远强于打印机 RIP：
   一份 65 KB、零图像、2 页 A4 的 PDF，新旧两版肉眼完全一致，佳能却直接拒收。所以
   `gate.py` 除了轮廓格式与逐字归属，还必须过 `structcheck.py` 的字典结构关。
9. **Symbolic 不能一概而论**。CID 字体（`/Type0`）标 `/Flags 4` 是正常做法（Chrome 导出即是），
   只有**简单字体**（`/Subtype /TrueType`、`/Type1`）的 Symbolic + ToUnicode 含 CJK 才是伪符号化。
   误报会让用户对门禁失去信任，宁可少判不可错判。
10. **无 ghostscript 用 pymupdf 转轮廓时，SVG 的 `width`/`height` 必须补 `pt` 单位**。
    cairosvg 把无单位数值当 px（96dpi），A4 会被缩成 446×631 pt。
11. **等宽字体的 `/Widths` 全同值是合法的**，不能当「假宽度」报。查 `Flags` bit0（FixedPitch），
    再兜一层字体名（`Mono`/`Courier`/`NimbusMon`）。
