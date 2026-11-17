# 学习娃 Lesson 分块格式

为减少生成 token，Bot 后续只需要写一个很小的个性化 `lesson-block.json`，不要生成完整 HTML/CSS/JS。
Python 脚本负责把分块数据与通用模板合成单文件 H5。

## 最小分块

```json
{
  "input": "我要一个破十法，孩子喜欢交通工具",
  "skillId": "break_ten",
  "themeId": "vehicle",
  "difficulty": "easy",
  "seed": 13,
  "storyOverrides": {
    "character": "小汽车",
    "itemName": "能量格",
    "goal": "过桥",
    "reward": "过桥小能手"
  },
  "copyOverrides": {
    "title": "小汽车过桥学破十法"
  }
}
```

## 字段说明

| 字段 | 是否必填 | 说明 |
|---|---|---|
| `input` | 是 | 用户原始自然语言，用于自动识别 skill/theme |
| `skillId` | 否 | 指定时跳过识别，可选 `break_ten` / `make_ten` / `level_ten` |
| `themeId` | 否 | 指定时跳过识别；只能用 5 个内置主题名 |
| `customTheme` | 否 | 用户点名了非内置兴趣时**必须**写，包含角色、物品、目标、配色 |
| `difficulty` | 否 | 默认 `easy` |
| `seed` | 否 | 用于可复现出题 |
| `numbers` | 否 | 固定题目 `{ "a": 15, "b": 8 }`，不合规会报错 |
| `storyOverrides` | 否 | 覆盖角色、物品、目标、奖励等故事变量 |
| `copyOverrides.title` | 否 | 覆盖标题 |

### 主题字段怎么填（容易出错的一步）

先判断用户有没有**点名主题**（写法：`来个X的` / `换个X` / `喜欢X` / `X主题`）：

| 情况 | 怎么写 |
|------|--------|
| 命中内置主题（交通工具/收集卡片/恐龙/小熊/小菜园） | 填 `themeId` |
| 点名了别的兴趣（足球、金龙鱼、城堡…） | 写 `customTheme` **并自己画 `heroSvg`/`itemSvg`**，不许换成别的主题 |
| 完全没提主题 | 可以都不写，用默认 `vehicle` |

点名了非内置主题却不写 `customTheme` 时，脚本会**直接报错**（退出码 `2`）并给出骨架。
报错是在提醒你**自己动手把这个主题画出来**，不是让你回头问用户或换主题。
不要用 `--allow-default-theme` 去压掉这个报错。

### customTheme 子字段

| 子字段 | 是否必填 | 说明 |
|--------|----------|------|
| `themeId` | 否 | 不给会用 `custom_theme` |
| `themeName` | 是 | 例如「足球」 |
| `character` | 是 | 主角，例如「小球员」 |
| `itemName` | 是 | 被摆的物品，例如「足球」 |
| `removeVerb` | 是 | 减法动词，例如「踢走」 |
| `addVerb` | 是 | 加法动词，例如「加入」 |
| `goal` | 是 | 故事目标，例如「踢进对方球门」 |
| `reward` | 否 | 结尾称号，例如「射门小能手」 |
| `themeCSS` | **是** | 配色变量；不给只能用中性灰，和主题不搭 |
| `visualKind` | 否 | 只在需要全新 SVG 造型时才给，默认 `generic` |

## 生成命令

```bash
python scripts/generate_learnwa.py --block path/to/lesson-block.json --output docs/lesson.html
```

或者直接用自然语言：

```bash
python scripts/generate_learnwa.py "我要一个破十法，孩子喜欢交通工具" --output docs/lesson.html
```

## 设计原则

- Bot 只写个性化分块，不写完整 HTML。
- 通用布局、SVG 角色、物品图形、按钮文案、iPhone SE 适配全部留在模板里。
- 主题不能定死：遇到新兴趣时，Bot 优先写 `customTheme`，让 Python 合成配置。
- **点名了主题就绝不能换成别的主题**：说了足球却生成小汽车，孩子对不上号，属于最严重的错误。
- `customTheme` 必须带 `themeCSS`，否则只能用中性灰配色。
- 若只是换故事、角色、物品和配色，不要改模板；遇到全新造型，**在分块里用 `heroSvg`/`itemSvg` 自己画**，同样不必改模板。
- 严禁在分块中放 emoji。

## 自定义主题示例

```json
{
  "input": "最近小孩对小猫钓鱼感兴趣，来个借十法",
  "skillId": "break_ten",
  "themeId": "custom_cat_fishing",
  "difficulty": "easy",
  "seed": 13,
  "customTheme": {
    "themeId": "custom_cat_fishing",
    "themeName": "小猫钓鱼",
    "visualKind": "cat_fishing",
    "character": "小猫",
    "itemName": "小鱼",
    "removeVerb": "钓走",
    "addVerb": "放进鱼篓",
    "goal": "去河边钓鱼",
    "reward": "钓鱼数学家",
    "themeCSS": {
      "--primary": "#F59E0B",
      "--secondary": "#0F766E",
      "--accent": "#38BDF8",
      "--bg-scene-top": "#DBEAFE",
      "--bg-scene-bottom": "#BAE6FD",
      "--ground-color": "#7DD3FC",
      "--item-color": "#38BDF8",
      "--text-on-item": "#182230",
      "--card-bg": "#F0FDFA"
    }
  },
  "copyOverrides": {
    "title": "小猫钓鱼学借十法"
  }
}
```
