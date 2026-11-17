# Change Log · {{ project.name }}

> Records all proposed / reviewed / implemented changes, forming a traceable change chain (CCB-managed). Stage gate conclusions
> and wave exit review conclusions should also be logged here.

| CR ID | Date | Type | Description | Impact (Scope/Schedule/Cost/Risk) | CCB Decision | Status |
|---------|------|------|------|------------------------------|----------|------|
{{#each changes}}
| {{this.id}} | {{this.date}} | {{this.type}} | {{this.description}} | {{this.impact}} | {{this.decision}} | {{this.status}} |
{{/each}}

## Change Type Legend
- **Scope** / **Schedule** / **Cost** / **Resource** / **Quality** / **Gate**

## Status Definitions
- Proposed / Under Review / Approved / Approved with Conditions / Rejected / In Implementation / Closed

> Tip: Any change deviating from baseline must first fill in `change_request`; after CCB review, the conclusion is recorded in this log;
> programs and hybrid projects must have this log (consistency check will alert on its absence).
