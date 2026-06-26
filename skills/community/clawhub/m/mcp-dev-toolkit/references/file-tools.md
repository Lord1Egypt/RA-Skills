# File Management MCP Tool Patterns

## Read File

```typescript
server.tool("read_file", {
  path: z.string().describe("Absolute or relative file path")
}, async ({ path }) => {
  const content = await fs.readFile(path, "utf-8");
  return { content: [{ type: "text", text: content }] };
});
```

## Write File

```typescript
server.tool("write_file", {
  path: z.string(),
  content: z.string()
}, async ({ path, content }) => {
  await fs.writeFile(path, content, "utf-8");
  return { content: [{ type: "text", text: `Written ${content.length} bytes to ${path}` }] };
});
```

## Search Files (ripgrep)

```typescript
server.tool("search_files", {
  pattern: z.string().describe("Regex pattern"),
  path: z.string().default("."),
  file_type: z.string().optional()
}, async ({ pattern, path, file_type }) => {
  const args = ["--json", pattern, path];
  if (file_type) args.push("--type", file_type);
  const result = await execFile("rg", args);
  // Parse ripgrep JSON output
  const matches = result.stdout.trim().split("\n")
    .filter(Boolean)
    .map(line => JSON.parse(line))
    .filter(m => m.type === "match");
  return { content: [{ type: "text", text: JSON.stringify(matches, null, 2) }] };
});
```

## List Directory

```typescript
server.tool("list_dir", {
  path: z.string().default("."),
  recursive: z.boolean().default(false)
}, async ({ path, recursive }) => {
  const entries = recursive
    ? await glob("**/*", { cwd: path })
    : await fs.readdir(path);
  return { content: [{ type: "text", text: entries.join("\n") }] };
});
```
