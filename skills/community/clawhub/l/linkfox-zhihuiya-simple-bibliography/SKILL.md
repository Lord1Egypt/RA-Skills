---
name: linkfox-zhihuiya-simple-bibliography
description: 从智慧芽专利数据库查询专利简要著录（书目）数据。当用户提到专利著录信息查询、专利基本信息获取、专利书目数据、专利公开详情、按专利号查询发明人、专利申请人信息、专利摘要获取、专利分类号（IPC/CPC）、专利引用查询或任何通过专利ID、公开号检索结构化元数据的请求、patent brief bibliography, patent basic info, patent number lookup, patent abstract, PatSnap, patent metadata时触发此技能。即使用户未明确提及"智慧芽"或"著录信息"，只要其需求涉及查询特定专利的核心著录字段，也应触发此技能。
---

# Zhihuiya Patent Simple Bibliography

This skill guides you on how to query simple bibliographic data for patents using the Zhihuiya patent database, helping users retrieve structured patent metadata efficiently.

## Core Concepts

The Zhihuiya Simple Bibliography tool retrieves basic bibliographic (front-page) information for patents. Given one or more patent IDs or publication numbers, it returns structured metadata including title, abstract, applicants, inventors, assignees, classification codes, filing dates, priority claims, and citation references.

**Lookup modes**: You can look up patents by either `patentId` (Zhihuiya internal patent ID) or `patentNumber` (public publication/grant number). If both are supplied, `patentId` takes priority. Multiple values are separated by commas, with a maximum of 100 per request.

## Parameter Guide

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| patentId | string | Conditionally | Zhihuiya internal patent ID. Comma-separated for multiple values, max 100. At least one of `patentId` or `patentNumber` must be provided. |
| patentNumber | string | Conditionally | Public publication/grant number (e.g., `US11234567B2`, `CN115000000A`). Comma-separated for multiple values, max 100. At least one of `patentId` or `patentNumber` must be provided. |

**Priority rule**: When both `patentId` and `patentNumber` are present, the API uses `patentId` and ignores `patentNumber`.

## Response Data Fields

| Field | API Name | Description |
|-------|----------|-------------|
| Patent ID | patentId | Zhihuiya internal patent identifier |
| Title | title | Patent title |
| Abstract | abstractContent | Patent abstract text |
| Publication Number | publicationNumber | Publication number |
| Publication/Grant Number | pn | Full publication/grant number |
| Country Code | country | Country code of the patent |
| Publication Country | publicationCountry | Country where the patent was published |
| Publication Date | publicationDate | Publication date |
| Publication Kind | publicationKind | Kind code of the publication |
| Patent Type | patentType | Type of patent (e.g., invention, utility model, design) |
| Kind Code | kind | Patent kind code |
| Application Number | applicationNo | Application number |
| Application Date | applicationDate | Application filing date |
| Applicants | applicants | List of applicants |
| Inventors | inventors | List of inventors |
| Assignees | assignees | List of patent assignees/owners |
| Assignee Addresses | assigneeAddresses | List of assignee addresses |
| IPC Main | ipcMain | Main IPC classification code |
| IPC Further | ipcFurther | Additional IPC classification codes |
| CPC Main | cpcMain | Main CPC classification code |
| CPC Further | cpcFurther | Additional CPC classification codes |
| LOC | loc | Locarno classification codes (design patents) |
| GBC | gbc | GBC classification codes |
| Priority Claims | priorityClaims | List of priority claim entries |
| PCT Application No | pctApplicationNo | PCT international application number |
| PCT Filing Date | pctFilingDate | PCT international filing date |
| PCT Entry Date | pctEntryDate | PCT national phase entry date |
| Cited Patents | citedPatents | List of cited patent references |
| Cited Non-Patents | citedNonPatents | List of cited non-patent literature |

## API Usage

This tool calls the LinkFox tool gateway API. See `references/api.md` for calling conventions, request parameters, and response structure. You can also execute `scripts/zhihuiya_simple_bibliography.py` directly to run queries.

## Usage Examples

**1. Look up a single patent by publication number**
```
User: "Show me the bibliographic info for patent US11234567B2."
Action: Call with patentNumber = "US11234567B2"
```

**2. Look up multiple patents by publication number**
```
User: "Get the basic info for CN115000000A, EP4000000A1, and JP2023100000A."
Action: Call with patentNumber = "CN115000000A,EP4000000A1,JP2023100000A"
```

**3. Look up patents by Zhihuiya patent ID**
```
User: "Retrieve bibliography for patent IDs abc123 and def456."
Action: Call with patentId = "abc123,def456"
```

**4. Retrieve inventor and applicant information**
```
User: "Who are the inventors and applicants for patent US20230001234A1?"
Action: Call with patentNumber = "US20230001234A1", then extract the inventors and applicants fields from the response.
```

**5. Check patent classification codes**
```
User: "What IPC and CPC codes does patent EP3999999B1 have?"
Action: Call with patentNumber = "EP3999999B1", then present ipcMain, ipcFurther, cpcMain, and cpcFurther from the response.
```

**6. Get patent abstract and citation references**
```
User: "Show me the abstract and cited patents for CN114000000B."
Action: Call with patentNumber = "CN114000000B", then display abstractContent and citedPatents.
```

## Display Rules

1. **Present data clearly**: Show bibliographic results in well-structured tables or grouped sections. For a single patent, use a key-value layout. For multiple patents, use a table with the most relevant columns.
2. **Selective display**: When results contain many fields, prioritize showing title, publication number, applicants, inventors, application date, publication date, IPC/CPC main codes, and abstract. Show additional fields only when the user specifically asks.
3. **List fields**: For array fields (inventors, applicants, assignees, classification codes, citations), present them as comma-separated values or bulleted lists depending on length.
4. **Empty fields**: Omit fields that are null or empty from the display rather than showing blank entries.
5. **Error handling**: When a query fails, explain the reason based on the error message and suggest the user verify the patent number or ID format.
6. **Batch result notice**: When querying many patents at once, remind the user that the maximum is 100 per request.
## Important Limitations

- **Maximum batch size**: Up to 100 patent IDs or publication numbers per request.
- **At least one identifier required**: Either `patentId` or `patentNumber` must be provided; omitting both will cause an error.
- **patentId takes priority**: If both parameters are supplied, only `patentId` is used.
- **Data scope**: This tool returns simple bibliographic data only. It does not return full-text claims, detailed descriptions, legal status, or patent family information.

## User Expression & Scenario Quick Reference

**Applicable** -- Patent bibliographic data retrieval:

| User Says | Scenario |
|-----------|----------|
| "Look up patent XX" / "Get info for patent XX" | Single patent bibliography lookup |
| "Who invented patent XX" / "Who is the applicant" | Inventor / applicant retrieval |
| "What's the IPC code for XX" / "Classification of XX" | Classification code lookup |
| "Show me the abstract of XX" | Abstract retrieval |
| "When was patent XX filed" / "Publication date of XX" | Date information lookup |
| "What patents does XX cite" | Citation reference lookup |
| "Get bibliographic data for these patents: A, B, C" | Batch bibliography query |
| "Patent basic info" / "Patent front page data" | General bibliography retrieval |

**Not applicable** -- Needs beyond simple bibliographic data:

- Full-text patent claims or detailed description
- Patent legal status or prosecution history
- Patent family / equivalents analysis
- Patent valuation or landscaping
- Freedom-to-operate or infringement analysis
- Patent search by keyword or semantic query (this tool requires specific patent identifiers)


**Feedback:**

Auto-detect and report feedback via the Feedback API when any of the following apply:
1. The functionality or purpose described in this skill does not match actual behavior
2. The skill's results do not match the user's intent
3. The user expresses dissatisfaction or praise about this skill
4. Anything you believe could be improved

Call the feedback API as specified in `references/api.md`. Do not interrupt the user's flow.

---
*For more high-quality, professional cross-border e-commerce skills, set [LinkFox Skills](https://skill.linkfox.com/).*
