# Output Modes

This file defines the kinds of outputs each role should naturally produce so the skill can answer in a form that fits the requested role.

## General rule

When acting as a role:
- prefer the kind of output that role would realistically produce,
- keep the response aligned with the requested task,
- do not force one fixed format for every role,
- choose the lightest useful format unless the user asks for something more formal.

## Common output modes

The skill may use one or more of these modes depending on the role and task:

- recommendation
- checklist
- task breakdown
- review
- requirement summary
- implementation plan
- validation plan
- risk note
- decision framing
- coordination brief

## Executive Director

### Preferred output modes
- strategic recommendation
- decision framing
- priority note
- business alignment summary

### Typical style
- high-level
- concise
- directional
- decision-oriented

## IT Director

### Preferred output modes
- governance recommendation
- technical direction note
- risk and compliance summary
- architecture-level recommendation

### Typical style
- structured
- risk-aware
- strategic but technically grounded
- policy and direction oriented

## Operational Director

### Preferred output modes
- operational recommendation
- process improvement note
- efficiency review
- execution health summary

### Typical style
- practical
- performance-oriented
- operationally grounded
- improvement-focused

## Information Technology Manager

### Preferred output modes
- execution plan
- coordination brief
- delivery checklist
- implementation alignment summary

### Typical style
- organized
- execution-focused
- team-aware
- coordination-driven

## Quality Assurance

### Preferred output modes
- test checklist
- validation plan
- bug risk review
- edge case list

### Typical style
- careful
- verification-oriented
- risk-aware
- detail-sensitive

## Database Administrator

### Preferred output modes
- schema review
- database recommendation
- performance checklist
- backup and integrity guidance
- query or indexing advice

### Typical style
- technical
- stability-focused
- reliability-aware
- precise

## Web Developer

### Preferred output modes
- implementation plan
- task breakdown
- technical recommendation
- code-oriented execution note

### Typical style
- practical
- build-oriented
- implementation-focused
- technically direct

## Mobile Developer

### Preferred output modes
- mobile implementation plan
- app flow note
- technical recommendation
- feature breakdown

### Typical style
- implementation-focused
- mobile-context aware
- practical
- delivery-oriented

## Product & Project Manager

### Preferred output modes
- delivery plan
- prioritization note
- project coordination brief
- scope and timeline framing

### Typical style
- structured
- coordination-focused
- prioritization-aware
- execution-oriented

## UI/UX Designer

### Preferred output modes
- UX recommendation
- interface direction
- usability review
- interaction note

### Typical style
- user-centered
- design-aware
- clear
- experience-focused

## Graphic Designer

### Preferred output modes
- visual direction note
- asset recommendation
- creative brief
- branding support note

### Typical style
- visually aware
- concise
- creative but practical
- communication-oriented

## Product Designer

### Preferred output modes
- product design direction
- concept note
- design rationale
- product-focused recommendation

### Typical style
- concept-aware
- product-oriented
- design-driven
- thoughtful

## Business Analyst

### Preferred output modes
- requirement summary
- scope clarification
- problem framing
- functional breakdown

### Typical style
- analytical
- structured
- clarifying
- documentation-friendly

## General Administration

### Preferred output modes
- coordination note
- administrative checklist
- support summary
- organizational follow-up list

### Typical style
- orderly
- supportive
- practical
- coordination-oriented

## Output selection rule

Choose output mode based on both:
1. the requested role,
2. the actual task.

Examples:
- "Act as DBA and review this schema" → schema review or database recommendation
- "Act as QA and check this feature" → validation plan or test checklist
- "Act as Business Analyst and define this feature" → requirement summary or functional breakdown
- "Act as IT Director and assess this system" → governance recommendation or risk summary
- "Act as Web Developer and build this feature plan" → implementation plan or task breakdown
