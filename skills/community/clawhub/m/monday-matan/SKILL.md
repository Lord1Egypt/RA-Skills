SKILL.md
Monday.com (via Maton Gateway)

Access the Monday.com API with managed OAuth authentication. Manage boards, items, columns, groups, users, and workspaces using GraphQL.

🚀 Quick Start
Get Current User
curl -X POST https://gateway.maton.ai/monday/v2 \
  -H "Authorization: Bearer $MATON_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "{ me { id name email } }"}' | jq

🌐 Base URL
https://gateway.maton.ai/monday/v2


All requests use POST to the GraphQL endpoint.

🔐 Authentication
-H "Authorization: Bearer $MATON_API_KEY"

Set API Key
export MATON_API_KEY="YOUR_API_KEY"

🔑 Getting Your API Key
Sign in at https://maton.ai
Go to /settings
Copy your API key
🔗 Connection Management

Manage OAuth connections:

https://ctrl.maton.ai

📄 List Connections
curl "https://ctrl.maton.ai/connections?app=monday&status=ACTIVE" \
  -H "Authorization: Bearer $MATON_API_KEY" | jq

➕ Create Connection
curl -X POST https://ctrl.maton.ai/connections \
  -H "Authorization: Bearer $MATON_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"app": "monday"}' | jq

🔍 Get Connection
curl https://ctrl.maton.ai/connections/{connection_id} \
  -H "Authorization: Bearer $MATON_API_KEY" | jq

❌ Delete Connection
curl -X DELETE https://ctrl.maton.ai/connections/{connection_id} \
  -H "Authorization: Bearer $MATON_API_KEY" | jq

🌐 Complete OAuth

Open the returned url in your browser.

🎯 Specify Connection
curl -X POST https://gateway.maton.ai/monday/v2 \
  -H "Authorization: Bearer $MATON_API_KEY" \
  -H "Content-Type: application/json" \
  -H "Maton-Connection: CONNECTION_ID" \
  -d '{"query": "{ me { id name } }"}' | jq

📚 API Reference
👤 Current User
curl -X POST https://gateway.maton.ai/monday/v2 \
  -H "Authorization: Bearer $MATON_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "{ me { id name email } }"}'

👥 Users
curl -X POST https://gateway.maton.ai/monday/v2 \
  -H "Authorization: Bearer $MATON_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "{ users(limit: 20) { id name email } }"}'

🏢 Workspaces
curl -X POST https://gateway.maton.ai/monday/v2 \
  -H "Authorization: Bearer $MATON_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "{ workspaces(limit: 10) { id name kind } }"}'

📋 Boards
List Boards
curl -X POST https://gateway.maton.ai/monday/v2 \
  -H "Authorization: Bearer $MATON_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "{ boards(limit: 10) { id name state board_kind workspace { id name } } }"}'

Get Board (Full)
curl -X POST https://gateway.maton.ai/monday/v2 \
  -H "Authorization: Bearer $MATON_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "{ boards(ids: [BOARD_ID]) { id name columns { id title type } groups { id title } items_page(limit: 20) { cursor items { id name state } } } }"}'

Create Board
curl -X POST https://gateway.maton.ai/monday/v2 \
  -H "Authorization: Bearer $MATON_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "mutation { create_board(board_name: \"New Board\", board_kind: public) { id name } }"}'

Update Board
curl -X POST https://gateway.maton.ai/monday/v2 \
  -H "Authorization: Bearer $MATON_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "mutation { update_board(board_id: BOARD_ID, board_attribute: description, new_value: \"Board description\") }"}'

Delete Board
curl -X POST https://gateway.maton.ai/monday/v2 \
  -H "Authorization: Bearer $MATON_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "mutation { delete_board(board_id: BOARD_ID) { id } }"}'

🧩 Items
Get Items
curl -X POST https://gateway.maton.ai/monday/v2 \
  -H "Authorization: Bearer $MATON_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "{ items(ids: [ITEM_ID]) { id name state } }"}'

Create Item
curl -X POST https://gateway.maton.ai/monday/v2 \
  -H "Authorization: Bearer $MATON_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "mutation { create_item(board_id: BOARD_ID, group_id: \"GROUP_ID\", item_name: \"New item\") { id name } }"}'

Create Item with Column Values
curl -X POST https://gateway.maton.ai/monday/v2 \
  -H "Authorization: Bearer $MATON_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "mutation { create_item(board_id: BOARD_ID, group_id: \"GROUP_ID\", item_name: \"New task\", column_values: \"{\\\"status\\\": {\\\"label\\\": \\\"Working on it\\\"}}\") { id name } }"}'

Update Item Name
curl -X POST https://gateway.maton.ai/monday/v2 \
  -H "Authorization: Bearer $MATON_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "mutation { change_simple_column_value(board_id: BOARD_ID, item_id: ITEM_ID, column_id: \"name\", value: \"Updated name\") { id name } }"}'

Update Column Value
curl -X POST https://gateway.maton.ai/monday/v2 \
  -H "Authorization: Bearer $MATON_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "mutation { change_column_value(board_id: BOARD_ID, item_id: ITEM_ID, column_id: \"status\", value: \"{\\\"label\\\": \\\"Done\\\"}\") { id name } }"}'

Delete Item
curl -X POST https://gateway.maton.ai/monday/v2 \
  -H "Authorization: Bearer $MATON_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "mutation { delete_item(item_id: ITEM_ID) { id } }"}'

📊 Columns
Create Column
curl -X POST https://gateway.maton.ai/monday/v2 \
  -H "Authorization: Bearer $MATON_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "mutation { create_column(board_id: BOARD_ID, title: \"Status\", column_type: status) { id title type } }"}'

🗂 Groups
Create Group
curl -X POST https://gateway.maton.ai/monday/v2 \
  -H "Authorization: Bearer $MATON_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "mutation { create_group(board_id: BOARD_ID, group_name: \"New Group\") { id title } }"}'

📄 Pagination
First Page
curl -X POST https://gateway.maton.ai/monday/v2 \
  -H "Authorization: Bearer $MATON_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "{ boards(ids: [BOARD_ID]) { items_page(limit: 50) { cursor items { id name } } } }"}'

Next Page
curl -X POST https://gateway.maton.ai/monday/v2 \
  -H "Authorization: Bearer $MATON_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "{ next_items_page(cursor: \"CURSOR_VALUE\", limit: 50) { cursor items { id name } } }"}'

⚠️ Notes
GraphQL only (no REST)
IDs are strings
Escape JSON inside GraphQL mutations carefully
Default limit: 25 (max: 100)
🛠 Troubleshooting
Check API Key
echo $MATON_API_KEY

Test Auth
curl https://ctrl.maton.ai/connections \
  -H "Authorization: Bearer $MATON_API_KEY" | jq

❌ Errors
Code	Meaning
400	GraphQL / connection error
401	Invalid API key
403	Missing OAuth scope
429	Rate limited