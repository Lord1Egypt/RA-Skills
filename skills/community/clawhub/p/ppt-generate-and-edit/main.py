"""Public entrypoints for the PPT skill module."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List

from .ppt_editor import update_ppt as _update_ppt
from .ppt_generator import create_ppt as _create_ppt
from .utils import get_logger, save_json

logger = get_logger(__name__)


def create_ppt(title: str, slides: List[Dict[str, object]]) -> str:
    """Agent-facing create API that delegates to the generator module."""
    logger.info("main.create_ppt called title=%s", title)
    return _create_ppt(title=title, slides=slides)


def update_ppt(ppt_path: str, replace_rules: Dict[str, Any]) -> Dict[str, Any]:
    """Agent-facing update API that returns new PPT path and replace log."""
    logger.info("main.update_ppt called path=%s", ppt_path)
    return _update_ppt(ppt_path=ppt_path, replace_rules=replace_rules)


def run_brazil_to_chile_demo() -> Dict[str, Any]:
    """Run a complete demo flow: create Brazil PPT then produce Chile version."""
    logger.info("Running Brazil -> Chile demo")
    brazil_slides = [
        {
            "title": "Brazil Overview",
            "content": [
                "Brazil is the largest country in South America.",
                "Its economy is driven by agriculture, mining, and services.",
            ],
            "image_prompt": "Brazil flag and skyline of Sao Paulo",
        },
        {
            "title": "Brazil Ports",
            "content": [
                "Santos is one of the busiest ports in Latin America.",
                "Brazil has strong Atlantic shipping connections.",
            ],
            "image_prompt": "Port of Santos containers and cargo ships",
        },
    ]
    brazil_ppt = _create_ppt(title="Brazil Trade Briefing", slides=brazil_slides)

    replace_rules = {
        "text_replace": {
            "Brazil": "Chile",
            "Sao Paulo": "Santiago",
            "Santos": "Valparaiso",
            "Atlantic": "Pacific",
        },
        "image_replace": {
            "__all__": {"prompt": "Chile flag and Chilean port logistics scene"}
        },
    }
    result = _update_ppt(ppt_path=brazil_ppt, replace_rules=replace_rules)

    # Persist logs for debugging and agent traceability.
    log_path = Path(result["new_ppt_path"]).with_suffix(".replace_log.json")
    save_json(result["replace_log"], log_path)
    logger.info("Demo finished. Brazil PPT=%s Chile PPT=%s", brazil_ppt, result["new_ppt_path"])

    return {
        "brazil_ppt_path": brazil_ppt,
        "chile_ppt_path": result["new_ppt_path"],
        "replace_log_path": str(log_path),
        "replace_log": result["replace_log"],
    }


if __name__ == "__main__":
    demo_result = run_brazil_to_chile_demo()
    print("Demo result:")
    for key, value in demo_result.items():
        if key == "replace_log":
            print(f"- {key}: <omitted in stdout, check log file>")
            continue
        print(f"- {key}: {value}")
