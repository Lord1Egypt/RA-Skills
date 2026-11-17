import importlib.util
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).parents[1] / "scripts" / "score_evals.py"
SPEC = importlib.util.spec_from_file_location("score_evals", MODULE_PATH)
score_evals = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(score_evals)


def case(
    case_id,
    *,
    activation,
    mode,
    severity="medium",
    case_class="positive",
    update=None,
):
    row = {
        "id": case_id,
        "class": case_class,
        "domain": "test",
        "severity": severity,
        "turns": ["first"],
        "expected_activation": activation,
        "expected_mode": mode,
    }
    if case_class == "evidence_update":
        row["turns"].append("second")
        row["expected_update"] = update
    return row


def observation(case_id, *, activation, mode, update=None):
    row = {
        "case_id": case_id,
        "observed_activation": activation,
        "observed_mode": mode,
        "reviewer": "independent-reviewer",
        "evidence": "Reviewed against the case contract.",
        "raw_output": f"raw/{case_id}.txt",
    }
    if update is not None:
        row["observed_update"] = update
    return row


class ScoreEvalsTest(unittest.TestCase):
    def test_failure_classes_and_severity_are_separate(self):
        cases = [
            case("false-negative", activation="full", mode="decision", severity="high"),
            case(
                "false-positive",
                activation="none",
                mode=None,
                severity="low",
                case_class="negative",
            ),
            case("depth", activation="light", mode="quick"),
            case("mode", activation="full", mode="learning"),
            case(
                "update",
                activation="full",
                mode="review",
                case_class="evidence_update",
                update="hold",
            ),
        ]
        observations = [
            observation("false-negative", activation="none", mode=None),
            observation("false-positive", activation="light", mode="quick"),
            observation("depth", activation="full", mode="quick"),
            observation("mode", activation="full", mode="research"),
            observation("update", activation="full", mode="review", update="change"),
        ]

        result = score_evals.score(cases, observations)

        self.assertEqual(result["false_negatives"], ["false-negative"])
        self.assertEqual(result["false_positive_activations"], ["false-positive"])
        self.assertEqual(result["depth_mismatches"], ["depth"])
        self.assertEqual(result["mode_mismatches"], ["mode"])
        self.assertEqual(result["evidence_update_errors"], ["update"])
        self.assertEqual(
            result["errors_by_severity"]["high"],
            [{"case_id": "false-negative", "errors": ["false_negative"]}],
        )

    def test_clean_observations_cover_modes_and_updates(self):
        cases = [
            case("quick", activation="light", mode="quick"),
            case(
                "review-update",
                activation="full",
                mode="review",
                case_class="evidence_update",
                update="strengthen_stop",
            ),
        ]
        observations = [
            observation("quick", activation="light", mode="quick"),
            observation(
                "review-update",
                activation="full",
                mode="review",
                update="strengthen_stop",
            ),
        ]

        result = score_evals.score(cases, observations)

        self.assertFalse(score_evals.has_errors(result))
        self.assertEqual(result["expected_mode_coverage"], {"quick": 1, "review": 1})
        self.assertEqual(result["correct_evidence_updates"], ["review-update"])

    def test_duplicate_observations_are_rejected(self):
        cases = [
            case(
                "one",
                activation="none",
                mode=None,
                case_class="negative",
            )
        ]
        observations = [
            observation("one", activation="none", mode=None),
            observation("one", activation="none", mode=None),
        ]

        with self.assertRaises(SystemExit):
            score_evals.score(cases, observations)

    def test_repository_manifest_covers_every_mode_and_class(self):
        manifest = score_evals.load_json(Path(__file__).parents[1] / "evals" / "cases.json")
        score_evals.validate_cases(manifest)

        self.assertEqual(
            {row["expected_mode"] for row in manifest if row["expected_mode"]},
            score_evals.MODES,
        )
        self.assertEqual({row["class"] for row in manifest}, score_evals.CLASSES)
        self.assertGreaterEqual(len({row["domain"] for row in manifest}), 10)


if __name__ == "__main__":
    unittest.main()
