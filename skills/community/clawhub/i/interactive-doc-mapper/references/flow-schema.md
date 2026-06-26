# Flow JSON Schema

Create one JSON object per interactive workflow map.

## Top-Level Fields

- `title` string, optional but recommended.
- `description` string, optional but recommended. State source, scope, and assumptions.
- `groups` array, optional. Use groups to create columns on the page.
- `nodes` array, required. Every package, service, component, database, queue,
  build tool, or external adapter that should stay visible.
- `actions` array, required. Every clickable workflow.

## Groups

```json
{
  "id": "backend",
  "label": "Backend",
  "color": "#2563eb"
}
```

- `id` must be stable and unique.
- `label` is what the page shows.
- `color` is optional and must be a six-digit hex value.

## Nodes

```json
{
  "id": "api",
  "label": "API Package",
  "type": "package",
  "group": "backend",
  "description": "Receives authenticated app requests and routes commands."
}
```

- `id` is referenced by action steps.
- `label` should match the repo or app naming when possible.
- `type` can be `package`, `service`, `component`, `database`, `queue`,
  `build`, `external`, or another project-specific term.
- `group` should match a group ID or use an implicit group.
- `description` should explain responsibility, not implementation trivia.

## Actions

```json
{
  "id": "invite-new-user",
  "label": "Invite new user",
  "summary": "Admin creates an invitation and the system emails a one-time link.",
  "trigger": "Admin submits the invite form",
  "owner": "Admin workspace",
  "steps": [
    {
      "from": "web-app",
      "to": "api",
      "label": "POST /invites",
      "payload": "email, role, workspaceId",
      "notes": "The web package sends the authenticated command to the API boundary.",
      "risk": "Role changes must be checked server-side."
    }
  ]
}
```

- `id` becomes the stable action selector.
- `label` becomes the button text.
- `summary` explains the workflow outcome.
- `trigger` and `owner` are optional metadata chips.
- `steps` must be ordered. Each step is one boundary crossing.
- `from` and `to` must reference node IDs.
- `label` should identify the call, event, artifact, or command.
- `payload` should say what crosses the boundary.
- `notes` should say why that handoff exists or what changes state.
- `risk` is optional and should be used only for real review concerns.

## Authoring Checklist

- Include all packages/components first, then add flows.
- Use source code names for nodes when the map is repo-derived.
- Keep action steps ordered by runtime sequence or build sequence.
- Do not include secrets, tokens, cookies, production customer data, or private
  account URLs.
- Prefer one map per app or bounded subsystem. Large monorepos should get one
  map per product surface or high-value workflow family.
