---
name: human-rent
description: Human-as-a-Service for OpenClaw - Dispatch verified human agents to perform physical world tasks and sensory validation
version: 0.2.1
homepage: https://docs.zhenrent.com
tags: [human-as-a-service, physical-verification, ai-agent, async-function-calling, hybrid-intelligence, human-in-the-loop]
metadata:
  clawdbot:
    requires:
      env:
        - ZHENRENT_API_KEY
        - ZHENRENT_API_SECRET
        - ZHENRENT_BASE_URL
      bins:
        - node
        - npm
    primaryEnv: ZHENRENT_API_KEY
    files:
      - "bin/*"
      - "lib/*"
---

# Human-Rent Skill

**Human-as-a-Service platform for AI Agents**

Enable OpenClaw agents to dispatch real human workers for physical world tasks that AI cannot perform: take photos, verify addresses, inspect equipment, make phone calls, and more.

## Core Concept

Transform AI agents from "digital-only" to "hybrid intelligence" by giving them the ability to interact with the physical world through verified human workers.

```
AI Agent → Human-Rent Skill → Human Worker → Physical Task → Verified Result → AI Agent
```

## Installation

The skill is self-contained and ready to use after installation:

```bash
clawhub install human-rent
```

### Configuration

Set up your ZhenRent API credentials:

```bash
export ZHENRENT_API_KEY="your-api-key-here"
export ZHENRENT_API_SECRET="your-api-secret-here"
```

Get your credentials at: https://www.zhenrent.com/api/keys

### Test Installation

```bash
human-rent test
```

## When to Use This Skill

Consider using this skill when the user's request involves:

- **Physical verification**: Check if an address exists, verify a business is open
- **Photo evidence**: Take a photo of something, get visual proof
- **Real-world inspection**: Inspect equipment, check product availability
- **Human interaction**: Make phone calls, ask questions in person
- **Trust verification**: Confirm something exists in the physical world

**Example Scenarios**:
- "I need someone to verify this address in San Francisco"
- "Take a photo of the building at 123 Main Street"
- "Check if this store has the product in stock"
- "Call this number and confirm the appointment"
- "Inspect this equipment and report its condition"

**Do NOT use when**:
- Task can be done with digital APIs (use web search, image API, etc.)
- No physical presence required
- Task is illegal or dangerous

## Important: User Confirmation Required

This skill ALWAYS requires explicit user confirmation before dispatching human workers because:

1. Real humans will be dispatched to physical locations
2. The user will be charged for the service ($15-100 per task)
3. Physical world actions have real consequences

The CLI will automatically prompt for confirmation. For non-interactive use, set:

```bash
export HUMAN_RENT_AUTO_CONFIRM=true  # Use with caution
```

## Usage

### Dispatch Human Task

When a user requests physical-world action, execute:

```bash
human-rent dispatch "instruction" [options]

# Example with location
human-rent dispatch "Take a photo of 123 Main St entrance" --location="37.7749,-122.4194"

# Example with budget
human-rent dispatch "Inspect warehouse condition" --budget="$50" --location="37.7749,-122.4194"
```

**Options**:
- `--location=<lat,lng>` - Location coordinates (e.g., "37.7749,-122.4194")
- `--budget=<amount>` - Budget in dollars (e.g., "$20" or "$15-25")
- `--priority=<level>` - Priority: low, normal, high, urgent
- `--timeout=<minutes>` - Task timeout in minutes (default: 30)
- `--type=<task_type>` - Task type (auto-detected if not specified)

### Check Task Status

```bash
human-rent status <task_id>

# Wait for completion
human-rent status <task_id> --wait
```

### List Available Humans

```bash
# List all available workers
human-rent humans

# Filter by location and radius
human-rent humans --location="37.7749,-122.4194" --radius=10000

# Search by skills
human-rent humans --skills="photography,legal_reading"
```

## Task Types

### Layer 1: Instant Human (Currently Available)

| Type | Description | Latency | Cost |
|------|-------------|---------|------|
| `photo_verification` | Take a photo of something | 5-15 min | $10-20 |
| `address_verification` | Verify physical address exists | 10-20 min | $15-25 |
| `document_scan` | Scan a physical document | 10-20 min | $15-25 |
| `visual_inspection` | Detailed visual inspection | 15-30 min | $20-40 |
| `voice_verification` | Make a phone call and verify | 5-10 min | $10-20 |
| `purchase_verification` | Check product availability | 15-30 min | $20-40 |

### Future Layers (Planned)

**Layer 2: Expert on Call**
- Legal document review
- Medical image analysis
- Code audit
- Professional consultation

**Layer 3: Embodied Agent**
- Attend meetings
- Equipment installation
- Long-term physical monitoring

## Technical Architecture

### Async Function Calling Pattern

Human tasks are asynchronous and take minutes to hours to complete. The workflow is:

1. Agent dispatches task (with user confirmation)
2. Task is assigned to a human worker
3. Agent receives task ID and continues other work
4. Agent periodically checks task status
5. When completed, agent processes results

```typescript
// Pseudo-code for agent integration
const task = await dispatch({
  instruction: "Take photo of building entrance",
  location: "37.7749,-122.4194"
});

// Returns immediately with task ID
console.log(task.task_id); // "abc-123-def"

// Agent continues other work (non-blocking)
await doOtherStuff();

// Later, check status
const result = await checkStatus(task.task_id);
if (result.status === "completed") {
  // Process human's result
  console.log(result.photos);
  console.log(result.notes);
}
```

### Authentication

All API requests use HMAC-SHA256 authentication:

1. Generate timestamp
2. Create message: `method + path + timestamp + body`
3. Sign with HMAC-SHA256 using API secret
4. Include signature in request headers

The CLI handles authentication automatically when you set the environment variables.

## Strategic Value

### 1. Capability Differentiation

**Problem**: All AI agents are limited to digital information  
**Solution**: OpenClaw can verify physical reality

**Example Use Cases**:
- Due diligence: Investor agent verifies company office exists before investment
- E-commerce: Purchasing agent inspects warehouse before bulk order
- Security: Safety agent verifies suspicious package before opening

### 2. Hybrid Intelligence Workflows

Enable "Human-in-the-Loop" automation:

```
Step 1: AI analysis (confidence: 85%)
Step 2: Human verification (if confidence < 90%)
Step 3: AI decision (based on verified data)
```

This makes OpenClaw agents auditable and trustworthy for regulated industries (finance, healthcare, legal).

### 3. New Revenue Model

- Per-task fee: $15-50/task
- Platform fee: 20% commission
- Subscription: $99/month for unlimited tasks

## Cost Estimation

| Task Type | Human Time | Human Cost | Platform Fee (20%) | Total Cost |
|-----------|-----------|-----------|-------------------|-----------|
| Quick photo | 10 min | $10 | $2 | $12 |
| Address verify | 20 min | $20 | $4 | $24 |
| Detailed inspect | 30 min | $30 | $6 | $36 |
| Expert consult | 60 min | $100 | $20 | $120 |

## Configuration Options

### Task Requirements

You can specify requirements when dispatching tasks:

```bash
human-rent dispatch "Inspect property condition" \
  --location="37.7749,-122.4194" \
  --budget="$50" \
  --type="visual_inspection"
```

For advanced requirements, use the API directly with:

```javascript
requirements: {
  minHumanRating: 4.5,
  requiredSkills: ['photography', 'legal_reading'],
  requiredEquipment: ['smartphone', 'tape_measure'],
  languageRequired: ['en', 'zh'],
  certificationRequired: ['driver_license']
}
```

## Usage Examples

### Example 1: Real Estate Investment

Scenario: AI agent analyzing potential property investment

```bash
# Agent requests physical inspection
human-rent dispatch \
  "Inspect the property at 123 Main St. Check for: roof condition, foundation cracks, water damage, neighborhood safety. Take 10+ photos." \
  --location="37.7749,-122.4194" \
  --budget="$50" \
  --timeout=60
```

### Example 2: Vendor Verification

Scenario: Procurement agent vetting new supplier

```bash
human-rent dispatch \
  "Visit supplier's warehouse at 456 Industrial Rd. Verify: business license displayed, clean facilities, proper safety equipment, actual inventory matches claim. Interview manager if possible." \
  --location="34.0522,-118.2437" \
  --budget="$40"
```

### Example 3: Address Verification

Scenario: Verifying customer shipping address

```bash
human-rent dispatch \
  "Go to 789 Oak Street and verify: building exists, address number is visible, location is accessible for delivery." \
  --location="40.7128,-74.0060" \
  --budget="$20"
```

## Troubleshooting

### Issue 1: No Humans Available

**Error**: "No suitable humans found for this task"

**Solutions**:
- Expand search radius (use `--radius` option)
- Increase budget to attract workers
- Try different time of day
- Check if location is accessible

### Issue 2: Task Timeout

**Error**: "Task timed out"

**Solutions**:
- Increase timeout (use `--timeout` option)
- Check if location is accessible
- Verify task is clear and reasonable
- Increase budget for complex tasks

### Issue 3: Authentication Error

**Error**: "Missing credentials" or "Authentication failed"

**Solutions**:
- Verify environment variables are set correctly
- Check API key is valid at https://www.zhenrent.com/api/keys
- Ensure API secret has not been compromised
- Try regenerating credentials

## Agent Behavior Guidelines

When using this skill, agents should:

**DO**:
- Use for tasks that REQUIRE physical presence
- Provide clear, specific instructions
- Set appropriate budgets (humans value their time)
- Handle async results (don't block waiting)
- Verify results before making decisions
- Respect human workers (polite instructions)

**DON'T**:
- Use for tasks that can be done digitally
- Request illegal or dangerous actions
- Expect instant results
- Underpay workers
- Share sensitive/private information unnecessarily
- Abuse the service with spam tasks

## Security & Privacy

### Data Security

- All API requests use HMAC-SHA256 authentication
- Credentials are never transmitted in plain text
- Task data is encrypted in transit (HTTPS)
- Results are stored securely and deleted after 30 days

### Privacy

- No PII collection without consent
- Workers cannot see requester identity
- Location data is anonymized after task completion
- Photo/document uploads are access-controlled

### Safety

- Dangerous tasks are rejected automatically
- Workers can decline tasks they deem unsafe
- Insurance coverage for worker injuries
- 24/7 safety hotline for workers

## Legal & Compliance

### Liability

Human workers assume responsibility for their actions (contractor model). The platform facilitates the connection but does not employ workers.

### Labor Law

Compliant with gig economy regulations in operating jurisdictions. Workers are independent contractors with full control over which tasks they accept.

### Geographic

Currently available in: United States (select cities)  
Expanding to: Canada, UK, EU (2026-2027)

## API Reference

### Command Line Interface

```bash
# Dispatch task
human-rent dispatch <instruction> [options]

# Check status
human-rent status <task_id> [--wait]

# List workers
human-rent humans [--location=<lat,lng>] [--radius=<meters>] [--skills=<skill1,skill2>]

# Test connection
human-rent test

# Show help
human-rent help
```

### Environment Variables

**Required**:
- `ZHENRENT_API_KEY` - Your API key
- `ZHENRENT_API_SECRET` - Your API secret

**Optional**:
- `ZHENRENT_BASE_URL` - API base URL (default: https://www.zhenrent.com/api/v1)
- `HUMAN_RENT_AUTO_CONFIRM` - Auto-confirm dispatches (default: false)

## Version History

### v0.2.0 - Security Refactor (2026-03-31)

- Self-contained package (no external git clone required)
- User confirmation prompts before every dispatch
- Integrity verification with checksums
- Proper credential declaration in _meta.json
- Real ZhenRent API integration
- Removed all unicode control characters
- Removed auto-trigger language
- Enhanced error handling and user feedback

### v0.1.0 - MVP Release (2026-03-07)

- Initial release with mock data
- Async task dispatch system
- Mock human pool (5 workers in SF)
- 6 task types supported
- CLI tools
- MCP protocol interface

## Project Status

**Status**: Production Beta  
**License**: MIT  
**Author**: @ZhenStaff  
**Support**: https://github.com/ZhenRobotics/openclaw-human-rent/issues  
**ClawHub**: https://clawhub.ai/zhenstaff/human-rent

## Quick Start

```bash
# 1. Install
clawhub install human-rent

# 2. Configure credentials
export ZHENRENT_API_KEY="your-key"
export ZHENRENT_API_SECRET="your-secret"

# 3. Test
human-rent test

# 4. Dispatch real task
human-rent dispatch "Take a photo of the Golden Gate Bridge" \
  --location="37.8199,-122.4783"

# 5. Check status
human-rent status <task_id>

# 6. List humans
human-rent humans
```

Make AI agents that can touch the physical world.
