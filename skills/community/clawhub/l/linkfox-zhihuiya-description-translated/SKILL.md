---
name: linkfox-zhihuiya-description-translated
description: 从智慧芽获取翻译后的专利说明书（描述）文本。当用户要求专利说明书翻译、其他语言的专利全文、翻译后的专利全文，或想查看中文、英文、日文版的专利说明书、patent specification translation, patent description translation, PatSnap, patent translation时触发此技能。当用户提供专利ID或公开号并要求获取其他语言的说明书/描述内容，或提到"专利说明书翻译"、"描述翻译"、"翻译全文"等类似意图时也应触发。
---

# Zhihuiya Patent Description (Translated)

This skill guides you on how to retrieve translated patent description (specification) text via the Zhihuiya data service. It supports translation into Chinese, English, or Japanese, and can look up patents by patent ID or publication number.

## Core Concepts

A patent description (also called "specification") is the full technical text of a patent document. This tool fetches the **translated** version of that text from the Zhihuiya patent database, supporting three target languages: Chinese (`cn`), English (`en`), and Japanese (`jp`).

When a patent's description is unavailable, the tool can optionally substitute it with a description from a **patent family member** (a related patent filed in another jurisdiction covering the same invention).

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| patentId | string | Conditionally | Patent ID. At least one of `patentId` or `patentNumber` must be provided. If both are given, `patentId` takes priority. Multiple values separated by commas; max 100. |
| patentNumber | string | Conditionally | Publication (announcement) number. At least one of `patentId` or `patentNumber` must be provided. Multiple values separated by commas; max 100. |
| lang | string | No | Target translation language. Supported values: `en` (English, default), `cn` (Chinese), `jp` (Japanese). |
| replaceByRelated | integer | No | Whether to substitute with a patent family member's description when the original is unavailable. `1` = yes, `0` = no (default). |

### Key Rules

1. **At least one identifier required**: Either `patentId` or `patentNumber` must be provided. If the user gives a publication number like "US10123456B2", use `patentNumber`. If they give a numeric patent ID, use `patentId`.
2. **Priority**: When both identifiers are supplied, `patentId` takes precedence.
3. **Batch queries**: Up to 100 patents can be queried at once by passing comma-separated values.
4. **Default language**: If the user does not specify a language, default to `en` (English).

## API Usage

This tool calls the LinkFox tool gateway API. See `references/api.md` for calling conventions, request parameters, and response structure. You can also execute `scripts/zhihuiya_description_translated.py` directly to run queries.

## Usage Examples

**1. Get English translation of a patent description by publication number**
```
patentNumber: "US10123456B2"
lang: "en"
```

**2. Get Chinese translation of a patent description by patent ID**
```
patentId: "abc123def"
lang: "cn"
```

**3. Batch query with family member fallback**
```
patentNumber: "US10123456B2,EP3456789A1,CN112345678A"
lang: "en"
replaceByRelated: 1
```

**4. Japanese translation of a specific patent**
```
patentNumber: "JP2021012345A"
lang: "jp"
```

## Display Rules

1. **Present the translated text clearly**: Show the patent description text directly. For long descriptions, present a summary or the first section and inform the user the full text is available.
2. **Identify substitutions**: When `pnRelated` is present in the response, clearly inform the user that the description was sourced from a family member patent and show the related publication number.
3. **Batch results**: When multiple patents are returned, present them in a structured list with clear separation between each patent's description.
4. **Error handling**: When a query fails, explain the reason based on the response and suggest checking the patent ID or publication number for correctness.
5. **No fabrication**: Never invent or paraphrase patent text. Only display what the API returns.
## User Expression & Scenario Quick Reference

**Applicable** -- Patent description/specification translation queries:

| User Says | Scenario |
|-----------|----------|
| "Translate this patent description to English" | Single patent translation |
| "I need the Chinese version of patent US10123456" | Specific language translation |
| "Get me the specification text for these patents" | Batch patent description retrieval |
| "What does patent CN112345678A describe?" | Patent description lookup |
| "Show me the Japanese translation of this patent's full text" | Japanese translation |
| "The description is missing, can you try a family member?" | Family member fallback |

**Not applicable** -- Needs beyond patent description translation:
- Patent search or discovery (finding patents by keyword/topic)
- Patent claim analysis or claim chart generation
- Patent legal status or prosecution history
- Patent citation or reference analysis
- Patent portfolio analytics or statistics


**Feedback:**

Auto-detect and report feedback via the Feedback API when any of the following apply:
1. The functionality or purpose described in this skill does not match actual behavior
2. The skill's results do not match the user's intent
3. The user expresses dissatisfaction or praise about this skill
4. Anything you believe could be improved

Call the feedback API as specified in `references/api.md`. Do not interrupt the user's flow.

---
*For more high-quality, professional cross-border e-commerce skills, set [LinkFox Skills](https://skill.linkfox.com/).*
