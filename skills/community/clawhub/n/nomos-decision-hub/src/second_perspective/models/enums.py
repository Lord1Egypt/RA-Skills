from enum import StrEnum


class DecisionStatus(StrEnum):
    DRAFT = "DRAFT"
    STRUCTURED = "STRUCTURED"
    EVIDENCE_PENDING = "EVIDENCE_PENDING"
    EVALUATED = "EVALUATED"
    AUDIT_FAILED = "AUDIT_FAILED"
    AUDIT_PASSED = "AUDIT_PASSED"
    HUMAN_APPROVAL_REQUIRED = "HUMAN_APPROVAL_REQUIRED"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"


class EvaluationMode(StrEnum):
    CONSTRAINT_ONLY = "constraint_only"
    WEIGHTED = "weighted"


class ConstraintKind(StrEnum):
    HARD = "hard"
    SOFT = "soft"


class ConstraintOperator(StrEnum):
    EQ = "eq"
    NE = "ne"
    GT = "gt"
    GTE = "gte"
    LT = "lt"
    LTE = "lte"
    IN = "in"
    NOT_IN = "not_in"


class EvidenceStatus(StrEnum):
    SUPPLIED = "supplied"
    MISSING = "missing"
    DISPUTED = "disputed"


class AssumptionSource(StrEnum):
    EXPLICIT = "explicit"
    INFERRED = "inferred"


class AlternativeStatus(StrEnum):
    ELIGIBLE = "eligible"
    INELIGIBLE = "ineligible"
    INCOMPLETE = "incomplete"


class IssueSeverity(StrEnum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"


class ScoringRule(StrEnum):
    HIGHER_IS_BETTER = "higher_is_better"
    LOWER_IS_BETTER = "lower_is_better"
    TARGET_IS_BETTER = "target_is_better"


class CounterfactualStatus(StrEnum):
    LEADER_STABLE = "leader_stable"
    LEADER_CHANGED = "leader_changed"
    NO_VIABLE_ALTERNATIVE = "no_viable_alternative"


class ScenarioOutcomeStatus(StrEnum):
    EVALUATED = "evaluated"
    BLOCKED = "blocked"
    NO_VIABLE_ALTERNATIVE = "no_viable_alternative"


class InformationPriorityTier(StrEnum):
    BLOCKING = "blocking"
    LEADER_EXPOSED = "leader_exposed"
    STRUCTURAL = "structural"
    REVIEW = "review"


class AssumptionState(StrEnum):
    """Per-round assumption state inside a reconstruction session.

    Transitions are monotone: once VERIFIED or FALSIFIED an assumption never
    returns to ASSUMED. UNFALSIFIABLE is a terminal human-declared state.
    """

    ASSUMED = "assumed"
    VERIFIED = "verified"
    FALSIFIED = "falsified"
    UNFALSIFIABLE = "unfalsifiable"


class ReconstructionKind(StrEnum):
    """The three layers of causal reconstruction.

    1. FORWARD_PROPAGATION  — invalidation_closure: A1 fails → what else breaks.
    2. BACKWARD_TRACING     — CausalReconstructor: deviation → candidate root cause.
    3. DELTA_RECONSTRUCTION — apply declared delta_vars, re-evaluate, check convergence.
    """

    FORWARD_PROPAGATION = "forward_propagation"
    BACKWARD_TRACING = "backward_tracing"
    DELTA_RECONSTRUCTION = "delta_reconstruction"


class SessionStatus(StrEnum):
    ACTIVE = "active"
    AWAITING_HUMAN = "awaiting_human"
    CONVERGED = "converged"
    SEALED = "sealed"
    BUDGET_EXCEEDED = "budget_exceeded"


class ConvergenceKind(StrEnum):
    """Why a reconstruction session stopped.

    - FIXED_POINT: re-evaluation changed neither candidates nor hypothesis set.
    - NO_GAIN:     no unresolved branches remain and every open hypothesis is answered.
    - BUDGET:      iteration or evidence budget exhausted.
    """

    FIXED_POINT = "fixed_point"
    NO_GAIN = "no_gain"
    BUDGET = "budget"


class InteractionEffectType(StrEnum):
    """How a multi-assumption interaction deviates from first-order additivity.

    - CONJUNCTIVE: Δ > 0 — joint failure amplifies impact (worse than sum of parts).
    - DISJUNCTIVE: Δ < 0 — joint failure is redundant (better than sum of parts).
    - DEGENERATE:  Δ = 0 — no interaction, kept as evidence of inspection.
    """

    CONJUNCTIVE = "conjunctive"
    DISJUNCTIVE = "disjunctive"
    DEGENERATE = "degenerate"
