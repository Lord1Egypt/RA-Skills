---
name: prompt-nubaby
description: "Nubaby prompt system for prompt augmentation, routers, dictionaries, dataset captions, prompt tags, compact prompts, video/storyboard prompt shaping, and structured visual tension expansion. Use when prompts are too short/vague or need structured upgrade before comfyui-nubaby execution."
---

# Prompt Nubaby Skill 🦞

## 概述
這是 Nubaby AI 的專屬提示詞大師技能。它內化了多個頂級 ComfyUI 提示詞插件的精華，具備「人像大師」、「影片導演」、「像素級反推」等多種專業模式。

## 核心功能
1. **人像大師 (Portrait Master)**：極致細化皮膚肌理、服飾材質，光影氛圍與微表情。
2. **影片導演 (Video Director)**：針對 Wan 2.1 等視頻模型，精確描述物理運動慣性與電影語言。
3. **Tags 專家 (Tag Expert)**：將簡單想法轉化為高權重、精確的 Danbooru Tags 流。
4. **智慧轉換 (Auto-Converter)**：根據亞瑟的簡單描述，自動判定領域並套用對應的專業術語。
5. **四維擴寫器 (Visual Retention Expander)**：把模糊需求擴成四層結構（2026-03-26 新增）。

## 知識庫來源
- **Base Recipes**: 內化自 `ComfyUI-Prompt-Assistant` (yawiii) 的核心邏輯。
- **Nubaby Custom**: 亞瑟親自微調與加入的專屬提示詞知識。
- **Visual Retention (2026-03-26)**: 從 `skill_upgrade_brief_prompt-comfyui-nubaby_20260326.md` 吸收的四維公式 + Camera/Lighting/Pose 參數層。

## 使用方式
當亞瑟要求「用大師模式寫一段提示詞」時，我會自動呼叫此 Skill 的知識庫進行腦內運算。

## 正式分工（2026-03-13 定案）
- `prompt-nubaby` 是 `comfyui-nubaby` 的正式 prompt augmentation layer。
- 當生成需求的 prompt 太短、太糊、缺鏡頭 / 風格 / 限制條件時，應先由 `prompt-nubaby` 補成可執行 prompt。
- `comfyui-nubaby` 則負責 routing / workflow / node / API 執行。

## 擴充協議
亞瑟隨時可以對我說：「龍蝦，記住這段大師提示詞：[內容]」，我會將其存入 `knowledge/master_recipes.json` 中，永久累積。

---

## 四維擴寫器（Visual Retention Expander）— 2026-03-26 新增

### 上層總公式
> **反差主體 × 極限視角 × 情緒光影 × 肢體語言 = 高停留感視覺骨架**

當使用者需求涉及「張力感、親密感、女友感、留存感」時，啟動此模式。

### 四層結構

**第一維：主體反差設定**
- 主體處於非預期狀態（放鬆 vs 緊繃、慵懶 vs 專注）
- 制服/正裝 vs 私領域肢體
- 室內安全感 vs 外部威脅感

**第二維：視角設計**
- 極限視角比正視角更有張力（低仰角 > eye_level > 俯視）
- 第一人稱 > 第三者觀察 > 無視角
- Viewer-主體關係影響親密感

**第三維：情緒光影**
- 情緒化光影比大平光更有深度（逆光 > 側光 > 正面平光）
- 雕刻光（collarbone、顴骨）增加真實感
- 光影是情緒的延伸，不是純技術參數

**第四維：肢體語言**
- 緊張的放鬆姿（看似放鬆但有張力）
- 輕微後仰 / 側身回眸 > 正面端坐
- 肢體微微越界（視覺停留感）但不露骨

### Camera 參數層

| 參數 | 值 |
|------|-----|
| `camera_angle` | eye_level / low_angle / extreme_low_angle / oblique_top_down |
| `camera_distance` | close_up / intimate_close / medium_close / medium |
| `viewer_relation` | first_person / observer / over_shoulder |
| `head_tilt` | none / subtle / dramatic |

### Lighting 參數層

| 參數 | 值 |
|------|-----|
| `flat_light` | false（預設）|
| `golden_hour` | true（暖調情緒）|
| `rim_light` | true（輪廓雕刻）|
| `window_blinds_shadow` | optional（百葉窗斑駁光）|
| `backlight_strength` | low / medium / high |
| `face_sculpting` | soft / defined / dramatic |

### Pose 參數層（高停留感姿勢庫）

優先姿勢：
- 微微後仰（cervical extension）
- 側身回眸（half-turn glance）
- 靠桌/靠牆站姿
- 頭部向後靠
- 扭腰 / 側身對角線
- 倒著看鏡頭

避免姿勢：
- 大平光正面端坐
- 正對鏡頭無表情
- 肢體過度僵硬
- 背景搶戲

### 負向 Prompt 自動原則（必含）

這些會破壞張力的元素，自動寫入 negative prompt：
- 大平光（flat lighting）
- 正經端坐（stiff pose）
- 無互動感平視（no engagement eye contact）
- 肢體過度僵硬（rigid body）
- 背景過度搶戲（dominant background）

---

## 安全收斂原則（重要！）

當需求涉及「校園感、學院風」等場景時，**自動強制成年化表述**：
- 禁止任何未成年年齡暗示
- 「校園感」只保留美學元素（窗邊光、制服廓型），不允許肢體/情緒暗示未成年
- 禁止露骨性行為描述
- 四維公式只用在**視覺張力結構化**，不用在性化描寫

四維公式橫向適用於：
- 女友感寫真
- 慵懶生活感
- 高級感棚拍
- 曖昧敘事視覺
- 商業廣吔級人像

---

## 收斂版（v1.0-rc）目前支援的模式（實務用）

### 圖片/人像/美甲（Qwen 生態中文優先）
- `mode=dataset`：8 行固定前綴 caption（Global Summary…Action & Interaction），利於訓練/解析
- `mode=prompt_tags`：生成用攝影語言 + anti-AI
- `mode=prompt_compact`：先 dataset 草稿再壓縮成單段生成 prompt（中文為主 + 少量固定英文控制詞）
- `mode=retention-shot`（新增）：四維擴寫器，用於高張力視覺需求

### 影片/分鏡
- `nubaby_router_wan_storyboard_base`：
  - `mode=wan2.2`：Wan2.2 英文單鏡頭（At 0…5 seconds）
  - `mode=ltx`：LTX 友善連續鏡頭 prompt
  - `mode=storyboard_grid`：九宮格 storyboard_grid 結構
