"""
Personal Assistant Skill — scripts package.

Modules:
    db.py           — Database connection management, schema init, CRUD
    task_manager.py — Task CRUD, queries, sort, and stats
    progress.py     — Progress logging and milestone management
    recurring.py    — Recurring task templates and instance generation
    reminder.py     — Reminder engine: filtering, sorting, dedup, formatting
    okr.py          — OKR (Objectives & Key Results) management
    report.py       — Daily/weekly report generation
    advisor.py      — Task scheduling advisor and workload analysis
"""

from __future__ import annotations
from .db import Database
from .task_manager import TaskManager
from .progress import ProgressTracker
from .recurring import RecurringManager
from .reminder import ReminderEngine
from .okr import OKRManager
from .report import ReportGenerator
from .advisor import Advisor

__all__ = [
    "Database",
    "TaskManager",
    "ProgressTracker",
    "RecurringManager",
    "ReminderEngine",
    "OKRManager",
    "ReportGenerator",
    "Advisor",
]
