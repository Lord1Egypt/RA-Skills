# mock-data 模板

将本目录**整份**复制到用户项目下的 `./mock-data`（与 [`SKILL.md`](../../SKILL.md) 中本地调试流程一致），然后：

```bash
# 在 skill 根目录
node scripts/mock-jsonv2.mjs --port 3847 --dir /path/to/your/mock-data
```

浏览器打开示例页时设置 `CONFIG.apiBase = 'http://127.0.0.1:3847'`（参见 `examples/vanilla/list-page-with-apibase.html`）。

也可以用 `scripts/fetch-form-spec.mjs` 从真实环境拉取 fielddef 覆盖子目录中的 `fielddef.json`。
