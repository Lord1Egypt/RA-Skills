"""Validate structured review artifacts and advance exactly one review gate."""

from pathlib import Path

from .io import read_json, safe_id, sha256_file, write_json_atomic
from .state import _find_chapter_body_path, read_chapter_state, transition_chapter


class ReviewError(ValueError):
    pass


def apply_review(root, review):
    if not isinstance(review, dict) or review.get("kind") not in ("text", "engine"):
        raise ReviewError("review kind must be text or engine")
    chapter = review.get("chapter")
    if not safe_id(chapter) or review.get("result") not in ("PASS", "FAIL"):
        raise ReviewError("review requires chapter and PASS/FAIL result")
    body = _find_chapter_body_path(root, chapter)
    if body is None or not body.is_file() or sha256_file(body) != review.get("source_hash"):
        raise ReviewError("review source hash does not match chapter body")
    if review.get("result") != "PASS":
        raise ReviewError("failed review cannot advance a chapter")
    state = read_chapter_state(root, chapter)
    expected_status = "DRAFTED" if review["kind"] == "text" else "TEXT_PASS"
    target = "TEXT_PASS" if review["kind"] == "text" else "ENGINE_PASS"
    if state["status"] != expected_status:
        raise ReviewError("{} review requires {}".format(review["kind"], expected_status))
    output = Path(root) / ".novelforge" / "reviews" / (chapter + "-" + review["kind"] + ".json")
    write_json_atomic(output, review)
    review_hash = sha256_file(output)
    current_hashes = dict(state.get("metadata", {}).get("review_hashes", {}))
    current_hashes[review["kind"]] = review_hash
    return transition_chapter(
        root,
        chapter,
        target,
        {
            "review": str(output.name),
            "review_kind": review["kind"],
            "review_hash": review_hash,
            "review_hashes": current_hashes,
        },
    )
