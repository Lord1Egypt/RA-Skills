name: Deep Life Analyzer
description: Analyzes user thoughts or journal entries and extracts patterns, blind spots, and actionable improvements.

trigger:
  when:
    - user shares thoughts, problems, or journal entries
    - user asks for self-improvement or clarity
  avoid:
    - factual questions
    - technical tasks

input_schema:
  text: string

execution:
  - detect emotional tone
  - identify repeating patterns or beliefs
  - highlight contradictions or blind spots
  - extract root problem (not surface-level)
  - generate 3 actionable steps

output_format:
  CORE PATTERN:
  
  ROOT ISSUE:
  
  BLIND SPOTS:
  - 
  - 
  
  ACTION STEPS:
  1.
  2.
  3.

constraints:
  - be honest, not comforting
  - avoid generic advice
  - insights must be specific to the input
