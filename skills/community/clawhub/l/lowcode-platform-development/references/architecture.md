# Architecture Overview for Low‑Code Platform

## 1. High‑level diagram
```
[User] <---> Frontend (Vue2 + ElementUI) <---> API Gateway (Spring Boot) <---> Services
```
- **Frontend**: Single‑page app, drag‑and‑drop page editor, component library, data‑source bindings.
- **API Gateway**: Exposes REST endpoints for CRUD, component metadata, workflow deployment.
- **Services**:
  - **Metadata Service** – stores page/component JSON in PostgreSQL.
  - **Data Model Service** – generates JPA entities & Spring Data repositories on the fly.
  - **Workflow Service** – embeds Camunda engine, exposes BPMN editor API.
  - **Auth Service** – Spring Security + JWT, multi‑tenant RBAC.

## 2. Frontend modules
- **Editor Canvas** – `vue-draggable-resizable` for component placement.
- **Property Panel** – ElementUI forms generated from component schema.
- **Component Registry** – JSON defining type, props, default style; loaded from `/api/components`.
- **Preview Mode** – renders the page directly from stored JSON.

## 3. Backend modules
- **Core** – Spring Boot application (`lowcode-platform`).
- **Persistence** – PostgreSQL + JPA/Hibernate.
- **Workflow Engine** – Camunda embedded, BPMN files stored in `workflow/`.
- **Script Engine** – GraalVM JavaScript sandbox for dynamic expressions.
- **Code Generation** – Handlebars templates under `templates/` generate Vue components and Java classes.

## 4. DevOps & Deployment
- Docker‑Compose defines three containers: `frontend`, `backend`, `postgres`.
- CI pipeline (GitHub Actions) runs `npm run build` and `mvn package`, builds Docker images, pushes to registry.
- Optional Kubernetes manifest for production scaling.

## 5. Extensibility points
- **scripts/** – reusable scripts (e.g., `generate_entity.py`).
- **assets/** – starter templates, icons, sample pages.
- **references/** – detailed docs for each module (see other files).

---
