---
name: neway-learnwa
display_name: "学习娃 LearnWa"
display_name_en: "LearnWa"
description: 学习娃 LearnWa — AI 数学互动教具生成器。当用户提到「学习娃」「LearnWa」「破十法」「借十法」「凑十法」「平十法」「生成数学教具」「给孩子做数学题」「数学教学H5」「一年级数学」「20以内加减法」，或需要生成家长控制型小学数学互动教学页面时使用。生成单文件 HTML 教具，支持 3 种数学方法 × 5 个内置主题，命中不了内置主题时由 Bot 现场创建 customTheme 并自画 SVG 造型，家长操作、孩子观察回答。
description_zh: "学习娃 LearnWa — 一句话生成孩子爱看的数学教具，把破十法、平十法、凑十法讲清楚"
description_en: "LearnWa — turn one sentence into an interactive, parent-guided math teaching page for kids (make-ten / break-ten / level-ten)."
version: 1.0.1
author: Neway Lau
agent_created: true
---

# 学习娃 LearnWa — AI 数学教具生成器

把家长的一句话，变成一份**家长控制型**的单文件 H5 数学教具。

---

## 30 秒上手

1. **定方法**：破十法/借十法 → `break_ten`；平十法 → `level_ten`；凑十法 → `make_ten`
2. **定主题**：说到的兴趣命中内置主题就直接填；**只要用户点名了别的兴趣，就必须写 `customTheme` 现场创建，绝不能换成默认主题**（见下方「主题判定」）
3. **只写一个小的分块 JSON**，交给脚本合成，**不要手写 HTML/CSS/JS**：

```bash
python scripts/generate_learnwa.py --block lesson-block.json --output docs/lesson.html
```

最小分块（更完整的字段见 `references/lesson-block-format.md`）：

```json
{
  "input": "孩子喜欢飞机，来个平十法",
  "skillId": "level_ten",
  "themeId": "vehicle",
  "numbers": { "a": 15, "b": 8 }
}
```

生成后先 `preview_url` 预览，再 `deliver_attachments` 交付。

---

## 触发与澄清

- 只有出现明确的方法词（破十法/借十法/凑十法/平十法）才动手生成；随口提到的数学词不要抢跑。
- 方法不明确时，先问一句「这次想讲破十法、平十法，还是凑十法？」，不要默认硬猜。
- **主题必须按「主题判定」走**：点名了兴趣就用 `customTheme` 实现，不要用默认主题顶替。
- 只有**完全没提**主题时（例如只说「来个破十法」），才允许用默认 `vehicle`。

---

## 三种方法怎么选

| 方法 | skillId | 适用题型 | 硬条件 | 步骤一句话 |
|------|---------|----------|--------|-----------|
| 破十法 / 借十法 | `break_ten` | 20 以内退位减法 | a 11–19，b 2–9，且 **b > a 的个位** | 拆成 `ones + 10`，先算 `10 - b`，再把 `ones` 加回来 |
| 平十法 | `level_ten` | 20 以内退位减法 | 同破十法 | 先拆 b，先减到 10，再减剩下的 |
| 凑十法 | `make_ten` | 20 以内进位加法 | a 6–9，b 2–9，且 **a + b > 10** | 先凑成 10，再加剩下的 |

- 「借十法」填 `break_ten`：两者逻辑一致，破十法专攻 20 以内退位减法，借十法常用于 100 以内或更多位数。
- 题目不合规时脚本会明确报错并给建议，**不要绕过报错自己改步骤**。

详细算式、变量与逐步骤模板 → `references/math-rules.md`

---

## 主题判定（最容易出错，先判清楚再生成）

内置主题只有 5 个：

| 内置 themeId | 主题 |
|--------------|------|
| `vehicle` | 交通工具（汽车/火车/飞机） |
| `card_collection` | 收集卡片 |
| `dinosaur` | 恐龙 |
| `animal_bear` | 小熊 |
| `vegetable_garden` | 小菜园 |

用户的主题要求分三种情况，处理方式完全不同：

| 情况 | 例子 | 正确处理 |
|------|------|----------|
| ① 明确说到内置主题 | 「孩子喜欢恐龙」「喜欢收集卡片」 | 填对应内置 `themeId` |
| ② **点名了具体兴趣，但不在内置主题里** | 「**来个足球的**」「**来个金龙鱼的**」「孩子迷上小猫钓鱼」 | **必须写 `customTheme` 现场创建，并且自己画 SVG 造型**，禁止换成别的主题 |
| ③ 完全没提主题 | 「来个破十法」 | 才可以用默认 `vehicle` |

**什么算「点名了主题」**（出现以下写法就算）：

`来个X的` / `来个X` / `换个X` / `换成X` / `用X` / `孩子喜欢X` / `迷上X` / `X主题`

### 硬规则：点名了主题，就绝不能换成别的主题

用户说「来个足球的」，你生成「小汽车过桥学破十法」，这是**本技能最严重的一类错误**：
孩子对不上号，兴趣点直接消失，家长还会以为工具坏了。

脚本已加保护：识别到「点名了主题但不是内置主题」时会直接报错（退出码 `2`），并给出可复制的 `customTheme` 骨架。
**不要用 `--allow-default-theme` 绕过**——除非用户自己明确说「就用默认交通工具」。

### 关键：报错不是终点，你要自己把这个主题画出来

脚本报「它不是内置主题」，**不是让你回头问用户，也不是让你换主题**，而是提醒你：这次必须自己动手，**一步到位**。
在分块里同时给出三样东西：

1. `customTheme` 的故事字段（主题名、主角、物品、动词、目标）
2. `themeCSS` 配色
3. **`heroSvg`（主角造型）+ `itemSvg`（被摆的物品造型）** —— 由你自己写内联 SVG

模板内置造型只有 5 个主题。命中不了又不给 `heroSvg/itemSvg` 时，页面只能退化成通用造型，
孩子看到的就不是他熟悉的那个东西 —— 这等于白点名了。**能点名，就要能画出来。**

### 自画 SVG 的三条硬规则

1. **尺寸固定**：主角 `heroSvg` 用 `viewBox="0 0 120 100"`；物品 `itemSvg` 用 `viewBox="0 0 40 40"`（会被逐个复制成 N 个）。
2. **颜色用占位符**，不要写死色值，这样配色改 `themeCSS` 就能联动：
   `{{primary}}` `{{secondary}}` `{{accent}}` `{{item}}` `{{text}}`（分别对应 `--primary` `--secondary` `--accent` `--item-color` `--text-on-item`）。
3. **纯静态内联 SVG**：不许 `<script>`、不许 `on*` 事件、不许 `javascript:`、不许外链 —— 脚本会自动剔除并提示。

写实不要求：抓最认得出的 1–2 个特征即可（金龙鱼 → 长身+大鳞+金红配色+嘴边须；足球 → 白底+黑色五边形）。

### 例子：用户说「来个金龙鱼」

这是"命中不了内置主题"的标准处理 —— 自己把金龙鱼画出来，而不是报错停下：

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
      "--item-color": "#FBBF24",
      "--text-on-item": "#7C2D12"
    },
    "heroSvg": "<svg viewBox=\"0 0 120 100\" aria-hidden=\"true\"><path d=\"M20 58c14-16 40-24 62-18 10 3 18 9 22 16-6 9-16 15-28 17-22 4-44-2-56-15Z\" fill=\"{{primary}}\" stroke=\"{{secondary}}\" stroke-width=\"4\" stroke-linejoin=\"round\"/><path d=\"M14 58 36 44M14 58 36 72\" stroke=\"{{secondary}}\" stroke-width=\"7\" stroke-linecap=\"round\"/><path d=\"M52 34c8-10 20-14 30-10\" stroke=\"{{accent}}\" stroke-width=\"6\" stroke-linecap=\"round\" fill=\"none\"/><circle cx=\"92\" cy=\"54\" r=\"5\" fill=\"#182230\"/><path d=\"M104 60c6 2 8 6 8 10M104 60c-2 6-1 10 2 13\" stroke=\"{{accent}}\" stroke-width=\"3\" stroke-linecap=\"round\" fill=\"none\"/><path d=\"M46 58c8-5 16-5 24 0M52 66c8-5 16-5 24 0\" stroke=\"#fff\" stroke-width=\"3\" stroke-linecap=\"round\" opacity=\".7\" fill=\"none\"/></svg>",
    "itemSvg": "<svg viewBox=\"0 0 40 40\"><path d=\"M8 20c8-9 17-9 25 0-8 9-17 9-25 0Z\" fill=\"{{item}}\" stroke=\"{{secondary}}\" stroke-width=\"2.5\"/><path d=\"M8 20 2 14M8 20 2 26\" stroke=\"{{secondary}}\" stroke-width=\"2.5\" stroke-linecap=\"round\"/><circle cx=\"26\" cy=\"19\" r=\"2\" fill=\"#182230\"/></svg>"
  }
}
```

### customTheme 必须写全

缺字段就会退化成没有个性的大路货，家长一眼能看出来。

| 字段 | 必填 | 说明 |
|------|------|------|
| `themeName` | 是 | 主题名，例如「足球」 |
| `character` | 是 | 主角，例如「小球员」 |
| `itemName` | 是 | 被摆的物品，例如「足球」 |
| `removeVerb` | 是 | 减法动词，例如「踢走」 |
| `addVerb` | 是 | 加法动词，例如「加入」 |
| `goal` | 是 | 故事目标，例如「踢进对方球门」 |
| `themeCSS` | **是** | 配色变量，见下 |
| `heroSvg` | **强烈建议** | 主角造型，`viewBox="0 0 120 100"`，颜色用 `{{primary}}` 等占位符 |
| `itemSvg` | **强烈建议** | 物品造型，`viewBox="0 0 40 40"`；不给就退回通用方块，孩子认不出 |
| `visualKind` | 否 | 只有希望复用模板某个内置造型时才给，默认 `generic` |

**`themeCSS` 不能省**：不给的话脚本只能用中性灰，孩子看到的颜色和「足球」完全不搭（这是之前的隐藏坑，脚本现在会提示）。至少给 `--primary`、`--item-color`、`--text-on-item`；也可以只写 `primaryColor` 简写，但推荐写全。

### 例子：用户说「来个足球的」

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

**错误做法**：把「足球」套进 `vehicle`，生成「小汽车过桥学平十法」。

更多字段说明 → `references/lesson-block-format.md`；完整对照示例 → `references/examples.md`

---

## 硬规范（必须遵守）

### 视觉与交互

1. **单文件 HTML**，CSS/JS/SVG 全部内联，禁止外部 CDN。
2. **严禁 emoji**：角色、物品、按钮、撒花一律用内联 SVG 或 CSS 绘制。
3. **禁止渐变按钮和模板化措辞**：按钮必须写当前动作（“开始摆出来”“第一排拿走”“说出答案”），不要写“下一步”。
4. **兼容 iPhone SE**（320×568、375×667）：按钮不低于 44px，首屏要同时看到孩子区、家长说和按钮。
5. 一屏只放一个数学动作；孩子区文字要少，动画要慢。
6. 家长控制：**家长操作按钮，孩子观察和口答**，不要设计成孩子自己点的游戏。

### 数学严谨性（最重要，错了会带偏孩子）

7. **破十/借十法**：第一排 10 个、第二排 `ones` 个；第二排全程不动；第一排减 `b` 后显示 `tenMinus + ones = answer`。
8. **破十法动画节奏**：进入 `10 - b = ?` **不能立刻灰掉**，必须按“第一排拿走”后才灰 `b` 个；按钮随即变“两排合起来”，再下一步变“说出答案”，禁止同一文案连续出现两次。
9. **平十法**：初始全绿框 → 点“开始摆出来”才分色 → 第二排全红框 + 第一排最后 `remain` 个也是红框（红框合计 = `b`）→ 先灰第二排红框（`a - toTen = 10`）→ 再灰第一排最后 `remain` 个（`10 - remain = answer`）。第一排前面的 7 个之类**绝不能标红**，顺序反了就是教错。
10. **凑十法**：第二个加数整体同色，红框合计正好 = `b`，让孩子看出 `b = needToTen + remain`。
11. **不要提前显示答案**，`?` 必须留到最后一步揭晓。
12. **朗读要中文教学化**：`+` 读“加”、`-` 读“减”、`=` 读“等于”、`?` 读“几”，避免把 `16 - 9` 读成“16 杠 9”。
13. **总结页必须有兜底**：孩子可能嘴上说“会了”却答不出，所以要有“没关系，再摆一次”按钮，文案温和、一键回到第一步。

配色与步骤的逐条规则 → `references/math-rules.md`；反模式与原因 → `references/faq.md`

---

## 交付前自检

1. 数学步骤能不能一句话复述？（先拆/先借/先凑 → 再减/再加）
2. **主题是不是用户点名的那个？**（说了金龙鱼就不许出现小汽车）
3. **点名非内置主题时，自己画的 `heroSvg`/`itemSvg` 给了吗？**造型是不是孩子认得出来的那个？
3. 颜色表达的关系对不对？（哪部分是同一个数，哪部分要减/要补）
4. 有没有提前暴露答案？
5. 每一步按钮文案是不是当前动作？
6. 结尾有没有“再摆一次”？页面里有没有 emoji、渐变、外部链接？

---

## 出问题怎么办

| 情况 | 处理 |
|------|------|
| 不知道有哪些方法和主题 | `python scripts/generate_learnwa.py --list` |
| 分块路径或 JSON 有问题 | 脚本会报出文件名、行号列号和常见原因，按提示改 |
| 指定的题目不合规 | 脚本会说明原因并给示例题；确实要换题就加 `--force-random` |
| 报错「你说到了主题「X」，它不是内置主题」 | **不是让你停下问用户**。这是提醒你自己动手：写 `customTheme` 并用 `heroSvg`/`itemSvg` 把「X」画出来，**不要**加 `--allow-default-theme` 绕过去 |
| 提示「customTheme 没有给 themeCSS」 | 补上配色，否则孩子看到的是中性灰，和主题不搭 |
| 提示「customTheme 没有 heroSvg/itemSvg」 | 自己画一份，否则角色物品是通用造型，孩子对不上号 |
| 提示「heroSvg 里有脚本/事件，已自动剔除」 | 教具页只允许纯静态内联 SVG，去掉 `on*`、`<script>`、外链即可 |
| 想看完整效果长什么样 | 打开 `references/examples.md`，里面有三种方法的完整对照 |

脚本退出码：`0` 成功 / `2` 输入问题 / `3` 技能文件缺失 / `1` 未预期异常。

报错对照表、FAQ、反模式清单 → `references/faq.md`

---

## 文件地图

| 路径 | 用途 |
|------|------|
| `SKILL.md` | 主规范（本文件）：判断、硬约束、自检 |
| `references/math-rules.md` | 三种方法的算式、变量、逐步骤模板、配色铁律 |
| `references/themes.md` | 内置主题的角色、物品、动词、配色变量 |
| `references/lesson-block-format.md` | 分块 JSON 的完整字段说明与 customTheme 示例 |
| `references/examples.md` | 三种方法 + 自定义主题的完整效果示例与命令 |
| `references/faq.md` | 报错对照表、常见问题、反模式清单及原因 |
| `templates/learnwa-template.html` | 通用 H5 模板（含 CSS/SVG/交互/朗读） |
| `scripts/generate_learnwa.py` | 分块 → 单文件 H5 的合成脚本 |

只有在**新增通用视觉类型或改模板本身**时，才动 `templates/learnwa-template.html`；个性主题一律写在分块里。

---

## 测试用例

- 「我要一个破十法，孩子喜欢交通工具」→ `break_ten` + `vehicle`
- 「帮我生成一个凑十法，孩子喜欢收集卡片」→ `make_ten` + `card_collection`
- 「孩子不会平十法，喜欢恐龙，给我一个简单点的」→ `level_ten` + `dinosaur`
- 「我小孩喜欢小熊，给他讲个破 10 法吧」→ `break_ten` + `animal_bear`
- 「孩子迷上小猫钓鱼，来个借十法」→ `break_ten` + `customTheme`（小猫钓鱼 + 自画 SVG）
- 「**来个足球的破十法**」→ `break_ten` + `customTheme`（足球）；**不是** `vehicle`
- 「**来个金龙鱼的**」→ 写 `customTheme`（金龙鱼）**并自己画金龙鱼 SVG**；**不是** `vehicle`，也不是"报错后停下"
- 「来个破十法」→ `break_ten` + `vehicle`（完全没提主题，才用默认）
- 直接跑脚本「来个金龙鱼的」→ 退出码 `2`，报错里有 `customTheme` 骨架和自画 SVG 提示（刻意设计的保护，随后应据此一步到位生成）
