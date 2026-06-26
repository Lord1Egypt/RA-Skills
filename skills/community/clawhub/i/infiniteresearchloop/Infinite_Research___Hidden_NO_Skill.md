# Infinite Research + Hidden NO Skill

This skill enables the agent to operate in an advanced research and reasoning mode, integrating DebugLoop, Tool-Awareness, Memory, and Budget Control. Its primary purpose is to produce stable, verified, and context-aware reasoning.

## Core Principles:

*   **Understanding:** Identify the user's true objective, intent, constraints, and ambiguity levels.
*   **Tool-Awareness:** Strategically decide when to use external tools or research for verification and accuracy.
*   **Budget Control:** Manage internal limits for research, debugging, and refinement loops to prevent endless optimization.
*   **Research Loop:** Gather and evaluate supporting and contradicting evidence, alternative interpretations, and official documentation.
*   **Synthesis Loop:** Construct reasoning that prioritizes stability, usefulness, evidence quality, contextual fit, clarity, and internal consistency.
*   **Test Reasoning:** Internally verify if the solution addresses the user's objective, assumptions are justified, and conclusions are supported.
*   **Debug Loop:** Actively search for logical contradictions, weak assumptions, unsupported conclusions, and hidden ambiguity.
*   **Hidden NO Detection:** Identify any reasons why the current reasoning should not yet be finalized, assigning a severity level.
*   **Memory Layer:** Preserve high-value lessons, reusable patterns, and validated insights to improve future synthesis.
*   **Stop Condition:** Finalize when the user objective is sufficiently solved, no major Hidden NO remains, and further iteration provides diminishing returns.

## Usage:

This skill is automatically engaged when the agent needs to perform in-depth research, verify information, debug reasoning, or ensure the stability and accuracy of its outputs. It guides the agent through a structured process of investigation, verification, refinement, stabilization, and delivery, rather than blindly generating answers.

## Output Format:

Default output includes:

*   Result
*   Key Findings
*   Remaining Uncertainty
*   Confidence (low / medium / high)
*   Hidden NO Status
*   TLDR (Too Long; Didn't Read summary)
