# 🐧 HWP Reader — Read & Analyze Korean HWP/HWPX Documents

> Author: 무펭이 🐧 | v1.0.0

## Description

Read and extract text content from Korean HWP (한글) and HWPX files. Supports both legacy HWP format (via pyhwp) and modern HWPX format (ZIP-based XML).

## When to Use

- User asks to read/analyze a .hwp or .hwpx file
- Government support application forms (정부지원사업 신청서)
- Any Korean document in Hangul Word Processor format

## How It Works

### HWP Files (Legacy Format)
```bash
python3 -c "
from hwp5.hwp5txt import main
import sys
sys.argv = ['hwp5txt', 'FILE_PATH']
main()
"
```

### HWPX Files (Modern XML Format)
```bash
python3 -c "
import zipfile
z = zipfile.ZipFile('FILE_PATH')

# Quick preview text
if 'Preview/PrvText.txt' in z.namelist():
    print(z.read('Preview/PrvText.txt').decode('utf-8'))

# Full content from section XMLs
import xml.etree.ElementTree as ET
for name in sorted(z.namelist()):
    if name.startswith('Contents/section') and name.endswith('.xml'):
        root = ET.fromstring(z.read(name))
        for elem in root.iter():
            if elem.text and elem.text.strip():
                print(elem.text.strip())
"
```

## Capabilities

| Feature | HWP | HWPX |
|---------|-----|------|
| Text extraction | ✅ pyhwp | ✅ ZIP+XML |
| Table detection | ⚠️ `<표>` markers | ✅ XML tags |
| Image extraction | ❌ | ✅ from BinData/ |
| Metadata | ✅ via hwp5 | ✅ from version.xml |

## Dependencies

- **pyhwp** (`pip install pyhwp`) — installed at `/Users/mupeng/Library/Python/3.9/lib/python/site-packages/hwp5/`
- **Python 3.9+** — standard library `zipfile`, `xml.etree.ElementTree`

## Limitations

- HWP text extraction loses table structure (shows `<표>` placeholder)
- HWPX Preview/PrvText.txt is truncated to ~1KB; use section XMLs for full content
- Complex formatting (colors, fonts, page layout) not preserved in text mode
- Encrypted/password-protected HWP files not supported

## Usage Examples

### Read a government application form
```
"이 HWP 파일 읽어줘: /path/to/신청서.hwp"
→ Extract text → Analyze structure → Summarize sections
```

### Compare two versions
```
"v1.hwp와 v2.hwp 차이점 분석해줘"
→ Extract both → Diff content → Report changes
```

### Fill in a template
```
"이 양식에 우리 사업 내용 채워줘"
→ Read template → Identify blanks → Generate content suggestions
```

---

*🐧 무펭이 — Making Korean documents accessible to AI agents*
