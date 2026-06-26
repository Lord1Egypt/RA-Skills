---
name: page_js_operation
description: Operate web page elements via CDP and Page JS Extension, save 95% Token (for UI automation testing only)
tools:
  - cdp
---

# Page JS CDP Web Operation Skill

## ⚠️ Important Notice

**This Skill is designed for browser automation testing scenarios only, NOT for handling sensitive data pages.**

### 🎯 Usage Recommendations

**✅ Recommended for:**
- Automation testing environments
- UI testing in CI/CD pipelines
- Page function verification during development
- Web operation demos with public information

**❌ NOT Recommended for:**
- Daily website browsing
- Pages handling personal sensitive information
- Production environment automation (unless thoroughly tested)

### Dependencies

This Skill **must** be used with the following components:

1. **Page JS Extension** - Chrome Extension (manual installation required)
   - GitHub: https://github.com/TangJing/openclaw_access_web_page_js
   - **Please download and review source code before installation**
   - Installation: `chrome://extensions/` → Developer mode → Load unpacked

2. **CDP Environment** - Chrome DevTools Protocol access
   - Local: `http://127.0.0.1:9222`
   - Or automation frameworks like Puppeteer/Playwright

---

## Workflow

1. **Check Extension** → Verify `ElementCollector` is injected (first time only)
2. **Get Element Index** → Call `exportData()` to get element key list (non-sensitive)
3. **AI Analysis** → Identify target elements by keys (buttons, inputs, etc.)
4. **Execute Operation** → Perform click/input operations via CDP

---

## ⚠️ Security Restrictions

### Prohibited Page Types

**DO NOT use this Skill on:**

- 🔒 Banking/financial websites
- 🔒 Login/registration pages (involving passwords)
- 🔒 Payment pages
- 🔒 Healthcare/medical websites
- 🔒 Government/ID-related websites
- 🔒 Any pages containing personal sensitive information

### Prohibited Data Types

**DO NOT read or modify:**

- Password input fields (`type="password"`)
- Credit card number inputs
- National ID number inputs
- Other sensitive personal data fields

### Recommended Operation Scenarios

**This Skill is suitable for:**

- ✅ Web operations with public information
- ✅ Automation testing environments
- ✅ Non-sensitive form filling (e.g., search boxes)
- ✅ Button click operations
- ✅ Dropdown selection operations

---

## Operation Templates

### Check Extension Availability (First Launch)

```javascript
typeof ElementCollector !== 'undefined'
// Returns true if extension is installed
```

### Get Page Element Index (Non-sensitive)

```javascript
ElementCollector.exportData()
// Returns: { elements: [...keys], keywords: [...], elementCount: N }
// Note: Only returns element key list, not actual DOM content
```

### Click Button

```javascript
const results = ElementCollector.searchElementsByKey('{button-keyword}');
const element = Object.values(results)[0];
if (element) element.click();
```

### Fill Regular Input (Non-sensitive)

```javascript
const inputs = ElementCollector.searchElementsByKey('{search-box/input}');
const input = Object.values(inputs)[0];
if (input) {
  input.value = '{value}';
  input.dispatchEvent(new Event('input', { bubbles: true }));
}
```

### Select Dropdown Option

```javascript
const selects = ElementCollector.searchElementsByKey('{selector-keyword}');
const select = Object.values(selects)[0];
if (select) {
  select.value = '{option-value}';
  select.dispatchEvent(new Event('change', { bubbles: true }));
}
```

---

## CDP Command Reference

| Operation | CDP Runtime.evaluate Expression |
|-----------|--------------------------------|
| Check extension | `typeof ElementCollector !== 'undefined'` |
| Get index | `ElementCollector.exportData()` |
| Click | `ElementCollector.searchElementsByKey('btn')[0].click()` |
| Fill | `ElementCollector.searchElementsByKey('input')[0].value = 'text'` |
| Select | `ElementCollector.searchElementsByKey('select')[0].value = 'option'` |

---

## Common Keywords

| Operation | Recommended Keywords |
|-----------|---------------------|
| Search | `'搜索'`, `'search'` |
| Submit | `'提交'`, `'submit'` |
| Cancel | `'取消'`, `'cancel'` |
| Confirm | `'确定'`, `'confirm'` |
| Delete | `'删除'`, `'delete'` |
| Edit | `'编辑'`, `'edit'` |
| Save | `'保存'`, `'save'` |

---

## ⚠️ Privacy & Data Flow

### Data Flow

```
Browser DOM → ElementCollector (Memory Index) → CDP → Local AI Agent
                     ↑
              (Key list only, no sensitive content)
```

### Privacy Notice

1. **Extension Level**:
   - ✅ Page JS Extension runs entirely in browser locally
   - ✅ Does not proactively send data to external servers
   - ✅ Data stored in memory, cleared when page closes

2. **Agent Level**:
   - ⚠️ **AI Agent may send element data to LLM services**
   - ⚠️ Element keys may contain page text content (button labels, input labels)
   - ⚠️ Ensure your AI Agent configuration meets privacy requirements

3. **User Responsibility**:
   - ⚠️ Users must review extension source code themselves
   - ⚠️ Users must ensure AI Agent won't send sensitive data to untrusted services
   - ⚠️ Users must avoid using this Skill on sensitive pages

### Data Scope

| Data Type | Collected | Operable | Description |
|-----------|-----------|----------|-------------|
| Element id | ✅ Yes | - | For indexing |
| Element class | ✅ Yes | - | For indexing |
| Element title | ✅ Yes | - | For indexing |
| Element innerText | ✅ Yes | - | For indexing (max 100 chars) |
| Regular inputs | ✅ Yes | ✅ Read/Write | Searchable, fillable, readable |
| Password fields | ❌ **Not collected** | ⚠️ **Write only** | Not indexed, cannot search by keyword, but can set value via native DOM |
| Hidden fields | ❌ **Not collected** | ⚠️ **Write only** | Not indexed, cannot search by keyword, but can set value via native DOM |
| File uploads | ❌ **Not collected** | ⚠️ **Write only** | Not indexed, cannot search by keyword, but can set value via native DOM |
| Cookie/Storage | ❌ No | ❌ Inaccessible | Extension has no such permission |

**Technical Implementation:**

```javascript
// Automatically skip sensitive fields in collectAllElements()
const sensitiveTypes = ['password', 'hidden', 'file'];
if (element.tagName === 'INPUT' && sensitiveTypes.includes(element.type)) {
  return;  // Not collected to index, cannot search via searchElementsByKey
}
```

**Note:** Sensitive fields are not indexed but can still be operated via native DOM API (e.g., `document.querySelector('input[type="password"]').value = 'xxx'`). This extension does not proactively read values from these fields.

---

## Installation Steps

### Step 1: Install Page JS Extension

```bash
# 1. Download source code
git clone https://github.com/TangJing/openclaw_access_web_page_js.git
cd openclaw_access_web_page_js

# 2. Review source code (recommended)
# Check for:
# - Network request code
# - Data exfiltration logic
# - manifest.json permissions

# 3. Install extension
# Open chrome://extensions/
# Enable "Developer mode"
# Click "Load unpacked", select project directory
```

### Step 2: Install OpenClaw Skill

```bash
# 1. Create Skill directory
mkdir -p ~/.openclaw/workspace/skills/page-js-operation

# 2. Save this SKILL.md to the directory
# Path: ~/.openclaw/workspace/skills/page-js-operation/SKILL.md

# 3. Refresh Skills
openclaw agent --message "refresh skills"
```

---

## Usage Examples

### Safe Scenario: Search Operation

```bash
# On search engine page
openclaw agent --message "use page_js_operation to fill search box with 'keyword'"
openclaw agent --message "use page_js_operation to click search button"
```

### Safe Scenario: Navigation Operation

```bash
# On content page
openclaw agent --message "use page_js_operation to click next page button"
openclaw agent --message "use page_js_operation to select category from dropdown"
```

### ❌ Prohibited Scenario: Login Operation

```bash
# DO NOT use on login pages
# openclaw agent --message "fill username and password and click login"
# Reason: Involves password fields
```

---

## Security Best Practices

1. **Use Dedicated Browser Profile**
   - Create separate Chrome user profile for automation testing
   - Do not save any real account credentials in test profile

2. **Limit Accessible Domains**
   - Restrict accessible domains in extension settings
   - Only allow test environments or public websites

3. **User Confirmation Mechanism**
   - Require user confirmation before sensitive operations
   - E.g., form submissions, deletions

4. **Regular Review**
   - Periodically review extension code for updates
   - Check Skill execution logs

---

## Technical Notes

### ElementCollector Working Principle

```javascript
// Collection phase
elementMap = Map<key, Element>  // key → DOM reference
keywordMap = Map<keyword, Set<keys>>  // keyword → key set

// key format: id|class|title|innerText
// Example: "login-btn|btn primary||Login"
```

### Why Token Savings

- **Traditional**: Send complete HTML (5000-20000 tokens)
- **This Extension**: Send element key list only (100-500 tokens)
- **Savings**: ~95%+

---

## Disclaimer

**By using this Skill, you agree:**

1. You have reviewed and trust the Page JS Extension source code
2. You understand AI Agent may send element data to LLM services
3. You will not use this Skill on pages involving sensitive information
4. You assume all risks of using this Skill
5. The Skill author is not liable for any data breaches or losses

---

## Links

- [GitHub Repository](https://github.com/TangJing/openclaw_access_web_page_js)
- [Chrome Extension Documentation](https://developer.chrome.com/docs/extensions/)
- [Chrome DevTools Protocol](https://chromedevtools.github.io/devtools-protocol/)
