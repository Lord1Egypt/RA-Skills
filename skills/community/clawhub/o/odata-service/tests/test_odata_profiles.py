import argparse
import importlib.util
import pathlib
import tempfile
import unittest


SCRIPT_DIR = pathlib.Path(__file__).parents[1] / "scripts"
SPEC = importlib.util.spec_from_file_location("odata_profiles", SCRIPT_DIR / "odata_profiles.py")
profiles = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(profiles)


class ODataProfileTests(unittest.TestCase):
    def test_save_load_and_default_resolution(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = pathlib.Path(temp_dir) / "services.json"
            value = profiles.empty_config()
            value["profiles"]["production"] = {
                "service_root": "https://api.example.test/odata",
                "odata_version": "4.01",
                "bearer_env": "PROD_ODATA_TOKEN",
                "headers_from_env": {"X-Tenant": "PROD_TENANT"},
            }
            value["default_profile"] = "production"
            profiles.save_config(path, value)
            args = argparse.Namespace(
                service_root=None,
                profile=None,
                config=str(path),
                odata_version=None,
                bearer_env=None,
                basic_user_env=None,
                basic_password_env=None,
                header_env=[],
            )
            profiles.resolve_profile_args(args)
            self.assertEqual(args.service_root, "https://api.example.test/odata/")
            self.assertEqual(args.odata_version, "4.01")
            self.assertEqual(args.bearer_env, "PROD_ODATA_TOKEN")
            self.assertEqual(args.header_env, ["X-Tenant=PROD_TENANT"])

    def test_explicit_service_root_does_not_require_config(self):
        args = argparse.Namespace(
            service_root="https://api.example.test/odata",
            profile=None,
            config="missing.json",
            odata_version=None,
        )
        profiles.resolve_profile_args(args)
        self.assertEqual(args.service_root, "https://api.example.test/odata/")
        self.assertEqual(args.odata_version, "4.0")

    def test_profile_rejects_embedded_credentials_and_invalid_env_names(self):
        with self.assertRaisesRegex(ValueError, "embedded credentials"):
            profiles.validate_profile("bad", {"service_root": "https://user:pass@example.test/odata"})
        with self.assertRaisesRegex(ValueError, "environment variable"):
            profiles.validate_profile(
                "bad",
                {"service_root": "https://example.test/odata", "bearer_env": "not an env name"},
            )

    def test_profile_and_explicit_root_are_mutually_exclusive(self):
        args = argparse.Namespace(
            service_root="https://api.example.test/odata",
            profile="production",
            config=None,
            odata_version=None,
        )
        with self.assertRaisesRegex(ValueError, "either --service-root or --profile"):
            profiles.resolve_profile_args(args)


if __name__ == "__main__":
    unittest.main()
