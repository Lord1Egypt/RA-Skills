#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Offline unit tests for huawei-cloud-rms-list (no credentials, no network).

Every hcloud invocation is mocked, so the tests cover: the write-intent guard,
command construction, JSON extraction and error-envelope classification
(including the RMS.00010006 permission envelope returned on stdout with rc=0),
marker paging, offset paging for providers, the SDK fallback, the output
renderers and the atomic file export.

Run from the skill directory:
    python3 -m unittest discover -s tests -v
"""

import io
import json
import os
import sys
import tempfile
import unittest
from contextlib import redirect_stdout, redirect_stderr

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPTS = os.path.join(os.path.dirname(HERE), "scripts")
sys.path.insert(0, SCRIPTS)
sys.dont_write_bytecode = True

import list_rms_resources as rms  # noqa: E402


def _proc(stdout="", stderr="", returncode=0):
    class P:
        pass

    p = P()
    p.stdout = stdout
    p.stderr = stderr
    p.returncode = returncode
    return p


class GuardTests(unittest.TestCase):
    def test_read_verbs_pass(self):
        for text in ("ListAllResources", "ListProviders", "RMS ListRegions",
                     "rms:resources:list", "list_rms_resources"):
            self.assertFalse(rms.guard_write_intent(text))

    def test_mutating_intents_blocked(self):
        for text in ("CreateConfigurationAggregator", "delete-aggregator",
                     "delete_configuration_aggregator", "UpdateTrackerConfig",
                     "enable policy assignment", "DeleteStoredQuery"):
            with self.assertRaises(rms.GuardError):
                rms.guard_write_intent(text)

    def test_operation_whitelist(self):
        for op in rms.ALLOWED_OPERATIONS:
            self.assertTrue(rms.guard_operation(op))
        with self.assertRaises(rms.GuardError):
            rms.guard_operation("DeletePolicyAssignment")

    def test_value_flags_stripped_from_guard_text(self):
        text = rms.guard_text_from_argv(
            ["--name", "delete-me", "--output", "rms-delete-report.json",
             "--region", "cn-north-4"])
        self.assertNotIn("delete-me", text)
        self.assertNotIn("rms-delete-report", text)

    def test_following_flag_still_scanned(self):
        text = rms.guard_text_from_argv(["--name", "--create-aggregator"])
        self.assertIn("--create-aggregator", text)


class ResolveOperationTests(unittest.TestCase):
    def test_default_all_resources(self):
        self.assertEqual(rms.resolve_operation(), "ListAllResources")

    def test_provider_type_scoped(self):
        self.assertEqual(
            rms.resolve_operation(provider="ecs", resource_type="cloudservers"),
            "ListResources")

    def test_provider_without_type_errors(self):
        with self.assertRaises(rms.ApiError):
            rms.resolve_operation(provider="ecs")

    def test_convenience_flags(self):
        self.assertEqual(rms.resolve_operation(list_providers=True), "ListProviders")
        self.assertEqual(rms.resolve_operation(list_regions=True), "ListRegions")


class CommandBuildTests(unittest.TestCase):
    def test_list_all_resources_filters(self):
        argv = rms.build_command(
            "ListAllResources", "cn-north-4", region_id="cn-north-4",
            resource_type="ecs.cloudservers", name="web", tags=["k=v"],
            limit=50, marker="M1")
        self.assertEqual(argv[:3], ["RMS", "ListAllResources", "--cli-region=cn-north-4"])
        self.assertIn("--region_id=cn-north-4", argv)
        self.assertIn("--type=ecs.cloudservers", argv)
        self.assertIn("--name=web", argv)
        self.assertIn("--tags.1=k=v", argv)
        self.assertIn("--limit=50", argv)
        self.assertIn("--marker=M1", argv)

    def test_scoped_list_requires_provider_type(self):
        argv = rms.build_command("ListResources", "cn-north-4", provider="ecs",
                                 resource_type="cloudservers", limit=10)
        self.assertIn("--provider=ecs", argv)
        self.assertIn("--type=cloudservers", argv)

    def test_list_providers_offset(self):
        argv = rms.build_command("ListProviders", "cn-north-4", limit=5, offset=10)
        self.assertIn("--offset=10", argv)
        self.assertIn("--limit=5", argv)

    def test_domain_id_and_language(self):
        argv = rms.build_command("ListRegions", "cn-north-4", domain_id="d1",
                                 language="en-us")
        self.assertIn("--domain_id=d1", argv)
        self.assertIn("--X-Language=en-us", argv)


class JsonAndEnvelopeTests(unittest.TestCase):
    def test_extract_json_with_noise(self):
        payload = rms.extract_json("noise\n{\"resources\": []}\n")
        self.assertEqual(payload, {"resources": []})

    def test_extract_json_raises_on_garbage(self):
        with self.assertRaises(rms.ApiError):
            rms.extract_json("not json at all")

    def test_payload_error_top_level(self):
        text = rms._payload_error(
            {"error_code": "RMS.00010006", "error_msg": "not authorized"})
        self.assertIn("RMS.00010006", text)

    def test_payload_error_nested(self):
        text = rms._payload_error({"error": {"code": "403", "message": "denied"}})
        self.assertIn("403", text)

    def test_payload_ok_returns_none(self):
        self.assertIsNone(rms._payload_error({"resources": [{"id": "x"}]}))

    def test_classify_permission_envelope(self):
        err = rms.classify_hcloud_failure("", "RMS.00010006 not authorized", 0)
        self.assertIsInstance(err, rms.AuthError)

    def test_classify_missing_credentials(self):
        err = rms.classify_hcloud_failure("", "no ak/sk configured", 1)
        self.assertIsInstance(err, rms.ConfigError)

    def test_classify_use_error(self):
        err = rms.classify_hcloud_failure("[USE_ERROR] invalid parameter", "", 0)
        self.assertIsInstance(err, rms.ApiError)
        self.assertIn("参数错误", str(err))


class PagingTests(unittest.TestCase):
    def setUp(self):
        self._orig = rms.run_hcloud

    def tearDown(self):
        rms.run_hcloud = self._orig

    def test_marker_paging(self):
        pages = [
            {"resources": [{"id": "1"}], "page_info": {"next_marker": "M2"}},
            {"resources": [{"id": "2"}], "page_info": {"next_marker": ""}},
        ]
        calls = {"n": 0}

        def fake(argv):
            page = pages[calls["n"]]
            calls["n"] += 1
            return json.dumps(page), "", 0

        rms.run_hcloud = fake
        items = rms.list_items("ListAllResources", "cn-north-4", limit=1)
        self.assertEqual([i["id"] for i in items], ["1", "2"])
        self.assertEqual(calls["n"], 2)

    def test_provider_offset_paging(self):
        pages = [
            {"resource_providers": [{"provider": "ecs"}], "total_count": 2},
            {"resource_providers": [{"provider": "vpc"}], "total_count": 2},
        ]
        calls = {"n": 0}

        def fake(argv):
            page = pages[calls["n"]]
            calls["n"] += 1
            return json.dumps(page), "", 0

        rms.run_hcloud = fake
        items = rms.list_items("ListProviders", "cn-north-4", limit=1)
        self.assertEqual([i["provider"] for i in items], ["ecs", "vpc"])

    def test_regions_single_page(self):
        def fake(argv):
            return json.dumps({"value": [{"region_id": "cn-north-4"}]}), "", 0

        rms.run_hcloud = fake
        items = rms.list_items("ListRegions", "cn-north-4")
        self.assertEqual(items[0]["region_id"], "cn-north-4")


class RenderTests(unittest.TestCase):
    RESOURCES = [
        {"id": "r1", "name": "web", "provider": "ecs", "type": "cloudservers",
         "region_id": "cn-north-4", "ep_name": "default",
         "provisioning_state": "Succeeded", "created": "2024-01-01",
         "updated": "2024-01-02", "tags": {"env": "prod"}},
    ]

    def test_table_has_key_columns(self):
        text = rms.render_table(self.RESOURCES, "ListAllResources")
        self.assertIn("id", text)
        self.assertIn("web", text)
        self.assertIn("env=prod", text)

    def test_markdown_headers_and_empty(self):
        text = rms.render_markdown(self.RESOURCES, "ListAllResources", summary=True,
                                   region="cn-north-4")
        self.assertIn("资源 ID", text)
        self.assertIn("web", text)
        empty = rms.render_markdown([], "ListAllResources")
        self.assertIn("资源 ID", empty)

    def test_csv_union_columns(self):
        text = rms.render_csv(self.RESOURCES, "ListAllResources")
        self.assertIn("id", text.splitlines()[0])
        self.assertIn("web", text)

    def test_json_roundtrip(self):
        text = rms.render_json(self.RESOURCES)
        self.assertEqual(json.loads(text)[0]["id"], "r1")

    def test_provider_resource_types_flattened(self):
        record = {"provider": "ecs", "resource_types": [{"name": "cloudservers"}]}
        flat = rms.normalize_record(record)
        self.assertEqual(flat["resource_types"], "cloudservers")


class ExportTests(unittest.TestCase):
    def test_atomic_export_and_dir_creation(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = os.path.join(tmp, "nested", "out.json")
            written = rms.export_report([{"id": "r1"}], target, "ListAllResources",
                                        "json")
            self.assertTrue(os.path.isfile(written))
            self.assertEqual(json.load(open(written))[0]["id"], "r1")

    def test_empty_export_is_header_only(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = os.path.join(tmp, "empty.csv")
            rms.export_report([], target, "ListAllResources", "csv")
            self.assertTrue(os.path.isfile(target))


class SdkFallbackTests(unittest.TestCase):
    def setUp(self):
        self._orig_run = rms.run_hcloud
        self._orig_sdk = rms.list_items_via_sdk
        self._saved_env = {k: os.environ.get(k) for k in rms._AK_ENV_NAMES + rms._SK_ENV_NAMES}

    def tearDown(self):
        rms.run_hcloud = self._orig_run
        rms.list_items_via_sdk = self._orig_sdk
        for k, v in self._saved_env.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v

    def test_sdk_fallback_triggered_when_hcloud_missing(self):
        calls = {"sdk": 0}

        def fake_run(argv):
            raise rms.ConfigError("hcloud missing")

        def fake_sdk(*args, **kwargs):
            calls["sdk"] += 1
            return [{"id": "sdk-1"}]

        rms.run_hcloud = fake_run
        rms.list_items_via_sdk = fake_sdk
        items = rms.list_items("ListAllResources", "cn-north-4", limit=10)
        self.assertEqual(items, [{"id": "sdk-1"}])
        self.assertEqual(calls["sdk"], 1)

    def test_sdk_missing_credentials_raises_config_error(self):
        for name in rms._AK_ENV_NAMES + rms._SK_ENV_NAMES:
            os.environ.pop(name, None)
        with self.assertRaises(rms.ConfigError):
            rms.list_items_via_sdk("ListAllResources", "cn-north-4")


class MainOutputTests(unittest.TestCase):
    def setUp(self):
        self._orig_run = rms.run_hcloud

    def tearDown(self):
        rms.run_hcloud = self._orig_run

    def test_guard_blocks_mutating_argv(self):
        err = io.StringIO()
        with redirect_stderr(err):
            rc = rms.main(["--create-aggregator"])
        self.assertEqual(rc, 1)
        self.assertIn("写操作意图", err.getvalue())

    def test_table_empty_message(self):
        rms.run_hcloud = lambda argv: (json.dumps(
            {"resources": [], "page_info": {}}), "", 0)
        out = io.StringIO()
        with redirect_stdout(out):
            rc = rms.main(["--format", "table"])
        self.assertEqual(rc, 0)
        self.assertIn("无 ListAllResources 结果", out.getvalue())


if __name__ == "__main__":
    unittest.main()
