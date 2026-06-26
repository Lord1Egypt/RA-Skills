from __future__ import annotations

from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any, Literal, Mapping

MediaKind = Literal["image"]


def _freeze_mapping(value: Mapping[str, Any]) -> Mapping[str, Any]:
    return MappingProxyType(dict(value))


@dataclass(frozen=True)
class GatewayRequest:
    prompt: str
    media_targets: tuple[MediaKind, ...]
    input_images: tuple[str, ...] = ()
    intent_hints: Mapping[str, Any] = field(default_factory=dict)
    extra_params: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "intent_hints", _freeze_mapping(self.intent_hints))
        object.__setattr__(self, "extra_params", _freeze_mapping(self.extra_params))


@dataclass(frozen=True)
class RouteDecision:
    capability: MediaKind
    reason: str


@dataclass(frozen=True)
class ClarificationRequest:
    reason: str
    question: str
    options: tuple[str, ...] = ()


@dataclass(frozen=True)
class WorkflowStepDraft:
    step_id: str
    capability: MediaKind
    goal: str
    depends_on: tuple[str, ...] = ()


@dataclass(frozen=True)
class WorkflowPlanDraft:
    summary: str
    steps: tuple[WorkflowStepDraft, ...]


@dataclass(frozen=True)
class TaskSpec:
    capability: MediaKind
    task_type: str
    prompt: str
    input_images: tuple[str, ...] = ()
    extra_params: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "extra_params", _freeze_mapping(self.extra_params))


@dataclass(frozen=True)
class ModelCandidate:
    name: str
    model_id: str
    version_id: str
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "metadata", _freeze_mapping(self.metadata))


@dataclass(frozen=True)
class ModelBinding:
    candidate: ModelCandidate
    attribute_id: int
    credit: int
    resolved_params: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "resolved_params", _freeze_mapping(self.resolved_params))


@dataclass(frozen=True)
class ExecutionResult:
    task_id: str
    url: str
    cover_url: str = ""
    model_id: str = ""
    model_name: str = ""
    credit: int = 0
