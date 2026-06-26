# Style Presets Reference

Detailed font, color, and spacing configuration for all 8 style presets.
These values must match `kai_docx_generator/styles/*.py`.

## Font Family Legend

| Font | Use | Platform |
|------|-----|----------|
| Microsoft YaHei | Default sans-serif for CJK | Windows/macOS |
| Consolas | Monospace body text | Windows/macOS |
| FangSong (仿宋) | Formal documents, contracts, dispatches | Windows (fallback: STFangSong macOS) |
| SimHei (黑体) | Headings in formal documents | Windows (fallback: STHeiti macOS) |
| KaiTi (楷体) | Sub-headings in formal documents | Windows (fallback: STKaiti macOS) |

## Color Legend

| Color | Hex | Use |
|-------|-----|-----|
| Dark navy | `#1A1A2E` | H1 text across most styles |
| Blue | `#2563EB` | H2 text (standard accent) |
| Dark gray | `#333333` | Normal body text |
| Medium gray | `#595959` | H3 text (subtle hierarchy) |
| Red | `#FF0000` | Dispatch H1 (红头文件) |

---

## standard (default)

General-purpose document with balanced spacing.

| Element | Font | Size | Color | Bold | Spacing |
|---------|------|------|-------|------|---------|
| Normal | YaHei | 11pt | default | No | after: 6pt, line: 1.5 |
| H1 | YaHei | 16pt | `#1A1A2E` | Yes | before: 18pt, after: 10pt |
| H2 | YaHei | 14pt | `#2563EB` | Yes | before: 12pt, after: 6pt |
| H3 | YaHei | 12pt | `#333333` | Yes | before: 10pt, after: 4pt |

## contract

Formal contracts with traditional Chinese fonts.

| Element | Font | Size | Color | Bold | Spacing |
|---------|------|------|-------|------|---------|
| Normal | FangSong | 12pt | `#333333` | No | after: 6pt, line: 1.5 |
| H1 | SimHei | 22pt | `#1A1A2E` | Yes | before: 24pt, after: 12pt |
| H2 | SimHei | 16pt | `#2563EB` | Yes | before: 18pt, after: 8pt |
| H3 | SimHei | 15pt | `#333333` | Yes | before: 12pt, after: 6pt |

## report

Business reports with compact blue-accented headers.

| Element | Font | Size | Color | Bold | Spacing |
|---------|------|------|-------|------|---------|
| Normal | YaHei | 10.5pt | `#333333` | No | after: 4pt, line: 1.25 |
| H1 | YaHei | 16pt | `#1A1A2E` | Yes | before: 18pt, after: 8pt |
| H2 | YaHei | 14pt | `#2563EB` | Yes | before: 12pt, after: 6pt |
| H3 | YaHei | 12pt | `#333333` | Yes | before: 8pt, after: 4pt |

## meeting

Compact meeting minutes with tight spacing.

| Element | Font | Size | Color | Bold | Spacing |
|---------|------|------|-------|------|---------|
| Normal | YaHei | 12pt | `#333333` | No | after: 4pt, line: 1.5 |
| H1 | YaHei | 16pt | `#1A1A2E` | Yes | before: 12pt, after: 8pt |
| H2 | YaHei | 14pt | `#2563EB` | Yes | before: 10pt, after: 4pt |
| H3 | YaHei | 12pt | `#333333` | Yes | before: 6pt, after: 2pt |

## business_letter

Traditional business letter format.

| Element | Font | Size | Color | Bold | Spacing |
|---------|------|------|-------|------|---------|
| Normal | YaHei | 12pt | `#333333` | No | after: 0pt, line: 1.5 |
| H1 | YaHei | 16pt | `#1A1A2E` | Yes | before: 12pt, after: 8pt |
| H2 | YaHei | 14pt | `#2563EB` | Yes | before: 8pt, after: 4pt |
| H3 | YaHei | 12pt | `#333333` | No | before: 6pt, after: 2pt |

## tech_spec

Technical documentation with monospace body text and dark theme.

| Element | Font | Size | Color | Bold | Spacing |
|---------|------|------|-------|------|---------|
| Normal | Consolas/YaHei | 10.5pt | `#333333` | No | after: 4pt, line: 1.5 |
| H1 | YaHei | 16pt | `#1A1A2E` | Yes | before: 24pt, after: 12pt |
| H2 | YaHei | 14pt | `#2563EB` | Yes | before: 18pt, after: 8pt |
| H3 | YaHei | 12pt | `#595959` | Yes | before: 12pt, after: 6pt |

## dispatch

红头文件 (official dispatch) with red H1 header.

| Element | Font | Size | Color | Bold | Spacing |
|---------|------|------|-------|------|---------|
| Normal | FangSong | 16pt | `#333333` | No | after: 0pt, line: 28pt |
| H1 | SimHei | 22pt | `#FF0000` | Yes | before: 12pt, after: 6pt |
| H2 | KaiTi | 16pt | `#333333` | Yes | before: 12pt, after: 6pt |
| H3 | FangSong | 16pt | `#333333` | No | before: 8pt, after: 4pt |

## notice

Official notices with large bold text.

| Element | Font | Size | Color | Bold | Spacing |
|---------|------|------|-------|------|---------|
| Normal | FangSong | 16pt | `#333333` | No | after: 0pt, line: 28pt |
| H1 | SimHei | 22pt | `#333333` | Yes | before: 12pt, after: 6pt |
| H2 | KaiTi | 16pt | `#333333` | Yes | before: 10pt, after: 4pt |
| H3 | FangSong | 16pt | `#333333` | No | before: 8pt, after: 4pt |
