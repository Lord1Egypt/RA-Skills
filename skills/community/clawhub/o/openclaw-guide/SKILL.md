---
name: openclaw-guide
description: Authoritative OpenClaw guidance and documentation lookup. Provides accurate information about OpenClaw capabilities, configuration, and usage based on official sources (docs.openclaw.ai and github.com/openclaw/openclaw). Use when users ask about OpenClaw features, setup, configuration, troubleshooting, or any OpenClaw-related topics.
---

# OpenClaw Guide

## Purpose
Provide authoritative, up-to-date information about OpenClaw based on official documentation and source code. This skill ensures users receive accurate answers by consulting primary sources rather than relying on potentially outdated knowledge.

## When to Use This Skill
- User asks about OpenClaw capabilities, features, or functionality
- User needs help with OpenClaw configuration or setup
- User has questions about OpenClaw architecture or components
- User requests troubleshooting guidance for OpenClaw issues
- User wants to understand OpenClaw best practices or workflows
- Any query related to OpenClaw that requires official documentation verification

## Core Responsibilities

### 1. Official Documentation Lookup
- Always prioritize information from https://docs.openclaw.ai
- Search the official documentation for relevant sections
- Extract and present accurate, current information
- Cite specific documentation sections when possible

### 2. Source Code Verification
- Consult https://github.com/openclaw/openclaw for implementation details
- Verify feature availability and behavior against actual source code
- Check for recent changes or updates in the repository
- Reference specific files, commits, or branches when relevant

### 3. Information Synthesis and Presentation
- Analyze gathered information from official sources
- Present clear, concise, and actionable guidance
- Avoid speculation or assumptions beyond documented facts
- Acknowledge when information is not available in official sources

### 4. Response Quality Standards
- **Accuracy**: Only provide information verified from official sources
- **Currency**: Prioritize the most recent documentation and code
- **Completeness**: Cover all relevant aspects of the user's question
- **Clarity**: Present information in an understandable, well-structured format

## Workflow Process

### Step 1: Query Analysis
- Identify the specific OpenClaw topic or question
- Determine which official sources are most relevant (docs vs. source code)
- Plan the search strategy for efficient information retrieval

### Step 2: Documentation Search
```bash
# Use web search to find relevant documentation pages
web_search "site:docs.openclaw.ai <topic>"
web_fetch "https://docs.openclaw.ai/<relevant-page>"
```

### Step 3: Source Code Investigation (if needed)
```bash
# Search GitHub repository for implementation details
web_search "site:github.com/openclaw/openclaw <topic>"
# Or navigate specific repository sections
web_fetch "https://github.com/openclaw/openclaw/tree/main/<relevant-path>"
```

### Step 4: Information Synthesis
- Cross-reference documentation and source code findings
- Resolve any discrepancies by prioritizing source code (most current)
- Organize information logically based on user's needs
- Prepare clear, actionable response

### Step 5: Response Delivery
- Present verified information with appropriate context
- Include relevant links to official sources for user reference
- Offer practical examples or commands when applicable
- Acknowledge limitations if complete information is unavailable

## Tool Usage Guidelines

### Web Search Patterns
- For documentation: `site:docs.openclaw.ai <specific topic>`
- For source code: `site:github.com/openclaw/openclaw <feature or component>`
- For general OpenClaw info: `openclaw <topic> site:docs.openclaw.ai OR site:github.com/openclaw/openclaw`

### Web Fetch Best Practices
- Always fetch from official domains only
- Prefer documentation pages over blog posts or third-party sites
- When fetching GitHub pages, focus on README, docs, and source files
- Validate fetched content against multiple sources when possible

## Common Query Categories

### Configuration Questions
- Gateway setup and management
- Agent configuration and workspace setup
- Channel integration (Telegram, Discord, etc.)
- Security and permissions settings

### Feature Questions  
- Available skills and their capabilities
- CLI commands and usage patterns
- Automation and workflow capabilities
- Integration with external tools and services

### Troubleshooting Questions
- Error message interpretation
- Common setup issues and solutions
- Performance optimization guidance
- Debugging and logging procedures

### Architecture Questions
- Component relationships and data flow
- Security model and isolation boundaries
- Extensibility and customization options
- Deployment and scaling considerations

## Quality Assurance

### Verification Checklist
- [ ] Information sourced from official documentation or source code
- [ ] Links provided to original sources for user verification
- [ ] No speculation or assumptions beyond documented facts
- [ ] Response addresses the specific user question completely
- [ ] Technical accuracy verified against current implementation

### Response Templates

#### When Documentation is Clear:
```
Based on the official OpenClaw documentation at [link]:

[Concise summary of relevant information]

For more details, see: [specific documentation section]
```

#### When Source Code Provides Better Insight:
```
According to the OpenClaw source code at [GitHub link]:

[Implementation details or behavior explanation]

This means that [practical implication for the user].
```

#### When Information is Limited:
```
I checked the official OpenClaw documentation and source code, but couldn't find specific information about [topic]. 

The closest relevant information I found is [related topic] at [link].

You may want to check the latest documentation directly or ask in the OpenClaw community.
```

## Important Notes

- **Always verify**: Never assume knowledge about OpenClaw features without checking official sources
- **Stay current**: OpenClaw evolves rapidly; always check for the latest documentation
- **Be precise**: Provide exact commands, file paths, and configuration options when available
- **Cite sources**: Always include links to official documentation or source code
- **Acknowledge limits**: If official sources don't contain the answer, say so clearly

## References

### Primary Sources
- Official Documentation: https://docs.openclaw.ai
- Source Repository: https://github.com/openclaw/openclaw
- Community: https://discord.com/invite/clawd

### Related Skills
- `github`: For detailed GitHub repository operations
- `web_search`: For broader information gathering when needed
- `clawhub`: For skill-related queries and management