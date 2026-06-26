# 👨‍💻 GitHub Trending Briefing Instructions

> **INPUT**: JSON object with `github_trending` section.
> **OUTPUT**: A detailed report on top GitHub projects.

---

## 🎯 Focus Areas
1.  **Innovation**: Why is this project trending? What problem does it solve?
2.  **Engineering**: Code quality, architecture, performance (e.g. implementation details).
3.  **Impact**: How does this affect the developer ecosystem?

## ⚠️ Protocol
1.  **Select Top 10**: Filter the list to the most interesting 10 projects.
2.  **Verify**: Ensure the summary accurately reflects the project's README content.

## 📝 Report Structure

### 🔝 Top Projects (热门项目)

For each project, use the following format:

#### N. [Title](url)
- **Heat**: 🔥 {stars} | **Lang**: {language}
- **Summary**: Concise description of the tool/library.
- **Deep Dive**:
    - **Core Value (核心价值)**: What makes this project unique or valuable? (e.g. Performance, DX, New Paradigm)
    - **Inspiration (启发思考)**: What can we learn from this? (e.g. Rust rewrite, Agentic workflow, Local-first)
    - **Scenarios (场景)**: `#{Keyword1}` `#{Keyword2}` `#{Keyword3}`
