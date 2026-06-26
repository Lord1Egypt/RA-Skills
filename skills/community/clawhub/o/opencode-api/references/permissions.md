## Permissions 權限系統

### 三種權限行為

| 權限 | 行為 |
|------|------|
| `allow` | 無需審批直接執行 |
| `ask` | 提示審批（once/always/reject）|
| `deny` | 阻止該操作 |

### 全域與細粒度設定

```json
{
  "permission": {
    "*": "ask",
    "bash": "allow",
    "edit": "deny"
  }
}
```

### 細粒度物件語法

```json
{
  "permission": {
    "bash": {
      "*": "ask",
      "git *": "allow",
      "npm *": "allow",
      "rm *": "deny",
      "grep *": "allow"
    },
    "edit": {
      "*": "deny",
      "packages/web/src/content/docs/*.mdx": "allow"
    }
  }
}
```

### 可用權限鍵

| 權限鍵 | 比對方式 |
|--------|----------|
| `read` | 檔案路徑 |
| `edit` | 檔案路徑（涵蓋 edit/write/patch/multiedit）|
| `glob` | 萬用字元模式 |
| `grep` | 正規表示式模式 |
| `list` | 目錄路徑 |
| `bash` | 解析後的指令 |
| `task` | 子代理類型 |
| `skill` | 技能名稱 |
| `lsp` | 不支援細粒度 |
| `webfetch` | URL |
| `websearch` / `codesearch` | 查詢內容 |
| `external_directory` | 外部路徑 |
| `doom_loop` | 相同工具呼叫重複 3 次 |

### 萬用字元語法

- `*` — 零或多個任意字元
- `?` — 精確比對一個字元

### 主目錄展開

```json
{
  "permission": {
    "external_directory": {
      "~/projects/personal/**": "allow"
    }
  }
}
```

### 預設值（重要！）

- 大多數權限預設為 `allow`
- `doom_loop` 和 `external_directory` 預設為 `ask`
- `.env` 檔案預設被拒絕讀取

```json
{
  "permission": {
    "read": {
      "*": "allow",
      "*.env": "deny",
      "*.env.*": "deny",
      "*.env.example": "allow"
    }
  }
}
```

### ask 的三種回覆

| 回覆 | 效果 |
|------|------|
| `once` | 僅批准本次請求 |
| `always` | 批准與模式匹配的後續請求（session 內有效）|
| `reject` | 拒絕請求 |

### 按代理覆寫權限

```json
{
  "permission": {
    "bash": {
      "*": "ask",
      "git *": "allow",
      "git commit *": "ask",
      "git push *": "deny"
    }
  },
  "agent": {
    "build": {
      "permission": {
        "bash": {
          "*": "ask",
          "git *": "allow",
          "git push *": "deny"
        }
      }
    }
  }
}
```

Markdown 代理設定：
```markdown
---
permission:
  edit: deny
  bash: ask
  webfetch: deny
---
```
