---
name: promotion-calendar-planner
description: Design monthly, quarterly, or annual ecommerce promotion calendars using business goals, platform mega-sale windows, inventory posture, and team capacity, then turn rough planning notes into a sequenced promotion roadmap. Use when operators, marketers, or managers need a promotion cadence plan without live calendar, ad-platform, or project-management integrations.
---

# Promotion Calendar Planner

## Overview

Use this skill to turn annual goals, platform nodes, inventory posture, and team resource notes into a structured promotion calendar. It is designed for operators who need a promotion cadence they can explain to management and hand off to cross-functional teams.

This MVP is heuristic. It does **not** connect to live calendars, ad platforms, merchandising systems, or project-management tools. It relies on the user's planning notes, seasonal context, and team constraints.

## Trigger

Use this skill when the user wants to:
- map a monthly, quarterly, or annual promotion cadence
- decide which sale nodes deserve a full push versus a lighter supporting role
- balance revenue, margin, inventory digestion, and team workload in one schedule
- prepare a promotion roadmap for ops, design, supply chain, and customer service
- turn rough campaign ideas into a sequenced business calendar with risk notes

### Example prompts
- "Build our Q4 promotion calendar around 11.11 and Black Friday"
- "Create a quarterly promo plan that also helps us digest aged inventory"
- "We need a yearly promotion roadmap for our ecommerce team"
- "Plan a lighter monthly cadence without overloading design and customer service"

## Workflow
1. Capture the planning window, business goal, seasonal anchors, and major capacity constraints.
2. Separate mandatory nodes, optional support nodes, and nodes that should probably be skipped.
3. Translate each node into a role such as acquisition, conversion, clearance, or retention.
4. Attach category focus, price posture, team preparation needs, and avoidable conflicts.
5. Return a markdown promotion plan with a calendar table, cadence principles, and a team checklist.

## Inputs
The user can provide any mix of:
- annual, quarterly, or monthly business goals
- platform nodes such as 618, Prime Day, 11.11, Black Friday, or brand days
- inventory posture such as healthy core stock, aged stock, or constrained hero SKUs
- category seasonality and hero categories
- resource limits across ops, design, supply chain, CRM, media, or customer service
- margin rules, discount rules, or customer-experience constraints

## Outputs
Return a markdown plan with:
- a promotion calendar table
- cadence principles before, during, and after major nodes
- a team preparation checklist
- conflict watchouts and risk notes
- assumptions and limits

## Safety
- Do not claim access to live calendars, platform policy feeds, or ad platforms.
- Verify official sale dates and platform rules before locking any execution plan.
- Keep pricing, discount depth, and activation decisions human-approved.
- Treat the plan as a baseline operating rhythm, not a substitute for daily campaign management.

## Best-fit Scenarios
- quarterly and annual ecommerce promotion planning
- cross-functional promotion alignment across ops, design, supply chain, and service
- businesses that need more structure than a spreadsheet of holiday names
- teams trying to reduce promotion chaos and discount overlap

## Not Ideal For
- live campaign pacing and day-to-day media management
- fully automated marketing orchestration
- businesses with no meaningful seasonality or promotion planning rhythm
- regulated categories where promotional language requires extensive review first

## Acceptance Criteria
- Return markdown text.
- Include calendar table, cadence principles, team checklist, and risk notes.
- Explain why key nodes matter instead of listing dates only.
- Surface at least two avoidable planning conflicts.
