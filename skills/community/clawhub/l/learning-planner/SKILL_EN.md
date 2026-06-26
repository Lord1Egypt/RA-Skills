---
name: learning-planner
description: "Personal learning management system with goal setting, spaced repetition scheduling, and progress tracking. Use when: (1) setting learning goals and skill trees, (2) creating daily/weekly study plans, (3) tracking learning progress, (4) managing spaced repetition reviews like Anki, (5) organizing learning resources, (6) evaluating learning outcomes."
---

# Learning Planner

A personal learning management system for setting goals, creating study plans, tracking progress, and implementing spaced repetition reviews.

## Description

Learning Planner is your personal learning companion that helps you structure your educational journey. It provides skill tree management for breaking down complex topics, automated study plan generation, progress visualization, and a built-in spaced repetition system based on the SM-2 algorithm. Whether you're learning a new programming language, preparing for certifications, or building knowledge in any domain, this skill keeps you organized and on track.

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
# Create a learning goal
learning goal create "Python Programming" --description "Master Python programming language" --deadline 2024-12-31

# Create sub-goals (knowledge breakdown)
learning goal create "Python Basics" --parent 1 --priority high
learning goal create "Python OOP" --parent 1 --priority high
learning goal create "Python Advanced Features" --parent 1 --priority medium

# List all goals
learning goal list

# Show goal details
learning goal show 1

# Update goal progress
learning goal progress 1 --percent 75

# Mark goal as completed
learning goal complete 1
```

### Study Plans

```bash
# Generate today's study plan
learning plan today

# Generate weekly study plan
learning plan week

# View all plans
learning plan list

# Mark task as completed
learning plan complete 1

# Postpone a task
learning plan postpone 1 --days 1
```

### Spaced Repetition Reviews

```bash
# Create a review card
learning card create "Python list comprehension syntax" --answer "[x for x in iterable if condition]" --tags python,basics

# Start today's review session
learning review today

# View review statistics
learning review stats

# Manually adjust card difficulty
learning card difficulty 1 --level hard
```

### Learning Resources

```bash
# Add a resource
learning resource add "Python Official Docs" --url https://docs.python.org --type documentation --tags python

# Link resource to a goal
learning resource link 1 --goal 1

# List all resources
learning resource list

# Search resources
learning resource search python
```

### Progress & Reports

```bash
# View learning statistics
learning stats

# Generate learning report
learning report --days 30

# View skill tree progress
learning tree

# View study time statistics
learning time --days 7
```

## Features

### Goal Management
- Skill tree definition and decomposition
- Knowledge point hierarchy
- Priority settings
- Deadline planning

### Study Plan Generation
- Daily study task generation
- Weekly study plans
- Automatic plan adjustment
- Study reminders

### Progress Tracking & Visualization
- Real-time progress tracking
- Progress visualization charts
- Study time statistics
- Completion rate analysis

### Spaced Repetition System
- SM-2 algorithm implementation
- Card-based review
- Automatic scheduling
- Forgetting curve optimization

### Resource Management
- Resource link collection
- Resource categorization
- Resource-goal association
- Resource usage statistics

### Learning Assessment
- Self-assessment records
- Test score management
- Learning effect analysis
- Skill growth curves

## Configuration

Database location: `~/.config/learning-planner/learning.db`

```bash
# View database path
learning data path
```

## Examples

### Scenario 1: Learning a New Programming Language

```bash
# Create main goal
learning goal create "JavaScript Mastery" --description "Become proficient in JavaScript" --deadline 2024-12-31

# Break down into sub-goals
learning goal create "JavaScript Basics" --parent 1 --priority high --estimated-hours 20
learning goal create "DOM Manipulation" --parent 1 --priority high --estimated-hours 15
learning goal create "Async Programming" --parent 1 --priority medium --estimated-hours 10
learning goal create "Node.js Basics" --parent 1 --priority medium --estimated-hours 15

# Add resources
learning resource add "MDN JavaScript Guide" --url https://developer.mozilla.org/en-US/docs/Web/JavaScript --type documentation --tags js,basics
learning resource link 1 --goal 2

# Create review cards
learning card create "Difference between let and const" --answer "let is reassignable, const creates a read-only reference" --tags js,basics

# Start learning
learning plan today
```

### Scenario 2: Daily Study Routine

```bash
# Check today's plan
learning plan today

# Complete a task
learning plan complete 1

# Log study time (manually or integrated)
# ... study session ...

# Do review cards
learning review today

# Check progress
learning stats
```

### Scenario 3: Preparing for Certification

```bash
# Create certification goal
learning goal create "AWS Solutions Architect" --description "Pass AWS SAA-C03 exam" --deadline 2024-06-30

# Add knowledge areas
learning goal create "EC2 & Compute" --parent 1 --priority high
learning goal create "S3 & Storage" --parent 1 --priority high
learning goal create "VPC & Networking" --parent 1 --priority high
learning goal create "IAM & Security" --parent 1 --priority high

# Add resources
learning resource add "AWS Whitepapers" --url https://aws.amazon.com/whitepapers --type documentation --tags aws,exam

# Create flashcards
learning card create "What is S3 Standard-IA?" --answer "Infrequent Access storage class for data accessed less frequently" --tags aws,s3

# Generate weekly plan
learning plan week
```

### Scenario 4: Progress Review

```bash
# Generate 30-day report
learning report --days 30

# View skill tree progress
learning tree

# Check study time
learning time --days 7

# View review statistics
learning review stats
```

## Technical Details

### Technology Stack
- **Python 3.8+**
- **SQLite** - Local database storage
- **Click** - CLI framework
- **Rich** - Terminal formatting
- **SM-2 Algorithm** - Spaced repetition scheduling

### Data Models

#### Goals Table
```python
{
    id: int
    title: str              # Goal name
    description: str        # Description
    parent_id: int          # Parent goal ID
    priority: str           # Priority: low, medium, high
    status: str             # Status: active, completed, paused
    progress: float         # Progress 0-100
    deadline: str           # Deadline date
    estimated_hours: int    # Estimated study hours
    completed_hours: int    # Completed hours
    created_at: str
    updated_at: str
}
```

#### Plans Table
```python
{
    id: int
    goal_id: int            # Associated goal
    title: str              # Task title
    description: str        # Description
    scheduled_date: str     # Planned date
    estimated_minutes: int  # Estimated duration (minutes)
    status: str             # Status: pending, completed, postponed
    completed_at: str       # Completion time
    created_at: str
}
```

#### Cards Table
```python
{
    id: int
    goal_id: int            # Associated goal
    front: str              # Card front (question)
    back: str                # Card back (answer)
    tags: str               # Tags
    ease_factor: float      # Difficulty factor
    interval: int           # Interval in days
    repetitions: int        # Repetition count
    next_review: str        # Next review date
    last_review: str        # Last review date
    created_at: str
}
```

#### Reviews Table
```python
{
    id: int
    card_id: int            # Card ID
    quality: int            # Score 0-5
    reviewed_at: str        # Review time
    time_spent: int         # Time spent (seconds)
}
```

#### Resources Table
```python
{
    id: int
    title: str              # Resource name
    url: str                # Link
    resource_type: str      # Type: video, article, book, documentation
    tags: str               # Tags
    goal_id: int            # Associated goal
    notes: str              # Notes
    created_at: str
}
```

#### Sessions Table
```python
{
    id: int
    goal_id: int            # Associated goal
    start_time: str         # Start time
    end_time: str           # End time
    duration: int           # Duration (minutes)
    notes: str              # Notes
}
```

### SM-2 Algorithm Details

The spaced repetition system is based on the SuperMemo-2 algorithm:

**Quality Score (0-5):**
- 5: Perfect response
- 4: Correct after hesitation
- 3: Correct but difficult
- 2: Incorrect, but recognized
- 1: Incorrect, some recall
- 0: Complete blackout

**Ease Factor (EF):**
- Initial value: 2.5
- Range: 1.3 - 2.5
- Update formula: EF' = EF + (0.1 - (5-q) × (0.08 + (5-q) × 0.02))

**Interval Calculation:**
- 1st repetition: 1 day
- 2nd repetition: 6 days
- nth repetition: previous interval × EF

The algorithm automatically adjusts intervals based on your performance, ensuring optimal review timing for long-term retention.

## License

Part of the OpenClaw skills ecosystem.