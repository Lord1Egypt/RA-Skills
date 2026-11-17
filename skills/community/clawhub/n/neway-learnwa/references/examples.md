# 学习娃 LearnWa · 效果示例库

这一页回答一个问题：**给这样的输入，最后会生成什么样的页面，孩子看到什么。**

三种方法的完整示例都给出：分块 JSON、页面步骤、画面上颜色和动画怎么变、可直接复制的命令。

---

## 示例一：破十法 · 15 - 8（能量格主题）

### 输入

孩子要算 `15 - 8`，用「破十法」讲。

### 分块

```json
{
  "input": "破十法",
  "skillId": "break_ten",
  "themeId": "vehicle",
  "numbers": { "a": 15, "b": 8 }
}
```

### 命令

```bash
python scripts/generate_learnwa.py --block lesson-block.json --output docs/lesson.html
```

### 页面步骤

| 步 | 孩子看到 | 家长说 | 画面怎么变 |
|----|----------|--------|-----------|
| 1 | `15 - 8` | 小汽车有 15 个能量格，要过桥用掉 8 个，还剩多少？ | 第一排 10 个 + 第二排 5 个，全部绿色框 |
| 2 | `15 = 5 + 10` | 破十法先把 15 拆成 5 和 10 | 两排用不同颜色区分“个位组”和“十组” |
| 3 | `10 - 8 = ?` | 第一排摆 10 个，第二排摆 5 个。第二排不动，只从第一排 10 个里用掉 8 个。 | **不立刻变**。点“第一排拿走”后，第一排才灰掉 8 个；按钮随即变成“两排合起来” |
| 4 | `2 + 5 = ?` | 第一排还剩 2 个，第二排 5 个一直没动。2 加 5 等于几？ | 已灰掉的不再动；按钮变成“说出答案” |
| 5 | `15 - 8 = 7` | 第一排 10 减 8 剩 2，第二排 5 不变，2 加 5 等于 7 | 撒花 + “没关系，再摆一次” |

### 关键点

- 第二排 5 个**全程不动**，这是破十法最容易讲错的地方。
- `10 - 8 = ?` 这一步不提前灰掉，必须先提问、后动作。

---

## 示例二：平十法 · 15 - 8（能量格主题）

### 输入

同一个算式，改用「平十法」讲。

### 分块

```json
{
  "input": "平十法",
  "skillId": "level_ten",
  "themeId": "vehicle",
  "numbers": { "a": 15, "b": 8 }
}
```

### 页面步骤

| 步 | 孩子看到 | 家长说 | 画面怎么变 |
|----|----------|--------|-----------|
| 1 | `15 - 8` | 有 15 个能量格，要用掉 8 个 | 15 个全部绿色框（表示它们属于同一个被减数） |
| 2 | `8 = 5 + 3` | 为了先把 15 减到 10，要先减 5。把 8 分成 5 和几？ | 点“开始摆出来”后才分色：第二排 5 个变红框，第一排最后 3 个也变红框，红框合计 8 个 |
| 3 | `15 - 5 = 10` | 先减掉第二排那 5 个，15 减 5 等于几？ | 第二排 5 个红框先灰掉 |
| 4 | `10 - 3 = ?` | 8 里面还剩 3 个没减，从 10 里再减 3 | 第一排最后 3 个红框再灰掉 |
| 5 | `15 - 8 = 7` | 先减 5 到 10，再从 10 减 3，所以等于 7 | 撒花 + “没关系，再摆一次” |

### 关键点

- **初始不分色**，点“开始摆出来”才分色。
- 红框只能标“要减掉的 8 个”：第二排 5 个 + 第一排最后 3 个；第一排前面的 7 个绝不能标红。
- 先灰第二排，再灰第一排最后 3 个，顺序反了就是教错。

---

## 示例三：凑十法 · 8 + 7（能量格主题）

### 输入

孩子要算 `8 + 7`，用「凑十法」讲。

### 分块

```json
{
  "input": "凑十法",
  "skillId": "make_ten",
  "themeId": "vehicle",
  "numbers": { "a": 8, "b": 7 }
}
```

### 页面步骤

| 步 | 孩子看到 | 家长说 | 画面怎么变 |
|----|----------|--------|-----------|
| 1 | `8 + 7` | 先有 8 个能量格，又加入 7 个，一共多少？ | 8 个一组 + 7 个一组 |
| 2 | `8 + ? = 10` | 8 还差几就能凑成 10？ | 高亮 8 和 10 之间的空缺 |
| 3 | `7 = 2 + 5` | 把 7 分成 2 和几？ | 第二个加数 7 整体红框，可看出要拆成 2 和 5 |
| 4 | `8 + 2 = 10` | 先拿 2 个过来把 8 凑成 10 | 红框里前 2 个补到 10 的位置 |
| 5 | `10 + 5 = ?` | 还有 5 个没加，10 加 5 等于几？ | 剩下 5 个红框加入 |
| 6 | `8 + 7 = 15` | 先凑 10，再加剩下的 5，所以等于 15 | 撒花 + “没关系，再摆一次” |

### 关键点

- 第二个加数（7）要**整体同色**，红框合计正好 7 个，孩子才看得出 `7 = 2 + 5`。
- 凑十法只用于“和大于 10”的加法；`8 + 1` 这种不适用。

---

## 示例四：自定义主题 · 小猫钓鱼（借十法）

内置主题不够用时，**现场创建主题**，不要硬套。

### 分块

```json
{
  "input": "孩子最近迷上小猫钓鱼，来个借十法",
  "skillId": "break_ten",
  "numbers": { "a": 15, "b": 8 },
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
  }
}
```

注意：借十法填 `break_ten`，不要新造 skillId。

---

## 示例五：自定义主题 · 足球（平十法）

这是**最容易做错**的一种输入：用户点名了主题，但它不在内置列表里。

### 输入

「**来个足球的**，讲平十法」

### 分块

```json
{
  "input": "来个足球的，讲平十法",
  "skillId": "level_ten",
  "numbers": { "a": 15, "b": 8 },
  "customTheme": {
    "themeId": "custom_soccer",
    "themeName": "足球",
    "character": "小球员",
    "itemName": "足球",
    "removeVerb": "踢走",
    "addVerb": "加入",
    "goal": "踢进对方球门",
    "reward": "射门小能手",
    "themeCSS": {
      "--primary": "#16A34A",
      "--secondary": "#064E3B",
      "--accent": "#FACC15",
      "--bg-scene-top": "#DCFCE7",
      "--bg-scene-bottom": "#BBF7D0",
      "--ground-color": "#4ADE80",
      "--item-color": "#FFFFFF",
      "--text-on-item": "#0F172A",
      "--card-bg": "#F0FDF4"
    },
    "heroSvg": "<svg viewBox=\"0 0 120 100\" aria-hidden=\"true\"><circle cx=\"60\" cy=\"24\" r=\"14\" fill=\"{{secondary}}\"/><rect x=\"40\" y=\"40\" width=\"40\" height=\"34\" rx=\"12\" fill=\"{{primary}}\"/><path d=\"M40 50 22 64M80 50l18 14\" stroke=\"{{primary}}\" stroke-width=\"10\" stroke-linecap=\"round\"/><path d=\"M50 72 44 90M70 72l6 18\" stroke=\"{{secondary}}\" stroke-width=\"10\" stroke-linecap=\"round\"/><path d=\"M52 44c5 6 11 6 16 0\" stroke=\"#fff\" stroke-width=\"3\" stroke-linecap=\"round\" fill=\"none\"/></svg>",
    "itemSvg": "<svg viewBox=\"0 0 40 40\"><circle cx=\"20\" cy=\"20\" r=\"16\" fill=\"#fff\" stroke=\"{{secondary}}\" stroke-width=\"2.5\"/><path d=\"M20 10 26 15 24 22h-8l-2-7z\" fill=\"{{secondary}}\"/><path d=\"M20 4v6M34 15h-7M28 32l-4-10M12 32l4-10M6 15h7\" stroke=\"{{secondary}}\" stroke-width=\"2\"/></svg>"
  }
}
```

### 页面步骤

数学步骤和示例二完全一致，只是故事与配色换成了足球：

| 步 | 孩子看到 | 家长说 | 画面怎么变 |
|----|----------|--------|-----------|
| 1 | `15 - 8` | 小球员有 15 个足球，要踢走 8 个 | 草地绿场景，15 个球全部绿框 |
| 2 | `8 = 5 + 3` | 为了先把 15 减到 10，要先踢走 5 个，把 8 分成 5 和几？ | 点“开始摆出来”后分色：第二排 5 个红框 + 第一排最后 3 个红框，合计 8 个 |
| 3 | `15 - 5 = 10` | 先踢走那 5 个，15 减 5 等于几？ | 第二排 5 个红框先灰掉 |
| 4 | `10 - 3 = ?` | 还剩 3 个没踢走，从 10 里再踢 3 个 | 第一排最后 3 个红框再灰掉 |
| 5 | `15 - 8 = 7` | 先减 5 到 10，再从 10 减 3，所以等于 7 | 撒花 +“没关系，再摆一次” |

### 关键点

- **不能套 `vehicle`**：说了足球却出现小汽车，孩子完全对不上号。
- 直接跑脚本 `python scripts/generate_learnwa.py "来个足球的"` 会**报错**（退出码 2）并要求写 `customTheme`，这是刻意设计的保护。
- `themeCSS` 必须给全，否则只能用中性灰，和足球不搭。
- **必须自画 `heroSvg`/`itemSvg`**：内置造型里没有足球；不给就只能退回通用造型，孩子认不出。

---

## 示例六：自定义主题 · 金龙鱼（平十法，自己画 SVG）

「**来个金龙鱼的**」这种最典型：**内置主题完全命中不了**。此时正确姿态不是报错停下，而是**自己把金龙鱼画出来**，一步到位。

### 输入

「来个金龙鱼的，讲平十法」

### 分块

```json
{
  "input": "来个金龙鱼的，讲平十法",
  "skillId": "level_ten",
  "numbers": { "a": 15, "b": 8 },
  "customTheme": {
    "themeId": "custom_arowana",
    "themeName": "金龙鱼",
    "character": "金龙鱼",
    "itemName": "金鳞片",
    "removeVerb": "掉下",
    "addVerb": "贴上",
    "goal": "游过龙门",
    "reward": "跃龙门小能手",
    "themeCSS": {
      "--primary": "#F5B301",
      "--secondary": "#B45309",
      "--accent": "#EF4444",
      "--bg-scene-top": "#FEF3C7",
      "--bg-scene-bottom": "#FDE68A",
      "--ground-color": "#F59E0B",
      "--item-color": "#FBBF24",
      "--text-on-item": "#7C2D12",
      "--card-bg": "#FFFBEB"
    },
    "heroSvg": "<svg viewBox=\"0 0 120 100\" aria-hidden=\"true\"><path d=\"M20 58c14-16 40-24 62-18 10 3 18 9 22 16-6 9-16 15-28 17-22 4-44-2-56-15Z\" fill=\"{{primary}}\" stroke=\"{{secondary}}\" stroke-width=\"4\" stroke-linejoin=\"round\"/><path d=\"M14 58 36 44M14 58 36 72\" stroke=\"{{secondary}}\" stroke-width=\"7\" stroke-linecap=\"round\"/><path d=\"M52 34c8-10 20-14 30-10\" stroke=\"{{accent}}\" stroke-width=\"6\" stroke-linecap=\"round\" fill=\"none\"/><circle cx=\"92\" cy=\"54\" r=\"5\" fill=\"#182230\"/><path d=\"M104 60c6 2 8 6 8 10M104 60c-2 6-1 10 2 13\" stroke=\"{{accent}}\" stroke-width=\"3\" stroke-linecap=\"round\" fill=\"none\"/><path d=\"M46 58c8-5 16-5 24 0M52 66c8-5 16-5 24 0\" stroke=\"#fff\" stroke-width=\"3\" stroke-linecap=\"round\" opacity=\".7\" fill=\"none\"/></svg>",
    "itemSvg": "<svg viewBox=\"0 0 40 40\"><path d=\"M8 20c8-9 17-9 25 0-8 9-17 9-25 0Z\" fill=\"{{item}}\" stroke=\"{{secondary}}\" stroke-width=\"2.5\"/><path d=\"M8 20 2 14M8 20 2 26\" stroke=\"{{secondary}}\" stroke-width=\"2.5\" stroke-linecap=\"round\"/><circle cx=\"26\" cy=\"19\" r=\"2\" fill=\"#182230\"/></svg>"
  },
  "copyOverrides": { "title": "金龙鱼游龙门学平十法" }
}
```

### 命令

```bash
python scripts/generate_learnwa.py --block lesson-block.json --output docs/arowana.html
```

### 关键点

- **报错不是终点**：脚本报「金龙鱼」不是内置主题，是在提醒你**自己动手**。正确响应是直接给 `customTheme` + 自画 SVG，而不是回头问用户「要不要用汽车主题」。
- **自画 SVG 三条硬规则**：`heroSvg` 用 `viewBox="0 0 120 100"`；`itemSvg` 用 `viewBox="0 0 40 40"`；颜色一律用 `{{primary}}`/`{{accent}}`/`{{item}}` 占位符，别写死色值。
- **纯静态内联**：不许 `<script>`、`on*` 事件、`javascript:` 或外链，脚本会剔除并提示。
- 抓特征即可：长身 + 大鳞 + 金红配色 + 嘴边须，孩子一眼就认得出是金龙鱼。

---

## 需求 → 分块写法对照表

**先判断用户有没有「点名主题」**（`来个X的` / `换个X` / `喜欢X` / `X主题`）；点名了就必须落到 `themeId` 或 `customTheme`，不允许换成别的主题。

| 家长的话 | skillId | 主题处理 |
|----------|---------|----------|
| 破十法 / 借十法 / 退位减法 | `break_ten` | 按兴趣 |
| 凑十法 / 凑成 10 / 进位加 | `make_ten` | 按兴趣 |
| 平十法 / 减到 10 再继续减 | `level_ten` | 按兴趣 |
| 孩子喜欢飞机 / 火车 / 汽车 | 按方法 | `themeId: "vehicle"` |
| 孩子喜欢收集卡片 | 按方法 | `themeId: "card_collection"` |
| 孩子喜欢恐龙 | 按方法 | `themeId: "dinosaur"` |
| 孩子喜欢小熊 / 蜂蜜 | 按方法 | `themeId: "animal_bear"` |
| 孩子喜欢种菜 / 小菜园 | 按方法 | `themeId: "vegetable_garden"` |
| **来个足球的** / 小猫钓鱼 / 城堡 / 超市 / 海洋 / 公主 | 按方法 | **必须 `customTheme` 现场创建**（见示例五） |
| 只说「来个破十法」，没提主题 | 按方法 | 才允许默认 `vehicle` |

---

## 快速试一遍

```bash
# 看有哪些方法和主题
python scripts/generate_learnwa.py --list

# 一句话生成（不给分块），没提主题 → 默认交通工具
python scripts/generate_learnwa.py "我要一个破十法，孩子喜欢飞机"

# 点名了非内置主题 → 会报错并要求写 customTheme（这是提醒你自画 SVG，不是 bug）
python scripts/generate_learnwa.py "来个足球的"

# 用分块生成，并指定输出路径
python scripts/generate_learnwa.py --block lesson-block.json --output docs/lesson.html
```

想看完整效果时，直接照抄本文上面任一分块 JSON，跑一次生成命令即可得到对应页面（输出路径自己指定，建议放在工作区 `docs/`）：

```bash
python scripts/generate_learnwa.py --block lesson-block.json --output docs/lesson.html
```

本文 4 个完整示例分别对应：破十法 `15 - 8`、平十法 `15 - 8`、凑十法 `8 + 7`、自定义主题（小猫钓鱼 / 足球 / 金龙鱼）。

> 工作区 `docs/` 只保留当前成品；历史迭代版本不再留存，需要对照旧效果时从 `.temp/neway-learnwa-docs-backup-20260919/` 取。
