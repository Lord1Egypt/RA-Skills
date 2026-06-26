# 🏨 Case tutorial: Build an Airbnb competitor price-tracking bot with zero code

This walkthrough shows how to use the OpenClaw-RPA skill with a short plain-language brief so the agent opens a real browser, pulls competitor prices and ratings from Airbnb, and appends everything into a Word report.

https://github.com/user-attachments/assets/829a0cf4-95e3-4dc0-9701-e0f40dea4f65

**Why it matters:** you record once and get a generated Python script. Every later run executes that script directly — **very fast, zero token spend, and no LLM hallucinations on replay.**

---

## 🛠️ Step 1: Install and prepare

1. **Install the OpenClaw RPA skill**  
   If you have not installed it yet, add the skill in OpenClaw:
   * **Skill URL:** [https://clawhub.ai/laziobird/openclaw-rpa](https://clawhub.ai/laziobird/openclaw-rpa)
   * Or follow the GitHub homepage for CLI install.

2. **Pick a capable model**  
   For reliable page understanding and codegen, switch OpenClaw to one of:
   * Minimax 2.7
   * Gemini Pro 3.0 or newer
   * Claude Sonnet 4.6

---

## 🎬️ Step 2: Send the prompt and start recording

Open the OpenClaw chat (RPA skill enabled) and paste **everything below** to the agent.

> **Tips**
> * The first line `#RPA` is the trigger.
> * The second line is the **task name** (here `AirbnbPriceTracker`); it becomes the generated script name.
> * The third line `F` is the capability code (browser + Word table).

```text
#RPA
AirbnbPriceTracker
F

[var]
query_time = ### Current local time to the minute, format MM/DD HH:mm ###

output_path = '~/Desktop/Airbnb/hotelCompare.docx'

urls:
  https://www.airbnb.cn/rooms/1517880824760006835?location=%C5%8Csaka-shi%2C%20%C5%8Csaka-fu%2C%20JP&search_mode=regular_search&adults=1&check_in=2026-04-20&check_out=2026-04-27
  https://www.airbnb.cn/rooms/1520897875971878894?location=%C5%8Csaka-shi%2C%20%C5%8Csaka-fu%2C%20JP&search_mode=regular_search&adults=1&check_in=2026-04-20&check_out=2026-04-27
  https://www.airbnb.cn/rooms/1239558906468787551?check_in=2026-04-20&check_out=2026-04-27&location=%E6%96%B0%E4%BB%8A%E5%AE%AB%E7%AB%99&search_mode=regular_search&adults=1

stay_dates = '2026-04-20 to 2026-04-27'

[do]
1. Loop over ${urls} and open each URL in order.
2. On each listing page extract: listing name, room name, price, rating; also attach ${query_time} and ${stay_dates}.
3. Build one table with headers: Listing name | Room name | Price | Rating | Query time | Stay dates
4. Append the table to the end of the Word file at ${output_path} and save (create the file if it does not exist).

[rule]
All ${urls} are from the same site; reuse one loop pattern.
```

> **Bilingual note:** the Chinese version of this tutorial uses the task name `Airbnb比价追踪` and the variable label `入住时间` for stay dates; behavior is the same — pick one naming style and keep it consistent in `#rpa-run`.

---

## ⏳ Step 3: Wait for recording and codegen

After you send the brief, the agent will:

1. Launch a real Chrome instance in the background.
2. Visit each Airbnb URL you listed.
3. Read the page (including vision where needed) and capture price, rating, and related fields.
4. Finish recording and leave a standalone Python script such as `AirbnbPriceTracker.py` under your `rpa/` folder.

*(Recording uses some tokens once; replay does not.)*

![Airbnb recording screenshot](https://github.com/user-attachments/assets/09023f4c-aece-4793-afc3-fdddcbbc5cfb)

---

## 🚀 Step 4: Daily runs (zero-cost replay)

After the script exists, you **do not** need to paste the long prompt again for routine checks.

**Option A — quick run from chat**

```text
#rpa-run:AirbnbPriceTracker
```

If you kept the Chinese task name from the other doc, use `#rpa-run:Airbnb比价追踪` instead.

OpenClaw (or a connected Feishu/Lark bot) runs the script in the background; within seconds the Word file on your Desktop updates.

**Option B — run locally or on a schedule**

```bash
python3 rpa/AirbnbPriceTracker.py
```

Use the actual filename your recording produced. Schedule with cron, Task Scheduler, etc., if you want a fixed daily time.

---

## 📊 Expected output

Open `~/Desktop/Airbnb/hotelCompare.docx`. You should see a clean table; each run **appends** new rows at the end so you can compare history.

| Listing name | Room name | Price | Rating | Query time | Stay dates |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Namba cozy stay | Deluxe double | ¥450 | 4.8 | 04/14 10:30 | 2026-04-20 to 2026-04-27 |
| Shinsaibashi apartment | Studio | ¥380 | 4.9 | 04/14 10:30 | 2026-04-20 to 2026-04-27 |
| Shin-Imamiya machiya | Tatami room | ¥520 | 4.7 | 04/14 10:30 | 2026-04-20 to 2026-04-27 |

*(Sample rows for illustration; a real run writes live data from the pages.)*
