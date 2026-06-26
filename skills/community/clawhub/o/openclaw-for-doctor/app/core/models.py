from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class ChannelType(str, Enum):
    feishu = "feishu"
    dingtalk = "dingtalk"
    email = "email"
    wechat = "wechat"
    xiaohongshu = "xiaohongshu"
    webchat = "webchat"


class RoleStage(str, Enum):
    encyclopedia = "encyclopedia"
    discussion_partner = "discussion_partner"
    trusted_assistant = "trusted_assistant"
    mentor = "mentor"


class ReasoningMode(str, Enum):
    strict = "strict"
    innovative = "innovative"


class UseCase(str, Enum):
    diagnosis = "diagnosis"
    treatment_rehab = "treatment_rehab"
    teaching = "teaching"
    research = "research"


class TaskStatus(str, Enum):
    queued = "queued"
    running = "running"
    completed = "completed"
    failed = "failed"
    cancelled = "cancelled"


class Citation(BaseModel):
    source: str
    title: str
    evidence_level: str
    note: str


class TaskRequest(BaseModel):
    query: str = Field(min_length=5, description="Doctor's original request")
    channel: ChannelType = ChannelType.webchat
    doctor_id: Optional[str] = None
    callback_url: Optional[str] = None
    case_summary: Optional[str] = None
    requested_role: Optional[RoleStage] = None
    reasoning_mode: Optional[ReasoningMode] = None
    use_case: UseCase = UseCase.diagnosis
    require_citations: bool = True
    attachments: List[str] = Field(default_factory=list)


class TaskExecutionProfile(BaseModel):
    role_stage: RoleStage
    reasoning_mode: ReasoningMode
    use_case: UseCase
    evidence_policy: str


class DeliveryReceipt(BaseModel):
    channel: ChannelType
    delivered: bool
    detail: str
    delivered_at: datetime = Field(default_factory=datetime.utcnow)


class TaskResult(BaseModel):
    task_id: str
    role_stage: RoleStage
    reasoning_mode: ReasoningMode
    use_case: UseCase
    summary: str
    analysis: List[str]
    action_plan: List[str]
    citations: List[Citation]
    guardrails: List[str]
    next_expansion_tracks: List[str]
    generated_at: datetime = Field(default_factory=datetime.utcnow)
    delivery: Optional[DeliveryReceipt] = None


class StoredTask(BaseModel):
    task_id: str
    request: TaskRequest
    status: TaskStatus
    attempts: int = 0
    profile: Optional[TaskExecutionProfile] = None
    result: Optional[TaskResult] = None
    error: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class HealthStatus(BaseModel):
    service: str = "openclaw-for-doctor"
    status: str = "ok"
    env: str = "dev"
    task_store: str = "unknown"
    now: datetime = Field(default_factory=datetime.utcnow)
    supported_channels: List[ChannelType] = Field(
        default_factory=lambda: [
            ChannelType.feishu,
            ChannelType.dingtalk,
            ChannelType.email,
            ChannelType.wechat,
            ChannelType.xiaohongshu,
            ChannelType.webchat,
        ]
    )


class ExecutionContext(BaseModel):
    profile: TaskExecutionProfile
    token_budget: int = 1600
    metadata: Dict[str, str] = Field(default_factory=dict)
