---
name: Mental Health AI Companion
slug: mental-health-companion
description: Evidence-based mental wellness skill providing CBT/DBT/ACT therapeutic exercises, mood tracking with pattern analysis, guided meditation scripts, crisis resource routing, and burnout prevention strategies for individuals and workplace programs.
version: 1.0.0
author: ai-gaoqian
tags:
  - mental-health
  - wellness
  - therapy
  - mindfulness
  - burnout-prevention
  - emotional-intelligence
  - self-care
metadata:
  openclaw:
    requires: openclaw>=1.0.0
---

# Mental Health AI Companion

## Overview
Evidence-based mental wellness skill grounded in clinical psychology frameworks. Provides structured therapeutic exercises from CBT (Cognitive Behavioral Therapy), DBT (Dialectical Behavior Therapy), and ACT (Acceptance and Commitment Therapy). Includes daily mood tracking with longitudinal pattern analysis, guided mindfulness/meditation scripts, crisis resource routing (with appropriate disclaimers), and workplace burnout prevention modules. **Not a replacement for professional therapy** — serves as a supportive self-help companion and early-intervention triage tool.

## Use Cases
- Guide user through structured CBT thought-record exercises
- Track daily mood scores and identify triggers over time with visual analytics
- Generate personalized DBT distress tolerance toolkit for acute anxiety
- Deliver 5/10/15-minute guided mindfulness audio scripts
- Assess workplace burnout risk using Maslach Burnout Inventory framework
- Route users to crisis hotlines based on detected severity (with clear disclaimers)
- Build ACT values-clarification exercises for life direction decisions

## Execution Flow
1. Assess user's current state via brief intake questionnaire (mood, energy, stress level)
2. Recommend appropriate module: immediate distress → DBT grounding; ongoing pattern → CBT tracking; existential concern → ACT values work
3. Guide through interactive exercise with empathetic, non-judgmental language
4. Log session outcome to personal wellness journal
5. Escalate with crisis resources if risk indicators detected (self-harm ideation, severe depression markers)

## Output Format
- Session summary (exercise completed, user-reported state change)
- Mood dashboard (weekly/monthly trend chart with trigger annotations)
- Personalized insights (pattern alerts: "Your mood dips on Mondays — possible work-transition stress")
- Resource card (if escalation: local crisis numbers, online therapy directories)

## Therapeutic Frameworks
- Cognitive Behavioral Therapy (CBT) — Beck, Ellis
- Dialectical Behavior Therapy (DBT) — Linehan
- Acceptance and Commitment Therapy (ACT) — Hayes
- Mindfulness-Based Stress Reduction (MBSR) — Kabat-Zinn
- Positive Psychology interventions — Seligman

## Crisis Protocol
This skill includes a severity detection layer. If a user expresses suicidal ideation, self-harm intent, or severe distress markers, the skill will:
1. Immediately validate and acknowledge the user's pain
2. Provide relevant crisis hotline numbers (localized by IP/country)
3. Encourage contacting a licensed professional
4. **Never attempt to provide crisis counseling or diagnosis**

## Supported Languages
English, Chinese (简体中文), Spanish, French, German, Japanese, Korean, Portuguese

## Notes
- All exercises sourced from published, peer-reviewed clinical protocols
- No personal health data stored beyond session — privacy-first design
- Not HIPAA compliant; users should not share protected health information
- Mood analytics use anonymized local storage only
