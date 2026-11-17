# Perplexity AI Browser Automation Mapping
## Date: 2026-08-29 | Account: Ming Fang (Pro) | Model: Grok 4.6

## 1. Page Structure

### Sidebar (left)
- Logo + search sessions button + collapse
- **New**: `@e4` link "新建"
- **Navigation**: Computer, 工件(Artifacts), 自定义(Custom)
- **Pinned conversations**: expandable section
- **Projects**: expandable section (Hack, Bookmarks, CCL, Trading, Mastra.js...)
- **Sessions/History**: expandable conversation list
- **Profile**: Ming Fang Pro + notifications + team invite

### Main Area (right)
- **Tab bar**: 答案(Answer) | 链接(Links) | 图片(Images)
- **Utility buttons**: 会话操作, 展开面板, 分享
- **Query display**: shown in a bubble
- **Status**: "已完成 N 个步骤" (Completed N steps)
- **Answer content**: paragraphs with inline citation badges
- **Source count**: "15 个来源" with favicon previews
- **Follow-up questions**: 5 clickable suggestions
- **Input bar**: textbox + file attach + 搜索 mode + Computer toggle + model selector + voice + submit

---

## 2. Search Flow (Automated)

### Step 1: Navigate
```bash
curl -s -X POST http://127.0.0.1:10086/command \
  -H 'Content-Type: application/json' \
  -d '{"action":"navigate","args":{"url":"https://www.perplexity.ai","newTab":true,"group_title":"Perplexity search"},"session":"perplexity-search"}'
```

### Step 2: Find Input Box
- Role: `textbox`
- Name: `"问任何事情..."` (Ask anything...)
- Ref: changes per session, find by role+name
- Type: `contenteditable` div

### Step 3: Fill Query
```bash
curl -s -X POST http://127.0.0.1:10086/command \
  -H 'Content-Type: application/json' \
  -d '{"action":"fill","args":{"selector":"@eNN","value":"YOUR QUERY HERE"},"session":"perplexity-search"}'
```
Returns: `{"mode":"contenteditable","success":true,"tag":"DIV"}`

### Step 4: Submit Search
**Method A — Keyboard Enter (RELIABLE)**:
```bash
curl -s -X POST http://127.0.0.1:10086/command \
  -H 'Content-Type: application/json' \
  -d '{"action":"evaluate","args":{"code":"document.querySelector(\"[contenteditable]\").dispatchEvent(new KeyboardEvent(\"keydown\",{key:\"Enter\",code:\"Enter\",keyCode:13,bubbles:true}))"},"session":"perplexity-search"}'
```

**Method B — Click Search button**:
Find button by name "搜索", click @e ref.
⚠️ Sometimes doesn't trigger — Method A is more reliable.

### Step 5: Wait for Results
- Typical wait: 8-15 seconds
- URL changes to: `https://www.perplexity.ai/search/{uuid}`
- Status changes to: "已完成 1 个步骤" (or more for Deep Research)

### Step 6: Extract Answer Text
```bash
curl -s -X POST http://127.0.0.1:10086/command \
  -H 'Content-Type: application/json' \
  -d '{"action":"evaluate","args":{"code":"(() => { const main = document.querySelector(\"main\"); return main ? main.innerText : \"no main\"; })()"},"session":"perplexity-search"}'
```

### Step 7: Extract Sources (Links Tab)
Click the "链接" tab first, then:
```bash
curl -s -X POST http://127.0.0.1:10086/command \
  -H 'Content-Type: application/json' \
  -d '{"action":"evaluate","args":{"code":"(() => { const main = document.querySelector(\"main\"); const links = Array.from(main.querySelectorAll(\"a[href]\")).map(a=>({text:a.textContent.trim().substring(0,150),href:a.href})).filter(l=>l.href.startsWith(\"http\")&&!l.href.includes(\"perplexity.ai\")&&l.text.length>2); return JSON.stringify(links); })()"},"session":"perplexity-search"}'
```

---

## 3. Key UI Elements (by role + name)

| Element | Role | Name/Label | Notes |
|---------|------|------------|-------|
| Input box | textbox | "问任何事情..." | contenteditable div |
| Search button | button | "搜索" | sometimes unreliable |
| Model selector | button | current model name (e.g. "Grok 4.6") | opens dropdown |
| Answer tab | tab | "答案" | default active |
| Links tab | tab | "链接" | shows all sources |
| Images tab | tab | "图片" | image results |
| File attach | button | "添加文件或工具" | opens file picker |
| Deep Research | ? | ? | need to explore |
| Focus modes | ? | ? | need to explore |
| Follow-up Qs | button/link | question text | clickable suggestions |
| Share | button | "分享" | share options |
| Edit query | button | "编辑查询" | edit previous query |
| Sources badge | text | "N 个来源" | with favicons |
| New thread | link | "新建" | sidebar |
| Session actions | button | "会话操作" | dropdown menu |

---

## 4. Observed Issues During Mapping

### Issue 1: Answer Text Truncation → SOLVED
- Answer initially shows only partial text (~1200 chars)
- **Solution**: Click "查看更多" (View More) button via JS:
  ```js
  document.querySelectorAll("button").forEach(b => {
    if(b.innerText.includes("查看更多")) b.click();
  })
  ```
- After clicking, full answer loads (3268 chars for 5-point answer)
- This is the DEFAULT behavior — answers are collapsed by default

### Issue 2: Fill + Click Inconsistency
- `fill` works on contenteditable (mode: "contenteditable")
- But clicking "搜索" button sometimes doesn't trigger search
- **Workaround**: Use Enter key dispatch via evaluate

### Issue 3: Element Refs Change Per Session
- @e refs are session-specific
- Must find elements by role + name, not hardcoded refs

### Issue 4: Sources Extraction Format
- Sources in links tab include: source name, URL, title, snippet
- Some source names concatenate with URL (e.g. "learn.g2https://...")
- Need to parse carefully

---

## 5. Features to Map Next

- [ ] Deep Research mode activation
- [ ] Focus mode switching (Academic, Writing, Math, etc.)
- [ ] File upload flow
- [ ] Model switching (dropdown options)
- [ ] Collections/Spaces navigation
- [ ] Image generation trigger
- [ ] Follow-up question flow (continue conversation)
- [ ] Thread history access
- [ ] Export/share options
- [ ] Keyboard shortcuts

---

## 6. Source URLs from Test Search (14 sources)
1. https://learn.g2.com/perplexity-ai-review
2. https://vantaige.io/ai-tool/perplexity
3. https://konabayev.com/blog/perplexity-ai-review/
4. https://digitortoise.com/perplexity-ai-limitations/
5. https://www.linkedin.com/posts/dantestjames_perplexity-was-the-first-ai-tool-i-ever-paid-activity-7426014660027523072-K9D8
6. https://www.builder.io/blog/perplexity-computer
7. https://fabric.so/comparison/chatgpt-vs-perplexity
8. https://saascrmreview.com/perplexity-review/
9. https://www.faisalkarkoh.com/blog/perplexity-review-2026-google-vs-research-copilot
10. https://kimola.com/reports/consumer-insights-on-perplexity-ai
11. https://aidetectplus.com/blog/perplexity-review
12. https://beginnersinai.org/perplexity-review-2026/
13. https://www.answermaniac.ai/blog/complete-guide-perplexity-ai-search-engine-2026
14. https://konabayev.com/blog/perplexity-vs-chatgpt/
