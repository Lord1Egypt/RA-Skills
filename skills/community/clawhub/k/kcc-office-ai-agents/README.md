# KCC Office v2 - AI Agents Collaboration System

This module implements the AI Agents collaboration component for the KCC Office v2 project, providing autonomous AI agents that can work together to manage and operate the virtual office environment.

## Overview

The AI Agents system enables:
- Autonomous operation of office agents (CEO, CFO, CTO, COO, EDN, Komi)
- Collaborative decision-making and task execution
- Proactive office management without constant human intervention
- Context persistence and learning from interactions

## Architecture

Based on the Proactive Agent framework with WAL Protocol and Working Buffer for context persistence.

### Agent Roles
- **Komi**: Task Coordinator / Chief of Operations
- **CEO**: Overall Strategy and Vision
- **CFO**: Financial Management and Investment
- **CTO**: Technology and Technical Implementation
- **COO**: Operations and Execution
- **EDN**: Independent User Assistance and Support

### Core Features
- Write-Ahead Logging (WAL) for critical details
- Working Buffer for danger zone protection
- Autonomous cron execution
- Self-improvement through learning capture
- Inter-agent communication and coordination

## Implementation

This system uses patterns from:
- proactive-agent skill (v3.1.0)
- self-improving-agent skill

## Usage

See individual agent implementations in the `agents/` directory.