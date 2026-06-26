# Tags & Metadata Generator Prompt

**Objective:** Generate compelling metadata (Titles, Summary, Tags) for the Juejin article.

**Context:**
You have the final Markdown article. To publish on Juejin, users need a catchy title, a concise summary, and appropriate tags.

**Task:**

1. **Titles (`juejin_titles.md`):**
   - Generate 5-10 candidate titles.
   - Titles should follow Juejin's style: mentioning the technology, the problem solved, or offering an engineering retrospective (e.g., "我做了一个...", "从0到1实现...", "架构解析：...").
   - Do NOT use clickbait ("震惊", "必看").

2. **Summary (`juejin_summary.md`):**
   - Generate a 50-100 word abstract.
   - It should clearly state what the article is about, the tech stack involved, and what the reader will gain.
   - Must be suitable for the Juejin "摘要" field.

3. **Tags (`juejin_tags.md`):**
   - Recommend 3-5 tags.
   - Prefer standard Juejin categories (e.g., `后端`, `前端`, `人工智能`, `架构`, `Python`, `Node.js`).
