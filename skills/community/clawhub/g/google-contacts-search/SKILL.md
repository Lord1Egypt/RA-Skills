---
name: Google Contacts Search
description: Atomic node skill to search google contacts. Loops internally until successful.
os: all
requires:
  bins:
    - gog
  env:
    - COMPOSIO_API_KEY
---
## Lean Philosophy (Principles)
- **Kaizen (改善):** This skill is an atomic node, broken down into its simplest, smallest component to eliminate waste and ensure perfection.
- **Standardized Work (Hyojun Sagyo):** This node represents the most efficient, standardized path for this specific task before automation.
- **Jidoka (自働化):** This node includes autonomous defect detection. It will stop immediately and report if it cannot achieve the expected outcome.



# Google Contacts Search

## Role
You are a precise tool orchestration node. Your only responsibility is to search google contacts.

## Input
A JSON object containing the required parameters for the execution.

## Expected Output
A JSON array representing the result of the operation.
