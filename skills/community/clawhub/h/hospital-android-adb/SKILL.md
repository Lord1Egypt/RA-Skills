---
name: hospital-android-adb
description: Book hospital appointments in Shanghai via USB ADB, through the WeChat 服务号 上海市级医院互联网总平台 (上海医联 / internethospital.shdc.org.cn). Battle-tested 2026-10-14 with a real end-to-end booking (华山医院 皮肤科 普通门诊). Covers the WeChat WebView navigation, the 便民服务 entrance, hospital/department/date-slot selection, the SMS verification gate, and the FLAG_SECURE + keyboard-layout traps. Uses uiautomator2 + RapidOCR, and requires the appium-android-adb base skill (it ships ocr_bridge.py) — ClawHub has no dependency resolver, so install it alongside.
---

# Shanghai Hospital Booking (微信服务号「上海市级医院互联网总平台」)

Book appointments at 37 Shanghai municipal hospitals (华山, 瑞金, 仁济, 第九, 中山, 第六 …)
through the WeChat 服务号 **上海市级医院互联网总平台** — the platform formerly known as
**上海医联**. This doc reflects **one successful end-to-end booking** on a Realme RMX3350
(1080×2400, USB ADB), 2026-10-14.

## ⚠️ The old 上海医联 app is dead

The standalone app `com.wonders.mobile.app.yilian` is **out of service**. Everything moved to
the WeChat 服务号. Do not look for the app package — it will fail. (Version 1.x of this skill
documented that app; that content is obsolete and has been replaced wholesale.)

| Field | Value |
|---|---|
| Package | `com.tencent.mm` (WeChat) |
| Entry | 服务号「上海市级医院互联网总平台」→ bottom menu **便民服务** |
| WebView URL | `internethospital.shdc.org.cn` |
| UI type | WeChat XWeb WebView — **single-page app**, the URL never changes |
| Navigation signal | **OCR only** — there is no activity chain to lean on |
| Input method | clipboard + `keyevent 279` (paste) — see below |

## 🚨 Setup

**Requires the `appium-android-adb` base skill.** It ships `ocr_bridge.py`, which both this
skill's commands and `book_helper.py` load. ClawHub has no dependency resolver, so it will *not*
be installed for you; install it alongside:

```bash
clawhub install appium-android-adb
```

```bash
# venv (one-time, shared with the other *-android-adb skills). The pins ship
# with the base skill — that is the other reason to install it first.
BASE=~/.openclaw/workspace/skills/appium-android-adb   # the base skill (ships ocr_bridge.py)
PY=~/.openclaw/workspace/.venv-adb/bin/python
test -f $BASE/ocr_bridge.py || echo "base skill missing — clawhub install appium-android-adb"
python3 -m venv ~/.openclaw/workspace/.venv-adb        # no-op if it already exists
$PY -m pip install -r $BASE/requirements-adb.txt
```

Keep the screen awake and don't let it sleep mid-flow:

```bash
adb shell svc power stayon true
```

All screen reading / tapping goes through `ocr_bridge.py` from the **appium-android-adb base
skill**: screenshot → RapidOCR → click/swipe → re-OCR verify.
`book_helper.py` (in this skill) wraps the whole flow — prefer it over hand-driving coordinates.
If you keep skills outside the usual directory, `book_helper.py` honours `ADB_OCR_BASE`.

## Preconditions (check BEFORE starting)

1. **User is logged in** on the platform. If a 用户登录 page appears (手机号 / 密码 / 短信验证码),
   the account is usually browser-autofilled — you still need the SMS code from the user.
2. **A 就诊卡 (visit card) is bound.** A card that exists but isn't bound makes 确认预约 fail
   at submit time — *after* you've burned an SMS code. Verify a card is **checked** on the
   预约信息 page before requesting the code.
3. **12306 must not be running** — the accessibility service is shared.
   `adb shell am force-stop com.MobileTicket`
4. **An SMS code is required** and only the user can supply it. Say so up front.

## 🖐️ Chinese & numeric input — clipboard paste

IME switching is blocked on these devices, and this is a WebView anyway. The proven route
(works for Chinese *and* for the numeric SMS code):

```python
d.set_clipboard("华山医院")
subprocess.run(["adb", "shell", "input", "keyevent", "279"])   # PASTE
```

**Focus the field first** (`d.click(x, y)`), or the paste goes nowhere. This is simpler and
more reliable than the long-press → 粘贴 menu dance, and it works for plain digits too.

## 🕳️ Three traps that will cost you the whole session

### 1. FLAG_SECURE blanks your screenshots

When a **password / secure field** is focused, WeChat raises its **安全键盘**
(`adb shell dumpsys window | grep -i secure` shows `SECURE`), and `screencap` returns
**nothing** — a 0-byte file.

`ocr_bridge.shot()` detects this and raises a `RuntimeError` naming FLAG_SECURE, so you
won't have to guess. (Older versions fell through to RapidOCR and died with a cryptic
`cannot identify image file`.)

- Confirm by hand if needed: `ls -la ~/.cache/ocr-bridge/sc.png` — 0 bytes is FLAG_SECURE,
  not a broken cable.
- Recover: tap an inert part of the page to blur the field, wait ~2 s, re-shoot.
  `$BASE/ocr_bridge.py a11y` still reads these screens via the accessibility tree.
- Note: the plain **numeric 验证码 field does *not* trigger this** — only the password field did.
  So the booking flow itself is screenshottable; the login page may not be.

A **uniformly black** capture is a *different* failure: it means the phone is asleep
(`mWakefulness=Dozing`). `shot()` raises for that too, pointing at
`adb shell input keyevent KEYCODE_WAKEUP`. Prevent it with `adb shell svc power stayon true`.

### 2. The keyboard reflows the whole page — never reuse stale coordinates

Focusing the 验证码 input scrolls the page so the button sits above the keyboard:

| State | 确认预约 at |
|---|---|
| Keyboard **up** | ≈ (540, **1480**) |
| Keyboard **down** | ≈ (540, **2310**) |

Tapping the wrong one is a no-op at best. **Always re-OCR right before the tap** and locate
the button from the fresh text box, then click its centre:

```python
b = [x for x in shot() if '确认预约' in x[0]][0]
d.click((b[1] + b[3]) // 2, (b[2] + b[4]) // 2)
```

`BOOK_HELPER`'s `submit` command does exactly this.

### 3. BACK navigates — it does not just close the keyboard

`adb shell input keyevent 4` pops the WebView's history (we lost the booking page this way
twice, landing back on the WeChat chat / search screen). ESC (111) does nothing.
To dismiss the keyboard, tap an inert area — or simply don't: tapping 确认预约 works fine
with the keyboard up.

**If the WebView does close**: re-enter via the 服务号 bottom menu **便民服务** (or the
便民服务 shortcut button on the WeChat search-result card), then re-run `reach`.
Nothing is lost except the current page — the booking hasn't happened until 预约成功 shows.

## Booking Flow (proven end-to-end)

```bash
BASE=~/.openclaw/workspace/skills/appium-android-adb   # the base skill (ships ocr_bridge.py)
PY=~/.openclaw/workspace/.venv-adb/bin/python
$PY book_helper.py reach                        # 便民服务 → 预约信息, then requests the SMS
# ...user reads the code off their phone...
$PY book_helper.py code <6-digit>               # paste code into the field
$PY book_helper.py submit --confirm "华山医院/皮肤科/2026-10-21 上午"
```

`reach` stops at the 预约信息 page **on purpose** — it never submits. Submission is a
separate command that **requires `--confirm`**, and the value must contain the hospital,
department, date and 上午/下午 as OCR'd from the page *at submit time*. Running `submit`
with no `--confirm` prints exactly what it expects and exits without tapping:

```
REFUSING TO SUBMIT — no --confirm given.
Show the above to the user, get their explicit yes, then re-run with:
  book_helper.py submit --confirm "华山医院/皮肤科/2026-10-21星期三上午"
```

The flag is an **acknowledgement, not a rubber stamp** — it cannot be produced without
having actually read (and shown) the confirmation page. This gate exists because the
v2.0.0 draft was flagged in ClawHub review for allowing an unconditional submit.

`book_helper.py` reads `HOSPITAL_DATE` / `HOSPITAL_AMPM` from the environment (defaults
`2026-10-21` / `上午`) so you can retarget without editing the file.

### Step-by-step (what `reach` does)

**1. Enter the platform.** WeChat 服务号「上海市级医院互联网总平台」→ bottom menu 便民服务
at ≈ (300, 2319). (If you're on the WeChat global-search result card instead, its
便民服务 shortcut sits at ≈ (385, 812).) Wait for 首页 (上海·医联 · 融合37家市级医院).

**2. 预约挂号** — 2nd icon of the first 诊疗服务 row, ≈ (540, 942).
A **location-permission dialog** may appear on first entry: 暂不提供 / 同意.
暂不提供 is fine — the platform is Shanghai-only. Then the 医院 list loads.

**3. Search the hospital.** Tap the search box 搜医院、科室、医生 ≈ (540, 316) → the 搜索
page shows 历史搜索 / 热门搜索. Pick the 华山医院 chip if present (≈ (164, 552)); otherwise
focus the box and paste the name. A pasted value may not auto-submit — tap the keyboard's
**搜索** key (≈ (1004, 2272)) to fire the query. Results: `医院(1)` → 华山医院 card.

**4. Open the hospital card** ≈ (540, 700) → 门诊科室 · **请选择就诊院区**.

**5. Pick the campus.** 华山医院 lists five sites — 华山医院 (总院), 浦东院区, 江苏路分部,
虹桥院区, 宝山院区. The rows start at y ≈ 442 and are ≈ 130 px apart, so **read the label
you're about to tap rather than trusting arithmetic**:

```python
row = [x for x in shot() if x[0].strip() == "华山医院"][0]   # exact match = 总院 row
d.click((row[1] + row[3]) // 2, (row[2] + row[4]) // 2)
```

皮肤科 普通门诊 is at the **总院** — verified by the address line on the next screen reading
**华山路493号** (静安区). Always confirm that address before continuing; the campuses lead to
completely different slot lists.

**6. Choose the clinic type tab**, then the department. Tabs 专家门诊 / 专病门诊 / 普通门诊
at y ≈ 683; 普通门诊 is the 3rd at x ≈ 887. The left department list then changes —
皮肤科 sits in the upper-middle (y ≈ 1828 in the default scroll position).

**7. Tap the matching entry in the right-hand panel** (≈ (664, 816)) to drill in.

**8. Enter the appointment type.** The panel now shows e.g. `皮肤科 | 有号` +
`普通门诊-[医联平台] ¥25` — tap the row ≈ (540, 584) to open the schedule list.

**9. Find the date slot.** See the schedule structure below.

**10. 预约信息 page** — verify, then request the code with 获取验证码 ≈ (914, 1038).
The button flips to a **countdown (e.g. `57秒`)** — that countdown is your proof the SMS
actually went out. No countdown ⇒ the tap didn't register; tap again.

**11. Enter the code**, verify the field shows 6 digits, then `submit`.

**12. Success page = 预约详情 / 预约成功** (green clipboard icon, 祝您身体健康), showing
医院 / 科室 / 类型 / 就诊日期 / 就诊时段 / 就诊人 / 金额 and the **就诊号**.

## Schedule List Structure

Under the 预约挂号 header the list renders one block per half-day:

```
2026-10-21  星期三 上午          [有号]
普通门诊-[皮肤科]  ¥25
```

- **Order within a date is 下午 first, then 上午.** Don't assume morning is on top.
- The date text sits at x ≈ 48; the 星期X 上午/下午 label on the same visual row at x ≈ 300.
- The **有号 button** is at x ≈ 903–990, ~45 px below the date line's top.
- Row pitch ≈ 230 px. Dates with no availability simply have **no 有号 button**.
- Scroll with `$BASE/ocr_bridge.py swipe up --scale 0.3` (≈ 2 rows per swipe); track position by
  reading the date texts, exactly like the 12306 `deps()` discipline.

**Matching a target row (the form that works):**

```python
d = [x for x in shot() if TARGET_DATE in x[0]][0]              # the date text box
amp = [x for x in shot() if WANT in x[0]                       # 上午 / 下午
       and x[1] > d[1] and abs(x[2] - d[2]) < 70][0]           # same visual row
hav = [x for x in shot() if x[0].strip() == "有号"
       and x[2] > d[2] and x[2] < d[4] + 300                   # just below the date
       and x[1] > 700][0]
```

Clamping on the date box's own y-band is what stops you from grabbing the 有号 belonging to
the row *below* (the 下午 row that follows the 上午 row).

## Booking Window

Measured 2026-10-14: selectable dates started at the next day (10-15) and ran at least to
10-31; **18 days out (11-01) was not bookable**. Treat the window as roughly **2–3 weeks**
and confirm the target date is actually on the list before promising it to the user — ask
for a fallback date up front.

## Platform Rules (from the success receipt — tell the user these)

- Bring the **original 身份证** (or 户口本 for children) to 挂号; 就诊号 and 诊间/诊位 are on the receipt.
- ⚠️ **超过预约时段不保留号源** — arriving late forfeits the slot.
- ⚠️ **挂号成功后不得退号** — there is no refund.
- To cancel, **撤销 before the visit day**; otherwise it records as 失约 (no-show), and
  **more than two no-shows blocks further booking**.
- Same 身份证号 may 撤销 only **6 times per month**.
- 病历本 must be brought; blank ones are available on each floor.

## Optional Helpers

| Command | Effect |
|---|---|
| `book_helper.py shot` | screenshot + OCR dump (recovery when lost) |
| `book_helper.py slot` | locate the current target date/time 有号 box, no clicking |
| `book_helper.py reach` | full navigation → 预约信息, then request SMS |
| `book_helper.py code <digits>` | paste the SMS code into the field |
| `book_helper.py submit` | **refuses** — prints the page's details and the `--confirm` string to use |
| `book_helper.py submit --confirm "<details>"` | validates the details against the live page, then taps 确认预约 |

## Decision Tree

```
OCR markers:
  ├─ 上海·医联 / 融合37家市级医院   → HOME — tap 预约挂号
  ├─ 搜医院、科室、医生             → HOSPITAL LIST — search box → hospital
  ├─ 历史搜索 / 热门搜索            → SEARCH — chip or paste + keyboard 搜索
  ├─ 请选择就诊院区                 → CAMPUS PICKER — pick row (总院 = y442)
  ├─ 普通门诊/专病门诊/专家门诊     → DEPARTMENTS — tab, then dept, then right panel
  ├─ 普通门诊-[医联平台] ¥25        → APPT TYPE — tap row → schedule
  ├─ 2026-mm-dd 星期X 上午/下午     → SCHEDULE — scroll to date → 有号
  ├─ 预约信息 / 选择就诊卡          → CONFIRM — verify, 获取验证码, code, submit
  ├─ 预约详情 / 预约成功            → SUCCESS — report 就诊号 etc.
  ├─ 连接错误 / 重新加载            → RELOAD — tap 重新加载 (≈ (542, 1596)); may bounce
  │                                    you back to the campus picker
  ├─ 用户登录                       → LOGIN GATE — needs SMS; screenshots may be blank
  └─ unknown                        → book_helper.py shot, dump OCR, re-orient
```

## Common Pitfalls (all hit in production)

1. **The app is gone** — `com.wonders.mobile.app.yilian` is decommissioned. WeChat only.
2. **Screenshots go 0-byte** on the login page's secure keyboard (FLAG_SECURE). Not a cable fault.
3. **Coordinates shift when the keyboard opens/closes** — re-OCR before every decisive tap.
4. **BACK leaves the page** — don't use it to hide the keyboard.
5. **The WebView closes on its own** (session/back). Re-enter via 便民服务; nothing is lost.
6. **就诊卡 not bound ⇒ submit fails** — and you've already spent an SMS code. Check first.
7. **The 获取验证码 countdown is the confirmation** that the SMS was actually sent.
8. **Pasted text may not auto-submit** in the search box — press the keyboard 搜索 key.
9. **The SMS code is short-lived** — have the user ready before you request it; draft the
   request only when you're already on the 预约信息 page.
10. **One tap is enough** for 确认预约 even with the keyboard up. After tapping, a spinner
    appears — **do not tap again**; poll for 预约详情 / 预约成功 (~10-20 s).
11. **Never put patient data in logs, screenshots or commits** — 就诊人 names, ID numbers and
    the account phone number are all PII. Report them to the user, then drop them.
12. **Connection errors are transient** — 重新加载 is enough; it may drop you back to the
    campus picker, which is a fine place to resume.

## 🛡️ Safety & Consent

- Use only when the user explicitly asks to book an appointment — never speculatively.
- **Confirm before submitting — and it is enforced, not just advised.** Show the user
  医院 / 科室 / 类型 / 就诊日期 / 就诊时段 / 就诊卡 / 费用, wait for an explicit yes, and only
  then pass `--confirm`. Submission creates a real appointment that **cannot be cancelled
  for a refund** and counts toward the 失约 limit.
- **The SMS code must come from the user.** Never guess or brute-force it. Ask, and pass it
  straight through — do not log it.
- **Let the user choose the 就诊卡.** The default selection can differ from the card the user
  used last time (it flipped between runs in our session after a rebinding).
- Screenshots may contain PII; they live in a private 0700 dir (`~/.cache/ocr-bridge`),
  auto-purged after 1 hour. `$BASE/ocr_bridge.py clean` purges immediately.

## Files

- `book_helper.py` — navigates the flow; **deliberately stops short of submitting**
- Uses `ocr_bridge.py` from the **appium-android-adb base skill** for all screen I/O
  (resolved by `book_helper._load_ocr_bridge()`; override with `ADB_OCR_BASE`)
- uiautomator2 only — Appium is not needed (and is dead on Realme: WRITE_SECURE_SETTINGS blocked)
