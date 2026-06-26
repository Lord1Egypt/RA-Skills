# 电子表格 API（Shees）

## 核心概念

表格（spreadsheet_token）→ 工作表（sheet_id）→ 范围（range = sheetId!A1:B5）

range 格式：工作表ID!开始单元格:结束单元格
例：0bdf12!A1:B5 = 工作表0bdf12第1行A列到B列

## 快速调用

# 读取单元格
python3 /workspace/skills/lark-skill/lark_mcp.py call sheets_v2_spreadsheets_values_get '{"spreadsheetToken":"表token","range":"工作表ID!A1:B5"}'

# 写入单元格
python3 /workspace/skills/lark-skill/lark_mcp.py call sheets_v2_spreadsheets_values_put '{"spreadsheetToken":"表token","range":"工作表ID!A1","values":"[[\"值1\",\"值2\"]]}'

## 使用限制

单表格中工作表数：≤ 300 / 单工作表列数：≤ 13,000
单工作表单元格数：≤ 5,000,000 / 单单元格字符数：≤ 50,000

单文档内大多数写入操作只能串行，不能并发
