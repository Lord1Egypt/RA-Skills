# Workflow JSON Output

Use this shape when producing importable or copy-paste n8n workflow JSON.

```markdown
## 导入前说明

- JSON 不包含真实 secrets。
- Credentials 使用占位名称，导入后需要在 n8n UI 中重新绑定。
- 默认 `active: false`。
- 写入型节点建议先手动执行或 dry-run。

## Workflow JSON

```json
{
  "name": "Workflow name",
  "nodes": [],
  "connections": {},
  "settings": {},
  "active": false
}
```

## 验证清单

- [ ] Trigger 正确
- [ ] Credentials 已绑定
- [ ] 样例输入测试通过
- [ ] 写入节点已 dry-run
- [ ] 失败路径可见
```

