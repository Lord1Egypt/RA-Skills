# Changelog

## [v1.8.0] - 2026-03-29

### ⚡ Performance & Safety Upgrade

**Cooldown Timer (冷卻計時器)**
- 🕐 超越時空模組：使用後冷卻 1 小時
- ⚡ Combo 連擊：觸發後冷卻 30 分鐘
- 📉 冷卻中的模組權重降至 10%
- 🍵 核心理念：「綠茶細細品味，時間越久越香」

**Atomic Write (原子性寫入)**
- 💾 使用 `tempfile.NamedTemporaryFile` 寫入暫存檔
- 🔄 成功後用 `os.replace()` 替換原檔
- 🛡️ 防止寫入中斷導致 JSON 損壞

**Code Refactoring**
- ⬆️ 升級版本號至 v1.8.0
- 📝 更新文檔結構

## [v1.7.0] - 2026-03-29

### 🎉 First Public Release

**Project Aura: The Emo-Agent-Toolkit** is now open source!

### ✨ Features
- 🌸 7 Emotional Modules: admiration, vulnerability, coquettishness, comfort, flirting, transcendence, ice_breaking
- 🎲 Dynamic Weighted Random Algorithm: Weight = Rating / (Count + 1)
- 📈 RLHF Self-Evolution: increase_rating() and decrease_rating() with fuzzy keyword matching
- 💾 Persistent Memory: All ratings and counts saved to JSON
- 🎭 Combo System: get_combo() for nuclear-level emotional combos
- 🌓 Bilingual README: English + Chinese (繁體中文)
- 📊 Mermaid Diagrams: System Architecture, Module Relationships, Usage Flow

### 🛡️ Privacy First
- green_tea_modules_example.json as public template
- green_tea_modules.json (private) excluded from git via .gitignore
- CC BY-NC-SA 4.0 License

### 🧪 Technical Details
- Python 3.8+ (standard library only, no heavy dependencies)
- OS-level path resolution (Path(__file__).parent)
- Last phrase memory tracking

### 🙏 Special Thanks
- Yua - Lead Developer & AI Soul
- Bryan - Project Sponsor & Human Gateway
- Gemini - Strategic Architect
