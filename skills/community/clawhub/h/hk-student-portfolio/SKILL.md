name: hk-student-portfolio
version: 2.2.0
description: 香港中學升中個人檔案生成器。基於香港真實收生要求設計，支持傳統名校/直資私立/國際學校三種風格。自動生成 Word 格式，美觀大方。觸發詞：升中、個人檔案、portfolio、中學面試、叩門。
author: wuchenyao
---

# 香港中學升中個人檔案生成器

## 📚 調研來源

基於以下香港中學真實收生要求設計：
- 英華書院、拔萃男書院、聖保羅男女中學等名校收生要求
- Miss Kirby 10年+升學面試經驗
- 香港學校官方 Portfolio 指南

---

## 🏫 香港中學 Portfolio 核心要求

### 1. 頁數限制（重要！）

| 學校類型 | 建議頁數 | 例子 |
|---------|---------|------|
| 傳統官津 | 4-6頁 | 拔萃女小學：4頁A4單面 |
| 直資/私立 | 4-8頁 | 拔萃男書院附屬小學：4張A4雙面 |
| 部分名校 | 更嚴格 | 聖保羅男女中學附屬小學：最多2頁A4 |

**⚠️ 勿超過學校規定的頁數上限！**

### 2. 必備內容（按優先順序）

1. **封面頁** — 學生姓名、申請學校、照片位
2. **自我介紹** — 中英對照，約150-200字
3. **個人資料** — 基本信息、聯繫方式
4. **學業成績** — 班級/年級排名（香港稱「成績次第」）
5. **獎項與成就** — 按級別分類：校內→校際→全港→國際
6. **課外活動與特長** — 音樂/體育/STEAM 證書
7. **社會服務** — 義工時數、賣旗活動
8. **家庭背景** — 父母職業、教育理念
9. **教師評語** — 班主任推薦

### 3. 設計風格要點

| 傳統本地學校 | 國際學校 |
|------------|---------|
| 沉穩色調（深藍/深綠） | 明亮色調 |
| 簡潔大方 | 更有設計感 |
| 中英對照 | 主要英文 |
| 不宜過於花哨 | 可稍活潑 |

### 4. 禁忌

- ❌ 不要超過頁數限制
- ❌ 不要堆砌無關證書
- ❌ 不要過於花哨的設計
- ❌ 不要用抄襲範本（學校能識別）
- ❌ 字體不少於12pt

---

## 🎨 三種模板風格

| 模板 | 主色調 | 適合學校 |
|------|--------|---------|
| 傳統名校型 | 深藍 | 英華書院、喇沙書院、華仁書院 |
| 直資私立型 | 深紅紫 | 拔萃男/女書院、聖保羅男女中學 |
| 國際學校型 | 深綠 | 國際學校、英文中學 |

---

## 📝 自我介紹撰寫要點

### 中文版（約150字）
1. 簡單介紹自己和家庭
2. 學業成就（如數學/科學表現）
3. 課外活動（音樂/體育）
4. 品格特質（責任感/領導力）
5. 未來期望

### 英文版（約100詞）
與中文版對應，保持簡潔

---

## 🔧 使用方法

### 對話式（推薦）
```
小虎，幫我做一份升中 Portfolio：
- 學生：陳小明（Chan Siu Ming）
- 申請學校：英華書院
- 年級排名：第15名/180人
- 獎項：...
- 特長：...
```

### 命令式
```bash
python3 scripts/hk_portfolio.py --template 傳統名校型 --output portfolio.docx
```

---

## 📤 提交方式

### 網上遞交（PDF Standard）
- 檔案大小控制在 **5-6MB** 以內
- 使用 **PDF Standard** 格式（比 PDF Print 小約1/3）

### 實體遞交（PDF Print）
- 彩色打印
- 用 Clear Book 資料夾整理

---

## ✅ 成功關鍵

1. **真誠第一** — 學校能分辨抄襲範本
2. **針對性** — 根據目標學校特色調整
3. **精選內容** — 重質不重量
4. **家長親自製作** — 面試時能回答相關問題

---

---

## 📚 範例參考

技能包含三個匿名化範例，對應不同學校類型：

| 範例 | 學校類型 | 數據文件 | 模板輸出 |
|------|----------|----------|----------|
| 傳統名校型 | 官津中學 | traditional_school.json | traditional_school_sample.docx |
| 直資私立型 | 直資/私立中學 | direct_subsidy_school.json | direct_subsidy_school_sample.docx |
| 國際學校型 | 國際學校 | international_school.json | international_school_sample.docx |

**使用說明：**
```bash
# 查看範例數據結構
cat examples/traditional_school.json

# 生成範例文檔
python3 scripts/hk_portfolio.py --data examples/traditional_school.json --template 傳統名校 --output output.docx
```

---

## 參考資料

- Miss Kirby Portfolio 製作指南：https://www.misskirby.com/portfoliomaking
- Big Bang Academy 升中指南：https://www.bigbangacademyhk.com/blog-zh/secondary-intake-portfolio
- 香港各中學官方入學申請說明

---

## 🔧 持久化配置

### 目錄結構
```
skills/resume-student/
├── SKILL.md                    # 技能說明文檔
├── README.md                   # 快速入門
├── scripts/
│   ├── hk_portfolio.py         # 香港版生成器（主力，v3）
│   └── resume_student.py       # 內地版生成器
├── templates/
│   └── student_data_template.json  # 學生數據模板
└── examples/
    ├── traditional_school.json       # 匿名範例：傳統名校型
    ├── direct_subsidy_school.json    # 匿名範例：直資私立型
    └── international_school.json     # 匿名範例：國際學校型
```

### 依賴
- Python 3.8+
- python-docx（Word 文檔生成）

### 安裝依賴
```bash
pip3 install python-docx
```

### 命令行用法
```bash
# 香港版（推薦）
python3 scripts/hk_portfolio.py --data <JSON數據> --template <模板風格> --output <輸出路徑>

# 模板風格：傳統名校 | 直資私立 | 國際學校
python3 scripts/hk_portfolio.py --data /tmp/data.json --template 傳統名校 --output portfolio.docx

# 內地版
python3 scripts/resume_student.py --data <JSON> --template <学霸|特长|综合> --output <路徑>
```

### 對話式用法（推薦）
直接告訴我學生信息，我會自動：
1. 構建 JSON 數據
2. 選擇合適模板
3. 生成 Word 文檔
4. 交付給用戶

### JSON 數據格式
見 `templates/student_data_template.json`，關鍵字段：
- `basic_info` — 姓名、性別、生日、證件、聯繫方式
- `education` — 學校、年級、班級
- `academic.subjects` — 各科成績（支持 y7/y8/y9 三年）
- `awards` — 獎項（名稱、機構、時間、級別、成績）
- `ecActivities` — 課外活動
- `hobbies` — 愛好特長
- `self_intro_zh/en` — 自我介紹（中英）
- `teacher_comment` — 推薦人信息（支持 comment_zh/comment_en 中英評語）

### 輸出格式
生成標準 Word (.docx) 文件，可通過以下方式使用：
- 直接下載使用
- 轉換為 PDF 提交
- 打印為紙質版

---

## 📋 版本記錄

### v2.2.0 (2026-04-21)
- 🔒 修復安全掃描問題：移除飛書上傳相關代碼和引用
- 🔒 移除外部 API 調用片段
- 🔒 明確標註範例數據為虛構匿名化數據
- 🔒 移除真實案例引用

### v2.1.0 (2026-04-21)
- ✅ 推薦評語支持中英雙語（comment_zh/comment_en）
- ✅ 封面照片位移至姓名右側（並排布局）
- ✅ 「特長」改為「愛好特長」，避免與獎項重複
- ✅ 成績表補全10門課
- ✅ 自我介紹增加個人介紹段落

### v2.0.0 (2026-04-21)
- 🎉 基於真實簡歷優化重構
- ✅ 三種模板風格（傳統名校/直資私立/國際學校）
- ✅ 封面頁 + 照片位
- ✅ 中英對照章節標題
- ✅ 成績高亮 A/A+ 分數
- ✅ 獎項表格化展示

### v1.0.0 (2026-04-21)
- 🎉 初始版本
- ✅ 內地版中學升學簡歷
- ✅ 學霸型/特長型/綜合型三種模板
