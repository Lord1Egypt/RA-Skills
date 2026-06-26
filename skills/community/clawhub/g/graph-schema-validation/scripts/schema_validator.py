#!/usr/bin/env python3
"""
Minimal graph schema validator for graph-schema-validation skill.
Provides core functionality for schema and data validation.
"""

from typing import List, Dict, Optional, Any
from dataclasses import dataclass, field
from enum import Enum


class ViolationType(Enum):
    """Types of validation violations."""
    MISSING_PROPERTY = "Missing Required Property"
    INVALID_TYPE = "Invalid Property Type"
    CONSTRAINT_VIOLATION = "Constraint Violation"
    RELATIONSHIP_ERROR = "Relationship Error"
    CARDINALITY_ERROR = "Cardinality Violation"
    ORPHAN_NODE = "Orphan Node"
    DUPLICATE_VALUE = "Duplicate Value"
    BROKEN_REFERENCE = "Broken Reference"


@dataclass
class Violation:
    """Represents a validation violation."""
    violation_type: ViolationType
    node_id: str
    description: str
    severity: str = "ERROR"  # ERROR, WARNING, INFO
    suggestion: str = ""

    def __repr__(self):
        return f"[{self.severity}] {self.violation_type.value}: {self.description}"


@dataclass
class ValidationRule:
    """Represents a validation rule."""
    name: str
    rule_type: str  # 'required_property', 'unique_constraint', etc.
    target_label: Optional[str] = None
    property_name: Optional[str] = None
    expected_type: Optional[str] = None
    min_count: int = 0
    max_count: Optional[int] = None
    allowed_values: List[str] = field(default_factory=list)


class SchemaValidator:
    """Validate graph schemas and data."""

    def __init__(self, schema_name: str = ""):
        """Initialize validator."""
        self.schema_name = schema_name
        self.rules: List[ValidationRule] = []
        self.violations: List[Violation] = []
        self.data: List[Dict] = []

    def add_rule(self, rule: ValidationRule) -> None:
        """Add a validation rule."""
        self.rules.append(rule)

    def add_required_property(self, label: str, property_name: str,
                             expected_type: str = "string") -> None:
        """Add rule for required property."""
        rule = ValidationRule(
            name=f"{label}.{property_name} required",
            rule_type="required_property",
            target_label=label,
            property_name=property_name,
            expected_type=expected_type,
            min_count=1
        )
        self.add_rule(rule)

    def add_unique_constraint(self, label: str, property_name: str) -> None:
        """Add rule for unique constraint."""
        rule = ValidationRule(
            name=f"{label}.{property_name} unique",
            rule_type="unique_constraint",
            target_label=label,
            property_name=property_name
        )
        self.add_rule(rule)

    def add_cardinality_constraint(self, label: str, property_name: str,
                                   min_count: int = 0,
                                   max_count: Optional[int] = None) -> None:
        """Add rule for cardinality constraint."""
        rule = ValidationRule(
            name=f"{label}.{property_name} cardinality",
            rule_type="cardinality_constraint",
            target_label=label,
            property_name=property_name,
            min_count=min_count,
            max_count=max_count
        )
        self.add_rule(rule)

    def add_enum_constraint(self, label: str, property_name: str,
                           allowed_values: List[str]) -> None:
        """Add rule for enum constraint."""
        rule = ValidationRule(
            name=f"{label}.{property_name} enum",
            rule_type="enum_constraint",
            target_label=label,
            property_name=property_name,
            allowed_values=allowed_values
        )
        self.add_rule(rule)

    def load_data(self, nodes: List[Dict]) -> None:
        """Load data to validate."""
        self.data = nodes

    def validate(self) -> bool:
        """
        Validate data against all rules.

        Returns:
            True if all validations pass, False otherwise
        """
        self.violations = []

        for rule in self.rules:
            if rule.rule_type == "required_property":
                self._validate_required_property(rule)
            elif rule.rule_type == "unique_constraint":
                self._validate_unique_constraint(rule)
            elif rule.rule_type == "enum_constraint":
                self._validate_enum_constraint(rule)
            elif rule.rule_type == "cardinality_constraint":
                self._validate_cardinality_constraint(rule)

        return len(self.violations) == 0

    def _validate_required_property(self, rule: ValidationRule) -> None:
        """Check for missing required properties."""
        for node in self.data:
            if node.get('label') == rule.target_label:
                if rule.property_name not in node or node[rule.property_name] is None:
                    violation = Violation(
                        violation_type=ViolationType.MISSING_PROPERTY,
                        node_id=node.get('id', 'unknown'),
                        description=f"Missing required property: {rule.property_name}",
                        severity="ERROR",
                        suggestion=f"Add {rule.property_name} to {rule.target_label}"
                    )
                    self.violations.append(violation)

    def _validate_unique_constraint(self, rule: ValidationRule) -> None:
        """Check for duplicate values."""
        values = {}
        for node in self.data:
            if node.get('label') == rule.target_label:
                prop_value = node.get(rule.property_name)
                if prop_value:
                    if prop_value in values:
                        violation = Violation(
                            violation_type=ViolationType.DUPLICATE_VALUE,
                            node_id=node.get('id', 'unknown'),
                            description=f"Duplicate {rule.property_name}: {prop_value}",
                            severity="ERROR",
                            suggestion="Ensure property values are unique"
                        )
                        self.violations.append(violation)
                    else:
                        values[prop_value] = node.get('id')

    def _validate_enum_constraint(self, rule: ValidationRule) -> None:
        """Check for allowed values."""
        for node in self.data:
            if node.get('label') == rule.target_label:
                prop_value = node.get(rule.property_name)
                if prop_value and prop_value not in rule.allowed_values:
                    violation = Violation(
                        violation_type=ViolationType.CONSTRAINT_VIOLATION,
                        node_id=node.get('id', 'unknown'),
                        description=f"Invalid value: {prop_value}",
                        severity="ERROR",
                        suggestion=f"Use one of: {', '.join(rule.allowed_values)}"
                    )
                    self.violations.append(violation)

    def _validate_cardinality_constraint(self, rule: ValidationRule) -> None:
        """Check cardinality constraints."""
        for node in self.data:
            if node.get('label') == rule.target_label:
                # This is a simplified check
                prop_value = node.get(rule.property_name)
                if isinstance(prop_value, list):
                    count = len(prop_value)
                    if count < rule.min_count:
                        violation = Violation(
                            violation_type=ViolationType.CARDINALITY_ERROR,
                            node_id=node.get('id', 'unknown'),
                            description=f"Minimum {rule.min_count} values required, found {count}",
                            severity="ERROR"
                        )
                        self.violations.append(violation)
                    if rule.max_count and count > rule.max_count:
                        violation = Violation(
                            violation_type=ViolationType.CARDINALITY_ERROR,
                            node_id=node.get('id', 'unknown'),
                            description=f"Maximum {rule.max_count} values allowed, found {count}",
                            severity="ERROR"
                        )
                        self.violations.append(violation)

    def get_violations(self) -> List[Violation]:
        """Get list of violations."""
        return self.violations

    def get_report(self) -> Dict:
        """Generate validation report."""
        errors = [v for v in self.violations if v.severity == "ERROR"]
        warnings = [v for v in self.violations if v.severity == "WARNING"]

        return {
            'schema_name': self.schema_name,
            'total_nodes': len(self.data),
            'total_violations': len(self.violations),
            'errors': len(errors),
            'warnings': len(warnings),
            'conformance': 100 * (1 - len(self.violations) / max(len(self.data), 1)),
            'violations': [
                {
                    'type': v.violation_type.value,
                    'node_id': v.node_id,
                    'description': v.description,
                    'severity': v.severity,
                    'suggestion': v.suggestion
                }
                for v in self.violations
            ]
        }

    def print_report(self) -> None:
        """Print validation report."""
        report = self.get_report()

        print(f"\n{'='*60}")
        print(f"VALIDATION REPORT: {report['schema_name']}")
        print(f"{'='*60}")
        print(f"\nTotal Nodes: {report['total_nodes']}")
        print(f"Violations: {report['total_violations']}")
        print(f"Conformance: {report['conformance']:.1f}%")

        if report['violations']:
            print(f"\nVIOLATIONS ({len(report['violations'])}):")
            for i, v in enumerate(report['violations'], 1):
                print(f"\n{i}. [{v['severity']}] {v['type']}")
                print(f"   Node: {v['node_id']}")
                print(f"   Issue: {v['description']}")
                if v['suggestion']:
                    print(f"   Fix: {v['suggestion']}")
        else:
            print("\n✓ No violations found!")


if __name__ == "__main__":
    # Example: Validate university schema
    validator = SchemaValidator("University")

    # Add rules
    validator.add_required_property("Student", "student_id")
    validator.add_required_property("Student", "name")
    validator.add_unique_constraint("Student", "student_id")
    validator.add_enum_constraint("Course", "status", ["Active", "Inactive", "Archived"])

    # Load sample data
    data = [
        {"id": "S001", "label": "Student", "student_id": "001", "name": "Alice"},
        {"id": "S002", "label": "Student", "student_id": "002", "name": "Bob"},
        {"id": "S003", "label": "Student", "student_id": "001", "name": "Charlie"},  # Duplicate!
        {"id": "S004", "label": "Student", "name": "David"},  # Missing student_id!
        {"id": "C001", "label": "Course", "course_code": "CS101", "status": "Active"},
        {"id": "C002", "label": "Course", "course_code": "CS102", "status": "Invalid"},  # Invalid!
    ]

    validator.load_data(data)
    validator.validate()
    validator.print_report()

