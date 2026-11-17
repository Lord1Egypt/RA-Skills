# ZHC 语言服务（LSP）协议面

`scripts/zhc_lsp.py` 是 ZHC 的 LSP 服务端，走标准 stdio 传输（`Content-Length` 帧头 + JSON-RPC 2.0），
供 VS Code 扩展及其他支持 LSP 的编辑器接入。

## 一、启动

```bash
python -X utf8 scripts/zhc_lsp.py --stdio
```

服务端启动时必须先找到语言内核（`zhc.py`）：

1. 环境变量 `ZHC_HOME` 指定的目录；
2. 与 `zhc_lsp.py` 同级的目录；
3. 扩展安装目录下的 `zhc/`。

任一处找到可导入的 `zhc.py` 即完成加载；三处都找不到则发 `window/logMessage` 报错并退出。
因此**分发时必须把 `zhc.py` 与 `zhc_lsp.py` 放在同级**（本包 `scripts/` 就是这么放的）。

## 二、已实现的 LSP 能力

| 方法 | 方向 | 说明 |
|---|---|---|
| `initialize` | C→S | 返回 `textDocumentSync: 1`（全量同步）及补全/悬停/文档符号触发器 |
| `initialized` | C→S | 通知，服务端回 `window/logMessage` 声明就绪 |
| `textDocument/didOpen` | 通知 | 载入全文并立即发布诊断 |
| `textDocument/didChange` | 通知 | 全量替换文本后发布诊断 |
| `textDocument/didSave` | 通知 | 重新诊断（保存不动语义，仅为刷新） |
| `textDocument/didClose` | 通知 | 清空该 uri 的诊断 |
| `textDocument/publishDiagnostics` | S→C | **最核心**：编译器诊断直出 |
| `textDocument/completion` | C→S | 44 关键字 + 11 类型名 + 39 内置函数 |
| `textDocument/hover` | C→S | 内置函数签名与手册描述、关键字说明 |
| `textDocument/documentSymbol` | C→S | 函数与顶层定义大纲 |
| `shutdown` / `exit` | C→S | 正常收尾 |

未实现（客户端请求会静默忽略）：重命名、定义跳转、引用查找、代码格式化、语义高亮、代码片段。

## 三、诊断口径

服务端不另写检查器，直接复用内核的 `检查(src)`，因此：

- 诊断条数与 `python -X utf8 zhc.py <file> --诊断` **逐条一致**；
- 每条诊断的 `message` 是中文原文（如「参数名非法」「无法识别的语句起始 '结束'」）；
- `range` 由词法阶段记录的行列换算，行列从 0 起算（LSP 约定）；
- 诊断不做裁切，超出编辑器可见区域的仍照发。

对应的 `--诊断` 输出形态：

```json
{"ok": true}
```

或

```json
{"ok": false, "诊断": [{"行":3,"列":5,"码":"E014","信息":"参数名非法"}]}
```

**一致性门禁**：协议面已实测 1294 个样本，诊断语义与位置零漂移。改动诊断逻辑时，
必须同时跑 `--诊断` 与真 LSP 客户端双通道比对，任一不一致即视为回归。

## 四、客户端接入（非 VS Code）

```json
{
  "command": "python",
  "args": ["-X", "utf8", "/abs/path/scripts/zhc_lsp.py", "--stdio"],
  "filetypes": ["zc"]
}
```

Neovim（nvim-lspconfig 自定义）：

```lua
vim.lsp.start({
  name = 'zhc',
  cmd = { 'python', '-X', 'utf8', '/abs/path/scripts/zhc_lsp.py', '--stdio' },
  root_dir = vim.fn.getcwd(),
})
```

## 五、排障

| 现象 | 原因 | 处置 |
|---|---|---|
| 启动即退出，日志报找不到内核 | `zhc.py` 不在同级或 `ZHC_HOME` | 把两者放同目录，或设 `ZHC_HOME` |
| 无诊断但 `--诊断` 有错 | 编辑器未把 `.zc` 关联到本服务 | 检查 filetypes / languageId |
| 中文变问号 | Python 未以 UTF-8 模式启动 | 启动参数加 `-X utf8`，并设 `PYTHONIOENCODING=utf-8` |
| 补全只有关键字 | 内核未加载成功，退化为静态表 | 看 `window/logMessage` 的报错原文 |
