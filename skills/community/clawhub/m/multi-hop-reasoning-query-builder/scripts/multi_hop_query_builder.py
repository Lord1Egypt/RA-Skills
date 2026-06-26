"""Multi-Hop Query Builder: Generate efficient multi-hop graph queries."""
from enum import Enum
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
class QueryType(Enum):
    """Query language types."""
    CYPHER = "cypher"
    SPARQL = "sparql"
class HopPattern(Enum):
    """Multi-hop pattern types."""
    FIXED_DEPTH = "fixed_depth"
    VARIABLE_DEPTH = "variable_depth"
    PATH_DISCOVERY = "path_discovery"
    SHORTEST_PATH = "shortest_path"
    FILTERED = "filtered"
    AGGREGATED = "aggregated"
    UNDIRECTED = "undirected"
@dataclass
class HopParameter:
    """Multi-hop query parameter."""
    name: str
    param_type: str
    description: str
    required: bool = True
@dataclass
class MultiHopQuery:
    """Complete multi-hop query definition."""
    query: str
    language: QueryType
    pattern: HopPattern
    num_hops: int
    min_hops: Optional[int] = None
    max_hops: Optional[int] = None
    parameters: List[HopParameter] = field(default_factory=list)
    description: str = ""
    complexity: str = ""
    performance_notes: str = ""
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "query": self.query,
            "language": self.language.value,
            "pattern": self.pattern.value,
            "hops": f"{self.min_hops}..{self.max_hops}" if self.min_hops else str(self.num_hops),
            "parameters": [{"name": p.name, "type": p.param_type} for p in self.parameters],
            "description": self.description,
            "complexity": self.complexity
        }
class MultiHopQueryBuilder:
    """Generates multi-hop traversal queries."""
    def __init__(self):
        """Initialize builder."""
        self.max_safe_depth = 4
        self.default_limit = 100
    def build_query(
        self,
        start_label: str,
        start_id_property: str,
        start_id_value: str,
        relationship_type: str,
        num_hops: int,
        target_label: Optional[str] = None,
        language: QueryType = QueryType.CYPHER,
        limit: int = 100
    ) -> MultiHopQuery:
        """Build fixed-depth multi-hop query."""
        if num_hops > self.max_safe_depth:
            return self._build_with_warning(
                f"Hop depth {num_hops} exceeds safe limit {self.max_safe_depth}",
                start_label, relationship_type, num_hops, language
            )
        if language == QueryType.CYPHER:
            return self._build_cypher_fixed_hop(
                start_label, start_id_property, start_id_value,
                relationship_type, num_hops, target_label, limit
            )
        else:
            return self._build_sparql_fixed_hop(
                start_label, start_id_property, start_id_value,
                relationship_type, num_hops, limit
            )
    def build_variable_hop_query(
        self,
        start_label: str,
        relationship_type: str,
        min_hops: int,
        max_hops: int,
        target_label: Optional[str] = None,
        language: QueryType = QueryType.CYPHER,
        limit: int = 100
    ) -> MultiHopQuery:
        """Build variable-depth multi-hop query."""
        if max_hops > self.max_safe_depth:
            max_hops = self.max_safe_depth
        if language == QueryType.CYPHER:
            return self._build_cypher_variable_hop(
                start_label, relationship_type, min_hops, max_hops,
                target_label, limit
            )
        else:
            return self._build_sparql_variable_hop(
                start_label, relationship_type, min_hops, max_hops, limit
            )
    def build_path_query(
        self,
        start_label: str,
        target_label: str,
        relationship_type: Optional[str] = None,
        max_depth: int = 3,
        language: QueryType = QueryType.CYPHER,
        limit: int = 10
    ) -> MultiHopQuery:
        """Build path discovery query."""
        if language == QueryType.CYPHER:
            if relationship_type:
                query = f"""MATCH path = (start:{start_label})-[:{relationship_type}*1..{max_depth}]-(end:{target_label})
RETURN path, LENGTH(path) as hops
ORDER BY hops
LIMIT {limit}"""
            else:
                query = f"""MATCH path = (start:{start_label})-[*1..{max_depth}]-(end:{target_label})
RETURN path, LENGTH(path) as hops
ORDER BY hops
LIMIT {limit}"""
            return MultiHopQuery(
                query=query,
                language=QueryType.CYPHER,
                pattern=HopPattern.PATH_DISCOVERY,
                num_hops=max_depth,
                max_hops=max_depth,
                description=f"Find paths from {start_label} to {target_label}",
                complexity=f"O(n^{max_depth})"
            )
        else:
            query = f"""PREFIX ex: <http://example.org/>
SELECT ?start ?end ?path
WHERE {{
  ?start a ex:{start_label} ;
         ex:connects+ ?end .
  ?end a ex:{target_label} .
}}
LIMIT {limit}"""
            return MultiHopQuery(
                query=query,
                language=QueryType.SPARQL,
                pattern=HopPattern.PATH_DISCOVERY,
                num_hops=max_depth,
                description=f"Find paths from {start_label} to {target_label}"
            )
    def _build_cypher_fixed_hop(
        self,
        start_label: str,
        start_id_property: str,
        start_id_value: str,
        relationship_type: str,
        num_hops: int,
        target_label: Optional[str],
        limit: int
    ) -> MultiHopQuery:
        """Build Cypher fixed-depth query."""
        target_part = f":{target_label}" if target_label else ""
        query = f"""MATCH (start:{start_label} {{{start_id_property}: ${start_id_property}}})-[:{relationship_type}*{num_hops}]->(target{target_part})
RETURN DISTINCT target
LIMIT {limit}"""
        return MultiHopQuery(
            query=query,
            language=QueryType.CYPHER,
            pattern=HopPattern.FIXED_DEPTH,
            num_hops=num_hops,
            parameters=[
                HopParameter(start_id_property, "string", f"Starting {start_label} {start_id_property}")
            ],
            description=f"Find targets exactly {num_hops} hops from starting {start_label}",
            complexity=f"O(n^{num_hops})",
            performance_notes=f"Fixed depth {num_hops} - use LIMIT {limit}"
        )
    def _build_sparql_fixed_hop(
        self,
        start_label: str,
        start_id_property: str,
        start_id_value: str,
        relationship_type: str,
        num_hops: int,
        limit: int
    ) -> MultiHopQuery:
        """Build SPARQL fixed-depth query."""
        path = f"ex:{relationship_type}" * num_hops
        query = f"""PREFIX ex: <http://example.org/>
SELECT ?target
WHERE {{
  ex:{start_id_value} {path} ?target .
}}
LIMIT {limit}"""
        return MultiHopQuery(
            query=query,
            language=QueryType.SPARQL,
            pattern=HopPattern.FIXED_DEPTH,
            num_hops=num_hops,
            description=f"Find targets exactly {num_hops} hops via {relationship_type}"
        )
    def _build_cypher_variable_hop(
        self,
        start_label: str,
        relationship_type: str,
        min_hops: int,
        max_hops: int,
        target_label: Optional[str],
        limit: int
    ) -> MultiHopQuery:
        """Build Cypher variable-depth query."""
        target_part = f":{target_label}" if target_label else ""
        query = f"""MATCH (start:{start_label})-[:{relationship_type}*{min_hops}..{max_hops}]->(target{target_part})
RETURN DISTINCT target
LIMIT {limit}"""
        return MultiHopQuery(
            query=query,
            language=QueryType.CYPHER,
            pattern=HopPattern.VARIABLE_DEPTH,
            num_hops=max_hops,
            min_hops=min_hops,
            max_hops=max_hops,
            description=f"Find targets {min_hops}-{max_hops} hops away",
            complexity=f"O(n^{max_hops})",
            performance_notes=f"Variable depth {min_hops}..{max_hops}"
        )
    def _build_sparql_variable_hop(
        self,
        start_label: str,
        relationship_type: str,
        min_hops: int,
        max_hops: int,
        limit: int
    ) -> MultiHopQuery:
        """Build SPARQL variable-depth query using + operator."""
        query = f"""PREFIX ex: <http://example.org/>
SELECT ?target
WHERE {{
  ?start a ex:{start_label} ;
         ex:{relationship_type}+ ?target .
}}
LIMIT {limit}"""
        return MultiHopQuery(
            query=query,
            language=QueryType.SPARQL,
            pattern=HopPattern.VARIABLE_DEPTH,
            num_hops=max_hops,
            min_hops=min_hops,
            max_hops=max_hops,
            description=f"Find targets via {min_hops}+ {relationship_type} hops"
        )
    def _build_with_warning(
        self,
        warning: str,
        start_label: str,
        relationship_type: str,
        num_hops: int,
        language: QueryType
    ) -> MultiHopQuery:
        """Build query with performance warning."""
        safe_hops = min(num_hops, self.max_safe_depth)
        query = f"-- WARNING: {warning}\n"
        query += f"-- Consider limiting depth to {safe_hops} or adding filters\n"
        if language == QueryType.CYPHER:
            query += f"MATCH (start:{start_label})-[:{relationship_type}*1..{safe_hops}]->(target)\n"
            query += f"RETURN target\nLIMIT 100"
        return MultiHopQuery(
            query=query,
            language=language,
            pattern=HopPattern.VARIABLE_DEPTH,
            num_hops=safe_hops,
            performance_notes=warning
        )
    def print_query(self, mh_query: MultiHopQuery):
        """Pretty print multi-hop query."""
        print("\n" + "="*70)
        print(f"Multi-Hop Query: {mh_query.pattern.value.upper()}")
        print("="*70)
        print(f"\nLanguage: {mh_query.language.value.upper()}")
        print(f"Pattern: {mh_query.pattern.value}")
        print(f"Hops: {mh_query.min_hops}..{mh_query.max_hops}" if mh_query.min_hops else f"Hops: {mh_query.num_hops}")
        print(f"Complexity: {mh_query.complexity}")
        if mh_query.description:
            print(f"Description: {mh_query.description}")
        print(f"\nQuery:")
        print(mh_query.query)
        if mh_query.parameters:
            print(f"\nParameters:")
            for param in mh_query.parameters:
                print(f"  - ${param.name} ({param.param_type}): {param.description}")
        if mh_query.performance_notes:
            print(f"\n⚠️  Performance Notes: {mh_query.performance_notes}")
        print("="*70 + "\n")
if __name__ == "__main__":
    print("🚀 Multi-Hop Query Builder Ready!")
    builder = MultiHopQueryBuilder()
    query = builder.build_query(
        start_label="Person",
        start_id_property="username",
        start_id_value="alice",
        relationship_type="FOLLOWS",
        num_hops=2,
        language=QueryType.CYPHER
    )
    builder.print_query(query)
