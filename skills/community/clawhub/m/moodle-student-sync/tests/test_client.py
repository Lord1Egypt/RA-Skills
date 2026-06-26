import sys
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.moodle_client import MoodleAPIError, MoodleClient, flatten_params


class _FakeResponse:
    def __init__(self, payload):
        self._payload = payload

    def raise_for_status(self):
        return None

    def json(self):
        return self._payload


class _FakeSession:
    def __init__(self, payload):
        self.payload = payload
        self.last_params = None

    def get(self, _url, params, timeout):
        self.last_params = params
        self.last_timeout = timeout
        return _FakeResponse(self.payload)


class MoodleClientTests(unittest.TestCase):
    def test_flatten_params_supports_nested_values(self):
        params = {
            "courseids": [101, 102],
            "options": [{"name": "timestart", "value": 1710000000}],
        }
        flat = flatten_params(params)
        self.assertEqual(flat["courseids[0]"], 101)
        self.assertEqual(flat["courseids[1]"], 102)
        self.assertEqual(flat["options[0][name]"], "timestart")
        self.assertEqual(flat["options[0][value]"], 1710000000)

    @patch("scripts.moodle_client.time.sleep")
    def test_call_raises_on_moodle_exception(self, _sleep):
        session = _FakeSession(
            {
                "exception": "core\\exception\\invalidparameter",
                "errorcode": "invalidparameter",
                "message": "Invalid parameter value detected",
            }
        )
        client = MoodleClient("https://moodle.example.edu", "token", session=session)
        with self.assertRaises(MoodleAPIError):
            client.call("core_webservice_get_site_info")

    @patch("scripts.moodle_client.time.sleep")
    def test_call_success_includes_required_auth_fields(self, _sleep):
        session = _FakeSession({"userid": 123})
        client = MoodleClient("https://moodle.example.edu", "secret", session=session)
        payload = client.call("core_webservice_get_site_info")
        self.assertEqual(payload["userid"], 123)
        self.assertEqual(session.last_params["wstoken"], "secret")
        self.assertEqual(session.last_params["wsfunction"], "core_webservice_get_site_info")
        self.assertEqual(session.last_params["moodlewsrestformat"], "json")


if __name__ == "__main__":
    unittest.main()
