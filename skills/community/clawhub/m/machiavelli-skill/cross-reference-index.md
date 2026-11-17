# 交叉引用索引 / Cross-Reference Index

> 双向映射场景、信条、来源、框架与案例之间的关联关系。
> Bidirectional mapping between scenes, credos, sources, frameworks, and cases.
> 最后更新 / Last updated: v1.8.2

---

## 1. 场景 → 信条 / Scenes → Credos

| 场景 | 关联信条 | 关联框架 |
|------|---------|---------|
| `scenes/forli-1499.md` — 弗利谈判 | Credo 8 (设身处地), Credo 2 (狮狐) | Framework 3 (狮狐) |
| `scenes/france-1500.md` — 法国宫廷 | Credo 1 (实效真理) | Framework 1 (实效真理) |
| `scenes/unsent-dispatch-1500.md` — 未寄出的急件 | Credo 9 (如当面说话) | — |
| `scenes/sinigaglia-1502.md` — 西尼加利亚 | **Credo 1** (实效真理), **Credo 3** (机运与准备), **Credo 7** (必然性) | Framework 2 (能力与机运) |
| `scenes/prato-1512.md` — 普拉托溃散 | Credo 13 (责在君主) | Framework 7 (自己的军队) |
| `scenes/torture-1513.md` — 牢房吊刑 | Credo 14 (讽刺即抵抗), Credo 15 (书信自我建构) | — |
| `scenes/study-1513.md` — 书房换装 | Credo 15 (书信自我建构), Credo 4 (畏惧vs爱戴) | — |
| `scenes/mandrake-1518.md` — 写《曼陀罗》 | Credo 14 (讽刺即抵抗) | — |
| `scenes/deathbed-1527.md` — 临终之梦 | Credo 16 (地狱胜过天堂) | — |

## 2. 信条 → 场景 / Credos → Scenes

| 信条 | 关联场景 | 关联来源 |
|------|---------|---------|
| Credo 1 — 实效真理 | france-1500, **sinigaglia-1502** | prince-from-dispatches.md |
| Credo 2 — 狮狐之喻 | forli-1499 | the-prince.md |
| Credo 3 — 机运与准备 | **sinigaglia-1502** | the-prince.md |
| Credo 4 — 畏惧vs爱戴 | study-1513 | the-prince.md |
| Credo 5 — 冲突的建设性 | — | discourses.md |
| Credo 6 — 回到源头 | — | discourses.md |
| Credo 7 — 必然性 | **sinigaglia-1502** | prince-from-dispatches.md |
| Credo 8 — 设身处地 | forli-1499 | letters.md |
| Credo 9 — 如当面说话 | unsent-dispatch-1500 | letters.md |
| Credo 10 — 地狱之路 | — | letters.md |
| Credo 11 — 君主首要技艺 | — | the-prince.md |
| Credo 12 — 制定规则者 | — | art-of-war.md |
| Credo 13 — 责在君主 | prato-1512 | art-of-war.md, florentine-histories.md |
| Credo 14 — 讽刺即抵抗 | mandrake-1518, torture-1513 | drama-poetry.md |
| Credo 15 — 书信自我建构 | study-1513, torture-1513 | letters.md |
| Credo 16 — 地狱胜过天堂 | deathbed-1527 | bio-alexander-lee.md |
| Credo 17 — 新的喀戎 | — | scholarship-strauss.md |

## 3. 案例 → 场景与来源 / Cases → Scenes & Sources

| 案例 | 关联场景 | 关联信条 |
|------|---------|---------|
| Case 01 — 切萨雷·博尔贾 | **sinigaglia-1502** | Credo 1, 3, 7 |
| Case 02 — 佛罗伦萨vs比萨 | — | Credo 5, 11 |
| Case 03 — 罗马vs萨谟奈人 | — | Credo 2, 5 |
| Case 04 — 教皇尤利乌斯二世 | — | Credo 3 |
| Case 05 — 卡特琳娜·斯福尔扎 | forli-1499 | Credo 2 |
| Case 06 — 晚间换装 | study-1513 | Credo 15 |
| Case 07 — 致圭恰迪尼 | — | Credo 14 |
| Case 08 — 角色扮演法 | — | Credo 8 |
| Case 09 — 佛罗伦萨史 | — | Credo 5, 13 |
| Case 10 — 法布里齐奥困境 | — | Credo 12 |
| Case 11 — 科西莫·法布里齐奥 | — | Credo 11, 12 |
| Case 12 — 临终之梦 | deathbed-1527 | Credo 16 |
| Case 13 — 1513年书信 | study-1513 | Credo 15 |
| Case 14 — 金驴记 | — | Credo 14 |
| Reverse 01 — 普拉托溃败 | prato-1512 | Credo 13 |
| Reverse 02 — 过度慷慨 | — | Credo 4 |
| Reverse 03 — 博尔贾失败 | **sinigaglia-1502** | Credo 3 |

## 4. 框架 → 场景与信条 / Frameworks → Scenes & Credos

| 框架 | 关联场景 | 关联信条 |
|------|---------|---------|
| Framework 1 — 实效真理 | france-1500, sinigaglia-1502 | Credo 1 |
| Framework 2 — 能力vs机运 | sinigaglia-1502 | Credo 3 |
| Framework 3 — 狮狐之喻 | forli-1499 | Credo 2 |
| Framework 4 — 畏惧vs爱戴 | study-1513 | Credo 4 |
| Framework 5 — 学会为恶 | — | Credo 7 |
| Framework 6 — 民众vs精英 | — | Credo 5 |
| Framework 7 — 自己的军队 | prato-1512 | Credo 13 |
| Framework 8 — 共和vs君主 | — | Credo 5, 6 |

## 5. 独白 → 场景与信条 / Monologues → Scenes & Credos

| 独白 | 关联场景 | 关联信条 |
|------|---------|---------|
| `3am-loyalty.md` — 忠诚与忤合 | torture-1513 | Credo 15 |
| `4am-unsent-letter.md` — 被遗忘的急件 | unsent-dispatch-1500 | Credo 9 |
| `rejected-1527.md` — 被共和国拒绝 | deathbed-1527 | Credo 16 |

## 6. 来源 → 组件 / Sources → Components

| 来源文件 | 被引用方 |
|---------|---------|
| `sources/the-prince.md` | Credo 1-4, 7, 11; Frameworks 1-5; Cases 01-08 |
| `sources/discourses.md` | Credo 5-6; Framework 6, 8 |
| `sources/dispatches-vol2.md` | france-1500, sinigaglia-1502 |
| `sources/prince-from-dispatches.md` | sinigaglia-1502; Credo 1, 7; Case 01 |
| `sources/letters.md` | Credo 8-10, 15; study-1513, torture-1513 |
| `sources/art-of-war.md` | Credo 11-13 |
| `sources/florentine-histories.md` | Credo 13; Case 09 |
| `sources/drama-poetry.md` | Credo 14; mandrake-1518 |
| `sources/bio-alexander-lee.md` | torture-1513, sinigaglia-1502, deathbed-1527 |
| `sources/bio-viroli.md` | deathbed-1527 |
| `sources/scholarship-strauss.md` | Credo 17 |
| `sources/eastern/guiguzi.md` | Credo 1, 2, 3, 8 (东方注) |

## 7. 按时间线 / By Timeline

| 年代 | 场景/独白 | 关键事件 |
|------|---------|---------|
| 1499 | forli-1499 | 卡特琳娜·斯福尔扎谈判 |
| 1500 | france-1500 | 法国宫廷首次出使 |
| 1500 | unsent-dispatch-1500 | 虚构：反思书信文体 |
| **1502** | **sinigaglia-1502** | **博尔贾"美丽的骗局"** |
| 1512 | prato-1512 | 民兵溃散，共和国倒台 |
| 1513 | torture-1513 | 被捕吊刑 |
| 1513 | study-1513 | 写信给韦托里，书房换装 |
| 1518 | mandrake-1518 | 创作《曼陀罗》 |
| 1527 | deathbed-1527 | 临终之梦 |
