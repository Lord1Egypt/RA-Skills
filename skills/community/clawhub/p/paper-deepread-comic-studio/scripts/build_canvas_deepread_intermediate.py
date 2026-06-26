from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("focus_spec", type=Path)
    parser.add_argument("output_json", type=Path)
    args = parser.parse_args()

    data = json.loads(args.focus_spec.read_text(encoding="utf-8"))
    payload = {
        "paper_id": data.get("paper_id", ""),
        "title": data.get("title", ""),
        "higher_ml_ai_problems": data.get("higher_ml_ai_problems", []),
        "algorithm_ancestry_upper_problems": data.get("algorithm_ancestry_upper_problems", []),
        "algorithm_encountered_problem_upper_problems": data.get("algorithm_encountered_problem_upper_problems", []),
        "field_problems": data.get("field_problems", []),
        "direction_native_problems": data.get("direction_native_problems", []),
        "module_to_problem_map": data.get("module_to_problem_map", []),
        "graph_node_candidates": data.get("graph_node_candidates", []),
        "graph_relation_candidates": data.get("graph_relation_candidates", []),
        "innovation_hooks": data.get("innovation_hooks", []),
        "research_generative_reading": data.get("research_generative_reading", {}),
    }
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(args.output_json.resolve())


if __name__ == "__main__":
    main()
