"""
Query Template Generator: Generate reusable parameterized graph query templates.

Produces Cypher and SPARQL query templates for common graph operations,
parameterized for easy reuse across applications.

Author: Knowledge Graph Project
Version: 1.0.0
"""

from enum import Enum
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
import json


# ============================================================================
# Enums and Data Classes
# ============================================================================

class QueryType(Enum):
    """Supported query language types."""
    CYPHER = "cypher"
    SPARQL = "sparql"


class TemplateGoal(Enum):
    """Template generation goals."""
    FIND_NODE = "find_node"
    FIND_RELATIONSHIPS = "find_relationships"
    FIND_PATHS = "find_paths"
    AGGREGATION = "aggregation"
    FILTERING = "filtering"
    COMPARISON = "comparison"
    MULTI_HOP = "multi_hop"
    PROPERTY_SEARCH = "property_search"


@dataclass
class Parameter:
    """Template parameter definition."""
    name: str
    param_type: str  # "string", "integer", "float", "boolean", etc.
    description: str = ""
    default_value: Optional[Any] = None
    required: bool = True
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            "name": self.name,
            "type": self.param_type,
            "description": self.description,
            "default": self.default_value,
            "required": self.required
        }


@dataclass
class QueryTemplate:
    """Complete query template definition."""
    name: str
    query: str
    language: QueryType
    parameters: List[Parameter] = field(default_factory=list)
    description: str = ""
    usage_example: str = ""
    performance_notes: str = ""
    index_recommendations: List[str] = field(default_factory=list)
    related_templates: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            "name": self.name,
            "query": self.query,
            "language": self.language.value,
            "parameters": [p.to_dict() for p in self.parameters],
            "description": self.description,
            "usage_example": self.usage_example,
            "performance_notes": self.performance_notes,
            "index_recommendations": self.index_recommendations,
            "related_templates": self.related_templates
        }
    
    def to_json(self) -> str:
        """Convert to JSON string."""
        return json.dumps(self.to_dict(), indent=2)


# ============================================================================
# Query Template Generator
# ============================================================================

class QueryTemplateGenerator:
    """Generates reusable query templates."""
    
    def __init__(self):
        """Initialize template generator."""
        self.templates: Dict[str, QueryTemplate] = {}
        self._register_standard_templates()
    
    def _register_standard_templates(self):
        """Register standard templates."""
        # Cypher node lookup
        self.register_template(QueryTemplate(
            name="cypher_find_node",
            query="MATCH (n:$label {$property: $value}) RETURN n LIMIT $limit",
            language=QueryType.CYPHER,
            parameters=[
                Parameter("label", "string", "Node label"),
                Parameter("property", "string", "Property name"),
                Parameter("value", "any", "Property value"),
                Parameter("limit", "integer", "Result limit", default_value=10)
            ],
            description="Find a node by label and property",
            performance_notes="O(1) with index, O(n) without"
        ))
        
        # Cypher relationship
        self.register_template(QueryTemplate(
            name="cypher_find_relationships",
            query="""MATCH (a:$sourceLabel)-[:$relationshipType]->(b:$targetLabel)
RETURN a, b LIMIT $limit""",
            language=QueryType.CYPHER,
            parameters=[
                Parameter("sourceLabel", "string", "Source node label"),
                Parameter("relationshipType", "string", "Relationship type"),
                Parameter("targetLabel", "string", "Target node label"),
                Parameter("limit", "integer", "Result limit", default_value=100)
            ],
            description="Find relationships between two node types"
        ))
        
        # Cypher aggregation
        self.register_template(QueryTemplate(
            name="cypher_aggregation",
            query="""MATCH (source:$sourceLabel)-[:$relationshipType]->(target:$targetLabel)
RETURN target.$groupProperty, COUNT(source) as count
GROUP BY target.$groupProperty
ORDER BY count DESC
LIMIT $limit""",
            language=QueryType.CYPHER,
            parameters=[
                Parameter("sourceLabel", "string", "Source node type"),
                Parameter("relationshipType", "string", "Relationship type"),
                Parameter("targetLabel", "string", "Target node type"),
                Parameter("groupProperty", "string", "Property to group by"),
                Parameter("limit", "integer", "Result limit", default_value=10)
            ],
            description="Aggregate entities by relationship"
        ))
        
        # Cypher path discovery
        self.register_template(QueryTemplate(
            name="cypher_find_paths",
            query="""MATCH path = (start:$startLabel)-[*1..$depth]-(end:$endLabel)
RETURN path, LENGTH(path) as hops LIMIT $limit""",
            language=QueryType.CYPHER,
            parameters=[
                Parameter("startLabel", "string", "Start node label"),
                Parameter("endLabel", "string", "End node label"),
                Parameter("depth", "integer", "Maximum path depth", default_value=3),
                Parameter("limit", "integer", "Result limit", default_value=10)
            ],
            description="Discover paths between node types",
            performance_notes="Exponential in depth - keep depth <= 3"
        ))
        
        # SPARQL node lookup
        self.register_template(QueryTemplate(
            name="sparql_find_node",
            query="""PREFIX ex: <http://example.org/>
SELECT ?entity
WHERE {
  ?entity a ex:$class ;
          ex:$property $value .
}
LIMIT $limit""",
            language=QueryType.SPARQL,
            parameters=[
                Parameter("class", "string", "Entity class"),
                Parameter("property", "string", "Property name"),
                Parameter("value", "string", "Property value"),
                Parameter("limit", "integer", "Result limit", default_value=10)
            ],
            description="SPARQL template for finding entities"
        ))
    
    def register_template(self, template: QueryTemplate):
        """Register a template."""
        self.templates[template.name] = template
    
    def get_template(self, name: str) -> Optional[QueryTemplate]:
        """Get a registered template by name."""
        return self.templates.get(name)
    
    def list_templates(self, language: Optional[QueryType] = None) -> List[str]:
        """List available templates."""
        if language:
            return [name for name, t in self.templates.items() if t.language == language]
        return list(self.templates.keys())
    
    def generate_template(
        self,
        goal: TemplateGoal,
        language: QueryType,
        **kwargs
    ) -> QueryTemplate:
        """Generate a template for a specific goal."""
        
        if goal == TemplateGoal.FIND_NODE:
            return self._generate_find_node_template(language, **kwargs)
        elif goal == TemplateGoal.FIND_RELATIONSHIPS:
            return self._generate_relationship_template(language, **kwargs)
        elif goal == TemplateGoal.FIND_PATHS:
            return self._generate_path_template(language, **kwargs)
        elif goal == TemplateGoal.AGGREGATION:
            return self._generate_aggregation_template(language, **kwargs)
        elif goal == TemplateGoal.FILTERING:
            return self._generate_filtering_template(language, **kwargs)
        else:
            raise ValueError(f"Unknown template goal: {goal}")
    
    def _generate_find_node_template(self, language: QueryType, **kwargs) -> QueryTemplate:
        """Generate find node template."""
        label = kwargs.get("label", "Entity")
        properties = kwargs.get("properties", ["id"])
        
        if language == QueryType.CYPHER:
            prop_str = ", ".join([f"{p}: ${p}" for p in properties[:1]])
            query = f"MATCH (n:{label} {{{prop_str}}}) RETURN n LIMIT $limit"
            
            params = [Parameter(p, "string", f"Property {p}") for p in properties]
            params.append(Parameter("limit", "integer", "Result limit", default_value=10))
            
            return QueryTemplate(
                name=f"find_{label}_node",
                query=query,
                language=language,
                parameters=params,
                description=f"Find {label} node by properties"
            )
        else:
            return self.templates.get("sparql_find_node")
    
    def _generate_relationship_template(self, language: QueryType, **kwargs) -> QueryTemplate:
        """Generate relationship template."""
        source = kwargs.get("source_label", "Entity")
        rel_type = kwargs.get("rel_type", "CONNECTS_TO")
        target = kwargs.get("target_label", "Entity")
        
        if language == QueryType.CYPHER:
            query = f"""MATCH (a:{source})-[:{rel_type}]->(b:{target})
RETURN a, b LIMIT $limit"""
            
            return QueryTemplate(
                name=f"find_{source}_{rel_type}_{target}",
                query=query,
                language=language,
                parameters=[Parameter("limit", "integer", "Result limit", default_value=100)],
                description=f"Find {rel_type} relationships between {source} and {target}"
            )
        else:
            return QueryTemplate(
                name=f"sparql_{source}_{rel_type}",
                query=f"""PREFIX ex: <http://example.org/>
SELECT ?source ?target
WHERE {{
  ?source ex:{rel_type} ?target .
}}
LIMIT $limit""",
                language=language,
                parameters=[Parameter("limit", "integer", "Result limit", default_value=100)]
            )
    
    def _generate_path_template(self, language: QueryType, **kwargs) -> QueryTemplate:
        """Generate path discovery template."""
        start = kwargs.get("start_label", "Entity")
        end = kwargs.get("end_label", "Entity")
        max_depth = kwargs.get("max_depth", 3)
        
        if language == QueryType.CYPHER:
            query = f"""MATCH path = (start:{start})-[*1..{max_depth}]-(end:{end})
RETURN path, LENGTH(path) as hops LIMIT $limit"""
            
            return QueryTemplate(
                name=f"find_paths_{start}_to_{end}",
                query=query,
                language=language,
                parameters=[Parameter("limit", "integer", "Result limit", default_value=10)],
                description=f"Discover paths from {start} to {end} (max depth: {max_depth})",
                performance_notes=f"Exponential complexity - depth limited to {max_depth}"
            )
        else:
            return QueryTemplate(
                name=f"sparql_paths_{start}_{end}",
                query=f"""PREFIX ex: <http://example.org/>
SELECT ?path
WHERE {{
  ?start a ex:{start} ;
         ex:connects* ?end .
  ?end a ex:{end} .
}}
LIMIT $limit""",
                language=language
            )
    
    def _generate_aggregation_template(self, language: QueryType, **kwargs) -> QueryTemplate:
        """Generate aggregation template."""
        source = kwargs.get("source_label", "Item")
        rel = kwargs.get("rel_type", "RELATED_TO")
        target = kwargs.get("target_label", "Category")
        group_by = kwargs.get("group_by", "name")
        
        if language == QueryType.CYPHER:
            query = f"""MATCH (s:{source})-[:{rel}]->(t:{target})
RETURN t.{group_by}, COUNT(s) as count
GROUP BY t.{group_by}
ORDER BY count DESC
LIMIT $limit"""
            
            return QueryTemplate(
                name=f"aggregate_{source}_by_{target}",
                query=query,
                language=language,
                parameters=[Parameter("limit", "integer", "Result limit", default_value=10)],
                description=f"Aggregate {source} counts by {target}.{group_by}"
            )
        else:
            return QueryTemplate(
                name=f"sparql_aggregate_{source}",
                query=f"""PREFIX ex: <http://example.org/>
SELECT ?category (COUNT(?item) AS ?count)
WHERE {{
  ?item a ex:{source} ;
        ex:{rel} ?category .
}}
GROUP BY ?category
ORDER BY DESC(?count)
LIMIT $limit""",
                language=language
            )
    
    def _generate_filtering_template(self, language: QueryType, **kwargs) -> QueryTemplate:
        """Generate filtering template."""
        label = kwargs.get("label", "Entity")
        property_name = kwargs.get("property", "status")
        operator = kwargs.get("operator", "=")
        
        if language == QueryType.CYPHER:
            query = f"""MATCH (n:{label})
WHERE n.{property_name} {operator} $value
RETURN n LIMIT $limit"""
            
            return QueryTemplate(
                name=f"filter_{label}_by_{property_name}",
                query=query,
                language=language,
                parameters=[
                    Parameter("value", "any", f"Filter value for {property_name}"),
                    Parameter("limit", "integer", "Result limit", default_value=100)
                ],
                description=f"Filter {label} nodes by {property_name}"
            )
        else:
            return QueryTemplate(
                name=f"sparql_filter_{label}",
                query=f"""PREFIX ex: <http://example.org/>
SELECT ?entity
WHERE {{
  ?entity a ex:{label} ;
          ex:{property_name} ?value .
  FILTER (?value {operator} $filterValue)
}}
LIMIT $limit""",
                language=language
            )
    
    def customize_template(
        self,
        base_template: str,
        **customizations
    ) -> QueryTemplate:
        """Customize an existing template."""
        template = self.get_template(base_template)
        if not template:
            raise ValueError(f"Template {base_template} not found")
        
        # Create a new template with customizations
        new_template = QueryTemplate(
            name=f"{base_template}_custom",
            query=template.query,
            language=template.language,
            parameters=template.parameters.copy(),
            description=template.description
        )
        
        # Apply customizations
        for key, value in customizations.items():
            if hasattr(new_template, key):
                setattr(new_template, key, value)
        
        return new_template
    
    def validate_template(self, template: QueryTemplate) -> List[str]:
        """Validate a template and return any issues."""
        issues = []
        
        # Check query is not empty
        if not template.query or not template.query.strip():
            issues.append("Query template is empty")
        
        # Check all parameters are documented
        if not template.parameters and "$" in template.query:
            issues.append("Query has parameters but none are documented")
        
        # Check parameters match query
        query_params = self._extract_parameters(template.query)
        documented_params = {p.name for p in template.parameters}
        
        if query_params - documented_params:
            issues.append(f"Undocumented parameters: {query_params - documented_params}")
        
        return issues
    
    def _extract_parameters(self, query: str) -> set:
        """Extract parameter names from query."""
        import re
        return set(re.findall(r'\$(\w+)', query))
    
    def print_template(self, template: QueryTemplate):
        """Pretty print a template."""
        print("\n" + "="*70)
        print(f"Template: {template.name}")
        print("="*70)
        print(f"\nDescription: {template.description}")
        print(f"Language: {template.language.value.upper()}")
        print(f"\nQuery:")
        print(f"  {template.query}")
        
        if template.parameters:
            print(f"\nParameters:")
            for param in template.parameters:
                required = " (required)" if param.required else " (optional)"
                print(f"  - ${param.name} ({param.param_type}){required}")
                print(f"    {param.description}")
        
        if template.index_recommendations:
            print(f"\nIndex Recommendations:")
            for index in template.index_recommendations:
                print(f"  - {index}")
        
        if template.performance_notes:
            print(f"\nPerformance Notes:")
            print(f"  {template.performance_notes}")
        
        if template.usage_example:
            print(f"\nUsage Example:")
            print(f"  {template.usage_example}")
        
        print("="*70 + "\n")


# ============================================================================
# Usage Example
# ============================================================================

if __name__ == "__main__":
    print("🚀 Query Template Generator - Example Usage\n")
    
    generator = QueryTemplateGenerator()
    
    # List available templates
    print("Available Cypher Templates:")
    for name in generator.list_templates(QueryType.CYPHER):
        template = generator.get_template(name)
        print(f"  - {name}: {template.description}")
    
    # Get and print a template
    print("\n")
    template = generator.get_template("cypher_find_node")
    generator.print_template(template)
    
    # Generate a custom template
    print("Generating custom template...")
    custom = generator.generate_template(
        TemplateGoal.FIND_RELATIONSHIPS,
        QueryType.CYPHER,
        source_label="Person",
        rel_type="WORKS_AT",
        target_label="Company"
    )
    generator.print_template(custom)
    
    print("✅ Query Template Generator Ready!")
