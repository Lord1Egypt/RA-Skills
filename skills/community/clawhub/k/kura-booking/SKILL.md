---
name: kura-booking
description: 使用 e-pai-ke.com (E排客) 進行餐廳預約管理、叫號查詢、登入及取消訂位。適用於藏壽司等使用 E排客 系統的餐廳。
---

# E-Pai-Ke (E排客) Skill

本 Skill 用於自動化操作 E排客 (e-pai-ke.com) 進行餐廳的登入、尋找、查詢及預約管理。

## 帳號資訊參考
- 登入資訊通常記載於 `e-pai-ke/notes.md`。

## 操作流程

### 1. 登入 (Login)
使用 `browser` 工具的 `evaluate` 行動注入 JS 進行登入，以避免表單填充失效：
```javascript
const emailInput = document.querySelector('input[placeholder="電子郵件"]') || document.querySelector('input[type="text"]');
const passwordInput = document.querySelector('input[placeholder="密碼"]') || document.querySelector('input[type="password"]');
const loginButton = Array.from(document.querySelectorAll('button')).find(b => b.textContent.includes('登入')) || document.querySelector('.login_btn');
if (emailInput && passwordInput && loginButton) {
  emailInput.value = 'YOUR_EMAIL';
  passwordInput.value = 'YOUR_PASSWORD';
  loginButton.click();
}
```

### 2. 尋找店鋪 (Search Shop)
1. 導航至 `https://e-pai-ke.com/`。
2. 在搜尋欄輸入店鋪名稱（如「藏壽司 土城金城路店」）。
3. 點擊進入店鋪詳情頁。

### 3. 查詢叫號與狀態
查看店鋪頁面中「指定時間預約」與「預約未到候補」的「現在叫號」及「最快可候位時間」。

### 4. 執行預約 (Booking)
1. 點擊「預約」按鈕（`.res_btn`）。
2. 在 Dialog 中依序：選取日期 -> 選取時段 -> 選擇人數 -> 點擊「內容確認」直至顯示預約成功及候位號碼。

### 5. 取消預約 (Cancel)
1. 導航至 `https://e-pai-ke.com/reservationA`。
2. 找到目標預約紀錄，點擊「取消」並於彈窗中點擊「確認取消」。

## 故障排除與 Playwright 自動化
若內建 `browser` 工具不穩定或出現逾時，建議使用 Playwright 獨立腳本進行操作。

### 1. 取消預約腳本範例 (`cancel_kura.js`)
```javascript
const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext();
  const page = await context.newPage();
  // 1. 登入邏輯 (參考 e-pai-ke/notes.md)
  // 2. 導航至 https://e-pai-ke.com/reservationA
  // 3. 定位預約卡片並點擊「取消」與「確認取消」
  await browser.close();
})();
```

### 2. 優點
- **穩定性**: 獨立進程執行，不受內建工具逾時限制。
- **精準定位**: 可使用 Playwright 強大的 `locator` 配合 `hasText` 進行複雜條件過濾，避免誤刪或找不到元素。
- **視覺調試**: 可隨時加入 `page.screenshot()` 捕捉失敗畫面。

## 錯誤偵測
- **時段額滿**: `button` 帶有 `[disabled]` 屬性。
- **提示訊息**: 檢查頁面是否出現 `該時段尚未開放候位或候位名額已滿` 或 `每個帳號每次僅能預約一筆`。
