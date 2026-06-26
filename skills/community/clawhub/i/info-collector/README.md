# Real-time Information Gathering Assistant (Info Collector)

A professional real-time information gathering skill module, adept at quickly aggregating the latest information on specific topics from multiple public sources and providing structured output.

## Function Overview

This skill module can:

- 🔍 **Multi-source Information Retrieval** - Retrieve information from RSS, news websites, social media, code repositories, forums, etc.

- ✅ **Authenticity Verification** - Perform multi-dimensional authenticity verification and cross-validation on all information.

- 🧹 **Intelligent Deduplication and Merging** - Deduplicate and merge multiple reports of the same event.

- 📊 **Structured Classification** - Classify information into seven categories, including official updates, media reports, and community discussions.

- 🎯 **Priority Sorting** - Sort information based on timeliness, credibility, relevance, and other dimensions.

- 📄 **Report Generation** - Output structured reports with a unified format and complete content.

## Core Capabilities

### 1. Multi-source Information Retrieval
Covering the following channels (in order of priority):

- **Official Channels** - Official website, official blog, official GitHub repository, verified account

- **Authoritative Media** - Tech media, industry media, mainstream news websites

**Developer Ecosystem** - GitHub Releases/Issues/PRs, technical forums

**Social Media Platforms** - X/Twitter, Weibo, WeChat Official Accounts

**Community Discussions** - Reddit, Hacker News, V2EX, Tieba, etc.

**Search Engines** - Comprehensive search supplement

### 2. Authenticity Verification
Each piece of information must pass the following checks:

- ✓ A clearly accessible original link exists

- ✓ An identifiable publication timestamp exists

- ✓ Traceable source (official/verified account/authoritative media)

- ✓ Content can be independently cross-verified

- ✓ Not an obvious advertisement or unverified leak

### 3. Categorization System

- **Official Updates** - Official announcements, updates, releases

**Media Reports** - In-depth reports, analysis, news

**Community Discussions** - Technical forums, hot posts, discussions

**Social Media Hot Topics** - Key topics on social media platforms

**Developer Ecosystem** - Release, Issue, PR, Documentation

- **In-depth Analysis** - Analysis, Opinions, Research Reports

- **Market Signals** - Funding, Cooperation, Product Dynamics

## Usage

### Basic Calls

```python

# Standard Collection Commands
Please perform real-time information collection around the topic "{topic}":

- Time Window: 48 hours (default)

- Language: zh-CN (default)

- Maximum per Category: 8 entries (default)

- Strict Time Limit: true (default)

```

### Input Parameters

| Parameter | Type | Default Value | Description |

|------|------|--------|------|

| `topic` | string | Required | The topic to collect (product name, technology name, event name, etc.) |

| `time_window_hours` | int | 48 | Time window (unit: hours) |

| `language` | string | zh-CN | Output Language (zh-CN/en-US) |

| `regions` | list | [] | Region Preference |

| `must_include_sources` | list | [] | Must-include channels |

| `exclude_sources` | list | [] | Excluded channels |

| `max_items_per_category` | int | 8 | Maximum number of items per category |

| `strict_recency` | bool | true | Whether to strictly limit the time window |

## Execution Flow

1. **Topic Parsing** - Extract keywords, synonyms, and abbreviations to generate Chinese and English search combinations

2. **Parallel Search** - Retrieve information from multiple channels simultaneously

3. **Authenticity Verification** - Verify the reliability of each piece of information

4. **Duplicate Removal and Merging** - Identify and merge duplicate information

5. **Categorization and Organization** - Categorize each piece of information into seven categories

6. **Priority Sorting** - Sort by timeliness, credibility, and relevance

7. **Report Generation** - Output Structured Report

## Output Example

```markdown

# AI Agent Information Collection Report

- **Retrieval Time**: 2026-04-10 16:00

- **Channels Covered**: GitHub / X / Tech Media / Developer Forums

- **Total Information**: 23 items

## I. Official Updates

### 1. Product Release

- **Source**: [Official Blog](https://example.com)

- **Release Time**: 2026-04-09 10:00

- **Summary**: Core feature updates...

## II. Media Reports

...
## Core Findings Summary

1. **Most Important**: {Key Findings}

2. **Official Updates**: {Major Official Actions}

3. **Market Reaction**: {Media/Community Opinions}

4. **Technological Progress**: {Developer Ecosystem Updates}

5. **Risk Warnings**: {Issues Requiring Attention}

```

## Recommended Use Cases

- 🎯 **Technology Tracking** - Track the latest developments of a technology or framework

- 🏢 **Competitor Monitoring** - Monitor competitors' activities

- 📊 **Public Opinion Analysis** - Analyze public opinion on a specific topic

- 🔬 **Industry Research** - Study the development trends of an industry

- 📰 **Hot Topic Tracking** - Quickly grasp industry hot topics

## Usage Suggestions

1. **Define the Topic** - Provide the specific product name, technology name, or event name

2. **Reasonable Time Window**

- 48 hours - Suitable for hot topic tracking

- 7 days - Suitable for trend observation

- 30 days - Suitable for long-term monitoring

3. **Specify Channels** - If you need to cover specific channels, you can specify them.

4. **Feedback and Correction** - Adjust parameters and re-search when information is missing or biased.

5. **Manual Review** - Manually review the key information sources for important decision-making suggestions.

## Limitations

This module has the following limitations:

- ❌ Unable to access content requiring login or payment

- ❌ Unable to crawl private/non-public social media content

- ❌ Some deleted or inaccessible content cannot be retrieved

- ❌ Real-time updates are limited by search frequency

- ⚠️ Some channels, such as WeChat, may be missing due to access restrictions

- ⚠️ Time judgment for some cross-timezone content may be inaccurate

## Quality Assurance

- Quality over coverage

- Only information from verifiable sources is retained

- Content without a definite publication time is downgraded

- Unverified leaks are marked "Unverified"

- Summaries are faithful to the original text, without exaggeration or fabrication

## Version Information

- **Version**: v1.0

- **Update Date**: 2026-04-10

- **Applicable Scenarios**: Technology tracking, competitor monitoring, public opinion analysis, industry research

## License

MIT
