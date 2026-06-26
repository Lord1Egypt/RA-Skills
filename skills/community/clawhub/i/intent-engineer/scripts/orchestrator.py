#!/usr/bin/env python3
"""
Skill Orchestrator: Composes and executes multi-skill workflows.

This orchestrator handles:
- Sequential skill execution
- Parallel skill execution
- Conditional branching
- Data contract validation
- Error handling and retries
- Comprehensive logging and decision tracking
"""

import json
import asyncio
import logging
from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass, asdict
from datetime import datetime
import jsonschema
from enum import Enum


class ExecutionStatus(Enum):
    """Status of a workflow execution."""
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    ESCALATED = "escalated"


@dataclass
class StepResult:
    """Result of a single skill execution."""
    step_id: int
    skill_id: str
    status: ExecutionStatus
    inputs: Dict[str, Any]
    outputs: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    execution_time_ms: float = 0.0
    timestamp: str = ""

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            **asdict(self),
            "status": self.status.value,
            "timestamp": self.timestamp or datetime.now().isoformat()
        }


@dataclass
class WorkflowExecution:
    """Execution record for an entire workflow."""
    workflow_id: str
    workflow_name: str
    status: ExecutionStatus
    steps: List[StepResult]
    inputs: Dict[str, Any]
    outputs: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    total_execution_time_ms: float = 0.0
    started_at: str = ""
    completed_at: str = ""

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            **asdict(self),
            "status": self.status.value,
            "steps": [step.to_dict() for step in self.steps],
            "started_at": self.started_at or datetime.now().isoformat(),
            "completed_at": self.completed_at or datetime.now().isoformat()
        }


class SkillRegistry:
    """Manages the skill registry and provides skill metadata."""

    def __init__(self, registry_path: str):
        """Initialize with path to skill registry JSON."""
        with open(registry_path, 'r') as f:
            self.registry = json.load(f)
        self.skills = {skill['id']: skill for skill in self.registry['skills']}

    def get_skill(self, skill_id: str) -> Optional[Dict[str, Any]]:
        """Get skill metadata by ID."""
        return self.skills.get(skill_id)

    def get_data_contract(self, contract_id: str) -> Optional[Dict[str, Any]]:
        """Get data contract schema by ID."""
        for contract in self.registry.get('data_contracts', []):
            if contract['id'] == contract_id:
                # Load the schema from file
                try:
                    with open(contract['file'], 'r') as f:
                        return json.load(f)
                except FileNotFoundError:
                    logging.warning(f"Contract file not found: {contract['file']}")
                    return None
        return None

    def get_skill_dependencies(self, skill_id: str) -> List[str]:
        """Get list of skill IDs that a skill depends on."""
        skill = self.get_skill(skill_id)
        if not skill:
            return []
        return [dep['skill_id'] for dep in skill.get('dependencies', [])]


class DataContractValidator:
    """Validates data against data contracts."""

    def __init__(self, registry: SkillRegistry):
        """Initialize with skill registry."""
        self.registry = registry

    def validate(self, data: Dict[str, Any], contract_id: str) -> tuple[bool, Optional[str]]:
        """
        Validate data against a contract.

        Returns:
            (is_valid, error_message)
        """
        contract = self.registry.get_data_contract(contract_id)
        if not contract:
            return False, f"Contract not found: {contract_id}"

        try:
            jsonschema.validate(data, contract)
            return True, None
        except jsonschema.ValidationError as e:
            return False, str(e)


class SkillExecutor:
    """Executes individual skills."""

    def __init__(self, registry: SkillRegistry, validator: DataContractValidator):
        """Initialize with registry and validator."""
        self.registry = registry
        self.validator = validator
        self.logger = logging.getLogger(__name__)

    async def execute(self, skill_id: str, inputs: Dict[str, Any],
                      skill_callable: Callable) -> StepResult:
        """
        Execute a single skill.

        Args:
            skill_id: ID of the skill to execute
            inputs: Input data for the skill
            skill_callable: Async callable that executes the skill

        Returns:
            StepResult with execution details
        """
        skill = self.registry.get_skill(skill_id)
        if not skill:
            return StepResult(
                step_id=0,
                skill_id=skill_id,
                status=ExecutionStatus.FAILED,
                inputs=inputs,
                error=f"Skill not found: {skill_id}"
            )

        # Validate inputs against data contracts
        for input_spec in skill.get('inputs', []):
            contract_id = input_spec.get('schema')
            if contract_id:
                is_valid, error = self.validator.validate(inputs, contract_id)
                if not is_valid:
                    return StepResult(
                        step_id=0,
                        skill_id=skill_id,
                        status=ExecutionStatus.FAILED,
                        inputs=inputs,
                        error=f"Input validation failed: {error}"
                    )

        # Execute the skill
        try:
            start_time = datetime.now()
            outputs = await skill_callable(inputs)
            execution_time = (datetime.now() - start_time).total_seconds() * 1000

            # Validate outputs against data contracts
            for output_spec in skill.get('outputs', []):
                contract_id = output_spec.get('schema')
                if contract_id:
                    is_valid, error = self.validator.validate(outputs, contract_id)
                    if not is_valid:
                        return StepResult(
                            step_id=0,
                            skill_id=skill_id,
                            status=ExecutionStatus.FAILED,
                            inputs=inputs,
                            error=f"Output validation failed: {error}",
                            execution_time_ms=execution_time
                        )

            return StepResult(
                step_id=0,
                skill_id=skill_id,
                status=ExecutionStatus.SUCCESS,
                inputs=inputs,
                outputs=outputs,
                execution_time_ms=execution_time
            )

        except Exception as e:
            execution_time = (datetime.now() - start_time).total_seconds() * 1000
            return StepResult(
                step_id=0,
                skill_id=skill_id,
                status=ExecutionStatus.FAILED,
                inputs=inputs,
                error=str(e),
                execution_time_ms=execution_time
            )


class WorkflowOrchestrator:
    """Orchestrates multi-skill workflows."""

    def __init__(self, registry_path: str):
        """Initialize with path to skill registry."""
        self.registry = SkillRegistry(registry_path)
        self.validator = DataContractValidator(self.registry)
        self.executor = SkillExecutor(self.registry, self.validator)
        self.logger = logging.getLogger(__name__)
        self.skill_callables: Dict[str, Callable] = {}

    def register_skill(self, skill_id: str, callable_func: Callable) -> None:
        """Register a callable for a skill."""
        self.skill_callables[skill_id] = callable_func

    async def execute_workflow(self, workflow_config: Dict[str, Any],
                               initial_input: Dict[str, Any]) -> WorkflowExecution:
        """
        Execute a workflow based on configuration.

        Args:
            workflow_config: Workflow configuration (from integration_patterns.md)
            initial_input: Initial input data for the workflow

        Returns:
            WorkflowExecution with complete execution record
        """
        workflow_id = workflow_config.get('id', 'unknown')
        workflow_name = workflow_config.get('name', 'Unnamed Workflow')
        pattern = workflow_config.get('pattern', 'sequential')

        execution = WorkflowExecution(
            workflow_id=workflow_id,
            workflow_name=workflow_name,
            status=ExecutionStatus.RUNNING,
            steps=[],
            inputs=initial_input,
            started_at=datetime.now().isoformat()
        )

        try:
            if pattern == 'sequential':
                await self._execute_sequential(workflow_config, execution, initial_input)
            elif pattern == 'parallel':
                await self._execute_parallel(workflow_config, execution, initial_input)
            elif pattern == 'conditional':
                await self._execute_conditional(workflow_config, execution, initial_input)
            else:
                raise ValueError(f"Unknown pattern: {pattern}")

            execution.status = ExecutionStatus.SUCCESS
            execution.completed_at = datetime.now().isoformat()

        except Exception as e:
            execution.status = ExecutionStatus.FAILED
            execution.error = str(e)
            execution.completed_at = datetime.now().isoformat()
            self.logger.error(f"Workflow execution failed: {e}")

        return execution

    async def _execute_sequential(self, config: Dict[str, Any],
                                  execution: WorkflowExecution,
                                  initial_input: Dict[str, Any]) -> None:
        """Execute workflow steps sequentially."""
        step_results = {}
        current_input = initial_input

        for step_config in config.get('steps', []):
            step_id = step_config['step']
            skill_id = step_config['skill']

            # Prepare inputs for this step
            step_inputs = self._prepare_step_inputs(step_config, step_results, current_input)

            # Execute the skill
            skill_callable = self.skill_callables.get(skill_id)
            if not skill_callable:
                result = StepResult(
                    step_id=step_id,
                    skill_id=skill_id,
                    status=ExecutionStatus.FAILED,
                    inputs=step_inputs,
                    error=f"No callable registered for skill: {skill_id}"
                )
            else:
                result = await self.executor.execute(skill_id, step_inputs, skill_callable)

            result.step_id = step_id
            execution.steps.append(result)
            step_results[step_id] = result

            # Stop on failure if configured
            if result.status == ExecutionStatus.FAILED:
                if config.get('error_handling') == 'fail_fast':
                    raise Exception(f"Step {step_id} failed: {result.error}")

            current_input = result.outputs or {}

        execution.outputs = current_input

    async def _execute_parallel(self, config: Dict[str, Any],
                                execution: WorkflowExecution,
                                initial_input: Dict[str, Any]) -> None:
        """Execute workflow steps in parallel where possible."""
        step_results = {}
        steps_by_group = {}

        # Group steps by parallel_group
        for step_config in config.get('steps', []):
            group = step_config.get('parallel_group', step_config['step'])
            if group not in steps_by_group:
                steps_by_group[group] = []
            steps_by_group[group].append(step_config)

        # Execute groups sequentially, but steps within a group in parallel
        for group in sorted(steps_by_group.keys()):
            tasks = []
            for step_config in steps_by_group[group]:
                step_id = step_config['step']
                skill_id = step_config['skill']

                step_inputs = self._prepare_step_inputs(step_config, step_results, initial_input)
                skill_callable = self.skill_callables.get(skill_id)

                if skill_callable:
                    tasks.append(self.executor.execute(skill_id, step_inputs, skill_callable))
                else:
                    tasks.append(asyncio.sleep(0))  # Placeholder

            # Execute all tasks in parallel
            results = await asyncio.gather(*tasks)

            # Store results
            for i, step_config in enumerate(steps_by_group[group]):
                result = results[i]
                result.step_id = step_config['step']
                execution.steps.append(result)
                step_results[step_config['step']] = result

    async def _execute_conditional(self, config: Dict[str, Any],
                                   execution: WorkflowExecution,
                                   initial_input: Dict[str, Any]) -> None:
        """Execute workflow with conditional branching."""
        step_results = {}
        current_input = initial_input

        for step_config in config.get('steps', []):
            # Check condition
            condition = step_config.get('condition')
            if condition:
                # Evaluate condition (simplified - in production, use safer evaluation)
                if not self._evaluate_condition(condition, step_results):
                    continue

            step_id = step_config['step']
            skill_id = step_config['skill']

            step_inputs = self._prepare_step_inputs(step_config, step_results, current_input)
            skill_callable = self.skill_callables.get(skill_id)

            if not skill_callable:
                result = StepResult(
                    step_id=step_id,
                    skill_id=skill_id,
                    status=ExecutionStatus.FAILED,
                    inputs=step_inputs,
                    error=f"No callable registered for skill: {skill_id}"
                )
            else:
                result = await self.executor.execute(skill_id, step_inputs, skill_callable)

            result.step_id = step_id
            execution.steps.append(result)
            step_results[step_id] = result
            current_input = result.outputs or {}

        execution.outputs = current_input

    def _prepare_step_inputs(self, step_config: Dict[str, Any],
                            step_results: Dict[int, StepResult],
                            initial_input: Dict[str, Any]) -> Dict[str, Any]:
        """Prepare inputs for a step by resolving references to previous steps."""
        inputs = {}
        input_config = step_config.get('inputs', {})

        for key, value in input_config.items():
            if isinstance(value, str) and value.startswith('{{') and value.endswith('}}'):
                # Resolve reference
                ref = value[2:-2].strip()
                inputs[key] = self._resolve_reference(ref, step_results, initial_input)
            else:
                inputs[key] = value

        return inputs

    def _resolve_reference(self, ref: str, step_results: Dict[int, StepResult],
                          initial_input: Dict[str, Any]) -> Any:
        """Resolve a reference like 'steps[1].outputs.ticket' or 'input'."""
        if ref == 'input':
            return initial_input

        # Parse reference like "steps[1].outputs.ticket"
        if ref.startswith('steps['):
            # Extract step number and path
            parts = ref.split(']', 1)
            step_num = int(parts[0][6:])
            path = parts[1].lstrip('.') if len(parts) > 1 else ''

            if step_num in step_results:
                result = step_results[step_num]
                if path == 'outputs':
                    return result.outputs
                elif path.startswith('outputs.'):
                    obj = result.outputs
                    for key in path.split('.')[1:]:
                        obj = obj.get(key) if isinstance(obj, dict) else None
                    return obj

        return None

    def _evaluate_condition(self, condition: str,
                           step_results: Dict[int, StepResult]) -> bool:
        """Evaluate a condition string (simplified)."""
        # In production, use a safer evaluation method
        try:
            # Replace references with actual values
            eval_str = condition
            for step_id, result in step_results.items():
                eval_str = eval_str.replace(
                    f"steps[{step_id}].outputs",
                    json.dumps(result.outputs)
                )
            return eval(eval_str)
        except Exception as e:
            self.logger.warning(f"Failed to evaluate condition: {e}")
            return False


# Example usage
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    # Initialize orchestrator
    orchestrator = WorkflowOrchestrator('references/skill_registry.json')

    # Register skill callables (these would be actual skill implementations)
    async def mock_skill(inputs: Dict[str, Any]) -> Dict[str, Any]:
        await asyncio.sleep(0.1)
        return {"result": "success", "data": inputs}

    orchestrator.register_skill('support-intake', mock_skill)
    orchestrator.register_skill('support-triage', mock_skill)
    orchestrator.register_skill('sentiment-analysis', mock_skill)

    # Define a workflow
    workflow_config = {
        "id": "support-pipeline-1",
        "name": "Support Processing Pipeline",
        "pattern": "sequential",
        "steps": [
            {
                "step": 1,
                "skill": "support-intake",
                "inputs": {"raw_ticket": "{{input}}"}
            },
            {
                "step": 2,
                "skill": "support-triage",
                "inputs": {"ticket": "{{steps[1].outputs}}"},
                "depends_on": [1]
            }
        ]
    }

    # Execute workflow
    async def main():
        result = await orchestrator.execute_workflow(
            workflow_config,
            {"raw_ticket": "Customer can't login"}
        )
        print(json.dumps(result.to_dict(), indent=2))

    asyncio.run(main())
