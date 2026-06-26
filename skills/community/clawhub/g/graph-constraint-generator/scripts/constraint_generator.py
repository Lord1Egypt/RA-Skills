#!/usr/bin/env python3
"""
Minimal constraint generator for graph-constraint-generator skill.
Provides core functionality for generating graph constraints.
"""

from typing import List, Dict, Optional, Set
from dataclasses import dataclass, field
from enum import Enum


class ConstraintType(Enum):
    """Types of graph constraints."""
    UNIQUE = "UNIQUE"
    REQUIRED = "REQUIRED"
    CARDINALITY = "CARDINALITY"
    DOMAIN_RANGE = "DOMAIN_RANGE"
    TYPE = "TYPE"
    RELATIONSHIP = "RELATIONSHIP"


@dataclass
class Constraint:
    """Represents a graph constraint."""
    constraint_type: ConstraintType
    target: str  # Label or property name
    property_name: Optional[str] = None
    min_count: int = 0
    max_count: Optional[int] = None
    description: str = ""

    def __repr__(self):
        if self.constraint_type == ConstraintType.UNIQUE:
            return f"{self.target}.{self.property_name} UNIQUE"
        elif self.constraint_type == ConstraintType.REQUIRED:
            return f"{self.target}.{self.property_name} REQUIRED"
        elif self.constraint_type == ConstraintType.CARDINALITY:
            max_str = str(self.max_count) if self.max_count else "∞"
            return f"{self.target}: [{self.min_count}, {max_str}]"
        return f"[{self.constraint_type.value}] {self.target}"


class ConstraintGenerator:
    """Generate constraints for graph schemas."""

    def __init__(self, domain: str = ""):
        """Initialize constraint generator."""
        self.domain = domain
        self.constraints: List[Constraint] = []
        self.labels: Set[str] = set()
        self.relationships: List[tuple] = []

    def add_label(self, label: str) -> None:
        """Register a node label."""
        self.labels.add(label)

    def add_unique_constraint(self, label: str, property_name: str) -> None:
        """Add unique constraint."""
        constraint = Constraint(
            constraint_type=ConstraintType.UNIQUE,
            target=label,
            property_name=property_name,
            description=f"{property_name} must be unique for {label}"
        )
        self.constraints.append(constraint)

    def add_required_property(self, label: str, property_name: str) -> None:
        """Add required property constraint."""
        constraint = Constraint(
            constraint_type=ConstraintType.REQUIRED,
            target=label,
            property_name=property_name,
            min_count=1,
            description=f"{property_name} is required for {label}"
        )
        self.constraints.append(constraint)

    def add_cardinality_constraint(self, label: str, rel_type: str, target: str,
                                   min_count: int = 0,
                                   max_count: Optional[int] = None) -> None:
        """Add cardinality constraint on relationship."""
        constraint = Constraint(
            constraint_type=ConstraintType.CARDINALITY,
            target=f"({label})-[:{rel_type}]->({target})",
            min_count=min_count,
            max_count=max_count,
            description=f"Cardinality [{min_count}, {max_count or 'unlimited'}]"
        )
        self.constraints.append(constraint)
        self.relationships.append((label, rel_type, target))

    def add_domain_range_constraint(self, property_name: str,
                                   domain: str, range_class: str) -> None:
        """Add domain/range constraint (for RDF/OWL)."""
        constraint = Constraint(
            constraint_type=ConstraintType.DOMAIN_RANGE,
            target=property_name,
            property_name=f"{domain} -> {range_class}",
            description=f"Domain: {domain}, Range: {range_class}"
        )
        self.constraints.append(constraint)

    def generate_cypher_constraints(self) -> List[str]:
        """Generate Neo4j Cypher constraint statements."""
        statements = []

        for constraint in self.constraints:
            if constraint.constraint_type == ConstraintType.UNIQUE:
                stmt = f"CREATE CONSTRAINT {constraint.target}_{constraint.property_name}_unique " \
                       f"ON ({constraint.target[0].lower()}:{constraint.target}) " \
                       f"REQUIRE {constraint.target[0].lower()}.{constraint.property_name} IS UNIQUE"
                statements.append(stmt)

            elif constraint.constraint_type == ConstraintType.REQUIRED:
                # Cypher doesn't support NOT NULL constraints directly, use validation query
                stmt = f"MATCH ({constraint.target[0].lower()}:{constraint.target}) " \
                       f"WHERE {constraint.target[0].lower()}.{constraint.property_name} IS NULL " \
                       f"RETURN {constraint.target[0].lower()}  -- Should be empty"
                statements.append(stmt)

        return statements

    def generate_shacl_shapes(self, namespace_uri: str = "http://example.org/") -> List[str]:
        """Generate SHACL shapes for RDF/OWL validation."""
        shapes = []
        shapes.append("@prefix sh: <http://www.w3.org/ns/shacl#> .")
        shapes.append("@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .")
        shapes.append("")

        for label in self.labels:
            shape_name = f"{label}Shape"
            shapes.append(f":{shape_name} a sh:NodeShape ;")
            shapes.append(f"  sh:targetClass :{label} ;")

            # Add property constraints
            for constraint in self.constraints:
                if constraint.target == label and constraint.constraint_type in \
                   [ConstraintType.REQUIRED, ConstraintType.UNIQUE]:
                    shapes.append(f"  sh:property [")
                    shapes.append(f"    sh:path :{constraint.property_name} ;")
                    if constraint.constraint_type == ConstraintType.REQUIRED:
                        shapes.append(f"    sh:minCount 1")
                    else:
                        shapes.append(f"    sh:maxCount 1")
                    shapes.append(f"  ] ;")

            shapes[-1] = shapes[-1].rstrip(" ;") + " ."

        return shapes

    def get_constraints_summary(self) -> Dict:
        """Get summary of all constraints."""
        summary = {
            'domain': self.domain,
            'total_constraints': len(self.constraints),
            'labels': len(self.labels),
            'relationships': len(self.relationships),
            'constraints_by_type': {}
        }

        for constraint_type in ConstraintType:
            count = sum(1 for c in self.constraints if c.constraint_type == constraint_type)
            if count > 0:
                summary['constraints_by_type'][constraint_type.value] = count

        return summary

    def print_constraints(self) -> None:
        """Print all constraints."""
        print(f"\n{'='*60}")
        print(f"CONSTRAINTS: {self.domain}")
        print(f"{'='*60}")

        if not self.constraints:
            print("No constraints defined")
            return

        by_type = {}
        for constraint in self.constraints:
            ctype = constraint.constraint_type.value
            if ctype not in by_type:
                by_type[ctype] = []
            by_type[ctype].append(constraint)

        for ctype in sorted(by_type.keys()):
            print(f"\n{ctype} CONSTRAINTS:")
            for constraint in by_type[ctype]:
                print(f"  {constraint}")


if __name__ == "__main__":
    # Example: Generate university constraints
    gen = ConstraintGenerator("University")

    # Add labels
    gen.add_label("Student")
    gen.add_label("Professor")
    gen.add_label("Course")
    gen.add_label("Department")

    # Add unique constraints
    gen.add_unique_constraint("Student", "student_id")
    gen.add_unique_constraint("Professor", "professor_id")
    gen.add_unique_constraint("Course", "course_code")
    gen.add_unique_constraint("Department", "dept_id")

    # Add required constraints
    gen.add_required_property("Student", "name")
    gen.add_required_property("Course", "title")
    gen.add_required_property("Department", "name")

    # Add cardinality constraints
    gen.add_cardinality_constraint("Student", "ENROLLED_IN", "Course", min_count=1, max_count=10)
    gen.add_cardinality_constraint("Professor", "TEACHES", "Course", min_count=1, max_count=5)
    gen.add_cardinality_constraint("Department", "MANAGES", "Course")

    # Print constraints
    gen.print_constraints()

    # Print summary
    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    summary = gen.get_constraints_summary()
    for key, value in summary.items():
        print(f"{key}: {value}")

    # Generate Cypher
    print(f"\n{'='*60}")
    print("CYPHER CONSTRAINTS")
    print(f"{'='*60}")
    for stmt in gen.generate_cypher_constraints():
        print(stmt)

