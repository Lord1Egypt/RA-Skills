---
name: lowcode-platform-development
description: Automates the creation of required development roles, scaffolds the project structure, and generates code for a low‑code development platform with Vue2 + ElementUI front‑end and Java (Spring Boot) back‑end. Trigger when a user wants a full low‑code platform built from scratch.
---

# Low‑Code Platform Development Skill

## When to use
- User asks to **build a low‑code development platform** using Vue2 + ElementUI for UI and Java (Spring Boot) for the back‑end.
- User wants the assistant to **create development roles** (frontend, backend, devops, QA) and set up the repository structure automatically.
- User expects the platform to include **page editor, component library, data model manager, workflow engine** as described in the architecture overview.

## Overview
This skill automates the end‑to‑end setup of the platform:
1. **Create project roles** (frontend engineer, backend engineer, devops, QA) and write brief role descriptions to `docs/roles.md`.
2. **Scaffold repository** with a standard Maven + npm layout (`frontend/`, `backend/`).
3. **Generate base code**:
   - Vue2 project using ElementUI, with a drag‑and‑drop editor skeleton.
   - Spring Boot project with JPA entities for data models, Camunda workflow engine integration, and REST API boilerplate.
4. **Add essential configuration files** (`docker‑compose.yml`, CI pipeline, security settings).
5. **Commit initial version** to a local Git repository.
6. **Provide next‑step guidance** for extending the platform.

## Resources
- **references/architecture.md** – Detailed architecture diagram and component responsibilities.
- **scripts/generate_project.ps1** – PowerShell script that runs the scaffold commands.
- **assets/vue‑template/** – Minimal Vue2+ElementUI starter template.
- **assets/spring‑boot‑template/** – Minimal Spring Boot Maven project template.

## Steps to execute
1. Call `scripts/generate_project.ps1` with the target directory.
2. The script creates the folder layout, writes `docs/roles.md`, copies template assets, and runs `npm install` and `mvn package`.
3. After the script finishes, the skill returns a summary of what was generated and any manual actions required.

## Manual post‑setup actions
- Push the repository to a remote if desired.
- customise the generated UI components in `frontend/src/components/`.
- Add domain‑specific data models to `backend/src/main/java/com/app/lowcode/model/`.
- Configure authentication/authorization in `backend/src/main/java/com/app/lowcode/security/`.

---
