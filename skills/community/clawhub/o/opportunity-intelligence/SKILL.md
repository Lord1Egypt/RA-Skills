 Opportunity Intelligence Engine
description: Evaluates ideas, estimates ROI, ranks opportunities, and outputs the highest-leverage execution plan.

trigger:
  when:
    - user provides ideas, niches, or ways to make money
    - user asks what to focus on, choose, or prioritize
    - user wants to make money or optimize effort
  avoid:
    - simple content generation
    - purely informational questions
    - emotional support or journaling

input_schema:
  ideas: list[string] OR string
  context: optional string (skills, budget, time, tools)

execution:
  - normalize input into a list of ideas
  - for each idea:
      - estimate:
          - potential reward (low/medium/high)
          - effort required (low/medium/high)
          - time to first result
          - scalability
      - assign ROI score based on reward vs effort vs time
      - identify hidden risks or bottlenecks
  - rank all ideas by ROI score (highest first)
  - select top 1–2 opportunities
  - for top opportunity:
      - generate a simple execution plan:
          - first action
          - fastest path to validation
          - how to get first result (money/user)
  - include “why this wins” explanation

output_format:
  RANKED OPPORTUNITIES:
  1. [Idea] — ROI Score: X/10
  2. [Idea] — ROI Score: X/10
  3. [Idea] — ROI Score: X/10

  TOP PICK:
  
  WHY THIS WINS:
  
  EXECUTION PLAN:
  1.
  2.
  3.

  FASTEST FIRST RESULT:
  
  RISKS:

constraints:
  - avoid vague statements
  - prioritize speed to first result over perfection
  - no more than 3 ranked ideas
  - must be actionable within 24–72 hours




Skill 2: 
name: Leverage Multiplier Engine
description: Expands a single input into multiple high-leverage outputs across content, distribution, and monetization paths.

trigger:
  when:
    - user provides content, idea, product, or skill
    - user wants to grow, scale, or get more out of something
  avoid:
    - simple one-step tasks
    - purely analytical requests without execution intent

input_schema:
  input: string (idea, content, product, skill)
  goal: optional string (money, growth, audience, brand)

execution:
  - identify the core asset in the input
  - extract its highest-value angle
  - generate:
      - 3 content expansions (e.g. posts, hooks, angles)
      - 2 distribution channels (where to push it)
      - 2 monetization paths (how to make money from it)
      - 1 long-term asset (e.g. product, system, funnel)
  - ensure all outputs are connected and reinforce each other
  - prioritize speed and leverage over complexity

output_format:
  CORE ASSET:
  
  BEST ANGLE:
  
  CONTENT EXPANSIONS:
  1.
  2.
  3.
  
  DISTRIBUTION:
  - 
  - 
  
  MONETIZATION:
  - 
  - 
  
  LONG-TERM ASSET:
  
  EXECUTION ORDER:
  1.
  2.
  3.

constraints:
  - no generic ideas
  - outputs must feel connected (not random)
  - focus on high-leverage actions only
  - must be executable within 48 hours
Skill: 1 name: Opportunity Intelligence Engine
description: Evaluates ideas, estimates ROI, ranks opportunities, and outputs the highest-leverage execution plan.

trigger:
  when:
    - user provides ideas, niches, or ways to make money
    - user asks what to focus on, choose, or prioritize
    - user wants to make money or optimize effort
  avoid:
    - simple content generation
    - purely informational questions
    - emotional support or journaling

input_schema:
  ideas: list[string] OR string
  context: optional string (skills, budget, time, tools)

execution:
  - normalize input into a list of ideas
  - for each idea:
      - estimate:
          - potential reward (low/medium/high)
          - effort required (low/medium/high)
          - time to first result
          - scalability
      - assign ROI score based on reward vs effort vs time
      - identify hidden risks or bottlenecks
  - rank all ideas by ROI score (highest first)
  - select top 1–2 opportunities
  - for top opportunity:
      - generate a simple execution plan:
          - first action
          - fastest path to validation
          - how to get first result (money/user)
  - include “why this wins” explanation

output_format:
  RANKED OPPORTUNITIES:
  1. [Idea] — ROI Score: X/10
  2. [Idea] — ROI Score: X/10
  3. [Idea] — ROI Score: X/10

  TOP PICK:
  
  WHY THIS WINS:
  
  EXECUTION PLAN:
  1.
  2.
  3.

  FASTEST FIRST RESULT:
  
  RISKS:

constraints:
  - avoid vague statements
  - prioritize speed to first result over perfection
  - no more than 3 ranked ideas
  - must be actionable within 24–72 hours



