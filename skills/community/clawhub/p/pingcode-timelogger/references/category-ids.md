# PingCode Work Category IDs

Standard work category IDs used in PingCode workload registration.

These IDs may vary between PingCode instances. The values below are defaults; if they don't work, discover them via the PingCode UI:
1. Open any work item → Log Hours → click the "工作类别" dropdown
2. Use browser DevTools (Network tab) to capture the actual IDs

## Default Category Mapping

| Category | Chinese | ID |
|----------|---------|-----|
| Design | 设计 | `5cb7e7fffda1ce4ca0050001` |
| Development | 研发 | `5cb7e7fffda1ce4ca0050002` |
| Deployment | 部署 | `5cb7e7fffda1ce4ca0050003` |
| Testing | 测试 | `5cb7e7fffda1ce4ca0050004` |
| Documentation | 文档 | `5cb7e7fffda1ce4ca0050005` |
| Product | 产品 | `5cb7e7fffda1ce4ca0050006` |
| Research | 调研 | `5cb7e7fffda1ce4ca0050007` |
| Other | 其他 | `5cb7e7fffda1ce4ca0050008` |

## Auto-Discovery

If the default IDs don't work, the skill should discover them by:
1. Opening a work item's time logging UI in the browser
2. Inspecting the dropdown options
3. Saving discovered IDs back to the user's config
