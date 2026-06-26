#!/usr/bin/env python3
"""Pipeline-specific error types."""


class PipelineError(RuntimeError):
    """Base error for shared redaction pipeline failures."""


class PlanningError(PipelineError):
    """Raised when plan construction fails."""


class ApplyError(PipelineError):
    """Raised when apply stage fails or violates policy."""


class VerificationError(PipelineError):
    """Raised when verification stage fails policy checks."""
