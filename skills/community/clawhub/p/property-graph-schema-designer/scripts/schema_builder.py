#!/usr/bin/env python3
"""
Minimal property graph schema builder for property-graph-schema-designer skill.
Provides core functionality for Neo4j schema design.
"""

from typing import List, Dict, Optional, Set
from dataclasses import dataclass, field
from enum import Enum


class PropertyType(Enum):
    """Property data types."""
    STRING = "String"
    INTEGER = "Integer"
    FLOAT = "Float"
    BOOLEAN = "Boolean"
    DATE = "Date"


@dataclass
class Property:
    """Represents a node or relationship property."""
    name: str
    prop_type: PropertyType = PropertyType.STRING
    unique: bool = False
    indexed: bool = False

    def __repr__(self):
        unique_str = " (UNIQUE)" if self.unique else ""
        indexed_str = " (INDEX)" if self.indexed else ""
        return f"{self.name}: {self.prop_type.value}{unique_str}{indexed_str}"


@dataclass
class NodeLabel:
    """Represents a node label in property graph."""
    name: str
    properties: List[Property] = field(default_factory=list)
    description: Optional[str] = None

    def add_property(self, prop: Property) -> None:
        """Add property to node label."""
        self.properties.append(prop)


@dataclass
class Relationship:
    """Represents a relationship type."""
    source: str
    rel_type: str
    target: str
    properties: List[Property] = field(default_factory=list)

    def __repr__(self):
        props_str = ""
        if self.properties:
            props_str = " {" + ", ".join(p.name for p in self.properties) + "}"
        return f"({self.source})-[:{self.rel_type}{props_str}]->({self.target})"


class SchemaBuilder:
    """Build Neo4j property graph schemas."""

    def __init__(self, domain: str = ""):
        """Initialize schema builder."""
        self.domain = domain
        self.nodes: Dict[str, NodeLabel] = {}
        self.relationships: List[Relationship] = []
        self.constraints: List[str] = []
        self.indexes: List[str] = []

    def add_node(self, label: str, description: str = None) -> NodeLabel:
        """Add a node label to schema."""
        node = NodeLabel(label, description=description)
        self.nodes[label] = node
        return node

    def add_property_to_node(self, node_label: str, prop_name: str,
                           prop_type: PropertyType = PropertyType.STRING,
                           unique: bool = False, indexed: bool = False) -> None:
        """Add property to a node label."""
        if node_label not in self.nodes:
            self.add_node(node_label)

        prop = Property(prop_name, prop_type, unique, indexed)
        self.nodes[node_label].add_property(prop)

        # Auto-create constraint for unique properties
        if unique:
            self.add_constraint(f"{node_label}.{prop_name} UNIQUE")

        # Auto-create index
        if indexed:
            self.add_index(f"ON (:{node_label})({prop_name})")

    def add_relationship(self, source: str, rel_type: str, target: str,
                        properties: List[Property] = None) -> Relationship:
        """Add a relationship type to schema."""
        rel = Relationship(source, rel_type, target, properties or [])
        self.relationships.append(rel)
        return rel

    def add_constraint(self, constraint: str) -> None:
        """Add constraint to schema."""
        self.constraints.append(f"CREATE CONSTRAINT ON {constraint} IF NOT EXISTS")

    def add_index(self, index: str) -> None:
        """Add index to schema."""
        self.indexes.append(f"CREATE INDEX {index} IF NOT EXISTS")

    def get_cypher_nodes(self) -> str:
        """Generate Cypher CREATE NODE statements."""
        output = []
        for label, node in self.nodes.items():
            output.append(f"\n-- {label}")
            if node.description:
                output.append(f"-- {node.description}")
            output.append(f"CREATE (:{label})")
        return "\n".join(output)

    def get_cypher_constraints(self) -> str:
        """Generate Cypher constraint statements."""
        output = ["-- CONSTRAINTS"]
        for constraint in self.constraints:
            output.append(constraint)
        return "\n".join(output)

    def get_cypher_indexes(self) -> str:
        """Generate Cypher index statements."""
        output = ["-- INDEXES"]
        for index in self.indexes:
            output.append(index)
        return "\n".join(output)

    def get_schema_summary(self) -> Dict:
        """Get schema statistics."""
        return {
            'domain': self.domain,
            'node_labels': len(self.nodes),
            'relationships': len(self.relationships),
            'total_properties': sum(len(n.properties) for n in self.nodes.values()),
            'constraints': len(self.constraints),
            'indexes': len(self.indexes),
            'nodes': list(self.nodes.keys()),
            'relationship_types': list(set(r.rel_type for r in self.relationships))
        }

    def to_dict(self) -> Dict:
        """Export schema as dictionary."""
        return {
            'domain': self.domain,
            'nodes': {
                label: {
                    'properties': [p.__dict__ for p in node.properties],
                    'description': node.description
                }
                for label, node in self.nodes.items()
            },
            'relationships': [
                {
                    'source': r.source,
                    'type': r.rel_type,
                    'target': r.target,
                    'properties': [p.__dict__ for p in r.properties]
                }
                for r in self.relationships
            ],
            'constraints': self.constraints,
            'indexes': self.indexes
        }

    def print_schema(self) -> None:
        """Print schema overview."""
        print(f"\n{'='*60}")
        print(f"PROPERTY GRAPH SCHEMA: {self.domain}")
        print(f"{'='*60}")

        print(f"\nNODE LABELS ({len(self.nodes)}):")
        for label, node in self.nodes.items():
            print(f"  {label}")
            for prop in node.properties:
                print(f"    └─ {prop}")

        print(f"\nRELATIONSHIPS ({len(self.relationships)}):")
        for rel in self.relationships:
            print(f"  {rel}")

        if self.constraints:
            print(f"\nCONSTRAINTS ({len(self.constraints)}):")
            for constraint in self.constraints:
                print(f"  {constraint}")

        if self.indexes:
            print(f"\nINDEXES ({len(self.indexes)}):")
            for index in self.indexes:
                print(f"  {index}")


if __name__ == "__main__":
    # Example: Build university schema
    builder = SchemaBuilder("University")

    # Add nodes
    student = builder.add_node("Student", "University students")
    builder.add_property_to_node("Student", "student_id", PropertyType.STRING, unique=True)
    builder.add_property_to_node("Student", "name", PropertyType.STRING, indexed=True)
    builder.add_property_to_node("Student", "email", PropertyType.STRING)
    builder.add_property_to_node("Student", "enrollment_year", PropertyType.INTEGER)

    professor = builder.add_node("Professor", "Teaching staff")
    builder.add_property_to_node("Professor", "professor_id", PropertyType.STRING, unique=True)
    builder.add_property_to_node("Professor", "name", PropertyType.STRING, indexed=True)
    builder.add_property_to_node("Professor", "research_area", PropertyType.STRING)

    course = builder.add_node("Course", "Academic courses")
    builder.add_property_to_node("Course", "course_code", PropertyType.STRING, unique=True)
    builder.add_property_to_node("Course", "title", PropertyType.STRING, indexed=True)
    builder.add_property_to_node("Course", "credits", PropertyType.INTEGER)

    department = builder.add_node("Department", "Academic departments")
    builder.add_property_to_node("Department", "dept_id", PropertyType.STRING, unique=True)
    builder.add_property_to_node("Department", "name", PropertyType.STRING)
    builder.add_property_to_node("Department", "budget", PropertyType.FLOAT)

    # Add relationships
    builder.add_relationship("Student", "ENROLLED_IN", "Course",
                           [Property("semester"), Property("grade")])
    builder.add_relationship("Professor", "TEACHES", "Course",
                           [Property("semester")])
    builder.add_relationship("Professor", "WORKS_IN", "Department")
    builder.add_relationship("Department", "OFFERS", "Course")
    builder.add_relationship("Course", "REQUIRES", "Course")

    # Print schema
    builder.print_schema()

    # Print statistics
    print(f"\n{'='*60}")
    print("SCHEMA STATISTICS")
    print(f"{'='*60}")
    stats = builder.get_schema_summary()
    for key, value in stats.items():
        print(f"{key}: {value}")

