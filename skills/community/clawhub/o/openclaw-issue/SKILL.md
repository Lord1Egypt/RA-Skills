# OpenClaw Issue Creator | OpenClaw Issue 创建器

**English** | **中文**

A specialized skill for creating GitHub Issues for OpenClaw/ClawHub projects - supports Skill appeals, bug reports, and feature requests.

专为 OpenClaw/ClawHub 项目创建 GitHub Issue 的 skill - 支持 Skill 申诉、Bug 报告、功能请求等。

---

## Features | 功能

**English:**
- Quick creation of OpenClaw/ClawHub related Issues
- Built-in Skill appeal template (for skills flagged as suspicious)
- Built-in Bug report and feature request templates
- Support for generating pre-filled URLs or using GitHub CLI

**中文:**
- 快速创建 OpenClaw/ClawHub 相关 Issue
- 内置 Skill 申诉模板（针对被标记为可疑的 skill）
- 内置 Bug 报告和功能请求模板
- 支持生成预填充 URL 或使用 GitHub CLI

---

## Usage | 使用方法

**English:**

When a user requests to create an OpenClaw-related Issue, follow these steps:

**中文:**

当用户请求创建 OpenClaw 相关 Issue 时，按以下流程执行：

### Step 1: Determine Issue Type | 步骤 1：确定 Issue 类型

| Type | 中文 | Description | Label |
|------|------|-------------|-------|
| **skill-appeal** | Skill 申诉 | Skill flagged as suspicious, request review | `skill-appeal` |
| **bug** | Bug 报告 | Report a bug | `bug` |
| **feature** | 功能请求 | Feature request | `enhancement` |
| **question** | 问题咨询 | General question | `question` |

---

### Step 2: Collect Information | 步骤 2：收集信息

**English:**

Collect different information based on the type:

**中文:**

根据类型收集不同信息：

#### Skill Appeal | Skill 申诉

**English:**
1. **Skill Slug**: e.g., `social-media-dashboard`
2. **Skill Name**: e.g., `Social Media Dashboard`
3. **Owner**: Your username
4. **Skill description**
5. **Why it's a false positive** (optional)

**中文:**
1. **Skill Slug**: 如 `social-media-dashboard`
2. **Skill Name**: 如 `Social Media Dashboard`
3. **Owner**: 你的用户名
4. **Skill 功能描述**
5. **为什么是误报**（可选）

---

### Step 3: Create Issue | 步骤 3：创建 Issue

#### Method 1: Generate Pre-filled URL | 方式 1：生成预填充 URL（推荐）

```bash
python3 -c "
import urllib.parse

title = '<issue-title>'
body = '''<issue-body>'''

encoded_title = urllib.parse.quote(title)
encoded_body = urllib.parse.quote(body)

url = f'https://github.com/openclaw/clawhub/issues/new?title={encoded_title}&body={encoded_body}'
print(url)
"
```

#### Method 2: Use GitHub CLI | 方式 2：使用 GitHub CLI

```bash
gh issue create \
  --repo openclaw/clawhub \
  --title "<title>" \
  --body "<body>" \
  --label "<label>"
```

---

### Step 4: Return Result | 步骤 4：返回结果

**English:**

> ✅ Issue URL generated!
>
> 👉 [Click to submit Issue](<url>)
>
> Review the content and click **Submit new issue**.

**中文:**

> ✅ Issue 链接已生成！
>
> 👉 [点击提交 Issue](<url>)
>
> 打开后检查内容，点击 **Submit new issue** 即可。

---

## Issue Templates | Issue 模板

### Skill Appeal Template | Skill 申诉模板

```markdown
## Skill Information

- **Slug**: <skill-slug>
- **Name**: <skill-name>
- **Owner**: <username>
- **URL**: https://clawhub.ai/<username>/<skill-slug>

## Description

<skill-description>

## Why This is a False Positive

The skill was flagged because it contains patterns that resemble automation scripts, but these are **legitimate operations**:

1. **AppleScript/Browser Automation**: Used to automate user's own browser with their consent
2. **JavaScript Execution**: Standard practice for data extraction in controlled environments
3. **Shell Commands**: Local operations only, no external servers contacted

## Security Guarantee

- ✅ No external file downloads
- ✅ No credential theft or exfiltration
- ✅ No reverse shells or remote code execution
- ✅ No hardcoded API keys or secrets
- ✅ All operations are local to the user's machine

## Code Review

The skill file can be reviewed at:
https://clawhub.ai/<username>/<skill-slug>

## Request

Please review and remove the "suspicious patterns detected" flag from this skill.

Thank you!
```

### Bug Report Template | Bug 报告模板

```markdown
## Bug Description | Bug 描述

<description>

## Steps to Reproduce | 复现步骤

1. <step 1>
2. <step 2>
3. <step 3>

## Expected Behavior | 预期行为

<expected>

## Actual Behavior | 实际行为

<actual>

## Environment | 环境信息

- OS: <os>
- Version: <version>

## Screenshots | 截图

If applicable, add screenshots.
```

### Feature Request Template | 功能请求模板

```markdown
## Feature Description | 功能描述

<description>

## Use Case | 使用场景

<use-case>

## Proposed Solution | 建议方案

<solution>
```

---

## Trigger Words | 触发词

**English:**
```
Create OpenClaw Issue
Submit ClawHub Issue
Skill appeal
My skill was flagged
OpenClaw bug report
ClawHub feature request
```

**中文:**
```
创建 OpenClaw Issue
提交 ClawHub Issue
Skill 申诉
我的 Skill 被标记了
OpenClaw Bug 报告
ClawHub 功能请求
```

---

## Related Repositories | 相关仓库

| Repository | Purpose | 用途 |
|------------|---------|------|
| `openclaw/clawhub` | ClawHub platform issues, Skill appeals | ClawHub 平台问题、Skill 申诉 |
| `openclaw/openclaw` | OpenClaw core issues | OpenClaw 核心问题 |

---

## Notes | 注意事项

**English:**
- Requires a GitHub account
- Ensure the Skill doesn't contain malicious code before appealing
- Provide as much detail as possible to speed up review

**中文:**
- 需要 GitHub 账号
- 申诉前确保 Skill 确实不包含恶意代码
- 提供尽可能详细的信息以加快审核
