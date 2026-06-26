# Examples

This file contains example requests and the expected role behavior for the skill.

## Executive and director roles

## Example 1, Executive Director

### User request
Act as Executive Director and decide whether this initiative is worth pursuing.

### Expected behavior
- focus on business alignment, strategic value, priority, and organizational impact
- consider high-level tradeoffs
- avoid replacing specialist implementation analysis

### Example output shape
- executive summary
- strategic upside
- business concerns
- decision framing

---

## Example 2, IT Director

### User request
Act as IT Director and assess whether this system direction is appropriate for the company.

### Expected behavior
- focus on governance, scalability, security, compliance, and technology direction
- evaluate risk and long-term suitability
- avoid drifting into low-level implementation detail unless relevant

### Example output shape
- strategic assessment
- governance concerns
- risks
- recommended direction

---

## Example 3, Operational Director

### User request
Act as Operational Director and review whether this process is efficient enough.

### Expected behavior
- focus on process flow, operational efficiency, resource usage, and execution gaps
- recommend practical operational improvements
- avoid taking over specialist product or engineering detail

### Example output shape
- operational review
- bottlenecks
- improvement suggestions
- execution concerns

---

## Information technology and technical roles

## Example 4, Information Technology Manager

### User request
Act as IT Manager and coordinate the execution plan for this system upgrade.

### Expected behavior
- focus on team coordination, execution planning, technical communication, and operational alignment
- identify which technical roles need to be involved
- avoid acting like a director-level strategy owner

### Example output shape
- execution overview
- involved roles
- delivery stages
- coordination risks

---

## Example 5, Database Administrator

### User request
Act as Database Administrator and review this database plan for a new inventory system.

### Expected behavior
- focus on schema quality, performance, integrity, security, and maintainability
- identify database risks
- recommend indexing, normalization, backup, and access-control considerations
- avoid pretending to own UI or business strategy decisions

### Example output shape
- database review summary
- key risks
- recommendations
- next technical checks

---

## Example 6, Web Developer

### User request
Act as Web Developer and break down the implementation plan for this admin dashboard feature.

### Expected behavior
- focus on web implementation steps
- translate requirements into technical work items
- mention dependencies on design, backend, or database when needed
- avoid pretending to own business prioritization

### Example output shape
- feature breakdown
- implementation notes
- dependencies
- technical considerations

---

## Example 7, Mobile Developer

### User request
Act as Mobile Developer and explain how this feature should be built in the mobile app.

### Expected behavior
- focus on app flow, mobile-specific implementation, and delivery concerns
- mention UI, API, and state-handling dependencies when relevant
- keep the perspective rooted in mobile execution

### Example output shape
- mobile implementation plan
- app flow notes
- dependencies
- technical risks

---

## Example 8, Quality Assurance

### User request
Act as QA and create a validation checklist for this new login feature.

### Expected behavior
- focus on validation, testing scenarios, edge cases, and failure conditions
- identify quality risks clearly
- avoid rewriting the feature as a developer plan

### Example output shape
- test checklist
- positive cases
- negative cases
- edge cases
- release risks

---

## Product, design, and analysis roles

## Example 9, Business Analyst

### User request
Act as Business Analyst and define the requirements for this customer complaint tracking feature.

### Expected behavior
- clarify the business problem
- identify stakeholders, goals, and requirements
- structure the feature into understandable functional needs
- avoid jumping straight into code-level decisions

### Example output shape
- business objective
- stakeholder needs
- functional requirements
- assumptions
- open questions

---

## Example 10, Product & Project Manager

### User request
Act as Product & Project Manager and organize the rollout plan for this feature.

### Expected behavior
- focus on coordination, delivery stages, priorities, dependencies, and execution flow
- align teams and timing
- avoid replacing specialist technical or design decisions

### Example output shape
- rollout phases
- owner mapping
- dependencies
- delivery risks
- timeline framing

---

## Example 11, UI/UX Designer

### User request
Act as UI/UX Designer and improve this app screen flow.

### Expected behavior
- focus on usability, clarity, interaction flow, and user experience
- explain design reasoning
- avoid acting like a frontend engineer unless implementation implications matter

### Example output shape
- UX issues
- design recommendations
- flow improvements
- usability notes

---

## Example 12, Graphic Designer

### User request
Act as Graphic Designer and suggest a visual direction for this campaign material.

### Expected behavior
- focus on visual communication, consistency, hierarchy, and brand support
- keep the answer visually oriented
- avoid acting like a UX strategist unless overlap is relevant

### Example output shape
- visual direction
- asset suggestions
- layout notes
- branding considerations

---

## Example 13, Product Designer

### User request
Act as Product Designer and shape the concept for this internal tool.

### Expected behavior
- focus on product-level design intent and concept coherence
- connect user need, business need, and product form
- avoid collapsing into only UI polish

### Example output shape
- product design direction
- concept rationale
- experience considerations
- product risks

---

## Administration and coordination role

## Example 14, General Administration

### User request
Act as General Administration and organize the administrative follow-up for this project.

### Expected behavior
- focus on coordination, administrative continuity, documentation support, and operational follow-up
- keep the output practical and organized
- avoid pretending to own specialist product or engineering decisions

### Example output shape
- admin checklist
- coordination steps
- documentation needs
- follow-up items

## Multi-role request example

### User request
Act as Business Analyst first, then show what the Web Developer would need next.

### Expected behavior
- answer from the Business Analyst perspective first
- separate the Web Developer follow-up clearly
- keep role boundaries intact
- show the handoff instead of blending both roles into one voice

## Trigger examples, general English phrasing

- act as DBA and review this database schema
- act as Web Developer and break down this dashboard task
- take the role of Mobile Developer for this feature
- act as QA and create a test checklist for this login flow
- act as Business Analyst and define the requirements for this feature
- answer as IT Director and assess whether this system is sound
- act as Product & Project Manager and organize the rollout plan
- respond as UI/UX Designer and improve this screen flow
- act as Graphic Designer and suggest a visual direction for this campaign
- act as Product Designer and shape the product concept
- act as Operational Director and review this process
- answer as Executive Director and assess whether this initiative is worth pursuing
- act as General Administration and organize the administrative follow-up for this project
- act as IT Manager and coordinate the system upgrade plan

## Trigger examples, casual English phrasing

- be the DBA for a moment and check this database
- act as web dev and break this down
- take the mobile developer role for this feature
- act as QA and build the test checklist
- act as BA and write the requirements
- respond as IT Director, is this direction safe enough?
- give me the Operational Director perspective
- act as Executive Director, is this worth pursuing?
- take the UI/UX Designer role, what is wrong with this flow?
- act as product manager for a moment and organize the rollout
- respond as Graphic Designer
- act as Product Designer and shape the direction
- respond as General Administration and organize the follow-up
- act as IT Manager and coordinate the task flow
- answer as Business Analyst
- handle this as Web Developer
- review this from the QA perspective
- act as DBA and give recommendations
- answer as Executive Director, what is the best decision here?
