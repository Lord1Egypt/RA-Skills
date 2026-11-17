# 题库 JSON 规范

生成题库时严格遵守本规范。`scripts/build_bank.py` 会逐条校验，任何一条不符都会中断构建。

## 顶层结构

```json
{
  "meta": {
    "title": "药理学复习题库",
    "brandName": "药理题库",
    "brandIcon": "pill",
    "version": "1.0.0",
    "generatedFrom": ["药理学讲义.docx", "期末重点.pdf"],
    "note": "由学习资料自动整理生成，原文档无分页信息，出处采用「文件名 + 章节」形式。"
  },
  "subjects": [
    { "id": "总论", "name": "总论", "desc": "药物作用基本规律与药代动力学", "icon": "pill" }
  ],
  "questions": [ ... ]
}
```

也接受**裸数组**形态（顶层直接是 `questions` 数组），此时 `meta` 与 `subjects` 由构建脚本自动补全。
但只要能确定标题和科目描述，就应显式提供 `meta` 与 `subjects`——这直接决定网页的品牌名与科目卡片文案。

### meta 字段

| 字段 | 必填 | 说明 |
| --- | --- | --- |
| `title` | 建议 | 浏览器标签页标题。缺省 `智能复习题库` |
| `brandName` | 建议 | 顶栏左上角显示的名称，**建议 2-5 字**，过长会挤压导航 |
| `brandIcon` | 可选 | 顶栏图标，取值见下方图标库。缺省 `book` |
| `generatedFrom` | 建议 | 来源文件名数组，便于用户追溯 |
| `note` | 可选 | 生成说明。若原始资料无页码，应在此声明「未编造页码」 |

`typeLabels` 与 `difficultyLabels` 由构建脚本注入，**不要手写**。

### subjects 字段

`subjects` 只需提供 `id`/`name`/`desc`/`icon`；`chapters` 与 `count` 由构建脚本自动统计填充。

- `id` 必须与题目里的 `subject` 字段**完全一致**（用科目名本身作为 id 最省事）
- `desc` 一句话，出现在科目卡片上，控制在 20 字以内
- 科目顺序即首页卡片顺序

## 题目通用字段

每道题都必须有：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `id` | string | 全局唯一。推荐 `<科目缩写>-<序号>`，如 `pk-001` |
| `subject` | string | 所属科目，须与 `subjects[].id` 对应 |
| `chapter` | string | 章节/知识点分组，用于筛选 |
| `type` | string | `single` / `multiple` / `judge` / `blank` / `short` |
| `difficulty` | number | `1` 基础 / `2` 进阶 / `3` 挑战 |
| `stem` | string | 题干 |
| `analysis` | string | 解析，**必填**。说明为什么，而不是复述答案 |
| `source` | object | 出处，见下 |
| `tags` | string[] | 可选，知识点标签 |

### source 出处

```json
"source": { "file": "药理学讲义.docx", "locator": "第三章 药物代谢动力学", "page": null }
```

- `file`、`locator` 均必填
- `page` 允许整数或 `null`
- **绝不编造页码。** .docx / .md / .txt 通常不含可靠分页信息，此时 `page` 必须为 `null`，
  用 `locator` 承载「章节名 / 小节标题 / 段落主题」。只有 PDF 等确有页码的来源才填整数。

## 按题型的专属字段

### single 单选题

```json
{
  "type": "single",
  "options": [
    { "key": "A", "text": "选项文本" },
    { "key": "B", "text": "选项文本" },
    { "key": "C", "text": "选项文本" },
    { "key": "D", "text": "选项文本" }
  ],
  "answer": "B"
}
```

- 至少 3 个选项，`key` 不得重复
- `answer` 是**字符串**，且必须命中某个 `key`

### multiple 多选题

同 single，但 `answer` 是**数组且至少 2 项**：

```json
{ "type": "multiple", "options": [...], "answer": ["A", "C", "D"] }
```

### judge 判断题

```json
{ "type": "judge", "answer": "T" }
```

- 无 `options` 字段
- `answer` 只能是 `"T"`（正确）或 `"F"`（错误）

### blank 填空题

```json
{
  "type": "blank",
  "stem": "药物在体内的过程包括吸收、分布、____ 和 ____。",
  "answer": [
    { "accept": ["代谢", "生物转化"] },
    { "accept": ["排泄"] }
  ]
}
```

- 题干用**连续 4 个下划线** `____` 标记空位
- `answer` 数组长度必须与题干里 `____` 的个数**严格相等**
- 每个空的 `accept` 是可接受答案数组，把同义写法都列上（如「代谢 / 生物转化」），
  否则用户写对了也会判错

### short 简答题

```json
{
  "type": "short",
  "answer": "参考答案全文……",
  "keywords": ["首过效应", "肝脏", "生物利用度"]
}
```

- `keywords` 需 **2-12 个**，用于自评时提示要点
- 关键词取「判分踩分点」，不要塞入无区分度的通用词

## 图标库

`subjects[].icon` 与 `meta.brandIcon` 只能取以下值，未命中自动回退 `book`：

| key | 适用 | key | 适用 |
| --- | --- | --- | --- |
| `book` | 通用 / 文科 | `chart` | 统计、经济、金融 |
| `pill` | 药学、医学 | `scroll` | 历史、古籍、文献 |
| `leaf` | 中医药、植物 | `cpu` | 计算机组成、硬件 |
| `sprout` | 生物、农学 | `palette` | 设计、美术 |
| `flask` | 化学、实验 | `music` | 音乐、艺术 |
| `brain` | 心理学、神经 | `briefcase` | 管理、商科、职业考试 |
| `code` | 编程、软件 | `compass` | 地理、导航、方法论 |
| `sigma` | 数学、统计 | `heart` | 护理、健康、生理 |
| `scale` | 法律、伦理 | `atom` | 物理 |
| `globe` | 地理、国际 | `language` | 语言、外语 |

## 出题质量准则

生成题目时遵守：

1. **一题一考点。** 不要把多个知识点塞进一道题，否则错了也不知道错在哪。
2. **干扰项要合理。** 单选/多选的错误选项必须是「看起来可能对」的近似概念，
   不要放明显荒谬的选项凑数——那样题目失去区分度。
3. **解析讲原因。** `analysis` 要解释为什么对、为什么其他选项错，而不是重复一遍答案。
4. **难度分层。** 同一章节内混合 1/2/3 三档，不要全是基础题。
   经验配比：基础 5 : 进阶 3 : 挑战 2。
5. **题型搭配。** 优先 single 与 judge（作答快、可高频复习），
   blank 与 short 适量（作答慢，但记忆效果强）。
   经验配比：单选 4 : 判断 2 : 多选 2 : 填空 1 : 简答 1。
6. **忠于原文。** 只考资料里真实存在的内容，不引入资料外的知识。
   拿不准的宁可不出题，也不要生成可能有误的题目——错题会被反复复习，危害成倍放大。
7. **题干自足。** 不要出现「如上所述」「见前文」这类依赖上下文的表述，
   因为练习时题目是打散随机出现的。
