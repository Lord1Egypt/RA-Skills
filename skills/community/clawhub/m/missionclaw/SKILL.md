---
name: missionclaw
description: >
  Integrates with MissionClaw for project management and AI agent orchestration. Use when the user wants to create projects, manage tasks via Kanban, assign work to agents, view organization charts, or schedule automated tasks. Calls the MissionClaw API at http://localhost:3000.
---

# MissionClaw Skill

This skill integrates Velo with MissionClaw - a visual "Mission Control" for orchestrating AI agents.

## Installation

MissionClaw skill is **automatically installed** with OpenClaw. If not present, install via:

```bash
# Using ClawHub
clawhub install missionclaw

# Or manually copy to skills folder
cp -r missionclaw ~/.openclaw/skills/
```

## Quick Start

1. **Start MissionClaw:**
   ```bash
   cd ~/.openclaw/workspace/missionclaw
   npm run dev
   ```
   
   Or use PM2 for production:
   ```bash
   pm2 start npm --name missionclaw -- run start
   ```

2. **Open in Browser:**
   ```
   http://localhost:3000
   ```

## Features

### 1. Dashboard
- Overview of all projects, agents, and tasks
- System status (Gateway, Ollama connections)
- Quick actions

### 2. Kanban Board
- 5 columns: Backlog → To Do → In Progress → Review → Done
- Drag & drop task management
- Assign tasks to agents
- Set priority levels (Low, Medium, High, Urgent)

### 3. Agent Forge
- Create and manage AI agents
- 3 agent types: OpenClaw, Ollama (Local), Cloud API
- 23 unique avatars to choose from
- Edit SOUL.md and IDENTITY.md for each agent

### 4. Org Chart
- Team-based hierarchy view
- Real-time agent status
- Agent details with personality

### 5. Scheduler
- Cron-based task scheduling
- One-click "Run Now"

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/projects` | List all projects |
| POST | `/api/projects` | Create new project (full fields) |
| GET | `/api/system` | System status |
| GET | `/api/gateway` | OpenClaw Gateway status |
| GET | `/api/ollama` | Ollama models |

## Create Project (Full Fields)

**POST** `http://localhost:3000/api/projects`

```json
{
  "projectName": "The DigiCode Landing Page",
  "shortDescription": "Modern landing page for digital marketing agency",
  "tech": "Next.js, React, Tailwind CSS",
  "author": "Suresh",
  "fullPRD": "1. Hero section with agency name\n2. Services grid\n3. Portfolio showcase\n4. Contact form\n5. Footer with social links",
  "projectType": "web development",
  "priority": "high"
}
```

**Example curl:**
```bash
curl -X POST http://localhost:3000/api/projects \
  -H "Content-Type: application/json" \
  -d '{
    "projectName": "The DigiCode Landing Page",
    "shortDescription": "Modern landing page for digital marketing agency",
    "tech": "Next.js, React, Tailwind CSS",
    "author": "Suresh",
    "fullPRD": "1. Hero section\n2. Services grid\n3. Portfolio\n4. Contact form\n5. Footer",
    "projectType": "web development",
    "priority": "high"
  }'
```

## Team Routing

Automatically route projects to the appropriate team:

| Keywords | Team |
|----------|------|
| marketing, seo, ads, content, social | Marketing |
| web, frontend, backend, api, database | Developer |
| design, logo, graphic, video, ui, ux | Creative |
| sales, crm, leads | Sales |
| support, help, bug, issue | Support |
| operations, automation, workflow | Operations |

## Example Usage

**User:** "Create a new SEO project"

**You:** Use the MissionClaw UI to:
1. Go to Projects → Create new project
2. Go to Kanban → Add tasks
3. Assign to SEO Specialist agent
4. Track progress on dashboard

---

For more info: https://github.com/sureshchitmil/missionclaw
