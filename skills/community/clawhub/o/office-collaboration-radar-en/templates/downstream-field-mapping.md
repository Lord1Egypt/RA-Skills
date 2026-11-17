# Downstream Field Mapping

| Card field | Feishu/Bitable | Notion |
| --- | --- | --- |
| `action_items[].task` | Task name | Title |
| `action_items[].owner` | Owner | Person/Text |
| `action_items[].ddl` | Deadline | Date |
| `risks_dependencies[].type` | Risk type | Select |
| `needs_human_confirmation[].item` | Review item | Text |

This skill only produces the mapping. A user or authorized connector performs any external write.
