# Intensity signals

Maps job-posting language to `intensity_tier` for the hard gate. Load this when
the posting is not in English, or when its intensity is ambiguous.

Tiers, in order: `strict_hours` < `standard` < `high` < `always_on`.
The gate fails when the **JD's implied tier exceeds the user's**.

## How to use it

1. Scan the posting — including the benefits and culture sections, where the
   strongest signals usually hide.
2. Take the **highest** tier any matched phrase implies.
3. No signal in either direction → assume the user's own tier, apply no penalty,
   and say the posting was silent on it.
4. A posting can carry signals from two tiers ("flexible hours" *and* "on-call
   rotation"). Report both and take the higher; the contradiction itself is worth
   an open question.

Phrases below are indicative, not exhaustive — match meaning, not strings.

## English

| Tier | Signals |
|---|---|
| `strict_hours` | "no overtime", "we don't work weekends", "core hours", "35-hour week", "strict work-life boundaries", "right to disconnect" |
| `standard` | "occasional crunch around launches", "some evenings during release weeks", "fast-paced but sustainable" |
| `high` | "fast-paced environment", "wear many hats", "hustle", "long hours", "whatever it takes", "we work hard and play hard", "comfortable with ambiguity and pace", early-stage with no counterweight language |
| `always_on` | "on-call rotation", "24/7 coverage", "follow the sun", "global team across time zones" with meetings outside local hours, "always-on culture" |

## Chinese

| Tier | Signals |
|---|---|
| `strict_hours` | "不加班", "准时下班", "弹性工作", "双休" with explicit no-overtime language |
| `standard` | "偶尔加班", "项目期加班", "节奏快但可持续" |
| `high` | "高强度", "抗压能力强", "能接受加班", "创业心态", "狼性", "全力以赴" |
| `always_on` | "996", "大小周", "单休", "7×12", "随时响应", "on-call 轮值" |

## Japanese

| Tier | Signals |
|---|---|
| `strict_hours` | "残業なし", "定時退社", "フレックス", "ワークライフバランス重視" |
| `standard` | "繁忙期のみ残業あり", "月20時間程度の残業" |
| `high` | "裁量労働制" without stated caps, "みなし残業" with a high included-hours figure, "ベンチャーマインド", "成長意欲の高い方" |
| `always_on` | "オンコール", "24時間体制", "深夜対応あり", "サービス残業" |

## German

| Tier | Signals |
|---|---|
| `strict_hours` | "keine Überstunden", "Gleitzeit", "35-Stunden-Woche", "Vertrauensarbeitszeit" with stated limits, "Work-Life-Balance" |
| `standard` | "gelegentliche Überstunden", "in Projektphasen" |
| `high` | "hohe Belastbarkeit", "Hands-on-Mentalität", "dynamisches Umfeld", "Start-up-Mentalität" |
| `always_on` | "Rufbereitschaft", "24/7-Support", "Schichtdienst" |

## French

| Tier | Signals |
|---|---|
| `strict_hours` | "35 heures", "droit à la déconnexion", "horaires fixes", "équilibre vie pro/vie perso" |
| `standard` | "quelques pics d'activité", "heures supplémentaires occasionnelles" |
| `high` | "forte capacité de travail", "environnement exigeant", "esprit start-up", "polyvalence" |
| `always_on` | "astreinte", "support 24/7", "disponibilité permanente" |

## Spanish

| Tier | Signals |
|---|---|
| `strict_hours` | "jornada intensiva", "horario flexible", "sin horas extra", "conciliación" |
| `standard` | "picos de trabajo puntuales", "horas extra ocasionales" |
| `high` | "alta capacidad de trabajo", "ambiente exigente", "mentalidad startup", "resistencia a la presión" |
| `always_on` | "guardias", "disponibilidad 24/7", "turnos rotativos" |

## Other languages

Reason from meaning using the tier definitions in
`assets/criteria-template.yaml`, and state that you inferred rather than matched.
If the user confirms or corrects your reading, offer to append the phrase to this
file's table for their language so the next posting matches directly.

## Watch for

- **Benefits sections that contradict the duties.** "Unlimited PTO" next to
  "always available for our global customers" is an `always_on` signal wearing a
  `strict_hours` costume. Report the contradiction.
- **Compensation structures implying hours** — a large "included overtime"
  allowance, or a base that assumes on-call pay, implies `high` or above whatever
  the culture section says.
- **Silence in markets where hours are regulated.** In markets with statutory
  limits, no mention of hours is weak evidence of `standard`, not of
  `strict_hours`. Do not upgrade a posting on silence alone.
