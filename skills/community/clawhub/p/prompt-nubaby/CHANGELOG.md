# prompt-nubaby — CHANGELOG

## v1.1 (frozen) — 2026-03-26 (Asia/Taipei)

### What changed (high level)
- **新增四維擴寫器 (Visual Retention Expander)**：把模糊需求擴成「反差主體 × 極限視角 × 情緒光影 × 肢體語言」四層結構
- **新增 Camera / Lighting / Pose 參數層**：可直接脫離自然語言控制視覺張力
- **新增負向 Prompt 自動原則**：自動排除大平光、正經端坐等張力殺手
- **新增安全收斂原則**：校園感強制成年化表述，禁止露骨內容
- **新增 `mode=retention-shot`**：正式列為可用模式之一
- **知識庫來源更新**：吸納 `skill_upgrade_brief_prompt-comfyui-nubaby_20260326.md` 的四維公式

### Frontend-visible entries (stable, v1.1)
以下 9 個是收斂後「前端可見」入口：
1) `nubaby_router_index_v1`
2) `nubaby_router_portrait_base`
3) `nubaby_router_portrait_pro_s2`
4) `nubaby_router_portrait_jp_lifestyle_soft`
5) `nubaby_router_portrait_cinematic_film`
6) `nubaby_router_nails_dataset_captioner`
7) `nubaby_router_nails_concept_designer`
8) `nubaby_router_wan_storyboard_base`
9) **NEW** `nubaby_router_retention_shot`（四維擴寫器）

### Key modes (how to use, v1.1)

#### Portrait / Nails
- `mode=dataset`：固定 8 行前綴 caption（利於資料集 parse/訓練）
- `mode=prompt_tags`：生成用 tags（攝影語言 + anti-AI）
- `mode=prompt_compact`：中文敘事為主 + 少量固定英文控制詞

#### Visual Retention（NEW）
- `mode=retention-shot`：四維擴寫器
  - 第一維：主體反差設定
  - 第二維：視角設計（camera_angle / camera_distance / viewer_relation / head_tilt）
  - 第三維：情緒光影（golden_hour / rim_light / window_blinds_shadow / face_sculpting）
  - 第四維：肢體語言（優先姿勢庫 / 避免姿勢庫）
  - 自動包含負向 Prompt（flat_light=false, stiff_pose=false 等）

#### Video / Storyboard
- `mode=wan2.2`：At 0..5 seconds 單鏡頭英文輸出
- `mode=ltx`：continuous shot 友善 prompt
- `mode=storyboard_grid`：九宮格 storyboard_grid 結構

### 四維總公式
> **反差主體 × 極限視角 × 情緒光影 × 肢體語言 = 高停留感視覺骨架**

### 安全收斂（重要）
- 校園感 / 學院風：強制成年化表述，只保留美學元素
- 禁止：未成年年齡暗示、露骨性行為描述、親密暴力內容
- 四維公式只用於視覺張力結構化，不用於性化描寫

### Notes / policies
- **Qwen 生態語言策略**：中文（繁中/台灣）敘事可作為主體語言；鏡頭/光線等「控制旋鈕」保留少量英文以穩定跨模型。
- **Noisy imports**：來自 Apple Notes HTML export 的片段字典保留但標記為 `draft_noisy_source`，並預設隱藏於前端。

---

## v1.0 (frozen) — 2026-03-09 (Asia/Taipei)

### What changed (high level)
- **UI 收斂（Frontend 白名單）**：前端只保留少量「入口型 routers」，避免字典/備忘錄污染選單。
- **模式統一**：dataset / prompt_tags / prompt_compact 與影片模式（wan2.2 / ltx / storyboard_grid）可透過 router 切換。
- **字典化**：把共用規則集中到 dictionaries，routers/presets 以「參照」方式引用，降低重複與維護成本。
- **分級**：新增 `meta.tier`（production/draft）概念；noisy 來源標記為 draft 並從 UI 隱藏。

### Frontend-visible entries (stable)
以下 8 個是收斂後「前端可見」入口（其餘皆 node-only 或 hidden）：
1) `nubaby_router_index_v1`
2) `nubaby_router_portrait_base`
3) `nubaby_router_portrait_pro_s2`
4) `nubaby_router_portrait_jp_lifestyle_soft`
5) `nubaby_router_portrait_cinematic_film`
6) `nubaby_router_nails_dataset_captioner`
7) `nubaby_router_nails_concept_designer`
8) `nubaby_router_wan_storyboard_base`

### Key modes (how to use)
#### Portrait / Nails
- `mode=dataset`：固定 8 行前綴 caption（利於資料集 parse/訓練）
- `mode=prompt_tags`：生成用 tags（攝影語言 + anti-AI）
- `mode=prompt_compact`：中文敘事為主 + 少量固定英文控制詞

#### Video / Storyboard (via `nubaby_router_wan_storyboard_base`)
- `mode=wan2.2`：At 0..5 seconds 單鏡頭英文輸出
- `mode=ltx`：continuous shot 友善 prompt
- `mode=storyboard_grid`：九宮格 storyboard_grid 結構

### Notes / policies
- **Qwen 生態語言策略**：中文（繁中/台灣）敘事可作為主體語言；鏡頭/光線等「控制旋鈕」保留少量英文以穩定跨模型。
- **Noisy imports**：來自 Apple Notes HTML export 的片段字典保留但標記為 `draft_noisy_source`，並預設隱藏於前端。

