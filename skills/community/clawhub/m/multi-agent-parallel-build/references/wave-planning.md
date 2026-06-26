# Wave Planning Guide

## Task Decomposition Checklist

Before spawning agents, verify:
- [ ] All shared components exist (shell, CSS, API client wrapper)
- [ ] API endpoints are built AND tested (curl each one)
- [ ] Each agent's output files are in separate paths (no overlap)
- [ ] Each agent prompt includes: file path, shell import path, API endpoints, data shapes
- [ ] No agent needs output from another agent

## Agent Prompt Template

```
Build {page_name} at {file_path}.

## Shared Resources
- Shell: Import createShell, createCard, mcFetch from {shell_path}
- CSS: Link to {css_path}
- API base: {api_base_url}

## Data Endpoints
{for each endpoint}
- GET {endpoint} → Returns: {json_shape_example}
{end}

## Requirements
- {specific_requirements}
- Dark theme (use CSS variables from shell.css)
- No external frameworks — vanilla JS, HTML, CSS
- Use Chart.js for charts (CDN: https://cdn.jsdelivr.net/npm/chart.js)

## Page Layout
{wireframe_description}
```

## Post-Merge Checklist
- [ ] Fix double-prefix API URLs (sed search for repeated path segments)
- [ ] Verify all pages load without console errors
- [ ] Check mcFetch calls use correct relative paths
- [ ] Add StaticFiles mount for new directories
- [ ] Test each page's data loading against live API
