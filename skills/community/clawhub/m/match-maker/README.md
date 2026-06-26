# Matchmaker - AI-Powered Dating Match System

> Professional matchmaking skill for OpenClaw - Intelligent relationship matching and dating guidance for individuals

**Version:** 0.1.0 | **Status:** Production Ready | **License:** MIT

---

## What is Matchmaker?

Matchmaker is an AI-powered matchmaking system designed to help **single individuals find compatible partners** through intelligent analysis and personalized guidance. It provides comprehensive profile analysis, compatibility scoring, conversation starters, and relationship tracking.

### Core Capabilities

- **Profile Analysis** - Multi-dimensional personality and lifestyle assessment
- **Smart Matching** - AI-powered compatibility algorithm with detailed scoring
- **Icebreaker Generation** - Personalized conversation starters and date ideas
- **Relationship Tracking** - Monitor relationship health and development progress

---

## Quick Start

### Installation

```bash
# Install dependencies
pip install -e .

# Or install from requirements
pip install -r requirements.txt
```

### Basic Usage

```python
import asyncio
from matchmaker import Matchmaker, Person, PersonalityTraits, Lifestyle, Values, Interests

async def main():
    # Initialize matchmaker
    matchmaker = Matchmaker()

    # Create person profile
    alex = Person(
        name="Alex Chen",
        age=28,
        gender="male",
        location="San Francisco, CA",
        personality=PersonalityTraits(
            openness=85,
            conscientiousness=70,
            extraversion=60,
            agreeableness=75,
            neuroticism=40,
            mbti="ENFP"
        ),
        lifestyle=Lifestyle(
            sleep_schedule="night-owl",
            exercise_frequency="weekly",
            social_activity="moderately-social",
            work_life_balance="balanced",
            travel_frequency="occasional",
            pets="has-dogs",
            smoking="never",
            drinking="social"
        ),
        values=Values(
            marriage_view="open",
            children_plan="want",
            family_importance=80,
            career_importance=70,
            communication_style="diplomatic"
        ),
        interests=Interests(
            categories=["tech", "travel", "music", "cooking"],
            specific_hobbies=["photography", "hiking", "guitar"],
            favorite_activities=["coffee date", "museum visit"]
        ),
        occupation="Software Engineer",
        education="Bachelor's Degree"
    )

    # Analyze profile
    profile = await matchmaker.analyze_profile(alex)
    print(f"Dating Readiness: {profile.dating_readiness}")
    print(f"Profile Score: {profile.overall_score}/100")

    # Find match compatibility (with another person)
    match = await matchmaker.find_match(alex, jamie)
    print(f"Compatibility: {match.compatibility.overall_score}/100")

    # Generate icebreakers
    icebreakers = await matchmaker.generate_icebreakers(alex, jamie)
    print("Opening line:", icebreakers.opening_lines[0])

if __name__ == "__main__":
    asyncio.run(main())
```

---

## Features in Detail

### 1. Profile Analysis

Evaluate dating readiness across multiple dimensions:

- **Personality** (30%): Big Five traits + MBTI
- **Lifestyle** (25%): Daily habits, sleep, exercise, social activities
- **Values** (30%): Marriage views, family plans, communication style
- **Interests** (15%): Hobbies, activities, passions

**Output:**
- Overall profile score (0-100)
- Dating readiness level (ready/mostly-ready/needs-work/not-ready)
- Profile type (e.g., "balanced-creative-professional")
- Strengths, weaknesses, and recommendations

```python
profile = await matchmaker.analyze_profile(person)
```

### 2. Smart Matching

Calculate compatibility using intelligent algorithms:

**Compatibility Dimensions:**
- Personality compatibility (considers complementarity)
- Lifestyle compatibility (habits, schedules, preferences)
- Values alignment (marriage, children, family - most critical)
- Interests overlap (shared hobbies and activities)

**Output:**
- Overall compatibility score (0-100)
- Component scores for each dimension
- Match quality rating (excellent/very-good/good/fair/poor)
- Why good match + potential challenges
- Relationship potential assessment

```python
match = await matchmaker.find_match(person1, person2)
```

### 3. Icebreaker Generation

Personalized conversation starters based on profiles:

**Includes:**
- 5 opening message suggestions
- Shared interest topics
- Unique conversation starters
- Questions to ask
- Personalized date ideas with reasoning
- Topics to avoid
- Communication tips based on personality

```python
icebreakers = await matchmaker.generate_icebreakers(person, match)
```

### 4. Relationship Tracking

Monitor relationship development and health:

**Analysis:**
- Relationship stage (initial-contact → serious)
- Health score based on interaction quality
- Positive indicators and concerns
- Communication quality and balance
- Momentum assessment (accelerating/steady/slowing/stalled)

**Output:**
- Recommended next steps
- Red flags and green flags
- Success likelihood prediction
- Timeline prediction for milestones

```python
from matchmaker import InteractionLog

interactions = [
    InteractionLog(date="2024-03-01", type="message", quality="good"),
    InteractionLog(date="2024-03-05", type="date", quality="excellent"),
]

assessment = await matchmaker.assess_relationship(person1, person2, interactions)
```

---

## Use Cases

### For Single Individuals

**Scenario 1: Self-Assessment**
```python
# Understand your dating profile
profile = await matchmaker.analyze_profile(me)
print(f"Dating readiness: {profile.dating_readiness}")
print("Strengths:", profile.strengths)
print("Recommendations:", profile.recommendations)
```

**Scenario 2: Evaluating a Match**
```python
# Check compatibility with someone you're interested in
match = await matchmaker.find_match(me, potential_match)
print(f"Compatibility: {match.compatibility.overall_score}/100")
print("Why good match:", match.why_good_match)
```

**Scenario 3: Getting Date Ideas**
```python
# Get personalized icebreakers and date suggestions
icebreakers = await matchmaker.generate_icebreakers(me, match)
for idea in icebreakers.date_ideas:
    print(f"{idea['activity']}: {idea['reason']}")
```

**Scenario 4: Tracking Relationship**
```python
# Monitor how your relationship is developing
assessment = await matchmaker.assess_relationship(me, partner, interactions)
print(f"Relationship health: {assessment.relationship_health}/100")
print("Next steps:", assessment.next_steps)
```

---

## Project Structure

```
openclaw-match-maker/
├── matchmaker/                # Main Python package
│   ├── matchmaker.py         # Main Matchmaker class
│   ├── types/                # Pydantic data models
│   │   ├── person.py         # Person schema
│   │   ├── profile.py        # Profile schema
│   │   └── models.py         # Result models
│   └── modules/              # Business logic modules
│       ├── profiling/        # Profile analyzer
│       ├── matching/         # Match algorithm
│       ├── icebreaker/       # Icebreaker generator
│       └── relationship/     # Relationship assessor
├── examples/                  # Usage examples
│   └── basic_example.py      # Complete demo
├── tests/                     # Test suite
├── test_complete.py          # Complete test script
├── SKILL.md                  # OpenClaw skill definition
├── README.md                 # This file
└── requirements.txt          # Python dependencies
```

---

## API Reference

### Matchmaker Class

```python
class Matchmaker:
    """Main Matchmaker class providing all matchmaking services."""

    async def analyze_profile(self, person: Person) -> Profile:
        """Analyze person's profile and generate assessment."""

    async def find_match(self, person1: Person, person2: Person) -> MatchResult:
        """Calculate compatibility between two people."""

    async def batch_match(self, person: Person, candidates: List[Person], top_n: int = 10) -> List[MatchResult]:
        """Match one person against multiple candidates."""

    async def generate_icebreakers(self, person: Person, match: Person) -> IcebreakerSuggestion:
        """Generate personalized conversation starters."""

    async def assess_relationship(self, person1: Person, person2: Person, interactions: List[InteractionLog]) -> RelationshipAssessment:
        """Assess relationship health and progress."""

    async def complete_match_analysis(self, person1: Person, person2: Person) -> dict:
        """Run complete analysis including match and icebreakers."""

    async def full_profile_and_matches(self, person: Person, candidates: List[Person], top_n: int = 5) -> dict:
        """Analyze profile and find best matches."""
```

---

## Testing

```bash
# Run complete test suite
python3 test_complete.py

# Run example
python3 examples/basic_example.py
```

Expected output:
```
✅ Test Passed: Profile Analysis
✅ Test Passed: Compatibility Matching
✅ Test Passed: Icebreaker Generation
✅ Test Passed: Relationship Assessment

🎉 All tests passed! Matchmaker system is ready to use.
```

---

## Configuration

### Custom Weights

You can customize the importance of different dimensions:

```python
# Custom profiling weights
matchmaker = Matchmaker(
    profiling_weights={
        "personality": 0.35,  # Default: 0.30
        "lifestyle": 0.20,    # Default: 0.25
        "values": 0.35,       # Default: 0.30
        "interests": 0.10,    # Default: 0.15
    },
    matching_weights={
        "personality": 0.25,  # Default: 0.30
        "lifestyle": 0.20,    # Default: 0.25
        "values": 0.40,       # Default: 0.30 (values are critical!)
        "interests": 0.15,    # Default: 0.15
    }
)
```

---

## Matching Algorithm Details

### Personality Compatibility

- **Openness**: Similarity preferred (shared curiosity)
- **Conscientiousness**: Moderate similarity
- **Extraversion**: Some difference okay (complementary energy)
- **Agreeableness**: Similarity preferred
- **Neuroticism**: Lower combined is better

### Values Alignment (Most Critical)

- **Marriage views**: Must align or have flexibility
- **Children plans**: CRITICAL - mismatch is major red flag
- **Family importance**: Should be similar
- **Religion**: If important to either, must align

### Lifestyle Compatibility

- **Sleep schedule**: Same or one flexible
- **Exercise habits**: Similar levels preferred
- **Social activity**: Can be complementary
- **Smoking**: Major incompatibility if mismatch

---

## Limitations & Disclaimers

### What Matchmaker Can Do
✅ Provide data-driven compatibility analysis
✅ Generate personalized conversation suggestions
✅ Track relationship health indicators
✅ Offer actionable dating advice

### What Matchmaker Cannot Do
❌ Guarantee relationship success
❌ Replace human judgment and intuition
❌ Predict exact outcomes
❌ Make decisions for you
❌ Replace professional counseling

**Important:** Compatibility scores are estimates based on models. Use as guidance, not absolute truth. Trust your feelings and intuition.

---

## Roadmap

### Version 0.2.0 (Q3 2024)
- [ ] Web UI for easy profile creation
- [ ] Integration with dating platforms
- [ ] Machine learning improvements
- [ ] Multi-language support

### Version 0.3.0 (Q4 2024)
- [ ] Group compatibility analysis
- [ ] Long-term relationship insights
- [ ] Photo analysis integration
- [ ] Voice compatibility features

---

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

Areas where we need help:
- Algorithm improvements
- Test coverage expansion
- Documentation enhancements
- Internationalization

---

## License

MIT License - See [LICENSE](LICENSE) for details

---

## Acknowledgments

- OpenClaw community for the skill framework
- Relationship psychology research
- Big Five personality model
- Open source Python ecosystem

---

**Built with care for meaningful connections**

*Making intelligent matchmaking accessible to everyone*
