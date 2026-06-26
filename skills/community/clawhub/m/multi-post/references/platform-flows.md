# Platform Automation Flows

Step-by-step browser automation for each platform. Use `browser` tool with `profile="user"` to leverage logged-in sessions.

## General Tips

- Always `snapshot` after navigation to verify page loaded and logged in
- Use `refs="aria"` for stable element references
- Wait 2-3s between platforms to avoid triggering anti-bot
- If a platform shows CAPTCHA or unusual block, **skip immediately** and report

---

## 微博 (Weibo)

```
1. browser navigate → https://weibo.com
2. browser snapshot → check if logged in (look for compose box or avatar)
3. browser act click → compose textarea / "有什么新鲜事" input
4. browser act type → paste adapted content
5. [If images] browser act click → image upload button (camera icon)
   → browser upload → select image files
   → wait for upload thumbnails to appear
6. browser act click → "发送" / submit button
7. browser snapshot → confirm "发送成功" or new post visible
8. Extract post URL from page
```

**Compose URL shortcut**: `https://weibo.com/` (homepage has compose box at top)

**Login check**: Look for "登录" button — if present, user is not logged in.

---

## 小红书 (Xiaohongshu)

```
1. browser navigate → https://creator.xiaohongshu.com/publish/publish
2. browser snapshot → check logged in (creator center)
3. [Images required] browser upload → drag or click upload area → select images
   → wait for all images to show as uploaded
4. browser act click → title input
5. browser act type → title text (≤20 chars)
6. browser act click → body textarea
7. browser act type → body content
8. [Add hashtags] browser act type → #话题名 in body
9. browser act click → "发布" button
10. browser snapshot → confirm published
```

**⚠️ Must upload at least 1 image** — 小红书 does not allow text-only posts.

**Login check**: Redirect to login page = not logged in.

---

## 知乎 (Zhihu) — 想法 (Short Post)

```
1. browser navigate → https://www.zhihu.com
2. browser snapshot → check logged in
3. browser act click → "写想法" or compose area
4. browser act type → content
5. [If images] browser act click → image icon → upload
6. browser act click → "发布想法" button
7. browser snapshot → confirm published
```

**For 文章 (Article)**:
```
1. browser navigate → https://zhuanlan.zhihu.com/write
2. Fill title + body + images
3. Click "发布"
```

---

## Twitter/X

```
1. browser navigate → https://x.com/compose/post
   (or https://x.com → click compose)
2. browser snapshot → check logged in
3. browser act click → tweet compose textarea
4. browser act type → content (≤280 chars)
5. [If images] browser act click → media button (image icon)
   → browser upload → select images (≤4)
6. browser act click → "Post" button
7. browser snapshot → confirm posted

[For thread — if content > 280 chars]:
8. After first tweet, click "+" to add to thread
9. Type next segment
10. Repeat until all content posted
11. Click "Post all"
```

---

## Reddit

```
1. browser navigate → https://www.reddit.com/r/{subreddit}/submit
2. browser snapshot → check logged in
3. browser act click → title input
4. browser act type → post title
5. browser act click → body textarea (Text tab)
6. browser act type → body content (markdown)
7. [If images] switch to "Images & Video" tab → upload
8. browser act click → "Post" button
9. browser snapshot → confirm posted, capture URL
```

**Default subreddits for tech tools**: r/OpenClaw, r/artificial, r/MachineLearning, r/SideProject

---

## V2EX

```
1. browser navigate → https://v2ex.com/new
2. browser snapshot → check logged in
3. Select node from dropdown (e.g. "分享创造")
4. browser act click → title input
5. browser act type → title
6. browser act click → content textarea
7. browser act type → body (supports markdown subset)
8. browser act click → "发布" button
9. browser snapshot → confirm posted
```

---

## LinkedIn

```
1. browser navigate → https://www.linkedin.com/feed/
2. browser snapshot → check logged in
3. browser act click → "Start a post" compose area
4. browser act type → content
5. [If images] browser act click → image icon → upload
6. browser act click → "Post" button
7. browser snapshot → confirm posted
```

---

## 豆瓣 (Douban)

```
1. browser navigate → https://www.douban.com/
2. browser snapshot → check logged in
3. browser act click → "说点什么..." broadcast compose
4. browser act type → content (≤280 chars)
5. [If images] browser act click → image upload icon
6. browser act click → "发布" button
7. browser snapshot → confirm posted
```

---

## Post-Publish Checklist

After each platform:
1. ✅ Capture screenshot as proof
2. ✅ Extract post URL if possible
3. ✅ Log result (platform, status, URL, timestamp)
4. ✅ Wait 3s before next platform
5. ✅ Report summary to user when all done
