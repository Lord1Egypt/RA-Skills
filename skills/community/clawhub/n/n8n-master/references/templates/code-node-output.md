# Code Node Output

Use this shape when producing n8n Code node JavaScript.

````markdown
## 输入假设

- Mode:
- Incoming items:
- Required fields:

## Code node JavaScript

```javascript
const items = $input.all();

return items.map((item) => ({
  json: {
    ...item.json,
  },
}));
```

## 输出结构

```json
[
  {
    "json": {}
  }
]
```

## 注意事项

- Keep secrets in credentials or environment variables.
- Return valid n8n items.
- Preserve item pairing when downstream nodes rely on per-item mapping.
````

