---
name: iq
version: 1.0.0
description: "Generate IQ tests, brain teasers, logical puzzles, riddles, and cognitive training challenges. Use when: user wants to test their intelligence quotient, solve logical reasoning problems, practice mental math, generate brain training exercises, create interactive intelligence quizzes, work on spatial reasoning, pattern recognition, or memory challenges. Also use when user asks for riddles, brain teasers, cognitive assessments, or wants to challenge their mind with puzzles."
---

# IQ Skill

Generate IQ tests, brain teasers, logical puzzles, riddles, and cognitive training challenges. This skill provides tools to create interactive intelligence assessments, daily mental challenges, and brain-training games.

## Overview

This skill enables the generation of comprehensive IQ-related content including:

- Multi-dimensional IQ test questions (logical reasoning, mathematical sequences, pattern recognition, spatial visualization, memory, verbal ability)
- Daily intelligence challenges with progressive difficulty
- Brain-training games (Sudoku, Tower of Hanoi, number puzzles, sliding puzzles)
- Beautiful interactive HTML-based IQ test interfaces
- Performance analysis and cognitive improvement suggestions

## When to Use This Skill

- User wants to test their IQ or create an IQ test for others
- User asks for brain teasers, riddles, or logical puzzles
- User wants daily mental challenges or cognitive exercises
- User needs to generate brain-training games or puzzles
- User requests pattern recognition or sequence problems
- User wants spatial reasoning or visual intelligence challenges
- User asks for memory tests or concentration exercises
- User wants to create an interactive quiz or assessment
- User requests mental math challenges or numerical reasoning problems

## Quick Start

To generate IQ-related content, determine the user's intent and use the appropriate workflow below.

### Decision Tree

1. Does the user want a **full IQ test**? → Use [Generate IQ Test](#generate-iq-test)
2. Does the user want a **single challenge or riddle**? → Use [Daily Challenge](#daily-challenge)
3. Does the user want a **brain-training game**? → Use [Brain Games](#brain-games)
4. Does the user want an **interactive HTML interface**? → Use [Interactive Test Builder](#interactive-test-builder)
5. Does the user want **analysis or feedback** on their performance? → Use [Performance Analysis](#performance-analysis)

## Generate IQ Test

Generate a comprehensive IQ test with multiple question categories.

### Steps

1. Determine the desired test parameters:
   - Number of questions (default: 20)
   - Categories to include (default: all)
   - Difficulty level (Easy / Medium / Hard / Mixed)
   - Output format (Plain text / Markdown / Interactive HTML)

2. Generate questions using `scripts/iq_test_generator.py` or craft them manually using the reference question bank.

3. Include these question categories for a balanced test:
   - **Logical Reasoning**: Deductive and inductive logic problems
   - **Mathematical Sequences**: Number patterns, series completion
   - **Pattern Recognition**: Visual and abstract pattern identification
   - **Spatial Visualization**: 3D rotation, folding, assembly problems
   - **Verbal Reasoning**: Analogies, classifications, comprehension
   - **Memory & Attention**: Recall and concentration challenges

4. Provide an answer key with explanations.

### Example Request

- "Generate a 15-question IQ test with medium difficulty"
- "Create a hard logic puzzle test for me"
- "I want a spatial reasoning assessment"

## Daily Challenge

Generate a single daily intelligence challenge.

### Steps

1. Use `scripts/daily_challenge.py` to generate a challenge, or create one manually.
2. Rotate through categories daily for variety:
   - Monday: Logical Reasoning
   - Tuesday: Mathematical
   - Wednesday: Pattern Recognition
   - Thursday: Spatial Visualization
   - Friday: Verbal Reasoning
   - Saturday: Memory Challenge
   - Sunday: Mixed / Riddle
3. Include the answer with a detailed explanation.

### Example Request

- "Give me today's brain challenge"
- "I need a difficult riddle"
- "Show me a pattern puzzle"

## Brain Games

Generate playable brain-training games.

### Steps

1. Identify the game type the user wants:
   - **Sudoku**: Number-placement puzzle (9x9 grid)
   - **Tower of Hanoi**: Classic disk-moving puzzle
   - **Number Puzzle**: Magic squares, arithmetic crosswords
   - **Sliding Puzzle**: 15-puzzle or custom grid
   - **Logic Grid**: Einstein's riddle style deduction puzzles

2. Use `scripts/brain_games.py` to generate the game, or create manually.
3. Provide rules, the puzzle, and the solution.

### Example Request

- "Generate a Sudoku puzzle for me"
- "Create a Tower of Hanoi challenge with 5 disks"
- "I want a logic grid puzzle"

## Interactive Test Builder

Create a beautiful, interactive HTML-based IQ test that users can take in a browser.

### Steps

1. Generate test questions using the IQ Test workflow.
2. Use the template in `assets/iq_test_template.html` as the foundation.
3. Inject questions into the template:
   - Replace `{{TEST_TITLE}}` with the test title
   - Replace `{{QUESTIONS_JSON}}` with a JSON array of questions
   - Replace `{{TIME_LIMIT}}` with time limit in minutes (optional)
4. Customize styling if requested (colors, fonts, layout).
5. Save the final HTML file and provide it to the user.

### Template Features

- Clean, responsive design
- Timer functionality
- Multiple choice and text input support
- Automatic scoring
- Result breakdown by category
- Progress tracking

## Performance Analysis

Analyze test results and provide feedback.

### Steps

1. Collect the user's answers and scores by category.
2. Calculate approximate IQ range based on performance (for reference only, not clinical).
3. Identify strongest and weakest categories.
4. Provide personalized improvement suggestions:
   - Recommended brain-training exercises
   - Category-specific practice tips
   - Recommended difficulty progression

### Analysis Categories

| Score Range | Approximate Level | Recommendation |
|-------------|-------------------|----------------|
| 90-100%     | Excellent         | Try harder challenges |
| 70-89%      | Good              | Maintain with varied practice |
| 50-69%      | Average           | Focus on weak categories |
| Below 50%   | Developing        | Start with easier puzzles |

## Resources

### scripts/

- **`iq_test_generator.py`**: Generates IQ test questions across multiple categories. Supports customizable question count, difficulty, and category selection. Outputs questions in structured format.
- **`daily_challenge.py`**: Generates a single daily challenge with category rotation. Includes answer and explanation.
- **`brain_games.py`**: Generates brain-training games including Sudoku, Tower of Hanoi, number puzzles, and sliding puzzles.

### references/

- **`question_bank.md`**: Comprehensive reference of IQ question patterns, examples by category, difficulty guidelines, and scoring methodologies. Load this when creating custom questions or needing detailed category information.

### assets/

- **`iq_test_template.html`**: A beautiful, interactive HTML template for IQ tests. Features responsive design, timer, automatic scoring, category breakdown, and progress tracking. Copy and customize for each test.

## Tips for Best Results

- Always include answers and explanations — learning from mistakes is key to improvement
- Mix difficulty levels to keep users engaged and accurately assess ability
- For interactive tests, ensure the HTML template is properly customized with the generated questions
- When generating games, verify solutions programmatically when possible
- Encourage users to time themselves for a more realistic assessment
- Rotate categories regularly to ensure well-rounded cognitive training
