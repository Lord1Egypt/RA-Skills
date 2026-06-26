--- 
name: learning-notes-explorer
description: 学习笔记 - Explore, search, and synthesize personal learning notes. Use when user asks about 笔记整理、学习回顾、知识搜索、笔记查询, or wants to explore their accumulated learning notes across topics. An interface to personal knowledge base.
---
 
# Learning Notes Explorer (学习笔记)
 
## Overview
 
This skill provides an interface to explore, search, and synthesize personal learning notes. It helps users retrieve relevant notes, discover connections between past learnings, and build on existing knowledge. Acts as a bridge between raw note-taking and actionable knowledge.
 
## When to Use This Skill
 
- Looking for specific information from past notes
- Reviewing notes on a particular topic
- Finding connections between different notes/topics
- Synthesizing knowledge from multiple sources
- Preparing to write or create based on past learning
- Checking what has been learned about a topic
- Discovering gaps in knowledge
 
## Core Functions
 
### 1. Note Search and Retrieval
- Search notes by keyword, topic, or concept
- Find notes from specific sources (books, courses, articles)
- Filter by date, tags, or categories
- Locate specific quotes or data points
 
### 2. Knowledge Discovery
- Identify related notes across topics
- Find patterns in learning history
- Surface connections user may have forgotten
- Highlight gaps in knowledge on a topic
 
### 3. Synthesis
- Combine relevant notes into coherent summaries
- Cross-reference insights from different sources
- Generate overview of knowledge on a subject
- Create study guides from note collections
 
### 4. Learning Path Guidance
- Recommend next steps based on existing knowledge
- Suggest topics to explore
- Identify prerequisites for advanced learning
- Map out learning journey on a topic
 
## Note Organization Model
 
The explorer works with notes organized in layers:
 
```
Learning Notes
├── Raw Notes (原始笔记)
│   ├── Book highlights & annotations
│   ├── Course notes
│   ├── Article clippings
│   └── Meeting/lecture notes
│
├── Processed Notes (整理笔记)
│   ├── Summaries
│   ├── Key concepts extracted
│   └── Questions generated
│
└── Connected Notes (关联笔记)
    ├── Personal insights
    ├── Cross-references
    └── Action items
```
 
## Usage Examples
 
### Search and Retrieval
```
"搜索我所有关于'刻意练习'的笔记"
"找出上周记录的读书笔记"
"查找关于Python的笔记"
"找出所有提到'第一性原理'的内容"
```
 
### Knowledge Review
```
"总结我关于时间管理的所有学习"    
"给我看看最近一个月学了什么"
"我关于心理学都有哪些笔记?"
"显示投资相关的所有笔记"
```
 
### Synthesis and Connections
```
"把关于'学习'的笔记整理成一个主题"
"找出'刻意练习'和'成长型思维'的关联"
"生成一个关于'写作'的知识总结"
"创建'决策'主题的阅读清单"
```
 
### Gap Analysis
```
"关于AI领域我还缺什么知识?"
"我哪个方面学习得最少?"
"有哪些相关主题我没有探索过?"
```
 
## Output Formats
 
### Search Results
```
Found X notes on "[topic]":
 
1. [Note Title] - [Source] - [Date]
   Preview: [First 2 lines]...
   Tags: [tag1], [tag2]
 
2. [Note Title] - [Source] - [Date]
   ...
```
 
### Synthesis Summary
```
## Knowledge Synthesis: [Topic]
 
### Key Concepts Learned
- [Concept 1]: From [source], [summary]
- [Concept 2]: From [source], [summary]
 
### Sources
- [Book 1] - [Key insight]
- [Course 2] - [Key insight]
 
### Practical Applications
- [Application 1]
- [Application 2]
 
### Suggested Next Steps
- [ ] Explore [related topic]
- [ ] Read [suggested source]
```
 
### Learning Path
```
## Learning Path: [Topic]
 
Prerequisites (already learned):
✓ [Concept A]
✓ [Concept B]
 
Recommended Sequence:
1. [Next topic] - Based on [note reference]
2. [Advanced topic] - After completing #1
3. [Expert topic] - Further study
 
Suggested Resources:
- [Book/Course] - Fills gap in [area]
```
 
## Integration with Other Skills
 
This skill works with:
- `book-knowledge-extractor` — For extracting and saving new notes
- `second-brain-triage` — For organizing notes in personal system
- `summarize` — For creating summaries of note collections
- `zettelkasten-writing-coach` — For writing based on note connections
 
## Limitations
 
- Depends on quality of underlying note collection
- May not find notes if indexing is incomplete
- Cannot "read" non-text content in notes
- Synthesis quality depends on note richness
 
## Implementation Notes
 
This skill requires:
- Access to note storage (local files, Obsidian vault, Notion, etc.)
- Note indexing system for search
- Source attribution for synthesized content
- User preferences for display format
 
## Acceptance Criteria
 
1. ✓ Can search notes by keyword/topic
2. ✓ Returns relevant results with context
3. ✓ Can synthesize multiple notes into summary
4. ✓ Identifies connections between notes
5. ✓ Provides learning path recommendations
6. ✓ Integrates with note sources
7. ✓ Respects user privacy in note access
