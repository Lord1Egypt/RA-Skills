# InvoiceTW - 台灣統一發票查詢 Skill

## 📦 基本資訊

- **ClawHub 名稱**: `InvoiceTW`
- **版本**: `1.0.0`
- **類型**: 台灣統一發票查詢與管理工具
- **主指令**: `Invoice`

## 🎯 功能特色

✅ **發票核對** - 支援單個或多個發票號碼查詢中獎狀態  
✅ **發票記錄** - 記錄發票明細（門市、金額、分類、備註）  
✅ **查詢功能** - 按分類或月份篩選發票  
✅ **統計報表** - 統計中獎情況與發票分類  
✅ **中獎追蹤** - 追蹤所有中獎發票與兌領狀態  

## 📋 使用方式

### 核對發票
```bash
Invoice check 12345678
Invoice check 12345678,23456789,34567890
```

### 新增發票記錄
```bash
Invoice add 12345678 7/15 全家 50 元 民生用品
Invoice add 87654321 7/15 7-11 320 元 餐飲
```

### 查詢發票
```bash
Invoice list
Invoice list --category 餐飲
Invoice list --month 7
```

### 統計報表
```bash
Invoice stats
Invoice stats --category
```

### 中獎明細
```bash
Invoice prizes
Invoice prizes --pending
```

## 📁 檔案結構

```
InvoiceTW/
├── Invoice           # 主指令包裝器
├── InvoiceTW.js      # 核心功能腳本
├── SKILL.md          # 詳細說明文件
├── package.json      # NPM 套件配置
├── InvoiceTW/        # 儲存目錄（運行時自動建立）
│   ├── receipts.json # 發票明細記錄
│   ├── wins.json     # 中獎記錄
│   └── reports/      # 報表目錄
└── README.md         # 本檔案
```

## 🚀 安裝方式

### 方法 1: 使用 ClawHub
```bash
clawhub install InvoiceTW
```

### 方法 2: 解壓 ZIP 檔
```bash
unzip /tmp/InvoiceTW.zip -d /path/to/openclaw/workspace/skills/
```

### 方法 3: 複製目錄
```bash
cp -r /home/ckk/.openclaw/workspace/skills/InvoiceTW \
      /path/to/openclaw/workspace/skills/
```

## 🔗 分享連結

**ClawHub**: https://clawhub.com/skills/InvoiceTW  
**ZIP 檔**: /tmp/InvoiceTW.zip

## 📝 注意事項

- 統一發票號碼為 8 位數字
- 發票每兩個月開獎一次（7 月 1 日、1 月 1 日）
- 中獎後可於超商、郵局或財政部指定地點兌領
- 建議保留發票存根至少一年
- 摸彩資格需同時符合尾碼中獎條件

## 🎮 範例對話

```
使用者：幫我看看 12345678 有沒有中獎
助理：   🎉 12345678: **特獎** - NT$2,000,000 ✨
         🎊 恭喜中獎！請攜帶發票和身份證到超商兌領。

使用者：新增發票 12345678，7/15 開獎，全家，50 元，民生用品
助理：   ✅ 已記錄發票 12345678
         發票號碼：12345678
         日期：7/15
         門市：全家
         金額：NT$50
         分類：其他
         備註：民生用品

使用者：統計一下我的中獎情形
助理：   📊 統一發票統計報表
         📝 發票總數：3 張
         💰 總金額：NT$370
         🎉 中獎次數：1 次
         💵 中獎總額：NT$2,000,000
```

---

**發票查詢，讓中獎更簡單！** 🎉
