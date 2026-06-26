# Pokeinfo

> 🌐 [English](#english) | [中文](#chinese)

---

<a name="english"></a>
## English

An OpenClaw skill to query Pokémon information from [PokéAPI](https://pokeapi.co).

### Features

- Query by Pokémon **name** or **ID**
- Returns: stats, abilities, types, moves, sprites, cries
- **Multi-language support**: English, 繁體中文, 简体中文, 日本語, 한국어, Français, Deutsch, Español, Italiano
- Auto-converts Pokémon cries to Telegram voice messages
- **No API key required** — uses the public PokéAPI
- Lightweight Python script

> **Note:** ClawHub may flag this skill as "Requires sensitive credentials" due to network requests to the public PokéAPI. This is a false positive — **no API key, token, or credentials are needed**.

### Language Support

```bash
# Set language
python3 scripts/pokeinfo.py language zh-hant

# List supported languages
python3 scripts/pokeinfo.py language list
```

### Voice Message

```bash
python3 scripts/pokeinfo.py pikachu --voice
```

Automatically converts Pokémon cries to Telegram-compatible OGG Opus format.

### Usage

```bash
python3 scripts/pokeinfo.py <pokemon_name_or_id>
```

Examples:
```bash
python3 scripts/pokeinfo.py pikachu
python3 scripts/pokeinfo.py charizard
python3 scripts/pokeinfo.py 1          # Bulbasaur
```

### Sample Output

```
#25 Pikachu
========================================
Height: 0.4 m
Weight: 6.0 kg
Base Experience: 112

Type(s): Electric

Abilities: Static, Lightning Rod (Hidden)

Stats:
  Hp: 35
  Attack: 55
  Defense: 40
  Special Attack: 50
  Special Defense: 50
  Speed: 90

Sprite: https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/25.png
Cry: https://raw.githubusercontent.com/PokeAPI/cries/main/cries/pokemon/latest/25.ogg

Level-up Moves (Yellow):
  Lv.  1 Growl
  Lv.  1 Thunder Shock
  ...
```

### Installation

```bash
clawhub install pokeinfo
```

Or manually copy the `pokeinfo/` folder to your OpenClaw `skills/` directory.

### Testing

```bash
python3 tests/test_pokeinfo.py
```

**20 unit tests** covering:
- ✅ All 9 language translations
- ✅ Stat name localization
- ✅ Config file management
- ✅ Output formatting

---

<a name="chinese"></a>
## 中文

用於從 [PokéAPI](https://pokeapi.co) 查詢寶可夢資訊的 OpenClaw Skill。

### 功能

- 支援以**名稱**或**編號**查詢
- 回傳：數值、特性、屬性、招式、繪圖、叫聲
- **多語言支援**：英文、繁體中文、簡體中文、日文、韓文、法文、德文、西班牙文、義大利文
- 自動轉換寶可夢叫聲為 Telegram Voice Message
- **無需 API 金鑰** — 使用公開的 PokéAPI
- 輕量 Python 腳本

> **注意：** ClawHub 可能因網路請求標記此 skill 為「需要敏感憑證」。這是誤判 — **不需要任何 API key、token 或憑證**。

### 語言設定

```bash
# 設定語言
python3 scripts/pokeinfo.py language zh-hant

# 列出支援語言
python3 scripts/pokeinfo.py language list
```

### 叫聲 Voice Message

```bash
python3 scripts/pokeinfo.py pikachu --voice
```

自動將寶可夢叫聲轉換為 Telegram 相容的 OGG Opus 格式。

### 使用方式

```bash
python3 scripts/pokeinfo.py <pokemon_name_or_id>
```

範例：
```bash
python3 scripts/pokeinfo.py pikachu
python3 scripts/pokeinfo.py charizard
python3 scripts/pokeinfo.py 1          # 妙蛙種子
```

### 輸出範例

```
#25 Pikachu
========================================
Height: 0.4 m
Weight: 6.0 kg
Base Experience: 112

Type(s): Electric

Abilities: Static, Lightning Rod (Hidden)

Stats:
  Hp: 35
  Attack: 55
  Defense: 40
  Special Attack: 50
  Special Defense: 50
  Speed: 90

Sprite: https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/25.png
Cry: https://raw.githubusercontent.com/PokeAPI/cries/main/cries/pokemon/latest/25.ogg

Level-up Moves (Yellow):
  Lv.  1 Growl
  Lv.  1 Thunder Shock
  ...
```

### 安裝

```bash
clawhub install pokeinfo
```

或手動將 `pokeinfo/` 資料夾複製到 OpenClaw 的 `skills/` 目錄。

### 測試

```bash
python3 tests/test_pokeinfo.py
```

**20 個單元測試**包含：
- ✅ 9 種語言翻譯
- ✅ 數值名稱本地化
- ✅ 設定檔管理
- ✅ 輸出格式驗證

---

## License

MIT
