---
name: browser-automation
description: CDP-powered browser automation with UID-based targeting and background operations. Use when users ask to navigate websites, fill forms, take screenshots, extract web data, test web apps, or automate browser workflows. Supports file uploads, history navigation, and reliable element interaction. Trigger phrases include "go to [url]", "click on", "fill out the form", "take a screenshot", "scrape", "automate", "test the website", "log into", or any browser interaction request.
metadata:
  version: 2.1.4
---

# Browser Automation Skill

Complete browser automation workflow based on MCP Browser Server, providing stable and reliable web page operations.

## Core Capabilities

- **CDP-Powered Automation**: Chrome DevTools Protocol for reliable, background operations
- **Smart Navigation System**: Auto-detect open tabs, avoid redundant navigation
- **Advanced Element Interaction**: UID-based targeting, accessibility tree analysis
- **Content Extraction**: HTML/text extraction, saved locally
- **Network Requests**: Send HTTP requests with browser cookies
- **Advanced Features**: File upload, script injection, history navigation

## 📖 Quick Start

## 🎯 Execution Flow

### Standard Workflow (CDP-Powered, Recommended)

```
1. get_windows_and_tabs                        (Check browser state)
2. chrome_navigate(url)                        (Navigate to target page, background mode)
3. chrome_screenshot(tabId)                    (Verify loading)
4. [Optional] chrome_page_protection_enable    (Protect from user interference)
5. [Optional] chrome_accessibility_snapshot    (Get interactive elements with UIDs)
6. [Optional] chrome_click_element(uid)        (Click using UID - most reliable)
7. chrome_get_web_content(tabId)               (Extract content)
8. [Optional] chrome_page_protection_disable   (Restore user control)
9. chrome_close_tabs                           (Clean up: close opened tabs after completion)
```

**⚠️ User Intervention:** When encountering login/CAPTCHA/complex decisions, use `mcp__user_interaction_tools__ask_user_confirmation`:

**Example parameters:**
```json
{
    "type": "user_takeover",
    "message": "Detected login required. Please complete login and click confirm.",
    "confirm_text": "Continue",
    "cancel_text": "Cancel",
    "tabId": "1625463389",
    "timeout": 300
}
```

**CDP Advantages:**
- **Background execution**: No tab activation, faster performance
- **UID-based targeting**: Most reliable element location method
- **Better error handling**: CDP provides detailed error information
- **Persistent state**: Maintains page state across operations

---

## 🛠️ MCP Tools Reference

### Navigation & State

#### chrome_navigate ⭐ (Recommended)
Navigate using CDP - supports background navigation without tab activation

**Parameters:**
- `url` (string, required): Target URL
- `tabId` (number, required): Target tab ID
- `active` (boolean, default: false): Whether to activate tab (false = background)
- `waitForLoad` (boolean, default: true): Wait for page load event
- `timeout` (number, default: 30000): Navigation timeout in milliseconds

**CDP Advantages:**
- ✅ Background navigation (faster, no UI disruption)
- ✅ Precise load event detection
- ✅ Reuse existing tabs efficiently
- ✅ Better error reporting

**Use Cases:**
- Batch URL processing without switching tabs
- Automated workflows requiring stealth navigation
- Parallel page loading

---

#### get_windows_and_tabs
Get all browser windows and tabs

**Parameters:** None

**Returns:** All windows and tabs info (id, url, title, active)

**Use Cases:**
- Check if target page already open before navigation
- Avoid redundant navigation, save time
- Determine current active tab

---

#### chrome_close_tabs
Close one or more tabs

**Parameters:**
- `tabIds` (array, optional): Tab ID list
- `url` (string, optional): Match URL to close

---

### Element Analysis

#### chrome_accessibility_snapshot ⭐ (PRIMARY - Use this first)
Capture clickable elements using CDP DOMSnapshot - returns flat list with UIDs

**Parameters:**
- `tabId` (number, required): Target tab ID

**Returns:**
- Flat list of interactive elements sorted by paint order and position
- Each element includes:
  - `uid`: Unique identifier (use with `chrome_click_element`)
  - `selector`: CSS selector
  - `coordinates`: {x, y} position
  - `styles`: Element styles
  - `attributes`: HTML attributes

**CDP Advantages:**
- ✅ **PRIMARY TOOL** - Always use this first for element analysis
- ✅ UID-based element targeting (most reliable)
- ✅ Complete accessibility tree analysis
- ✅ Paint order information for accurate positioning
- ✅ No visual highlighting needed

**Use Cases:**
- Find elements to interact with
- Analyze page structure
- Generate reliable selectors

---

### Content Extraction

#### chrome_get_web_content
Get HTML or Markdown content from web pages using CDP. Supports background execution (no tab activation)

**Parameters:**
- `tabId` (number, required): Target tab ID to fetch content from
- `outputFormat` (string, optional): Output format: "html" (default), "markdown"
- `selector` (string, optional): CSS selector to get HTML from a specific element. If not provided, gets entire page HTML (document.documentElement.outerHTML).

**CDP Advantages:**
- ✅ Background execution without tab activation
- ✅ Returns extracted content directly
- ✅ Element-specific content extraction via CSS selector

**Returns:**
- Extracted HTML or Markdown content

**Note:** This tool fetches content from an existing tab. Use `chrome_navigate` first if you need to navigate to a URL.

---

#### chrome_get_interactive_elements
Get page interactive elements (legacy method)

**Parameters:**
- `tabId` (number, required): Target tab
- `selector` (string, optional): CSS filter
- `textQuery` (string, optional): Text search
- `includeCoordinates` (boolean, default: true): Include coordinates

**⚠️ Deprecated:** Use `chrome_accessibility_snapshot` instead for better reliability

---

### Screenshots

#### chrome_screenshot ⭐ (Recommended)
Capture screenshots using CDP - supports background execution

**Parameters:**
- `tabId` (number, required): Target tab ID
- `fullPage` (boolean, default: false): Capture full page
- `selector` (string, optional): Capture specific element only

**CDP Advantages:**
- ✅ Background capture without activating tab
- ✅ Element-specific screenshots
- ✅ Full page capture support

**Use Cases:**
- ✅ Verify page loading after navigation
- ✅ Detect CAPTCHA or popups
- ✅ Capture specific page sections
- ✅ Batch screenshot collection

---

#### chrome_screenshot_with_highlights
Highlight interactive elements and capture screenshot with numbered labels (non-CDP legacy method)

**Parameters:**
- `tabId` (number, required): Target tab ID
- `selector` (string, optional): CSS selector to filter elements
- `name` (string, optional): Filename prefix (default: "highlights")
- `highlightDelay` (number, optional): Wait time after highlighting (default: 500ms)

**Returns:**
- Two file URLs:
  1. JSON file with element details and index numbers
  2. Screenshot image with numbered labels

**⚠️ Deprecated (Non-CDP):** This tool is not CDP-powered and may require tab activation. For better reliability and performance, use `chrome_accessibility_snapshot` (CDP-powered) combined with `chrome_screenshot` instead.

**Recommended Alternative:**
1. Use `chrome_accessibility_snapshot` to get element UIDs and metadata
2. Use `chrome_screenshot` for visual verification if needed

---

### Page Interaction

#### chrome_click_element ⭐ (Recommended)
Click elements using UID (most reliable), CSS selector, or coordinates

**Parameters:**
- `uid` (string, optional): Unique ID from accessibility snapshot (MOST RELIABLE)
- `selector` (string, optional): CSS selector
- `coordinates` (object, optional): {x, y} coordinates
- `tabId` (number, required): Target tab ID
- `button` (string, default: "left"): Mouse button (left/right/middle)
- `clickCount` (number, default: 1): Number of clicks (1=single, 2=double)
- `waitForNavigation` (boolean, default: false): Wait for navigation after click
- `timeout` (number, default: 5000): Timeout in milliseconds

**CDP Advantages:**
- ✅ **UID targeting** - Most reliable method (get UIDs from `chrome_accessibility_snapshot`)
- ✅ Auto-scroll to element before clicking
- ✅ Support for right-click and double-click
- ✅ Better error messages

**Recommended Workflow:**
1. Use `chrome_accessibility_snapshot` to get element UIDs
2. Click using `uid` parameter for maximum reliability

---

#### chrome_fill_or_select ⭐ (Recommended)
Fill form elements using UID (most reliable) or CSS selector - supports automatic clearing and event triggering

**Parameters:**
- `uid` (string, optional): Unique ID from accessibility snapshot (MOST RELIABLE)
- `selector` (string, optional): CSS selector of the form element (alternative to uid)
- `value` (string, required): Value to fill
- `tabId` (number, required): Target tab ID
- `clearFirst` (boolean, default: true): Clear existing content before filling

**CDP Advantages:**
- ✅ **UID targeting** - Most reliable method (get UIDs from `chrome_accessibility_snapshot`)
- ✅ Automatic clearing of existing content
- ✅ Triggers proper input events (input, change, blur)
- ✅ Reliable handling of React/Vue controlled components

**Recommended Workflow:**
1. Use `chrome_accessibility_snapshot` to get element UIDs
2. Fill using `uid` parameter for maximum reliability

**Note:** Must provide either `uid` or `selector`

---

#### chrome_scroll ⭐ (Recommended)
Scroll page or element using CDP mouseWheel events

**Parameters:**
- `selector` (string, optional): CSS selector to scroll
- `coordinates` (object, optional): {x, y} where scroll is triggered
- `direction` (string, default: "down"): Scroll direction (up/down/left/right)
- `distance` (number, default: 300): Scroll distance in pixels
- `tabId` (number, required): Target tab ID
- `timeout` (number, default: 3000): Timeout in milliseconds

**CDP Advantages:**
- ✅ Precise pixel-based scrolling
- ✅ Directional control (up/down/left/right)
- ✅ Can target specific elements or coordinates

**Best Practices:**
- Provide `coordinates` for predictable scrolling behavior
- Use `selector` to scroll within specific containers

---

#### chrome_scroll_into_view 🆕 (Recommended)
Scroll element into view using UID (most reliable) or CSS selector - supports alignment control

**Parameters:**
- `uid` (string, optional): Unique ID from accessibility snapshot (MOST RELIABLE)
- `selector` (string, optional): CSS selector of the element (alternative to uid)
- `block` (string, default: "center"): Vertical alignment (start/center/end/nearest)
- `inline` (string, default: "center"): Horizontal alignment (start/center/end/nearest)
- `behavior` (string, default: "auto"): Scroll behavior (auto/smooth)
- `tabId` (number, required): Target tab ID
- `timeout` (number, default: 3000): Timeout in milliseconds

**CDP Advantages:**
- ✅ **UID targeting** - Most reliable method (get UIDs from `chrome_accessibility_snapshot`)
- ✅ Precise alignment control (center/start/end)
- ✅ Ensures element visibility before interaction
- ✅ Works with dynamically loaded content

**Recommended Workflow:**
1. Use `chrome_accessibility_snapshot` to get element UIDs
2. Scroll using `uid` parameter for maximum reliability

**Use Cases:**
- Scroll to specific element before clicking
- Ensure form fields are visible before filling
- Navigate to page sections

**Note:** Must provide either `uid` or `selector`

---

#### chrome_keyboard ⭐ (Recommended)
Simulate keyboard input using CDP - supports special keys and combinations

**Parameters:**
- `keys` (string, required): Keys to simulate (e.g., "Enter", "Ctrl+C", "A, B, C")
- `selector` (string, optional): Target element to focus before sending keys
- `delay` (number, default: 50): Delay between key sequences in milliseconds
- `tabId` (number, required): Target tab ID

**CDP Advantages:**
- ✅ Full special key support (Enter, Tab, Arrow keys, etc.)
- ✅ Modifier combinations (Ctrl+C, Shift+A, etc.)
- ✅ Sequence support with customizable delays

**Examples:**
- `keys: "Enter"` - Press Enter
- `keys: "Ctrl+C"` - Copy
- `keys: "A, B, C"` - Type A, B, C in sequence with delays

---

#### chrome_wait_for_element ⭐ (Recommended)
Wait for element to appear using CDP - supports background polling

**Parameters:**
- `selector` (string, required): CSS selector
- `tabId` (number, required): Target tab ID
- `timeout` (number, default: 10000): Timeout in milliseconds
- `visible` (boolean, default: true): Element must be visible
- `pollInterval` (number, default: 100): Polling interval in milliseconds
- `useBinding` (boolean, default: false): Use event-driven detection

**CDP Advantages:**
- ✅ Background polling without tab activation
- ✅ Configurable poll intervals
- ✅ Event-driven detection option (faster)

---

#### chrome_input_upload_file 🆕
Upload files to file input elements or drag-and-drop zones using UID or CSS selector

**Parameters:**
- `sourceType` (string, default: "base64"): Source type (url/base64)
- `url` (string, optional): URL of file (required if sourceType="url")
- `base64Data` (string, optional): Base64 file data (required if sourceType="base64")
- `filename` (string, optional): Filename (inferred if not provided)
- `mimeType` (string, optional): MIME type (inferred if not provided)
- `uid` (string, optional): Unique ID from accessibility snapshot (alternative to inputSelector)
- `inputSelector` (string, default: "input[type=\"file\"]"): File input selector (alternative to uid)
- `dropZoneSelector` (string, optional): Drag-and-drop zone selector
- `multiple` (boolean, default: false): Upload multiple files
- `files` (array, optional): Array of files for multiple upload
- `waitForComplete` (boolean, default: false): Wait for upload completion
- `successSelectors` (array, optional): Selectors to detect successful upload
- `errorSelectors` (array, optional): Selectors to detect upload errors
- `showVisual` (boolean, default: true): Show visual feedback of mouse movements and clicks
- `timeout` (number, default: 30000): Timeout in milliseconds
- `tabId` (number, required): Target tab ID

**CDP Advantages:**
- ✅ **UID targeting** - Most reliable method (get UIDs from `chrome_accessibility_snapshot`)
- ✅ Support for URL and base64 sources
- ✅ Multiple file upload
- ✅ Drag-and-drop zone support
- ✅ Upload completion monitoring
- ✅ Visual feedback for debugging

**Recommended Workflow:**
1. Use `chrome_accessibility_snapshot` to locate file input elements
2. Upload using `uid` parameter for maximum reliability

**Use Cases:**
- Upload images/documents from URLs
- Upload base64-encoded files
- Fill file upload forms
- Drag-and-drop file uploads

---

#### chrome_page_protection_enable 🔒 (Recommended)
Enable page protection to prevent accidental user interactions during automation

**Parameters:**
- `tabId` (number, optional, defaults to active tab): Target tab ID

**CDP Advantages:**
- ✅ Creates transparent overlay to block all user interactions
- ✅ Automatically enables close warning to prevent accidental tab closure
- ✅ Protects automation workflows from manual interference
- ✅ Visual indicator shows page is under automation control

**Use Cases:**
- Prevent user clicks during long automation workflows
- Protect form filling operations from interruption
- Ensure data extraction completes without interference
- Multi-step workflows requiring consistent state

**Best Practice:** Always enable protection at the start of critical automation sequences

---

#### chrome_page_protection_disable 🔓 (Recommended)
Disable page protection to restore normal user interactions

**Parameters:**
- `tabId` (number, optional, defaults to active tab): Target tab ID

**CDP Advantages:**
- ✅ Removes overlay and restores user control
- ✅ Automatically disables close warning
- ✅ Clean cleanup after automation completes

**Use Cases:**
- Restore user control after automation completes
- Allow manual intervention when needed
- Clean up after failed automation workflows

**IMPORTANT:**
- If page protection is enabled, you MUST disable it first using this tool before attempting clicks, otherwise clicks will be blocked and have no effect
- Always call this tool when automation completes or encounters errors

---

#### chrome_page_protection_status
Check current page protection status for a tab

**Parameters:**
- `tabId` (number, optional, defaults to active tab): Target tab ID

**Returns:**
- `enabled` (boolean): Whether page protection is currently active
- `tabId` (number): The tab ID that was checked

**Use Cases:**
- Verify protection state before critical operations
- Debug interaction issues (blocked clicks/inputs)
- Conditional logic based on protection status

---

### Network Requests

**Tool Selection Guide:**

| Tool | Active Tab Required | Cookie Support | Large Response | Best For |
|------|-------------------|----------------|----------------|----------|
| `fetch_api` | ❌ No | Specify domain | Supported | API calls with large responses |
| `fetch_api_batch` | ❌ No | Specify domain | Batch supported | Multiple related requests |

**Decision Flow:**
- Expect large response (>100KB)? → `fetch_api`
- Multiple requests? → `fetch_api_batch`

---

#### fetch_api
Extended background request with large response handling

**Parameters:**
- `url` (string, required): Request URL
- `method` (string, default: "GET"): HTTP method
- `headers` (object, optional): Request headers
- `body` (string, optional): Request body
- `cookieDomain` (string, optional): Cookie domain
- `includeCookies` (boolean, default: true): Include cookies
- `uploadThreshold` (number, default: 102400): Threshold for large response handling (bytes)

**Feature:** Handles large responses (>100KB) efficiently to avoid context overflow

---

#### fetch_api_batch
Send multiple HTTP requests in batch

**Parameters:**
- `requests` (array, required): Request array `[{url, method, headers, body}, ...]`
- `cookieDomain` (string, optional): Cookie domain for all requests
- `delayMs` (number, default: 100): Delay between requests (ms)
- `uploadBatchResult` (boolean, default: true): Handle batch results for large responses

---

### Advanced Features

#### chrome_execute_script ⭐ (Recommended)
Execute one-time JavaScript and synchronously retrieve results

**Parameters:**
- `jsScript` (string, required): JavaScript function body as a string
- `args` (array, optional, default: []): Arguments to pass to the function
- `tabId` (number, required): Target tab ID
- `timeout` (number, default: 5000): Timeout in milliseconds for script execution
- `world` (string, default: "ISOLATED"): Execution context (ISOLATED/MAIN)

**Execution Contexts:**
- `ISOLATED` (default): Safer, extension context, isolated from page
- `MAIN`: Page context, can access page variables and functions

**CDP Advantages:**
- ✅ Synchronous result retrieval (unlike `chrome_inject_script`)
- ✅ One-time execution (no persistent code injection)
- ✅ Function argument support with serialization
- ✅ Timeout control for safety

**Use Cases:**
- Extract data from page (e.g., `() => document.title`)
- Perform calculations with page data
- Query DOM state and return values
- Execute utilities without persistent injection

**Examples:**
```javascript
// Get page title
jsScript: "() => document.title"

// Calculate with arguments
jsScript: "(a, b) => a + b"
args: [5, 3]

// Extract JSON data from page
jsScript: "() => JSON.parse(document.getElementById('data').textContent)"
```

**Key Difference from chrome_inject_script:**
- `chrome_execute_script`: **One-time** execution, **returns value** synchronously
- `chrome_inject_script`: **Persistent** code injection, no return value

---

#### chrome_inject_script
Inject persistent JavaScript into page

**Parameters:**
- `jsScript` (string, required): JavaScript code
- `type` (string, required): Execution environment ("ISOLATED" or "MAIN")
- `url` (string, optional): Inject into specific URL page

**Execution Environments:**
- `ISOLATED`: Isolated environment (recommended, secure)
- `MAIN`: Main page environment (can access page globals)

---

#### chrome_send_command_to_inject_script
Send event to injected script

**Parameters:**
- `eventName` (string, required): Event name
- `payload` (string, optional): JSON format payload
- `tabId` (number, required): Target tab

---

#### chrome_console
Capture console output

**Parameters:**
- `url` (string, optional): Target page URL
- `maxMessages` (number, default: 100): Maximum messages
- `includeExceptions` (boolean, default: true): Include exceptions

---

## ⚡ Best Practices

### 1. Prefer CDP Tools

**Why CDP Tools are Better:**
- ✅ Background execution (no tab switching, faster)
- ✅ More reliable (Chrome DevTools Protocol)
- ✅ Better error reporting
- ✅ UID-based element targeting (most accurate)

**Recommended Tool Mapping:**

| Task | Recommended Tool | Notes |
|------|------------------|-------|
| Navigate | `chrome_navigate` | Background mode, faster |
| Screenshot | `chrome_screenshot` | Element-specific, full page support |
| Click | `chrome_click_element` | UID-based targeting |
| Fill form | `chrome_fill_or_select` | Auto-triggers events |
| Scroll | `chrome_scroll` | Precise pixel control |
| Keyboard | `chrome_keyboard` | Special keys support |
| Wait | `chrome_wait_for_element` | Background polling |
| Analyze page | `chrome_accessibility_snapshot` | UID-based element analysis |

---

### 2. Smart Navigation

**Standard Flow (CDP-Powered):**
```
1. get_windows_and_tabs             (Check existing tabs)
2. Analyze if matching tab exists
3. Match → Reuse tabId | No match → chrome_navigate
```

**URL Matching Rules:**
- Protocol agnostic: `http://` == `https://`
- www optional: `www.jd.com` == `jd.com`
- Query param order irrelevant: `?a=1&b=2` == `?b=2&a=1`
- Trailing slash ignored: `/products/` == `/products`
- Hash removed: `#section` removed before matching

**Performance Gain:** Background navigation saves 3-5 seconds per page

---

### 3. Element Interaction Workflow

**✅ Correct Approach (UID-based, Most Reliable):**
```
1. chrome_accessibility_snapshot  (Get elements with UIDs)
2. chrome_click_element(uid="...")  (Click using UID)
```

**❌ Old Approach (Selector-based, Less Reliable):**
```
1. chrome_screenshot_with_highlights  (Slower, visual only)
2. chrome_click_element(selector="...")  (May fail if selector changes)
```

**Why UID is Better:**
- Immune to CSS class changes
- Works with dynamically generated selectors
- No ambiguity with multiple matching elements

---

### 4. Navigation Verification (Performance Optimized)

**✅ Correct Approach (3 tools, ~2-3 seconds):**
```
1. get_windows_and_tabs              (0.5s)
2. chrome_navigate                   (1-2s, background)
3. chrome_screenshot                 (0.5s)
```

**❌ Wrong Approach (6+ tools, 60+ seconds):**
```
1. get_windows_and_tabs
2. chrome_accessibility_snapshot      ← Over-verification (use only when interaction needed)
3. fetch_file (screenshot)            ← Unnecessary
4. fetch_file (JSON)                  ← Unnecessary
5. Read JSON                          ← Why?
6. get_windows_and_tabs again         ← Duplicate
```

---

### 5. Parameter Best Practices

**chrome_get_web_content:**
- ✅ Must provide `tabId` (required parameter)
- ✅ Use `selector` to extract specific element content
- ✅ Prefer `outputFormat="markdown"` for better performance (smaller size, faster processing, clearer structure)

**chrome_screenshot:**
- ✅ Use `fullPage: true` only when necessary (performance impact)
- ✅ Use `selector` to capture specific elements

**chrome_click_element:**
- ✅ **Prefer UID over selector** for reliability
- Get UIDs from `chrome_accessibility_snapshot` first
- Only use selector/coordinates as fallback

**chrome_fill_or_select:**
- ✅ **Prefer UID over selector** for reliability
- Get UIDs from `chrome_accessibility_snapshot` first
- `clearFirst: true` by default (auto-clears existing content)

**chrome_scroll_into_view:**
- ✅ **Prefer UID over selector** for reliability
- Get UIDs from `chrome_accessibility_snapshot` first
- Use `block` and `inline` for precise alignment control

**chrome_scroll:**
- ✅ Provide `coordinates` parameter for predictable scrolling
- Recommended: `{x: 640, y: 360}` (viewport center for 1280x720)

---

### 6. Page Protection Best Practices

**When to Enable Protection:**
- ✅ Long automation workflows (>10 seconds)
- ✅ Multi-step form filling
- ✅ Critical data extraction operations
- ✅ Workflows where user interference could cause errors

**When to Disable Protection:**
- ✅ After automation completes successfully
- ✅ When encountering errors (cleanup)
- ✅ Before manual user intervention is needed
- ✅ Before closing tabs

**Protection Workflow Pattern:**
```
try {
    chrome_page_protection_enable(tabId)      // Enable at start
    // ... automation steps ...
} finally {
    chrome_page_protection_disable(tabId)     // Always cleanup
}
```

**⚠️ Critical Rules:**
- MUST disable protection before clicks if already enabled
- ALWAYS disable protection when automation ends
- Check status with `chrome_page_protection_status` if clicks fail unexpectedly
- Don't forget to disable on error paths

---

### 7. Error Handling

| Error Type | Strategy | Example |
|------------|----------|---------|
| Navigation timeout | Increase timeout, check network | `chrome_navigate(url, timeout=60000)` |
| Element not found | Use `chrome_wait_for_element` first | Wait before clicking |
| Screenshot timeout | Reduce viewport size or skip fullPage | Use default 800x600 |
| Hook denies tool execution | Check parameter constraints | Verify required parameters |
| Network request timeout | Retry with exponential backoff | Wait 2s, 4s, 8s between retries |

**General Principles:**
- Use `chrome_wait_for_element` before interacting with dynamic content
- Check hook constraints before tool calls (see Section 4)
- For unreliable pages: Take screenshot to verify state before proceeding

---

## 🎯 Quick Tool Selection Guide

### "I need to..."

| Task | Recommended Tool (CDP) | Notes |
|------|----------------------|-------|
| Open a webpage | `chrome_navigate` ⭐ | Background mode, faster |
| Check if page loaded | `chrome_screenshot` ⭐ | Visual verification |
| Find interactive elements | `chrome_accessibility_snapshot` ⭐ | Returns UIDs (PRIMARY) |
| Click a button | `chrome_click_element(uid)` ⭐ | Use UID from snapshot |
| Fill a form | `chrome_fill_or_select` ⭐ | Auto-triggers events |
| Scroll down/up | `chrome_scroll` ⭐ | Precise pixel control |
| Scroll to element | `chrome_scroll_into_view` 🆕 | Alignment control |
| Upload a file | `chrome_input_upload_file` 🆕 | Supports URL/base64 |
| Type keys | `chrome_keyboard` ⭐ | Special keys support |
| Wait for element | `chrome_wait_for_element` ⭐ | Background polling |
| Extract page content | `chrome_get_web_content` | HTML or Markdown |
| Execute JavaScript | `chrome_execute_script` ⭐ | Returns value synchronously |
| Send API request | See Network Requests table | Choose based on cookies/size |
| Go back/forward | `chrome_go_back_or_forward` 🆕 | History navigation |
| Check for errors | `chrome_screenshot` ⭐ | Visual inspection |
| Protect page from interference | `chrome_page_protection_enable` 🔒 | Blocks user interactions |
| Restore user control | `chrome_page_protection_disable` 🔓 | Removes protection overlay |
| Check protection status | `chrome_page_protection_status` | Debug interaction issues |

**Legend:** ⭐ = CDP-powered (recommended), 🆕 = New feature

### Decision Tree (CDP-Optimized)

```
Task: Navigate to a page
  ├─ Check browser state first? → get_windows_and_tabs
  ├─ Navigate (background) → chrome_navigate ⭐
  └─ Verify loading → chrome_screenshot ⭐

Task: Interact with elements (UID-based workflow)
  ├─ Get interactive elements → chrome_accessibility_snapshot ⭐
  ├─ Click button → chrome_click_element(uid="...") ⭐
  ├─ Fill form → chrome_fill_or_select(selector, value) ⭐
  └─ Extract data → chrome_get_web_content

Task: Advanced interaction
  ├─ Upload file → chrome_input_upload_file 🆕
  ├─ Type special keys → chrome_keyboard ⭐
  ├─ Scroll to element → chrome_scroll_into_view 🆕
  └─ Go back/forward → chrome_go_back_or_forward 🆕

Task: Execute custom logic
  ├─ Need return value? → chrome_execute_script ⭐ (one-time, returns value)
  └─ Need persistent code? → chrome_inject_script (persistent injection)

Task: Send network requests
  ├─ Large response (>100KB)? → fetch_api
  └─ Multiple requests? → fetch_api_batch

Task: Page protection (prevent interference)
  ├─ Start automation → chrome_page_protection_enable 🔒
  ├─ Check status → chrome_page_protection_status
  ├─ Clicks not working? → chrome_page_protection_disable 🔓 (must disable first)
  └─ End automation → chrome_page_protection_disable 🔓
```

---

## 🚫 Common Mistakes

| ❌ Wrong Approach | ✅ Correct Approach |
|------------------|---------------------|
| Navigate blindly without checking browser state | Call `get_windows_and_tabs` first |
| Use selector-based clicking directly | Use `chrome_accessibility_snapshot` first to get UIDs |
| Use basic screenshot for element analysis | Use `chrome_accessibility_snapshot` ⭐ (PRIMARY tool) |
| Click with selector only | Use `chrome_click_element(uid)` ⭐ (more reliable) |
| Fill form with selector only | Use `chrome_fill_or_select(uid)` ⭐ (more reliable) |
| Use `chrome_get_interactive_elements` | Use `chrome_accessibility_snapshot` ⭐ |
| Use `fullPage=true` without reason | Avoid (performance issue) |
| Call 7-8 tools for simple verification | 3-4 tools are enough |
| Don't provide `coordinates` for scrolling | Provide coordinates for predictable behavior |
| Expect HTML in response | Returns URL, use WebFetch to get HTML content |
| Try to navigate with `chrome_get_web_content` | Use `chrome_navigate` first, then fetch content |
| Clicks not working, protection enabled | Call `chrome_page_protection_disable` 🔓 first |
| Forget to disable protection after automation | Always call `chrome_page_protection_disable` 🔓 at the end |

---

### 📌 Understanding Tool Selection

**Scenario A: Verify Page Loading (Post-Navigation Check)**
- **Goal**: Confirm the page has loaded successfully
- **Tool**: `chrome_screenshot` ⭐ (lightweight, 0.5-1 second)
- **When**: Immediately after `chrome_navigate`
- **Example**: Check if homepage rendered correctly

**Scenario B: Find Elements for Interaction**
- **Goal**: Locate elements and get UIDs for clicking/filling
- **Tool**: `chrome_accessibility_snapshot` ⭐ (PRIMARY - returns elements with UIDs)
- **When**: Before clicking, filling, or analyzing page structure
- **Example**: Find the search button UID before clicking

**Decision Rule:**
```
Need to interact with elements? → chrome_accessibility_snapshot ⭐
Just checking if page loaded?   → chrome_screenshot ⭐
```

---

## Version History

- **v2.1.4** (2025-12-27): Parameter requirement update
  - 🔄 Changed: All `tabId` parameters from optional to required
  - 📖 Rationale: Explicit tab targeting improves reliability and reduces ambiguity in multi-tab scenarios

---

**Maintainer**: datasaver-agent project team

**Use Cases**: Data extraction, automated testing, page interaction automation
