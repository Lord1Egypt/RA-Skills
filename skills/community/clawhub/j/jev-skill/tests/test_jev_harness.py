import copy
import json
import sys
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import jev_harness as harness  # noqa: E402
from jev_calibration import apply_calibration_profile, fit_temperature, scale_binary_probability  # noqa: E402


QUESTIONS = harness.validate_questions(
    {
        "urgent": {"type": "noul", "instructions": "Does this need urgent attention?"},
        "team": {
            "type": "choice",
            "instructions": "Which team should handle this?",
            "criteria": {"billing": "Charges", "technical": "Bugs", "other": "None"},
        },
        "severity": {
            "type": "score",
            "instructions": "How severe is this?",
            "criteria": ["Minor", "Material", "Critical"],
        },
    }
)
CASE = {
    "_index": 0,
    "id": "case-1",
    "tags": ["golden"],
    "state": {"message": "I was charged twice."},
    "expected": {"urgent": True, "team": "billing", "severity": {"level": 1, "tolerance": 0.5}},
}


def candidate_answers(verify: bool) -> dict[str, dict]:
    if verify:
        return {
            "verify_urgent": {"type": "noul", "noul": 0.95},
            "verify_team": {"type": "noul", "noul": 0.95},
            "verify_severity": {"type": "noul", "noul": 0.95},
        }
    return {
        "urgent": {"type": "noul", "noul": 0.95},
        "team": {
            "type": "choice",
            "choice": "billing",
            "probabilities": {"billing": 0.9, "technical": 0.05, "other": 0.05},
            "confidence": 0.9,
        },
        "severity": {
            "type": "score",
            "score": 1.0,
            "legend": {"0": "Minor", "1": "Material", "2": "Critical"},
            "probabilities": {"0": 0.0, "1": 1.0, "2": 0.0},
            "confidence": 1.0,
        },
    }


def options(base_url: str, *, provider: str = "openai-compatible", verify: bool = True, samples: int = 3) -> dict:
    return {
        "provider": provider,
        "model": "fake-local",
        "api_key": None,
        "base_url": base_url,
        "max_state_bytes": None,
        "timeout": 3.0,
        "retries": 0,
        "max_backoff": 0.1,
        "structured_output": True,
        "structured_protocol": "openai",
        "temperature": 0.3,
        "max_output_tokens": 256,
        "seed": 10,
        "allow_json_repair": False,
        "samples": samples,
        "min_valid_samples": samples,
        "noul_threshold": 0.5,
        "score_tolerance": 0.5,
        "consensus_threshold": 0.6,
        "verify": verify,
        "verifier_model": None,
        "verify_threshold": 0.7,
    }


class OpenAIHandler(BaseHTTPRequestHandler):
    calls = []

    def do_POST(self):  # noqa: N802 - stdlib handler API
        length = int(self.headers.get("Content-Length", "0"))
        body = json.loads(self.rfile.read(length))
        self.__class__.calls.append(body)
        prompt = body["messages"][-1]["content"]
        verify = "verify_urgent" in prompt
        content = {"model": body["model"], "answers": candidate_answers(verify)}
        envelope = {
            "model": body["model"],
            "choices": [{"message": {"content": json.dumps(content)}}],
            "usage": {"prompt_tokens": 10, "completion_tokens": 5},
        }
        encoded = json.dumps(envelope).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("x-request-id", f"test-{len(self.__class__.calls)}")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def log_message(self, *_args):
        return


class OllamaHandler(BaseHTTPRequestHandler):
    path_seen = None

    def do_POST(self):  # noqa: N802 - stdlib handler API
        self.__class__.path_seen = self.path
        length = int(self.headers.get("Content-Length", "0"))
        body = json.loads(self.rfile.read(length))
        content = {"model": body["model"], "answers": candidate_answers(False)}
        envelope = {
            "model": body["model"],
            "message": {"role": "assistant", "content": json.dumps(content)},
            "prompt_eval_count": 7,
            "eval_count": 8,
        }
        encoded = json.dumps(envelope).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def log_message(self, *_args):
        return


class OpenJevHandler(BaseHTTPRequestHandler):
    path_seen = None
    body_seen = None

    def do_POST(self):  # noqa: N802 - stdlib handler API
        self.__class__.path_seen = self.path
        length = int(self.headers.get("Content-Length", "0"))
        self.__class__.body_seen = json.loads(self.rfile.read(length))
        response = {
            "model": "gemma-3-4b-it",
            "answers": candidate_answers(False),
            "usage": {"input_tokens": 21, "output_tokens": 6},
        }
        encoded = json.dumps(response).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def log_message(self, *_args):
        return


class OpenJevHFHandler(BaseHTTPRequestHandler):
    path_seen = None
    body_seen = None

    def do_POST(self):  # noqa: N802 - stdlib handler API
        self.__class__.path_seen = self.path
        length = int(self.headers.get("Content-Length", "0"))
        self.__class__.body_seen = json.loads(self.rfile.read(length))
        embeddings = []
        for text in self.__class__.body_seen["text"]:
            if "urgent" in text:
                embeddings.append([0.0, 4.0, 0.0])
            elif "billing" in text:
                embeddings.append([0.0, 4.0, 0.0])
            elif "Material" in text:
                embeddings.append([0.0, 4.0, 0.0])
            else:
                embeddings.append([4.0, 0.0, 0.0])
        encoded = json.dumps([{"embedding": embedding} for embedding in embeddings]).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("x-request-id", "hf-test-1")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def log_message(self, *_args):
        return


class HarnessTests(unittest.TestCase):
    def test_provider_registry_describes_native_systemone_variants(self):
        for provider in ("openjev", "localjev", "von", "litjev", "simple-jev"):
            self.assertIn(provider, harness.PROVIDERS)
            self.assertIn(provider, harness.NATIVE_JEV_PROVIDERS)
            self.assertEqual(harness.local_endpoint(provider, "http://127.0.0.1:8000"), "http://127.0.0.1:8000/v1/systemone")
            capabilities = harness.provider_capabilities(provider)
            self.assertEqual(capabilities["protocol"], "systemone")
            self.assertIn("probability_semantics", capabilities)

    def test_calibration_profile_binding_rejects_wrong_model(self):
        profile = {
            "source": {"provider": "von", "model": "von-old", "question_sha256": "q"}
        }
        with self.assertRaises(ValueError):
            harness.calibration_binding_warnings(
                profile,
                provider="von",
                model="von-new",
                question_sha256="q",
            )

    def test_temperature_scaling_softens_overconfident_predictions(self):
        samples = [
            {"kind": "binary", "probability": 0.9, "label": True},
            {"kind": "binary", "probability": 0.9, "label": False},
            {"kind": "binary", "probability": 0.8, "label": True},
            {"kind": "binary", "probability": 0.8, "label": False},
        ]
        temperature = fit_temperature(samples, minimum=0.1, maximum=20.0)
        self.assertGreater(temperature, 1.0)
        self.assertLess(scale_binary_probability(0.9, temperature), 0.9)

    def test_calibration_profile_recomputes_typed_answers(self):
        response = {"model": "fake", "answers": candidate_answers(False)}
        profile = {
            "schema_version": "jev-calibration-v1",
            "profile_id": "test-profile",
            "temperatures": {"noul": 2.0, "choice": 2.0, "score": 2.0},
        }
        calibrated, warnings = apply_calibration_profile(response, QUESTIONS, profile)
        self.assertEqual(len(warnings), 1)
        self.assertLess(calibrated["answers"]["urgent"]["noul"], 0.95)
        self.assertAlmostEqual(sum(calibrated["answers"]["team"]["probabilities"].values()), 1.0)
        self.assertAlmostEqual(
            calibrated["answers"]["severity"]["score"],
            sum(float(key) * value for key, value in calibrated["answers"]["severity"]["probabilities"].items()),
        )
        harness.validate_response(calibrated, QUESTIONS)

    def test_score_probability_drift_is_rejected(self):
        answer = candidate_answers(False)
        answer["severity"]["score"] = 2.0
        with self.assertRaises(ValueError):
            harness.validate_response({"model": "fake", "answers": answer}, QUESTIONS)

    def test_strict_json_and_aggregation(self):
        with self.assertRaises(ValueError):
            harness.parse_local_json("Here is the answer: {\"ok\": true}", allow_repair=False)
        repaired, warnings = harness.parse_local_json("```json\n{\"ok\": true}\n```", allow_repair=True)
        self.assertEqual(repaired, {"ok": True})
        self.assertEqual(len(warnings), 1)

        responses = [
            {"model": "fake", "answers": {"urgent": {"type": "noul", "noul": value}}}
            for value in (0.8, 0.9, 1.0)
        ]
        answers, ensemble = harness.aggregate_answers(responses, {"urgent": QUESTIONS["urgent"]})
        self.assertAlmostEqual(answers["urgent"]["noul"], 0.9)
        self.assertEqual(ensemble["questions"]["urgent"]["agreement"], 1.0)

    def test_openai_compatible_ensemble_and_verifier(self):
        OpenAIHandler.calls = []
        server = ThreadingHTTPServer(("127.0.0.1", 0), OpenAIHandler)
        threading.Thread(target=server.serve_forever, daemon=True).start()
        try:
            record = harness.run_case(
                copy.deepcopy(CASE),
                QUESTIONS,
                options(f"http://127.0.0.1:{server.server_port}/v1"),
            )
        finally:
            server.shutdown()
            server.server_close()
        self.assertTrue(record["ok"], record)
        self.assertEqual(record["decision"], "accept")
        self.assertEqual(record["sample_count"], 3)
        self.assertEqual(record["valid_sample_count"], 3)
        self.assertTrue(record["verifier"]["urgent"]["accepted"])
        self.assertEqual(record["usage"], {"input_tokens": 40, "output_tokens": 20})
        self.assertEqual(len(OpenAIHandler.calls), 4)
        self.assertIn("response_format", OpenAIHandler.calls[0])

        summary = harness.summarize([record], QUESTIONS, None, None)
        self.assertEqual(summary["providers"], {"openai-compatible": 1})
        self.assertEqual(summary["exact_accuracy"], 1.0)
        self.assertEqual(summary["review_rate"], 0.0)

    def test_state_size_guardrail(self):
        guarded = options("http://127.0.0.1:1/v1", verify=False, samples=1)
        guarded["max_state_bytes"] = 1
        record = harness.run_case(copy.deepcopy(CASE), QUESTIONS, guarded)
        self.assertFalse(record["ok"])
        self.assertIn("maximum is 1", record["error"])

    def test_ollama_native_endpoint_and_usage(self):
        server = ThreadingHTTPServer(("127.0.0.1", 0), OllamaHandler)
        threading.Thread(target=server.serve_forever, daemon=True).start()
        try:
            response, _, _, warnings = harness.request_local(
                {"state": CASE["state"], "model": "fake-ollama", "questions": QUESTIONS},
                "ollama",
                "fake-ollama",
                f"http://127.0.0.1:{server.server_port}",
                None,
                3.0,
                0,
                0.1,
                True,
                "openai",
                0.0,
                256,
                None,
                False,
            )
        finally:
            server.shutdown()
            server.server_close()
        validated, validation_warnings = harness.validate_response(response, QUESTIONS)
        self.assertEqual(OllamaHandler.path_seen, "/api/chat")
        self.assertEqual(validated["usage"], {"input_tokens": 7, "output_tokens": 8})
        self.assertEqual(warnings, [])
        self.assertEqual(validation_warnings, [])

    def test_openjev_native_typed_endpoint_and_usage(self):
        OpenJevHandler.path_seen = None
        OpenJevHandler.body_seen = None
        server = ThreadingHTTPServer(("127.0.0.1", 0), OpenJevHandler)
        threading.Thread(target=server.serve_forever, daemon=True).start()
        try:
            record = harness.run_case(
                copy.deepcopy(CASE),
                QUESTIONS,
                options(
                    f"http://127.0.0.1:{server.server_port}",
                    provider="openjev",
                    verify=False,
                    samples=1,
                ),
            )
        finally:
            server.shutdown()
            server.server_close()
        self.assertTrue(record["ok"], record)
        self.assertEqual(record["model"], "gemma-3-4b-it")
        self.assertEqual(record["usage"], {"input_tokens": 21, "output_tokens": 6})
        self.assertEqual(OpenJevHandler.path_seen, "/v1/systemone")
        self.assertEqual(set(OpenJevHandler.body_seen), {"state", "model", "questions"})
        self.assertNotIn("messages", OpenJevHandler.body_seen)

    def test_localjev_native_typed_endpoint_alias(self):
        OpenJevHandler.path_seen = None
        OpenJevHandler.body_seen = None
        server = ThreadingHTTPServer(("127.0.0.1", 0), OpenJevHandler)
        threading.Thread(target=server.serve_forever, daemon=True).start()
        try:
            record = harness.run_case(
                copy.deepcopy(CASE),
                QUESTIONS,
                options(
                    f"http://127.0.0.1:{server.server_port}",
                    provider="localjev",
                    verify=False,
                    samples=1,
                ),
            )
        finally:
            server.shutdown()
            server.server_close()
        self.assertTrue(record["ok"], record)
        self.assertEqual(record["provider"], "localjev")
        self.assertEqual(OpenJevHandler.path_seen, "/v1/systemone")

    def test_openjev_hf_sglang_nli_adapter(self):
        OpenJevHFHandler.path_seen = None
        OpenJevHFHandler.body_seen = None
        server = ThreadingHTTPServer(("127.0.0.1", 0), OpenJevHFHandler)
        threading.Thread(target=server.serve_forever, daemon=True).start()
        try:
            record = harness.run_case(
                copy.deepcopy(CASE),
                QUESTIONS,
                options(
                    f"http://127.0.0.1:{server.server_port}",
                    provider="openjev-hf",
                    verify=False,
                    samples=1,
                ),
            )
        finally:
            server.shutdown()
            server.server_close()
        self.assertTrue(record["ok"], record)
        self.assertEqual(record["provider"], "openjev-hf")
        self.assertEqual(record["model"], "fake-local")
        self.assertEqual(OpenJevHFHandler.path_seen, "/classify")
        self.assertGreater(len(OpenJevHFHandler.body_seen["text"]), 1)
        self.assertTrue(any("maps three-way NLI" in warning for warning in record["warnings"]))
        self.assertEqual(record["answers"]["team"]["choice"], "billing")
        self.assertEqual(record["answers"]["severity"]["legend"]["1"], "Material")


if __name__ == "__main__":
    unittest.main()
