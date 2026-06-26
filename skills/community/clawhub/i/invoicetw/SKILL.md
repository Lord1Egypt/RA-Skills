---
name: InvoiceTW
description: "台灣統一發票查詢與管理工具 - 支持發票核對、記錄、統計與中獎追蹤"
homepage: https://clawhub.ai/skills/InvoiceTW
metadata:
  {
    "openclaw":
      {
        "emoji": "🧾",
        "requires": { "bins": ["node"] },
        "install":
          [
            {
              "id": "node",
              "kind": "node",
              "package": "InvoiceTW",
              "bins": ["Invoice"],
              "label": "Install InvoiceTW (Node.js)",
            },
          ],
      },
  }
---

# Skill: InvoiceTW 台灣統一發票查詢

## 概述
台灣統一發票的查詢、記錄與中獎統計功能。使用 `Invoice` 指令來核對統一發票是否中獎，以及管理發票明細。

## 使用時機
- 查詢統一發票是否中獎
- 記錄日常發票明細（如公司報帳、個人開支）
- 生成中獎統計報表
- 管理發票存根

## 核心指令

### 1. 核對中獎 (`Invoice check`)
```
Invoice check 12345678
Invoice check 12345678,87654321
```
- 輸入統一發票 8 位號碼（可單個或逗號分隔多個）
- 自動查詢中獎狀態
- 顯示中獎獎項與金額

### 2. 新增發票記錄 (`Invoice add`)
```
Invoice add 12345678 7/15 全家 50 元 民生用品
Invoice add --memo "聚餐" 12345678 7/15 7-11 320 元 餐飲
```
- `12345678`: 發票號碼
- `7/15`: 開獎日期
- `全家`: 發票來源
- `50`: 金額
- `民生用品`: 分類標籤

### 3. 查詢發票 (`Invoice list`)
```
Invoice list                    # 顯示所有發票
Invoice list --category 餐飲    # 按分類篩選
Invoice list --month 7          # 按月份篩選
```

### 4. 中獎統計 (`Invoice stats`)
```
Invoice stats                   # 總統計
Invoice stats --category        # 按分類統計
Invoice stats --summary         # 簡易摘要
```

### 5. 中獎明細 (`Invoice prizes`)
```
Invoice prizes                  # 顯示所有中獎發票
Invoice prizes --pending        # 顯示未兌領的中獎發票
```

## 儲存方式
- 發票明細：`~/openclaw_workspace/InvoiceTW/receipts.json`
- 中獎記錄：`~/openclaw_workspace/InvoiceTW/wins.json`
- 報表：`~/openclaw_workspace/InvoiceTW/reports/`

## 中獎獎項（台灣統一發票）
- 特獎：新台幣 200 萬元（2 名）
- 一獎：新台幣 10 萬元（10 名）
- 二獎：新台幣 2 萬元（20 名）
- 三獎：新台幣 1 萬元（40 名）
- 四獎：新台幣 4,000 元（80 名）
- 五獎：新台幣 2,000 元（240 名）
- 六獎：新台幣 400 元（800 名）
- 特別獎：新台幣 200 元（若干名）
- 摸彩資格：尾碼中獎可參加摸彩

## 例句範例

### 查詢發票
- 「幫我看看 12345678 有沒有中獎」
- 「核對這支發票：87654321」
- 「檢查 12345678,23456789,34567890 的中獎狀況」

### 新增發票
- 「新增發票 12345678，7/15 開獎，全家，50 元，民生用品」
- 「記一筆發票：87654321, 7/15, 7-11, 320 元，餐飲」
- 「新增發票 12345678, 23456789 兩張，都是今天全家買的」

### 查詢記錄
- 「列出我所有的發票」
- 「我 7 月的發票明細」
- 「顯示餐飲類的發票」

### 中獎查詢
- 「我有哪些中獎發票？」
- 「哪些發票還沒兌領？」
- 「顯示所有中獎明細」

### 統計報表
- 「統計一下我的中獎情形」
- 「我的發票按分類統計」
- 「給我一個中獎摘要」

## 注意事項
- 統一發票號碼為 8 位數字
- 發票每兩個月開獎一次（7 月 1 日、1 月 1 日）
- 中獎後可於超商、郵局或財政部指定地點兌領
- 建議保留發票存根至少一年
- 摸彩資格需同時符合尾碼中獎條件
