# 学习娃 — 主题配置参考

## 交通工具主题 (vehicle)

```json
{
  "themeId": "vehicle",
  "themeName": "交通工具",
  "characters": ["小汽车", "小火车", "小飞机"],
  "itemNames": ["能量格", "电量格", "燃料格"],
  "goals": ["过桥", "开到下一站", "飞到目的地"],
  "removeVerb": "用掉",
  "addVerb": "加入",
  "rewardNames": ["过桥小能手", "能量小达人", "小小驾驶员"],
  "css": {
    "--primary": "#FF6B35",
    "--secondary": "#004E89",
    "--accent": "#FFD700",
    "--bg-scene-top": "#87CEEB",
    "--bg-scene-bottom": "#B0E0E6",
    "--ground-color": "#7B8D6F",
    "--item-color": "#FF6B35",
    "--text-on-item": "#FFFFFF",
    "--card-bg": "#FFF8F0",
    "--font": "'PingFang SC', 'Microsoft YaHei', sans-serif"
  }
}
```

### 场景元素
- 蓝天渐变背景 + 道路/铁轨/跑道
- 角色：🚗 小汽车 / 🚂 小火车 / ✈️ 小飞机（emoji或CSS绘制）
- 物品用进度条/格子表示

### 故事包装示例
- 「小汽车过桥学破十法」：汽车有13格能量，过桥用掉8格
- 「小火车到站学平十法」：火车有16格电，到站用掉9格
- 「小飞机加油学凑十法」：飞机有8格油，又加5格

---

## 收集卡片主题 (card_collection)

```json
{
  "themeId": "card_collection",
  "themeName": "收集卡片",
  "characters": ["小收藏家", "卡片小达人"],
  "itemNames": ["卡片", "普通卡", "能量卡"],
  "goals": ["兑换稀有卡", "集齐一套卡", "完成卡册"],
  "removeVerb": "交出",
  "addVerb": "加入",
  "rewardNames": ["稀有卡收藏家", "卡片小达人", "凑十收藏家"],
  "css": {
    "--primary": "#7C3AED",
    "--secondary": "#EC4899",
    "--accent": "#FBBF24",
    "--bg-scene-top": "#F5F3FF",
    "--bg-scene-bottom": "#EDE9FE",
    "--ground-color": "#DDD6FE",
    "--item-color": "#7C3AED",
    "--text-on-item": "#FFFFFF",
    "--card-bg": "#FAFAFE",
    "--font": "'PingFang SC', 'Microsoft YaHei', sans-serif"
  }
}
```

### 场景元素
- 浅紫背景 + 卡册/卡桌
- 角色：🃏 卡片形式或小孩emoji
- 物品：彩色小卡片方块

### 故事包装示例
- 「稀有卡兑换学破十法」：小收藏家有13张普通卡，兑换稀有卡要交出8张
- 「集齐10张卡学凑十法」：有8张卡，又得到5张，先凑满10张
- 「卡片整理学平十法」：有16张卡，先收拾6张让卡册整齐

---

## 恐龙主题 (dinosaur)

```json
{
  "themeId": "dinosaur",
  "themeName": "恐龙",
  "characters": ["小恐龙", "恐龙宝宝"],
  "itemNames": ["恐龙蛋", "树叶", "小脚印"],
  "goals": ["找到妈妈", "收集树叶", "回到山洞"],
  "removeVerb": "拿走",
  "addVerb": "放入",
  "rewardNames": ["恐龙小勇士", "恐龙探险家", "森林小达人"],
  "css": {
    "--primary": "#059669",
    "--secondary": "#92400E",
    "--accent": "#F59E0B",
    "--bg-scene-top": "#D1FAE5",
    "--bg-scene-bottom": "#A7F3D0",
    "--ground-color": "#65A30D",
    "--item-color": "#059669",
    "--text-on-item": "#FFFFFF",
    "--card-bg": "#F0FDF4",
    "--font": "'PingFang SC', 'Microsoft YaHei', sans-serif"
  }
}
```

### 场景元素
- 绿色森林/草原背景 + 山洞/树林
- 角色：🦕 小恐龙 / 🦖 恐龙宝宝
- 物品：🥚 恐龙蛋 / 🍃 树叶

### 故事包装示例
- 「恐龙蛋分组学破十法」：恐龙妈妈有13个蛋，被拿走了8个
- 「收集树叶学凑十法」：小恐龙有8片树叶，又找到5片
- 「回到山洞学平十法」：恐龙宝宝走16步到家，先走6步到树，再走剩下的

---

## 在 H5 中使用主题

生成 HTML 时，将主题 CSS 变量注入 `:root`，替换角色/物品名到故事文案，使用对应 emoji 作为视觉元素。
