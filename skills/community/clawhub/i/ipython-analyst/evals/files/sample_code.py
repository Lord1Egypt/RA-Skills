"""
Sample Python file with various functions of different complexity.

Used for the code analysis test case.
The user says: "Analyze this file and tell me which functions are too complex."
"""

import re
from typing import List, Dict, Optional


def simple_function(x: int) -> int:
    """A simple function — complexity 1."""
    return x * 2


def moderate_function(items: List[int]) -> int:
    """A moderate function with a loop and a conditional — complexity 3."""
    total = 0
    for item in items:
        if item > 0:
            total += item
    return total


def complex_function(records: List[Dict]) -> Dict[str, int]:
    """A complex function with nested branches — complexity 7.

    This should trigger a 'high_complexity' warning in the analyzer.
    """
    result = {"high": 0, "medium": 0, "low": 0}
    for record in records:
        if record.get("status") == "active":
            if record.get("amount", 0) > 1000:
                if record.get("priority") == "high":
                    result["high"] += 1
                elif record.get("priority") == "medium":
                    result["medium"] += 1
                else:
                    result["low"] += 1
            elif record.get("amount", 0) > 100:
                result["medium"] += 1
            else:
                result["low"] += 1
    return result


def deep_nesting_function(data: Dict) -> Optional[str]:
    """A function with deep nesting — nesting depth 5.

    Should trigger a 'deep_nesting' warning.
    """
    if "users" in data:
        if data["users"]:
            if "admin" in data["users"][0]:
                if data["users"][0]["admin"]:
                    if "name" in data["users"][0]:
                        return data["users"][0]["name"]
    return None


def many_params(a, b, c, d, e, f, g, h) -> int:
    """A function with too many parameters — 8 params.

    Should trigger a 'too_many_params' info.
    """
    return a + b + c + d + e + f + g + h


def parse_with_regex(text: str) -> List[str]:
    """Function that uses re.compile — picked up by CodeAnalyzer.regex_patterns."""
    pattern = re.compile(r'\b[A-Z][a-z]+\b')
    return pattern.findall(text)


def try_except_function(s: str) -> int:
    """Function with try/except — complexity 3 (try + 2 except handlers)."""
    try:
        return int(s)
    except ValueError:
        return 0
    except TypeError:
        return -1


class DataProcessor:
    """Sample class for the analyzer to find."""

    def __init__(self, data):
        self.data = data

    def process(self):
        return [self.transform(item) for item in self.data]

    def transform(self, item):
        return item.upper() if isinstance(item, str) else item


def main():
    """Entry point — never called internally."""
    sample = [{"status": "active", "amount": 1500, "priority": "high"}]
    print(complex_function(sample))
    print(parse_with_regex("Hello World Foo Bar"))


if __name__ == "__main__":
    main()
