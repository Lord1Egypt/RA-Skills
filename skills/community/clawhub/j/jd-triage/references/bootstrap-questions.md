# Bootstrap questions

Ask the user these questions to populate `jd_criteria.md`. Group into three blocks (Profile / Hard Gates / Soft Axes); ask one block at a time. Translate to the user's language; only the field keys (in code blocks) stay English.

After all three blocks are answered, show a full summary and ask "Confirm and save? (y / edit <field>)" before writing.

---

## Block 1 — Profile (about you now)

1. **Years of experience** (`years_of_experience`) — integer years of professional work.
2. **Current title and company** (`current_title_company`) — e.g. "PM @ Acme".
3. **Current salary** (`current_salary`) — include currency and period (monthly / yearly), e.g. "30k CNY/month".

---

## Block 2 — Hard gates (any failure → OUT)

4. **Salary floor** (`salary_floor`) — the minimum total comp you would accept. Below this is auto-reject.

5. **Target cities** (`target_cities`) — list. Include `Remote` if you accept fully remote roles.

6. **Lifestyle tier** (`lifestyle_tier`) — pick one:
   - `strict_9to5` — Strict 9-to-5, weekends fully off, no after-hours
   - `standard` — Standard hours, occasional crunch, weekends generally off
   - `crunch` — 10+ hour days common, occasional weekend work expected
   - `always_on` — Always-on, on-call, cross-timezone availability

7. **Hard red lines** (`hard_red_lines`) — list any dealbreaker keywords or patterns. Examples:
   - Specific responsibilities you refuse (e.g. "growth", "monetization", "customer support ops")
   - Reporting relationships you reject (e.g. "reports to growth head")
   - Business types you reject (e.g. "K12 tutoring", "MCN content")
   - Anything else: substring match against JD text → instant OUT

---

## Block 3 — Soft axes (scored 1–5 per JD)

8. **Target title keywords** (`target_title_keywords`) — titles you want to see in the JD header. e.g. "Agent PM", "AI Product Manager", "Developer Tools PM".

9. **Target industries** (`target_industries`) — broad industry buckets you want. e.g. "AI", "DevTools", "Creative Tools", "Embodied Intelligence". Free-text — write in whatever granularity matches your thinking.

10. **Company type preferences** (`company_type_preferences`) — rate each 1–5 (1 = avoid, 5 = strongly prefer):
    - `foreign_company` (foreign-headquartered, English working language likely)
    - `model_company` (frontier AI labs, e.g. Anthropic, Moonshot, MiniMax)
    - `domestic_big_tech`
    - `mid_size`
    - `startup`

11. **Company size preferences** (`company_size_preferences`) — rate each 1–5:
    - `under_50`
    - `50_to_500`
    - `500_to_5000`
    - `over_5000`

12. **Positive vibe anchors** (`vibe_anchors_positive`) — 3–5 specific companies or products you'd love to work at / build like. This anchors the "vibe fit" axis.
    - Examples: "Notion", "Linear", "Duolingo", "Stripe", "Vercel"

13. **Negative vibe anchors** (`vibe_anchors_negative`) — 3–5 companies or products you'd reject or whose energy you actively avoid.
    - Examples: "Zuoyebang", "specific companies you've rejected before"

---

## Summary & confirm

After all 13 are collected, show:

```
Here's what I'll save:

PROFILE
  Years: <n>
  Now: <title @ company>
  Current salary: <value>

HARD GATES
  Salary floor: <value>
  Cities: <list>
  Lifestyle: <tier>
  Red lines: <list>

SOFT AXES
  Target titles: <list>
  Target industries: <list>
  Company type: <map>
  Company size: <map>
  Vibe ✅: <list>
  Vibe ❌: <list>

Confirm and save? (y / edit <field>)
```

If user replies `y` → write to `~/.openclaw/workspace/jd_criteria.md` with `last_updated` = today's ISO date.
If user replies `edit <field>` → re-ask only that field, then re-show summary.
