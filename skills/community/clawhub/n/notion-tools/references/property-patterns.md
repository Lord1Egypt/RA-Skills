# Property Patterns

Use these shapes only after confirming the property exists in the target schema:

- Title: `{"title":[{"text":{"content":"..."}}]}`
- Rich text: `{"rich_text":[{"text":{"content":"..."}}]}`
- Select: `{"select":{"name":"Option"}}`
- Multi-select: `{"multi_select":[{"name":"A"},{"name":"B"}]}`
- Date: `{"date":{"start":"2024-01-15","end":"2024-01-16"}}`
- Checkbox: `{"checkbox":true}`
- Number: `{"number":42}`
- URL: `{"url":"https://..."}`
- Email: `{"email":"a@b.com"}`
- Relation: `{"relation":[{"id":"page_id"}]}`
