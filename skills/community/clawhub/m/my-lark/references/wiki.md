# 知识库 API（Wiki）

## 快速调用

# 搜索知识库（需要 User Token）
python3 /workspace/skills/lark-skill/lark_mcp.py call wiki_v1_node_search '{"query":"关键词","count":5}'

# 获取节点详情（含 obj_token，用于读写文档内容）
python3 /workspace/skills/lark-skill/lark_mcp.py call wiki_v2_space_getNode '{"space_id":"7241909889038073859","node_token":"节点token"}'

## obj_type 类型对照

1=Doc 3=Bitable 4=Mindnote 5=File 8=Docx（新版） 9=Folder 10=Catalog 11=Slides

## API 分类

wiki_v1_node_search - 搜索知识库节点（⚠️ User Token）
wiki_v2_spaces - 获取知识库空间列表
wiki_v2_space_getNode - 获取节点详情（含 obj_token）
wiki_v2_nodes_create - 创建知识库节点
wiki_v2_nodes_delete - 删除节点
wiki_v2_nodes_move - 移动节点
