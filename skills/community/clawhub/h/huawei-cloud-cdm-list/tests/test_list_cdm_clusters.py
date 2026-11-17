#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Offline unit tests for huawei-cloud-cdm-list (no credentials, no network).

Every hcloud invocation is mocked (either the ``run_hcloud`` seam or a fake
executable through ``CDM_LIST_HCLOUD_BIN``), so the tests cover: the
write-intent guard, operation resolution, command construction (incl. the
"ListClusters has no query parameters" fact), JSON extraction and error-envelope
classification (including the permission envelope returned on stdout with
rc=0), client-side name/status filtering, cluster normalization, the SDK
fallback, the output renderers, atomic file export and ``--help``.

Run from the skill directory:
    python3 -m unittest discover -s tests -v
"""

import io
import json
import os
import stat
import sys
import tempfile
import unittest
from contextlib import redirect_stdout, redirect_stderr

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPTS = os.path.join(os.path.dirname(HERE), "scripts")
sys.path.insert(0, SCRIPTS)
sys.dont_write_bytecode = True

import list_cdm_clusters as cdm  # noqa: E402


def _proc(stdout="", stderr="", returncode=0):
    class P:
        pass

    p = P()
    p.stdout = stdout
    p.stderr = stderr
    p.returncode = returncode
    return p


CLUSTER_OK = {
    "id": "bae65496-643e-47ca-84af-948672de7eeb",
    "name": "cdm-c018",
    "status": "200",
    "statusDetail": "Normal",
    "datastore": {"type": "cdm", "version": "2.9.1"},
    "instances": [
        {"id": "vm-1", "name": "cdm-c018-1", "status": "200", "type": "cdm"},
    ],
    "created": "2018-09-05T08:38:25",
    "updated": "2018-09-05T08:38:25",
    "publicEndpoint": "49.0.0.10",
    "flavorName": "cdm.large",
    "azName": "cn-north-4a",
    "isFrozen": "0",
}
CLUSTER_FAIL = {
    "id": "aaaa1111-2222-3333-4444-555566667777",
    "name": "cdm-fail",
    "status": "300",
    "statusDetail": "Abnormal",
    "datastore": {"type": "cdm", "version": "2.9.1"},
    "instances": [],
    "created": "2024-01-01T00:00:00",
    "updated": "2024-01-02T00:00:00",
}
CLUSTERS_PAYLOAD = {"clusters": [CLUSTER_OK, CLUSTER_FAIL]}
DETAIL_PAYLOAD = {
    "id": "bae65496-643e-47ca-84af-948672de7eeb",
    "name": "cdm-c018",
    "status": "200",
    "statusDetail": "Normal",
    "datastore": {"type": "cdm", "version": "2.9.1"},
    "instances": [
        {"id": "vm-1", "name": "cdm-c018-1", "status": "200",
         "publicIp": "49.0.0.11", "manageIp": "192.168.0.11"},
    ],
    "vpc_id": "vpc-abc",
    "subnet_id": "subnet-abc",
    "security_group_id": "sg-abc",
    "eps_id": "0",
    "created": "2018-09-05T08:38:25",
}


class GuardTests(unittest.TestCase):
    def test_read_verbs_pass(self):
        for text in ("ListClusters", "ShowClusterDetail", "CDM ListClusters",
                     "cdm:cluster:list", "list_cdm_clusters"):
            self.assertFalse(cdm.guard_write_intent(text))

    def test_mutating_intents_blocked(self):
        for text in ("CreateCluster", "delete-cluster", "delete_cluster",
                     "RestartCluster", "StartCluster", "StopCluster",
                     "ModifyCluster", "DeleteCluster", "resize cluster",
                     "stop the cluster", "CreateAndStartRandomClusterJob"):
            with self.assertRaises(cdm.GuardError):
                cdm.guard_write_intent(text)

    def test_operation_whitelist(self):
        for op in cdm.ALLOWED_OPERATIONS:
            self.assertTrue(cdm.guard_operation(op))
        for op in ("CreateCluster", "DeleteCluster", "RestartCluster",
                   "StartCluster", "StopCluster", "ModifyCluster"):
            with self.assertRaises(cdm.GuardError):
                cdm.guard_operation(op)

    def test_value_flags_stripped_from_guard_text(self):
        text = cdm.guard_text_from_argv(
            ["--name", "cdm-delete-test", "--output", "cdm-delete-report.json",
             "--status", "stop-me", "--region", "cn-north-4"])
        self.assertNotIn("cdm-delete-test", text)
        self.assertNotIn("cdm-delete-report", text)
        self.assertNotIn("stop-me", text)

    def test_following_flag_still_scanned(self):
        text = cdm.guard_text_from_argv(["--name", "--create-cluster"])
        self.assertIn("--create-cluster", text)

    def test_extra_hcloud_args_guarded(self):
        saved = os.environ.get("CDM_LIST_HCLOUD_ARGS")
        os.environ["CDM_LIST_HCLOUD_ARGS"] = "--restart now"
        try:
            with self.assertRaises(cdm.GuardError):
                cdm.run_hcloud(["CDM", "ListClusters", "--cli-region=x"])
        finally:
            if saved is None:
                os.environ.pop("CDM_LIST_HCLOUD_ARGS", None)
            else:
                os.environ["CDM_LIST_HCLOUD_ARGS"] = saved

    def test_main_blocks_mutating_argv(self):
        err = io.StringIO()
        with redirect_stderr(err):
            rc = cdm.main(["--create-cluster"])
        self.assertEqual(rc, 1)
        self.assertIn("写操作意图", err.getvalue())


class ResolveOperationTests(unittest.TestCase):
    def test_default_list_clusters(self):
        self.assertEqual(cdm.resolve_operation(), "ListClusters")

    def test_cluster_id_selects_detail(self):
        self.assertEqual(cdm.resolve_operation(cluster_id="abc"),
                         "ShowClusterDetail")

    def test_explicit_operation(self):
        self.assertEqual(cdm.resolve_operation(explicit="ListClusters"),
                         "ListClusters")


class CommandBuildTests(unittest.TestCase):
    def test_list_clusters_has_no_query_parameters(self):
        # Official API fact: ListClusters takes NO query parameters.
        argv = cdm.build_command("ListClusters", "cn-north-4")
        self.assertEqual(argv, ["CDM", "ListClusters", "--cli-region=cn-north-4"])

    def test_show_cluster_detail_cluster_id(self):
        argv = cdm.build_command("ShowClusterDetail", "cn-north-4",
                                 cluster_id="abc-123")
        self.assertEqual(
            argv,
            ["CDM", "ShowClusterDetail", "--cli-region=cn-north-4",
             "--cluster_id=abc-123"])

    def test_detail_without_cluster_id_errors(self):
        with self.assertRaises(cdm.ApiError):
            cdm.build_command("ShowClusterDetail", "cn-north-4")

    def test_language_header(self):
        argv = cdm.build_command("ListClusters", "cn-north-4",
                                 language="en-us")
        self.assertIn("--X-Language=en-us", argv)

    def test_rest_paths(self):
        self.assertEqual(cdm.REST_PATHS["ListClusters"],
                         "/v1.1/{project_id}/clusters")
        self.assertEqual(cdm.REST_PATHS["ShowClusterDetail"],
                         "/v1.1/{project_id}/clusters/{cluster_id}")


class JsonAndEnvelopeTests(unittest.TestCase):
    def test_extract_json_with_noise(self):
        payload = cdm.extract_json("noise\n{\"clusters\": []}\n")
        self.assertEqual(payload, {"clusters": []})

    def test_extract_json_raises_on_garbage(self):
        with self.assertRaises(cdm.ApiError):
            cdm.extract_json("not json at all")

    def test_extract_clusters_container(self):
        self.assertEqual(cdm.extract_clusters(CLUSTERS_PAYLOAD), CLUSTERS_PAYLOAD["clusters"])
        self.assertEqual(cdm.extract_clusters([{"id": "x"}]), [{"id": "x"}])
        self.assertEqual(cdm.extract_clusters({}), [])

    def test_payload_error_top_level(self):
        text = cdm._payload_error(
            {"error_code": "CDM.00001203", "error_msg": "not authorized"})
        self.assertIn("CDM.00001203", text)

    def test_payload_error_nested(self):
        text = cdm._payload_error({"error": {"code": "403", "message": "denied"}})
        self.assertIn("403", text)

    def test_payload_ok_returns_none(self):
        self.assertIsNone(cdm._payload_error(CLUSTERS_PAYLOAD))

    def test_classify_permission_envelope(self):
        err = cdm.classify_hcloud_failure(
            "", "403 没有操作权限 cdm:cluster:list", 0)
        self.assertIsInstance(err, cdm.AuthError)

    def test_classify_missing_credentials(self):
        err = cdm.classify_hcloud_failure("", "no ak/sk configured", 1)
        self.assertIsInstance(err, cdm.ConfigError)

    def test_classify_use_error(self):
        err = cdm.classify_hcloud_failure("[USE_ERROR] invalid parameter", "", 0)
        self.assertIsInstance(err, cdm.ApiError)
        self.assertIn("参数错误", str(err))

    def test_classify_generic_api_error(self):
        err = cdm.classify_hcloud_failure("", "connection reset", 7)
        self.assertIsInstance(err, cdm.ApiError)


class FilterTests(unittest.TestCase):
    ITEMS = [CLUSTER_OK, CLUSTER_FAIL]

    def test_no_filter_returns_all(self):
        self.assertEqual(len(cdm._filter_clusters(self.ITEMS)), 2)

    def test_name_substring_case_insensitive(self):
        got = cdm._filter_clusters(self.ITEMS, name="C018")
        self.assertEqual([c["name"] for c in got], ["cdm-c018"])

    def test_status_code_match(self):
        got = cdm._filter_clusters(self.ITEMS, statuses=["300"])
        self.assertEqual([c["name"] for c in got], ["cdm-fail"])

    def test_status_meaning_match(self):
        got = cdm._filter_clusters(self.ITEMS, statuses=["正常"])
        self.assertEqual([c["name"] for c in got], ["cdm-c018"])

    def test_multi_status_union(self):
        got = cdm._filter_clusters(self.ITEMS, statuses=["200", "300"])
        self.assertEqual(len(got), 2)

    def test_no_match_empty(self):
        got = cdm._filter_clusters(self.ITEMS, name="no-such-cluster")
        self.assertEqual(got, [])


class NormalizeTests(unittest.TestCase):
    def test_camel_to_snake_and_derived_fields(self):
        flat = cdm.normalize_cluster(CLUSTER_OK)
        self.assertEqual(flat["status_detail"], "Normal")
        self.assertEqual(flat["flavor_name"], "cdm.large")
        self.assertEqual(flat["az_name"], "cn-north-4a")
        self.assertEqual(flat["public_endpoint"], "49.0.0.10")
        self.assertEqual(flat["version"], "2.9.1")
        self.assertEqual(flat["datastore_type"], "cdm")
        self.assertEqual(flat["instance_count"], 1)
        self.assertEqual(flat["instances"], "cdm-c018-1(200)")
        self.assertEqual(flat["status_meaning"], "正常")

    def test_unknown_status_falls_back_to_status_detail(self):
        record = dict(CLUSTER_FAIL, status="999")
        flat = cdm.normalize_cluster(record)
        self.assertEqual(flat["status_meaning"], "Abnormal")

    def test_empty_instances_rendered_as_dash(self):
        flat = cdm.normalize_cluster(CLUSTER_FAIL)
        self.assertEqual(flat["instance_count"], 0)
        self.assertEqual(flat["instances"], "-")

    def test_non_dict_record(self):
        self.assertEqual(cdm.normalize_cluster("oops"), {})


class ListAndDetailTests(unittest.TestCase):
    def setUp(self):
        self._orig_run = cdm.run_hcloud

    def tearDown(self):
        cdm.run_hcloud = self._orig_run

    def test_list_clusters_happy_path(self):
        calls = {"n": 0}

        def fake(argv):
            calls["n"] += 1
            self.assertEqual(argv, ["CDM", "ListClusters",
                                    "--cli-region=cn-north-4"])
            return json.dumps(CLUSTERS_PAYLOAD), "", 0

        cdm.run_hcloud = fake
        items = cdm.list_clusters("cn-north-4")
        self.assertEqual(len(items), 2)
        self.assertEqual(calls["n"], 1)

    def test_list_clusters_max_calls_does_not_duplicate(self):
        """--max-calls > 1 must not append the same full list twice (no paging)."""
        calls = {"n": 0}

        def fake(argv):
            calls["n"] += 1
            return json.dumps(CLUSTERS_PAYLOAD), "", 0

        cdm.run_hcloud = fake
        items = cdm.list_clusters("cn-north-4", max_calls=3)
        self.assertEqual([i["id"] for i in items],
                         [CLUSTER_OK["id"], CLUSTER_FAIL["id"]])
        self.assertEqual(calls["n"], 2)

    def test_list_clusters_error_envelope_on_stdout_rc0(self):
        cdm.run_hcloud = lambda argv: (
            json.dumps({"error_code": "CDM.00001203",
                        "error_msg": "403 not authorized"}), "", 0)
        with self.assertRaises(cdm.AuthError):
            cdm.list_clusters("cn-north-4")

    def test_list_clusters_nonzero_rc(self):
        cdm.run_hcloud = lambda argv: ("", "boom", 7)
        with self.assertRaises(cdm.ApiError):
            cdm.list_clusters("cn-north-4")

    def test_list_clusters_sdk_fallback_on_missing_hcloud(self):
        calls = {"sdk": 0}

        def fake_run(argv):
            raise cdm.ConfigError("hcloud missing")

        def fake_sdk(region):
            calls["sdk"] += 1
            return [{"id": "sdk-1"}]

        cdm.run_hcloud = fake_run
        cdm.list_clusters_via_sdk = fake_sdk
        items = cdm.list_clusters("cn-north-4")
        self.assertEqual(items, [{"id": "sdk-1"}])
        self.assertEqual(calls["sdk"], 1)

    def test_show_cluster_happy_path(self):
        def fake(argv):
            self.assertIn("--cluster_id=abc", argv)
            self.assertIn("ShowClusterDetail", argv)
            return json.dumps(DETAIL_PAYLOAD), "", 0

        cdm.run_hcloud = fake
        record = cdm.show_cluster("cn-north-4", "abc")
        self.assertEqual(record["name"], "cdm-c018")

    def test_show_cluster_sdk_fallback(self):
        calls = {"sdk": 0}

        def fake_run(argv):
            raise cdm.ConfigError("hcloud missing")

        def fake_sdk(region, cluster_id):
            calls["sdk"] += 1
            self.assertEqual(cluster_id, "abc")
            return {"id": "abc"}

        cdm.run_hcloud = fake_run
        cdm.show_cluster_via_sdk = fake_sdk
        record = cdm.show_cluster("cn-north-4", "abc")
        self.assertEqual(record["id"], "abc")
        self.assertEqual(calls["sdk"], 1)


class RenderTests(unittest.TestCase):
    def test_table_has_key_columns(self):
        text = cdm.render_table([CLUSTER_OK])
        for needle in ("id", "cdm-c018", "200", "2.9.1", "cdm-c018-1(200)"):
            self.assertIn(needle, text)

    def test_markdown_headers_and_empty(self):
        text = cdm.render_markdown([CLUSTER_OK], summary=True,
                                   region="cn-north-4")
        self.assertIn("集群 ID", text)
        self.assertIn("cdm-c018", text)
        self.assertIn("**汇总**：共 1 个", text)
        empty = cdm.render_markdown([])
        self.assertIn("集群 ID", empty)

    def test_markdown_instance_count_cells(self):
        """The 节点数 column must carry the real count (1 / 0), not the dash."""
        text = cdm.render_markdown([CLUSTER_OK, CLUSTER_FAIL])
        lines = [ln for ln in text.splitlines() if ln.startswith("|")]
        headers = [c.strip() for c in lines[0].strip("|").split("|")]
        node_index = headers.index("节点数")
        cells = [[c.strip() for c in ln.strip("|").split("|")]
                 for ln in lines[2:]]
        self.assertEqual([row[node_index] for row in cells], ["1", "0"])
        self.assertEqual([row[headers.index("名称")] for row in cells],
                         ["cdm-c018", "cdm-fail"])

    def test_csv_union_columns(self):
        text = cdm.render_csv([CLUSTER_OK, CLUSTER_FAIL])
        header = text.splitlines()[0]
        for col in ("id", "name", "status", "version", "instance_count"):
            self.assertIn(col, header)
        self.assertIn("cdm-fail", text)

    def test_json_roundtrip(self):
        text = cdm.render_json([CLUSTER_OK])
        self.assertEqual(json.loads(text)[0]["id"],
                         "bae65496-643e-47ca-84af-948672de7eeb")

    def test_detail_table_and_markdown(self):
        table = cdm.render_table([DETAIL_PAYLOAD], detail=True)
        self.assertIn("字段", table)
        self.assertIn("vpc-abc", table)
        md = cdm.render_markdown(None, detail_record=DETAIL_PAYLOAD)
        self.assertIn("| 字段 | 值 |", md)
        self.assertIn("vpc_id", md)

    def test_csv_detail_rejected(self):
        with self.assertRaises(cdm.ApiError):
            cdm.render_csv([DETAIL_PAYLOAD], detail=True)

    def test_csv_detail_rejected_through_render_dispatch(self):
        """--cluster-id --format csv must be rejected on the real dispatch path."""
        with self.assertRaises(cdm.ApiError):
            cdm._render([DETAIL_PAYLOAD], "csv", detail_record=DETAIL_PAYLOAD)

    def test_flat_views_drop_raw_datastore(self):
        """Raw nested datastore is dropped from table/CSV/detail (version kept)."""
        table = cdm.render_table([CLUSTER_OK])
        self.assertNotIn("{", table)
        self.assertIn("2.9.1", table)
        self.assertIn("datastore_type", table)
        csv_columns = cdm.render_csv([CLUSTER_OK]).splitlines()[0].split(",")
        self.assertNotIn("datastore", csv_columns)
        self.assertIn("datastore_type", csv_columns)
        self.assertNotIn("{", cdm.render_csv([CLUSTER_OK]))
        detail = cdm.render_table([DETAIL_PAYLOAD], detail=True)
        self.assertNotIn("datastore ", detail)
        self.assertIn("version", detail)
        detail_md = cdm.render_markdown(None, detail_record=DETAIL_PAYLOAD)
        self.assertNotIn("| datastore |", detail_md)
        payload = json.loads(cdm.render_json([CLUSTER_OK]))
        self.assertEqual(payload[0]["datastore"]["version"], "2.9.1")


class ExportTests(unittest.TestCase):
    def test_atomic_export_and_dir_creation(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = os.path.join(tmp, "nested", "out.json")
            written = cdm.export_report(cdm.render_json([CLUSTER_OK]), target)
            self.assertTrue(os.path.isfile(written))
            self.assertEqual(json.load(open(written))[0]["name"], "cdm-c018")

    def test_empty_export_is_header_only(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = os.path.join(tmp, "empty.csv")
            cdm.export_report(cdm.render_csv([]), target)
            self.assertTrue(os.path.isfile(target))
            self.assertIn("(empty)", open(target).read())


class SdkFallbackTests(unittest.TestCase):
    def setUp(self):
        self._saved_env = {k: os.environ.get(k)
                           for k in (cdm._AK_ENV_NAMES + cdm._SK_ENV_NAMES
                                     + cdm._PROJECT_ID_ENV_NAMES)}

    def tearDown(self):
        for k, v in self._saved_env.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v

    def test_sdk_missing_credentials_raises_config_error(self):
        for name in (cdm._AK_ENV_NAMES + cdm._SK_ENV_NAMES):
            os.environ.pop(name, None)
        with self.assertRaises(cdm.ConfigError):
            cdm._sdk_credentials()

    def test_sdk_credentials_from_whitelisted_env(self):
        os.environ["HUAWEICLOUD_SDK_AK"] = "test-ak"
        os.environ["HUAWEICLOUD_SDK_SK"] = "test-sk"
        try:
            from huaweicloudsdkcore.auth.credentials import BasicCredentials  # noqa: F401
        except ImportError:
            self.skipTest("huaweicloudsdkcore not installed in this env")
        credentials = cdm._sdk_credentials()
        self.assertEqual(credentials.ak, "test-ak")
        self.assertEqual(credentials.sk, "test-sk")

    def test_sdk_client_missing_package_raises_config_error(self):
        saved = sys.modules.pop("huaweicloudsdkcdm", None)
        sys.modules["huaweicloudsdkcdm"] = None  # force ImportError
        try:
            os.environ["HUAWEICLOUD_SDK_AK"] = "test-ak"
            os.environ["HUAWEICLOUD_SDK_SK"] = "test-sk"
            with self.assertRaises(cdm.ConfigError):
                cdm._sdk_client("cn-north-4")
        finally:
            if saved is None:
                sys.modules.pop("huaweicloudsdkcdm", None)
            else:
                sys.modules["huaweicloudsdkcdm"] = saved


class FakeHcloudBinTests(unittest.TestCase):
    """End-to-end through the real subprocess path with a fake hcloud binary."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.bin_path = os.path.join(self.tmp.name, "hcloud-fake")
        self.argv_file = os.path.join(self.tmp.name, "argv.json")
        with open(self.bin_path, "w", encoding="utf-8") as handle:
            handle.write(
                "#!/bin/sh\n"
                ": > %s\n"
                'for a in "$@"; do printf \'%%s\\n\' "$a" >> %s; done\n'
                "cat %s/clusters.json\n" % (self.argv_file, self.argv_file,
                                            self.tmp.name)
            )
        os.chmod(self.bin_path, stat.S_IRWXU)
        with open(os.path.join(self.tmp.name, "clusters.json"), "w",
                  encoding="utf-8") as handle:
            json.dump(CLUSTERS_PAYLOAD, handle)
        self._saved_bin = os.environ.get("CDM_LIST_HCLOUD_BIN")
        os.environ["CDM_LIST_HCLOUD_BIN"] = self.bin_path

    def tearDown(self):
        if self._saved_bin is None:
            os.environ.pop("CDM_LIST_HCLOUD_BIN", None)
        else:
            os.environ["CDM_LIST_HCLOUD_BIN"] = self._saved_bin
        self.tmp.cleanup()

    def test_table_output_via_subprocess(self):
        out = io.StringIO()
        with redirect_stdout(out):
            rc = cdm.main(["--region", "cn-north-4", "--format", "table"])
        self.assertEqual(rc, 0)
        self.assertIn("cdm-c018", out.getvalue())
        with open(self.argv_file, encoding="utf-8") as handle:
            argv = [line.rstrip("\n") for line in handle if line.strip()]
        self.assertEqual(argv, ["CDM", "ListClusters",
                                "--cli-region=cn-north-4"])

    def test_json_output_via_subprocess(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = os.path.join(tmp, "out.json")
            out = io.StringIO()
            with redirect_stdout(out):
                rc = cdm.main(["--format", "json", "--output", target])
            self.assertEqual(rc, 0)
            self.assertIn("已导出", out.getvalue())
            with open(target, encoding="utf-8") as handle:
                payload = json.load(handle)
            self.assertEqual(len(payload), 2)


class MainOutputTests(unittest.TestCase):
    def setUp(self):
        self._orig_run = cdm.run_hcloud

    def tearDown(self):
        cdm.run_hcloud = self._orig_run

    def test_table_empty_message(self):
        cdm.run_hcloud = lambda argv: (json.dumps({"clusters": []}), "", 0)
        out = io.StringIO()
        with redirect_stdout(out):
            rc = cdm.main(["--format", "table"])
        self.assertEqual(rc, 0)
        self.assertIn("无 CDM 集群", out.getvalue())

    def test_table_filtered_empty_message(self):
        cdm.run_hcloud = lambda argv: (json.dumps(CLUSTERS_PAYLOAD), "", 0)
        out = io.StringIO()
        with redirect_stdout(out):
            rc = cdm.main(["--format", "table", "--name", "no-such"])
        self.assertEqual(rc, 0)
        self.assertIn("无 CDM 集群", out.getvalue())
        self.assertIn("name=no-such", out.getvalue())

    def test_table_list_message(self):
        cdm.run_hcloud = lambda argv: (json.dumps(CLUSTERS_PAYLOAD), "", 0)
        out = io.StringIO()
        with redirect_stdout(out):
            rc = cdm.main(["--format", "table"])
        self.assertEqual(rc, 0)
        self.assertIn("共 2 个", out.getvalue())

    def test_detail_view_main(self):
        cdm.run_hcloud = lambda argv: (json.dumps(DETAIL_PAYLOAD), "", 0)
        out = io.StringIO()
        with redirect_stdout(out):
            rc = cdm.main(["--format", "table", "--cluster-id", "abc"])
        self.assertEqual(rc, 0)
        self.assertIn("集群详情", out.getvalue())
        self.assertIn("vpc-abc", out.getvalue())

    def test_detail_with_wrong_operation_rejected(self):
        err = io.StringIO()
        with redirect_stderr(err):
            rc = cdm.main(["--cluster-id", "abc", "--operation", "ListClusters"])
        self.assertEqual(rc, 1)
        self.assertIn("ShowClusterDetail", err.getvalue())

    def test_detail_view_csv_rejected_main(self):
        cdm.run_hcloud = lambda argv: (json.dumps(DETAIL_PAYLOAD), "", 0)
        err = io.StringIO()
        with redirect_stderr(err):
            rc = cdm.main(["--cluster-id", "abc", "--format", "csv"])
        self.assertEqual(rc, 1)
        self.assertIn("csv", err.getvalue())

    def test_markdown_export_has_real_instance_count(self):
        cdm.run_hcloud = lambda argv: (json.dumps(CLUSTERS_PAYLOAD), "", 0)
        with tempfile.TemporaryDirectory() as tmp:
            target = os.path.join(tmp, "out.md")
            with redirect_stdout(io.StringIO()):
                rc = cdm.main(["--format", "markdown", "--output", target])
            self.assertEqual(rc, 0)
            with open(target, encoding="utf-8") as handle:
                body = handle.read()
        lines = [ln for ln in body.splitlines() if ln.startswith("|")]
        headers = [c.strip() for c in lines[0].strip("|").split("|")]
        node_index = headers.index("节点数")
        cells = [[c.strip() for c in ln.strip("|").split("|")]
                 for ln in lines[2:]]
        self.assertEqual([row[node_index] for row in cells], ["1", "0"])

    def test_export_message(self):
        cdm.run_hcloud = lambda argv: (json.dumps(CLUSTERS_PAYLOAD), "", 0)
        with tempfile.TemporaryDirectory() as tmp:
            target = os.path.join(tmp, "out.md")
            out = io.StringIO()
            with redirect_stdout(out):
                rc = cdm.main(["--format", "markdown", "--summary",
                               "--output", target])
            self.assertEqual(rc, 0)
            self.assertIn("已导出", out.getvalue())
            self.assertIn("共 2 条", out.getvalue())
            body = open(target, encoding="utf-8").read()
            self.assertIn("集群 ID", body)
            self.assertIn("**汇总**：共 2 个", body)

    def test_help_exit_zero(self):
        out = io.StringIO()
        with redirect_stdout(out):
            with self.assertRaises(SystemExit) as ctx:
                cdm.parse_args(["--help"])
        self.assertEqual(ctx.exception.code, 0)
        self.assertIn("usage", out.getvalue())
        self.assertIn("cluster-id", out.getvalue())

    def test_max_calls_validation(self):
        err = io.StringIO()
        with redirect_stderr(err):
            rc = cdm.main(["--max-calls", "0"])
        self.assertEqual(rc, 1)
        self.assertIn("--max-calls", err.getvalue())


if __name__ == "__main__":
    unittest.main()
