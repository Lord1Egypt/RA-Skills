# skills/ib-portfolio-analyst/ib_analyst/findings.py
"""Structured finding vocabulary shared by every diagnostic module.

A Finding is a graded fact: rules decide the priority, wording is added
later by the LLM layer. `grade` maps a metric to a priority against
configurable warn/crit cutoffs, in either direction.
"""
from __future__ import annotations
from enum import Enum
from pydantic import BaseModel, Field


class Priority(str, Enum):
    P0 = "P0"   # act now / hard risk breach
    P1 = "P1"   # high
    P2 = "P2"   # medium
    P3 = "P3"   # informational


class Finding(BaseModel):
    priority: Priority
    dimension: str
    finding: str
    evidence: dict = Field(default_factory=dict)
    impact: str
    suggestion: str
    trigger_condition: str
    confidence: float
    data_limitations: str


def grade(value: float, warn: float, crit: float, higher_is_worse: bool = True) -> Priority:
    """Grade a metric to P1/P2/P3 against warn/crit cutoffs.

    higher_is_worse=True: value >= crit -> P1, >= warn -> P2, else P3.
    higher_is_worse=False: value <= crit -> P1, <= warn -> P2, else P3.
    """
    if higher_is_worse:
        if value >= crit:
            return Priority.P1
        if value >= warn:
            return Priority.P2
        return Priority.P3
    else:
        if value <= crit:
            return Priority.P1
        if value <= warn:
            return Priority.P2
        return Priority.P3
