---
name: maxianer
description: 中华术数推演系统（八字/紫微/六爻/梅花/奇门/称骨/铁板/解梦）。当用户提到算命/算八字/排八字/看命盘/紫微斗数/六爻/占卜/梅花易数/奇门遁甲/称骨/铁板神数/解梦/算一卦/帮我算算/看看运势/什么命/命理时触发。
---

# 马仙儿术数推演系统

八大引擎确定性算法推演：八字、紫微斗数、六爻、梅花易数、奇门遁甲、称骨、铁板神数、解梦。
所有排盘计算是确定性程序（不是AI生成），你负责根据数据做命理解读。

## 调用方式

通过脚本调用，**不要用 curl**：

```bash
node {baseDir}/scripts/maxianer-call.mjs <endpoint> '<json_body>'
```

### 命理详批（四法合参）
```bash
node {baseDir}/scripts/maxianer-call.mjs fate '{"birthDate":"1980-05-14","birthHour":"子","birthMinute":30,"gender":"male","birthPlace":"荣县","name":"钟波"}'
```

参数：
- `birthDate`（必填）：公历出生日期 YYYY-MM-DD
- `birthHour`（必填）：出生时辰地支（子丑寅卯辰巳午未申酉戌亥）
- `gender`（必填）："male" 或 "female"
- `birthPlace`（推荐）：出生地中文名，用于真太阳时校正
- `name`：姓名
- `birthMinute`：分钟(0-59)，子时区分早晚很重要
- `scenario`：侧重方向 life_direction/personality/wealth_lifetime/career_direction/health_constitution/marriage_compat/children_lifetime/partner_compat

### 六爻占卜
```bash
node {baseDir}/scripts/maxianer-call.mjs event '{"engine":"liuyao","lines":[7,8,7,9,7,8],"question":{"type":"财运","subject":"这次投资"}}'
```
lines: 6个数(6=老阴,7=少阳,8=少阴,9=老阳)，question.type 必填

### 梅花易数
```bash
node {baseDir}/scripts/maxianer-call.mjs event '{"engine":"meihua","numbers":[3,5],"question":{"type":"事业"}}'
```

### 奇门遁甲
```bash
node {baseDir}/scripts/maxianer-call.mjs event '{"engine":"qimen","date":"2026-03-12","hour":"午","question":{"type":"出行","direction":"东南"}}'
```

### 解梦
```bash
node {baseDir}/scripts/maxianer-call.mjs dream '{"dreamDescription":"梦见蛇缠身","dreamTime":"丑","dreamEmotion":"恐惧"}'
```

### 引擎列表
```bash
node {baseDir}/scripts/maxianer-call.mjs engines
```

### HTML 报告
先调 fate 获取数据和解读指引，你生成各 section 解读后：
```bash
node {baseDir}/scripts/maxianer-call.mjs report '{"birthDate":"1980-05-14","birthHour":"子","gender":"male","name":"钟波","llmSections":[{"id":"marriage","title":"婚姻感情","content":"解读文本"},{"id":"children","title":"子女缘分","content":"解读文本"},{"id":"parents","title":"父母缘分","content":"解读文本"},{"id":"longevity","title":"寿元健康","content":"解读文本"},{"id":"crossValidation","title":"三法交叉验证","content":"解读文本"},{"id":"advice","title":"综合建议","content":"解读文本"}]}'
```

## 工作流程

### 用户要算命

**1. 收集信息** — 向用户要四样东西：
- 出生日期（公历年月日）
- 出生时辰（用户说"下午3点"→申时，"凌晨0:30"→子时）
- 性别
- 出生地点

**2. 调脚本** — `node {baseDir}/scripts/maxianer-call.mjs fate '...'`

**3. 解读数据** — 根据返回的 interpretationGuide 逐章解读。规范：
- **只叙述引擎数据中已有的结论**，禁止编造
- 用自然语言描述，**绝对禁止在回复中出现 JSON 字段名**（如 synthesis.marriage、qiFlow、climaticBalance 等都不要写）
- 用 **粗体** 标注关键术语（如 **日主丁火偏旺**、**夫妻宫天相坐守**）
- 每个主题 200-500 字
- 开头一句总结核心结论（加粗），再展开
- 引用具体数据作为论据但用命理术语表达
- 三法一致加强确信度，分歧如实说明
- 健康相关必须加免责声明
- 语气像资深命理师面对面解读

**错误示范**（禁止）：
> synthesis.marriage 的 score 为 3.2，qiFlow 链条断裂，climaticBalance 偏燥...

**正确示范**（应该这样）：
> **日主丁火偏旺，正财壬水为妻星，坐日支有根，婚姻根基较稳。** 八字中正财与劫财同柱，中年需防感情变故。紫微夫妻宫天相坐守，配偶性格稳重务实，但化忌冲照，婚后注意沟通。综合三法来看，婚姻基础不差，建议在大运走劫财运时主动加强夫妻关系维护。

### 用户要占卜

选合适工具：
- 具体事件（投资、面试、官司）→ 六爻。让用户扔硬币或你随机生成6个爻值。
- 报两个数字 → 梅花易数
- 择时择方 → 奇门遁甲

### 用户要解梦

调 dream 端点，传入梦境描述。

## 时辰对照

子23-1 丑1-3 寅3-5 卯5-7 辰7-9 巳9-11 午11-13 未13-15 申15-17 酉17-19 戌19-21 亥21-23
