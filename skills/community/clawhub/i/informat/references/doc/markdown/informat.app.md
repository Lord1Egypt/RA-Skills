This document defines the global concepts, structure, and capability boundaries of the Informat Application (App).

# Informat App Documentation

## 1. Application (App) Overview

In Informat, an **Application** is an independent business system unit designed to support specific business scenarios.

An application can be understood as a complete system, for example:

- CRM (Customer Relationship Management)
- ERP (Enterprise Resource Planning)
- OA (Office Automation)
- Project Management System

An application contains Data Tables (Table), Dashboards (Dashboard), Workflows (Bpmn), AI Assistants (AiAgent), Websites (Website), Automations (Automatic), Scripts (Script), Scheduled Tasks (Schedule), and other logic to implement a complete business loop.

---

## 2. Application Structure

### 2.1 Modules

Modules are creatable functional units within an application, each corresponding to an independent feature page. Supported module types:

- **Data Table (Table)** — Structured data management, doc: `informat.table.md`, script API: `script/table.md`
- **Workflow (Bpmn)** — Business approval and process orchestration, script API: `script/bpmn.md`
- **Dashboard** — Data visualization and statistical analysis, doc: `informat.dashboard.md`
- **AI Assistant (AiAgent)** — Intelligent conversation and AI capability integration, doc: `informat.aiassistant.md`, script API: `script/aiagent.md`
- **Website** — Custom pages and static resource hosting, doc: `informat.website.md`, script API: `script/website.md`
- **Survey** — Questionnaire and form collection, script API: `script/survey.md`

---

### 2.2 Application Default Components

The following features are built-in default components of an application, not modules. They do not need to be created separately — every application automatically includes them:

- **Automation (Automatic)** — Event-triggered and data-change-triggered auto-execution logic, reference: `informat.automatic.md`
- **Script** — JavaScript extensions, can call platform APIs and integrate with external systems, reference: `informat.script.md`
- **Scheduled Task (Schedule)** — Tasks executed periodically via Cron expressions, reference: `informat.schedule.md`
- **API Interface (API)** — Externally exposed data interfaces, reference: `informat.api.md`
- **Internationalization (I18n)** — Multi-language translation configuration
- **App Listener** — Application-level lifecycle event listeners, supporting automation execution on events such as app install, uninstall, enable, and disable, reference: `informat.listeners.md`

---

### 2.3 Interfaces

Entry points for user interaction with the system, including:

- Form pages
- List pages
- Dashboards
- Custom views

Supports rapid UI construction through drag-and-drop components.

---

## 3. Application Access URL

Application page access format:
https://${webUrl}/app/${appId}

## 4. Application Designer Access URL (Designer)

Application designer page access format:
https://${webUrl}/designer/${appId}/setting/info


---

## 5. Application Configuration Capabilities

### 5.1 Basic Configuration

- Application information
- Theme styles
- Internationalization
- Environment variables

### 5.2 Permission Management

- User management
- Role permissions
- Data permission control

### 5.3 Extension Capabilities

- API interfaces
- Scripts
- Listeners
- Extension libraries (Java)

---

## 6. Use Cases

Applications can be used to build:

Enterprise Management Systems (ERP / OA)
Data Management Systems
Approval Workflow Systems
Project Management Systems
Industry-specific Custom Systems

## 7. Summary

App = Data + Interface + Workflow + Automation + Extension Capabilities
It is not just an "application", but a complete business system container.
