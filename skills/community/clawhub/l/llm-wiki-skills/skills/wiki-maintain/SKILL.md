---
name: wiki-maintain
description: |
  Manage and evolve the schema and conventions of an LLM wiki knowledge base. Use this skill whenever the user wants to update the CLAUDE.md schema, modify page conventions, adjust naming patterns, refine workflows (ingest, query, lint), or adapt the wiki structure as the knowledge base grows. Perfect for: updating wiki conventions, adapting workflows, changing page templates, adding new page types, or evolving the wiki schema over time. Always use this when user mentions schema, conventions, maintain, update rules, or modify wiki structure.
compatibility: Write, Read, Glob, Grep, Bash
---

# Wiki Knowledge Base - Maintain Skill

This skill manages and evolves the schema and conventions of an LLM-powered wiki knowledge base following the LLM Wiki pattern.

## Core Concept

The schema (CLAUDE.md) is the key configuration file that tells the LLM how the wiki is structured, what conventions to follow, and what workflows to use. This evolves over time as you figure out what works for your domain.

## When to Use This Skill

- User wants to update CLAUDE.md schema
- User wants to modify page conventions
- User wants to adjust naming patterns
- User wants to refine workflows
- User wants to adapt wiki structure
- User mentions schema, conventions, maintain, update rules

## What This Skill Does

1. **Reviews current schema**: Reads existing CLAUDE.md
2. **Proposes improvements**: Suggests updates based on usage patterns
3. **Updates conventions**: Modifies page templates, naming rules
4. **Refines workflows**: Adjusts ingest, query, lint procedures
5. **Adds new page types**: Introduces new categories as needed
6. **Documents changes**: Records schema updates in log.md

## Maintain Workflow

### Step 1: Review Current Schema

Read the current CLAUDE.md to understand:
- Current page types and templates
- Naming conventions
- Workflow definitions
- Cross-reference rules

### Step 2: Identify Needed Changes

Based on wiki usage, identify:
- Conventions that are not working
- Missing page types needed
- Workflows that need refinement
- Naming patterns to improve

### Step 3: Propose Changes

Document proposed changes:
- What will change
- Why the change is needed
- How it affects existing pages
- Migration plan if needed

### Step 4: Update CLAUDE.md

Make the changes to the schema:
- Update page type definitions
- Modify templates
- Refine workflows
- Add new conventions

### Step 5: Update Affected Pages

If needed, update existing pages to conform:
- Rename files to match new conventions
- Update templates in existing pages
- Add missing frontmatter fields

### Step 6: Document Changes

Record the schema update:
`markdown
## [YYYY-MM-DD] maintain | Schema Update
- Changed: [description]
- Reason: [why]
- Affected pages: [list if any]
`

## Common Maintenance Tasks

### Updating Page Templates
- Add new frontmatter fields
- Change section structure
- Add or remove elements

### Refining Naming Conventions
- Change file naming pattern
- Update link format
- Adjust categorization

### Workflow Refinements
- Add steps to ingest process
- Modify query procedure
- Enhance lint checks

### Adding New Page Types
- Define new category
- Create template
- Update index.md structure

## Quality Standards

- Must review current schema before making changes
- Must document reasons for changes
- Must consider impact on existing pages
- Must update log.md
- Should test changes on a few pages first
- Should maintain backward compatibility when possible

## Schema Sections to Maintain

1. **Wiki Overview**: Purpose and scope
2. **Architecture**: Three-layer explanation
3. **Page Types**: All category definitions
4. **Naming Conventions**: File and link patterns
5. **Frontmatter Schema**: All field definitions
6. **Ingest Workflow**: Current procedure
7. **Query Workflow**: Current procedure
8. **Lint Workflow**: Current procedure
9. **Cross-Reference Rules**: Current rules
