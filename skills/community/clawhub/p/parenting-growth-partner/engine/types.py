"""
Parenting Growth Partner - Core Types
Defines all data structures based on design document.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Literal

# ---- Child Profile ----
@dataclass
class ChildBasicInfo:
    name: str
    birth_date: str
    gender: Literal["male", "female"]
    birth_weight: float  # kg
    birth_length: float  # cm
    gestational_age: int  # weeks

@dataclass
class ChildMeasurements:
    weight: float       # kg
    height: float       # cm
    head_circumference: Optional[float] = None
    last_measured: Optional[str] = None

@dataclass
class ChildProfile:
    id: str
    basic_info: ChildBasicInfo
    measurements: Optional[ChildMeasurements] = None
    temperament: Literal["easy", "difficult", "slow-to-warm-up", "mixed"] = "mixed"
    interests: List[str] = field(default_factory=list)
    strengths: List[str] = field(default_factory=list)
    challenges: List[str] = field(default_factory=list)

# ---- Milestone ----
@dataclass
class Milestone:
    id: str
    domain: Literal["gross-motor", "fine-motor", "language", "cognitive", "social-emotional", "adaptive"]
    age_range: tuple[int, int]   # (min_months, max_months)
    description: str
    behaviors: dict              # {early, typical, advanced}
    red_flags: dict              # {absence, regression, extreme}
    support_strategies: dict

# ---- Activity ----
@dataclass
class Activity:
    id: str
    name: str
    description: str
    age_range: tuple[int, int]
    domains: List[str]
    difficulty: Literal["easy", "medium", "hard"]
    duration_minutes: int
    materials: List[str]
    steps: List[str]
    safety_notes: List[str] = field(default_factory=list)

# ---- Communication ----
@dataclass
class CommunicationScript:
    situation: str
    effective_words: str
    ineffective_words: str
    rationale: str

@dataclass
class CommunicationTechnique:
    name: str
    description: str
    when_to_use: str
    scripts: List[CommunicationScript]

# ---- Behavior ----
@dataclass
class BehaviorAnalysis:
    behavior: str
    frequency: Literal["occasional", "frequent", "persistent"]
    intensity: Literal["mild", "moderate", "severe"]
    context: str
    likely_function: Literal["attention-seeking", "escape-avoidance", "tangible", "sensory", "communication"]
    causes: List[str]
    preventive_strategies: List[str]
    responsive_strategies: List[str]
    teaching_steps: List[str]
