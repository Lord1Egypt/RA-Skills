# 文档翻译

POST https://ai-skills.open-idea.net/api/v1/mongolian-ai/word/translation
POST https://ai-skills.open-idea.net/api/v1/mongolian-ai/pdf/translation

multipart/form-data：恰好一个 file，Word 仅 DOCX，PDF 仅 PDF，最大 5 MB。from/to 必填，仅 zh、mw、mn 且不同。mode 可选，默认 all_text；允许 all_text（全部文字）或 mongolian_only（仅蒙古文）。不支持 DOC、文档 URL 或客户端传入正文替代文件。

PDF 默认 include_layout_ocr=true，按阅读顺序提取文字层与图片块并对图片 OCR。可选 layout_max_pages（1–200，默认30）、layout_max_image_ocr（1–60，默认20）、layout_dpi（72–200，默认110）、ocr_language（mw/mn/zh，默认mw）。关闭 include_layout_ocr 后仅处理文字层。扫描件开启版式 OCR 后可提取识别文字；图片 OCR 与翻译按实际字符合并为一次结算。未知上游结果保留余额预留用于对账，不能通过新幂等键强制重新执行。

成功只提取 data.text（译文文字），不是文件下载链接；不承诺保留原始排版或生成可下载 DOCX/PDF。失败时不得伪造译文。保存首次返回的译文，重放不包含正文。
