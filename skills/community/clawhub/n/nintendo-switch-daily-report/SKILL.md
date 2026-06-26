# Nintendo Switch 游戏日报

自动抓取任天堂官方资讯，生成 Nintendo Switch 游戏日报。

## 触发关键词

用户可通过以下方式触发此技能：
- "Nintendo Switch 日报"
- "NS 日报"
- "Switch 日报"
- "任天堂日报"
- 直接请求"帮我做 Switch 日报"

## 功能概述

1. **游戏新闻**：游戏发布、DLC、活动、联动内容等
2. **近期新作**：未来一周内发售的新游戏列表
3. **主机消息**：系统更新公告

## 信息来源

| 来源 | 网址 | 可访问性 |
|------|------|---------|
| 任天堂（香港）TOPICS | nintendo.com.hk/hk/topics | ✅ 正常 |
| 任天堂（香港）发售日程 | nintendo.com.hk/hk/schedule/ | ✅ 正常 |
| 任天堂（香港）eShop | ec.nintendo.com/HK/zh/titles/ | ✅ 正常 |
| 任天堂（台湾）TOPICS | nintendo.com.tw/topics/ | ✅ 正常 |
| 任天堂（台湾）软件一览 | nintendo.com.tw/tw/software/switch/ | ✅ 正常 |
| 任天堂（日本）| nintendo.co.jp | ⚠️ 经常 404 |
| 巴哈 GNN 新闻 NS/NS2 区 | gnn.gamer.com.tw | ⚠️ 经常无法访问 |

**注意**：若任天堂日本、巴哈 GNN 无法访问，日报中注明"当日无法存取，以任天堂香港及台湾来源补充"。

## 搜索时间范围

- 默认抓取**前36小时内**的资讯
- 近期新作表格仅收录**未来一周**（当天起算+7天）发售的游戏

## 日报格式（三段式）

### 标题
```
# 🎮 Nintendo Switch 游戏日报
**YYYY年MM月DD日（星期X）**
```

### 第一部分：游戏新闻（含新作 & DLC）
每条格式：
```
X. **游戏名称** 简介
   [來源：站点名称](超链接)
```

**收录标准：**
- 近期36小时内的游戏发布/发售消息
- DLC 扩展内容（**必须有才列**，无则注明"无"）
- 游戏内活动/祭典/联动
- App 服务更新（如 Nintendo Music 音乐内容更新）
- 限时体验活动

**整合规则：**
- 同一游戏的所有信息整合为1条
- 不同来源的相同信息合并叙述

### 第二部分：未来一周 eShop 新作
以表格呈现，包含：发售日、游戏名称、厂商、来源链接

**收录标准：**
- 发售日在「今天 + 7天」范围内的游戏
- 每条游戏名称后附超链接来源

### 第三部分：主机消息
- 仅收录前36小时内的**系统更新公告**
- 无更新时注明"当日无主机系统更新公告"

### 补充说明（如有）
- 标注"某来源当日无法存取"的情况
- eShop 优惠信息（无则注明"暂无"）

## 游戏名称翻译规则

**优先使用香港任天堂官方译名**，参考来源：
- nintendo.com.hk 的软件页面
- ec.nintendo.com 的游戏页面标题

**常见译名对照：**
| 英文/日文 | 香港译名 |
|-----------|---------|
| Pokémon Champions | 寶可夢 Champions |
| Tomodachi Life | Tomodachi Life 朋友收集 夢想生活 |
| Xenoblade X | 異度神劍 X |
| Goat Simulator 3 | 模擬山羊 3 |
| Demon Castle Story | 魔王城物語 |
| People of Note | 樂土之人 |
| Minecraft | Minecraft |
| Content Warning | Content Warning |
| Dosa Divas | Dosa Divas |

## 每条消息来源写法

**格式**：`[來源：站点名称](完整URL)`

**示例：**
- `[來源：任天堂（香港）TOPICS](https://www.nintendo.com.hk/hk/topics/article/xxx)`
- `[來源：任天堂（台灣）eShop](https://ec.nintendo.com/HK/zh/titles/70010000094614)`
- `[來源：任天堂（台灣）軟體一覽](https://www.nintendo.com.tw/tw/software/switch/)`

## 输出语言

- **全部中文**（正文、标题、备注均为中文）
- 游戏名称采用香港任天堂官方译名

## 执行流程

1. 并行抓取以下来源：
   - `nintendo.com.hk/hk/topics`（任天堂香港 TOPICS）
   - `nintendo.com.tw/topics/`（任天堂台湾 TOPICS）
   - `nintendo.com.tw/tw/software/switch/`（任天堂台湾软件一览）
   - `nintendo.com.hk/hk/schedule/`（任天堂香港发售日程）
   - 尝试访问任天堂日本、巴哈 GNN（失败则跳过）

2. 筛选36小时内（今天 00:00 前推36小时）的资讯

3. 识别并整合：
   - 游戏新闻（新作、活动、DLC、App更新）
   - 未来一周发售游戏
   - 系统更新

4. 按三段式格式输出，每条附来源超链接

## 注意事项

- DLC 消息**必须有实质内容**，空洞描述（如"带来新内容"）需补充具体信息
- 系统更新若无36小时内新公告，**直接省略该部分**
- 若两个来源信息重复，以任天堂香港为准，注明合并
- 游戏新闻每条不超过3句话，聚焦核心资讯
