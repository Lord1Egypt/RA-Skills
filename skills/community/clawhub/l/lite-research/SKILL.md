---
name: lite-research
description: Perform lite research using web search and web fetch tools. Use when user asks to "research" something (not "deep research"). Uses advanced search strategies with synonyms, Boolean operators, and alternative terminology. Never spawns sub-agents.
---

# Lite Research Skill

This skill performs quick research by searching the web and reading the top results using built-in tools with advanced search strategies.

## When to Use This Skill

Use this skill when the user says "research <topic>" (but NOT "deep research"). This skill:
- Uses web_search to find results for multiple related queries using search best practices
- Uses web_fetch to read the top 5 results for each query
- Does NOT spawn sub-agents
- Provides a summary of findings with sources

## Advanced Search Strategy

Instead of basic queries, this skill uses research-proven techniques and limits queries to maximum 5:

### 1. Query Variations with Synonyms and Alternatives
For a topic like "artificial intelligence", create 2-5 queries like:
- "artificial intelligence" OR "AI" OR "machine learning"
- "artificial intelligence" overview introduction basics
- "artificial intelligence" recent developments 2024 2025
- "artificial intelligence" challenges problems issues
- "artificial intelligence" applications uses examples

**Limit**: Maximum 5 queries total to balance thoroughness with efficiency.

### 2. Boolean Operators and Search Techniques
- Use OR for synonyms: "climate change" OR "global warming"
- Use quotation marks for exact phrases
- Include both singular and plural forms
- Add time constraints when relevant

### 3. Alternative Terminology
Consider:
- Different spellings (globalization vs globalisation)
- Technical vs common terms ("myocardial infarction" vs "heart attack")
- Regional variations ("university" vs "college")
- Historical terminology changes

### 4. Multi-Perspective Approach
Create queries from different angles:
- Basic overview: "{topic} overview introduction"
- Current state: "{topic} 2024 2025 recent developments"
- Critical analysis: "{topic} challenges problems issues"
- Applications: "{topic} applications uses examples"

## Implementation Workflow

When user says "research <topic>":

1. **Analyze the topic** - identify key concepts and potential synonyms

2. **Create 2-5 strategic queries maximum** using:
   - Synonyms with OR operators
   - Different query types (overview, recent, critical, applications)
   - Time-specific terms when relevant
   - Quotation marks for exact phrases
   - **Important: Never exceed 5 distinct queries**

3. **Execute searches** with count=5 for each query (max 5 queries total)

4. **Fetch and analyze** content from results

5. **Compile findings** focusing on:
   - Key concepts and definitions
   - Current developments and trends
   - Different perspectives and applications
   - Notable challenges or controversies

## Example Queries for "renewable energy"

- "renewable energy" OR "clean energy" OR "green energy"
- "renewable energy" overview introduction "current state"
- "renewable energy" 2024 2025 "recent developments" trends
- "renewable energy" challenges problems limitations issues
- "renewable energy" applications examples projects case studies

**Maximum 5 queries total** - adjust based on topic complexity and available information.

## Important Notes

- Only triggers on "research" commands, not "deep research"
- Never spawn sub-agents - use direct tool calls
- Focus on comprehensive but quick overview
- Provide sources and URLs for transparency
- Adapt query strategy based on topic complexity