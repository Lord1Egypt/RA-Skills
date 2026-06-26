# OpenCode Formatters、Share、Keybinds 綜合參考

> 本檔案收錄 OpenCode 的格式化器設定、分享功能與快捷鍵速查，供快速參考使用。

---

## Formatters 格式化器

### 內建格式化器速查

| 格式化器 | 副檔名 | 需求 |
|----------|--------|------|
| ruff | .py, .pyi | ruff 指令 |
| biome | .js/.ts/.jsx/.tsx/.html/.css/.json/.yaml | biome.json 設定檔 |
| prettier | 同上 | package.json 有 prettier |
| rustfmt | .rs | rustfmt 可用 |
| gofmt | .go | gofmt 可用 |
| clang-format | .c/.cpp/.h | .clang-format 設定檔 |
| shfmt | .sh/.bash | shfmt 可用 |
| rubocop | .rb | rubocop 可用 |
| mix | .ex/.exs/.eex | mix 指令可用 |
| pint | .php | laravel/pint |
| cargo | .rs | cargo fmt |
| sqlformat | .sql | sqlformat 指令 |

### 設定格式

```json
{
  "formatter": {
    "ruff": {
      "command": [".venv/Scripts/ruff", "format", "$FILE"],
      "extensions": [".py", ".pyi"]
    },
    "prettier": {
      "disabled": true
    }
  }
}
```

全域停用：
```json
{ "formatter": false }
```

---

## Share 分享功能

### 三種分享模式

| 模式 | 說明 |
|------|------|
| `manual` | 手動分享（預設）|
| `auto` | 新對話自動分享 |
| `disabled` | 完全停用 |

### 使用方式

```bash
/share      # 手動分享
/unshare    # 取消分享
```

```json
{ "share": "auto" }
```

分享連結格式：`opncd.ai/s/<id>`

### 隱私注意事項

- 共享對話在取消分享前持續可存取
- 建議避免分享含專有程式碼或機密資料的對話
- 協作完成後立即取消分享

---

## Keybinds 快捷鍵

### 常用快捷鍵速查

| 按鍵 | 動作 |
|------|------|
| `Tab` | 切換內建代理 |
| `Ctrl+X, a` | 開啟代理列表 |
| `Ctrl+X, s` | 開啟狀態視圖 |
| `Ctrl+X, c` | 壓縮當前 session |
| `Ctrl+X, e` | 開啟編輯器 |
| `Ctrl+X, t` | 切換主題 |
| `Ctrl+X, b` | 切換側邊欄 |
| `Ctrl+X, x` | 匯出 session |
| `Ctrl+X, l` | 開啟 session 列表 |
| `Ctrl+X, g` | 開啟 session 時間軸 |
| `Ctrl+P` | 開啟指令列表 |
| `Ctrl+X, n` | 新建 session |
| `Escape` | 中斷當前 session |
| `F2` | 切換到下一個最近使用的模型 |
| `Shift+F2` | 切換到上一個最近使用的模型 |
| `Ctrl+T` | 切換模型變體 |

### 輸入框導航

| 按鍵 | 動作 |
|------|------|
| `Ctrl+A` / `Ctrl+E` | 行首/行尾 |
| `Alt+F` / `Alt+B` | 往前/往後跳躍單字 |
| `Ctrl+W` | 刪除前一個單字 |
| `Ctrl+K` | 刪除到行尾 |
| `Ctrl+U` | 刪除到行首 |
