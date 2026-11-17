#!/usr/bin/env python3
"""Small offline tests for the M5Burner query CLI."""

from __future__ import annotations

import contextlib
import io
import json
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

import m5stack_firmware_query as cli


class MockHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        query = parse_qs(parsed.query)
        payload: dict[str, object]

        if parsed.path == "/api/v1/devices":
            payload = {
                "code": 200,
                "msg": "ok",
                "data": [
                    {
                        "deviceId": "device-cores3",
                        "deviceCode": "CORES3",
                        "deviceName": "CoreS3",
                        "deviceSlug": "",
                        "firmwareCount": 2,
                    }
                ],
            }
        elif parsed.path == "/api/v1/firmware-categories":
            payload = {
                "code": 200,
                "msg": "ok",
                "data": [
                    {
                        "categoryId": "category-tools",
                        "categoryCode": "TOOLS",
                        "categoryName": "Tools",
                        "firmwareCount": 1,
                    }
                ],
                "totalFirmwareCount": 1,
            }
        elif parsed.path == "/api/v1/firmwares":
            assert query.get("deviceId") in (["device-cores3"], None)
            if "categoryId" in query:
                assert query.get("categoryId") == ["category-tools"]
            payload = {
                "code": 200,
                "msg": "ok",
                "rows": [
                    {
                        "firmwareId": "firmware-1",
                        "firmwareName": "Demo Firmware",
                        "uploadedAt": "2026-09-10T00:00:00Z",
                        "currentVersion": {
                            "versionName": "v1.2",
                            "publishTime": "2026-09-10T00:00:00Z",
                        },
                        "supportedDevices": [{"deviceName": "CoreS3"}],
                        "categories": [{"categoryName": "Development & Learning"}],
                        "statistics": {"downloadCount": 7},
                    },
                    {
                        "firmwareId": "music-1",
                        "firmwareName": "M5 Music CoreS3",
                        "firmwareDescription": json.dumps(
                            {
                                "format": "markdown",
                                "content": "Music sequencer with SD card samples and MIDI export.",
                            }
                        ),
                        "uploadedAt": "2026-09-10T00:00:00Z",
                        "currentVersion": {
                            "versionName": "v3.0",
                            "publishTime": "2026-09-10T00:00:00Z",
                        },
                        "supportedDevices": [{"deviceName": "CoreS3"}],
                        "categories": [{"categoryName": "Audio & Media"}],
                        "statistics": {"downloadCount": 3, "likeCount": 1},
                    }
                ],
                "total": 2,
            }
        elif parsed.path == "/api/v1/firmwares/music-1":
            payload = {
                "code": 200,
                "msg": "ok",
                "data": {
                    "firmwareId": "music-1",
                    "firmwareName": "M5 Music CoreS3",
                    "firmwareDescription": json.dumps(
                        {
                            "format": "markdown",
                            "content": "Music sequencer with SD card samples and MIDI export.",
                        }
                    ),
                    "sourceUrl": "https://example.invalid/music",
                    "sourceType": "COMMUNITY",
                    "currentVersion": {
                        "versionId": "music-version-1",
                        "versionName": "v3.0",
                        "status": "PUBLISHED",
                        "publishTime": "2026-09-10T00:00:00Z",
                    },
                    "supportedDevices": [{"deviceName": "CoreS3"}],
                    "categories": [{"categoryName": "Audio & Media"}],
                    "statistics": {"downloadCount": 3, "likeCount": 1},
                },
            }
        elif parsed.path == "/api/v1/firmwares/firmware-1":
            payload = {
                "code": 200,
                "msg": "ok",
                "data": {
                    "firmwareId": "firmware-1",
                    "firmwareName": "Demo Firmware",
                    "currentVersion": {
                        "versionName": "v1.2",
                        "status": "PUBLISHED",
                        "publishTime": "2026-09-10T00:00:00Z",
                    },
                    "supportedDevices": [{"deviceName": "CoreS3"}],
                    "categories": [{"categoryName": "Development & Learning"}],
                    "statistics": {"downloadCount": 7},
                },
            }
        elif parsed.path == "/api/v1/firmwares/firmware-1/versions":
            payload = {
                "code": 200,
                "msg": "ok",
                "data": [
                    {
                        "versionId": "version-1",
                        "versionName": "v1.2",
                        "publishTime": "2026-09-10T00:00:00Z",
                        "status": "PUBLISHED",
                        "current": True,
                        "downloadCount": 7,
                    }
                ],
            }
        elif parsed.path == "/api/v1/devices/by-slug/blocked":
            body = json.dumps(
                {
                    "code": 401,
                    "msg": "login required",
                    "requestId": "mock-request-id",
                }
            ).encode("utf-8")
            self.send_response(401)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        else:
            self.send_response(404)
            self.end_headers()
            return

        body = json.dumps(payload).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *_args: object) -> None:
        return


class FirmwareQueryCliTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.server = ThreadingHTTPServer(("127.0.0.1", 0), MockHandler)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.base_url = f"http://127.0.0.1:{cls.server.server_port}"

    @classmethod
    def tearDownClass(cls) -> None:
        cls.server.shutdown()
        cls.thread.join(timeout=2)

    def run_cli(self, *args: str) -> tuple[int, str]:
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            code = cli.main(
                [
                    *args,
                    "--base-url",
                    self.base_url,
                    "--format",
                    "json",
                ]
            )
        return code, output.getvalue()

    def test_name_filters_are_resolved_before_search(self) -> None:
        code, output = self.run_cli(
            "search",
            "--device-name",
            "CoreS3",
            "--category-name",
            "Tools",
        )
        self.assertEqual(code, 0)
        payload = json.loads(output)
        self.assertEqual(payload["total"], 2)
        self.assertEqual(payload["rows"][0]["firmwareName"], "Demo Firmware")

    def test_intent_search_returns_derived_counts(self) -> None:
        code, output = self.run_cli(
            "intent-search",
            "--intent",
            "ai",
            "--device-name",
            "CoreS3",
        )
        self.assertEqual(code, 0)
        payload = json.loads(output)
        self.assertEqual(payload["candidateTotal"], 2)
        self.assertEqual(payload["categoryCandidateTotal"], 0)
        self.assertEqual(payload["matchedTotal"], 0)
        self.assertEqual(payload["excludedTotal"], 2)
        self.assertEqual(payload["notableExclusionTotal"], 0)

    def test_versions_are_read_only_and_json_serializable(self) -> None:
        code, output = self.run_cli("versions", "firmware-1")
        self.assertEqual(code, 0)
        payload = json.loads(output)
        self.assertEqual(payload["data"][0]["versionName"], "v1.2")

    def test_object_table_renderers_keep_object_fields(self) -> None:
        firmware = {
            "data": {
                "firmwareId": "firmware-1",
                "firmwareName": "Demo Firmware",
                "currentVersion": {
                    "versionName": "v1.2",
                    "status": "PUBLISHED",
                    "publishTime": "2026-09-10T00:00:00Z",
                },
                "supportedDevices": [{"deviceName": "CoreS3"}],
                "statistics": {"downloadCount": 7},
            }
        }
        developer = {
            "data": {
                "developerId": "developer-1",
                "nickname": "Demo Developer",
                "statistics": {
                    "totalFirmware": 2,
                    "totalDownloads": 9,
                    "totalLikes": 3,
                    "totalFollowers": 1,
                },
            }
        }
        self.assertIn("Demo Firmware", cli.table_for("detail", firmware))
        self.assertIn("Demo Developer", cli.table_for("developer", developer))

    def test_authentication_errors_are_structured(self) -> None:
        code, output = self.run_cli("device-by-slug", "blocked")
        self.assertEqual(code, 2)
        payload = json.loads(output)
        self.assertEqual(payload["status"], 401)
        self.assertEqual(payload["requestId"], "mock-request-id")

    def test_recommend_device_enriches_interesting_candidates(self) -> None:
        code, output = self.run_cli(
            "recommend-device",
            "--device-name",
            "CoreS3",
            "--limit",
            "1",
            "--detail-limit",
            "2",
        )
        self.assertEqual(code, 0)
        payload = json.loads(output)
        first = payload["recommendations"][0]
        self.assertEqual(first["firmwareId"], "music-1")
        self.assertEqual(first["sourceUrl"], "https://example.invalid/music")
        self.assertIn("音乐", first["recommendation"]["kind"])
        self.assertIn("SD", " ".join(first["recommendation"]["needs"]))

    def test_ai_intent_requires_functional_signals(self) -> None:
        actual_ai = cli.firmware_record(
            {
                "firmwareId": "ai-1",
                "firmwareName": "Pocket Gemini Assistant",
                "firmwareDescription": "Chat with Gemini AI using the Cardputer.",
                "categories": [{"categoryName": "AI & Assistants"}],
            },
            self.base_url,
        )
        authoring_only = cli.firmware_record(
            {
                "firmwareId": "game-1",
                "firmwareName": "Space Invaders",
                "firmwareDescription": "A game made with Claude.",
                "categories": [{"categoryName": "AI & Assistants"}],
            },
            self.base_url,
        )
        generic_assistant = cli.firmware_record(
            {
                "firmwareId": "utility-1",
                "firmwareName": "Hike Assistant",
                "firmwareDescription": "GPS navigation and track recording for hikers.",
                "categories": [{"categoryName": "Utilities"}],
            },
            self.base_url,
        )

        actual_result = cli.classify_intent(actual_ai, "ai")
        authoring_result = cli.classify_intent(authoring_only, "ai")
        generic_result = cli.classify_intent(generic_assistant, "ai")
        profile = cli.recommendation_profile(actual_ai, include_baseline=True)
        self.assertTrue(actual_result["matched"])
        self.assertFalse(authoring_result["matched"])
        self.assertFalse(generic_result["matched"])
        self.assertIn("只提到项目由", authoring_result["reason"])
        self.assertIn("需要配置 Gemini API Key", profile["needs"])


if __name__ == "__main__":
    unittest.main()
