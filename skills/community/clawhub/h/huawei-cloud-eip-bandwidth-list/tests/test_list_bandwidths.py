import glob
import io
import json
import os
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts"))

from list_bandwidths import (  # noqa: E402
    ALLOWED_OPERATIONS,
    LIST_OPERATION,
    SHOW_OPERATION,
    ApiError,
    AuthError,
    BandwidthListError,
    ConfigError,
    ExportError,
    GuardError,
    active_filter_descriptions,
    build_list_command,
    build_show_command,
    classify_api_error_payload,
    classify_hcloud_failure,
    default_output_path,
    empty_message,
    export_markdown,
    export_markdown_detail,
    extract_bandwidth,
    extract_bandwidths,
    extract_json,
    guard_operation,
    guard_text_from_argv,
    guard_write_intent,
    list_bandwidths,
    list_bandwidths_via_sdk,
    main,
    normalize_bandwidth,
    render_detail,
    render_markdown,
    render_markdown_detail,
    render_table,
    show_bandwidth,
    show_bandwidth_via_sdk,
)

BANDWIDTH_1 = {
    "id": "bw-0001",
    "name": "bw-demo-01",
    "size": 10,
    "share_type": "PER",
    "publicip_info": [
        {
            "publicip_id": "eip-0001",
            "publicip_address": "1.2.3.4",
            "ip_version": 4,
            "publicip_type": "5_bgp",
        }
    ],
    "tenant_id": "tenant-1",
    "bandwidth_type": "bgp",
    "charge_mode": "traffic",
    "billing_info": "",
    "enterprise_project_id": "0",
    "status": "NORMAL",
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z",
    "enable_bandwidth_rules": False,
    "rule_quota": 0,
    "bandwidth_rules": [],
}
BANDWIDTH_2 = {
    "id": "bw-0002",
    "name": "bw-demo-02",
    "size": 300,
    "share_type": "WHOLE",
    "publicip_info": [
        {"publicip_id": "eip-0002", "publicip_address": "5.6.7.8",
         "ip_version": 4, "publicip_type": "5_bgp"},
        {"publicip_id": "eip-0003", "publicip_address": "5.6.7.9",
         "ip_version": 4, "publicip_type": "5_bgp"},
    ],
    "charge_mode": "bandwidth",
    "enterprise_project_id": "0",
    "status": "NORMAL",
    "created_at": "2024-02-01T00:00:00Z",
}


def hcloud_result(stdout="", stderr="", returncode=0):
    return subprocess.CompletedProcess(
        args=["hcloud"], returncode=returncode, stdout=stdout, stderr=stderr
    )


class FakeRunner:
    def __init__(self, results):
        self.results = list(results)
        self.calls = []

    def __call__(self, cmd, **kwargs):
        self.calls.append(cmd)
        if not self.results:
            raise AssertionError("unexpected extra hcloud call: %s" % cmd)
        out = self.results.pop(0)
        if isinstance(out, Exception):
            raise out
        return hcloud_result(*out)


class TestWriteIntentGuard(unittest.TestCase):
    def test_read_intent_passes(self):
        self.assertFalse(guard_write_intent("--share-type WHOLE --limit 10"))
        self.assertFalse(guard_write_intent("show bandwidth details"))
        self.assertFalse(guard_write_intent("list bandwidths"))

    def test_create_blocked(self):
        with self.assertRaises(GuardError):
            guard_write_intent("CreateBandwidth bw-new")

    def test_delete_blocked(self):
        with self.assertRaises(GuardError):
            guard_write_intent("--operation DeleteBandwidth")

    def test_change_charge_mode_blocked(self):
        with self.assertRaises(GuardError):
            guard_write_intent("change charge mode traffic")

    def test_bind_unbind_blocked(self):
        for text in ("bind public ip", "unbind public ip", "associate eip",
                     "disassociate eip", "release bandwidth"):
            with self.assertRaises(GuardError):
                guard_write_intent(text)

    def test_normalized_separators_blocked(self):
        with self.assertRaises(GuardError):
            guard_write_intent("--create-bandwidth")
        with self.assertRaises(GuardError):
            guard_write_intent("update_bandwidth_size")

    def test_operation_guard_rejects_unknown(self):
        with self.assertRaises(GuardError):
            guard_operation("CreateBandwidth")
        for op in ALLOWED_OPERATIONS:
            self.assertTrue(guard_operation(op))


class TestGuardTextFromArgv(unittest.TestCase):
    def test_output_value_stripped(self):
        text = guard_text_from_argv(["-o", "bandwidth-release-report.md"])
        self.assertNotIn("release", text)
        self.assertEqual(text, "")

    def test_output_equals_form_stripped(self):
        self.assertNotIn("delete", guard_text_from_argv(
            ["--output=delete-report.md"]))

    def test_other_values_still_scanned(self):
        self.assertIn("release-me", guard_text_from_argv(
            ["--bandwidth-id", "release-me"]))

    def test_following_flag_not_swallowed(self):
        text = guard_text_from_argv(["-o", "--create-bandwidth"])
        self.assertIn("--create-bandwidth", text)


class TestBuildCommands(unittest.TestCase):
    def test_list_basic(self):
        argv = build_list_command("cn-north-4")
        self.assertEqual(argv[0], "EIP")
        self.assertEqual(argv[1], LIST_OPERATION)
        self.assertIn("--cli-region=cn-north-4", argv)
        self.assertIn("--limit=10", argv)
        self.assertFalse(any(a.startswith("--marker=") for a in argv))
        self.assertFalse(any(a.startswith("--share_type=") for a in argv))

    def test_list_filters_and_marker(self):
        argv = build_list_command("cn-south-1", share_type="WHOLE",
                                  enterprise_project_id="0", limit=50,
                                  marker="bw-9")
        self.assertIn("--cli-region=cn-south-1", argv)
        self.assertIn("--limit=50", argv)
        self.assertIn("--share_type=WHOLE", argv)
        self.assertIn("--enterprise_project_id=0", argv)
        self.assertIn("--marker=bw-9", argv)

    def test_show(self):
        argv = build_show_command("cn-north-4", "bw-1")
        self.assertEqual(argv[0], "EIP")
        self.assertEqual(argv[1], SHOW_OPERATION)
        self.assertIn("--cli-region=cn-north-4", argv)
        self.assertIn("--bandwidth_id=bw-1", argv)


class TestParsingAndFailure(unittest.TestCase):
    def test_extract_list(self):
        self.assertEqual(extract_bandwidths({"bandwidths": [BANDWIDTH_1]}), [BANDWIDTH_1])
        self.assertEqual(extract_bandwidths([BANDWIDTH_1]), [BANDWIDTH_1])
        self.assertEqual(extract_bandwidths({}), [])

    def test_extract_detail(self):
        self.assertEqual(extract_bandwidth({"bandwidth": BANDWIDTH_1}), BANDWIDTH_1)
        self.assertEqual(extract_bandwidth(BANDWIDTH_1), BANDWIDTH_1)
        self.assertEqual(extract_bandwidth({}), {})

    def test_extract_json_noise(self):
        self.assertEqual(extract_json('noise {"bandwidths": []} tail'),
                         {"bandwidths": []})
        with self.assertRaises(ApiError):
            extract_json("not json at all")

    def test_classify_use_error(self):
        err = classify_hcloud_failure("[USE_ERROR]Invalid parameter", "", 0)
        self.assertIsInstance(err, ApiError)
        self.assertIn("参数错误", str(err))

    def test_classify_credentials(self):
        err = classify_hcloud_failure("", "ERROR: cli-ak empty", 1)
        self.assertIsInstance(err, ConfigError)
        self.assertIn("AK/SK", str(err))

    def test_classify_403_list(self):
        err = classify_hcloud_failure("", "403 Forbidden", 1, LIST_OPERATION)
        self.assertIsInstance(err, AuthError)
        self.assertIn("eip:bandwidths:list", str(err))

    def test_classify_403_show(self):
        err = classify_hcloud_failure("", "403 Forbidden", 1, SHOW_OPERATION)
        self.assertIsInstance(err, AuthError)
        self.assertIn("eip:bandwidths:get", str(err))

    def test_classify_not_found_show(self):
        err = classify_hcloud_failure("", "404 not found", 1, SHOW_OPERATION)
        self.assertIsInstance(err, ApiError)
        self.assertIn("不存在", str(err))


VPC_0305_BODY = {
    "code": "VPC.0305",
    "message": json.dumps({
        "NeutronError": {
            "message": "No Eip bandwidth exist with id 00000000-0000-4000-8000-000000000000",
            "type": "NoEipBandWidthExist",
            "detail": "",
        }
    }),
}


class TestApiErrorPayload(unittest.TestCase):
    def test_vpc_0305_show_points_to_list(self):
        err = classify_api_error_payload(VPC_0305_BODY, SHOW_OPERATION)
        self.assertIsInstance(err, ApiError)
        self.assertIn("VPC.0305", str(err))
        self.assertIn("不存在", str(err))
        self.assertIn("ListBandwidths", str(err))
        self.assertIn("--bandwidth-id", str(err))

    def test_success_payload_is_not_an_error(self):
        self.assertIsNone(classify_api_error_payload({"bandwidth": BANDWIDTH_1}))
        self.assertIsNone(classify_api_error_payload({"bandwidths": [BANDWIDTH_1]}))
        self.assertIsNone(classify_api_error_payload([]))
        self.assertIsNone(classify_api_error_payload(None))

    def test_generic_api_error_code(self):
        err = classify_api_error_payload(
            {"code": "EIP.0001", "message": "internal error"}, LIST_OPERATION)
        self.assertIsInstance(err, ApiError)
        self.assertIn("EIP.0001", str(err))

    def test_api_auth_code_maps_to_auth_error(self):
        err = classify_api_error_payload(
            {"code": "APIGW.0301", "message": "Authentication failed"},
            SHOW_OPERATION)
        self.assertIsInstance(err, AuthError)
        self.assertIn("eip:bandwidths:get", str(err))

    def test_show_bandwidth_raises_on_vpc_0305_body(self):
        fake = FakeRunner([(json.dumps(VPC_0305_BODY), "", 0)])
        with mock.patch("list_bandwidths.subprocess.run", fake):
            with self.assertRaises(ApiError) as ctx:
                show_bandwidth("cn-north-4", "00000000-0000-4000-8000-000000000000")
        self.assertIn("VPC.0305", str(ctx.exception))

    def test_list_bandwidths_raises_on_api_error_body(self):
        fake = FakeRunner([(json.dumps(VPC_0305_BODY), "", 0)])
        with mock.patch("list_bandwidths.subprocess.run", fake):
            with self.assertRaises(ApiError):
                list_bandwidths("cn-north-4")

    def test_main_exits_1_and_prints_vpc_0305_hint(self):
        fake = FakeRunner([(json.dumps(VPC_0305_BODY), "", 0)])
        stderr = io.StringIO()
        with mock.patch("list_bandwidths.subprocess.run", fake), \
                mock.patch("sys.stderr", stderr):
            rc = main(["--bandwidth-id", "00000000-0000-4000-8000-000000000000"])
        self.assertEqual(rc, 1)
        self.assertIn("VPC.0305", stderr.getvalue())


class TestPaging(unittest.TestCase):
    def test_marker_paging_by_full_page(self):
        page1 = json.dumps({"bandwidths": [BANDWIDTH_1, BANDWIDTH_2]})
        page2 = json.dumps({"bandwidths": [dict(BANDWIDTH_1, id="bw-0003")]})
        fake = FakeRunner([(page1, "", 0), (page2, "", 0)])
        with mock.patch("list_bandwidths.subprocess.run", fake):
            result = list_bandwidths("cn-north-4", limit=2)
        self.assertEqual([b["id"] for b in result], ["bw-0001", "bw-0002", "bw-0003"])
        self.assertEqual(len(fake.calls), 2)
        self.assertIn("--marker=bw-0002", fake.calls[1])

    def test_stops_when_partial_page(self):
        fake = FakeRunner([(json.dumps({"bandwidths": [BANDWIDTH_1]}), "", 0)])
        with mock.patch("list_bandwidths.subprocess.run", fake):
            result = list_bandwidths("cn-north-4", limit=10)
        self.assertEqual(result, [BANDWIDTH_1])
        self.assertEqual(len(fake.calls), 1)

    def test_stops_on_empty_page(self):
        fake = FakeRunner([
            (json.dumps({"bandwidths": [BANDWIDTH_1]}), "", 0),
            (json.dumps({"bandwidths": []}), "", 0),
        ])
        with mock.patch("list_bandwidths.subprocess.run", fake):
            result = list_bandwidths("cn-north-4", limit=1)
        self.assertEqual(result, [BANDWIDTH_1])
        self.assertEqual(len(fake.calls), 2)

    def test_explicit_next_marker_wins(self):
        page1 = json.dumps({"bandwidths": [BANDWIDTH_1],
                            "page_info": {"next_marker": "tok-2"}})
        page2 = json.dumps({"bandwidths": []})
        fake = FakeRunner([(page1, "", 0), (page2, "", 0)])
        with mock.patch("list_bandwidths.subprocess.run", fake):
            list_bandwidths("cn-north-4", limit=10)
        self.assertIn("--marker=tok-2", fake.calls[1])

    def test_filters_forwarded(self):
        fake = FakeRunner([(json.dumps({"bandwidths": []}), "", 0)])
        with mock.patch("list_bandwidths.subprocess.run", fake):
            list_bandwidths("cn-north-4", share_type="WHOLE",
                            enterprise_project_id="eps-1", limit=10)
        argv = fake.calls[0]
        self.assertIn("--share_type=WHOLE", argv)
        self.assertIn("--enterprise_project_id=eps-1", argv)

    def test_sdk_fallback_when_hcloud_missing(self):
        with mock.patch("list_bandwidths.subprocess.run",
                        FakeRunner([FileNotFoundError()])), \
                mock.patch("list_bandwidths.list_bandwidths_via_sdk",
                           return_value=[BANDWIDTH_1, BANDWIDTH_2]) as sdk_mock:
            result = list_bandwidths("cn-north-4", share_type="PER",
                                     enterprise_project_id="0", project_id="proj-1")
        self.assertEqual(result, [BANDWIDTH_1, BANDWIDTH_2])
        self.assertEqual(sdk_mock.call_args.kwargs.get("share_type"), "PER")
        self.assertEqual(sdk_mock.call_args.kwargs.get("project_id"), "proj-1")

    def test_sdk_fallback_unavailable(self):
        with mock.patch("list_bandwidths.subprocess.run",
                        FakeRunner([FileNotFoundError()])), \
                mock.patch("list_bandwidths.list_bandwidths_via_sdk",
                           side_effect=ConfigError("未安装")):
            with self.assertRaises(ConfigError):
                list_bandwidths("cn-north-4")


class TestShow(unittest.TestCase):
    def test_show_cli(self):
        fake = FakeRunner([(json.dumps({"bandwidth": BANDWIDTH_1}), "", 0)])
        with mock.patch("list_bandwidths.subprocess.run", fake):
            result = show_bandwidth("cn-north-4", "bw-0001")
        self.assertEqual(result, BANDWIDTH_1)
        self.assertIn("--bandwidth_id=bw-0001", fake.calls[0])

    def test_show_sdk_fallback(self):
        with mock.patch("list_bandwidths.subprocess.run",
                        FakeRunner([FileNotFoundError()])), \
                mock.patch("list_bandwidths.show_bandwidth_via_sdk",
                           return_value=BANDWIDTH_1) as sdk_mock:
            result = show_bandwidth("cn-north-4", "bw-0001", project_id="p-1")
        self.assertEqual(result, BANDWIDTH_1)
        self.assertEqual(sdk_mock.call_args.kwargs.get("project_id"), "p-1")


class TestSdkFallbackUnit(unittest.TestCase):
    def test_sdk_list_pagination_and_request(self):
        import types
        eip_pkg = types.ModuleType("huaweicloudsdkeip")
        eip_v3 = types.ModuleType("huaweicloudsdkeip.v3")
        eip_v3.ListBandwidthsRequest = mock.Mock(
            side_effect=lambda **kwargs: mock.Mock(**kwargs))
        eip_pkg.v3 = eip_v3
        batches = [
            [BANDWIDTH_1, BANDWIDTH_2],
            [dict(BANDWIDTH_1, id="bw-0003")],
        ]
        client = mock.Mock()
        responses = []
        for batch in batches:
            response = mock.Mock()
            response.bandwidths = [mock.Mock(**{
                "to_dict.return_value": item}) for item in batch]
            response.page_info = None
            responses.append(response)
        client.list_bandwidths.side_effect = responses
        with mock.patch.dict(sys.modules, {"huaweicloudsdkeip": eip_pkg,
                                           "huaweicloudsdkeip.v3": eip_v3}), \
                mock.patch("list_bandwidths._build_sdk_client", return_value=client):
            result = list_bandwidths_via_sdk(
                "cn-north-4", share_type="WHOLE", enterprise_project_id="0",
                limit=2)
        self.assertEqual([b["id"] for b in result],
                         ["bw-0001", "bw-0002", "bw-0003"])
        first_req = client.list_bandwidths.call_args_list[0][0][0]
        self.assertEqual(getattr(first_req, "share_type", None), "WHOLE")
        self.assertEqual(getattr(first_req, "enterprise_project_id", None), "0")
        second_req = client.list_bandwidths.call_args_list[1][0][0]
        self.assertEqual(getattr(second_req, "marker", None), "bw-0002")

    def test_sdk_list_missing_dependency_raises_config(self):
        with mock.patch.dict(sys.modules, {"huaweicloudsdkeip": None,
                                           "huaweicloudsdkeip.v3": None}):
            with self.assertRaises(ConfigError):
                list_bandwidths_via_sdk("cn-north-4")

    def test_sdk_show_missing_dependency_raises_config(self):
        with mock.patch.dict(sys.modules, {"huaweicloudsdkeip": None,
                                           "huaweicloudsdkeip.v3": None}):
            with self.assertRaises(ConfigError):
                show_bandwidth_via_sdk("cn-north-4", "bw-1")

    def test_sdk_show_uses_request(self):
        import types
        eip_pkg = types.ModuleType("huaweicloudsdkeip")
        eip_v3 = types.ModuleType("huaweicloudsdkeip.v3")
        eip_v3.ShowBandwidthRequest = mock.Mock(
            side_effect=lambda **kwargs: mock.Mock(**kwargs))
        eip_pkg.v3 = eip_v3
        client = mock.Mock()
        bandwidth = mock.Mock()
        bandwidth.to_dict.return_value = BANDWIDTH_1
        client.show_bandwidth.return_value = mock.Mock(bandwidth=bandwidth)
        with mock.patch.dict(sys.modules, {"huaweicloudsdkeip": eip_pkg,
                                           "huaweicloudsdkeip.v3": eip_v3}), \
                mock.patch("list_bandwidths._build_sdk_client", return_value=client):
            result = show_bandwidth_via_sdk("cn-north-4", "bw-0001")
        self.assertEqual(result, BANDWIDTH_1)
        request = client.show_bandwidth.call_args[0][0]
        self.assertEqual(getattr(request, "bandwidth_id", None), "bw-0001")


class TestRender(unittest.TestCase):
    def test_normalize_counts_publicips(self):
        flat = normalize_bandwidth(BANDWIDTH_2)
        self.assertEqual(flat["publicip_info_count"], 2)

    def test_table_columns(self):
        table = render_table([BANDWIDTH_1, BANDWIDTH_2])
        for fragment in ("带宽名称", "带宽 ID", "大小(Mbit/s)", "共享类型",
                         "计费方式", "关联公网 IP 数", "状态", "企业项目 ID",
                         "创建时间", "bw-demo-01", "bw-0002", "WHOLE", "300"):
            self.assertIn(fragment, table)

    def test_detail_text(self):
        detail = render_detail(BANDWIDTH_2, region="cn-north-4")
        self.assertIn("EIP 带宽明细", detail)
        self.assertIn("bw-0002", detail)
        self.assertIn("5.6.7.8", detail)
        self.assertIn("5.6.7.9", detail)
        self.assertIn("规则配额", detail)

    def test_detail_text_empty_publicips(self):
        detail = render_detail({"id": "bw-empty", "name": "x"}, region="cn-north-4")
        self.assertIn("无数据", detail)

    def test_markdown_list_full_header(self):
        md = render_markdown([BANDWIDTH_1, BANDWIDTH_2], region="cn-north-4",
                             generated_at="2026-11-12T00:00:00Z")
        self.assertIn("# 华为云 EIP 带宽列表", md)
        self.assertIn("查询区域：cn-north-4", md)
        self.assertIn("记录数：2", md)
        self.assertIn("| 带宽名称 | 带宽 ID | 大小(Mbit/s) | 共享类型 | 计费方式 | "
                      "关联公网 IP 数 | 状态 | 企业项目 ID | 创建时间 |", md)
        self.assertIn("bw-demo-01", md)
        self.assertIn("WHOLE", md)

    def test_markdown_missing_fields_dash(self):
        md = render_markdown([{"id": "bw-9"}], region="cn-north-4")
        row = [line for line in md.splitlines() if "| bw-9 |" in line][0]
        cells = [cell.strip() for cell in row.strip("|").split("|")]
        self.assertEqual(cells.count("-"), 7)

    def test_markdown_empty_has_header_and_no_data(self):
        md = render_markdown([], region="cn-north-4",
                             generated_at="2026-11-12T00:00:00Z")
        self.assertIn("| 带宽名称 |", md)
        self.assertIn("记录数：0", md)
        self.assertIn("无数据", md)

    def test_markdown_detail(self):
        md = render_markdown_detail(BANDWIDTH_2, region="cn-north-4",
                                    generated_at="2026-11-12T00:00:00Z")
        self.assertIn("# 华为云 EIP 带宽明细", md)
        self.assertIn("带宽 ID：bw-0002", md)
        self.assertIn("## 关联公网 IP（2）", md)
        self.assertIn("5.6.7.8", md)
        self.assertIn("## 带宽规则", md)


class TestEmptyMessages(unittest.TestCase):
    def test_overall_empty(self):
        self.assertIn("无带宽（Bandwidth）数据",
                      empty_message("cn-north-4"))

    def test_share_type_whole_empty(self):
        message = empty_message("cn-north-4", share_type="WHOLE")
        self.assertIn("share_type=WHOLE", message)
        self.assertIn("共享带宽", message)

    def test_share_type_per_empty(self):
        self.assertIn("share_type=PER", empty_message("cn-north-4", share_type="PER"))

    def test_enterprise_project_empty(self):
        self.assertIn("企业项目 eps-1",
                      empty_message("cn-north-4", enterprise_project_id="eps-1"))

    def test_filter_descriptions(self):
        self.assertEqual(active_filter_descriptions("WHOLE", "0"),
                         ["share_type=WHOLE", "enterprise_project_id=0"])


class TestExport(unittest.TestCase):
    def test_export_creates_parents_and_is_atomic(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = os.path.join(tmp, "nested", "reports", "bw.md")
            written = export_markdown([BANDWIDTH_1], target, region="cn-north-4")
            self.assertEqual(written, os.path.abspath(target))
            self.assertTrue(os.path.isfile(written))
            self.assertEqual(os.listdir(os.path.dirname(written)), ["bw.md"])

    def test_export_detail(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = os.path.join(tmp, "bw-detail.md")
            export_markdown_detail(BANDWIDTH_2, target, region="cn-north-4")
            with open(target, encoding="utf-8") as handle:
                content = handle.read()
            self.assertIn("华为云 EIP 带宽明细", content)
            self.assertIn("5.6.7.8", content)

    def test_export_unwritable_parent(self):
        with tempfile.TemporaryDirectory() as tmp:
            blocker = os.path.join(tmp, "not-a-dir")
            with open(blocker, "w", encoding="utf-8") as handle:
                handle.write("x")
            with self.assertRaises(ExportError):
                export_markdown([], os.path.join(blocker, "bw.md"))

    def test_default_output_path_shape(self):
        name = default_output_path("cn-north-4")
        self.assertTrue(name.startswith("eip_bandwidth_list_cn-north-4_"))
        self.assertTrue(name.endswith(".md"))


class TestMain(unittest.TestCase):
    def _run(self, argv, results):
        fake = FakeRunner(results)
        with mock.patch("list_bandwidths.subprocess.run", fake), \
                mock.patch("sys.stdout") as stdout, \
                mock.patch("sys.stderr") as stderr:
            rc = main(argv)
        out = "".join(c[0][0] for c in stdout.write.call_args_list)
        err = "".join(c[0][0] for c in stderr.write.call_args_list)
        return rc, out, err

    def test_table_output(self):
        rc, out, err = self._run(
            ["--region", "cn-north-4"],
            [(json.dumps({"bandwidths": [BANDWIDTH_1, BANDWIDTH_2]}), "", 0)])
        self.assertEqual(rc, 0)
        self.assertIn("EIP 带宽（Bandwidth）列表", out)
        self.assertIn("bw-demo-01", out)
        self.assertEqual(err, "")

    def test_json_list_output(self):
        rc, out, err = self._run(
            ["--json"], [(json.dumps({"bandwidths": [BANDWIDTH_1]}), "", 0)])
        self.assertEqual(rc, 0)
        self.assertEqual(json.loads(out), [BANDWIDTH_1])

    def test_json_detail_output(self):
        rc, out, err = self._run(
            ["--bandwidth-id", "bw-0001", "--json"],
            [(json.dumps({"bandwidth": BANDWIDTH_1}), "", 0)])
        self.assertEqual(rc, 0)
        self.assertEqual(json.loads(out), BANDWIDTH_1)

    def test_detail_table_output(self):
        rc, out, err = self._run(
            ["--bandwidth-id", "bw-0002"],
            [(json.dumps({"bandwidth": BANDWIDTH_2}), "", 0)])
        self.assertEqual(rc, 0)
        self.assertIn("EIP 带宽明细", out)
        self.assertIn("5.6.7.8", out)

    def test_empty_message_overall(self):
        rc, out, err = self._run(
            ["--region", "cn-south-1"],
            [(json.dumps({"bandwidths": []}), "", 0)])
        self.assertEqual(rc, 0)
        self.assertIn("无带宽（Bandwidth）数据", out)
        self.assertIn("cn-south-1", out)

    def test_empty_message_share_type_whole(self):
        rc, out, err = self._run(
            ["--share-type", "WHOLE"],
            [(json.dumps({"bandwidths": []}), "", 0)])
        self.assertEqual(rc, 0)
        self.assertIn("share_type=WHOLE", out)
        self.assertIn("共享带宽", out)

    def test_share_type_forwarded(self):
        fake = FakeRunner([(json.dumps({"bandwidths": [BANDWIDTH_2]}), "", 0)])
        with mock.patch("list_bandwidths.subprocess.run", fake), \
                mock.patch("sys.stdout"), mock.patch("sys.stderr"):
            rc = main(["--share-type", "WHOLE"])
        self.assertEqual(rc, 0)
        self.assertIn("--share_type=WHOLE", fake.calls[0])

    def test_auth_error_mentions_iam(self):
        rc, out, err = self._run([], [("", "403 Forbidden", 1)])
        self.assertEqual(rc, 1)
        self.assertIn("[错误]", err)
        self.assertIn("IAM", err)

    def test_missing_ak_sk(self):
        rc, out, err = self._run([], [("", "ERROR: cli-ak empty", 1)])
        self.assertEqual(rc, 1)
        self.assertIn("AK/SK", err)

    def test_hcloud_not_installed(self):
        with mock.patch("list_bandwidths.list_bandwidths_via_sdk",
                        side_effect=ConfigError("huaweicloudsdkeip 未安装")):
            rc, out, err = self._run([], [FileNotFoundError()])
        self.assertEqual(rc, 1)
        self.assertIn("未安装", err)

    def test_hcloud_missing_falls_back_to_sdk(self):
        with mock.patch("list_bandwidths.list_bandwidths_via_sdk",
                        return_value=[BANDWIDTH_1]):
            rc, out, err = self._run([], [FileNotFoundError()])
        self.assertEqual(rc, 0)
        self.assertIn("bw-0001", out)

    def test_write_intent_argv_blocked(self):
        rc, out, err = self._run(["--operation", "CreateBandwidth"], [])
        self.assertEqual(rc, 1)
        self.assertIn("写操作意图", err)

    def test_write_keyword_value_blocked(self):
        rc, out, err = self._run(["--bandwidth-id", "release-me"], [])
        self.assertEqual(rc, 1)
        self.assertIn("守卫拦截", err)

    def test_markdown_output_creates_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = os.path.join(tmp, "bw.md")
            rc, out, err = self._run(
                ["--format", "md", "-o", target],
                [(json.dumps({"bandwidths": [BANDWIDTH_1]}), "", 0)])
            self.assertEqual(rc, 0)
            self.assertTrue(os.path.isfile(target))
            self.assertIn(os.path.abspath(target), out)
            with open(target, encoding="utf-8") as handle:
                self.assertIn("bw-demo-01", handle.read())

    def test_markdown_detail_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = os.path.join(tmp, "bw-detail.md")
            rc, out, err = self._run(
                ["--bandwidth-id", "bw-0002", "--format", "md", "-o", target],
                [(json.dumps({"bandwidth": BANDWIDTH_2}), "", 0)])
            self.assertEqual(rc, 0)
            with open(target, encoding="utf-8") as handle:
                content = handle.read()
            self.assertIn("带宽明细", content)
            self.assertIn("5.6.7.8", content)

    def test_markdown_default_filename(self):
        with tempfile.TemporaryDirectory() as tmp:
            cwd = os.getcwd()
            os.chdir(tmp)
            try:
                rc, out, err = self._run(
                    ["--format", "md", "--region", "cn-north-4"],
                    [(json.dumps({"bandwidths": [BANDWIDTH_1]}), "", 0)])
            finally:
                os.chdir(cwd)
            self.assertEqual(rc, 0)
            files = glob.glob(os.path.join(tmp, "eip_bandwidth_list_cn-north-4_*.md"))
            self.assertEqual(len(files), 1)

    def test_markdown_empty_still_writes_no_data(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = os.path.join(tmp, "empty.md")
            rc, out, err = self._run(
                ["--share-type", "WHOLE", "--format", "md", "-o", target],
                [(json.dumps({"bandwidths": []}), "", 0)])
            self.assertEqual(rc, 0)
            self.assertIn("无数据", out)
            with open(target, encoding="utf-8") as handle:
                content = handle.read()
            self.assertIn("| 带宽名称 |", content)
            self.assertIn("无数据", content)

    def test_output_path_with_write_word_not_blocked(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = os.path.join(tmp, "bandwidth-release-report.md")
            rc, out, err = self._run(
                ["-o", target],
                [(json.dumps({"bandwidths": [BANDWIDTH_1]}), "", 0)])
            self.assertEqual(rc, 0)
            self.assertTrue(os.path.isfile(target))


class TestErrorHierarchy(unittest.TestCase):
    def test_subclasses(self):
        for exc in (GuardError, ConfigError, AuthError, ApiError, ExportError):
            self.assertTrue(issubclass(exc, BandwidthListError))


if __name__ == "__main__":
    unittest.main()