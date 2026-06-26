---
name: kpop-tracker
description: >
  Track K-Pop idol updates including comebacks, albums, concerts, solo activities, merch,
  and official YouTube content with 3-stage search architecture (Official accounts → Media → Taiwan fans)
  and automatic Chinese member Weibo monitoring. Use when the user asks about idol schedules, comeback info,
  album details, concert dates, merchandise, collaboration goods, member solo activities,
  or wants to check for new updates from their followed artists. Also triggers on "追星",
  "回歸", "專輯", "演唱會", "周邊", "偶像動態", "idol updates", "comeback schedule",
  "團綜", "solo", "聯名", "巡演", "搶票".
metadata:
  openclaw:
    requires:
      bins:
        - browser
      primaryEnv: none
    version: "2.1.0"
    changelog: "重大更新：3階段搜尋架構 + 中國成員微博監控 + 來源標註系統"
---

# K-Pop Tracker Skill

Track K-Pop idol updates from official and fan sources, summarized in Traditional Chinese.

## Config

`<workspace>/kpop-tracker/config.json` — artist list and sources.

If the file doesn't exist, create it with the user's first artist. Schema:

```json
{
  "artists": [
    {
      "name": "顯示名稱",
      "group": "團名（solo 可省略）",
      "keywords": ["搜尋關鍵字", "韓文名", "英文名"],
      "chinese_members": [
        {
          "name": "中文名",
          "weibo": "@weibo_account"
        }
      ],
      "sources": {
        "instagram": "https://www.instagram.com/official_account/",
        "x": "https://x.com/official_account",
        "youtube": "https://www.youtube.com/@official_channel",
        "weverse": "https://weverse.io/community-name/feed",
        "berriz": "https://berriz.in/group-name",
        "taiwan_fan_sources": [
          "台灣粉絲團FB或IG"
        ]
      }
    }
  ],
  "last_check": null,
  "check_history_file": "kpop-tracker/check_history.json"
}
```

### Managing Artists

- **Add**: Ask user for name, group, keywords, social links. Append to `artists[]`.
- **Remove**: Remove by name or group.
- **List**: Show current tracked artists.
- Don't require all sources — user fills in what they have.

## Information Categories (6 Fixed Categories)

Every check MUST output exactly these 6 categories per group, in this order.

### 1. 🎵 團體回歸

What to find:
- Latest comeback date, album/single release date
- New song MV or audio on YouTube this week
- Concept photos, tracklist, teaser schedule

Output rules:
- List confirmed comeback date (or "目前無回歸消息")
- If new MV/song released this week → include YouTube link
- If comeback is announced but not yet released → show schedule/timeline

### 2. 💿 專輯 & 周邊商品

Split into two sub-sections: **專輯** and **周邊/聯名商品**.

#### 專輯 (Albums)
What to find:
- Album name, versions, release date
- Pre-order links by store/platform
- **Each store's exclusive benefits (特典)** — photocards, posters, etc.
- Price comparison across stores

Output rules:
- List album name + versions
- Table or list comparing store benefits:
  ```
  📀 專輯名稱：《XXX》
  | 通路 | 特典 | 價格 |
  |------|------|------|
  | Weverse Shop | 隨機小卡 A ver. | ₩18,000 |
  | Ktown4u | 海報 + 小卡 | ₩16,500 |
  | Yes24 | 摺疊海報 | ₩17,200 |
  ```
- Include a **💡 分析** section recommending which store is best value

⚠️ **IVE 特別規則**: Always check Starship US official store (https://www.starshipent.com or
https://shop.starship-ent.com) for **signed albums (親簽專輯)**. If found, output with 🚨 alert:
```
🚨 IVE 親簽專輯警報！
Starship 美國官網現正販售親簽版本！
💰 價格：$XX.XX USD
🔗 <link>
⏰ 數量有限，建議立即搶購！
```

#### 周邊 & 聯名商品
What to find:
- Official goods, limited merch drops, pop-up stores
- Brand collaborations (e.g. clothing, cosmetics, food collabs)
- Prices and purchase channels

Output rules:
- List each item: name, price, where to buy
- If collab → note the brand + collab period + availability

### 3. 🎪 演唱會消息

What to find:
- New tour announcements (tour name, cities, dates)
- Ticket sale dates and prices by tier
- This week's concert highlights, fan-recorded moments, interesting news
- Setlists if newly revealed

Output rules:
- New tour → full table:
  ```
  🎪 巡演名稱：《XXX World Tour》
  | 日期 | 城市 | 場地 | 搶票日期 | 票價 |
  |------|------|------|----------|------|
  | 6/27-28 | 香港 | 啟德主場館 | 5/10 12:00 | HK$880-1,880 |
  ```
- This week's concert news → summarize interesting moments with YouTube links if available
- If no concert news → "目前無演唱會新消息"

### 4. 📋 團體活動

What to find:
- Award shows (MAMA, MMA, GDA, SMA, etc.)
- Music festivals, variety shows, fan meetings
- Brand events, press conferences
- TV/radio appearances

Output rules:
- List each event:
  ```
  📋 活動名稱：2026 MAMA Awards
  📍 地點：日本京瓷巨蛋
  📅 日期：11/25-26
  ⏰ 時間：18:00 KST
  📺 直播：Mnet YouTube
  ```
- If no upcoming events → "目前無團體活動消息"

### 5. 📺 官方 YouTube 更新

What to find:
- Official YouTube channel new uploads
- **Priority content**: group variety shows (團綜), tour behind-the-scenes, dance practice, live clips
- Lower priority: short clips, teasers (include only if nothing else is available)

Output rules:
- **只列出本週（7 天內）上傳的影片**，超過一週的不要列
- List recent videos with title + upload date + link:
  ```
  📺 官方 YT 更新（本週）
  • [巡演幕後] Syncopation Behind the Rhythm EP.02 (3/27)
    🔗 https://youtube.com/watch?v=...
  ```
- If no uploads this week → "本週官方 YT 無新影片"

### 6. 👤 成員 Solo 消息

What to find:
- Solo album releases or announcements
- Solo concert/fan meeting tours
- Brand ambassador activities, fashion show appearances
- Acting roles, variety show solo appearances
- Solo magazine covers, interviews

Output rules:
- Group by member name:
  ```
  👤 成員 Solo 消息

  ✦ Miyeon (薇娟)
  • Solo 專輯《XXX》預計 5/20 發行
    🔗 <link>

  ✦ Shuhua (舒華)
  • 出席 Dior 2026 秋冬秀，巴黎
    📅 4/15
    🔗 <link>
  ```
- If no solo news for any member → "本週無成員 Solo 消息"

## Output Format (Fixed Template)

Every check outputs this exact structure:

```
🌟 K-Pop 追星快報 — YYYY/MM/DD HH:MM

━━━━━━━━━━━━━━━━━━━━
🏷️ <團體名稱>
━━━━━━━━━━━━━━━━━━━━

🎵 1. 團體回歸
<content or "目前無回歸消息">

💿 2. 專輯 & 周邊商品
【專輯】
<content or "目前無新專輯消息">
【周邊 & 聯名】
<content or "目前無新周邊消息">

🎪 3. 演唱會消息
<content or "目前無演唱會新消息">

📋 4. 團體活動
<content or "目前無團體活動消息">

📺 5. 官方 YouTube 更新
<content or "本週官方 YT 無新影片">

👤 6. 成員 Solo 消息
<content or "本週無成員 Solo 消息">

━━━━━━━━━━━━━━━━━━━━
🏷️ <下一個團體>
━━━━━━━━━━━━━━━━━━━━
...

✅ 更新完成 | 下次自動檢查：YYYY/MM/DD HH:MM
```

Rules:
- [新] tag on genuinely new items since last check
- Always include source links (🔗)
- Translate Korean/English content to **繁體中文**
- Keep IVE signed album alert (🚨) at the very top if triggered

## Fetching Workflow

### 新搜尋架構（3階段）

按照以下順序進行搜尋，確保涵蓋所有重要來源：

#### 第一階段：官方帳號檢查
1. **官方 Instagram**
   ```
   browser open → https://www.instagram.com/<official_account> (profile=openclaw)
   browser act evaluate → extract recent posts (本週內)
   ```

2. **官方 Berriz / Weverse**
   - I-DLE / IVE → Berriz (必須用 browser，SPA 網站)
   - BLACKPINK → Weverse
   ```
   browser open → https://berriz.in/<group> OR https://weverse.io/<group>/feed
   browser act evaluate → 抓取官方 Notice + From.藝人貼文
   ```

3. **官方 X (Twitter)**
   ```
   browser open → https://x.com/<official_account> (profile=openclaw)
   browser act evaluate → extract recent tweets (本週內)
   ```

4. **官方 YouTube**
   ```
   DDG search: "site:youtube.com @<channel> 2026" (filter 本週上傳)
   或 Google: "site:youtube.com <channel> <group>" + time filter (past week)
   ```

5. **中國成員微博檢查** ⭐ 新增規則
   - 如果團體有中國成員，檢查其個人微博
   - I-DLE 雨琦 → @Song_Yuqi (宋雨琦)
   - 其他團體中國成員根據 config.chinese_members 設定
   ```
   web_search: "<中文名> 微博 weibo.com" (找官方微博帳號)
   browser open → https://weibo.com/<account> (if found)
   browser act evaluate → 抓取近期動態 (本週內)
   ```

#### 第二階段：新聞媒體搜尋
1. **韓國娛樂媒體**
   ```
   DDG/Google: "<group> comeback OR concert OR album 2026 site:soompi.com"
   DDG/Google: "<group> 2026 site:allkpop.com"
   DDG/Google: "<group> 2026 site:naver.com"
   ```

2. **訪談節目與綜藝**
   ```
   DDG/Google: "<group> interview OR variety show OR 訪談 OR 節目 2026"
   DDG/Google: "<group> Running Man OR 知音 OR 我獨自生活 2026"
   ```

3. **國際媒體報導**
   ```
   DDG/Google: "<group> news OR announcement 2026 site:billboard.com OR site:variety.com"
   ```

#### 第三階段：台灣粉絲團消息
1. **台灣 K-Pop 社群**
   ```
   DDG/Google: "<group> 台灣 OR Taiwan OR 粉絲團 2026"
   DDG/Google: "<group> 演唱會 OR 見面會 台北 OR 高雄 2026"
   ```

2. **台灣購買資訊**
   ```
   DDG/Google: "<group> 專輯 OR 預購 五大 OR 博客來 OR 誠品 2026"
   ```

### 特殊商店檢查
- **IVE Starship US Store** — 親簽專輯檢查 (每次必檢)
  ```
  browser open → https://shop.starship-ent.com (profile=openclaw)
  搜尋: "signed", "autograph", "IVE", "親簽", "hand-signed"
  ```

### YouTube Checking

For official YouTube channels, use DDG search (more reliable than direct web_fetch on YT):
```
web_fetch DDG: "site:youtube.com @<channel> 2026" (filter for this week's uploads)
```
Or use Google search with time filter:
```
browser open → https://www.google.com/search?q=site:youtube.com+<channel>+<group>&tbs=qdr:w
```

**Only include videos uploaded within the past 7 days.** Discard anything older.

Filter for (priority order):
- 團綜 / variety / vlog / log
- Behind / making / rehearsal / tour
- Dance practice / performance
- MV / official audio

### IVE Starship Store Check

For IVE only, always include this step. **Use browser** (web_fetch often gets blocked):
```
browser(action=open, targetUrl="https://shop.starship-ent.com", profile=openclaw)
browser(action=act, ..., request={kind: "wait", timeMs: 3000})
browser(action=snapshot, ...) or browser(action=act, ..., request={kind: "evaluate", fn: "() => document.body.innerText"})
```
Search page content for: "signed", "autograph", "IVE", "親簽", "hand-signed"
If found → trigger 🚨 alert at top of IVE section
After checking → close tab

## Check History

Track reported items in `kpop-tracker/check_history.json`:

```json
{
  "last_check": "2026-04-02T14:00:00+08:00",
  "reported_urls": ["https://..."],
  "ive_signed_album_alerted": false
}
```

- Check URL against history before outputting → skip duplicates
- Keep last 200 URLs, rotate old ones
- Track IVE signed album alert separately to avoid re-alerting

## Automated Checks (Cron)

```
openclaw cron add --schedule "0 9 * * *" --task "Run kpop-tracker skill: check all tracked artists for updates and report via webchat" --label kpop-morning
openclaw cron add --schedule "0 21 * * *" --task "Run kpop-tracker skill: check all tracked artists for updates and report via webchat" --label kpop-evening
```

Only set up cron when user explicitly asks.

## User Commands

| User says | Action |
|-----------|--------|
| 「查偶像動態」「追星更新」 | Full check all artists |
| 「查 IVE 最新消息」 | Check single group |
| 「加追蹤 aespa」 | Add artist to config |
| 「移除追蹤 xxx」 | Remove from config |
| 「追蹤清單」 | Show tracked artists |
| 「設定自動更新」 | Set up cron jobs |

## Browser Best Practices

> **⚠️ Always use `profile=openclaw` + `targetId` for all browser actions.**

- Use `evaluate` to extract text, not screenshot
- Close tabs after each source: `browser(action=close, targetId=..., profile=openclaw)`
- Rate limit: wait 2s between sources

## Error Handling

- Source fails → skip + note:「⚠️ [來源名] 暫時無法存取」
- Browser unavailable → fall back to `web_fetch`
- All sources fail → report:「❌ [團體名] 所有來源暫時無法存取，下次再試」
- DDG captcha → retry once, then try Google via browser
