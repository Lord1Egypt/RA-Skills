---
name: nexus-clinical-case-gen
description: Medical clinical case generator for education with PubMed RAG and OSCE
  evaluations.
version: '2.1.0'
metadata:
  openclaw:
    emoji: 🏥
    homepage: https://github.com/Shuwanito/SkillsMP/tree/main/.claude/skills/nexus-clinical-case-gen
    os:
    - macos
    - linux
    - windows
---

# Nexus Clinical Case Gen

## Capabilities
- Clinical case generation
- Differential diagnosis
- OSCE scenario creation
- PubMed RAG integration
- Competency tracking

## Workflow
1. Receive task description and target context
2. Analyze using department-specific engines (healthcare)
3. Generate findings with severity classification
4. Produce improvement proposals with impact/effort scoring
5. Cross-validate with synergy departments
6. Return structured results with confidence scores

## Pricing
- Per-execution: $5.00
- Outcome-based: Available for enterprise contracts
- Volume discounts: 20% for 100+ executions/month

## Guidelines
- All outputs include confidence scores and source citations
- Cross-validation requires minimum 2 independent sources
- Findings are classified: CRITICAL, HIGH, MEDIUM, LOW, INFO
- Proposals include impact (1-10), effort (1-10), and priority score