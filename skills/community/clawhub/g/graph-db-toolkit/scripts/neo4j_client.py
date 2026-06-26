"""
Neo4j client wrapper for graph database operations.
"""
from typing import List, Dict, Any, Optional

try:
    from neo4j import GraphDatabase
except ImportError:
    GraphDatabase = None

class Neo4jClient:
    def __init__(self, uri: str = "bolt://localhost:7687", user: str = "neo4j", password: str = "password"):
        if GraphDatabase is None:
            raise ImportError("neo4j not installed. Run: pip install neo4j")
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def create_node(self, label: str, properties: Dict[str, Any]) -> str:
        cypher = f"CREATE (n:{label} $props) RETURN id(n) as node_id"
        with self.driver.session() as session:
            result = session.run(cypher, props=properties)
            record = result.single()
            return record["node_id"] if record else None

    def create_relationship(self, from_name: str, from_label: str, rel_type: str,
                          to_name: str, to_label: str, properties: Optional[Dict] = None,
                          match_key: str = "name") -> bool:
        props = properties or {}
        cypher = f"""
            MATCH (a:{from_label} {{{match_key}: $from_name}})
            MATCH (b:{to_label} {{{match_key}: $to_name}})
            CREATE (a)-[r:{rel_type} $props]->(b)
            RETURN r
        """
        with self.driver.session() as session:
            result = session.run(cypher, from_name=from_name, to_name=to_name, props=props)
            return result.single() is not None

    def query(self, cypher: str, parameters: Optional[Dict] = None) -> List[Dict]:
        with self.driver.session() as session:
            result = session.run(cypher, parameters or {})
            return [dict(record) for record in result]

    def delete_all(self):
        with self.driver.session() as session:
            session.run("MATCH (n) DETACH DELETE n")

    def get_node(self, label: str, key: str, value: Any) -> Optional[Dict]:
        cypher = f"MATCH (n:{label} {{{key}: $value}}) RETURN n"
        results = self.query(cypher, {"value": value})
        return results[0] if results else None

    def update_node(self, label: str, key: str, value: Any, new_props: Dict[str, Any]) -> bool:
        cypher = f"MATCH (n:{label} {{{key}: $value}}) SET n += $new_props RETURN n"
        results = self.query(cypher, {"value": value, "new_props": new_props})
        return len(results) > 0
