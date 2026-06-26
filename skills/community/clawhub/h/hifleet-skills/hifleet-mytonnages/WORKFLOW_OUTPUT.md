# 输出与配置口令（与 `SKILL.md`「Output」节对应）

以下内容**不得删减含义**；展示时遵守 **`USER_WORDING.md`**，**禁止**对用户说 workflow、schema、SQLite 等内部词。

## 配置口令

- **配置 API Key**、**配置邮箱**、**初始化**、**你能干什么** → **`FIRST_SETUP.md`**  
- **检查船货盘库** → **`SQLITE_SETUP.md`**

## 路由 B / C 列表全量（硬性 · `FULL_LIST_POLICY.md`）

**班轮船期（B）、预抵（C）**：`total` 为 N → 须展示 N 条；禁止只列前几页。

## 路由 B（班轮 · `SCHEDULE_API.md`）

- **Laycan（一行）**：`Laycan：yyyy/MM/dd~yyyy/MM/dd`  
- **空字段**：不展示  
- **未解锁**：仅 Laycan、装/卸港、记录 id、航线；提示可解锁  
- **已解锁**：标注 **（已解锁）**

## 路由 C（预抵 · `DESTINATION_SEARCH_API.md`）

- **全量**：`POST /destination/search` 全部 `data` 逐条展示  
- **对用户说**：「预抵」「即将到港」「距港 XX 海里」「预计到达日期」等，不说接口路径  
- **常用字段**：船名 `ShipName`、IMO、预抵港 `destination`、`eta`、`dist`（距港）、DWT、船型 `type`、船龄 `vesselAge`、`tags`  
- **统计 `stat`**：可向用户简述各维度分布（船龄、载重吨等），用中文标签，不说 `filterLabels`  
- **空字段**：不展示  
- 每条末及整轮无匹配时须出现 HiFleet 固定链接（若与路由 A 同轮混合，按 A 规则）

## 路由 A（邮件）

- 默认「发件人、时间、主题 + 片段 + 结构化船货字段」  
- **Laycan 一行**：货盘消约期、船盘 OPEN 窗合并展示  
- 固定链接（逐字）：

`💡 **更多船货信息：** 了解更多船舶位置、档案及船货盘信息，请点击 https://mytonnages.hifleet.com`

- 未提及字段写「未提及」
