from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Literal, Optional, Union

from pydantic import BaseModel, Field, model_validator


class DecisionType(str, Enum):
    ALLOW = "ALLOW"
    DENY = "DENY"
    MODIFY = "MODIFY"
    REQUIRE_APPROVAL = "REQUIRE_APPROVAL"


class PolicyFormat(str, Enum):
    STRUCTURED = "structured"
    NATURAL_LANGUAGE = "natural_language"
    JSON = "json"
    YAML = "yaml"


class ConditionOperator(str, Enum):
    EQ = "eq"
    NEQ = "neq"
    GT = "gt"
    GTE = "gte"
    LT = "lt"
    LTE = "lte"
    IN = "in"
    NOT_IN = "not_in"
    CONTAINS = "contains"
    EXISTS = "exists"
    BETWEEN = "between"
    TIME_BETWEEN = "time_between"
    TIME_OUTSIDE = "time_outside"


class PolicyCondition(BaseModel):
    field: str = Field(description="Dot-path field in the action payload/context")
    operator: ConditionOperator
    value: Optional[Any] = None
    value_to: Optional[Any] = None
    timezone: Optional[str] = "UTC"


class StructuredPolicyDefinition(BaseModel):
    action_types: List[str] = Field(default_factory=lambda: ["*"])
    effect: DecisionType
    conditions: List[PolicyCondition] = Field(default_factory=list)
    reason: str
    modifications: Dict[str, Any] = Field(default_factory=dict)
    requires_approval: bool = False
    tags: List[str] = Field(default_factory=list)


class PolicyCreate(BaseModel):
    policy_id: str
    name: str
    description: Optional[str] = None
    priority: int = 100
    enabled: bool = True
    policy_format: PolicyFormat = PolicyFormat.STRUCTURED
    definition: Optional[Union[StructuredPolicyDefinition, Dict[str, Any]]] = None
    raw_policy: Optional[str] = None

    @model_validator(mode="after")
    def validate_source(self) -> "PolicyCreate":
        if self.policy_format == PolicyFormat.STRUCTURED and self.definition is None:
            raise ValueError("`definition` is required when policy_format=structured")
        if self.policy_format in (PolicyFormat.JSON, PolicyFormat.YAML, PolicyFormat.NATURAL_LANGUAGE) and not self.raw_policy:
            raise ValueError("`raw_policy` is required for json/yaml/natural_language formats")
        return self


class PolicyUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[int] = None
    enabled: Optional[bool] = None
    definition: Optional[Union[StructuredPolicyDefinition, Dict[str, Any]]] = None


class PolicyResponse(BaseModel):
    policy_id: str
    name: str
    description: Optional[str]
    priority: int
    enabled: bool
    policy_format: str
    definition: Dict[str, Any]
    created_at: datetime
    updated_at: Optional[datetime]

    model_config = {"from_attributes": True}


class ActionRequest(BaseModel):
    action_id: Optional[str] = None
    action_type: str
    actor_id: Optional[str] = None
    timestamp: Optional[datetime] = None
    payload: Dict[str, Any] = Field(default_factory=dict)
    context: Dict[str, Any] = Field(default_factory=dict)


class MatchedPolicy(BaseModel):
    policy_id: str
    name: str
    priority: int
    effect: DecisionType
    reason: str
    modifications: Dict[str, Any] = Field(default_factory=dict)
    requires_approval: bool = False


class DecisionResponse(BaseModel):
    decision: DecisionType
    reason: str
    policy_id: Optional[str] = None
    requires_approval: bool = False
    modifications: Dict[str, Any] = Field(default_factory=dict)
    matched_policies: List[MatchedPolicy] = Field(default_factory=list)
    explanation: str


class EvaluationResponse(BaseModel):
    action_id: Optional[str]
    action_type: str
    result: DecisionResponse


class AuditLogResponse(BaseModel):
    action_id: Optional[str]
    action_type: str
    decision: Dict[str, Any]
    matched_policies: List[Dict[str, Any]]
    created_at: datetime

    model_config = {"from_attributes": True}


class HealthResponse(BaseModel):
    status: Literal["ok"] = "ok"
