---
name: learning-planner
description: "Personal learning management system with goal setting, spaced repetition scheduling, and progress tracking. Use when: (1) setting learning goals and skill trees, (2) creating daily/weekly study plans, (3) tracking learning progress, (4) managing spaced repetition reviews like Anki, (5) organizing learning resources, (6) evaluating learning outcomes."
---

# Learning Planner

Personal learning management system that helps set learning goals, create plans, track progress, and provides spaced repetition review features.

## Features

### 1. Learning Goal Management
- Skill tree definition and breakdown
- Knowledge point hierarchy management
- Goal priority settings
- Goal completion time planning

### 2. Learning Plan Generation
- Daily learning task generation
- Weekly learning plans
- Automatic plan adjustment
- Learning reminder settings

### 3. Progress Tracking and Visualization
- Real-time learning progress tracking
- Progress visualization charts
- Learning time statistics
- Completion rate analysis

### 4. Spaced Repetition Review System
- SM-2 algorithm implementation
- Flashcard-based review
- Automatic scheduling
- Forgetting curve optimization

### 5. Learning Resource Management
- Resource link bookmarking
- Resource categorization
- Resource to knowledge point mapping
- Resource usage statistics

### 6. Learning Outcome Evaluation
- Self-assessment records
- Test score management
- Learning effectiveness analysis
- Ability growth curves

## Installation

```bash
cd ~/.openclaw/workspace/skills/learning-planner
pip install -e .

# Add to PATH (optional)
ln -s ~/.openclaw/workspace/skills/learning-planner/src/learning_cli.py ~/.local/bin/learning
```

## Usage

### Learning Goals

```bash
# Create learning goal
learning goal create "Python Programming" --description "Master Python programming language" --deadline 2024-12-31

# Create sub-goals (knowledge point breakdown)
learning goal create "Python Basic Syntax" --parent 1 --priority high
learning goal create "Python OOP" --parent 1 --priority high
learning goal create "Python Advanced Features" --parent 1 --priority medium

# List goals
learning goal list

# View goal details
learning goal show 1

# Update goal progress
learning goal progress 1 --percent 75

# Complete goal
learning goal complete 1
```

### Learning Plans

```bash
# Generate today's learning plan
learning plan today

# Generate this week's learning plan
learning plan week

# View plans
learning plan list

# Mark task complete
learning plan complete 1

# Postpone task
learning plan postpone 1 --days 1
```

### Spaced Repetition Review

```bash
# Create review card
learning card create "Python list comprehension syntax" --answer "[x for x in iterable if condition]" --tags python,basics

# Today's review
learning review today

# View review statistics
learning review stats

# Manually adjust card difficulty
learning card difficulty 1 --level hard
```

### Learning Resources

```bash
# Add resource
learning resource add "Python Official Documentation" --url https://docs.python.org --type documentation --tags python

# Link resource to goal
learning resource link 1 --goal 1

# List resources
learning resource list

# Search resources
learning resource search python
```

### Progress and Reports

```bash
# Learning statistics
learning stats

# Generate learning report
learning report --days 30

# View skill tree progress
learning tree

# Learning time statistics
learning time --days 7
```

## Data Storage

Database location: `~/.config/learning-planner/learning.db`

```bash
# View database path
learning data path
```

## Tech Stack

- Python 3.8+
- SQLite data storage
- Click (CLI framework)
- Rich (terminal styling)
- SM-2 spaced repetition algorithm

## Data Models

### Learning Goals Table (goals)
```python
{
    id: int
    title: str              # Goal name
    description: str        # Description
    parent_id: int          # Parent goal ID
    priority: str           # Priority: low, medium, high
    status: str             # Status: active, completed, paused
    progress: float         # Progress 0-100
    deadline: str           # Deadline
    estimated_hours: int    # Estimated study hours
    completed_hours: int    # Completed hours
    created_at: str
    updated_at: str
}
```

### Learning Plans Table (plans)
```python
{
    id: int
    goal_id: int            # Related goal
    title: str              # Task title
    description: str        # Description
    scheduled_date: str     # Planned date
    estimated_minutes: int  # Estimated duration (minutes)
    status: str             # Status: pending, completed, postponed
    completed_at: str       # Completion time
    created_at: str
}
```

### Review Cards Table (cards)
```python
{
    id: int
    goal_id: int            # Related goal
    front: str              # Card front (question)
    back: str                # Card back (answer)
    tags: str               # Tags
    ease_factor: float      # Difficulty factor
    interval: int           # Interval days
    repetitions: int        # Repetition count
    next_review: str        # Next review time
    last_review: str        # Last review time
    created_at: str
}
```

### Review Records Table (reviews)
```python
{
    id: int
    card_id: int            # Card ID
    quality: int            # Rating 0-5
    reviewed_at: str        # Review time
    time_spent: int         # Time spent (seconds)
}
```

### Learning Resources Table (resources)
```python
{
    id: int
    title: str              # Resource name
    url: str                # Link
    resource_type: str      # Type: video, article, book, documentation
    tags: str               # Tags
    goal_id: int            # Related goal
    notes: str              # Notes
    created_at: str
}
```

### Learning Sessions Table (sessions)
```python
{
    id: int
    goal_id: int            # Related goal
    start_time: str         # Start time
    end_time: str           # End time
    duration: int           # Duration (minutes)
    notes: str              # Notes
}
```

## SM-2 Algorithm Explanation

Spaced repetition algorithm based on SuperMemo-2:

1. **Quality Rating**: 0-5 points
   - 5: Perfect response
   - 4: Correct response, hesitated
   - 3: Correct response, difficult
   - 2: Incorrect, close to correct
   - 1: Incorrect, remembered some
   - 0: Completely forgot

2. **Ease Factor (EF)**: Initial 2.5, range 1.3-2.5
   - EF' = EF + (0.1 - (5-q) * (0.08 + (5-q) * 0.02))

3. **Interval Days**:
   - First: 1 day
   - Second: 6 days
   - Nth: Previous interval * EF