# 画板 API（Board）

## 快速调用

# 下载画板为图片（返回二进制流）
python3 /workspace/skills/lark-skill/lark_mcp.py call board/v1/whiteboards/{whiteboard_id}/download_as_image '{}'

# 解析 PlantUML
python3 /workspace/skills/lark-skill/lark_mcp.py call board/v1/whiteboards/{whiteboard_id}/nodes/plantuml '{"plant_uml_code":"@startuml\nAlice -> Bob\n@enduml","syntax_type":1}'

## 定位画板

独立画板：直接用 whiteboard_id
文档中的画板：通过 docx_v1_document_blocks，block_type = 43 对应 block.token = whiteboard_id

## 支持格式

下载画板返回：image/png / image/jpeg / image/gif / image/svg+xml

## 语法解析

plant_uml_code - PlantUML 或 Mermaid 代码
syntax_type - 1=PlantUML；2=Mermaid
style_type - 1=画板样式（多节点，不可二次编辑）；2=经典样式（单图片，可二次编辑）

## 频率限制

下载画板为图片：50次/秒
解析 PlantUML/Mermaid：5次/秒
