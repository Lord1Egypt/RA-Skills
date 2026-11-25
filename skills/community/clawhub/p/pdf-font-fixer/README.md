# pdf-font-fixer

交付 PDF 前的字体关卡：**本机看着正常、别人手机上中文乱码**、**能显示却打印不出来** 的体检、修复与门禁。

Smartphone-safe PDF fonts: detect, verify, gate and fix CJK font embedding issues.

## 问题

PDF 里文字靠「字体程序」画字形，轮廓格式决定别人手机能不能显示：

| 轮廓格式 | PDF 内部 | 实测（华为真机） |
|---|---|---|
| TrueType（glyf） | `FontFile2` / `CIDFontType2` | ✅ 正常 |
| CFF（OpenType 包装） | `FontFile3` / `/OpenType` | ❌ 中文乱码 |
| CFF（裸 CIDFontType0C） | `FontFile3` / `/CIDFontType0C` | ⚠️ charset 错位则乱码，可无损修 |
| 未嵌入 | 无字体流 | ❌ 换设备缺字 |

另有一类「字体字典结构畸形」：字形画得出来、预览也正常，但打印机拒收整个文件
（如佳能「未导入太大的图像或格式不受支持的文件」）。典型来源是 python-docx →
LibreOffice 导出，中文字体被当成 Symbolic 简单字体。

## 能力

- `detect.py` — PDF 字体体检（含 `--deep` charset 错位检查）
- `structcheck.py` — 字体字典结构校验（伪 Symbolic 简单字体等打印杀手）
- `verify.py` — 逐字符审计，定位豆腐块
- `gate.py` — 交付门禁，退出码非 0 不许交付
- `gate_hook.py` — 供其它 skill 在导出后强制调用门禁的统一钩子
- `fix.py` — 递进修复：charset 重写 → 矢量轮廓 → 300dpi 扫描版，并保留原生版对照
- `_deps.py` — 依赖持久化：沙箱重置后自动从持久目录补齐 pikepdf / pymupdf / fontTools
- `pptx.py` — PPT 递进式导出（单份可复制 → 轮廓版 → 扫描版）
- `fontkit.py` — 本机中文 TrueType 发现、OTF→TTF、缺字 lint
- `autofallback.py` — 缺字兜底字体生成 + CSS 片段
- `discover.py` / `locate.py` — 跨平台字体发现与 skill 定位

## 设计原则

1. 任何交付 PDF，导出后第一件事跑 `gate.py`
2. **不内嵌任何字体**，只发现本机已有的 TrueType 中文字体
3. 不自动安装 ghostscript，也不从非官方来源取二进制
4. 兜底产物双份，原生版能被手机正常显示就不用轮廓/扫描版
5. 修复按代价递进：无损 → 轮廓 → 位图

## 依赖

`pymupdf`、`fonttools`、`pikepdf`（可选 `ghostscript`、`cairosvg`、`soffice`），全部有官方获取路径；
缺失时脚本自行降级并打印官方安装方式。
无 ghostscript 时优先用 pymupdf + cairosvg 转轮廓，二者都不可用才回退扫描版。
`_deps.py` 会把必需包装进 `~/.pdf-font-fixer-deps`（可用 `PDF_FONT_FIXER_DEPS` 覆盖），
环境重置后自动补齐；字典结构关无法执行时门禁会明确报「不完整」而不是静默放行。

## 用法

```bash
python3 scripts/locate.py --check      # 环境自检
python3 scripts/detect.py 产物.pdf     # 体检
python3 scripts/gate.py   产物.pdf     # 交付门禁（必跑）
python3 scripts/fix.py    坏.pdf       # 修复
```

详见 [SKILL.md](SKILL.md)。

## License

MIT
