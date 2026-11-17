"""Wikidata SPARQL endpoint + entity lookup."""
import os
from . import _http

SPARQL = "https://query.wikidata.org/sparql"
ENTITY = "https://www.wikidata.org/wiki/Special:EntityData"


def _headers(auth):
    return {
        "User-Agent": auth.get("user_agent", "ocas-reach (contact: os.environ.get("OCAS_AGENT_EMAIL", "agent@example.com"))"),
        "Accept": "application/sparql-results+json",
    }


def query(action, params, auth):
    if action == "sparql":
        q = params.get("query")
        if not q:
            raise ValueError("sparql requires {'query': '<SPARQL string>'}")
        body = f"query={_http.qs({'q': q}).split('=', 1)[1]}"
        # Use POST form-urlencoded to avoid URL length limits.
        return _http.post(
            SPARQL,
            body=f"query={__import__('urllib.parse', fromlist=['quote']).quote(q)}",
            headers={**_headers(auth), "Content-Type": "application/x-www-form-urlencoded"},
        )

    if action == "entity":
        qid = params.get("qid")
        if not qid or not qid.upper().startswith("Q"):
            raise ValueError("entity requires {'qid': 'Q42'}")
        return _http.get(f"{ENTITY}/{qid.upper()}.json", headers=_headers(auth))

    raise ValueError(f"Unknown action: {action}")
