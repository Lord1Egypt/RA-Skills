---
name: interpret-fate-via-ziwei
description: 通过紫薇斗数解释命运 A skill to interpret fate using Ziwei astrology principles.
---

# 紫薇斗数

## 技能描述

本技能通过紫薇斗数的原理来解释命运，提供关于个人命运的见解和建议。用户输入出生日期、时间和地点，系统将根据这些信息进行计算，并输出命运解释、关键人生事件以及相关建议。

## 环境检查

- 需要安装 Node.js 版本 18 或更高，如果没有 node 环境需要先进行安装。

执行下面的命令进行检查：

```bash
node -v
```

## 用户输入

- 出生日期（需要包含年月日时）
- 性别（男/女）

## 输入检查

如果输入不完整或格式错误，系统将提示用户提供正确的信息。

注意事项如下：

- 需要与用户确认出生日期为12小时制，还是24小时制
- 需要与用户确认是否闰月

## 计算出生时辰

根据用户提供的出生时间，系统将计算出对应的时辰。中国传统的时辰划分如下：

| 时间序号 | 时辰名称 | 时间范围      |
| -------- | -------- | ------------- |
| 0        | 子时     | 23:00 - 00:59 |
| 1        | 丑时     | 01:00 - 02:59 |
| 2        | 寅时     | 03:00 - 04:59 |
| 3        | 卯时     | 05:00 - 06:59 |
| 4        | 辰时     | 07:00 - 08:59 |
| 5        | 巳时     | 09:00 - 10:59 |
| 6        | 午时     | 11:00 - 12:59 |
| 7        | 未时     | 13:00 - 14:59 |
| 8        | 申时     | 15:00 - 16:59 |
| 9        | 酉时     | 17:00 - 18:59 |
| 10       | 戌时     | 19:00 - 20:59 |
| 11       | 亥时     | 21:00 - 22:59 |

为用户输出对应的时辰名称和时间范围。

## 阅读文献资料

阅读对应的文献资料

- 星盘介绍 (docs/learn-astrolabe.md)
- 宫位知识 (docs/learn-palace.md)
- 星曜知识 (docs/learn-star.md)
- 四化 (docs/learn-mutagen.md)
- 格局 (docs/learn-pattern.md)
- 安星决 (docs/learn-setup.md)
- 紫薇斗数全书 (docs/learn-ancient-book.md)
- 诸星问答论 (docs/learn-ancient-book-qa.md)

## 输出在线排盘地址

```txt
https://ziwei.pub/astrolabe/?d=<出生日期，格式为 YYYY-M-D>&t=<时辰序号>&leap=<是否闰月，true 或 false>&g=<性别，male或female>&type=<日历类型，solar 或 lunar>
```

## 获取星盘数据和运限数据

1. 如果用户提供的出生日期为公历（阳历），则使用 `node` 执行下面的脚本来排星盘。

```mjs
import { astro } from "iztro"
const timeIndex = 0 // 根据用户提供的出生时间计算出的时辰序号
const isLeapMonth = false // 根据用户提供的信息确定是否为闰月
const astrolabe = astro.bySolar(
  "<出生日期，格式为 YYYY-M-D>",
  timeIndex,
  "<性别，男或女>",
  isLeapMonth,
)

// 获取星盘数据
console.log(astrolabe)

// 获取运限数据
astrolabe.horoscope(new Date())
```

2. 如果用户提供的出生日期为农历（阴历），则使用 `node` 执行下面的脚本来排星盘。

```mjs
import { astro } from "iztro"
const timeIndex = 0 // 根据用户提供的出生时间计算出的时辰序号
const isLeapMonth = false // 根据用户提供的信息确定是否为闰月
const astrolabe = astro.byLunar(
  "<出生日期，格式为 YYYY-M-D>",
  timeIndex,
  "<性别，男或女>",
  isLeapMonth,
)

// 获取星盘数据
console.log(astrolabe)

// 获取运限数据
astrolabe.horoscope(new Date())
```

## 数据字段解释

### 星盘数据字段说明

| 字段名                    | 字段含义                   |
| ------------------------- | -------------------------- |
| solarDate                 | 阳历日期                   |
| lunarDate                 | 农历日期                   |
| chineseDate               | 四柱                       |
| time                      | 时辰                       |
| timeRange                 | 时辰对应的时间段           |
| sign                      | 星座                       |
| zodiac                    | 生肖                       |
| earthlyBranchOfSoulPalace | 命宫地支                   |
| earthlyBranchOfBodyPalace | 身宫地支                   |
| soul                      | 命主                       |
| body                      | 身主                       |
| fiveElementsClass         | 五行局                     |
| palaces                   | 十二宫数据（数组，见下表） |

#### 十二宫数据（palaces）字段说明

| 字段名           | 字段含义                            |
| ---------------- | ----------------------------------- |
| name             | 宫名                                |
| isBodyPalace     | 是否身宫                            |
| isOriginalPalace | 是否来因宫                          |
| heavenlyStem     | 宫位天干                            |
| earthlyBranch    | 宫位地支                            |
| majorStars       | 主星（含天马禄存，数组）            |
| minorStars       | 辅星（含六吉六煞，数组）            |
| adjectiveStars   | 杂耀（数组）                        |
| changsheng12     | 长生12神                            |
| boshi12          | 博士12神                            |
| jiangqian12      | 流年将前12神                        |
| suiqian12        | 流年岁前12神                        |
| stage            | 大限（对象，含range和heavenlyStem） |
| ages             | 小限（数组）                        |

##### majorStars / minorStars / adjectiveStars 结构

| 字段名     | 字段含义                               |
| ---------- | -------------------------------------- |
| name       | 星名                                   |
| type       | 星类型                                 |
| scope      | 星所属范围                             |
| brightness | 星曜状态（如庙、得等，仅majorStars有） |

### 运限数据字段说明

| 字段名                 | 字段含义                             |
| ---------------------- | ------------------------------------ |
| solarDate              | 阳历日期                             |
| lunarDate              | 农历日期                             |
| decadal                | 大限（十年运）相关数据对象           |
| decadal.index          | 大限序号                             |
| decadal.heavenlyStem   | 大限天干                             |
| decadal.earthlyBranch  | 大限地支                             |
| decadal.palaceNames    | 大限对应的十二宫名称数组             |
| decadal.mutagen        | 大限变星（主变星数组）               |
| decadal.stars          | 大限相关星曜数组                     |
| decadal.age            | 大限年龄对象                         |
| decadal.age.index      | 大限年龄序号                         |
| decadal.age.nominalAge | 大限虚岁年龄                         |
| yearly                 | 流年（年度运）相关数据对象           |
| yearly.index           | 流年序号                             |
| yearly.heavenlyStem    | 流年天干                             |
| yearly.earthlyBranch   | 流年地支                             |
| yearly.palaceNames     | 流年对应的十二宫名称数组             |
| yearly.mutagen         | 流年变星（主变星数组）               |
| yearly.stars           | 流年相关星曜二维数组（每宫一个数组） |
| monthly                | 流月（月度运）相关数据对象           |
| monthly.index          | 流月序号                             |
| monthly.heavenlyStem   | 流月天干                             |
| monthly.earthlyBranch  | 流月地支                             |
| monthly.palaceNames    | 流月对应的十二宫名称数组             |
| monthly.mutagen        | 流月变星（主变星数组）               |
| daily                  | 流日（每日运）相关数据对象           |
| daily.index            | 流日序号                             |
| daily.heavenlyStem     | 流日天干                             |
| daily.earthlyBranch    | 流日地支                             |
| daily.palaceNames      | 流日对应的十二宫名称数组             |
| daily.mutagen          | 流日变星（主变星数组）               |
| hourly                 | 流时（时辰运）相关数据对象           |
| hourly.index           | 流时序号                             |
| hourly.heavenlyStem    | 流时天干                             |
| hourly.earthlyBranch   | 流时地支                             |
| hourly.palaceNames     | 流时对应的十二宫名称数组             |
| hourly.mutagen         | 流时变星（主变星数组）               |

## 输出星盘数据和运限数据

得到的数据，按照字段的具体含义，为用户输出详细的星盘数据和运限数据。

## 输出解盘结论

根据星盘数据和运限数据，结合参考资料，为用户提供详细的关于个人命运的见解和建议。
