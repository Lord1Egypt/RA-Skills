# PoE1 BD 產生器與驗證器

本技能會針對指定版本或聯盟，產生可重現的《Path of Exile 1》**僅限終局**分析。它使用使用者提供的 PoE Ninja DB 紀錄、公開角色資料，或完整的 PoB character code，固定被動樹、技能、連線、裝備、珠寶與配置來源，再透過 `qpooqp777/pob-cli` 執行 Path of Building Community 計算。主動工作流程不再產生初期或中期配置。

主動技能預設語言為英文。本地化文件請參考 [`README.zh-TW.md`](README.zh-TW.md)、[`README.zh-CN.md`](README.zh-CN.md)、[`SKILL.zh-TW.md`](SKILL.zh-TW.md) 與 [`SKILL.zh-CN.md`](SKILL.zh-CN.md)。

## 儲存庫版本

本儲存庫目前追蹤的發布候選版本為 **0.1.2**，版本來源記錄在 [`VERSION`](VERSION)。在明確發布更新套件之前，ClawHub 仍維持 `0.1.1`；不可將此檔案的版本直接視為 ClawHub registry 版本。

## 功能

產生器可接收聯盟、主技能、職業／昇華、遊戲模式、經濟環境、預算與目標。它會取得或接收合法的 Ninja JSON 快照、篩選候選、解釋排名，並在本機具備 PoB Community 根目錄與 LuaJIT 時驗證選定的 PoB XML。

每個結果都會輸出一筆固定的終局紀錄。匯入的角色資料不會被靜默最佳化或改寫：使用者提供的被動樹、技能、連線、裝備、珠寶與配置保持為權威來源。報告包含來源出處、PoB 指標、防禦門檻、警告與限制；初期與中期配置會刻意省略。

## PoE 3.29 範例

當使用者要求「推薦 PoE1 3.29 BD」時，產生器以 **Curse of the Allflame** 作為人類可讀的聯盟範例，接著核對實際聯盟識別碼並取得帶時間戳的資料快照。不可從影片、搜尋摘要或人氣圖表硬編一個「最強 BD」。

當指定的 3.29 快照確實包含這些候選時，報告可以比較 `Vortex Occultist`、`Kinetic Fusillade Totems Hierophant` 與 `Static Strike Slayer` 等流派家族。這些名稱只是查詢假設，不是預先認證的 Tier List；最終選擇必須反映使用者要求的模式、預算、主技能、防禦期待與 PoB 驗證狀態。

> GGG 官方 3.29.0 公告將挑戰聯盟列為 Curse of the Allflame，並提供 Standard、Hardcore 與 Solo Self-Found 變體。[1]

## 資料與驗證模型

PoE Ninja 被視為統計證據。由於公開建構頁主要由前端動態載入，產生器優先使用合法的 JSON 端點、資料傾印、使用者提供的匯出檔、公開角色資料或 PoB code。它會記錄來源 URL、擷取時間、聯盟、篩選條件、回應 schema 與樣本數，不會繞過驗證、速率限制或私人角色存取控制。

PoB Community 被視為計算權威。產生器先檢查技能、天賦樹與裝備，再以明確指定的主技能執行 `pob analyze` 與 `pob calc`。若缺少 LuaJIT、PoB root 無效、XML 不受支援或計算失敗，流程會輸出警告並標示未驗證，而不是自行捏造數字。

## 終局角色 code 命令

```bash
python scripts/poe1_build_pipeline.py endgame-analyze \
  --pob-code CHARACTER_CODE.txt \
  --pob-root "$POB_ROOT" \
  --skill "Vortex" \
  --class "Witch" \
  --ascendancy "Occultist" \
  --league "Curse of the Allflame" \
  --xml-output endgame_imported.xml \
  --output endgame_report.json
```

此命令會解碼完整的 PoB character code，保留匯入的天賦樹、技能與裝備，並呼叫 `pob analyze` 與 `pob calc`。短的 `https://pobb.in/<id>` 網址不是 character code，會被拒絕；請提供完整 code 或包含完整 code 的文字檔。此命令永遠不會上傳 BD。

若要從既有 XML 產生不公開的 code，請使用：

```bash
pob share BUILD.xml --dry-run
```

公開的 `pobb.in` 連結必須另外取得明確確認。「已產生 code」與「已公開 URL」是不同狀態。

## 可選的被動樹研究工具

`optimize-tree` 子命令仍可用於離線研究與候選比較，但它不會被終局 character-code 工作流程呼叫。主動工作流程絕不會用最佳化器結果取代匯入的天賦樹、技能、連線或裝備。

```bash
python scripts/poe1_build_pipeline.py optimize-tree \
  --pob-root "$POB_ROOT" \
  --tree-version 3_29 \
  --class-id 3 \
  --target-nodes 112 \
  --objective cold-dot \
  --objective energy-shield \
  --objective curse \
  --required-node 32417 \
  --build BASELINE.xml \
  --skill Vortex \
  --output-xml optimized.xml \
  --output-json optimized.json
```

可用的 objective 是 `cold-dot`、`energy-shield`、`life`、`curse`、`spell`、`defence` 與 `damage`。必選節點的連通路徑會計入節點預算。無法連通的必選路徑、斷開的候選或無效的 TreeData 版本都會造成硬性失敗。此命令是以 objective 加權的 frontier search，不是全域最佳解證明；做出最終推薦時，應比較多組 objective。

## 輸出 schema

機器可讀報告包含聯盟、BD 概念、來源 metadata、Ninja 候選、階段紀錄、PoB 驗證狀態、角色 code 狀態與警告。人類可讀報告會分開四類證據：**Ninja 觀察結果**、**官方 PoB 計算**、**人工推薦**與**未驗證估計**。

| 主動紀錄 | 來源 | 決策閘門 |
| --- | --- | --- |
| 僅限終局 | PoE Ninja DB／公開角色資料／完整 PoB character code | 保留匯入的天賦樹、技能、連線與裝備；以 `pob analyze` 和 `pob calc` 驗證。 |

## 內含資源

| 路徑 | 用途 |
| --- | --- |
| `SKILL.md` | Manus 載入的英文主動指令。 |
| `scripts/poe1_build_pipeline.py` | JSON 正規化、非上傳式 PoB 分析包裝器，以及 `optimize-tree` 子命令分派器。 |
| `scripts/poe1_tree_optimizer.py` | 支援必選／排除節點與可選 PoB 計算的連通被動樹最佳化器。 |
| `references/api_reference.md` | API 與 CLI 使用說明。 |
| `references/research_notes.md` | 已驗證的限制與 3.29 研究筆記。 |
| `templates/character_build.json` | 機器可讀的角色／BD 範本。 |

## 參考資料

[1]: https://www.pathofexile.com/forum/view-thread/3985332 "Content Update 3.29.0 — Path of Exile: Curse of the Allflame"
[2]: https://poe.ninja/poe1/builds "PoE Ninja — Path of Exile 1 Builds"
[3]: https://github.com/qpooqp777/pob-cli "qpooqp777/pob-cli"
