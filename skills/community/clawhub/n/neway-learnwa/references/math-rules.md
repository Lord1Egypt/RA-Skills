# 学习娃 — 数学规则与步骤模板

## Suite 信息

```json
{
  "suiteId": "learnwa_math_skills",
  "suiteName": "学习娃",
  "suiteEnglishName": "LearnWa",
  "version": "0.1.0",
  "targetUser": "parent",
  "childRole": "observer_and_responder",
  "deviceControl": "parent_controlled",
  "supportedSkills": ["break_ten", "make_ten", "level_ten"]
}
```

## 统一 LessonConfig

```json
{
  "lessonId": "",
  "suiteId": "learnwa_math_skills",
  "suiteName": "学习娃",
  "suiteEnglishName": "LearnWa",
  "skillId": "",
  "skillName": "",
  "englishName": "",
  "templateId": "",
  "themeId": "",
  "title": "",
  "grade": 1,
  "difficulty": "easy",
  "mode": "parent_controlled",
  "question": {},
  "story": {},
  "steps": [],
  "practice": [],
  "parentTips": [],
  "offlineMaterials": []
}
```

---

## Skill 1：破十法 break_ten

### 基本信息

```json
{
  "skillId": "break_ten",
  "skillName": "破十法",
  "englishName": "Break Ten Method",
  "grade": 1,
  "topic": "20以内退位减法",
  "templateId": "remove_to_ten",
  "goal": "理解十几减几时，把十几拆成个位数和10，先算10减几，再把个位数加回来。"
}
```

### 题目约束

通用形式：`a - b`

- `a` 是 11 到 19
- `b` 是 2 到 9
- `ones = a - 10`
- 必须满足 `b > ones`

### 计算变量

以 `15 - 8` 为例：

```json
{
  "text": "15 - 8",
  "a": 15,
  "b": 8,
  "ones": 5,
  "tenMinus": 2,
  "answer": 7
}
```

计算规则：

```text
ones = a - 10
把 a 拆成 ones + 10
tenMinus = 10 - b
answer = ones + tenMinus
```

示例过程：

```text
第一排：10 - 8 = 2
第二排：5 不变
最后：2 + 5 = 7
所以 15 - 8 = 7
```

### 步骤模板

1. `intro`：展示主问题  
   - childText：`{a} - {b}`
   - 家长说：`{character}有{a}{itemName}，{goal}要{removeVerb}{b}{itemName}。还剩多少？`

2. `split_to_10`：摆成两排  
   - childText：`{a} = {ones} + 10`
   - 家长说：`破十法先把{a}拆成{ones}和10。{a}里面有几个单独的？`
   - expected：`{ones}`
   - wrongHint：`{a}就是10再多{ones}个，所以可以写成{ones}加10。`
   - 画面：第一排固定 10 个，第二排 `{ones}` 个；此步只摆开、不分色、不灰掉。

3. `borrow_from_ten`：第一排 10 个减少  
   - childText：`10 - {b} = ?`
   - 动画规则：进入此步时不能立即减少；等家长按“第一排拿走”后，第一排才灰掉 `{b}` 个，第二排始终不动。
   - 家长说：`第一排摆10{itemName}，第二排摆{ones}{itemName}。现在第二排不动，只从第一排10个里{removeVerb}{b}{itemName}。10减{b}等于几？`
   - expected：`{tenMinus}`
   - wrongHint：`看第一排：10个里面{removeVerb}{b}个，还剩几个？第二排{ones}个先不要动。`

4. `add_ones_back`：两排合起来  
   - childText：`{tenMinus} + {ones} = ?`
   - 动画规则：此步不能再触发新动画；已灰掉的保持灰掉，其余不动，让家长带孩子直接数第一排剩余和第二排数量。
   - 家长说：`第一排还剩{tenMinus}{itemName}，第二排{ones}{itemName}一直没动。现在算{tenMinus}加{ones}等于几？`
   - expected：`{answer}`
   - wrongHint：`先看第一排剩下的{tenMinus}个，再加上第二排没动的{ones}个。`

5. `summary`：总结  
   - childText：`{a} - {b} = {answer}`
   - 家长说：`所以{a}减{b}，先把{a}摆成第一排10个、第二排{ones}个；第一排10个减{b}还剩{tenMinus}个；第二排{ones}个不变；最后{tenMinus}加{ones}等于{answer}。这就是破十法/借十法的核心。`

---

## Skill 2：凑十法 make_ten

### 基本信息

```json
{
  "skillId": "make_ten",
  "skillName": "凑十法",
  "englishName": "Make Ten Method",
  "grade": 1,
  "topic": "20以内进位加法",
  "templateId": "fill_to_ten",
  "goal": "理解加法中先凑成10，再加剩下的数。"
}
```

### 题目约束

通用形式：`a + b`

- `a` 是 6 到 9
- `b` 是 2 到 9
- 必须满足 `a + b > 10`

### 计算变量

以 `8 + 5` 为例：

```json
{
  "text": "8 + 5",
  "a": 8,
  "b": 5,
  "needToTen": 2,
  "remain": 3,
  "answer": 13
}
```

计算规则：

```text
needToTen = 10 - a
remain = b - needToTen
answer = 10 + remain
```

### 步骤模板

1. `intro`：展示主问题  
   - childText：`{a} + {b}`
   - 家长说：`{character}先有{a}{itemName}，又{addVerb}{b}{itemName}。一共有多少？`

2. `ask_need_to_ten`：问差几到10  
   - childText：`{a} + ? = 10`
   - 家长说：`{a}还差几就能凑成10？`
   - expected：`{needToTen}`
   - wrongHint：`从{a}往后数到10，看看一共数了几个。`

3. `split_b`：拆第二个数  
   - childText：`{b} = {needToTen} + {remain}`
   - 家长说：`我们把{b}分成{needToTen}和几？`
   - expected：`{remain}`
   - wrongHint：`伸出{b}根手指，先拿出{needToTen}根，还剩几根？`

4. `make_ten`：先凑成10  
   - childText：`{a} + {needToTen} = 10`
   - 家长说：`先拿{needToTen}{itemName}过来，把{a}凑成10。`
   - expected：`知道先凑10`
   - wrongHint：`10是很好算的数，所以我们先凑成10。`

5. `add_remain`：再加剩下的  
   - childText：`10 + {remain} = {answer}`
   - 家长说：`还有{remain}{itemName}没加，现在10加{remain}等于几？`
   - expected：`{answer}`
   - wrongHint：`从10往后数{remain}个。`

6. `summary`：总结  
   - childText：`{a} + {b} = {answer}`
   - 家长说：`我们先把{a}凑成10，再加剩下的{remain}，所以{a}加{b}等于{answer}。这就是凑十法。`

---

## Skill 3：平十法 level_ten

### 基本信息

```json
{
  "skillId": "level_ten",
  "skillName": "平十法",
  "englishName": "Level Ten Method",
  "grade": 1,
  "topic": "20以内退位减法",
  "templateId": "subtract_to_ten_then_continue",
  "goal": "理解减法中先减到10，再继续减剩余部分。"
}
```

### 题目约束

通用形式：`a - b`

- `a` 是 11 到 19
- `b` 是 2 到 9
- `ones = a - 10`
- 必须满足 `b > ones`

### 计算变量

以 `16 - 9` 为例：

```json
{
  "text": "16 - 9",
  "a": 16,
  "b": 9,
  "toTen": 6,
  "remain": 3,
  "answer": 7
}
```

计算规则：

```text
toTen = a - 10
remain = b - toTen
answer = 10 - remain
```

### 步骤模板

**顺序必须固定为：先拆减数 → 再减到 10 → 再减剩余。** 拆减数在前，孩子才先建立“要减的 b 被分成两段”的概念。

1. `intro`：展示主问题  
   - childText：`{a} - {b}`
   - 家长说：`{character}有{a}{itemName}，{goal}要{removeVerb}{b}{itemName}。我们来算算还剩几。`
   - 画面：`{a}` 个物品全部**同一种颜色（绿框）**，表示它们都属于同一个被减数。

2. `split_subtrahend`：拆减数  
   - childText：`{b} = {toTen} + {remain}`
   - 家长说：`先看要减的{b}。为了把{a}先减到10，要先减{toTen}，所以把{b}分成{toTen}和几？`
   - expected：`{remain}`
   - wrongHint：`第二排有{toTen}{itemName}，第三排里先拿出同样多的{toTen}{itemName}，剩下就是{remain}。`
   - 画面：**此步才开始分色**。第二排 `{toTen}` 个标**红框**；第三排 `{b}` 个里，前 `{toTen}` 个也是红框，剩下 `{remain}` 个是绿框。红框合计正好等于 `{b}`。这一小步先分成两段即可，**不要在这里灰掉任何物品**。
   - 注意：拆分步不要先减第二排，家长还在带孩子建立 `{b} = {toTen} + {remain}`。

3. `subtract_to_ten`：先减到 10  
   - childText：`{a} - {toTen} = 10`
   - 家长说：`先从{a}里面{removeVerb}{toTen}{itemName}，就正好退到10。{a}减{toTen}等于几？`
   - expected：`10`
   - wrongHint：`{a}里面有10和{toTen}，先把多出来的{toTen}减掉，就变成10。`
   - 画面：**先灰掉第二排的红框 `{toTen}` 个**（也就是“与第二排颜色相同的部分”），第一排最后 `{remain}` 个红框暂不动。

4. `continue_subtract`：继续从 10 减  
   - childText：`10 - {remain} = ?`
   - 家长说：`刚才{b}里面还剩{remain}{itemName}没减。现在从10里面再{removeVerb}{remain}{itemName}，还剩几？`
   - expected：`{answer}`
   - wrongHint：`从10往回数{remain}步。`
   - 画面：再灰掉第一排最后 `{remain}` 个红框。

5. `summary`：总结  
   - childText：`{a} - {b} = {answer}`
   - 家长说：`我们先把要减的{b}分成{toTen}和{remain}，先减{toTen}到10，再从10里减{remain}，所以{a}减{b}等于{answer}。这就是平十法。`

### 平十法配色铁律

以 `15 - 8` 为例（`toTen = 5`，`remain = 3`）：

- 初始页：15 个全部绿框。
- 点“开始摆出来”后：第二排 5 个红框 + 第一排最后 3 个红框，红框合计 8 个 = 要减掉的数。第一排前面的 7 个**绝不能标红**。
- 减到 10 时：先灰第二排红框 5 个；最后才灰第一排最后 3 个红框。顺序反了就是教错。
- 不要一开始就分色，也不要把第二排画成非红框。

---

## 通用 practice 生成规则

每个教具生成 3 道迁移练习：
- 与主题型相同
- 难度接近
- 只给题目和答案，用于最后让家长带孩子口算或摆实物

示例：

```json
"practice": [
  { "text": "12 - 7", "answer": 5 },
  { "text": "14 - 8", "answer": 6 },
  { "text": "15 - 9", "answer": 6 }
]
```

## 通用 offlineMaterials

根据题目数量生成：

```json
[
  "10到20个瓶盖、积木或小卡片",
  "一张写着数字10的纸",
  "一支笔和一张草稿纸",
  "如果不想让孩子看屏幕，可以把屏幕当家长提示卡，只让孩子摆实物"
]
```
