---
name: kids-english-teacher
description: "根據上傳的小朋友英語作業圖片，自動生成一個完整的互動教學網頁（HTML），包含：單字發音、句子跟讀評分（麥克風）、寫作練習、Phonics 和對話練習。Use when: (1) 用戶上傳小朋友英語作業照片, (2) 用戶說「幫小朋友做英語學習頁」, (3) 用戶說「生成教學網頁」, (4) 用戶說「分析這張作業」並希望做成互動頁面。即使用戶只說「幫我做一個學習頁」並附有圖片，也應觸發此技能。NOT for: 純文字英語練習、成人英語學習、非圖片輸入的一般英語問題。"
version: 1.0.0
---

# kids-english-teacher — 兒童英語作業 → 互動教學網頁

用戶上傳一張小朋友英語作業照片，Claude 分析圖片內容，然後生成一個完整的互動 HTML 教學網頁，並返回可下載的文件。

---

## 整體流程

```
1. 分析圖片  →  2. 提取內容  →  3. 生成 HTML  →  4. 輸出文件
```

**每一步都很重要，不要跳過。**

---

## Step 1：分析圖片

仔細看圖片，提取以下信息：

### 必須提取
- **主題/場景**：圖片的主題是什麼？（例：動物園、農場、學校、家庭...）
- **詞彙列表**：圖片中出現的所有英文單字（帶編號標籤的更重要）
- **寫作題目**：Writing 部分的問題和小朋友的答案（包括錯誤的）
- **Phonics 目標音**：本頁練習的字母/發音（例：Z, S, Th...）
- **小朋友的錯誤**：仔細對比正確答案和小朋友寫的，找出拼寫錯誤、用詞錯誤、漏字等

### 分析小朋友的錯誤（非常重要）
對每道 Writing 題：
- 正確答案應該是什麼？
- 小朋友寫了什麼？
- 錯在哪裡？（拼寫？用詞？漏字？）
- 怎麼糾正？用什麼方式讓 6 歲小朋友容易理解？

---

## Step 2：規劃頁面內容

根據提取的信息，規劃 5 個版塊：

| 版塊 | 內容來源 | 說明 |
|------|---------|------|
| 🐾 單字版塊 | 圖片中的詞彙 | 點擊動物/物品聽讀音 + 數字練習 |
| 🎤 跟讀評分 | 主題相關句子 | 聽→跟讀→麥克風評分 |
| ✏️ 寫作練習 | Writing 題目 | 帶針對性錯誤提示的填空 |
| 🔤 Phonics | 圖片中的目標音 | 找目標音開頭的單字 |
| 🎭 對話練習 | 主題角色 | 選角色→多輪對話 |

---

## Step 3：生成 HTML

按照下面的完整模板生成 HTML 文件。**所有內容都要根據圖片替換成實際內容。**

### HTML 模板結構

```html
<!DOCTYPE html>
<html lang="zh">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>🌟 [主題] English Fun!</title>
<link href="https://fonts.googleapis.com/css2?family=Fredoka+One&family=Nunito:wght@400;700;900&display=swap" rel="stylesheet">
<style>
  /* === 完整樣式 - 按主題調整配色 === */
  /* 主題色變量：根據場景替換 */
  /* 動物園: --primary:#87CEEB  農場: --primary:#90EE90  海洋: --primary:#006994 */
  [貼入完整CSS - 見下方 CSS 規範]
</style>
</head>
<body>
  [雲朵/背景裝飾 - 按主題調整]
  
  <div class="container">
    <div class="title">[主題 emoji] [主題名] English!</div>
    <div class="subtitle">[中文副標題] / [英文副標題]!</div>
    
    [星星進度條]
    
    [5個Tab按鈕]
    
    [Tab 1: 單字版塊]
    [Tab 2: 跟讀評分版塊 - 含麥克風]
    [Tab 3: 寫作練習版塊 - 含錯誤提示]
    [Tab 4: Phonics版塊]
    [Tab 5: 對話練習版塊]
  </div>
  
  <script>
    [完整JS邏輯]
  </script>
</body>
</html>
```

### CSS 規範

必須包含以下樣式組件，按主題調色：

```css
/* 1. 背景和裝飾 */
body { background: linear-gradient(180deg, [天空色] 0%, [淺天空色] 38%, [草地色] 38%, [深草地色] 100%); }
.cloud { /* 飄動雲朵 */ animation: drift linear infinite; }
.sun { /* 太陽/月亮/主題裝飾 */ position: fixed; top:20px; right:30px; }

/* 2. 星星進度條 */
.star { filter: grayscale(1); transition: all .3s; }
.star.lit { filter: grayscale(0); animation: starPop .4s ease-out; }
.progress-wrap { background: rgba(255,255,255,.3); border-radius:50px; height:9px; }
.progress-bar { background: linear-gradient(90deg,#f97316,#fbbf24); transition: width .4s; }

/* 3. Tab 導航 */
.tab-btn { background: rgba(255,255,255,.35); color:white; border-radius:50px; font-family:'Fredoka One',cursive; }
.tab-btn.active { background: white; color: #0369a1; }

/* 4. 卡片容器 */
.card { background: #FFFEF0; border-radius:22px; box-shadow: 0 8px 0 rgba(0,0,0,.12); }

/* 5. 單字卡片 */
.vocab-card { border-radius:14px; cursor:pointer; transition: all .2s; }
.vocab-card:hover { transform: translateY(-4px) scale(1.05); }
.vocab-card.playing { border-color: #f97316; }

/* 6. 跟讀按鈕 */
.rec-btn.idle { background: linear-gradient(135deg,#ec4899,#db2777); }
.rec-btn.recording { animation: recPulse .7s ease-in-out infinite; }

/* 7. 分數顯示 */
.score-bar { transition: width .6s ease; border-radius: 50px; }

/* 8. 對話氣泡 */
.msg.animal .msg-bubble { background: linear-gradient(135deg,#ede9fe,#ddd6fe); }
.msg.child .msg-bubble { background: linear-gradient(135deg,#d1fae5,#a7f3d0); }

/* 9. 答對/錯反饋 */
.feedback.ok { background:#dcfce7; color:#166534; border:2px solid #86efac; }
.feedback.bad { background:#fee2e2; color:#991b1b; border:2px solid #fca5a5; }

/* 10. 彩帶慶祝 */
.confetti-piece { animation: confettiFall 1.5s ease-in forwards; }
```

### JS 核心邏輯規範

必須實現以下功能模塊：

#### A. 星星系統
```javascript
let starCount = 0, MAX_STARS = 10;
function addStar() { /* 點亮下一顆星，集滿觸發 celebrate() */ }
function celebrate() { /* 生成彩帶 confetti */ }
```

#### B. 語音合成（所有朗讀按鈕）
```javascript
function speak(text, rate=0.82, callback) {
  const u = new SpeechSynthesisUtterance(text);
  u.lang = 'en-US';
  u.rate = rate;
  speechSynthesis.speak(u);
}
// 慢速版本：rate=0.6
// 句子版本：rate=0.78
```

#### C. 麥克風跟讀評分（核心功能）
```javascript
const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

function scoreText(heard, target) {
  // 詞語匹配算法：模糊匹配，適合小朋友發音
  // 返回 0-100 分
}

function startRecording(idx, targetText) {
  // 開始錄音 → 識別 → 調用 showScore()
  // 按鈕狀態：idle → recording → idle
}

function showScore(idx, score, heard, target) {
  // 顯示：分數、進度條、綠色=說對/紅色=漏掉、聽到的文字
  // 85+ 分：🌟 太棒了 + addStar()
  // 65-84：👍 很好
  // 40-64：💪 再試試
  // 0-39：🎤 說大聲點
}
```

#### D. 寫作批改
```javascript
function checkAnswer(questionId) {
  // 1. 取得用戶輸入
  // 2. 對比正確答案（支持多種正確寫法）
  // 3. 檢測常見錯誤（從圖片分析的錯誤）
  // 4. 顯示針對性反饋
  // 5. 答對 → addStar() + speak(正確句子)
}
```

#### E. 對話系統
```javascript
// 數據結構
const dialogues = {
  [角色名]: [
    { who:'animal', en:"...", zh:"..." },
    { who:'child', opts:[
      { en:"...", zh:"...", ok:true },
      { en:"...", zh:"...", ok:false, msg:"提示..." },
    ]},
    // ...
  ]
};

function runStep() { /* 驅動對話流程 */ }
function selectReply(opt, btn) { /* 處理選項，答對繼續，答錯給提示 */ }
```

---

## Step 4：內容填充指南

### 單字版塊
- 從圖片提取所有詞彙，每個配上合適的 emoji
- 加入中文翻譯
- 數字 1-5（或根據題目數量調整）也要加入

### 句子版塊（10-12句）
必須包含：
- 圖片中 Writing 部分的問題句（How many...? What is...?）
- 正確答案句（There are... / It is a...）
- 主題相關延伸句（I like... / I can see... / The [animal] is...）
- 日常用語（Hello! / Goodbye! / I love...!）

### 寫作批改
對每道題：
```javascript
// 正確答案（支持多種寫法）
const correct = ['正確答案1', '正確答案2'];

// 從圖片分析到的小朋友錯誤 → 特定提示
if (val.includes('常見錯誤片段')) {
  // 顯示針對性提示，用中英文解釋
}
```

提示框格式：
```html
<div class="error-note">
  💡 你寫了 "[小朋友的錯誤]" — [用中文解釋錯在哪]！<br>
  [英文]的[複數/時態/拼寫]規則：<b>[正確寫法]</b>！
</div>
```

### Phonics 版塊
- 目標音字母大展示（動畫）
- 6個單字：3個是目標音開頭，3個不是（做干擾項）
- 加一個包含2個目標音的完整句子
- 提供正常速度和慢速兩個播放按鈕

### 對話版塊
- 3個角色可選（來自圖片的詞彙）
- 每個角色 4 輪對話（1輪 = 動物說 + 小朋友選擇回答）
- 每輪 3 個選項（1個正確，2個錯誤但有針對性提示）
- 對話內容要包含圖片中的句型（How many...? There are...）
- 最後一輪動物說再見

---

## Step 5：輸出文件

1. 將完整 HTML 保存到 `/mnt/user-data/outputs/[主題]-english-lesson.html`
2. 使用 `present_files` 工具返回文件給用戶
3. 在回覆中說明：
   - 網頁包含哪些版塊
   - 找到了哪些作業錯誤並已內置提示
   - **下載後用 Chrome 打開**，麥克風功能才能正常使用
   - 第一次打開時允許麥克風權限

---

## 質量檢查清單

生成 HTML 前確認：

- [ ] 所有詞彙都來自圖片（不要憑空添加無關詞彙）
- [ ] 圖片中小朋友的錯誤已被識別並有針對性提示
- [ ] 句子版塊包含作業原題的句型
- [ ] 對話腳本至少使用 2 個作業中的句型
- [ ] 麥克風按鈕有 `idle / recording / processing` 三種狀態
- [ ] 答對後有 `speak()` 朗讀正確答案
- [ ] 星星系統連接到所有互動（跟讀85分+、寫作答對、Phonics答對、對話答對）
- [ ] 有「無麥克風」的降級提示（`.no-mic` banner）
- [ ] 文件名反映主題（例：`zoo-english-lesson.html`，不要用 `learn.html`）

---

## 主題配色參考

| 場景 | 天空色 | 草地色 | 強調色 | 裝飾 |
|------|--------|--------|--------|------|
| 動物園 | #87CEEB | #5DBB63 | #f97316 | ☀️ 太陽 |
| 農場 | #FFF4B2 | #8BC34A | #f59e0b | 🌻 向日葵 |
| 海洋 | #E0F7FA | #006994 | #0284c7 | 🌊 海浪 |
| 學校 | #F3E5F5 | #C8E6C9 | #7c3aed | 📚 書本 |
| 家庭 | #FFF8E1 | #DCEDC8 | #ec4899 | 🏠 房子 |
| 超市/食物 | #FFF3E0 | #E8F5E9 | #16a34a | 🛒 購物車 |

---

## 注意事項

1. **年齡適配**：所有文字說明要同時有中文和英文，方便 6 歲小朋友和家長一起使用
2. **字體**：標題用 `Fredoka One`，正文用 `Nunito`（從 Google Fonts 加載）
3. **離線兼容**：字體加載失敗時要有備用字體，核心功能不依賴網路
4. **麥克風**：在本地 Chrome 中正常工作；Claude 預覽環境因安全限制無法使用，要告知用戶需下載後在 Chrome 中打開
5. **文件大小**：整個 HTML 控制在 60KB 以內（單文件，CSS/JS 都內聯）
6. **不要外部依賴**：除 Google Fonts 外，不引用任何外部 JS 庫
