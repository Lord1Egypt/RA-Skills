# macOS CJK Font Reference

## The Core Problem

macOS's Chinese fonts come in two flavors:
- **`.ttc`** (TrueType Collection) — multiple fonts in one file. Apple's PingFang.ttc, STHeiti Medium.ttc, and Libian.ttc all use **PostScript outlines** (CFF/Type 2), which `reportlab` and `weasyprint` **cannot load**:
  ```
  reportlab.pdfbase.ttfonts.TTFError: TTC file "X.ttc": postscript outlines are not supported
  ```
- **`.ttf`** (single font) — uses TrueType outlines, which Python font libraries CAN load. These live in `/System/Library/AssetsV2/com_apple_MobileAsset_Font8/.../AssetData/`.

## Working Font Paths (verified 2026-06-11)

| 用途 | 路径 |
|------|------|
| 正文（细黑/中等） | `/System/Library/AssetsV2/com_apple_MobileAsset_Font8/10e7a462a671950b802274fad767b566ff8457d1.asset/AssetData/STXIHEI.ttf` |
| 标题（粗黑） | `/System/Library/AssetsV2/com_apple_MobileAsset_Font8/53fe5be564086fefc7523ccd0a31200acf92e0e5.asset/AssetData/STHEITI.ttf` |
| 注释/引用（楷体） | `/System/Library/AssetsV2/com_apple_MobileAsset_Font8/6331c5916c361af1b83fb8b8b76ef2eece20c8eb.asset/AssetData/Kai.ttf` |
| 中等黑（备选正文） | `/System/Library/AssetsV2/com_apple_MobileAsset_Font8/5feac9245cca79adaf638ded7a4994b1ddb33ca0.asset/AssetData/Hei.ttf` |
| 苹方（仅 CJK，TTF） | 未在 AssetsV2 中找到纯净的苹方 TTF；用 STXIHEI 替代 |

> ⚠️ **路径中的 hash 可能因系统版本/语言包不同而变化。** 用 `find` 验证：
> ```bash
> find /System/Library/AssetsV2 -name "STXIHEI.ttf"
> find /System/Library/AssetsV2 -name "STHEITI.ttf"
> find /System/Library/AssetsV2 -name "Kai.ttf"
> ```

## Verification Snippet

```python
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

for name, path in [
    ('STXIHEI', '/System/Library/AssetsV2/com_apple_MobileAsset_Font8/10e7a462a671950b802274fad767b566ff8457d1.asset/AssetData/STXIHEI.ttf'),
    ('STHEITI', '/System/Library/AssetsV2/com_apple_MobileAsset_Font8/53fe5be564086fefc7523ccd0a31200acf92e0e5.asset/AssetData/STHEITI.ttf'),
    ('Kai',     '/System/Library/AssetsV2/com_apple_MobileAsset_Font8/6331c5916c361af1b83fb8b8b76ef2eece20c8eb.asset/AssetData/Kai.ttf'),
]:
    try:
        f = TTFont(name, path)
        print(f"✓ {name}")
    except Exception as e:
        print(f"✗ {name}: {e}")
```

## Common Failure Modes

### reportlab
```
TTFError: TTC file "X.ttc": postscript outlines are not supported
```
**Fix:** Use `.ttf` files, not `.ttc`. (See paths above.)

### weasyprint
```
WeasyPrint could not import some external libraries.
cannot load library 'libgobject-2.0-0': ...
```
**Fix:** Install pango via Homebrew and set `DYLD_FALLBACK_LIBRARY_PATH`:
```bash
brew install pango
export DYLD_FALLBACK_LIBRARY_PATH=/opt/homebrew/lib
```

### Garbled Chinese in PDF (boxes / question marks)
**Cause:** Font path points to wrong file, or font isn't loaded.
**Fix:** Verify the path with `find`, then verify the font loads with the snippet above.
