# Inter-Agent Communication via Email

## Overview

This guide covers how to enable autonomous agent-to-agent communication using email and Himalaya, the CLI email client integrated with OpenClaw.

**Normative task envelope:** For a channel-agnostic JSON wrapper (HOLA + task payload + routing hints), use MCP `doc:reference:collaboration-envelope` or [`collaboration-envelope.md`](collaboration-envelope.md).

---

## Why Email for Inter-Agent Communication?

Email is the most pragmatic option for unrelated agents because:
- ✅ **Universal** - Everyone has it, no special setup required
- ✅ **No pre-arrangement** - Just need an email address
- ✅ **Immediate delivery** - Works across organizations and owners
- ✅ **No platform limitations** - Not restricted by API access or tokens
- ✅ **Attachment support** - Native file transfer capability
- ✅ **Autonomous** - Agents can send/receive without human intervention

---

## Himalaya: Email for AI Agents

### What is Himalaya?

Himalaya is a standalone CLI email client (like mutt/neomutt but modern and Rust-based).

**Key Features:**
- CLI-first (terminal-based)
- Supports IMAP (reading) and SMTP (sending)
- Handles attachments, multiple accounts, folders
- Written in Rust, fast and lightweight
- Completely separate from OpenClaw - works without it

### Installation
```bash
brew install himalaya
himalaya account configure
```

### Architecture

```
┌─────────────────────────────────────┐
│     OpenClaw Agent (You/Me)         │
└──────────┬──────────────────────────┘
           │
           │ 1. "Send email to X"
           ▼
┌─────────────────────────────────────┐
│  OpenClaw Himalaya Skill            │
│  (skills/himalaya/SKILL.md)         │
└──────────┬──────────────────────────┘
           │
           │ 2. himalaya message write ...
           ▼
┌─────────────────────────────────────┐
│     Himalaya CLI (Standalone)       │
│     /usr/local/bin/himalaya         │
└──────────┬──────────────────────────┘
           │
           │ 3. SMTP protocol
           ▼
┌─────────────────────────────────────┐
│      Email Server                   │
│     (Gmail, Outlook, etc.)          │
└─────────────────────────────────────┘
```

### Relationship to OpenClaw

| Layer | Example | Purpose |
|-------|---------|---------|
| Tool | himalaya | Does actual work (email processing) |
| OpenClaw Skill | himalaya skill | Wraps himalaya for AI to use |
| AI Agent | Me/You | Uses skill to accomplish tasks |

**Benefits of Separation:**
- ✅ Himalaya is standalone - Use it without OpenClaw, test manually
- ✅ Battle-tested - Thousands of users, bugs fixed, stable
- ✅ OpenClaw doesn't reinvent wheel - Uses proven email client
- ✅ Skill is thin - Just CLI wrapper, minimal complexity
- ✅ Updates independently - Himalaya improves without OpenClaw changes

---

## Email Communication Patterns

### Basic Agent-to-Agent via Email

```bash
# Agent A sends task to Agent B
himalaya message write \
  -H "To:agent-b@example.com" \
  -H "Subject:TASK_REQUEST" \
  'Delegated task: Analyze market data'

# Agent B checks inbox and processes
himalaya envelope list --folder INBOX
himalaya message read <id>

# Agent B replies with result
himalaya message reply <id> \
  'Here is the analysis result: {...}'
```

### Email + HOLA Signature Pattern

Combine email transport with IdentyClaw verification for security:

```javascript
// Agent-to-Email pattern with verification
async function delegateTaskViaEmail(recipientEmail, task) {
  // 1. Create task with verification
  const message = {
    type: "TASK_REQUEST",
    task: task,
    timestamp: Date.now(),
    signature: sign(task, privateKey) // HOLA-style
  };

  // 2. Send via Himalaya
  await himalaya.send({
    to: recipientEmail,
    subject: `TASK:${task.id}`,
    body: JSON.stringify(message)
  });

  // 3. Poll for reply
  const response = await himalaya.poll({
    folder: "INBOX",
    filter: `subject:"RESULT:${task.id}"` 
  });

  // 4. Verify and process
  if (verify(response.signature, response.content)) {
    return response.content;
  }
}
```

### Message Format with Verification

```
Subject: TASK_REQUEST:12345

Body:
{
  "type": "TASK_REQUEST",
  "task": {...},
  "timestamp": 1715443200000,
  "HOLA_SIGNATURE": "ed25519_signature_here"
}
```

### Checking Incoming Tasks

```javascript
// Agent checking email for delegated tasks
async function checkIncomingTasks() {
  const result = await exec({
    command: "himalaya envelope list --folder INBOX"
  });

  const emails = parseHimalayaOutput(result);

  for (const email of emails) {
    if (email.subject.startsWith("TASK_REQUEST:")) {
      const task = parseTask(email.body);
      
      // Verify HOLA signature
      if (verifySignature(task)) {
        const result = await processTask(task);
        
        // Reply via Himalaya
        await exec({
          command: "himalaya message reply " + email.id,
          input: JSON.stringify(result)
        });
      }
    }
  }
}
```

---

## Subject Tag Conventions

For email-based communication, use these subject prefixes:

- `TASK_REQUEST:` - Delegating a task
- `TASK_RESULT:` - Returning task results
- `AGENT_DISCOVERY:` - Agent capability announcement
- `TASK_STATUS:` - Status update on ongoing task
- `TASK_ERROR:` - Error notification

---

## Security Considerations

### Email Transport
- SPF/DKIM provides weak verification
- Add HOLA signatures for cryptographic verification
- Validate timestamps to prevent replay attacks
- Use subject filtering to prevent spam

### Verification Layer
```javascript
// Always verify before processing
function processIncomingTask(email) {
  const task = JSON.parse(email.body);
  
  // Check timestamp (prevent replay)
  if (Date.now() - task.timestamp > 300000) { // 5 min
    throw new Error("Task expired");
  }
  
  // Verify signature
  if (!verify(task.signature, task.content, task.publicKey)) {
    throw new Error("Invalid signature");
  }
  
  // Process task
  return executeTask(task);
}
```

---

## OpenClaw Email vs Gmail Web Interface

| Feature | Gmail Web | OpenClaw + Himalaya |
|---------|-----------|---------------------|
| Access | Human only | AI agents |
| Automation | Manual triggers | Cron jobs, heartbeat checks |
| Integration | Copy-paste | Direct in workflows |
| Attachment handling | Download manually | Parse programmatically |
| Bulk processing | Slow (click each) | Script/iterate instantly |
| Agent-to-agent | Requires human | Fully autonomous |

---

## Summary

**Email + HOLA Signatures = Universal Agent Communication**

**Himalaya's Role:**
- **The engine** - Rust CLI email client (standalone tool)
- **OpenClaw skill** - Wrapper that lets AI agents control Himalaya
- **Together** - Agents can send/receive emails autonomously

**Communication Pattern:**
1. Send tasks via email (universal transport)
2. Sign with Ed25519 (cryptographic trust)
3. Verify signature before accepting (security)
4. Use subject tags for routing (organization)

**Key Benefits:**
- ✅ No pre-arrangement needed between agents
- ✅ Works across different owners and organizations
- ✅ Battle-tested email infrastructure
- ✅ Cryptographic verification via HOLA
- ✅ No complex P2P setup required
