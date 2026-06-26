# Kan.bn TODO API Scope (Single-User)

Base URL: `https://kan.bn/api/v1`

Auth (docs show both patterns):
- `Authorization: Bearer <token>`
- `x-api-key: <api_key>`

This skill intentionally focuses on personal TODO flows.

## Core TODO CRUD

- Create TODO (card)
  - `POST /cards`
  - Required body: `title`, `description`, `listPublicId`, `labelPublicIds`, `memberPublicIds`, `position`
- Read TODO
  - `GET /cards/{cardPublicId}`
- Update TODO
  - `PUT /cards/{cardPublicId}`
  - Updatable: `title`, `description`, `dueDate`, `listPublicId`, `index`
- Delete TODO
  - `DELETE /cards/{cardPublicId}`

## Status Changes

- Move TODO across lists (recommended status model)
  - `PUT /cards/{cardPublicId}` with `listPublicId`
- Optional reordering inside list
  - `PUT /cards/{cardPublicId}` with `index`
- Checklist item completion status
  - `PATCH /checklists/items/{checklistItemPublicId}` with `completed`

## Priority Labels

- Create-time labels
  - `POST /cards` with `labelPublicIds`
- Existing-card label changes
  - `PUT /cards/{cardPublicId}/labels/{labelPublicId}`
  - Endpoint toggles the label on the card and returns `newLabel: true|false`
- Do not expect `PUT /cards/{cardPublicId}` to update labels; official docs only list `title`, `description`, `index`, `listPublicId`, and `dueDate` there.

## Personal Productivity Features

- Workspace and board discovery
  - `GET /workspaces`
  - `GET /workspaces/{workspacePublicId}/boards`
  - `GET /boards/{boardPublicId}`
- Search TODOs by keyword
  - `GET /workspaces/{workspacePublicId}/search?query=...&limit=...`
- List management
  - `POST /lists`
  - `PUT /lists/{listPublicId}`
  - `DELETE /lists/{listPublicId}`
- Comments as personal notes
  - `POST /cards/{cardPublicId}/comments`
  - `PUT /cards/{cardPublicId}/comments/{commentPublicId}`
  - `DELETE /cards/{cardPublicId}/comments/{commentPublicId}`
- Checklists for subtasks
  - `POST /cards/{cardPublicId}/checklists`
  - `POST /checklists/{checklistPublicId}/items`
  - `PATCH /checklists/items/{checklistItemPublicId}`
  - `DELETE /checklists/items/{checklistItemPublicId}`
- Personal profile
  - `GET /users/me`
  - `PUT /users`

## Excluded in This Skill

- Multi-user collaboration and role/permission management
- Invites
- Integrations and imports
- Attachments
