---
name: hospital-android-adb
description: Automate hospital appointment booking on the 医联 (Yilian) Android app using uiautomator2. Covers hospital search (with Chinese text input), department selection, date/time slot selection, and confirmation flow. Uses uiautomator2 only — no Appium needed.
---

# Hospital Appointment Booking (医联 / Yilian)

Automate doctor appointment booking on the 医联 Android app (`com.wonders.mobile.app.yilian`). The app uses native Android views (no UC WebView issues). Use **uiautomator2** for all interactions — Appium is NOT needed.

## Before Any Action

```python
import uiautomator2 as u2
d = u2.connect()
```

Kill 12306 first if running — both apps can't share the accessibility service:

```python
import subprocess
subprocess.run(["adb", "shell", "am", "force-stop", "com.MobileTicket"])
```

Launch 医联:

```python
subprocess.run(["adb", "shell", "monkey", "-p", "com.wonders.mobile.app.yilian",
                "-c", "android.intent.category.LAUNCHER", "1"])
import time; time.sleep(5)
```

## App Info

| Field | Value |
|-------|-------|
| Package | `com.wonders.mobile.app.yilian` |
| Activity chain | `MainActivity` → `SearchActivity` → `HospitalHomePageActivity` → `DepartmentActivity` → `SpecialDiseaseActivity` → `SchedulingActivity` → `ReserveInfoActivity` |
| UI type | Native Android (RecyclerView, LinearLayout, TextView) — no WebView issues |
| Input method | `el.set_text("华山医院")` via AccessibilityService — no IME needed |

## ⚠️ Key Technical Constraints

### Chinese Text Input: Use `set_text()`

`d.send_keys("华山医院")` fails (clipboard permission denied). `adb shell input text` fails (NullPointerException on Chinese chars). **Use `set_text()` instead:**

```python
# Focus the field, then set text via AccessibilityService ACTION_SET_TEXT
el = d(className='android.widget.EditText')
el.click()         # focus first
time.sleep(0.5)
el.set_text("华山医院")  # bypasses IME/clipboard entirely
```

This works because `set_text()` uses the Android AccessibilityService's `ACTION_SET_TEXT` action, which directly injects text into the focused EditText without needing an IME or clipboard permissions.

### Element Clickability

Many department/button TextViews have `clickable=false`. Their **parent container** (LinearLayout/FrameLayout) has `clickable=true`. Always check parent containers by bounds containment:

```python
for p in root.iter('node'):
    if p.get('clickable') == 'true' and parent_bounds_contains(p, child_bounds):
        # This is the actual clickable target
```

### Schedule Data Loading Delay

The `SchedulingActivity`` RecyclerView takes **2-10 seconds** to populate with available dates. After tapping a slot, poll the dump for date texts like `"2026-06-01"` until they appear.

## Screen Reading

### Primary: uiautomator2 dump_hierarchy + XML parsing

```python
xml = d.dump_hierarchy()
root = __import__('xml.etree.ElementTree', fromlist=['ElementTree']).fromstring(xml.encode())
```

### Helper: find clickable elements with text

```python
import re
for node in root.iter('node'):
    text = node.get('text', '').strip()
    bounds = node.get('bounds', '')
    clickable = node.get('clickable')
    if text and clickable == 'true':
        nums = re.findall(r'\d+', bounds)
        if len(nums) >= 4:
            h = int(nums[3]) - int(nums[1])
            if h > 20:  # meaningful height
                print(f"'{text}' at {bounds}")
```

### Helper: find clickable parent by bounds

```python
def find_clickable_parent(root, child_bounds):
    child_nums = __import__('re').findall(r'\d+', child_bounds)
    if len(child_nums) < 4: return None
    cx1, cy1, cx2, cy2 = int(child_nums[0]), int(child_nums[1]), int(child_nums[2]), int(child_nums[3])
    for p in root.iter('node'):
        if p.get('clickable') != 'true': continue
        pn = __import__('re').findall(r'\d+', p.get('bounds', ''))
        if len(pn) >= 4:
            px1, py1, px2, py2 = int(pn[0]), int(pn[1]), int(pn[2]), int(pn[3])
            if px1 <= cx1 and py1 <= cy1 and px2 >= cx2 and py2 >= cy2:
                return p
    return None
```

### Fallback: Screenshot + OCR

```python
d.screenshot('/tmp/screen.png')
import pytesseract
from PIL import Image
text = pytesseract.image_to_string(Image.open('/tmp/screen.png'),
    lang='chi_sim', config='--psm 6')
```

## Booking Flow

### Step 1: Home Page — Search for Hospital

Home page UI:
- "搜医院、科室、医生" — search box (clickable) at top
- "当日挂号" — same-day appointments
- "预约挂号" — appointment booking label (NOT clickable)

```
d(text='搜医院、科室、医生').click()
time.sleep(2)
```

On the search page, type the hospital name:

```python
el = d(className='android.widget.EditText')
el.click()
time.sleep(0.5)
el.set_text("华山医院")  # set text via AccessibilityService
time.sleep(2)            # wait for suggestions
```

After typing, the search results / suggestions appear. Tap the hospital card:

```python
xml = d.dump_hierarchy()
if '华山医院' in xml:
    # Tap at hospital card position
    d.click(540, 1033)  # center of hospital card
```

### Step 2: Hospital Card → Tap to Enter

On the search result page, tap the hospital card to go to its detail page:

```python
# Look for the hospital card in the results
for node in root.iter('node'):
    if '华山医院' in node.get('text', ''):
        parent = find_clickable_parent(root, node.get('bounds', ''))
        # Tap parent's center
        ...
```

This navigates to `HospitalHomePageActivity`.

### Step 3: Find "预约挂号" Icon

On the hospital detail page (`HospitalHomePageActivity`), there are icon buttons:
- 预约挂号 at column 2 (x: 270-540) in the first row
- 当日挂号 at column 3 (x: 540-810) in the first row

```python
# The "预约挂号" icon is in the clickable container:
# Row 1: [0,1279][270,1522], [270,1279][540,1522], [540,1279][810,1522], [810,1279][1080,1522]
# Column 2 (270-540) = 预约挂号
d.click(405, 1400)  # center of second icon
```

This navigates to `DepartmentActivity`.

### Step 4: Select Appointment Type Tab + Department

On `DepartmentActivity`:
- Tabs at top: "专家门诊", "专病门诊", "普通门诊" (text, NOT clickable — tap their clickable parent)
- Department list shows available departments

First select the appointment type tab, then tap the target department:

```python
# Tap "普通门诊" tab
d.click(900, 516)  # center of third tab

# The department list refreshes. Now find "皮肤科":
xml = d.dump_hierarchy()
root = __import__('xml.etree.ElementTree', fromlist=['ElementTree']).fromstring(xml.encode())
for node in root.iter('node'):
    if node.get('text', '').strip() == '皮肤科':
        parent = find_clickable_parent(root, node.get('bounds', ''))
        if parent:
            nums = __import__('re').findall(r'\d+', parent.get('bounds', ''))
            cx = (int(nums[0]) + int(nums[2])) // 2
            cy = (int(nums[1]) + int(nums[3])) // 2
            d.click(cx, cy)
```

This may navigate to `SpecialDiseaseActivity` (department detail).

### Step 5: Select Appointment Entry

On `SpecialDiseaseActivity`, find the appointment type entry for the department:

```python
# Look for entries like "普通门诊-[医联平台] ¥25" with "有号" (available)
for node in root.iter('node'):
    t = node.get('text', '').strip()
    if '有号' in t or '普通门诊' in t:
        parent = find_clickable_parent(root, node.get('bounds', ''))
        if parent:
            # Tap to navigate to SchedulingActivity
```

### Step 6: Select Date and Time Slot

On `SchedulingActivity` (`activity == ".patient.ui.hospital.SchedulingActivity"`):

The RecyclerView takes 2-10 seconds to populate. **Poll for data:**

```python
# Wait for schedule data to load
for i in range(15):
    time.sleep(1)
    xml = d.dump_hierarchy()
    if '2026-06-01' in xml:  # target date appeared
        break

# Target date will show as: "2026-06-01  星期一 上午"
# Find its clickable parent and tap
root = __import__('xml.etree.ElementTree', fromlist=['ElementTree']).fromstring(xml.encode())
for node in root.iter('node'):
    if node.get('text', '').strip() == '2026-06-01  星期一 上午':
        parent = find_clickable_parent(root, node.get('bounds', ''))
        ...
```

This navigates to `ReserveInfoActivity`.

### Step 7: Confirm Appointment

On `ReserveInfoActivity`, verify all details:
- 医院: 华山医院
- 科室: 皮肤科
- 类型: 普通门诊
- 就诊日期: 2026-06-01 星期一 上午
- 就诊时段: 07:45-08:00 (changeable by tapping)

Patient selection: tap the patient name to select/deselect. Captcha section:
- "获取验证码" — tap to request SMS code
- "请输入验证码" — tap to enter code
- "确定预约" at bottom — tap to finalize

**SMS verification code is required** — inform the user to check their phone.

```python
# Tap 确定预约 after captcha is entered
d.click(540, 2292)
```

## Activity Flow Reference

| # | Activity | What You See |
|---|----------|-------------|
| 1 | `.patient.ui.MainActivity` | Home page: search box, 当日挂号 |
| 2 | `.patient.ui.hospital.search.SearchActivity` | Hospital search results / suggestions |
| 3 | `.patient.ui.hospital.HospitalHomePageActivity` | Hospital detail: 预约挂号 icon |
| 4 | `.patient.ui.hospital.depart.DepartmentActivity` | Department list with tabs |
| 5 | `.patient.ui.hospital.SpecialDiseaseActivity` | Department detail: appointment type entry |
| 6 | `.patient.ui.hospital.SchedulingActivity` | Date/time slot picker (RecyclerView) |
| 7 | `.patient.ui.hospital.ReserveInfoActivity` | Confirmation: details, captcha, 确定预约 |

## Key Elements Reference

| Element | Where | Notes |
|---------|-------|-------|
| 搜医院、科室、医生 | Home page | Clickable search box |
| 预约挂号 (icon) | Hospital page | 2nd icon in row 1 |
| 当日挂号 | Hospital page | 3rd icon in row 1 |
| 普通门诊 | Department page | Tab, 3rd position |
| 皮肤科 / other dept | Department page | In scroll list |
| 有号 | Various | Indicates availability |
| 确定预约 | Reserve page | Submit button |
| 获取验证码 | Reserve page | Request SMS |
| 请输入验证码 | Reserve page | Captcha input |

## Common Pitfalls

1. **12306 conflict**: Can't run both apps' automation simultaneously. Force-stop 12306 first.
2. **Chinese text input**: NOT supported via ADB. Use hot search suggestions or pre-existing text.
3. **Schedule loading delay**: RecyclerView populates asynchronously. Poll for date text (up to 15s).
4. **Elements with clickable=false**: TextViews may not be clickable — tap their parent container instead.
5. **ADB disconnects**: USB can drop. Run `adb kill-server && adb start-server` to recover.
6. **SMS captcha**: The user must enter the verification code manually.
7. **Patient selection**: Verify correct patient is checked before confirming.

## Decision Tree

```
d.dump_hierarchy() + check activity:
  ├─ activity == "MainActivity" → HOME
  │   → tap search box → tap hot suggestion
  ├─ activity == "SearchActivity" → SEARCH RESULTS
  │   → tap hospital card
  ├─ activity == "HospitalHomePageActivity" → HOSPITAL PAGE
  │   → tap 预约挂号 icon (2nd icon, 1st row)
  ├─ activity == "DepartmentActivity" → DEPARTMENTS
  │   → select tab (普通门诊) → tap department name
  ├─ activity == "SpecialDiseaseActivity" → DEPT DETAIL
  │   → tap available appointment entry (有号)
  ├─ activity == "SchedulingActivity" → DATE PICKER
  │   → wait for data → tap target date/time slot
  ├─ activity == "ReserveInfoActivity" → CONFIRMATION
  │   → verify details → get SMS captcha → tap 确定预约
  └─ otherwise → unknown state, take screenshot
```

## Files

- Uses `uiautomator2` Python library only (no Appium)
- No app-specific scripts needed
