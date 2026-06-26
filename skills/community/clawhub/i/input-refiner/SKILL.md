name: input-refiner
description: Rewrite vague, rough, or lengthy user input into a clear, structured, and execution-friendly form based on conversation context.
version: 2026.3.26
metadata:
  openclaw:
    emoji: "🪄"
---

# Input Refiner

## Overview
Use this skill when the user's input is vague, rough, overly colloquial, incomplete, poorly structured, or excessively long.

This skill rewrites the user's original input into a clearer, more structured, and more execution-friendly form while preserving the original intent.

When the user's input contains many points, mixed ideas, or long descriptions, the rewritten result should be organized into ordered bullet points based on importance and execution priority, instead of being compressed into a single paragraph.

The goal is to improve the input itself, not to invent new requirements or rename things.

## When to use
Use this skill when the user says things like:
- "Please help organize this input."
- "My wording is too rough. Please rewrite it."
- "Make this sentence clearer."
- "Improve this input so the downstream model can understand it better."
- "My description is messy. Please turn it into a clearer version."
- "Rewrite the user's input into a more complete expression."
- "This paragraph is too long. Please break it down clearly."
- "Organize these requirements by priority."

## Do not use
Do not use this skill to:
- invent new requirements not supported by context
- expand a short request into a full product spec
- change the user's underlying goal
- add important constraints that were never mentioned
- generate names or titles as the main objective

## Inputs to collect
Collect from the conversation:
- the user's original input
- nearby context that helps clarify intent
- the likely target format if implied:
  - task instruction
  - feature request
  - prompt
  - document request
  - execution command
- language preference from the conversation

If some details are missing, only infer what is strongly supported by context.

## Working method
Follow these steps:

1. Identify the core intent
   - What is the user trying to achieve?
   - What is the main object or topic?
   - What result is expected?
   - What context is already available?

2. Remove noise
   - Remove filler words, repetition, vague phrasing, and purely conversational wording.

3. Extract key points
   - Identify major goals
   - Identify supporting requirements
   - Identify constraints
   - Identify expected outputs
   - Identify optional or lower-priority details

4. Rebuild structure
   Rewrite the input into a clearer structure, such as:
   - goal
   - object
   - action
   - constraints
   - expected result

5. Order by importance
   If the original input is long, mixed, or multi-part:
   - break the rewritten content into bullet points
   - order items by importance or execution priority
   - put the main goal first
   - place constraints and secondary details after the core task
   - keep optional ideas at the end

6. Preserve intent
   Keep the original meaning unchanged.
   Improve clarity, not scope.

7. Produce rewritten input
   Return one primary rewritten version and one to three alternative versions if useful.

## Rewriting principles
- Preserve the user's original intent.
- Prefer clarity over style.
- Prefer structure over verbosity.
- Use context, but do not hallucinate missing facts.
- Make the rewritten input easier for an agent, model, or collaborator to act on.
- Do not over-expand the request.
- Do not turn a simple request into a detailed specification unless the context clearly supports it.
- When the input contains multiple ideas, separate them rather than merging everything into one sentence.
- When the input is long, present the refined result as an ordered list by priority.
- Distinguish between core requirements and secondary details.
- Never flatten long multi-point input into one paragraph when priority ordering would improve clarity.

## Output format
Return exactly this structure:

Intent:
<one-sentence summary of the user's true intent>

Refined Input:
<the rewritten version of the user's input>

If the input is short and focused:
<write one clear rewritten paragraph or instruction>

If the input is long or contains multiple points:
1. <highest-priority requirement or main goal>
2. <second most important requirement>
3. <next important constraint, action, or expected result>
4. <secondary detail if needed>
5. <optional or lower-priority detail if needed>

Alternative Versions:
- <alternative 1>
- <alternative 2>
- <alternative 3>

Why:
<short explanation of what was improved, including whether the content was reorganized by priority>

## Examples

### Example 1
User:
"Please organize this input. It is too rough right now and not easy to use for the next step."

Output:
Intent:
Make the rough input clearer and easier to use for the next step.

Refined Input:
Please rewrite the current rough input into a clearer, more structured, and execution-friendly version while preserving the original intent.

Alternative Versions:
- Please refine the current input so it is easier to understand and act on.
- Rewrite the user's rough input into a more explicit and structured instruction.
- Turn the current vague input into a clearer and more usable request.

Why:
The rewritten versions remove conversational vagueness and make the task easier for a downstream agent or collaborator to follow.

### Example 2
User:
"The user's message is too messy. Please rewrite it into a version that is easier for the next model to understand."

Output:
Intent:
Rewrite a messy user message into a version that is easier for a model to understand.

Refined Input:
Please rewrite the user's original message into a clearer, more structured, and model-friendly form without changing its meaning.

Alternative Versions:
- Convert the user's messy input into a clearer prompt for downstream model processing.
- Rewrite the original user message into a structured and unambiguous instruction.
- Make the user's input easier for the next model to interpret accurately.

Why:
The rewritten input keeps the original meaning but improves clarity, structure, and downstream usability.

### Example 3
User:
"I want to build an AI tool where the user types one sentence, the system first figures out what they mean, then cleans up the unclear parts, outputs something more explicit, and if there are many points it should list them in order so another model can continue processing afterward."

Output:
Intent:
Turn a rough product idea into a clear and structured execution-oriented input for downstream processing.

Refined Input:
1. Build an AI tool that analyzes the user's original input and identifies the intended meaning.
2. Rewrite vague or unclear parts into a clearer and more explicit form while preserving the original intent.
3. Structure the rewritten result so it is easier for downstream models or agents to process.
4. If the content contains multiple points, organize it into ordered items based on importance or execution priority.
5. Keep the final output clear, concise, and suitable for further automated handling.

Alternative Versions:
- Create a system that clarifies vague user input and outputs a structured, model-friendly version.
- Build an input-refinement tool that rewrites unclear user requests into prioritized, actionable instructions.
- Develop a rewriting layer that transforms rough user input into a clear and ordered format for downstream AI processing.

Why:
The original input contained several mixed ideas in one sentence. The refined version separates the core objective, rewriting behavior, structural requirement, and output priority into an ordered format that is easier to execute.