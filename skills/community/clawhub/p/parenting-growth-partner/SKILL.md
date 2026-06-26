# Parenting Growth Partner / 育儿成长伙伴

## Overview

Parenting Growth Partner is an AI-powered companion for parents and caregivers, providing evidence-based guidance on child development, positive parenting techniques, and age-appropriate activities. The skill helps parents navigate the challenges of raising children from infancy through preschool years.

育儿成长伙伴是一个为父母和照顾者提供基于科学证据的育儿指导的AI伴侣，涵盖儿童发展里程碑、正向管教技巧和适龄活动推荐。帮助父母应对从婴儿期到学龄前儿童的育儿挑战。

## Core Features

### 1. Child Development Milestone Tracking
- Assess developmental milestones across 6 domains: gross motor, fine motor, language, cognitive, social-emotional, adaptive
- Identify potential red flags based on age
- Generate personalized recommendations

### 2. Age-Appropriate Activity Recommendations
- Recommend developmentally appropriate activities
- Filter by available time and preferred developmental domains
- Include safety notes and step-by-step instructions

### 3. Positive Communication Guidance
- Provide evidence-based techniques for common parenting scenarios
- Offer age-appropriate communication scripts
- Help prevent common communication mistakes

### 4. Behavior Analysis & Positive Discipline
- Analyze behavior patterns and underlying causes
- Recommend positive discipline techniques
- Create customized behavior intervention plans

### 5. Daily Routine Suggestions
- Suggest age-appropriate daily schedules
- Provide tips for establishing healthy routines
- Offer flexibility guidelines

## Input/Output

### Input Parameters
```json
{
  "action": "milestone_assessment|activity_recommendation|communication_guidance|behavior_analysis|daily_routine",
  "params": {
    "age_months": 24,
    "observations": {"gross-motor": ["walks well", "can climb stairs"]},
    "available_time": 30,
    "preferred_domains": ["cognitive", "fine-motor"],
    "scenario": "tantrum|refusal|sharing|bedtime",
    "behavior_description": "经常说'不'，拖延",
    "frequency": "occasional|frequent|constant",
    "context": "被要求做事时"
  }
}
```

### Output Structure
```json
{
  "success": true,
  "assessment": {...},
  "recommendations": [...],
  "summary": {...}
}
```

## Handler Functions

### `handle_milestone_assessment(age_months, observations)`
- **Purpose**: Assess child's developmental progress
- **Parameters**: 
  - `age_months`: Child's age in months (0-60)
  - `observations`: Optional dictionary of observed behaviors by domain
- **Returns**: Assessment results with achieved milestones, upcoming milestones, and red flags

### `handle_activity_recommendation(age_months, available_time, preferred_domains)`
- **Purpose**: Recommend developmentally appropriate activities
- **Parameters**:
  - `age_months`: Child's age in months
  - `available_time`: Available time in minutes (default: 30)
  - `preferred_domains`: Optional list of developmental domains to focus on
- **Returns**: List of suitable activities with details

### `handle_communication_guidance(scenario, child_age_months)`
- **Purpose**: Provide communication strategies for common parenting scenarios
- **Parameters**:
  - `scenario`: One of: tantrum, refusal, sharing, bedtime
  - `child_age_months`: Optional child's age for age-specific advice
- **Returns**: Communication techniques, example scripts, and common mistakes to avoid

### `handle_behavior_analysis(behavior_description, frequency, context, child_age_months)`
- **Purpose**: Analyze behavior patterns and recommend positive discipline
- **Parameters**:
  - `behavior_description`: Description of the behavior
  - `frequency`: How often it occurs
  - `context`: When/where it happens
  - `child_age_months`: Optional child's age for age-appropriate strategies
- **Returns**: Behavior analysis, possible patterns, and positive discipline plan

### `handle_daily_routine_suggestion(child_age_months)`
- **Purpose**: Suggest age-appropriate daily routines
- **Parameters**:
  - `child_age_months`: Child's age in months
- **Returns**: Suggested routine schedule and implementation tips

## Usage Examples

### Example 1: Milestone Assessment
```python
from handler import ParentingGrowthPartner

partner = ParentingGrowthPartner()
result = partner.handle_milestone_assessment(
    age_months=18,
    observations={"language": ["says mama", "understands no"]}
)
print(f"Development status: {result['assessment']['summary']['development_status']}")
```

### Example 2: Activity Recommendation
```python
result = partner.handle_activity_recommendation(
    age_months=30,
    available_time=20,
    preferred_domains=["fine-motor", "cognitive"]
)
for activity in result['recommendations']['recommended_activities'][:2]:
    print(f"- {activity['name']} ({activity['duration_minutes']} min)")
```

### Example 3: Communication Guidance
```python
result = partner.handle_communication_guidance(
    scenario="tantrum",
    child_age_months=24
)
for technique in result['guidance']['techniques']:
    print(f"Technique: {technique['name']}")
    print(f"Example: {technique['example_scripts']['effective']}")
```

## Safety & Considerations

### Developmental Variability
- Children develop at different paces
- Milestones are guidelines, not strict deadlines
- Always consult professionals for concerns

### Cultural Sensitivity
- Parenting practices vary across cultures
- Recommendations should be adapted to family values
- Respect diverse parenting styles

### Professional Consultation
- This tool is for informational purposes only
- Not a substitute for professional medical or psychological advice
- Seek professional help for serious concerns

## Data Sources & References

### Developmental Milestones
- Based on CDC Developmental Milestones
- WHO Child Growth Standards
- American Academy of Pediatrics guidelines

### Positive Parenting Techniques
- Positive Discipline (Jane Nelsen)
- Conscious Parenting
- Evidence-based parenting interventions

### Activity Recommendations
- Developmentally Appropriate Practice (NAEYC)
- Montessori principles
- Play-based learning research

## Testing

Run self-test:
```bash
cd ~/.openclaw/skills/parenting-growth-partner
python3 handler.py
```

Expected output includes 5 test cases with success indicators.

## File Structure
```
parenting-growth-partner/
├── SKILL.md              # This documentation
├── handler.py            # Main handler with self-test
├── skill.json           # Skill metadata
├── .claw/identity.json  # Identity configuration
├── engine/              # Core engines
│   ├── __init__.py
│   ├── milestones.py    # Milestone tracking engine
│   ├── activities.py    # Activity recommendation engine
│   ├── communication.py # Communication guidance engine
│   └── behavior.py      # Behavior analysis engine
└── scripts/
    └── test-handler.py  # Additional test scripts
```

## Version History
- v0.1.0: Initial release with 5 core features
- v0.2.0: Planned: Sleep guidance, feeding advice, sibling rivalry

## Support & Feedback
For issues or suggestions, please contact the skill maintainer.