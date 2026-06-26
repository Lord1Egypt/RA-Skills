from __future__ import annotations
import re

FORBIDDEN_KEYWORDS = [
    "INSERT", "UPDATE", "DELETE", "DROP", "ALTER", "CREATE", "TRUNCATE",
    "REPLACE", "GRANT", "REVOKE", "EXEC", "EXECUTE", "CALL", "MERGE",
    "UPSERT", "LOAD", "COPY", "ATTACH", "DETACH", "PRAGMA", "SET", "VACUUM",
]

def check_sql_safety(sql: str) -> tuple[bool, str | None]:
    """Check if SQL is safe (read-only). Returns (safe, reason)."""
    trimmed = sql.strip()
    if not trimmed:
        return False, "Empty SQL statement"

    # Remove comments
    cleaned = re.sub(r'--.*$', '', trimmed, flags=re.MULTILINE)
    cleaned = re.sub(r'/\*[\s\S]*?\*/', '', cleaned).strip()
    if not cleaned:
        return False, "Empty SQL after removing comments"

    # Check starts with SELECT or WITH
    first_word = cleaned.upper().split()[0]
    if first_word not in ("SELECT", "WITH"):
        return False, f"Only SELECT statements are allowed. Got: {first_word}"

    # Remove string literals for keyword checking
    without_strings = re.sub(r"'[^']*'", "''", cleaned)
    without_strings = re.sub(r'"[^"]*"', '""', without_strings)
    upper_no_strings = without_strings.upper()

    # Check forbidden keywords
    for keyword in FORBIDDEN_KEYWORDS:
        pattern = rf'(^|;|\s){keyword}(\s|\(|$)'
        if re.search(pattern, upper_no_strings, re.IGNORECASE):
            return False, f"Forbidden keyword detected: {keyword}"

    # Check multiple statements
    statements = [s for s in without_strings.split(';') if s.strip()]
    if len(statements) > 1:
        return False, "Multiple statements are not allowed"

    return True, None
