# 系统初始化

## 触发条件
首次使用，或用户明确说"初始化记忆系统"、"重新开始"、"建立档案"。

---

## Step 0：检测是否真的是全新用户

先问：
> "你之前用过这个记忆系统吗？还是第一次开始？"

- 全新用户 → 继续以下流程
- 断更重启 → 跳转 `references/05-protocols.md` § 重启协议

---

## Step 1：建立目录

告知用户在本地执行：

```bash
mkdir -p memory/present/{diary,response,quick,letters,weekly,summary}
mkdir -p memory/past/{timeline,themes}
mkdir -p memory/future/{signals/signals-archive,patterns,goals,decisions,verification,reports}
```

复制模板文件：
- `templates/profile-template.md` → `memory/profile.md`
- `templates/signals-log-template.md` → `memory/future/signals/signals-log.md`
- `templates/active-goals-template.md` → `memory/future/goals/active-goals.md`
- `templates/ai-portrait-template.md` → `memory/ai-portrait.md`
- `templates/pattern-alerts-template.md` → `memory/future/patterns/pattern-alerts.md`

---

## Step 2：建立 profile.md（对话引导）

**原则**：分轮进行，每轮 1-2 个问题，等用户回答后再继续。不要一口气问完。

### 第一轮：基本信息
> "你好！让我来帮你建立你的个人档案。
> 首先——你叫什么名字，或者你希望我怎么称呼你？今年多大，目前在做什么？"

### 第二轮：生活现状
> "你现在住在哪儿？一个人还是和家人/朋友一起？"

### 第三轮：当前状态（最重要）
> "用你自己的话，说说现在生活的整体状态是什么样的。不用很完整，想到什么说什么。"

追问：
> "有没有最近特别压着你、或者让你很在意的事？"

### 第四轮：性格自述
> "你怎么看自己这个人？有没有一些你自己都意识到的习惯或者行为模式——不管好的还是坏的？"

### 第五轮：目标
> "你现在最想实现的事情是什么？可以是任何方面的，说 1-3 个就好。"

### 第六轮：使用期望
> "最后一个问题——你最希望这个系统能帮你做什么？
> 是帮你坚持记录、帮你做决策、帮你整理自己的人生，还是别的什么？"

### 整理并生成 profile.md

基于用户的所有回答，生成完整的 profile.md，然后给用户看，说：
> "这是我对你的初步了解，你觉得有没有不准确或者想补充的地方？"

用户确认后，profile.md 正式建立。

---

## Step 3：建立初始 ai-portrait.md

基于 profile.md 的内容，生成一个初始版本的 AI 画像。
这个文件由 AI 维护，随着数据积累持续更新。

**ai-portrait.md 初始模板：**

```markdown
# AI 眼中的 [用户名]

> 最后更新：YYYY-MM-DD（基于X天的数据）
> 这个文件由 AI 基于用户的所有记录持续维护和更新。

## 我对你的核心理解

[AI 用 3-5 句话描述对用户最本质的理解，要有具体感，不泛泛而谈]

## 你的决策风格

[基于历史数据识别出的决策模式]

## 你的情绪模式

[你的情绪通常怎么运作？有哪些触发因素？]

## 你的能量规律

[你在什么时候状态好？什么时候容易低落？有没有周期性规律？]

## 你反复出现的主题

[你的日记和对话里，什么话题/困境/渴望反复出现？]

## 你的成长轨迹

[基于时间维度，你在哪些方面有可见的成长？]

## 你可能还没意识到的事

[AI 从数据中观察到的、用户本人可能没有察觉的模式或特点]

## 已观察到的矛盾

[用户在不同时间说的相互矛盾的事情，记录在这里，不判断，只记录]

---

## 更新记录

| 日期 | 更新内容 | 基于的数据 |
|---|---|---|
| YYYY-MM-DD | 初始建立 | profile.md |
```

---

## Step 4：建立初始目标档案

根据用户在 profile 中提到的目标，引导用户细化，建立 active-goals.md 初始版本。

每个目标至少要明确：
- 具体想实现什么（不能模糊）
- 为什么这个目标重要
- 最近一步要做的事

---

## Step 5：询问是否有已有内容可以导入

> "你有没有写过日记、公众号文章、朋友圈，或者任何形式的个人记录？
> 如果有，可以把内容发给我，我帮你整理归档，不需要你自己分类。"

**导入处理规则：**

| 内容类型 | 归档位置 |
|---|---|
| 日记/流水账 | past/timeline/ 对应年份 |
| 文章/观点/思考 | past/themes/cognition.md |
| 重要经历/事件 | past/themes/ 对应主题 |
| 旧的目标记录 | future/goals/completed-goals.md 或 active-goals.md |

---

## Step 6：初始化完成

说：
> "好了，你的记忆系统已经建好了。
>
> 从今天起，想记录的时候就来找我，说'记录今天'或者直接把你想说的发给我就行。
>
> 它会越来越懂你。"
