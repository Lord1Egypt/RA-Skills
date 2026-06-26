# 云文档 API（Docx）

## 快速调用

# 搜索文档（需要 User Token）
python3 /workspace/skills/lark-skill/lark_mcp.py call docx_builtin_search '{"data":{"search_key":"关键词","count":5}}'

# 获取文档块列表
python3 /workspace/skills/lark-skill/lark_mcp.py call docx_v1_document_blocks '{"document_id":"文档token"}'

## 核心概念

每篇云文档 = 树形块结构
根节点 = Page 块（page_id = document_id）
文本/标题/表格/图片等 = 不同块类型

## API 分类

docx_v1_documents - 创建空白文档
docx_v1_document_blocks - 获取文档所有块（树形结构）
docx_v1_blocks_create - 在指定块下创建子块
docx_v1_blocks_update - 更新块内容
docx_v1_blocks_delete - 删除块
docx_builtin_import - 导入文件（docx/md/html → 云文档）
