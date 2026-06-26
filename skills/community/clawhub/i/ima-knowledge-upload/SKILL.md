---
name: ima-knowledge-upload
description: |
  上传Markdown文件到IMA知识库的标准流程。
  方法A（推荐）：笔记import_doc → add_knowledge（支持markdown，最简单）
  方法B：create_media → COS上传 → add_knowledge（支持任意文件）
  ⚠️ title必须等于file_name。
metadata:
  openclaw:
    emoji: 📤
    requires:
      env:
        - IMA_OPENAPI_CLIENTID
        - IMA_OPENAPI_APIKEY
---

# IMA知识库上传

上传Markdown报告到IMA知识库的标准方法。

## 方法A：笔记路径（推荐，用于Markdown文件）

```javascript
const api = require('C:\\Users\\shibi\\.openclaw\\skills\\ima-skill\\ima_api.cjs');

// Step 1: 创建笔记
const ir = JSON.parse(await api.imaApi('openapi/note/v1/import_doc', {
  title: '报告标题_2026-05-11',
  content: markdownContent,
  content_format: 1  // 1=MARKDOWN
}));
if (ir.code !== 0) throw new Error('import_doc failed: ' + ir.msg);
const noteId = ir.data.note_id;

// Step 2: 添加到知识库
const ar = JSON.parse(await api.imaApi('openapi/wiki/v1/add_knowledge', {
  knowledge_base_id: 'fh6uPoAPAxgoaknrmlrV18u3yl1tmtzDEfaeRX-EVtE=',
  media_type: 11,  // 11=笔记
  note_info: { content_id: noteId }
}));
if (ar.code !== 0) throw new Error('add_knowledge failed: ' + ar.msg);
```

## 方法B：文件路径（用于PDF/Word等非文本文件）

```javascript
const api = require('C:\\Users\\shibi\\.openclaw\\skills\\ima-skill\\ima_api.cjs');

// Step 1: preflight检查
// node skills/ima-skill/knowledge-base/scripts/preflight-check.cjs --file "path/to/file.pdf"

// Step 2: create_media
const cr = JSON.parse(await api.imaApi('openapi/wiki/v1/create_media', {
  knowledge_base_id: kbId,
  file_name: '报告.pdf',
  file_size: fs.statSync(filePath).size,
  media_type: 1  // 1=PDF 5=Excel 7=Markdown
}));

// Step 3: COS上传
// node skills/ima-skill/knowledge-base/scripts/cos-upload.cjs --file "file" --secret-id "..." --secret-key "..." --token "..." --bucket "..." --region "..." --cos-key "..." --content-type "application/pdf"

// Step 4: add_knowledge
const ar = JSON.parse(await api.imaApi('openapi/wiki/v1/add_knowledge', {
  media_type: 1,
  media_id: cr.data.media_id,
  title: '报告.pdf',
  knowledge_base_id: kbId
}));
```

## 关键规则

- **title必须等于file_name**（含扩展名）— 违反后文件显示为原名而非描述性标题
- **COS上传失败立即停止** — 不要继续add_knowledge
- **不要用错KB_ID** — 每个知识库ID不同

## 常用KB_ID

| 知识库 | KB_ID |
|--------|-------|
| 巴巴塔知识框架 | 3CQtyf9Ix1b_qSqNpcqJb0NOrb1KHvgXQuwV5HtObJk= |
| 医院智慧监督 | oXAIXrjt1QHiMF2p9HcuvFVsGz4-HcWSvNn9x-Vd9GM= |
| AI原生医院研究探索 | fh6uPoAPAxgoaknrmlrV18u3yl1tmtzDEfaeRX-EVtE= |
| 中山一院纪检监察 | GwoQS60RM0dtD0z-k1wZnPPIXcHv_T0bYeGC_KyS36k= |
