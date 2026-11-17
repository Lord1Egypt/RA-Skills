<!-- DOCKEY: tsk-3a8d5 -->
This document is the AI conversation task documentation for the Informat low-code platform.

## Overview

The Informat platform has the following agents. When creating an AI conversation task, aiModuleId corresponds to the ID field of these agents:
- Data Table Agent. 	id:designer-ai-agent-table, description: The Informat Data Table Agent can assist you with data table modeling, field configuration, and other needs, comprehensively improving low-code development efficiency.
- Dashboard Agent. 	id:designer-ai-agent-dashboard, description: The Informat Dashboard Agent can assist you with dashboard creation and dashboard card creation.
- Script Agent.		id:designer-ai-agent-script, description: The Informat Script Agent can assist you with script generation and execution tasks, and supports querying modules and application information, script management, and other features, comprehensively improving low-code development efficiency.
- Data Agent.		id:designer-ai-agent-data, description: The Data Agent is used to understand and operate data resources in the current application. It can automatically retrieve data tables and their structure information, execute flexible data queries (supporting filtering, pagination, sorting, grouping, and aggregation analysis), and supports batch generation of test data and importing data from Excel and other files. Applicable to data analysis, data modeling, test data construction, and business validation scenarios.
- Workflow Agent.	id:designer-ai-agent-bpmn, description: The Workflow Agent can assist you in generating, editing, validating, and publishing workflows through natural language, enabling intelligent end-to-end construction of approval and business processes.
- Website Agent.		id:designer-ai-agent-website, description: The Informat Website Agent is used to assist users in building and managing website resources, supporting static resource hosting, page display, and website structure design. Without writing any backend code, you can display data from Informat as a website, suitable for corporate websites, portals, showcase pages, and other scenarios.
- API Agent.		id:designer-ai-agent-api, description: The API Agent is used to assist users in designing, configuring, validating, and managing application APIs, covering API path definition, script invocation, pre/post processing logic, rate limiting and security policies, and ensuring APIs have completeness and executability after creation or update.
- Scheduled Task Agent.	id:designer-ai-agent-schedule, description: The Scheduled Task Agent is used to assist users in designing, configuring, validating, and managing scheduled tasks (Schedule / Job) in applications, covering trigger rules, execution scripts, failure strategies, concurrency control, and security constraints, and ensuring tasks have completeness and executability after creation or update.
- App Structure Agent.	id:designer-ai-agent-appconfig, description: The App Structure Agent is dedicated to managing application metadata structure (Define AST), supporting reading, analyzing, modifying, validating, and publishing application configurations, ensuring all structural changes are safe, traceable, and verifiable.

Important Dependency Notes
The following three agents all depend on data tables created by designer-ai-agent-table (Data Table Agent) to function properly and cannot be used independently:
- designer-ai-agent-dashboard (Dashboard Agent)
- designer-ai-agent-data (Data Agent)
- designer-ai-agent-bpmn (Workflow Agent)

## Task ordering (hard constraint — order by dependency topology)

Components reference one another, so the task list MUST be ordered "dependencies first"; otherwise a later component cannot fill in the real IDs of an earlier one:

1. **Data tables** (first) — the data foundation of everything else.
2. **Scripts** — called by APIs / automations / scheduled tasks.
3. **APIs**.
4. **Workflows (BPMN)** — bound to data tables.
5. **Dashboards** — reference data tables.
6. **Automations / listeners / scheduled tasks** (last) — their steps reference real values such as the workflow module ID, table ID, and script ID, and can only be orchestrated **after all the above exist and their real IDs can be queried**. Put these tasks at the end, and before writing each step query the real ID of the referenced object; never leave a reference empty or use a placeholder (empty references are rejected on save).

## Data-modeling requirement (relations must not all be 1:1)

When an app contains ≥2 tables, the task list MUST explicitly include "build the inter-table relations" steps and pick the right relation type by semantics — **do not model every link as a single RelationRecord (N:1)**:

- Master→detail one-to-many: add a LookupList (1:N, with a filter) on the master table.
- Many-to-many / weak links: add a Relation (M:N).
- Every relation field needs its display columnList ("fields to show").

If the whole app has no Relation or LookupList field at all, the finish self-check judges the model too flat and blocks (see the data table doc).
