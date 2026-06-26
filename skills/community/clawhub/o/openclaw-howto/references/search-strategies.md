# OpenClaw Search Strategy Guide

## Table of Contents
1. [Search Scenario Classification](#search-scenario-classification)
2. [MiniMax web_search Usage](#minimax-web_search-usage)
3. [Official Documentation Search](#official-documentation-search)
4. [CLI Command Search](#cli-command-search)
5. [Knowledge Base Maintenance](#knowledge-base-maintenance)
6. [Search Optimization Tips](#search-optimization-tips)

## Search Scenario Classification

### Scenario 1: Fuzzy Capability Query
**Characteristics**: User asks if OpenClaw supports a feature, but you're unsure about the specific implementation.

**Example Questions**:
- "Can OpenClaw handle images?"
- "Does OpenClaw support cron jobs?"
- "Does OpenClaw have email sending functionality?"

**Processing Strategy**:
1. Use MiniMax web_search to search official documentation
2. Keywords: `OpenClaw [Feature] documentation`
3. Prioritize searching docs.openclaw.ai

### Scenario 2: Specific Feature Implementation
**Characteristics**: User asks about specific feature implementation methods.

**Example Questions**:
- "How to set up OpenClaw cron jobs?"
- "How to create a new agent with OpenClaw?"
- "How to install skills with OpenClaw?"

**Processing Strategy**:
1. Directly use `openclaw [Feature] --help`
2. Search command reference manual
3. Provide specific command examples

### Scenario 3: Configuration Issues
**Characteristics**: User asks about configuration-related issues.

**Example Questions**:
- "How to configure models with OpenClaw?"
- "How to set OpenClaw log level?"
- "How to configure OpenClaw workspace?"

**Processing Strategy**:
1. Use `openclaw configure --help`
2. Search configuration documentation
3. Provide configuration examples

### Scenario 4: Troubleshooting
**Characteristics**: User encounters problems needing solutions.

**Example Questions**:
- "What should I do if OpenClaw fails to start?"
- "How to troubleshoot cron jobs not executing?"
- "How to handle unresponsive agents?"

**Processing Strategy**:
1. Use `openclaw doctor` for diagnostics
2. Search error messages
3. Check official issues and discussions

## MiniMax web_search Usage

### Basic Syntax
```bash
# Call via mcporter
mcporter call MiniMax.web_search query:"Search Keyword"

# Example: Search OpenClaw cron jobs
mcporter call MiniMax.web_search query:"OpenClaw cron job configuration"
```

### Search Templates

#### Template 1: Feature Search
```bash
# Search specific feature
mcporter call MiniMax.web_search query:"OpenClaw [Feature Name] tutorial"

# Examples
mcporter call MiniMax.web_search query:"OpenClaw agent management create delete"
mcporter call MiniMax.web_search query:"OpenClaw skills installation configuration"
```

#### Template 2: Problem Solution
```bash
# Search error solutions
mcporter call MiniMax.web_search query:"OpenClaw error [Error Message]"

# Examples
mcporter call MiniMax.web_search query:"OpenClaw startup failed permission denied"
mcporter call MiniMax.web_search query:"OpenClaw cron task not executing"
```

#### Template 3: Best Practices
```bash
# Search best practices
mcporter call MiniMax.web_search query:"OpenClaw [Feature] best practices"

# Examples
mcporter call MiniMax.web_search query:"OpenClaw agent configuration best practices"
mcporter call MiniMax.web_search query:"OpenClaw performance optimization tips"
```

### Search Parameter Optimization

#### Keyword Combination Strategy
```bash
# Basic combination
"OpenClaw" + [Feature] + [Action]

# Example combinations
"OpenClaw cron add schedule example"
"OpenClaw agents create model selection"
"OpenClaw skills install from github"
```

#### Time Filtering
```bash
# Search recent information (via keywords)
mcporter call MiniMax.web_search query:"OpenClaw 2026 new features"
mcporter call MiniMax.web_search query:"OpenClaw latest version v2.1"
```

#### Source Restriction
```bash
# Specify source (include in keywords)
mcporter call MiniMax.web_search query:"site:docs.openclaw.ai agents"
mcporter call MiniMax.web_search query:"OpenClaw GitHub issues"
mcporter call MiniMax.web_search query:"OpenClaw Discord discussion"
```

### Result Processing

#### Result Evaluation Criteria
1. **Authoritativeness**: Official docs > Community tutorials > Personal blogs
2. **Timeliness**: Recently updated > Historical docs
3. **Relevance**: Exact match > Partial match
4. **Completeness**: Complete tutorial > Fragmented information

#### Information Extraction Flow
```markdown
1. **Filter Results**:
   - Exclude ads, irrelevant content
   - Prioritize official documentation
   - Note publication dates

2. **Extract Key Information**:
   - Command syntax
   - Configuration examples
   - Important notes

3. **Verify Information**:
   - Cross-verify multiple sources
   - Test command validity
   - Check version compatibility
```

## Official Documentation Search

### Core Documentation Sites
1. **Main Docs**: https://docs.openclaw.ai
2. **GitHub**: https://github.com/openclaw/openclaw
3. **Discord**: https://discord.com/invite/clawd
4. **Blog**: https://blog.openclaw.ai

### Documentation Structure Navigation

#### docs.openclaw.ai Structure
```
/
├── /concepts/          # Core Concepts
│   ├── multi-agent     # Multi-Agent Systems
│   ├── tools          # Tool System
│   └── memory         # Memory System
├── /guides/           # User Guides
│   ├── getting-started # Getting Started
│   ├── configuration  # Configuration Guide
│   └── deployment     # Deployment Guide
├── /tools/           # Tool Documentation
│   ├── built-in      # Built-in Tools
│   └── custom        # Custom Tools
└── /api/            # API Documentation
```

#### Search Keyword Mapping
| User Question | Doc Path | Search Keyword |
|---------------|----------|----------------|
| "How do multi-agents work?" | /concepts/multi-agent | "multi-agent concepts" |
| "How to use tools?" | /tools/built-in | "built-in tools" |
| "How to configure models?" | /guides/configuration | "model configuration" |
| "How to deploy?" | /guides/deployment | "deployment guide" |

### Documentation Search Techniques

#### Direct URL Access
```bash
# Common doc links
- Concepts: https://docs.openclaw.ai/concepts/
- Guides: https://docs.openclaw.ai/guides/
- Tools: https://docs.openclaw.ai/tools/
- API: https://docs.openclaw.ai/api/
```

#### Site Search
```bash
# Use site search syntax
mcporter call MiniMax.web_search query:"site:docs.openclaw.ai agents create"

# Search specific section
mcporter call MiniMax.web_search query:"site:docs.openclaw.ai/concepts/multi-agent"
```

## CLI Command Search

### Help System Usage

#### Basic Help
```bash
# View all commands
openclaw help

# View command categories
openclaw --help

# View subcommands
openclaw agents --help
openclaw cron --help
openclaw skills --help
```

#### Detailed Help
```bash
# View command details
openclaw agents create --help
openclaw cron add --help
openclaw skills install --help

# View all options
openclaw agents create --help-all
```

#### Examples View
```bash
# View command examples
openclaw agents create --examples
openclaw cron add --examples
openclaw configure --examples
```

### Command Discovery Techniques

#### Command Completion
```bash
# Use Tab completion (if configured)
openclaw [TAB][TAB]

# View available subcommands
openclaw agents [TAB][TAB]
```

#### Command Search
```bash
# Search commands containing keyword
openclaw help | grep -i "agent"
openclaw help | grep -i "cron"
openclaw help | grep -i "skill"

# View command tree
openclaw --tree
```

#### Parameter Exploration
```bash
# View parameter descriptions
openclaw agents create --help | grep -A2 -B2 "model"

# View required parameters
openclaw cron add --help | grep "Required"
```

### Command Testing Flow

#### Safe Testing
```bash
# 1. First view help
openclaw [command] --help

# 2. Test with --dry-run
openclaw cron add --dry-run --name "test" --schedule "* * * * *" --command "echo test"

# 3. Use --verbose for details
openclaw agents create --verbose --name "test-agent" --model "gpt-3.5-turbo"

# 4. Execute actual command
openclaw [command] [parameters]
```

#### Error Handling Tests
```bash
# Test error scenarios
openclaw agents create --name ""  # Test empty name
openclaw cron add --schedule "invalid" --command "echo test"  # Test invalid schedule
openclaw skills install "nonexistent-skill"  # Test non-existent skill
```

## Knowledge Base Maintenance

### Knowledge Base Structure
```
memory/openclaw-knowledge/
├── commands/          # Command Documentation
│   ├── agents.md
│   ├── cron.md
│   ├── skills.md
│   └── gateway.md
├── configuration/     # Configuration Documentation
│   ├── basic.md
│   ├── advanced.md
│   └── examples.md
├── troubleshooting/   # Troubleshooting
│   ├── common-errors.md
│   ├── performance.md
│   └── recovery.md
├── best-practices/    # Best Practices
│   ├── agents.md
│   ├── cron.md
│   └── security.md
└── updates/          # Update Records
    ├── changelog.md
    ├── version-history.md
    └── migration-guides.md
```

### Information Collection Flow

#### Step 1: Identify Information Type
```markdown
1. **Command Info**: Syntax, parameters, examples
2. **Configuration Info**: Options, defaults, examples
3. **Best Practices**: Recommendations, notes, patterns
4. **Troubleshooting Info**: Errors, solutions, prevention
```

#### Step 2: Collect Information
```bash
# Collect from CLI
openclaw agents create --help > memory/openclaw-knowledge/commands/agents-create.md

# Collect from docs
mcporter call MiniMax.web_search query:"OpenClaw agents configuration" >> memory/openclaw-knowledge/configuration/agents.md

# Collect from practices
echo "## Experience Summary" >> memory/openclaw-knowledge/best-practices/agents.md
```

#### Step 3: Organize Information
```markdown
# Information Organization Template
## [Feature Name]

### Command Syntax
```bash
[Complete command]
```

### Parameter Description
| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| param1 | Yes | - | Parameter description |
| param2 | No | default | Parameter description |

### Usage Examples
```bash
# Example 1: Basic usage
[Command example]

# Example 2: Advanced usage
[Command example]
```

### Important Notes
- [Note 1]
- [Note 2]

### Related Links
- [Official doc link]
- [GitHub Issue link]
```

#### Step 4: Verify Information
```bash
# Test command
bash -c "[Collected command]"

# Check configuration
openclaw config validate --config memory/openclaw-knowledge/configuration/example.yaml

# Verify links
curl -I "[Doc link]"
```

### Knowledge Base Update Strategy

#### Regular Updates
```bash
# Weekly update command help
for cmd in agents cron skills gateway; do
  openclaw $cmd --help > memory/openclaw-knowledge/commands/$cmd.md
done

# Monthly search for latest info
mcporter call MiniMax.web_search query:"OpenClaw latest updates $(date +%Y-%m)" >> memory/openclaw-knowledge/updates/changelog.md
```

#### Trigger-based Updates
```bash
# When user asks about new features
if [ "$USER_QUESTION" = *"new feature"* ]; then
  mcporter call MiniMax.web_search query:"OpenClaw new features 2026" >> memory/openclaw-knowledge/updates/latest.md
fi

# When encountering errors
if [ $? -ne 0 ]; then
  echo "Error: $ERROR_MSG" >> memory/openclaw-knowledge/troubleshooting/errors.md
  mcporter call MiniMax.web_search query:"OpenClaw $ERROR_MSG solution" >> memory/openclaw-knowledge/troubleshooting/solutions.md
fi
```

#### Version Management
```bash
# Knowledge base version control
cd memory/openclaw-knowledge
git add .
git commit -m "Update OpenClaw knowledge base $(date +%Y-%m-%d)"
git tag -a "v$(date +%Y.%m.%d)" -m "Daily update"
```

## Search Optimization Tips

### Keyword Optimization

#### Extended Keywords
```bash
# Basic keyword
"OpenClaw agents"

# Extended keywords
"OpenClaw agents create configuration management delete list"
"OpenClaw multi-agent system architecture design"
"OpenClaw agent model selection performance optimization"
```

#### Exclude Irrelevant Terms
```bash
# Use minus to exclude
mcporter call MiniMax.web_search query:"OpenClaw -commercial -enterprise -price"

# Exclude specific types
mcporter call MiniMax.web_search query:"OpenClaw tutorial -video -youtube"
```

#### Synonym Search
```bash
# Use OR search
mcporter call MiniMax.web_search query:"OpenClaw (cron job OR scheduled task OR scheduler)"

# Multi-language search
mcporter call MiniMax.web_search query:"OpenClaw (configuration OR config OR setup)"
```

### Time Range Optimization

#### Search Latest Information
```bash
# Include year month
mcporter call MiniMax.web_search query:"OpenClaw 2026 March"

# Use time keywords
mcporter call MiniMax.web_search query:"OpenClaw latest update version"

# Search recent discussions
mcporter call MiniMax.web_search query:"OpenClaw recent issue discussion"
```

#### Search Historical Information
```bash
# Search specific version
mcporter call MiniMax.web_search query:"OpenClaw v2.0 docs"

# Search migration guides
mcporter call MiniMax.web_search query:"OpenClaw v1 to v2 migration"
```

### Source Quality Evaluation

#### Authoritative Source Scoring
```markdown
# Source scoring criteria (1-5 points)

## 5 points: Official Sources
- docs.openclaw.ai
- github.com/openclaw/openclaw
- Official blog and announcements

## 4 points: Community Recognized
- Stack Overflow highly-voted answers
- Reputable tech blogs
- Community-recommended tutorials

## 3 points: General Tutorials
- Personal tech blogs
- Video tutorials
- Non-official docs

## 2 points: Suspicious Sources
- Content farms
- Outdated information
- Machine-generated content

## 1 point: Spam Sources
- Ad pages
- Irrelevant content
- Malicious sites
```

#### Cross-Verification Strategy
```bash
# Verify command info
openclaw agents create --help | diff - memory/openclaw-knowledge/commands/agents-create.md

# Verify configuration info
openclaw config get system.log_level | grep -q "$EXPECTED_VALUE"

# Verify best practices
mcporter call MiniMax.web_search query:"OpenClaw $PRACTICE community feedback"
```

### Performance Optimization

#### Cache Search Results
```bash
# Create cache directory
mkdir -p ~/.openclaw/cache/search

# Cache search results
mcporter call MiniMax.web_search query:"OpenClaw agents" | tee ~/.openclaw/cache/search/agents-$(date +%Y%m%d).json

# Use cache
if [ -f ~/.openclaw/cache/search/agents-$(date +%Y%m%d).json ]; then
  cat ~/.openclaw/cache/search/agents-$(date +%Y%m%d).json
else
  mcporter call MiniMax.web_search query:"OpenClaw agents"
fi
```

#### Batch Search
```bash
# Batch search related topics
topics=("agents" "cron" "skills" "gateway")
for topic in "${topics[@]}"; do
  mcporter call MiniMax.web_search query:"OpenClaw $topic" >> memory/openclaw-knowledge/search-results/$topic-$(date +%Y%m%d).md
  sleep 2  # Avoid rate limiting
done
```

#### Result Deduplication
```bash
# Deduplicate search results
sort memory/openclaw-knowledge/search-results/*.md | uniq > memory/openclaw-knowledge/consolidated.md

# Extract unique links
grep -o 'http[s]*://[^"]*' memory/openclaw-knowledge/search-results/*.md | sort | uniq > memory/openclaw-knowledge/unique-links.md
```

---

**Last Updated**: 2026-03-28  
**Version**: 1.0  
**Maintainer**: OpenClaw HowTo Skill
