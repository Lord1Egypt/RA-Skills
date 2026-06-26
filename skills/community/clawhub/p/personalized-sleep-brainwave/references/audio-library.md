# 音频库清单（完整版）

> 命名规则：`bw_{症状}_{使用时段}_{使用时长}_{严重度}.mp3`
> - 症状：`general`（通用）/ `soi`（入睡困难）/ `fna`（睡眠维持困难）/ `ema`（早醒）/ `mix`（混合型）
> - 使用时段：`sleep_pre`（睡前使用）
> - 使用时长：`15min` / `30min` / `45min`（音频时长）
> - 严重度：`mil`（轻度）/ `mod`（中度）/ `sev`（重度）

---

## 一、通用型（general）— 症状未明确分类或混合型首选

| 严重度 | 时长 | URL |
|-------|------|-----|
| 轻度 | 30min | http://hc.com/cusresources/sleepAudio/bw_general_sleep_pre_30min_mil.mp3 |
| 中度 | 30min | http://hc.com/cusresources/sleepAudio/bw_general_sleep_pre_30min_mod.mp3 |
| 重度 | 30min | http://hc.com/cusresources/sleepAudio/bw_general_sleep_pre_30min_sev.mp3 |

**适用场景：** 症状类型不明确、MIX混合型、用户选"不确定"原因

---

## 二、SOI型（soi）— 入睡困难

| 严重度 | 时长 | URL |
|-------|------|-----|
| 轻度 | 15min | http://hc.com/cusresources/sleepAudio/bw_soi_sleep_pre_15min_mil.mp3 |
| 中度 | 15min | http://hc.com/cusresources/sleepAudio/bw_soi_sleep_pre_15min_mod.mp3 |
| 重度 | 30min | http://hc.com/cusresources/sleepAudio/bw_soi_sleep_pre_30min_sev.mp3 |

**适用场景：** 躺下睡不着、入睡潜伏期 >30min

---

## 三、FNA型（fna）— 睡眠维持困难

| 严重度 | 时长 | URL |
|-------|------|-----|
| 轻度 | 30min | http://hc.com/cusresources/sleepAudio/bw_fna_sleep_pre_30min_mil.mp3 |
| 中度 | 30min | http://hc.com/cusresources/sleepAudio/bw_fna_sleep_pre_30min_mod.mp3 |
| 重度 | 45min | http://hc.com/cusresources/sleepAudio/bw_fna_sleep_pre_45min_sev.mp3 |

**适用场景：** 夜里频繁觉醒、醒后难再入睡

---

## 四、EMA型（ema）— 早醒

| 严重度 | 时长 | URL |
|-------|------|-----|
| 轻度 | 15min | http://hc.com/cusresources/sleepAudio/bw_ema_sleep_pre_15min_mil.mp3 |
| 中度 | 15min | http://hc.com/cusresources/sleepAudio/bw_ema_sleep_pre_15min_mod.mp3 |
| 重度 | 30min | http://hc.com/cusresources/sleepAudio/bw_ema_sleep_pre_30min_sev.mp3 |

**适用场景：** 比预期早醒 ≥30min、醒后无法再入睡

---

## 五、匹配速查表

根据 **症状类型 × 严重度** 直接查找对应 URL：

| 症状类型 | 轻度（mil）| 中度（mod）| 重度（sev）|
|---------|-----------|-----------|-----------|
| 通用/不确定/MIX | bw_general_sleep_pre_**30min**_mil | bw_general_sleep_pre_**30min**_mod | bw_general_sleep_pre_**30min**_sev |
| SOI 入睡困难 | bw_soi_sleep_pre_**15min**_mil | bw_soi_sleep_pre_**15min**_mod | bw_soi_sleep_pre_**30min**_sev |
| FNA 睡眠维持 | bw_fna_sleep_pre_**30min**_mil | bw_fna_sleep_pre_**30min**_mod | bw_fna_sleep_pre_**45min**_sev |
| EMA 早醒 | bw_ema_sleep_pre_**15min**_mil | bw_ema_sleep_pre_**15min**_mod | bw_ema_sleep_pre_**30min**_sev |

> 完整 URL 前缀：`http://hc.com/cusresources/sleepAudio/`

---

## 六、严重度判定对照（来自 symptom-classification.md）

| 严重度 | 频率 | 白天影响 | 对应代码 |
|-------|------|---------|---------|
| 轻度 | 1–2天/周 | 轻微 | `mil` |
| 中度 | 3–4天/周 | 明显疲倦/注意力下降 | `mod` |
| 重度 | ≥5天/周 | 功能明显受损 | `sev` |

---

## 七、MIX混合型处理规则

MIX 型按以下顺序选取音频：

1. 用户明确"最想先解决哪个" → 以该症状类型音频为主
2. 若用户无明确偏好 → 使用 `general` 通用型
3. 严重度取**最严重**的那个症状的严重度

**向用户展示时：** 只输出1个主音频URL，不堆叠多个链接。

---

## 八、使用时序说明（输出到方案中）

| 症状 | 建议使用时间 | 说明 |
|------|------------|------|
| SOI | 睡前15–30分钟（轻/中度15min，重度30min）| 与音频时长对应 |
| FNA | 睡前30–45分钟（重度45min）| 入睡前使用，睡着后自然停止 |
| EMA | 睡前15–30分钟（轻/中度15min，重度30min）| 配合规律作息时间使用 |
| general | 睡前30分钟 | 通用时序 |

---

## 九、睡眠亚健康（SUB）匹配规则

| 情况 | 匹配音频 | 说明 |
|------|---------|------|
| 无明显症状、整体改善 | `bw_general_sleep_pre_30min_mil.mp3` | 通用轻度，预防性干预 |
| 偶尔入睡稍慢 | `bw_soi_sleep_pre_15min_mil.mp3` | SOI轻度 |
| 偶尔睡眠较浅 | `bw_fna_sleep_pre_30min_mil.mp3` | FNA轻度 |
| 偶尔醒得较早 | `bw_ema_sleep_pre_15min_mil.mp3` | EMA轻度 |

**SUB流程简化：** 亚健康用户跳过严重度评分，统一按**轻度（mil）**匹配；4周改善计划侧重预防和习惯建立，而非症状治疗。
