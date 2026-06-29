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
| `themeId` | 否 | 指定时跳过识别；可用内置主题，也可用 `custom_*` 自定义主题 |
| `customTheme` | 否 | Bot 按孩子兴趣动态创建主题，包含角色、物品、目标、视觉类型和颜色 |
| `difficulty` | 否 | 默认 `easy` |
| `seed` | 否 | 用于可复现出题 |
| `storyOverrides` | 否 | 覆盖角色、物品、目标、奖励等故事变量 |
| `copyOverrides.title` | 否 | 覆盖标题 |

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
- 若只是换故事、角色、物品和配色，不要改模板；若需要全新视觉，再扩展模板里的 `visualKind` SVG 绘制函数。
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
