# {{product_name}}

## Overview

{{overview_paragraph}}

## Tech Stack

{{#each stack_items}}
- **{{layer}}**: {{choice}} ({{packages}})
{{/each}}

## File Structure

```
{{file_structure}}
```

## Setup

```bash
{{setup_commands}}
```

## Environment Variables

```bash
{{env_vars}}
```

## Core Requirements

{{#each requirements}}
{{number}}. **{{title}}**
   - {{description}}
   {{#each acceptance_criteria}}
   - [ ] {{criterion}}
   {{/each}}

{{/each}}

## Data Model

{{#each entities}}
### {{name}}

| Field | Type | Required | Notes |
|-------|------|----------|-------|
{{#each fields}}
| `{{name}}` | `{{type}}` | {{required}} | {{notes}} |
{{/each}}

{{/each}}

## API Endpoints

| Method | Path | Auth | Description |
|--------|------|------|-------------|
{{#each endpoints}}
| `{{method}}` | `{{path}}` | {{auth}} | {{description}} |
{{/each}}

## Testing

```bash
{{test_commands}}
```

## Deployment

```bash
{{deploy_commands}}
```
