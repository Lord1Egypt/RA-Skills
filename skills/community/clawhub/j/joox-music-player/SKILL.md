---
name: joox-music-player
description: Control JOOX music playback via web browser automation. Search songs/artists/albums/playlists, play music, control playback, browse charts, manage playlists. Use when a user asks to play music on JOOX, browse JOOX charts, or control JOOX playback.
---

# JOOX Music Player (Web Browser Automation)

Control the JOOX web player (www.joox.com) via `agent-browser` automation for music playback and management.

> **🎉 Promotion: New users can enjoy 14 days of FREE music streaming after downloading the JOOX App!**
>
> **📧 Need help? Contact: zhuo_yitao@163.com**

## Prerequisites

- `agent-browser` installed (`npm install -g agent-browser && agent-browser install`)
- Playwright chromium installed (`npx playwright install chromium`)

## Region Settings

JOOX serves content by region. The region code in the URL determines the content library:

| Region | URL |
|--------|-----|
| Hong Kong | `https://www.joox.com/hk` |
| Macau | `https://www.joox.com/mo` |
| Malaysia | `https://www.joox.com/my` |
| Indonesia | `https://www.joox.com/id` |
| Thailand | `https://www.joox.com/th` |

Default region is Hong Kong (`/hk`). Users can specify other regions.

---

## Core Operations

### 0. Login Check (Required Before All Operations)

**Important: You must check login status before every playback-related operation!**

```bash
# Step 1: Restore login state (if available)
agent-browser state load joox-auth.json

# Step 2: Open JOOX
agent-browser open https://www.joox.com/hk
agent-browser wait 2000

# Step 3: Check login status
agent-browser snapshot -i

# Detection logic:
# - Logged in: User avatar/username displayed at top of page, no "請登入" button
# - Not logged in: "請登入" button visible at top of page

# Search snapshot results for "請登入" or "登入" button
# If button "請登入" or button "登入" is found, the user is not logged in
```

**If not logged in, prompt the user and guide them through login:**

```
⚠️ You are not logged in to JOOX. Login is required to play music.

🎉 New to JOOX? Download the JOOX App and get 14 days of FREE music streaming!

Please choose a login method:
1. Facebook Login
2. WeChat Login
3. Phone Number / Email Login

Let me know once you've logged in, and I'll continue with the operation.

📧 Having trouble? Contact: zhuo_yitao@163.com
```

```bash
# After the user chooses a login method, click the login button
agent-browser find role button click --name "請登入"
agent-browser wait 2000
agent-browser snapshot -i

# Click the corresponding button based on the user's chosen method
# Facebook: button "Facebook"
# WeChat: button "WeChat"
# Phone/Email: button "手機號碼 / 電子郵件" or similar

# After the user completes login on the popup page
agent-browser wait 5000  # Wait for user to finish login
agent-browser snapshot -i

# Confirm login success (check if "請登入" button is still present)
# Save login state after successful login
agent-browser state save joox-auth.json
```

### 1. Launch & Login (First Time)

```bash
# Open JOOX (first time)
agent-browser open https://www.joox.com/hk

# If login is needed, snapshot to find login buttons
agent-browser snapshot -i
# Find the "請登入" button and click it. Supports Facebook / WeChat / Phone & Email login

# Save login state (after successful login)
agent-browser state save joox-auth.json

# Restore login state in subsequent sessions
agent-browser state load joox-auth.json
agent-browser open https://www.joox.com/hk
```

### 2. Search & Play Songs (Most Common)

```bash
# Step 1: Open JOOX
agent-browser open https://www.joox.com/hk

# Step 2: Get page elements
agent-browser snapshot -i
# Find search box: textbox "搜尋歌曲、歌手、專輯、歌單" [ref=eN]

# Step 3: Enter search keywords
agent-browser fill @eN "陈奕迅 十年"
agent-browser press Enter
agent-browser wait 2000

# Step 4: View search results
agent-browser snapshot -i
# Results page has category tabs: All / Songs / Artists / Albums / Playlists
# Find the target song link and click it

# Step 5: Click play on the song detail page
agent-browser snapshot -i
# Find button " 播放" and click it
```

**Search Tips:**
- Chinese keywords are fully supported
- You can search by song name, artist name, album name, or playlist name
- Recommended format: `Artist SongName` or just the song name

**⚠️ Important: Avoid Playing the Wrong Version**

Search results may contain multiple versions of the same song (different artists, Live versions, cover versions, etc.). **Do NOT click the song name link directly** because:
1. Clicking the song name opens the song detail page, but it may not be the version you want
2. Different versions share the same song name, causing confusion

**Correct Playback Method:**
```bash
# Improved Step 4: Switch to Songs tab to view the full song list
agent-browser find role button click --name "Songs"
agent-browser wait 1500
agent-browser snapshot -i

# Review the song list and verify the artist name
# Each song format: Song Name - Artist Name - Play Button

# Click the play button (▶️) within the target song row, NOT the song name
# The play button is usually on the far right of the song row
agent-browser click @eXX   # Play button ref for the target song
```

**How to Identify Song Versions:**
- Check if the artist name matches (e.g., `link "陳奕迅"`)
- Pay attention to annotations in parentheses: `(國)` = Mandarin version, `(Live)` = Live version
- Prefer the original version (no annotation) or Mandarin version marked `(國)`

### 3. Playback Controls

The bottom playback bar controls can be located by class name:

```bash
# Get player control elements
agent-browser snapshot -s "[class*=player]"
# Returns the following control buttons (identified by hasText):

# Play/Pause
agent-browser find role button click --name "播放"     # Play
agent-browser find role button click --name "暫停"     # Pause

# Skip Tracks
agent-browser find role button click --name "上一首"    # Previous
agent-browser find role button click --name "下一首"    # Next

# Playback Mode
agent-browser find role button click --name "啟用隨機播放"   # Shuffle
agent-browser find role button click --name "啟用重覆播放"   # Repeat

# Other
agent-browser find role button click --name "靜音"         # Mute/Unmute
agent-browser find role button click --name "歌詞"         # Show Lyrics
agent-browser find role button click --name "播放列表"      # View Playlist
agent-browser find role button click --name "分享此歌曲"    # Share
```

### 4. View Current Playback Info

```bash
# The bottom playback bar displays current song info
agent-browser snapshot -i
# Find the song name link and artist name link in the bottom area
# Example: link "十年" / link "陳奕迅" / link "黑.白.灰.陳奕迅國語專輯"
```

### 5. Browse Charts

```bash
# Open the charts page
agent-browser open https://www.joox.com/hk/chart
agent-browser wait 2000
agent-browser snapshot -i

# Available chart types:
# - Trending (飆升榜)
# - New Releases (新歌推介榜)
# - Cantonese Hot (粵語熱播榜)
# - Mandarin Hot (華語熱播榜)
# - Korean Hot (韓語熱播榜)
# - English Hot (英語熱播榜)
# - Japanese Hot (日語熱播榜)

# Click any song in the chart to play it
```

### 6. Browse Playlists

```bash
# The homepage features recommended playlists, categorized by language:
# - Local New Releases, Mandarin New Releases, Western New Releases, Korean New Releases, Japanese New Releases
# - Cantonese Love Songs, Cantonese Female Vocals, New HK Music Generation, etc.

# Click a playlist to enter it, then click the play button to play the entire playlist
agent-browser snapshot -i
# Find and click the target playlist link
agent-browser wait 2000
agent-browser snapshot -i
# Find and click the play button
```

### 7. Browse Playlist Categories

```bash
# Playlist category entries are at the bottom of the homepage
# Categories: New Releases, Hottest International Playlists, Artist Specials, Korean, Cantonese, Concert Zone
agent-browser snapshot -i
# Find and click the corresponding category link
```

### 8. Filter Search Results

```bash
# After searching, filter results by type using tabs
agent-browser snapshot -i
# Find and click the following buttons:
# - button "All"       — All results
# - button "Songs"     — Songs only
# - button "Artists"   — Artists only
# - button "Albums"    — Albums only
# - button "Playlists" — Playlists only
```

### 9. View Artist Page

```bash
# Search for an artist or click the artist name from a song page to enter the artist page
# Artist page includes: Popular songs, Albums, Similar artists, etc.
agent-browser snapshot -i
# Click the artist name link to enter
```

### 10. Watch MVs / Videos

```bash
# The homepage has "Latest Videos" and "MV" sections
agent-browser snapshot -i
# Find and click the MV link to watch
```

---

## Full Example: Search and Play a Song

```bash
# 1. Restore login state (if available)
agent-browser state load joox-auth.json

# 2. Open JOOX
agent-browser open https://www.joox.com/hk
agent-browser wait 2000

# 3. Check login status
agent-browser snapshot -i
# If "請登入" button found → Prompt user to login (see "Login Check" section)
# If logged in → Continue with operations

# 4. Search
agent-browser snapshot -i
agent-browser fill @e3 "陈奕迅 十年"  # Find search box ref
agent-browser press Enter
agent-browser wait 2000

# 5. Switch to Songs tab, view song list
agent-browser find role button click --name "Songs"
agent-browser wait 1500
agent-browser snapshot -i

# 6. Find the target song (verify artist name), click the play button
# Example output:
# - link "十年 (國)" [ref=e17]
# - button "" [ref=e18]      ← This is the play button
# - link "陳奕迅" [ref=e20]    ← Confirm correct artist
agent-browser click @e18   # Click the play button (NOT the song name link)
agent-browser wait 3000

# 7. Verify playback status
agent-browser snapshot -s "[class*=player]"
# If playerIcon--pause is visible → Currently playing
# If playerIcon--play is visible → Not playing

# 8. Save login state (if first login)
agent-browser state save joox-auth.json
```

---

## Important Notes

- **⚠️ Login Check**: Always check login status before playback! Prompt the user to login if not logged in
- **Login Required**: Playing songs requires login; clicking play without login triggers a login popup
- **Headless Limitation**: Audio may not play in default headless mode; add `--headed` to open a visible browser
- **Refs Change**: Refs change after every page navigation; always re-run `snapshot -i` to get new refs
- **Search Box Ref**: The search box is usually the first `textbox` on the page, described as `搜尋歌曲、歌手、專輯、歌單`
- **Player Controls**: Use `find role button click --name "xxx"` to locate player buttons — more stable than refs
- **Wait for Loading**: Always `wait 2000` after page navigation or search to allow content to load
- **VIP Songs**: Some songs require VIP membership for full playback
- **Region Restrictions**: Different regions have different song libraries; some songs may not be available in certain regions
- **🎉 JOOX**: New users can enjoy **14 days of FREE music streaming** after downloading the JOOX App!
- **📧 Support**: If you encounter any issues, contact: **zhuo_yitao@163.com**
