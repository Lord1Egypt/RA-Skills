# NEXUS.md — 記憶網路樞紐

> Connect everything, create value.

## 架構概覽

```
         MEMORY.md（長期）
              ↑
daily log → NEXUS Hub → lessons learned
              ↓
         ideas / insights
```

所有記憶節點透過 Nexus Hub 連接，形成網絡而非孤島。

---

## 四層記憶架構

| 層級 | 名稱 | 存放位置 | 保留時間 |
|------|------|---------|---------|
| L1 | Working Memory | session 上下文 | session 結束即清除 |
| L2 | Short-term | `memory/YYYY-MM-DD.md` | 7 天 |
| L3 | Long-term | `MEMORY.md` | 永久 |
| L4 | Compressed | `memory/archive/` | 封存，按需取回 |

**沉澱規則：**
- L2 → L3：重要決策、教訓、Jazz 的偏好
- L3 → L4：超過 3 個月未參考的舊脈絡

---

## 知識節點連接

每個記憶節點可附帶連接權重：
- **強連接（1.0）**：直接相關，每次一起讀取
- **中連接（0.6）**：相關任務，按需讀取
- **弱連接（0.3）**：背景脈絡，僅在深度分析時用

範例：
```
MEMORY.md#代理架構 --1.0--> MEMORY.md#省錢策略
MEMORY.md#代理架構 --0.6--> memory/2026-03-24.md#模型切換
```

---

## Nexus 每日維護

session 結束或 heartbeat 時執行：

1. **L2 整理**：`memory/YYYY-MM-DD.md` 有無值得沉澱到 L3
2. **L3 更新**：把今天的重要決策寫進 `MEMORY.md`
3. **節點清理**：超過 7 天的 L2 日誌標記為候選封存
4. **Ideas 記錄**：把本次 session 產生的新想法寫到 `memory/ideas.md`

---

## Ideas Journal

路徑：`memory/ideas.md`

格式：
```
## YYYY-MM-DD
- [想法標題]：[一句話描述] #tag
```

Nexus 鼓勵主動記錄靈光一現的想法，下次 session 可以主動提給 Jazz。

---

## 查詢協議

需要找舊資料時，依序：
1. 先看 L1（當前 session 上下文）
2. 查 L3（`MEMORY.md`）
3. 查 L2（最近幾天的 daily log）
4. 按需讀 L4（archive）

不要每次都讀所有檔案，按需取用。
