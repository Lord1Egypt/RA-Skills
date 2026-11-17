"""
Predefined agent role templates
"""

from typing import List, Dict, Any


class StandardTemplate:
    """Standard 9-agent governance template"""

    @staticmethod
    def get_roles() -> List[Dict[str, Any]]:
        """Return standard 9-agent roles"""
        return [
            {
                "name": "orchestrator_agent",
                "role": "Flow orchestration Agent",
                "responsibilities": [
                    "Identify user intent, change type, size, and risk level",
                    "Select workflow based on routing rules",
                    "Assign roles and coordinate handoffs between specialist agents",
                    "Check stage inputs, outputs, and gates before transition",
                    "Trigger reflection lifecycle on gate failures or user rejection"
                ],
                "must_not": [
                    "Bypass blocking gates",
                    "Perform all specialist roles for a non-lightweight change",
                    "Modify workflow rules without approved process improvement"
                ],
                "outputs": [
                    "workflow_selection",
                    "agent_assignment_plan",
                    "stage_transition_decision"
                ],
                "priority": 10
            },
            {
                "name": "requirement_agent",
                "role": "Requirement analysis Agent",
                "responsibilities": [
                    "Clarify problem, goal, non-goals, and scope",
                    "Create or verify proposal.md",
                    "Define acceptance criteria and open questions"
                ],
                "must_not": [
                    "Approve requirements without user confirmation",
                    "Skip validation of acceptance criteria"
                ],
                "outputs": [
                    "proposal.md",
                    "acceptance_criteria",
                    "requirement_open_questions"
                ],
                "priority": 9
            },
            {
                "name": "design_agent",
                "role": "Solution design Agent",
                "responsibilities": [
                    "Create or verify design.md",
                    "Compare alternatives and record rationale",
                    "Define impact scope, test strategy, risks, and rollback"
                ],
                "must_not": [
                    "Approve design without architecture review",
                    "Skip risk and rollback analysis"
                ],
                "outputs": [
                    "design.md",
                    "test_strategy",
                    "risk_and_rollback_plan"
                ],
                "priority": 8
            },
            {
                "name": "implementation_agent",
                "role": "Implementation Agent",
                "responsibilities": [
                    "Implement only the approved proposal, design, and tasks",
                    "Update implementation task status",
                    "Record implementation notes when needed"
                ],
                "must_not": [
                    "Expand scope without returning to requirement or design",
                    "Self-approve final code review, verification, or archive readiness"
                ],
                "outputs": [
                    "code_changes",
                    "updated_tasks",
                    "implementation_notes"
                ],
                "priority": 7
            },
            {
                "name": "code_review_agent",
                "role": "Code review Agent",
                "responsibilities": [
                    "Review correctness, maintainability, security, performance",
                    "Review design alignment",
                    "Separate blocking issues from non-blocking suggestions"
                ],
                "reviewer_for": "implementation_agent",
                "must_not": [
                    "Approve own implementation",
                    "Skip security and performance checks"
                ],
                "outputs": [
                    "review_findings",
                    "blocking_issues",
                    "review_decision"
                ],
                "priority": 6
            },
            {
                "name": "test_planner_agent",
                "role": "Test planning Agent",
                "responsibilities": [
                    "Map acceptance criteria to test coverage",
                    "Define testing scope before implementation or verification",
                    "Identify required regression coverage for hotfixes"
                ],
                "must_not": [
                    "Skip regression test planning for hotfixes",
                    "Approve test plan without coverage mapping"
                ],
                "outputs": [
                    "test_plan",
                    "test_mapping"
                ],
                "priority": 5
            },
            {
                "name": "verification_agent",
                "role": "Verification Agent",
                "responsibilities": [
                    "Run applicable tests and checks",
                    "Collect verification evidence",
                    "Create or update verification-report.md",
                    "Check documentation impact"
                ],
                "must_not": [
                    "Claim completion without evidence",
                    "Skip documentation impact check"
                ],
                "outputs": [
                    "verification-report.md",
                    "verification_evidence",
                    "pass_fail_result"
                ],
                "priority": 4
            },
            {
                "name": "reflection_agent",
                "role": "Reflection Agent",
                "responsibilities": [
                    "Analyze rework, blockers, gate friction",
                    "Analyze agent collaboration issues",
                    "Create retrospective.md",
                    "Classify improvement candidates"
                ],
                "must_not": [
                    "Modify AGENTS.md or rules without user approval",
                    "Archive without completing retrospective"
                ],
                "outputs": [
                    "retrospective.md",
                    "reflection_findings",
                    "improvement_candidates"
                ],
                "priority": 3
            },
            {
                "name": "documentation_agent",
                "role": "Documentation synchronization Agent",
                "responsibilities": [
                    "Check whether long-term specs or docs need updates",
                    "Synchronize approved documentation changes before archive",
                    "Record documentation impact decisions"
                ],
                "must_not": [
                    "Modify docs without verification agent approval",
                    "Skip documentation impact recording"
                ],
                "outputs": [
                    "documentation_impact_result",
                    "updated_docs"
                ],
                "priority": 2
            }
        ]


class SimplifiedTemplate:
    """Simplified 5-agent governance template"""

    @staticmethod
    def get_roles() -> List[Dict[str, Any]]:
        """Return simplified 5-agent roles"""
        return [
            {
                "name": "orchestrator_agent",
                "role": "Flow orchestration Agent",
                "responsibilities": [
                    "Identify user intent and select workflow",
                    "Coordinate handoffs between agents",
                    "Check gates before transition"
                ],
                "must_not": [
                    "Bypass blocking gates",
                    "Perform all specialist roles"
                ],
                "outputs": [
                    "workflow_selection",
                    "agent_assignment_plan"
                ],
                "priority": 10
            },
            {
                "name": "requirement_agent",
                "role": "Requirement analysis Agent",
                "responsibilities": [
                    "Clarify problem and goal",
                    "Create proposal.md",
                    "Define acceptance criteria"
                ],
                "must_not": [
                    "Approve without user confirmation"
                ],
                "outputs": [
                    "proposal.md",
                    "acceptance_criteria"
                ],
                "priority": 9
            },
            {
                "name": "implementation_agent",
                "role": "Implementation Agent",
                "responsibilities": [
                    "Implement approved tasks",
                    "Update task status"
                ],
                "must_not": [
                    "Expand scope without approval",
                    "Self-approve review"
                ],
                "outputs": [
                    "code_changes",
                    "updated_tasks"
                ],
                "priority": 7
            },
            {
                "name": "code_review_agent",
                "role": "Code review Agent",
                "responsibilities": [
                    "Review correctness, security, performance",
                    "Identify blocking issues"
                ],
                "reviewer_for": "implementation_agent",
                "must_not": [
                    "Approve own implementation"
                ],
                "outputs": [
                    "review_findings",
                    "review_decision"
                ],
                "priority": 6
            },
            {
                "name": "verification_agent",
                "role": "Verification Agent",
                "responsibilities": [
                    "Run tests",
                    "Create verification-report.md"
                ],
                "must_not": [
                    "Claim completion without evidence"
                ],
                "outputs": [
                    "verification-report.md",
                    "pass_fail_result"
                ],
                "priority": 4
            }
        ]


class MinimalTemplate:
    """Minimal 3-agent governance template"""

    @staticmethod
    def get_roles() -> List[Dict[str, Any]]:
        """Return minimal 3-agent roles"""
        return [
            {
                "name": "orchestrator_agent",
                "role": "Flow orchestration Agent",
                "responsibilities": [
                    "Coordinate workflow",
                    "Manage handoffs"
                ],
                "must_not": [
                    "Bypass gates"
                ],
                "outputs": [
                    "workflow_selection"
                ],
                "priority": 10
            },
            {
                "name": "implementation_agent",
                "role": "Implementation Agent",
                "responsibilities": [
                    "Implement tasks",
                    "Update status"
                ],
                "must_not": [
                    "Self-approve"
                ],
                "outputs": [
                    "code_changes"
                ],
                "priority": 7
            },
            {
                "name": "verification_agent",
                "role": "Verification Agent",
                "responsibilities": [
                    "Run tests",
                    "Verify completion"
                ],
                "must_not": [
                    "Skip evidence"
                ],
                "outputs": [
                    "verification-report.md"
                ],
                "priority": 4
            }
        ]