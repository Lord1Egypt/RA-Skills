## LSP 語言伺服器整合

### 內建支援的 LSP 伺服器

| LSP | 副檔名 | 需求 |
|-----|--------|------|
| astro | .astro | 自動安裝 |
| bash | .sh/.bash/.zsh | 自動安裝 |
| clangd | .c/.cpp/.h | 自動安裝 |
| csharp | .cs | .NET SDK |
| dart | .dart | dart 指令 |
| deno | .ts/.tsx/.js | deno 指令 |
| eslint | .ts/.tsx/.js | 專案需 eslint |
| gleam | .gleam | gleam 指令 |
| gopls | .go | go 指令 |
| haskell | .hs | haskell-language-server |
| jdtls | .java | Java SDK 21+ |
| kotlin | .kt/.kts | 自動安裝 |
| lua | .lua | 自動安裝 |
| ocaml | .ml/.mli | ocamllsp |
| oxlint | .vue/.svelte | 專案需 oxlint |
| php | .php | 自動安裝 |
| prisma | .prisma | prisma 指令 |
| pyright | .py/.pyi | 專案需 pyright |
| ruby | .rb | ruby + rubocop |
| rust | .rs | rust-analyzer |
| sourcekit | .swift | macOS/Xcode |
| svelte | .svelte | 自動安裝 |
| terraform | .tf/.tfvars | 自動安裝 |
| tinymist | .typ | 自動安裝 |
| typescript | .ts/.tsx | 專案需 typescript |
| vue | .vue | 自動安裝 |
| yaml | .yaml/.yml | 自動安裝 |
| zls | .zig | zig 指令 |

### LSP 工具支援的操作

- `goToDefinition` — 跳轉定義
- `findReferences` — 查找參考
- `hover` — 懸停資訊
- `documentSymbol` — 文件符號
- `workspaceSymbol` — 工作區符號
- `goToImplementation` — 跳轉實作
- `prepareCallHierarchy` — 呼叫階層
- `incomingCalls` / `outgoingCalls` — 呼叫來往

### LSP 設定

停用特定 LSP：
```json
{
  "lsp": {
    "typescript": {
      "disabled": true
    }
  }
}
```

全域停用：
```json
{ "lsp": false }
```

環境變數：
```json
{
  "lsp": {
    "rust": {
      "env": { "RUST_LOG": "debug" }
    }
  }
}
```

初始化選項：
```json
{
  "lsp": {
    "typescript": {
      "initialization": {
        "preferences": {
          "importModuleSpecifierPreference": "relative"
        }
      }
    }
  }
}
```

### PHP Intelephense 授權

建立 `$HOME/intelephense/license.txt`，內容僅含授權金鑰。
