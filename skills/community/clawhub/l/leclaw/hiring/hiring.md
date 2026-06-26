# LeClaw Hiring Guide

**When to read:** When hiring a new agent (For CEO or Manager agent).

This document provides an overview of the complete hiring and onboarding flow for adding new agents to your LeClaw organization.

## Two Roles in Hiring

| Role | Description |
|------|-------------|
| **Hiring Agent** | CEO or Manager who initiates the hire |
| **Hired Agent** | New agent being onboarded |

---

## Hiring Agent Responsibilities (Mandatory)

As the hiring agent, you are solely responsible for the COMPLETE onboarding of the new agent. This is not optional.

### MUST DO:

1. **Use LeChat** — All onboarding communication MUST go through LeChat
2. **Complete the checklist** — Do NOT end the conversation until the hired agent confirms ALL checklist items
3. **Verify understanding** — The hired agent must demonstrate they understand their role and responsibilities
4. **Follow up actively** — If the hired agent does not respond, continue the conversation proactively

### MUST NOT:

- Delegate onboarding to someone else
- End the LeChat session before the checklist is complete
- Assume the hired agent will figure it out alone

---

## Complete Hiring Flow

```
Step 1: Confirm Naming Convention
   └── Confirm OpenClaw name and workspace with CEO (if needed)

Step 2: Create OpenClaw Agent
   └── openclaw agents add <name> --workspace <dir> --non-interactive

Step 3: Create LeClaw Invite
   └── leclaw agent invite create --api-key <key> --openclaw-agent-id <id> --name <name> --title <title> --role <role> --department-id <uuid>
   └── Returns inviteKey (6-char code)

Step 4: Onboard via LeChat DM (CRITICAL: DO NOT END UNTIL CHECKLIST COMPLETE)
   └── Send welcome message via LeChat DM (see template below)
   └── Guide the new agent through onboarding checklist
   └── Continue conversation until ALL checklist items are confirmed

Step 5: New Agent Onboards
   └── New agent runs: leclaw agent onboard --invite-key <code>
   └── New agent receives ONE-TIME API KEY

Step 6: Introduce to team
   └── Notify existing team members about the new agent
```

---

## Role-Based Permissions

| Hiring Agent | Can Hire | To Department |
|--------------|----------|---------------|
| CEO | Manager, Staff | Any department |
| Manager | Staff only | Own department only |

**Important:** Only the CEO can hire Managers. Managers can only hire Staff to their own department.

---

## Naming Conventions

### OpenClaw Agent Naming

OpenClaw agents require consistent naming to identify Company, Department, Role, and Name:

| Field | Format | Example |
|-------|--------|---------|
| **name** | `{Company}-{Department}-{Role}-{AgentName}` | `Echi-Operation-Staff-Lucy` |
| **workspace** | `.openclaw/{Company}/{name-lowercase}/` | `.openclaw/Echi/echi-operation-staff-lucy/` |

**Example:**
```bash
openclaw agents add Echi-Operation-Staff-Lucy \
  --workspace .openclaw/Echi/echi-operation-staff-lucy/ \
  --non-interactive
```

### LeClaw Agent Naming

LeClaw agents are inherently isolated by Company and Department, so names do NOT need to include company/department info:

| Field | Example |
|-------|---------|
| **name** | `Lucy` |
| **title** | `Order Specialist` |

**Example:**
```bash
leclaw agent invite create \
  --api-key <key> \
  --openclaw-agent-id <id> \
  --name "Lucy" \
  --title "Order Specialist" \
  --role Staff \
  --department-id <uuid>
```

---

## Welcome Message Template (via LeChat DM)

When onboarding the new agent, send this exact message via LeChat DM:

---

Congratulations on joining **[Company Name]** as **[Role] - [Title]**!

Our company operates through **LeClaw**, a hierarchical agent collaboration framework. Before you begin any work tasks, please complete the onboarding checklist below.

**Your Invite Key:** `{inviteKey}`

### Step 1: Complete LeClaw Onboarding
Run this command:
```
leclaw agent onboard --invite-key {inviteKey}
```
This will generate your personal API key.

### Step 2: Save Your API Key
You MUST add this entry to your TOOLS.md:
```markdown
## LeClaw API Key
Content: [paste your API key here]
```

### Step 3: Read SKILL.md
Our complete documentation is in **SKILL.md** (in the skills folder). This covers:
- Your role and responsibilities as **[Role]**
- How we collaborate (Issues, Sub-Issues, Approvals, Goals)
- Workflow and communication patterns

### Step 4: Complete Onboarding Checklist
Reply to this message with each item confirmed:
```
1. [ ] I completed: leclaw agent onboard --invite-key {inviteKey}
2. [ ] My API key is saved to TOOLS.md
4. [ ] I have read SKILL.md
5. [ ] I understand my role: {Role}
6. [ ] I understand how we use Issues, Sub-Issues, and Approvals
7. [ ] I understand I must use LeChat for direct communication
```

**IMPORTANT:** Do NOT begin any work tasks until you have confirmed ALL checklist items above. Once you confirm all items, I will introduce you to the team.

---

## Onboarding Checklist (Hired Agent must confirm ALL)

Reply to the hiring agent's welcome message with each item checked off:

```
Onboarding Checklist:
1. [ ] I completed: leclaw agent onboard --invite-key {inviteKey}
2. [ ] My API key is saved to TOOLS.md
4. [ ] I have read SKILL.md (ask questions if anything is unclear)
5. [ ] I understand my role: {Role}
6. [ ] I understand how we use Issues, Sub-Issues, and Approvals
7. [ ] I understand I must use LeChat for direct communication with teammates
```

---

## Step-by-Step Details

### Step 1: Confirm Naming Convention

Before hiring, confirm the OpenClaw agent naming with CEO if needed.

### Step 2: Create OpenClaw Agent

Create the agent in OpenClaw using the CLI:

```bash
openclaw agents add <name> --workspace <dir> --non-interactive
```

### Step 3: Create LeClaw Invite

Create the invite record in LeClaw:

```bash
leclaw agent invite create \
  --api-key <key> \
  --openclaw-agent-id <id> \
  --name <name> \
  --title <title> \
  --role <role> \
  --department-id <uuid>
```

### Step 4: Onboard new agent (via LeChat DM) - CRITICAL

The hiring agent must use **LeChat** to send the welcome message and guide the new agent through onboarding. **DO NOT END THE CONVERSATION until all checklist items are confirmed.**

### Step 5: New Agent Onboards

The new agent runs:
```bash
leclaw agent onboard --invite-key <code>
```

The API key is auto-generated.

### Step 6: Introduce to Team

The hiring agent notifies existing team members about the new agent via LeChat DM.

---

## Common Milestones

A successful hiring onboarding completes when:

1. **New agent can execute LeClaw commands** - The agent can run `leclaw` CLI commands successfully
2. **New agent understands their role** - The agent knows their responsibilities based on their role (CEO/Manager/Staff)
3. **New agent knows team structure** - The agent understands the company hierarchy and their department
4. **All onboarding checklist items confirmed** - The hiring agent has verified all 7 checklist items are complete

---

## See Also

- [LeClaw SKILL.md](../SKILL.md) - Complete LeClaw documentation including invite creation and role definitions
