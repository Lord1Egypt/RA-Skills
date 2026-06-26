# OpenCode Code Review 強化檢查清單

> 適用場景：OpenCode 對任何 PR/程式碼變更進行 code review 時使用。
> 目標：補足傳統 review 容易忽略的三類問題。

---

## 每次 Review 都必須問的問題

### 1. Schema 新增欄位 → 確認有對應實作讀取

**問題：「每個新增到 schema 的欄位，確認有對應的 TypeScript 程式碼讀取它」**

實作方式：
1. 列出所有新增的 schema 欄位（從 `openclaw.plugin.json` diff）
2. 對每個欄位搜尋 `index.ts` 中的 `cfg.<field>` 或 `cfg.<section>.<field>` 存取點
3. 如果找不到任何讀取 → 標記為「Dead schema」→ 必須修復或移除

**問法：**
```
請列出這次 PR 中 openclaw.plugin.json 的 schema 新增了哪些欄位，
並對每個欄位確認 index.ts 中是否有對應的 cfg 讀取。
如果某欄位只加在 schema 但從未被讀取，標記為「Dead schema」。
```

---

### 2. Pattern Matching 函式 → 邊界條件驗證

**問題：「每個 pattern 比對邏輯，提供具體測試案例，確認輸出結果」**

實作方式：
1. 找出 `isAgentOrSessionExcluded` 之類的 pattern matching 函式
2. 提供三個具體測試案例（正常、邊界、負向）
3. 要求 OpenCode 說出每個測試的輸出

**問法：**
```
針對 isAgentOrSessionExcluded 函式，請用以下測試案例說出輸出：
- "pi-" vs "pi-agent" → ?
- "pi-" vs "pizza" → ?
- "memory-distiller" vs "memory-distiller" → ?
- "pi-" vs "pi" → ?
```

---

### 3. 常數/函式定義 → 確認沒有被取代後遺留

**問題：「每個 const 或 function，確認沒有被其他方式取代後變成多餘」**

實作方式：
1. 搜尋所有 `const XXX =` 定義
2. 對每個定義，搜尋所有參照點
3. 如果定義只出現一次（只有自己）→ 可能是孤兒或被取代

**問法：**
```
請搜尋所有「定義但可能未使用」的 symbol：
1. `const SERIAL_GUARD_COOLDOWN_MS` 或其他 hardcoded 常數
2. 如果有某常數同時有 runtime config 覆寫，是否還需要保留？
3. 標記所有「只有一個參照點」的 symbol
```

---

### 4. 改動範圍確認 → 只涵蓋需要修改的範圍

**問題：「新 commit 的變更範圍是否只涵蓋需要修改的範圍」**

實作方式：
1. 對照 diff，確認沒有意外修改到無關程式碼
2. 格式變更（空行、縮排）應獨立出來
3. upstream/master 已經有的重構不應該出現在 PR diff

**問法：**
```
請對照 e3470dc vs HEAD 的 index.ts diff，
標記出任何與這次 PR 目的無關的變更。
例如：格式調整、 upstream 已有變更被重引入等。
```

---

### 5. Error Handling 完整性

**問題：「每個 early return / throw，是否有對應的 log」**

實作方式：
1. 找出所有 `return;` 和 `throw new Error()`
2. 檢查是否在 return/throw 前有 `api.logger.debug/info/warn/error`
3. 特別是 `runMemoryReflection` 之類的關鍵函式

---

### 6. 向後相容性

**問題：「新改動是否破壞現有設定」**

實作方式：
1. 新增可選欄位 → 預設值是否合理
2. 移除欄位 → 是否影响現有使用者
3. 變更預設值 → 現有使用者的行為是否改變

---

## 適用於記憶體插件（memory-lancedb-pro）的額外檢查

### PluginConfig vs Schema 一致性

每次在 `openclaw.plugin.json` 加欄位，必須確認：
1. PluginConfig TypeScript interface 有同樣的欄位
2. `parsePluginConfig` 有處理該欄位
3. **使用處**（hooks / functions）有讀取該欄位

### Three-Layer Guard 完整性

確認 `runMemoryReflection` 的三層 guard：
1. `isInternalReflectionSessionKey` guard 在正確位置
2. `globalLock` check 在正確位置
3. `serialGuard` check 在 `cfg` 解析之後

### 向後相容性

- `serialCooldownMs: undefined` → 應預設 120000
- `autoRecallExcludeAgents: []` → 應與未設定時行為一致
