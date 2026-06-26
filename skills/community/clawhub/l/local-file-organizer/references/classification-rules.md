# 文件分类规则库

## 默认分类规则

| 类型 | 扩展名 | 目标目录 |
|------|--------|----------|
| 文档 | pdf, doc, docx, xls, xlsx, ppt, pptx, txt, md, pages, numbers, key | Documents/ |
| 图片 | jpg, jpeg, png, gif, webp, bmp, tiff, raw, heic, svg | Pictures/ |
| 视频 | mp4, mov, avi, mkv, wmv, flv, m4v | Videos/ |
| 音频 | mp3, wav, flac, aac, ogg, m4a, opus | Audio/ |
| 压缩包 | zip, rar, 7z, tar, gz, bz2, xz | Archives/ |
| 代码 | py, js, ts, sh, java, go, rs, cpp, c, h, css, html, json, yaml, yml | Code/ |
| 临时文件 | tmp, temp, cache, log, bak | Temp/ |

## 按项目分类（文件名匹配）

文件名包含项目关键词时，优先归入对应项目目录：
- 规则格式：`{"keyword": "ProjectA", "target": "Projects/ProjectA"}`
- 支持正则表达式匹配

## 按时间分类（照片/视频）

读取 EXIF 拍摄时间或文件修改时间，按年份/月份归档：
- `Photos/2026/01/` 格式
- 需要 exiftool 支持精确 EXIF 读取
