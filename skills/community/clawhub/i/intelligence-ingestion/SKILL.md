---
name: Intelligence Ingestion
version: 2.0.0
description: >
  Analyze and evaluate URLs, links, articles, tweets, and external info sources for strategic
  value. NOT a summarizer — this skill classifies, scores importance, maps to architecture,
  stores structured notes in Obsidian, updates the Strategic Landscape, and auto-generates
  draft Skills when new capabilities are detected (Auto-Skill Synthesis).
  Use when: user shares a link (x.com, github.com, arxiv.org, any URL), pastes article text,
  says "analyze this", "evaluate this", "what do you think about this", or forwards content.
  Do NOT use for: simple summarization requests (use summarize skill instead).
---

# Intelligence Ingestion Skill

> *You are feeding something smarter than you.*
> *This Skill ensures you know exactly what it ate and what it became.*

**MCP Compatible:** This Skill ships with a `manifest.json` that follows the MCP capability declaration spec, making it discoverable and invokable by any MCP-compatible Agent workflow.

---

## Design Philosophy

> *"giving my private data/keys to 400K lines of vibe coded monster is not very appealing at all"* — Andrej Karpathy

This Skill embraces a trust-first design philosophy:

1. **No Self-Modifying Agents.** Auto-generated Skills are isolated as drafts. You, the human operator, must review and approve them before they activate.
2. **Skills are the new Config.** No need to modify configuration files or monster if-else scripts. A single Skill file defines a capability.
3. **Build. For. Agents.** Built with an MCP manifest, structured outputs, and CLI installation so that any Agent in the ecosystem can find, understand, and use it.

## Permissions & Privacy

**This Skill writes files to your local filesystem and may access sensitive browser state.** Full transparency on what it touches:

| Permission | What | Why |
|------------|------|-----|
| **File Write** | `{obsidian_vault}/{intelligence_folder}/` | Creates structured intelligence notes |
| **File Write** | `{workspace}/STRATEGIC_LANDSCAPE.md` | Updates capability map when critical info is ingested |
| **File Write** | `{workspace}/skills/_drafts/` | Creates auto-synthesized Skill drafts (isolated, never auto-loaded) |
| **File Write** | `{workspace}/memory/` | Appends to daily memory logs |
| **File Create** | `STRATEGIC_LANDSCAPE.md` | Auto-creates from template if missing on first run |
| **File Read** | `{workspace}/skills/` | Reads existing Skills for gap analysis during synthesis |
| **Network** | User-provided URLs | Fetches content via HTTP; may fall back to search if primary fetch fails |
| **Credential** | xurl X API auth (Optional) | Used for authenticated X/Twitter API v2 access via the xurl Skill |

> **Privacy Note:** The "never return empty-handed" fallback policy means the Skill may make multiple external network requests per ingestion (direct fetch → xurl → web search). All fetched content is stored locally in your Obsidian vault; no data is transmitted to third-party servers beyond the original fetch.

## Prerequisites

| Tool | Purpose | Required? |
|------|---------|-----------|
| **Obsidian** | Knowledge storage (notes land here) | ✅ Required |
| **OpenClaw** | Skill host + Agent orchestration | ✅ Required |

## Configuration

Edit `config.json` after installation:

```json
{
  "obsidian_vault_path": "/path/to/your/Obsidian_Vault",
  "intelligence_folder": "20_Intelligence",
  "landscape_path": "STRATEGIC_LANDSCAPE.md",
  "output_dir": "/path/to/your/output"
}
```

| Field | Description | Default |
|-------|-------------|---------|
| `obsidian_vault_path` | Absolute path to Obsidian Vault root | None (Required) |
| `intelligence_folder` | Subfolder for intelligence notes | `20_Intelligence` |
| `landscape_path` | Strategic Landscape file path (relative to workspace) | `STRATEGIC_LANDSCAPE.md` |
| `output_dir` | Directory for non-knowledge outputs | None (Optional) |

> **Storage Strategy: Obsidian = Knowledge Inputs (Analysis/Notes), Output = Content Generation (Posts/Scripts)**

### First-time Setup

If `STRATEGIC_LANDSCAPE.md` does not exist, the Skill will automatically generate an empty template.
If the Obsidian Vault path does not exist or `config.json` is missing, the Skill will error and provide remediation steps.

---

## Triggers

**Auto-triggers on:**
- User sharing a URL (x.com, github.com, arxiv.org, etc.)
- User pasting an article/tweet block
- User prompts like "analyze this", "evaluate this", "what do you think about this"
- User forwarding content from Telegram or any chat interface

**Does not trigger on:**
- General questions unrelated to external knowledge
- Explicit commands to simply summarize
- E-commerce, music, or entertainment links

---

## Content Extraction Strategy (Critical)

Different sources require different extraction methods. The Agent must run down this priority chain:

### Standard Web Pages
```
1. read_url_content(url) → If successful, use it
2. Fallback → Direct user to paste content
```

### X/Twitter (Aggressive Anti-Scraping)
X strictly prevents unauthenticated scraping. Use this degradation chain:

```
1. xurl Skill (Recommended) → Native OpenClaw skill using X API v2
   - Most reliable method
   - Requires xurl authentication
2. Fallback → Web search the tweet text (often indexed by search engines)
3. Fallback → Ask user to paste the raw text
```

> **Principle: Never return empty-handed.** Even if extraction fails, inform the user exactly which step failed, why, and how to fix it.

### GitHub
```
1. read_url_content(url) → Usually accessible
2. If repo root → Target README.md
3. If issue/PR → Target title, description, and primary comments
```

### Paywalls / Login Walls
```
1. Mark as unreachable and analyze based solely on user-provided summary
```

---

## The 8-Step Pipeline

### Step 1: READ — Extract Content
Execute extraction according to the Strategy chain. Log the successful extraction method.

### Step 2: CLASSIFY — Categorize
Assign **1 primary category** + up to 2 tags:

| Category | Description | Example |
|----------|-------------|---------|
| `infra` | Infrastructure / protocols / networking | MCP, Pilot Protocol |
| `strategy` | Architectural decisions / routing / cost op | Model routing, multi-account |
| `skill` | Agent Skills / tools / capabilities | Skill patterns, MCP interfaces |
| `business` | Business models / market signals | SaaS frameworks, pricing |
| `theory` | Conceptual frameworks / mental models | Bayes, decision theory |
| `tutorial` | Learning material / guides | Claude Code, Agent Loops |
| `product` | New tool/service releases | LM Studio, model drops |
| `threat` | Risk / security / deprecations | API changes, vulnerabilities |

### Step 3: ANALYZE — Strategic Valuation

Formulate the following breakdown:
```markdown
## Strategic Assessment
- **What is it?** [One-sentence summary]
- **Value Proposition:** [Specific capability/benefit]
- **Actionability:** [Specific outputs/projects it enables]
- **Strategic Value:** [🔴 Critical / 🟡 High / 🟢 Medium / ⚪ Low]
- **Competitive Advantage:** [What is the cost of NOT knowing this?]
- **Capability Boundary Shift:** [What can the Agent do now that it couldn't do before?]
```

### Step 4: MAP — Correlate with Architecture

Read `{landscape_path}` (Strategic Landscape). Answer:
- What architectural layer does this impact?
- What existing components does this depend on?
- Does the Landscape map need to be updated?

*(If Landscape file does not exist, skip and prompt user in Step 8 to initialize.)*

### Step 5: STORE — Mint Obsidian Note

Target Path: `{obsidian_vault_path}/{intelligence_folder}/YYYYMMDD_Source_Title.md`

Template:
```markdown
# [Title]

**Source:** [Link](URL)
**Date:** YYYY-MM-DD
**Category:** [Primary] / [Tags]
**Strategic Value:** [🔴/🟡/🟢/⚪] + reason
**Extraction Method:** [read_url / browser / search / user_paste]

---

## Abstract
[2-3 paragraph core summary]

## Key Takeaways
[Numbered list]

## Architectural Impact
[Relationship with current systems]

## Capability Boundary Shift
[What the Agent can do now vs before. If none, write "None"]

## Action Items
[Next steps. If none, write "N/A"]

---

**Analytical Notes:** [Direct, sharp, opinionated analysis]
```

### Step 6: SYNTHESIZE — Auto-Skill Generation (Evolution Step)

**Trigger:** Content describes an **actionable tool, API, protocol, or technique** that the Agent currently lacks.

**Do NOT trigger if:** Content is purely theoretical, an opinion piece, a capability the Agent already possesses, or ranked ⚪ Low purely regarding strategic value.

**Execution:**

1. **Gap Analysis:** Compare current `skills/` directory and Strategic Landscape to confirm this is a missing capability.
2. **Draft Minting:** Create a new Skill folder in `{workspace}/skills/_drafts/`:

```
skills/_drafts/[skill-name]/
├── SKILL.md          # Generated behavior definition
└── README.md         # Brief description, source, dependencies
```

3. **SKILL.md Template:**

```markdown
---
name: [Skill Name]
version: 0.1.0-draft
description: >
  [Generated description based on ingestion]
  Auto-synthesized by Intelligence Ingestion from: [Source URL]
---

# [Skill Name]

> 🧬 This Skill was auto-generated by Intelligence Ingestion and requires human review.
> Source: [URL]
> Generated: YYYY-MM-DD

## Prerequisites
[Dependencies extracted from content: API Keys, CLI tools, services]

## Trigger Conditions
[When should this trigger based on capability description]

## Execution Flow
[Step-by-step logic pulled from ingested docs]

## Input/Output
- **Input:** [Expected input]
- **Output:** [Expected output]
```

4. **Security Isolation:** Drafts remain in `_drafts/` and are ignored by the Agent runtime. The operator must review the code and manually move it to the `skills/` directory to activate it.

### Step 7: REMEMBER — Update Core Memory

1. **Mandatory:** Append to daily log `{workspace}/memory/YYYY-MM-DD.md`
2. **If 🔴 Critical:** Sync update to `{landscape_path}`
3. **If Tool related:** Flag `TOOLS.md` for review
4. **If Skill Draft Synthesized:** Log the draft path and flag it as entirely pending human review.

### Step 8: RESPOND — Feedback to Operator

Respond exactly in this layout:
```
📥 Ingested: [Title]
📂 Class: [Category]
🎯 Value: [🔴/🟡/🟢/⚪] [One sentence]
🔄 Cap Shift: [Delta explanation / None]
🧬 Skill Draft: [Generated → skills/_drafts/[name]/ | N/A]
💾 Archived: Obsidian → {intelligence_folder}/[Filename]
🗺️ Landscape: [Updated / Unchanged / Missing]
⚡ Action: [Review draft / Review landscape / None]
```

---

## Companion: Strategic Landscape

Intelligence Ingestion pairs directly with your **Strategic Landscape**:

- **Intelligence Ingestion** = The "Information Input"
- **Strategic Landscape** = The "Capability Map" 

Every time 🔴 Critical information is ingested, the Landscape updates automatically, providing a real-time view of what the Agent knows, what it can do, and what the blind spots are.

---

## Complete Execution Example

### Input
```
Analyze this: https://x.com/kaboraAI/status/1234567890
```

### Execution
```
Step 1: READ
  → xurl Skill invoked → Success
  → Content: "MCP is the new TCP for agents. 97M downloads..."

Step 2: CLASSIFY
  → Primary: infra
  → Tags: skill, strategy

Step 3: ANALYZE
  → Value: 🔴 Critical
  → Cap Shift: Skills must adopt MCP interfaces immediately.

Step 4: MAP
  → Impact Layer: Layer 2 (Communication) + Layer 4 (Orchestration)
  → Update Landscape: Yes

Step 5: STORE
  → Obsidian Node: 20_Intelligence/20260225_kaboraAI_MCP_Agent_TCP.md

Step 6: SYNTHESIZE
  → Gap: Agent currently lacks automatic MCP schema generation
  → Draft: skills/_drafts/mcp-schema-generator/SKILL.md
  → Logic: Reads existing Skills and auto-generates MCP JSON

Step 7: REMEMBER
  → Updated memory/2026-02-25.md
  → Updated STRATEGIC_LANDSCAPE.md
  → Logged Draft: mcp-schema-generator pending review

Step 8: RESPOND
```

### Output
```
📥 Ingested: MCP is the new TCP for agents
📂 Class: infra / skill, strategy
🎯 Value: 🔴 Critical — MCP passing 97M downloads signals 24-month standardization window
🔄 Cap Shift: Skills require MCP interfaces to be discovered by external swarms
🧬 Skill Draft: Generated → skills/_drafts/mcp-schema-generator/
   → Function: Auto-compiles OpenClaw Skills to MCP schemas
   → Review: mv skills/_drafts/mcp-schema-generator skills/mcp-schema-generator
💾 Archived: Obsidian → 20_Intelligence/20260225_kaboraAI_MCP_Agent_TCP.md
🗺️ Landscape: Updated (Communication + Orchestration layers)
⚡ Action: Review schema generator draft; plan fleet-wide audit
```

---

## Edge Cases

| Condition | Handler |
|-----------|---------|
| Multiple URLs | Process separately; create independent notes |
| Redundant info | Map to existing note; append or reference |
| Non-English | Analyze raw content; write notes in user's native tongue |
| Unreachable URL | Mark as failed; analyze whatever context user provided |
| User provided analysis | Integrate with assessment; do not override |
| `config.json` missing | Halt; stream remediation steps |
| Landscape missing | Skip Step 4; prompt initialization in Step 8 |
| All X/Twitter falls fail | Ask user to paste text |
| Pure theory/opinion | Skip SYNTHESIZE; mark N/A |
| Capability exists | Skip SYNTHESIZE; mark existing |
| `_drafts/` missing | Auto-create `{workspace}/skills/_drafts/` |

---

## Quality Checklist

Before responding, verify (using `ls` or checks):

- [ ] Obsidian note minted as `YYYYMMDD_Source_Title.md`
- [ ] Daily memory log appended
- [ ] Source URL retained in metadata
- [ ] Strategic Value scored
- [ ] Capability Shift assessed
- [ ] Skill draft synthesized (if applicable, verify `_drafts/` path exists)
- [ ] Strategic Landscape updated (if applicable)
- [ ] Operator received standard Step 8 output
- [ ] Explicit fallback reasoning provided if extraction failed
