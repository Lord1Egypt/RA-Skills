---
name: poe1-build-analyst-zh-tw
description: 繁體中文參考版：產生、比較並驗證指定版本或聯盟的 PoE1 BD，支援 PoE 3.29、PoE Ninja 與 qpooqp777/pob-cli。
---

# PoE1 BD 產生器與驗證器

## 目標與邊界

依使用者指定的版本、聯盟、職業、昇華、主技能、玩法、模式、預算與目標，產生可重現的 PoE1 BD。PoE Ninja 只代表公開統計快照；Path of Building Community 透過 `pob-cli` 的 headless 計算，才是傷害與防禦數值的權威來源。沒有相容 XML 與 PoB root 時，不得把估算值標成官方 PoB 結果。

使用者說「PoE 3.29」時，以 **Curse of the Allflame** 作為預設人類可讀範例，但仍須核對實際聯盟識別碼與資料快照。Standard、Hardcore、SSF 必須分開處理，並記錄擷取時間、聯盟、篩選條件、樣本數、PoB／Tree 版本與限制。

## 執行流程

1. **確認輸入。** 取得版本／聯盟、主技能、職業／昇華、SC／HC、Trade／SSF、預算與目標。主技能不可以誤判成位移、Guard、Aura 或觸發技能；若不明確，先提出候選。
2. **取得 Ninja 資料。** 優先使用合法公開 JSON、資料傾印、使用者匯出檔、公開角色資料或 PoB code。建構頁是動態前端，不可依賴靜態 HTML，也不可繞過登入、速率限制或私人角色權限。記錄 URL、時間、schema、篩選條件與樣本數。
3. **正規化並排名。** 每列至少保存 `league`、`patch`、`class`、`ascendancy`、`main_skill`、`level`、`skills`、`items`、`passives`、`keystones` 與來源。排名不可只看 DPS，還要考慮生命／ES、抗性、抑制／格擋、TotalEHP／MaximumHitTaken、成本與轉換難度。
4. **執行 PoB 驗證。** 先執行：

```bash
pob skills BUILD.xml --format json
pob skills BUILD.xml --details --pob-root "$POB_ROOT" --format json
pob tree BUILD.xml --all
pob items BUILD.xml
pob analyze BUILD.xml --pob-root "$POB_ROOT" --skill "主技能" --format json
pob calc BUILD.xml --pob-root "$POB_ROOT" --skill "主技能" --format json
```

若缺少 LuaJIT、PoB root、技能 metadata、相容 XML 或版本不符，保留 stdout／stderr，標示 `blocked` 或 `failed`，不要自行重寫 PoB 公式。

5. **建立三階段。** 初期涵蓋劇情至初入地圖；中期涵蓋穩定黃圖／紅圖；後期涵蓋成熟刷圖、巔峰王或高預算。每一階段必須列出等級範圍、完整技能連線、輔助／防禦技能、天賦路線、裝備目標、屬性／抗性門檻、升級順序、轉換條件、PoB 指標、假設與警告。
6. **產生 JSON 與 code。** 可使用 `scripts/poe1_build_pipeline.py` 保存候選與警告。`pob share BUILD.xml --dry-run` 只產生 code，不得自動上傳。`pobb.in` 是公開內容，必須另行取得明確確認。

## 3.29 推薦範例規則

可以把 `Vortex Occultist`、`Kinetic Fusillade Totems Hierophant`、`Static Strike Slayer` 當作查詢候選，但只有在指定 3.29 快照實際包含它們時才能納入比較。範例名稱不是固定 Tier List；最終推薦必須由 Ninja 快照、使用者限制與 PoB 驗證共同決定。

## 固定輸出

報告依序使用：資料來源與假設、推薦與替代方案、初期配置、中期配置、後期配置、Ninja 證據、PoB 驗證、角色 JSON／code、風險與下一步。清楚區分 Ninja 觀察、官方 PoB 計算、人工建議與未驗證估算。每個 DPS 必須說明敵人、Charges、Flask、Buff、Shock／ailment 與 uptime 假設。

## 資源

`references/api_reference.md` 說明端點與命令；`references/research_notes.md` 保存 3.29 與限制；`scripts/poe1_build_pipeline.py` 負責 JSON 正規化與非上傳式 PoB 分析；`templates/character_build.json` 是輸出範本。英文 [`SKILL.md`](SKILL.md) 是實際載入的預設技能文件。

## 參考資料

[1]: https://www.pathofexile.com/forum/view-thread/3985332 "Content Update 3.29.0 — Path of Exile: Curse of the Allflame"
[2]: https://poe.ninja/poe1/builds "PoE Ninja — Path of Exile 1 Builds"
[3]: https://github.com/qpooqp777/pob-cli "qpooqp777/pob-cli"
