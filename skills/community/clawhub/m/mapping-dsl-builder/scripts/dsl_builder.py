#!/usr/bin/env python3
"""
Mapping DSL Builder implementation for mapping-dsl-builder skill.
Provides core functionality for generating mapping DSL specifications.
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum
import json
from datetime import datetime

try:
    import yaml
except ImportError:
    yaml = None


class SourceType(Enum):
    """Data source types."""
    DATABASE = "database"
    CSV = "csv"
    JSON = "json"
    API = "api"
    STREAM = "stream"


class OutputFormat(Enum):
    """Output formats for mapping specifications."""
    CUSTOM_DSL = "custom_dsl"
    R2RML = "r2rml"
    YAML = "yaml"
    JSON = "json"


@dataclass
class PropertyMapping:
    """Property mapping definition."""
    source_column: str
    target_predicate: str
    datatype: str = "xsd:string"
    transformation: Optional[str] = None
    required: bool = False


@dataclass
class RelationshipMapping:
    """Relationship mapping definition."""
    name: str
    source_column: str
    target_entity: str
    target_identifier: str
    predicate: str
    cardinality: str = "*..1"


@dataclass
class EntityMapping:
    """Entity mapping definition."""
    entity_type: str
    identifier_column: str
    uri_template: str
    properties: List[PropertyMapping] = field(default_factory=list)
    relationships: List[RelationshipMapping] = field(default_factory=list)


@dataclass
class SourceDefinition:
    """Source specification."""
    source_type: SourceType
    location: str
    table_name: Optional[str] = None
    delimiter: Optional[str] = None
    connection_string: Optional[str] = None


class MappingDSLBuilder:
    """Main Mapping DSL Builder class."""

    def __init__(self, name: str, version: str = "1.0"):
        """Initialize mapping builder."""
        self.name = name
        self.version = version
        self.description = ""
        self.source: Optional[SourceDefinition] = None
        self.entities: Dict[str, EntityMapping] = {}
        self.transformations: Dict[str, str] = {}
        self.errors: List[str] = []

    def set_source(self, source_type: str, location: str,
                  table_name: Optional[str] = None,
                  **kwargs) -> None:
        """Define data source."""
        try:
            stype = SourceType(source_type)
            self.source = SourceDefinition(
                source_type=stype,
                location=location,
                table_name=table_name,
                delimiter=kwargs.get("delimiter"),
                connection_string=kwargs.get("connection_string")
            )
        except ValueError:
            self.errors.append(f"Unknown source type: {source_type}")

    def add_entity_mapping(self, entity_type: str,
                          identifier_column: str,
                          uri_template: Optional[str] = None) -> str:
        """Add entity mapping."""
        if uri_template is None:
            entity_name = entity_type.split("/")[-1]
            uri_template = f"http://example.org/{entity_name.lower()}/{{{{id}}}}"

        entity_id = entity_type.lower().replace(" ", "_")

        self.entities[entity_id] = EntityMapping(
            entity_type=entity_type,
            identifier_column=identifier_column,
            uri_template=uri_template
        )

        return entity_id

    def add_property_mapping(self, source_column: str,
                            target_predicate: str,
                            entity_id: Optional[str] = None,
                            datatype: str = "xsd:string") -> None:
        """Add property mapping to entity."""
        if not self.entities:
            self.errors.append("No entities defined. Add entity first.")
            return

        # Use last entity if not specified
        if entity_id is None:
            entity_id = list(self.entities.keys())[-1]

        if entity_id not in self.entities:
            self.errors.append(f"Entity {entity_id} not found")
            return

        prop = PropertyMapping(
            source_column=source_column,
            target_predicate=target_predicate,
            datatype=datatype
        )

        self.entities[entity_id].properties.append(prop)

    def add_relationship_mapping(self, relationship_name: str,
                                source_column: str,
                                target_entity: str,
                                target_identifier: str,
                                entity_id: Optional[str] = None,
                                predicate: Optional[str] = None) -> None:
        """Add relationship mapping to entity."""
        if not self.entities:
            self.errors.append("No entities defined. Add entity first.")
            return

        # Use last entity if not specified
        if entity_id is None:
            entity_id = list(self.entities.keys())[-1]

        if entity_id not in self.entities:
            self.errors.append(f"Entity {entity_id} not found")
            return

        if predicate is None:
            predicate = f"http://example.org/{relationship_name.lower()}"

        rel = RelationshipMapping(
            name=relationship_name,
            source_column=source_column,
            target_entity=target_entity,
            target_identifier=target_identifier,
            predicate=predicate
        )

        self.entities[entity_id].relationships.append(rel)

    def add_transformation(self, name: str, function: str) -> None:
        """Add transformation function."""
        self.transformations[name] = function

    def to_dsl(self) -> str:
        """Generate custom DSL format."""
        output = f"""mapping: {self.name}
version: {self.version}
description: {self.description or 'Auto-generated mapping'}

source:
  type: {self.source.source_type.value if self.source else 'unknown'}
  location: {self.source.location if self.source else 'not defined'}
"""

        if self.source.table_name:
            output += f"  table: {self.source.table_name}\n"

        output += "\nentities:\n"

        for entity_id, entity in self.entities.items():
            output += f"""  - entity_id: {entity_id}
    type: {entity.entity_type}
    identifier: {entity.identifier_column}
    uri_template: "{entity.uri_template}"
    
    properties:
"""
            for prop in entity.properties:
                output += f"""      - source: {prop.source_column}
        predicate: {prop.target_predicate}
        type: {prop.datatype}
"""

            if entity.relationships:
                output += "    relationships:\n"
                for rel in entity.relationships:
                    output += f"""      - name: {rel.name}
        source: {rel.source_column}
        target: {rel.target_entity}
        predicate: {rel.predicate}
        cardinality: {rel.cardinality}
"""

        return output

    def to_r2rml(self) -> str:
        """Generate R2RML Turtle format."""
        output = """@prefix rr: <http://www.w3.org/ns/r2rml#> .
@prefix foaf: <http://xmlns.com/foaf/0.1/> .
@prefix schema: <http://schema.org/> .
@prefix ex: <http://example.org/> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

"""

        for entity_id, entity in self.entities.items():
            entity_name = entity_id.replace("_", " ").title().replace(" ", "")
            output += f"ex:{entity_name}Mapping a rr:TriplesMap ;\n"

            if self.source and self.source.table_name:
                output += f'  rr:logicalTable [ rr:tableName "{self.source.table_name}" ] ;\n'

            output += f"""  rr:subjectMap [
    rr:template "{entity.uri_template}" ;
    rr:class {entity.entity_type}
  ] ;
"""

            # Add property mappings
            for prop in entity.properties:
                output += f"""  rr:predicateObjectMap [
    rr:predicate {prop.target_predicate} ;
    rr:objectMap [ rr:column "{prop.source_column}" ]
  ] ;
"""

            # Add relationship mappings
            for rel in entity.relationships:
                output += f"""  rr:predicateObjectMap [
    rr:predicate {rel.predicate} ;
    rr:objectMap [
      rr:parentTriplesMap ex:{rel.target_entity}Mapping ;
      rr:joinCondition [ rr:child "{rel.source_column}" ; rr:parent "{rel.target_identifier}" ]
    ]
  ] ;
"""

            output = output.rstrip(";") + " .\n\n"

        return output

    def to_yaml(self) -> str:
        """Generate YAML format."""
        if yaml is None:
            return self._to_yaml_string()

        config = {
            "mapping": self.name,
            "version": self.version,
            "description": self.description or "Auto-generated mapping",
            "source": {
                "type": self.source.source_type.value if self.source else None,
                "location": self.source.location if self.source else None
            },
            "entities": []
        }

        for entity_id, entity in self.entities.items():
            entity_config = {
                "entity_id": entity_id,
                "type": entity.entity_type,
                "identifier": entity.identifier_column,
                "uri_template": entity.uri_template,
                "properties": [
                    {
                        "source": prop.source_column,
                        "predicate": prop.target_predicate,
                        "datatype": prop.datatype
                    }
                    for prop in entity.properties
                ],
                "relationships": [
                    {
                        "name": rel.name,
                        "source": rel.source_column,
                        "target": rel.target_entity,
                        "target_identifier": rel.target_identifier,
                        "predicate": rel.predicate,
                        "cardinality": rel.cardinality
                    }
                    for rel in entity.relationships
                ]
            }
            config["entities"].append(entity_config)

        return yaml.dump(config, default_flow_style=False)

    def _to_yaml_string(self) -> str:
        """Generate YAML as string (fallback)."""
        output = f"""mapping: {self.name}
version: {self.version}
description: {self.description or 'Auto-generated mapping'}

source:
  type: {self.source.source_type.value if self.source else 'unknown'}
  location: {self.source.location if self.source else 'not defined'}

entities:
"""

        for entity_id, entity in self.entities.items():
            output += f"""  - entity_id: {entity_id}
    type: {entity.entity_type}
    identifier: {entity.identifier_column}
    uri_template: "{entity.uri_template}"
    properties:
"""
            for prop in entity.properties:
                output += f"""      - source: {prop.source_column}
        predicate: {prop.target_predicate}
        datatype: {prop.datatype}
"""

            if entity.relationships:
                output += "    relationships:\n"
                for rel in entity.relationships:
                    output += f"""      - name: {rel.name}
        source: {rel.source_column}
        target: {rel.target_entity}
        target_identifier: {rel.target_identifier}
        predicate: {rel.predicate}
        cardinality: {rel.cardinality}
"""

        return output

    def to_json(self) -> str:
        """Generate JSON format."""
        config = {
            "mapping": self.name,
            "version": self.version,
            "description": self.description,
            "source": {
                "type": self.source.source_type.value if self.source else None,
                "location": self.source.location if self.source else None
            },
            "entities": {}
        }

        for entity_id, entity in self.entities.items():
            config["entities"][entity_id] = {
                "type": entity.entity_type,
                "identifier": entity.identifier_column,
                "uri_template": entity.uri_template,
                "properties": [
                    {
                        "source": prop.source_column,
                        "predicate": prop.target_predicate,
                        "datatype": prop.datatype
                    }
                    for prop in entity.properties
                ],
                "relationships": [
                    {
                        "name": rel.name,
                        "source": rel.source_column,
                        "target": rel.target_entity,
                        "target_identifier": rel.target_identifier,
                        "predicate": rel.predicate
                    }
                    for rel in entity.relationships
                ]
            }

        return json.dumps(config, indent=2)

    def get_summary(self) -> Dict:
        """Get builder summary."""
        return {
            "name": self.name,
            "version": self.version,
            "source_type": self.source.source_type.value if self.source else None,
            "entities_count": len(self.entities),
            "total_properties": sum(len(e.properties) for e in self.entities.values()),
            "total_relationships": sum(len(e.relationships) for e in self.entities.values()),
            "transformations": len(self.transformations),
            "errors": self.errors
        }

    def print_summary(self) -> None:
        """Print builder summary."""
        print(f"\n{'='*60}")
        print(f"MAPPING DSL BUILDER: {self.name}")
        print(f"{'='*60}")

        summary = self.get_summary()
        print(f"Version: {summary['version']}")
        print(f"Source Type: {summary['source_type']}")
        print(f"Entities: {summary['entities_count']}")
        print(f"Properties: {summary['total_properties']}")
        print(f"Relationships: {summary['total_relationships']}")

        if self.entities:
            print(f"\nEntity Details:")
            for entity_id, entity in self.entities.items():
                print(f"  {entity_id}:")
                print(f"    Type: {entity.entity_type}")
                print(f"    Properties: {len(entity.properties)}")
                print(f"    Relationships: {len(entity.relationships)}")


if __name__ == "__main__":
    # Example: Employee-Company Mapping
    print("Example 1: Employee-Company Database Mapping")

    builder = MappingDSLBuilder(
        name="EmployeeCompanyMapping",
        version="1.0"
    )

    builder.description = "Map employee and company tables to RDF"

    # Set source
    builder.set_source(
        source_type="database",
        location="postgresql://localhost/company_db",
        table_name="employee"
    )

    # Add employee entity
    emp_id = builder.add_entity_mapping(
        entity_type="http://xmlns.com/foaf/0.1/Person",
        identifier_column="employee_id",
        uri_template="http://example.org/employee/{employee_id}"
    )

    builder.add_property_mapping("employee_name", "http://xmlns.com/foaf/0.1/name", emp_id)
    builder.add_property_mapping("email", "http://xmlns.com/foaf/0.1/mbox", emp_id)
    builder.add_property_mapping("salary", "http://example.org/salary", emp_id, "xsd:decimal")

    builder.add_relationship_mapping(
        "WORKS_AT",
        "company_id",
        "Company",
        "company_id",
        emp_id,
        "http://schema.org/worksFor"
    )

    # Add company entity
    company_id = builder.add_entity_mapping(
        entity_type="http://schema.org/Organization",
        identifier_column="company_id",
        uri_template="http://example.org/company/{company_id}"
    )

    builder.add_property_mapping("company_name", "http://schema.org/name", company_id)
    builder.add_property_mapping("industry", "http://schema.org/industry", company_id)

    builder.print_summary()

    print("\n\nGenerated Custom DSL:")
    print(builder.to_dsl())

    print("\n\nGenerated YAML:")
    print(builder.to_yaml())

    print("\n\nGenerated JSON:")
    print(builder.to_json())




