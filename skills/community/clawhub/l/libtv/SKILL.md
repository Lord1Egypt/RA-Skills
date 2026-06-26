# libtv-qunqin

## 描述
使用 libtv 后端把《寻秦记》改造成漫画（web‑toon）形式。  
接受 JSON payload，返回每一页的 PNG 图片路径及文字说明。

## Entry Point
`libtv_qunqin.py`

## 参数
- `story_file` (string) – 书籍或章节文本文件路径（UTF‑8）。
- `panel_count` (int, optional) – 每章生成的漫画格数（默认 6）。
- `font` (string, optional) – 文字字体（默认 “Noto Serif SC”）。
- `output_dir` (string, optional) – 输出目录（默认 `./output/寻秦记`）。

## 运行示例
```json
{
  "story_file": "novel/寻秦记.txt",
  "panel_count": 8,
  "font": "Noto Serif SC",
  "output_dir": "output/寻秦记"
}