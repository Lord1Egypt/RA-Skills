# kindle-clip Usage Examples

This file contains practical examples for AI agents using the kindle-clip skill.

## Example 1: List All Books

**User Request**: "Show me all the books I've highlighted on my Kindle"

**AI Agent Command**:
```bash
kindle-clip list ~/Documents/Kindle --verbose
```

**Expected Output**:
```markdown
# Books

- **Sapiens (Yuval Noah Harari)**
  - clips: 42
  - first: 2024-01-15T10:30:00Z
  - last: 2024-02-20T14:22:00Z
- **Thinking, Fast and Slow (Daniel Kahneman)**
  - clips: 67
  - first: 2024-03-01T09:15:00Z
  - last: 2024-03-28T18:45:00Z
```

## Example 2: Export Highlights from a Specific Book

**User Request**: "Export all my highlights from Sapiens to a markdown file"

**AI Agent Command**:
```bash
kindle-clip print --book "Sapiens" --export-md ./sapiens-highlights.md
```

**Expected Output to Console**:
```markdown
# Output saved

- file: `./sapiens-highlights.md`
```

**Content of sapiens-highlights.md**:
```markdown
# Sapiens (Yuval Noah Harari)

> Culture tends to argue that it forbids only that which is unnatural. But from a biological perspective, nothing is unnatural. Whatever is possible is by definition also natural.

> **Note**: This connects to the social construction argument in sociology.

> The real difference between us and chimpanzees is the mysterious glue that enables millions of humans to cooperate effectively.
```

## Example 3: Search for a Specific Topic

**User Request**: "Find all my highlights about cognitive biases"

**AI Agent Command**:
```bash
kindle-clip search "cognitive bias" --export-md ./cognitive-bias-research.md
```

**Expected Output**:
```markdown
# Thinking, Fast and Slow (Daniel Kahneman)

> The confidence that individuals have in their beliefs depends mostly on the quality of the story they can tell about what they see, even if they see little.

> **Note**: Confirmation bias example

> We are prone to overestimate how much we understand about the world and to underestimate the role of chance in events.

# Predictably Irrational (Dan Ariely)

> Once we buy a new product at a particular price, we become anchored to that price.
```

## Example 4: Filter by Author and Date Range

**User Request**: "Show me highlights from books by Daniel Kahneman that I made in 2024"

**AI Agent Command**:
```bash
kindle-clip print --author "Kahneman" --from 2024-01-01 --to 2024-12-31 --export-md ./kahneman-2024.md
```

## Example 5: Quick Search Without Path

**User Request**: "Search for mentions of 'metacognition' in my kindle notes"

**AI Agent Setup** (first time):
```bash
# Set default path once
kindle-clip set ~/Documents/Kindle
```

**AI Agent Command**:
```bash
# Now can use without specifying path
kindle-clip search metacognition --verbose
```

**Expected Output**:
```markdown
# Thinking, Fast and Slow (Daniel Kahneman)

> Metacognition: thinking about thinking

> *- Your Highlight on page 45 | Added on Monday, March 4, 2024 2:30:00 PM*
```

## Example 6: Combine Multiple Filters

**User Request**: "Find all highlights about 'decision making' from books by Daniel Kahneman after January 2024"

**AI Agent Command**:
```bash
kindle-clip search "decision making" --author "Kahneman" --from 2024-01-01 --export-md ./decision-making-kahneman.md
```

## Example 7: Get Book List for a Specific Author

**User Request**: "What books by Yuval Noah Harari have I read?"

**AI Agent Command**:
```bash
kindle-clip list --author "Harari" --verbose
```

**Expected Output**:
```markdown
# Books

- **Sapiens (Yuval Noah Harari)**
  - clips: 42
  - first: 2024-01-15T10:30:00Z
  - last: 2024-02-20T14:22:00Z
- **Homo Deus (Yuval Noah Harari)**
  - clips: 28
  - first: 2024-04-01T11:00:00Z
  - last: 2024-04-15T16:30:00Z
```

## Example 8: Reading Timeline Analysis

**User Request**: "What was I reading in Q1 2024?"

**AI Agent Command**:
```bash
kindle-clip list --from 2024-01-01 --to 2024-03-31 --verbose
```

## Tips for AI Agents

1. **Save path early**: When starting a session, use `kindle-clip set <path>` so subsequent commands don't need the path
2. **Use --export-md for long outputs**: When the output might be large, always export to a file
3. **Combine filters strategically**: Multiple filters can narrow down results precisely
4. **Case doesn't matter**: All text filters are case-insensitive
5. **Partial matches work**: `--book "Think"` will match "Thinking, Fast and Slow"
6. **Use --verbose when context matters**: Includes metadata like page numbers and timestamps

## Common Error Scenarios

### Error: Binary not installed

```
Error: exec: "kindle-clip": executable file not found in $PATH
```

**AI Agent Response**: "The kindle-clip tool is not installed. Let me help you install it..."

### Error: No path configured

```
Error: no clippings path provided; use `kindle-clip set <path>` or KINDLE_CLIP_PATH
```

**AI Agent Response**: "I need to know where your Kindle clippings file is located. Please tell me the path to your Kindle device or the My Clippings.txt file."

### Error: Invalid date format

```
Error: invalid date "2024-1-1", expected YYYY-MM-DD
```

**AI Agent Response**: Retry with correct date format (2024-01-01)

## Integration Patterns

### Pattern 1: Initial Setup

```bash
# First interaction with user
kindle-clip set ~/Documents/Kindle
kindle-clip list --verbose
```

### Pattern 2: Research Workflow

```bash
# User exploring a topic across books
kindle-clip search "topic" --export-md ./topic-research.md
# Review results
# If needed, narrow down
kindle-clip search "topic" --author "specific author" --export-md ./topic-author.md
```

### Pattern 3: Book Review

```bash
# User wants to review a specific book
kindle-clip print --book "Book Title" --verbose --export-md ./book-review.md
```

### Pattern 4: Periodic Summary

```bash
# User wants to see reading activity for a period
kindle-clip list --from 2024-01-01 --to 2024-03-31 --verbose --export-md ./q1-2024-reading.md
```
