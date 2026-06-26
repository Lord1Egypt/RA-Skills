---
name: prd-skill
description: Generate structured Product Requirements Documents (PRD) from natural language user requirements. Use when a user provides an app idea or feature request and needs a comprehensive PRD with functional requirements, user flows, technical specifications, and implementation details. This is the first step in the auto-dev-pipeline that triggers dev-skill and qa-skill automatically.
---

# PRD Skill - Product Requirements Document Generator

## Overview

This skill transforms natural language app ideas into structured Product Requirements Documents (PRD). It analyzes user requirements and generates comprehensive documentation including functional specifications, user flows, technical requirements, and implementation details.

## Workflow

### 1. Input Analysis
- Parse natural language requirements
- Identify core features and user needs
- Determine app type and target platform

### 2. PRD Structure Generation
Generate a structured PRD with the following sections:

#### 2.1 Product Overview
- App name and description
- Target audience
- Core value proposition
- Success metrics

#### 2.2 Functional Requirements
- Feature list with priority (P0, P1, P2)
- User stories and acceptance criteria
- Screen-by-screen specifications

#### 2.3 User Flows
- User journey maps
- Navigation flow diagrams
- Key user interactions

#### 2.4 Technical Specifications
- Platform requirements (iOS version, device support)
- Architecture decisions
- Third-party integrations
- Data models and APIs

#### 2.5 Non-Functional Requirements
- Performance requirements
- Security considerations
- Accessibility standards
- Localization needs

### 3. Output Format
The PRD is generated in markdown format with clear section headers and structured content. After generating the PRD, the skill automatically triggers the dev-skill to begin implementation.

## Examples

**User Input:** "做一个待办事项App，支持分类、提醒和分享功能"

**Generated PRD Sections:**
1. **Product Overview**: Todo List App with categorization, reminders, and sharing
2. **Functional Requirements**: 
   - P0: Create/Edit/Delete tasks
   - P1: Task categorization with tags
   - P1: Push notifications for reminders
   - P2: Share tasks via iMessage/Email
3. **User Flows**: Onboarding → Task creation → Categorization → Reminder setup
4. **Technical Specs**: SwiftUI, Core Data, UserNotifications framework
5. **Non-Functional**: Offline support, iCloud sync, accessibility features

## Auto-Trigger Next Steps

After generating the PRD, this skill automatically:
1. Saves the PRD to `prd-output/` directory with timestamp
2. Triggers `dev-skill` with the PRD as input
3. Monitors the pipeline progress through session messaging

## Integration with Auto-Dev-Pipeline

This skill is designed to work seamlessly with:
- **dev-skill**: Receives PRD and generates SwiftUI code
- **qa-skill**: Receives code and generates test cases
- **session coordination**: Uses `sessions_send` to trigger next steps

## Best Practices

1. **Be specific**: Ask clarifying questions if requirements are vague
2. **Prioritize**: Always assign priority levels to features
3. **Consider constraints**: Include iOS platform limitations
4. **Think MVP**: Focus on minimum viable product first
5. **Document assumptions**: Clearly state any assumptions made