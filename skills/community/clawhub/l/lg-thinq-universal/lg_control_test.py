import json
import unittest

from scripts.assemble_device_workspace import build_skill_markdown, slugify
from scripts.generate_control_script import generate_script


PROFILE = {
    "response": {
        "property": {
            "operation": {
                "airConOperationMode": {
                    "type": "enum",
                    "mode": ["r", "w"],
                    "value": {"r": ["POWER_OFF", "POWER_ON"], "w": ["POWER_OFF", "POWER_ON"]},
                }
            },
            "temperature": {
                "coolTargetTemperature": {
                    "type": "range",
                    "mode": ["w"],
                    "value": {"w": {"min": 16, "max": 30, "step": 0.5}},
                }
            },
            "windDirection": {
                "rotateLeftRight": {
                    "type": "boolean",
                    "mode": ["r", "w"],
                    "value": {"r": [True, False], "w": [True, False]},
                }
            },
            "timer": {
                "absoluteHourToStop": {
                    "type": "number",
                    "mode": ["r", "w"],
                }
            },
        }
    }
}


class GenerateControlScriptTests(unittest.TestCase):
    def test_generated_script_has_no_confirm_requirement(self):
        script = generate_script(json.dumps(PROFILE))
        self.assertIn('print("  on                  Turn device on (POWER_ON)")', script)
        self.assertNotIn("--confirm", script)

    def test_generated_script_includes_power_commands(self):
        script = generate_script(json.dumps(PROFILE))
        self.assertIn("elif cmd == 'on':", script)
        self.assertIn("elif cmd == 'off':", script)
        self.assertNotIn("\\n        print(json.dumps(control_property", script)

    def test_generated_script_parses_typed_values(self):
        script = generate_script(json.dumps(PROFILE))
        self.assertIn("parse_number(filtered_args[1])", script)
        self.assertIn("filtered_args[1].lower() in ('1', 'true', 'yes', 'on')", script)


class AssembleWorkspaceTests(unittest.TestCase):
    def test_slugify_normalizes_locations(self):
        self.assertEqual(slugify("Living Room"), "living-room")
        self.assertEqual(slugify("  ### "), "device")

    def test_skill_markdown_uses_workspace_path_and_shell_env(self):
        doc = build_skill_markdown(
            skill_name="lg-ac-living-room",
            device_name="Living Room AC",
            device_type="ac",
            skill_path="/home/test/.openclaw/workspace/skills/lg-ac-living-room",
            properties=PROFILE["response"]["property"],
        )
        self.assertIn("/home/test/.openclaw/workspace/skills/lg-ac-living-room", doc)
        self.assertIn("LG_PAT", doc)
        self.assertIn("python lg_control.py on", doc)


if __name__ == "__main__":
    unittest.main()
