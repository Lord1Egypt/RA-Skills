---
name: translator
description: Professional Chinese-English bidirectional translation for technical documentation, following established style guides and terminology standards. Use when translating technical documents, API documentation, user guides, product descriptions, code comments, or any technical content between Chinese and English. Ensures consistency, accuracy, and adherence to technical writing conventions.
---

# Translator

## Overview

This skill provides professional Chinese-English bidirectional translation specialized for technical documentation. It ensures translations follow industry-standard style guides, maintain terminology consistency through a comprehensive terminology database, and adhere to technical writing best practices.

## Core Translation Workflow

### 1. Understand the Content

Before translating:
- Read the entire content to understand context and purpose
- Identify the document type (API docs, user guide, tutorial, etc.)
- Note any special terminology or technical concepts
- Understand the target audience

### 2. Apply Translation Standards

**For Chinese to English:**
- Use active voice and present tense
- Address the reader directly with "you"
- Keep sentences concise and clear
- Follow English punctuation rules (half-width)
- Use bold for UI elements: **Button Name**
- Use code formatting for technical terms: `function_name()`

**For English to Chinese:**
- Use formal written Chinese, avoid colloquialisms
- Follow Chinese punctuation rules (full-width for Chinese, half-width for code)
- Add spaces around English words in Chinese text
- Keep technical names in English: React, API, JSON
- Use bold for UI elements: **按钮名称**

### 3. Ensure Terminology Consistency

**Always check the terminology database first:**
- Load `references/terminology.md` to find standard translations
- Use the exact translations specified in the terminology table
- For terms not in the database, follow industry conventions
- Maintain consistency throughout the document

**For first occurrences:**
- Chinese to English: Optionally use "English (中文注释)" format
- English to Chinese: Optionally use "中文（English）" format
- Subsequent uses maintain the standard translation

### 4. Maintain Technical Accuracy

**Code elements:**
- Never translate variable names, function names, or code syntax
- Translate code comments according to target language
- Keep string literals as-is unless they're user-facing text
- Preserve code formatting and indentation

**Technical concepts:**
- Ensure technical meaning is preserved
- Do not add or remove information
- Maintain logical relationships from the original
- Verify technical accuracy over linguistic fluency

### 5. Format Properly

**Document structure:**
- Preserve markdown formatting
- Maintain heading hierarchy
- Keep lists and tables properly formatted
- Ensure links remain functional

**Special elements:**
- Translate alt text for images
- Keep code blocks untranslated (except comments)
- Format UI paths consistently: **Settings** > **Security**
- Use appropriate note/warning/tip formatting

## Quick Translation Patterns

### Common Scenarios

**API Documentation:**
```markdown
Original (EN):
### Get User Profile
Retrieves the profile information for a specific user.

Translation (ZH):
### 获取用户资料
获取指定用户的资料信息。
```

**User Instructions:**
```markdown
Original (EN):
Click **Save** to save your changes.

Translation (ZH):
点击**保存**按钮保存更改。
```

**Technical Descriptions:**
```markdown
Original (ZH):
该函数返回一个包含用户数据的 JSON 对象。

Translation (EN):
This function returns a JSON object containing user data.
```

## Reference Materials

This skill includes comprehensive reference materials. Load them as needed:

### Style Guide
`references/style-guide.md` - Complete translation style guide including:
- Translation principles (accuracy, consistency, readability)
- Chinese to English conventions
- English to Chinese conventions
- Punctuation rules
- Number and unit formatting
- Code-related translation guidelines
- Common expression mappings

**When to load:** Reference when you need clarification on style conventions, punctuation rules, or formatting standards.

### Terminology Database
`references/terminology.md` - Comprehensive technical terminology with standard Chinese-English mappings covering:
- Software development terms (API, SDK, framework, etc.)
- Cloud computing and architecture
- Data and storage
- Network and security
- Frontend development
- API and integration
- User interface elements
- Development tools
- Document structure terms
- Status and operation terms
- Common verbs

**When to load:** Reference at the start of any translation task to ensure terminology consistency. Search for specific terms as needed during translation.

### Writing Guidelines
`references/writing-guidelines.md` - Technical writing best practices including:
- Document structure standards
- Writing style (clarity, active voice, present tense, second person)
- Formatting standards for code, UI elements, links, images
- Notes and warnings formatting
- Step-by-step instructions format
- API documentation standards
- Code examples guidelines
- Tables and version documentation

**When to load:** Reference when creating or translating technical documentation to ensure it follows professional technical writing standards.

## Quality Checklist

Before finalizing any translation, verify:

**Accuracy:**
- [ ] Technical meaning preserved
- [ ] No information added or removed
- [ ] Logical relationships maintained
- [ ] Code elements untranslated (except comments)

**Consistency:**
- [ ] Terminology matches the database
- [ ] Style follows the guide
- [ ] Tone is consistent throughout
- [ ] Format is consistent

**Readability:**
- [ ] Clear and natural in target language
- [ ] Appropriate for target audience
- [ ] Not overly literal
- [ ] Flows well

**Format:**
- [ ] Markdown formatting preserved
- [ ] Code blocks properly formatted
- [ ] Links functional
- [ ] Punctuation correct for target language
- [ ] UI elements properly marked (bold)
- [ ] Code elements properly marked (backticks)

## Usage Examples

**Example 1: User asks for API documentation translation**
```
User: "请将这段 API 文档翻译成中文"

Process:
1. Load references/terminology.md to check API-related terms
2. Read the entire API documentation
3. Translate following Chinese conventions (full-width punctuation, spaces around English)
4. Maintain code examples unchanged
5. Ensure UI elements are bolded
6. Verify terminology consistency
```

**Example 2: User asks for user guide translation**
```
User: "Translate this user guide to English"

Process:
1. Load references/terminology.md and references/style-guide.md
2. Identify UI elements and technical terms
3. Translate using active voice, present tense, second person
4. Keep technical terms standardized
5. Format UI elements with bold
6. Check formatting and readability
```

**Example 3: User asks for terminology verification**
```
User: "检查这段翻译的术语是否一致"

Process:
1. Load references/terminology.md
2. Extract all technical terms from the text
3. Compare against standard translations
4. Identify inconsistencies
5. Provide corrections with reference to terminology database
```
