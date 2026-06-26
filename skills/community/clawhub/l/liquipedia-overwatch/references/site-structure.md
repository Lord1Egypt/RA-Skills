# Liquipedia Overwatch 站点结构参考

## 通用 URL 格式

```
https://liquipedia.net/overwatch/
```

## 主要分类页面

| 分类 | URL | 说明 |
|------|-----|------|
| 首页 | `/overwatch/` | 展示最新新闻和赛事 |
| 战队 | `/overwatch/Category:Teams` | 所有战队列表 |
| 选手 | `/overwatch/Category:Players` | 所有选手列表 |
| 赛事 | `/overwatch/Tournaments` | 赛事索引页 |
| 新闻 | `/overwatch/News` | 最新新闻 |

## OWL 赛季页面命名

OWL 历史上各赛季对应 URL：
- OWL 2023（Season 7）：`/overwatch/Overwatch_League/Season_7`
- OWL 2024（Season 8）：`/overwatch/Overwatch_League/Season_8`
- OWL 2025（Season 9）：`/overwatch/Overwatch_League/Season_9`

OWL 子页面：
- 常规赛：`/Season_X/Regular_Season`
- 季后赛：`/Season_X/Playoffs`
- 升降赛：`/Season_X/Play-In`
- 总决赛：`/Season_X/Grand_Finals`

## 战队页面

战队页面 URL 直接以战队名称为 slug：
```
/overwatch/Team_Name
```
示例：`/overwatch/Seoul_Dynasty`、`/overwatch/Shanghai_Dragons`

战队页面通常包含：
- 战队简介（成立日期、所属地区）
- 阵容名单（选手 ID、真名、位置）
- 历届赛季成绩
- 荣誉墙（冠军/亚军/季军）

## 选手页面

选手页面 URL 格式：
```
/overwatch/Player:PlayerName
```
或直接：`/overwatch/PlayerName`

选手页面通常包含：
- 基本信息（真名、出生日期、国籍）
- 生涯数据（K/D、Ace%、登场次数）
- 所属战队历史
- 擅长英雄

## 赛程页面

赛程列表页：`/overwatch/Match_List`

具体赛事页：`/overwatch/Tournament_Name`

赛事页面通常包含：
- 赛事信息（时间、地点、奖金池）
- 小组赛/淘汰赛赛程
- 每场比赛结果
- 最终排名

## 抓取技巧

### 提取表格数据
Liquipedia 的排名表、赛程表均为 HTML `<table>`，抓取后解析 td/th 内容即可。

### 提取 Infobox
战队和选手页面右侧有 Infobox（信息框），包含关键结构化数据，优先提取。

### 新闻页面
新闻页面列表：`/overwatch/News`
每条新闻详情：`/overwatch/News/YYYY/News_Title`

### 搜索
如找不到具体页面，可尝试：
```
https://liquipedia.net/overwatch/api.php?action=opensearch&search={关键词}
```
或直接用通用搜索 URL：
```
https://liquipedia.net/overwatch/Special:Search?search={关键词}
```

## 常见问题

**Q：页面找不到怎么办？**
A： Liquipedia 的 slug 有时会因为名称变更/空格处理而不同，建议搜索或从分类页切入。

**Q：内容太多太杂怎么办？**
A： 聚焦用户查询意图，只提取相关段落，不需要全文。

**Q：需要登录吗？**
A： Liquipedia 为公开页面，不需要登录。
