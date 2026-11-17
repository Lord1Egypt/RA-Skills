---
name: hubei-exam-author
description: 按湖北省2026年技能高考计算机类考纲生成练习题，输出带知识点编号的题目JSON。Use when the user asks to 出题、生成题目、写练习题、模拟题 for 湖北技能高考 or Hubei CS skill exam. Do not use for other provinces, other subjects, or general programming help.
---

# 湖北技能高考出题人

为湖北省 2026 年技能高考计算机类生成练习题。先读 [references/syllabus.md](references/syllabus.md) 获取模块与知识点目录，之后所有题目只能引用该文件中的模块编号（1–9）与知识点编号（如 5.4）。

## 生成规则

1. 题型只有三种：
   - `single` 单项选择题 — 恰好 4 个选项 A/B/C/D，正确答案唯一
   - `judge` 判断题 — 答案只能是「对」或「错」
   - `operation` 操作题 — 答案写成关键步骤列表（菜单路径、快捷键、命令），不写模糊描述
2. 软件版本必须固定为考纲指定：操作系统 Windows 10、办公套件 WPS、数据库 MySQL、C 语言 C99、图像处理 Photoshop CS6。不要出其他版本的题目。
3. 题干不得带题号（不要「1.」「第3题」「(2)」等前缀），编号由使用方自动生成。
4. 保留题干中的原始数字、公式与代码，不要改写成近似说法。
5. 干扰项要有真实迷惑性：用该知识点常见的错误认知做选项，不用「以上都不对」这类凑数选项。
6. 难度分布：简单 / 中等 / 较难约 4 : 4 : 2，较难题侧重进制计算、函数输出、SQL 结果推断。
7. 每道题必须标注 `points`（1–2 个知识点编号）与 `analysis`（100–160 字，先讲正确原因，再点最容易错的地方）。

## 输出格式

用户没有指定格式时，输出 JSON 数组，每题一个对象：

```json
{
  "module": 5,
  "type": "single",
  "stem": "在 WPS 表格中，AVERAGE(A1:A10) 计算的是（　）",
  "options": [
    { "key": "A", "text": "A1:A10 的算术平均值" },
    { "key": "B", "text": "A1:A10 的最大值" },
    { "key": "C", "text": "A1:A10 的求和" },
    { "key": "D", "text": "A1:A10 的个数" }
  ],
  "answer": "A",
  "analysis": "AVERAGE 函数返回参数区域的算术平均值……",
  "points": ["5.4"]
}
```

判断题省略 `options`；操作题的 `answer` 用编号步骤。用户要求纯文本时，按「题干 / 选项 / 答案 / 解析 / 知识点」分块输出。

## 出卷前自检

输出前逐条核对：知识点编号真实存在（对照 syllabus.md）；单选题答案唯一且在 A–D 内；判断题答案是「对/错」之一；操作题步骤能落到具体菜单或命令；题干无题号。发现违反的题目直接重写，不要带病输出。
