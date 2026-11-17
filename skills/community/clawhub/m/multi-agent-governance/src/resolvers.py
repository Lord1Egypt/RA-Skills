"""
Conflict resolver for agent disagreements
"""

from typing import Dict, Any, List
from .models import (
    ResolutionResult,
    AgentConflict,
    ResolutionStrategy,
)


class ConflictResolver:
    """Resolver for agent conflicts"""

    def __init__(self, strategy: ResolutionStrategy = ResolutionStrategy.ORCHESTRATOR_FIRST):
        self.strategy = strategy

    def resolve(self, conflict: AgentConflict, registry) -> ResolutionResult:
        """Resolve a conflict based on the configured strategy"""
        if self.strategy == ResolutionStrategy.ORCHESTRATOR_FIRST:
            return self._orchestrator_first_resolve(conflict, registry)
        elif self.strategy == ResolutionStrategy.USER_FIRST:
            return self._user_first_resolve(conflict)
        elif self.strategy == ResolutionStrategy.VOTING:
            return self._voting_resolve(conflict, registry)
        elif self.strategy == ResolutionStrategy.PRIORITY_BASED:
            return self._priority_based_resolve(conflict, registry)
        else:
            return self._default_resolve(conflict)

    def _orchestrator_first_resolve(self, conflict: AgentConflict, registry) -> ResolutionResult:
        """Resolve by letting orchestrator make the decision"""
        orchestrator_role = registry.get_role("orchestrator_agent")

        if not orchestrator_role:
            return ResolutionResult(
                resolved=False,
                final_decision="no_decision",
                decision_maker="system",
                reasoning="No orchestrator registered to resolve conflict",
                alternative_options=[]
            )

        # Orchestrator decides based on conflict type
        decision_map = {
            "workflow_selection_disputed": "Use standard_change workflow as default",
            "gate_result_disputed": "Re-run gate with additional validation",
            "scope_or_risk_disputed": "Escalate to user with options",
        }

        final_decision = decision_map.get(
            conflict.disagreement_type,
            "Orchestrator reviews context and makes decision"
        )

        return ResolutionResult(
            resolved=True,
            final_decision=final_decision,
            decision_maker="orchestrator_agent",
            reasoning="Orchestrator has authority to resolve coordination conflicts",
            alternative_options=["Escalate to user", "Request additional context"]
        )

    def _user_first_resolve(self, conflict: AgentConflict) -> ResolutionResult:
        """Resolve by asking user for decision"""
        return ResolutionResult(
            resolved=False,
            final_decision="pending_user_input",
            decision_maker="user",
            reasoning="User has final authority over disputed decisions",
            alternative_options=self._generate_alternatives(conflict)
        )

    def _voting_resolve(self, conflict: AgentConflict, registry) -> ResolutionResult:
        """Resolve by voting among involved agents"""
        # Get priorities for each agent
        agent_priorities = {}
        for agent in conflict.agents:
            role = registry.get_role(agent)
            if role:
                agent_priorities[agent] = role.priority
            else:
                agent_priorities[agent] = 0

        # Find highest priority agent
        highest_priority_agent = max(
            agent_priorities.keys(),
            key=lambda k: agent_priorities[k]
        )

        return ResolutionResult(
            resolved=True,
            final_decision=f"Decision by {highest_priority_agent} (highest priority)",
            decision_maker=highest_priority_agent,
            reasoning="Voting mechanism: highest priority agent wins",
            alternative_options=list(agent_priorities.keys())
        )

    def _priority_based_resolve(self, conflict: AgentConflict, registry) -> ResolutionResult:
        """Resolve based on agent priorities"""
        return self._voting_resolve(conflict, registry)

    def _default_resolve(self, conflict: AgentConflict) -> ResolutionResult:
        """Default resolution: escalate to user"""
        return ResolutionResult(
            resolved=False,
            final_decision="escalate_to_user",
            decision_maker="system",
            reasoning="No configured strategy matches, defaulting to user escalation",
            alternative_options=self._generate_alternatives(conflict)
        )

    def _generate_alternatives(self, conflict: AgentConflict) -> List[str]:
        """Generate alternative resolution options"""
        alternatives = []

        based_on_type = {
            "workflow_selection_disputed": [
                "Use standard_change workflow",
                "Use lightweight_tweak workflow",
                "Request user clarification"
            ],
            "gate_result_disputed": [
                "Re-run gate validation",
                "Accept gate result with warnings",
                "Request manual review"
            ],
            "scope_or_risk_disputed": [
                "Adjust scope to lower risk",
                "Request additional safeguards",
                "Escalate to architecture review"
            ],
        }

        alternatives = based_on_type.get(conflict.disagreement_type, [
            "Request user input",
            "Request additional context",
            "Use conservative approach"
        ])

        return alternatives