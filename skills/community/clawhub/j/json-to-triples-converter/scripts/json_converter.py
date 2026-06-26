#!/usr/bin/env python3
"""
JSON to Triples Converter implementation for json_to_triples_converter skill.
Provides core functionality for converting JSON to RDF triples and semantic formats.
"""

from typing import Dict, List, Optional, Any, Set, Tuple
from dataclasses import dataclass, field
from enum import Enum
import json
import hashlib
from datetime import datetime
from urllib.parse import quote


class OutputFormat(Enum):
    """Output formats for RDF triples."""
    TURTLE = "turtle"
    NTRIPLES = "ntriples"
    JSONLD = "jsonld"
    GRAPH_JSON = "graph_json"


class DataType(Enum):
    """RDF data types."""
    STRING = "xsd:string"
    INTEGER = "xsd:integer"
    DECIMAL = "xsd:decimal"
    BOOLEAN = "xsd:boolean"
    DATE = "xsd:date"
    DATETIME = "xsd:dateTime"
    URI = "xsd:anyURI"


@dataclass
class Triple:
    """Represents an RDF triple."""
    subject: str
    predicate: str
    obj: str
    object_type: str = "literal"  # "literal" or "uri"
    language_tag: Optional[str] = None
    data_type: Optional[str] = None

    def to_turtle(self, namespaces: Dict[str, str]) -> str:
        """Convert to Turtle format."""
        subject_str = self._format_uri(self.subject, namespaces)
        predicate_str = self._format_uri(self.predicate, namespaces)

        if self.object_type == "uri":
            obj_str = self._format_uri(self.obj, namespaces)
        elif self.language_tag:
            obj_str = f'"{self.obj}"@{self.language_tag}'
        elif self.data_type:
            obj_str = f'"{self.obj}"^^{self.data_type}'
        else:
            obj_str = f'"{self.obj}"'

        return f"{subject_str} {predicate_str} {obj_str}"

    def to_ntriples(self) -> str:
        """Convert to N-Triples format."""
        subject_str = f"<{self.subject}>"
        predicate_str = f"<{self.predicate}>"

        if self.object_type == "uri":
            obj_str = f"<{self.obj}>"
        elif self.language_tag:
            obj_str = f'"{self.obj}"@{self.language_tag}'
        elif self.data_type:
            obj_str = f'"{self.obj}"^^<{self.data_type}>'
        else:
            obj_str = f'"{self.obj}"'

        return f"{subject_str} {predicate_str} {obj_str} ."

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            "subject": self.subject,
            "predicate": self.predicate,
            "object": self.obj,
            "object_type": self.object_type,
            "language_tag": self.language_tag,
            "data_type": self.data_type
        }

    @staticmethod
    def _format_uri(uri: str, namespaces: Dict[str, str]) -> str:
        """Format URI with namespace prefixes."""
        for prefix, namespace in namespaces.items():
            if uri.startswith(namespace):
                local_name = uri[len(namespace):]
                return f"{prefix}:{local_name}"
        return uri


@dataclass
class Namespace:
    """RDF namespace definition."""
    prefix: str
    uri: str


class JSONTriplesConverter:
    """Core JSON to Triples converter."""

    def __init__(self, base_namespace: str = "http://example.org/",
                 output_format: OutputFormat = OutputFormat.TURTLE):
        """Initialize JSON to Triples converter."""
        self.base_namespace = base_namespace
        self.output_format = output_format
        self.namespaces: Dict[str, str] = {
            "ex": base_namespace,
            "foaf": "http://xmlns.com/foaf/0.1/",
            "schema": "http://schema.org/",
            "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
            "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
            "xsd": "http://www.w3.org/2001/XMLSchema#",
            "dcterms": "http://purl.org/dc/terms/"
        }
        self.triples: List[Triple] = []
        self.entities: Dict[str, Dict] = {}
        self.entity_mappings: Dict[str, str] = {}
        self.property_mappings: Dict[str, str] = {}
        self.errors: List[str] = []

    def add_namespace(self, prefix: str, uri: str) -> None:
        """Add a custom namespace."""
        self.namespaces[prefix] = uri

    def add_entity_mapping(self, json_key: str, entity_type: str) -> None:
        """Map JSON key to entity type."""
        self.entity_mappings[json_key] = entity_type

    def add_property_mapping(self, json_key: str, predicate: str) -> None:
        """Map JSON property to RDF predicate."""
        self.property_mappings[json_key] = predicate

    def convert(self, json_data: Dict[str, Any], base_id: str = "") -> List[Triple]:
        """Convert JSON to RDF triples."""
        self.triples.clear()
        self.entities.clear()

        self._process_json(json_data, base_id)
        return self.triples

    def _process_json(self, data: Any, parent_id: str = "", key: str = "") -> str:
        """Process JSON recursively."""
        if isinstance(data, dict):
            # Generate entity ID
            entity_id = self._generate_entity_id(data, parent_id, key)

            # Detect entity type
            entity_type = self._detect_entity_type(key, data)
            if entity_type:
                self._add_type_triple(entity_id, entity_type)

            # Process properties
            for prop_key, prop_value in data.items():
                if isinstance(prop_value, dict):
                    # Nested object - create relationship
                    nested_id = self._process_json(prop_value, entity_id, prop_key)
                    predicate = self._get_predicate(prop_key)
                    self._add_triple(entity_id, predicate, nested_id, object_type="uri")

                elif isinstance(prop_value, list):
                    # Array - create multiple triples
                    for item in prop_value:
                        if isinstance(item, dict):
                            item_id = self._process_json(item, entity_id, prop_key)
                            predicate = self._get_predicate(prop_key)
                            self._add_triple(entity_id, predicate, item_id, object_type="uri")
                        else:
                            predicate = self._get_predicate(prop_key)
                            self._add_literal_triple(entity_id, predicate, str(item))

                else:
                    # Literal property
                    if prop_value is not None:
                        predicate = self._get_predicate(prop_key)
                        self._add_literal_triple(entity_id, predicate, prop_value)

            return entity_id

        elif isinstance(data, list):
            # Process list items
            for item in data:
                self._process_json(item, parent_id, key)
            return parent_id

        else:
            # Scalar value
            return str(data)

    def _generate_entity_id(self, data: Dict, parent_id: str, key: str) -> str:
        """Generate unique URI for entity."""
        # Try to use id field
        if "id" in data:
            entity_id = data["id"]
        elif "name" in data:
            entity_id = self._slugify(str(data["name"]))
        elif key:
            entity_id = key
        else:
            # Generate hash-based ID
            data_str = json.dumps(data, sort_keys=True)
            entity_hash = hashlib.md5(data_str.encode()).hexdigest()[:8]
            entity_id = entity_hash

        return f"{self.base_namespace}entity_{entity_id}"

    def _detect_entity_type(self, key: str, data: Dict) -> Optional[str]:
        """Detect entity type from key and data."""
        if key in self.entity_mappings:
            return self.entity_mappings[key]

        # Auto-detect from common keys
        if "type" in data:
            return f"{self.namespaces['schema']}{data['type']}"

        return None

    def _get_predicate(self, key: str) -> str:
        """Get RDF predicate for JSON key."""
        if key in self.property_mappings:
            return self.property_mappings[key]

        # Default predicate generation
        return f"{self.base_namespace}{self._slugify(key)}"

    def _add_type_triple(self, entity_id: str, entity_type: str) -> None:
        """Add RDF type triple."""
        rdf_type = f"{self.namespaces['rdf']}type"
        self._add_triple(entity_id, rdf_type, entity_type, object_type="uri")

    def _add_literal_triple(self, subject: str, predicate: str,
                           value: Any) -> None:
        """Add literal triple with type inference."""
        data_type = self._infer_data_type(value)

        triple = Triple(
            subject=subject,
            predicate=predicate,
            obj=str(value),
            object_type="literal",
            data_type=data_type
        )
        self.triples.append(triple)

    def _add_triple(self, subject: str, predicate: str, obj: str,
                   object_type: str = "literal") -> None:
        """Add RDF triple."""
        triple = Triple(
            subject=subject,
            predicate=predicate,
            obj=obj,
            object_type=object_type
        )
        self.triples.append(triple)

    def _infer_data_type(self, value: Any) -> Optional[str]:
        """Infer RDF data type from Python value."""
        if isinstance(value, bool):
            return f"{self.namespaces['xsd']}boolean"
        elif isinstance(value, int):
            return f"{self.namespaces['xsd']}integer"
        elif isinstance(value, float):
            return f"{self.namespaces['xsd']}decimal"
        elif isinstance(value, str):
            # Check if it's a date
            if self._is_date(value):
                return f"{self.namespaces['xsd']}date"
            elif self._is_datetime(value):
                return f"{self.namespaces['xsd']}dateTime"

        return None

    def _is_date(self, value: str) -> bool:
        """Check if string is ISO date."""
        try:
            datetime.fromisoformat(value.split("T")[0])
            return len(value) == 10
        except (ValueError, AttributeError):
            return False

    def _is_datetime(self, value: str) -> bool:
        """Check if string is ISO datetime."""
        try:
            datetime.fromisoformat(value.replace("Z", "+00:00"))
            return "T" in value
        except (ValueError, AttributeError):
            return False

    @staticmethod
    def _slugify(text: str) -> str:
        """Convert text to slug format."""
        return text.lower().replace(" ", "_").replace("-", "_")

    def to_turtle(self) -> str:
        """Generate Turtle format output."""
        output = ""

        # Add namespace declarations
        for prefix, uri in self.namespaces.items():
            output += f"@prefix {prefix}: <{uri}> .\n"

        output += "\n"

        # Group triples by subject for readability
        subjects: Dict[str, List[Triple]] = {}
        for triple in self.triples:
            if triple.subject not in subjects:
                subjects[triple.subject] = []
            subjects[triple.subject].append(triple)

        for subject, triples in subjects.items():
            turtle_triples = [t.to_turtle(self.namespaces) for t in triples]
            output += " ;\n  ".join(turtle_triples) + " .\n\n"

        return output

    def to_ntriples(self) -> str:
        """Generate N-Triples format output."""
        output = ""
        for triple in self.triples:
            output += triple.to_ntriples() + "\n"
        return output

    def to_jsonld(self) -> Dict:
        """Generate JSON-LD format output."""
        context = {
            "@vocab": f"{self.namespaces['schema']}",
            "foaf": self.namespaces["foaf"],
            "ex": self.namespaces["ex"]
        }

        graph = []
        for subject, triples in self._group_by_subject().items():
            node = {
                "@id": subject,
                "@context": context
            }

            for triple in triples:
                if triple.predicate.endswith("/type"):
                    node["@type"] = triple.obj
                else:
                    key = triple.predicate.split("/")[-1]
                    if triple.object_type == "uri":
                        node[key] = {"@id": triple.obj}
                    else:
                        node[key] = triple.obj

            graph.append(node)

        return {"@context": context, "@graph": graph}

    def to_graph_json(self) -> Dict:
        """Generate Graph JSON format output."""
        nodes = []
        edges = []
        seen_subjects: Set[str] = set()

        for triple in self.triples:
            # Add subject node
            if triple.subject not in seen_subjects:
                nodes.append({
                    "id": triple.subject,
                    "type": "Entity",
                    "properties": {}
                })
                seen_subjects.add(triple.subject)

            # Add edge if object is URI
            if triple.object_type == "uri":
                edges.append({
                    "source": triple.subject,
                    "target": triple.obj,
                    "type": triple.predicate
                })

                # Add target node
                if triple.obj not in seen_subjects:
                    nodes.append({
                        "id": triple.obj,
                        "type": "Entity",
                        "properties": {}
                    })
                    seen_subjects.add(triple.obj)

        return {
            "nodes": nodes,
            "edges": edges,
            "metadata": {
                "total_nodes": len(nodes),
                "total_edges": len(edges),
                "generated_at": datetime.now().isoformat()
            }
        }

    def _group_by_subject(self) -> Dict[str, List[Triple]]:
        """Group triples by subject."""
        grouped: Dict[str, List[Triple]] = {}
        for triple in self.triples:
            if triple.subject not in grouped:
                grouped[triple.subject] = []
            grouped[triple.subject].append(triple)
        return grouped

    def get_summary(self) -> Dict:
        """Get converter summary."""
        return {
            "total_triples": len(self.triples),
            "unique_subjects": len(self._group_by_subject()),
            "output_format": self.output_format.value,
            "namespaces": len(self.namespaces),
            "errors": self.errors
        }

    def print_summary(self) -> None:
        """Print converter summary."""
        print(f"\n{'='*60}")
        print(f"JSON TO TRIPLES CONVERTER SUMMARY")
        print(f"{'='*60}")

        summary = self.get_summary()
        print(f"Total Triples Generated: {summary['total_triples']}")
        print(f"Unique Subjects: {summary['unique_subjects']}")
        print(f"Output Format: {summary['output_format']}")
        print(f"Namespaces Defined: {summary['namespaces']}")

        if self.errors:
            print(f"\nErrors: {len(self.errors)}")
            for error in self.errors[:5]:
                print(f"  - {error}")


if __name__ == "__main__":
    # Example 1: Simple Person to Triples
    print("Example 1: Person to Triples Conversion")

    converter = JSONTriplesConverter(
        base_namespace="http://example.org/",
        output_format=OutputFormat.TURTLE
    )

    converter.add_entity_mapping("person", "foaf:Person")
    converter.add_property_mapping("email", "foaf:mbox")
    converter.add_property_mapping("age", "foaf:age")

    json_data = {
        "person": {
            "id": "alice_001",
            "name": "Alice",
            "age": 30,
            "email": "alice@example.com",
            "company": {
                "id": "acme_001",
                "name": "Acme Corp"
            }
        }
    }

    converter.convert(json_data)
    converter.print_summary()

    print("\nGenerated Turtle:")
    print(converter.to_turtle())

    # Example 2: Different output format
    print("\n\nExample 2: JSON-LD Output")

    jsonld_output = converter.to_jsonld()
    print(json.dumps(jsonld_output, indent=2))

    # Example 3: Graph JSON output
    print("\n\nExample 3: Graph JSON Output")

    graph_json = converter.to_graph_json()
    print(json.dumps(graph_json, indent=2))


