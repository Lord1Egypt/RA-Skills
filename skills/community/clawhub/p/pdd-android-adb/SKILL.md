---
name: pdd-android-adb
description: Buy products on the Pinduoduo (拼多多) Android app via USB ADB. Battle-tested 2026-08-30 (bought 健生大英语簿【5本】¥5.9 end-to-end incl. wallet payment and 直接免拼). Primary method: direct uiautomator2 + RapidOCR via ocr_bridge.py, shipped by the appium-android-adb base skill (install it alongside — ClawHub has no dependency resolver). Covers search-with-clear, spec selection & verification, FLAG_SECURE payment pages (a11y tree as the eye), PIN-pad typing, fingerprint handoff, and the 免拼 flow.
---

# Pinduoduo (拼多多) Shopping — Android

PDD-specific knowledge, workflows, and pitfalls, from a **successful end-to-end purchase** (2026-08-30, Realme RMX3350 1080x2400). App package: `com.xunmeng.pinduoduo`.

## 🚨 Setup (proven)

**Requires the `appium-android-adb` base skill.** It ships `ocr_bridge.py` — the OCR loop every
command below runs. ClawHub has no dependency resolver, so it will *not* be installed for you;
install it alongside:

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
$PY -c "import uiautomator2 as u2; d=u2.connect(); d.app_start('com.xunmeng.pinduoduo')"
```

Same stack as 12306-android-adb: the OCR loop (`ocr_bridge.py` in the **appium-android-adb base skill**) for everything, a11y tree where screenshots fail. Appium is dead on Realme (WRITE_SECURE_SETTINGS blocked) — don't try it.

## Purchase Flow (proven end-to-end)

### Step 1: Search — clear the box BEFORE pasting

The search box may already hold text (PDD keeps the last query). **Pasting over it concatenates** — clear first, then clipboard + long-press 粘贴 (IME switching is blocked on Realme):

```bash
BASE=~/.openclaw/workspace/skills/appium-android-adb   # the base skill (ships ocr_bridge.py)
PY=~/.openclaw/workspace/.venv-adb/bin/python
$PY $BASE/ocr_bridge.py type 上海健生英语练习簿 --x 500 --y 180  # clears focused EditText, sets clipboard, long-presses
$PY $BASE/ocr_bridge.py dump                                    # find 粘贴
$PY $BASE/ocr_bridge.py tap-text 粘贴                           # paste
$PY $BASE/ocr_bridge.py tap-text 搜索                           # submit search
```

### Step 2: Pick the right product & spec (规格)

- Search results are **ad-mixed** — open candidates and check their spec panels.
- Open the spec panel via the **发起拼单** button on the product page.
- Spec options are chips like `大英语簿【5本】¥5.9` / `20本装` — verify you're on the right quantity/size before proceeding.

**Verifying which chip is selected** (OCR is ambiguous here):
1. Pixel-sample the chip borders with PIL (`img.getpixel`) — the selected chip has a highlight border.
2. **Authoritative: a11y tree** — the selected node carries `selected="true"`:

```bash
BASE=~/.openclaw/workspace/skills/appium-android-adb   # the base skill (ships ocr_bridge.py)
PY=~/.openclaw/workspace/.venv-adb/bin/python
$PY $BASE/ocr_bridge.py a11y-selected
```

### Step 3: Submit → Payment (FLAG_SECURE page)

- Tap 提交订单 (or the bottom-bar price button) → PayConfirmActivity.
- **The payment page sets FLAG_SECURE**: `screencap` returns black/0-byte files. **The a11y tree still works** — it's the only eye here:

```bash
BASE=~/.openclaw/workspace/skills/appium-android-adb   # the base skill (ships ocr_bridge.py)
PY=~/.openclaw/workspace/.venv-adb/bin/python
$PY $BASE/ocr_bridge.py a11y          # page text + bounds
```

- 多多钱包 PIN pad layout (from a11y bounds on 1080x2400; re-read per device):
  - digits 1-9: three rows at x=180/540/900, y=1818/1973/2127; 0 at (540, 2282)
  - type the PIN with `d.click` per digit (user supplies the PIN), then check the tree again.
- **Fingerprint/face verification is manual** — pause and ask the user to touch the sensor, then re-check state.

### Step 4: 免拼 (skip group-buy) — do it right after payment

PDD orders start as 拼团中 ("差1人"). The buyer can convert them directly:

```bash
BASE=~/.openclaw/workspace/skills/appium-android-adb   # the base skill (ships ocr_bridge.py)
PY=~/.openclaw/workspace/.venv-adb/bin/python
$PY $BASE/ocr_bridge.py a11y-tap 直接免拼     # click the button found in the a11y tree
```

Success state: 免拼成功 / 打包中 (seller packing). Report the order details (product, spec, price, shop, payment method) to the user.

## Decision Tree

```
OCR/a11y markers:
  ├─ search box + 搜索           → SEARCH — clear → paste → search
  ├─ 发起拼单 / 立即购买          → PRODUCT — tap to open spec panel
  ├─ spec chips + price          → SPEC PANEL — select → verify a11y-selected
  ├─ PayConfirmActivity (a11y)   → PAYMENT — PIN via pad clicks → fingerprint (user)
  ├─ 拼团中 / 差1人              → ORDER — a11y-tap 直接免拼
  ├─ 免拼成功 / 打包中            → SUCCESS — report
  └─ unknown                     → OCR dump; on FLAG_SECURE pages use a11y
```

## 🛡️ Safety & Consent

- Use only when the user explicitly asks to buy something on PDD — never speculatively.
- **Confirm before submitting**: show the user the product, spec, quantity,
  price and shop, and wait for confirmation before tapping 提交订单.
- Wallet PIN is provided by the user at payment time and used only in memory
  to tap the pad; fingerprint/face verification is ALWAYS done by the user.
- Screenshots may contain personal data; they are stored in a private 0700 dir
  (`~/.cache/ocr-bridge`) — see appium-android-adb for cleanup.

## Common Pitfalls (hit in production)

1. **Pasting without clearing** — old query text stays and concatenates. `$BASE/ocr_bridge.py type` clears by default.
2. **Screencap fails on payment pages** — FLAG_SECURE: 0-byte/black screenshots. Use `a11y`/`a11y-tap` instead of OCR there.
3. **OCR can't tell selected specs apart** — use `a11y-selected` (`selected="true"`), optionally pixel-check borders with PIL.
4. **Don't automate the fingerprint** — that's the user's step; pause and ask.
5. **免拼 is separate from payment** — after paying, the order sits in 拼团中 until you tap 直接免拼. Do it before reporting success.
6. **Mixed quantity specs** — the same listing offers 20本装 and 5本装; confirm the spec chip text matches the user's request before submitting.
7. **Ad results** — the first results may be promoted items; prefer items with 已拼 counts and check the shop.
