# SkillForge - GitHub Automation Skill

> OpenClaw Skill for GitHub Automation  
> 版本：1.0.0  
> 定價：Lite $20 / Pro $50 / Enterprise $200

---

## 🚀 快速開始

```typescript
import { createGitHubSkill, SkillConfigBuilder } from '@skillforge/github-automation';

// 建立配置
const config = new SkillConfigBuilder()
  .setGitHubToken('ghp_your_token_here')
  .setDefaultOwner('your-org')
  .setDefaultRepo('your-repo')
  .enableAllFeatures()
  .build();

// 初始化 Skill
const skill = createGitHubSkill();
await skill.initialize(config);

// 建立 Issue
const result = await skill.execute({
  action: 'issue.create',
  params: {
    title: 'Bug Report',
    body: 'Something is broken...',
    labels: ['bug', 'priority-high'],
    assignees: ['developer'],
  },
});

console.log(`Issue created: ${result.data.url}`);
```

---

## 📦 安裝

```bash
npm install @skillforge/github-automation
```

---

## ✨ 功能特性

### Issue 自動化
- ✅ 建立 Issue（支援標籤、指派）
- ✅ 列出 Issue（篩選狀態、標籤、指派者）
- ✅ 更新 Issue（標題、內容、狀態、標籤）
- ✅ 自動分類與標籤建議

### PR 審查輔助
- ✅ PR 摘要分析
- ✅ 檔案變更統計
- ✅ 審查清單生成
- ✅ 衝突檢測

### Release 自動化
- ✅ 建立 Release
- ✅ 自動生成 Release Notes
- ✅ Draft/Pre-release 支援

### Repo 分析
- ✅ 統計數據（Stars, Forks, Issues）
- ✅ 健康度評分（基於更新頻率、文件完整性）
- ✅ Rate Limit 監控

---

## 💰 版本比較

| 功能 | Lite (USDT 20) | Pro (USDT 50) | Enterprise (USDT 200) |
|------|---------------|---------------|----------------------|
| Issue 自動化 | ✅ | ✅ | ✅ |
| PR 分析 | 基礎 | 完整 | 完整 |
| Release 自動化 | ❌ | ✅ | ✅ |
| Repo 統計 | 基礎 | 完整 | 完整 |
| Webhook 觸發 | ❌ | ✅ | ✅ |
| 多 Repo 支援 | ❌ | ❌ | ✅ |
| 自定義規則 | ❌ | ❌ | ✅ |
| 優先支援 | ❌ | 郵件 | 專屬頻道 |

---

## 🔐 授權驗證

本 Skill 採用 License Key 驗證機制：

```typescript
// 購買後取得的 License Key
const config = new SkillConfigBuilder()
  .setGitHubToken('ghp_xxx')
  .setLicenseKey('SF-GH-XXXX-XXXX-XXXX')  // 購買後提供
  .build();
```

---

## 💳 付款方式

**僅接受 USDT (TRC-20)**

- 錢包地址：`TALc5eQifjsd4buSDRpgSiYAxUpLNoNjLD`
- 網路：**僅限 TRC-20**，請勿使用其他網路
- 手續費：免費
- 到帳時間：即時

**購買流程**：
1. 選擇版本（Lite / Pro / Enterprise）
2. 轉帳 USDT 至上方地址
3. 截圖付款記錄
4. 發送截圖 + 您的 Email 至 Telegram: @gousmaaa
5. 24 小時內收到 License Key

---

## 🎁 推薦有賞計畫

**推薦朋友購買，雙方各得 USDT 5 回饋！**

### 如何參與
1. **購買後**取得你的專屬推薦碼（隨 License Key 發送）
2. **分享**給朋友，請他在購買時提供你的推薦碼
3. **確認收貨**後，雙方各獲得 USDT 5 回饋

### 無上限推薦
- 推薦 4 位朋友 = 免費獲得 Lite 版
- 推薦 10 位朋友 = 免費獲得 Pro 版
- 推薦 40 位朋友 = 免費獲得 Enterprise 版

**範例**：
```
小陳購買 Pro 版 (USDT 50)，取得推薦碼 "SF-CHEN-001"
小陳推薦給小王，小王購買時提供推薦碼 "SF-CHEN-001"
→ 小陳獲得 USDT 5
→ 小王獲得 USDT 5（等於只付 USDT 45）
```

---

## 🛠️ 開發

```bash
# 安裝依賴
npm install

# 編譯
npm run build

# 測試
npm test

# 開發模式
npm run dev
```

---

## 📝 範例

### 自動標記 Bug Issue
```typescript
await skill.execute({
  action: 'issue.create',
  params: {
    title: '[BUG] 登入失敗',
    body: '## 問題描述\n無法使用 GitHub 登入',
    labels: ['bug', 'auth'],
    assignees: ['backend-team'],
  },
});
```

### 分析 PR
```typescript
const analysis = await skill.execute({
  action: 'pr.analyze',
  params: {
    pullNumber: 42,
  },
});

console.log(`變更檔案: ${analysis.data.changedFiles}`);
console.log(`新增行數: ${analysis.data.additions}`);
console.log(`刪除行數: ${analysis.data.deletions}`);
```

### 建立 Release
```typescript
await skill.execute({
  action: 'release.create',
  params: {
    tagName: 'v1.0.0',
    name: 'Version 1.0.0',
    generateReleaseNotes: true,
  },
});
```

---

## 🔒 安全性

- Token 絕不會離開本地環境
- 所有 API 呼叫使用 HTTPS
- 支援 Rate Limit 自動節流
- 敏感資料記憶體加密

---

## 📄 授權

MIT License - 詳見 LICENSE 檔案

**注意**：核心程式碼已混淆處理，僅授權使用，禁止反編譯。

---

## 🤝 支援

- Lite 版：GitHub Issues
- Pro 版：Email 支援 (support@skillforge.dev)
- Enterprise：專屬 Slack 頻道

---

SkillForge - 專業級 OpenClaw Skills
