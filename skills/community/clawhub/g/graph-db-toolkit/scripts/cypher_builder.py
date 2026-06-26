"""
Cypher query builder utilities.
"""
from typing import List, Dict, Any, Optional

class CypherBuilder:
    def __init__(self):
        self._match = []
        self._where = []
        self._return = []
        self._order = []
        self._limit = None
        self._parameters = {}

    def match_node(self, var: str, label: Optional[str] = None, props: Optional[Dict] = None):
        label_str = f":{label}" if label else ""
        if props:
            self._parameters.update({f"{var}_{k}": v for k, v in props.items()})
            prop_str = "{" + ", ".join([f"{k}: ${var}_{k}" for k in props]) + "}"
            self._match.append(f"({var}{label_str} {prop_str})")
        else:
            self._match.append(f"({var}{label_str})")
        return self

    def match_path(self, start: str, rel: str, end: str, rel_props: Optional[Dict] = None):
        if rel_props:
            rp = "{" + ", ".join([f"{k}: ${rel}_{k}" for k in rel_props]) + "}"
            self._parameters.update({f"{rel}_{k}": v for k, v in rel_props.items()})
            self._match.append(f"({start})-[:{rel} {rp}]->({end})")
        else:
            self._match.append(f"({start})-[:{rel}]->({end})")
        return self

    def where(self, condition: str):
        self._where.append(condition)
        return self

    def returns(self, *fields: str):
        self._return.extend(fields)
        return self

    def order_by(self, field: str, desc: bool = False):
        self._order.append(f"{field} DESC" if desc else field)
        return self

    def limit(self, n: int):
        self._limit = n
        return self

    def build(self) -> str:
        parts = []
        if self._match:
            parts.append("MATCH " + ", ".join(self._match))
        if self._where:
            parts.append("WHERE " + " AND ".join(self._where))
        if self._return:
            parts.append("RETURN " + ", ".join(self._return))
        if self._order:
            parts.append("ORDER BY " + ", ".join(self._order))
        if self._limit:
            parts.append(f"LIMIT {self._limit}")
        return " ".join(parts)

    @property
    def parameters(self) -> Dict[str, Any]:
        return self._parameters

    @staticmethod
    def shortest_path(start_label: str, start_key: str, start_val: Any,
                      end_label: str, end_key: str, end_val: Any, max_hops: int = 4) -> str:
        return f"""
            MATCH path = shortestPath(
                (a:{start_label} {{{start_key}: $start_val}})-[*..{max_hops}]-(b:{end_label} {{{end_key}: $end_val}})
            )
            RETURN path
        """
