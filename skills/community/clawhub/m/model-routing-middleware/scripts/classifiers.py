"""
Task Classifier — Keyword-based intent detection (v1)

Classifies prompts into task types for model routing.
Phase 1 uses simple keyword matching.
Phase 2 will use lightweight embedding-based semantic routing.


"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class TaskType(Enum):
    """Supported task types for routing."""
    CODING = "coding"
    REASONING = "reasoning"
    CHAT = "chat"
    SUMMARIZE = "summarize"
    RESEARCH = "research"
    TOOLS = "tools"
    VISION = "vision"


# Keyword patterns for each task type (ordered by specificity)
# More specific patterns are checked first to avoid false matches
KEYWORD_PATTERNS: dict[TaskType, list[str]] = {
    TaskType.CODING: [
        r'\bcode\b', r'\bcoding\b', r'\bprogram\b', r'\bprogramming\b',
        r'\bpython\b', r'\bjavascript\b', r'\btypescript\b', r'\brust\b',
        r'\bgo\b', r'\bjava\b', r'\bc\+\+\b', r'\bc#\b', r'\b ruby\b',
        r'\bdocker\b', r'\bkubernetes\b', r'\bk8s\b', r'\byaml\b',
        r'\bjson\b', r'\bxml\b', r'\bhtml\b', r'\bcss\b',
        r'\bbug\b', r'\bdebug\b', r'\bfix\b', r'\bimplement\b',
        r'\bfunction\b', r'\bclass\b', r'\bmethod\b', r'\bmodule\b',
        r'\bapi\b', r'\bendpoint\b', r'\broute\b', r'\bhandler\b',
        r'\brefactor\b', r'\boptimize\b', r'\bcompile\b', r'\bbuild\b',
        r'\bdeploy\b', r'\bgit\b', r'\bcommit\b', r'\bbranch\b',
        r'\bmerge\b', r'\bpull request\b', r'\btest\b', r'\bunit test\b',
        r'\bsyntax\b', r'\berror\b', r'\btraceback\b', r'\bexception\b',
        r'\bstack\b', r'\bvariable\b', r'\bparameter\b', r'\breturn\b',
        r'\bimport\b', r'\bexport\b', r'\bpackage\b', r'\bdependency\b',
        r'\bregex\b', r'\bregexp\b', r'\bshell\b', r'\bbash\b',
        r'\bscript\b', r'\bautomation\b', r'\bCI\b', r'\bCD\b',
        r'\bscaffold\b', r'\btemplate\b', r'\bboilerplate\b',
        r'\bwrite\s+(?:a\s+)?(?:code|function|class|script|program|module)\b',
    ],

    TaskType.REASONING: [
        r'\bplan\b', r'\bplanning\b', r'\banalyze\b', r'\banalysis\b',
        r'\bresearch\b', r'\barchitecture\b', r'\bstrategy\b', r'\bstrategic\b',
        r'\bdesign\b', r'\bevaluate\b', r'\bcompare\b', r'\bcontrast\b',
        r'\bpros and cons\b', r'\btrade.?off\b', r'\bdecision\b',
        r'\bthink\s+about\b', r'\bconsider\b', r'\bweigh\b',
        r'\breason\b', r'\breasoning\b', r'\blogic\b', r'\blogical\b',
        r'\bdeduce\b', r'\binfer\b', r'\binference\b',
        r'\bhypothesis\b', r'\bhypothesize\b',
        r'\bsolve\b', r'\bsolution\b', r'\bapproach\b',
        r'\bwhat\s+should\b', r'\bwhich\s+(?:is\s+)?better\b',
        r'\bwhy\b', r'\bhow\s+does\b', r'\bexplain\b',
        r'\bbreak\s+down\b', r'\bstep.?by.?step\b',
        r'\bfirst\s+principles\b', r'\broot\s+cause\b',
    ],

    TaskType.SUMMARIZE: [
        r'\bsummarize\b', r'\bsummary\b', r'\bsummarise\b',
        r'\bcondense\b', r'\bbrief\b', r'\btl;?dr\b', r'\btl.?dr\b',
        r'\bkey\s+points\b', r'\bmain\s+ideas\b', r'\bhighlights\b',
        r'\boverview\b', r'\bdigest\b', r'\bwrap.?up\b',
        r'\bshorten\b', r'\babridge\b',
        r'\bgive\s+me\s+(?:a\s+)?summary\b',
        r'\bsum\s+up\b',
    ],

    TaskType.RESEARCH: [
        r'\bresearch\b', r'\binvestigate\b', r'\binvestigation\b',
        r'\bexplore\b', r'\bfind\s+out\b', r'\blook\s+into\b',
        r'\bdig\s+into\b', r'\bstudy\b', r'\bsurvey\b',
        r'\bliterature\s+review\b', r'\bdeep\s+dive\b',
        r'\bwhat\s+(?:is|are)\s+(?:the\s+)?(?:latest|current|recent)\b',
        r'\bsearch\s+for\b', r'\blook\s+up\b',
    ],

    TaskType.TOOLS: [
        r'\btool\b', r'\btools\b', r'\bcommand\b', r'\bcommands\b',
        r'\bcli\b', r'\bshell\b', r'\bterminal\b', r'\bexec\b',
        r'\brun\b', r'\bexecute\b', r'\blaunch\b', r'\bstart\b',
        r'\bstop\b', r'\brestart\b', r'\bstatus\b', r'\bcheck\b',
        r'\binstall\b', r'\bsetup\b', r'\bconfigure\b', r'\bconfig\b',
        r'\bmonitor\b', r'\bwatch\b', r'\blog\b', r'\blogs\b',
        r'\bservice\b', r'\bdaemon\b', r'\bprocess\b',
        r'\bping\b', r'\bcurl\b', r'\bwget\b', r'\bssh\b',
        r'\bdocker\b(?:\s+(?:run|ps|exec|logs|build|compose))\b',
        r'\bffmpeg\b', r'\bconvert\b',
    ],

    TaskType.VISION: [
        r'\bimage\b', r'\bphoto\b', r'\bpicture\b', r'\bscreenshot\b',
        r'\bscreen\b', r'\bcamera\b', r'\bvisual\b', r'\bsee\b',
        r'\blook\s+at\b', r'\bwatch\b', r'\bvideo\b',
        r'\bdescribe\s+(?:this\s+)?(?:image|photo|picture|screenshot)\b',
        r'\bwhat\s+(?:is|do)\s+(?:this|that|the)\s+(?:image|photo|picture|screen)\b',
        r'\bocr\b', r'\brecognize\b', r'\bdetect\s+(?:in|on)\b',
    ],
}

# Priority order for classification when multiple types match
# More specific types are checked first
CLASSIFICATION_PRIORITY = [
    TaskType.VISION,      # Vision is very specific
    TaskType.CODING,      # Coding is specific
    TaskType.SUMMARIZE,   # Summarize is specific
    TaskType.RESEARCH,    # Research is specific
    TaskType.REASONING,   # Reasoning is moderately specific
    TaskType.TOOLS,       # Tools is somewhat generic
    TaskType.CHAT,        # Chat is the default fallback
]


@dataclass
class ClassificationResult:
    """Result of task classification."""
    task_type: TaskType
    confidence: float
    matched_keywords: list[str] = field(default_factory=list)
    scores: dict[TaskType, float] = field(default_factory=dict)

    def __str__(self) -> str:
        return f"ClassificationResult(task={self.task_type.value}, confidence={self.confidence:.2f}, matches={self.matched_keywords})"


def classify_task(prompt: str) -> ClassificationResult:
    """
    Classify a prompt into a task type using keyword matching.

    Args:
        prompt: The user prompt to classify.

    Returns:
        ClassificationResult with the detected task type, confidence score,
        matched keywords, and scores for all task types.
    """
    if not prompt or not prompt.strip():
        return ClassificationResult(
            task_type=TaskType.CHAT,
            confidence=0.3,
            matched_keywords=[],
            scores={t: 0.0 for t in TaskType},
        )

    prompt_lower = prompt.lower()
    scores: dict[TaskType, float] = {}
    all_matches: dict[TaskType, list[str]] = {}

    for task_type, patterns in KEYWORD_PATTERNS.items():
        matches = []
        for pattern in patterns:
            found = re.findall(pattern, prompt_lower)
            matches.extend(found)
        # Deduplicate matches
        unique_matches = list(dict.fromkeys(matches))
        scores[task_type] = len(unique_matches)
        all_matches[task_type] = unique_matches

    # Find the best scoring task type, using priority for tie-breaking
    best_type = TaskType.CHAT
    best_score = 0
    for task_type in CLASSIFICATION_PRIORITY:
        score = scores.get(task_type, 0)
        if score > best_score:
            best_score = score
            best_type = task_type

    # Calculate confidence
    total_score = sum(scores.values())
    if total_score == 0:
        # No keywords matched — default to chat with low confidence
        return ClassificationResult(
            task_type=TaskType.CHAT,
            confidence=0.4,  # Low confidence default
            matched_keywords=[],
            scores={t: 0.0 for t in TaskType},
        )

    # Confidence = best_score / total_score, scaled to [0.4, 1.0]
    # If one type dominates, confidence is high
    # If scores are spread, confidence is lower
    raw_confidence = best_score / total_score if total_score > 0 else 0
    # Scale: 0.4 (even spread) to 1.0 (complete dominance)
    scaled_confidence = 0.4 + 0.6 * raw_confidence

    return ClassificationResult(
        task_type=best_type,
        confidence=round(scaled_confidence, 3),
        matched_keywords=all_matches.get(best_type, []),
        scores={t: float(s) for t, s in scores.items()},
    )


def classify_task_simple(prompt: str) -> str:
    """
    Simple classification that returns just the task type string.
    Convenience wrapper for classify_task().
    """
    result = classify_task(prompt)
    return result.task_type.value