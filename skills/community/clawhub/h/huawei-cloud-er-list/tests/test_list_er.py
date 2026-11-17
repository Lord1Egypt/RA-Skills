import json
import os
import subprocess
import sys
import unittest
from types import SimpleNamespace
from unittest import mock

sys.path.insert(0, os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts"))

from list_er import (  # noqa: E402
    ApiError,
    AuthError,
    ConfigError,
    ErListError,
    GuardError,
    NotFoundError,
    apply_local_filters,
    build_attachment_command,
    build_detail_command,
    build_er_command,
    build_route_table_command,
    check_payload_error,
    classify_error_text,
    classify_hcloud_failure,
    extract_items,
    extract_json,
    guard_operation,
    guard_text_from_argv,
    guard_write_intent,
    list_attachments,
    list_attachments_via_sdk,
    list_ers,
    list_ers_via_sdk,
    list_route_tables,
    list_route_tables_via_sdk,
    main,
    next_marker,
    render_compact_sections,
    render_detail,
    render_fixed_table,
    render_sections,
    show_er,
    show_er_via_sdk,
    split_by_state,
    ATTACHMENT_TABLE_COLUMNS,
    ER_TABLE_COLUMNS,
    ER_ITEM_KEYS,
    ATTACHMENT_ITEM_KEYS,
    ROUTE_TABLE_ITEM_KEYS,
    ROUTE_TABLE_COLUMNS,
)

ER_AVAILABLE = {
    "id": "er-0001",
    "name": "er-demo-01",
    "state": "available",
    "asn": 64512,
    "enterprise_project_id": "0",
    "availability_zone_ids": ["cn-north-4a", "cn-north-4b"],
    "description": "primary router",
    "default_association_route_table_id": "rt-1",
    "default_propagation_route_table_id": "rt-2",
    "created_at": "2024-01-01T00:00:00",
    "updated_at": "2024-01-02T00:00:00",
}
ER_FAILED = {
    "id": "er-0002",
    "name": "er-demo-02",
    "state": "failed",
    "asn": 64513,
    "enterprise_project_id": "0",
}
ATTACH_AVAILABLE = {
    "id": "att-0001",
    "name": "vpc-att-01",
    "state": "available",
    "vpc_id": "vpc-0001",
    "virsubnet_id": "subnet-0001",
    "created_at": "2024-01-01T00:00:00",
}
ATTACH_FAILED = {
    "id": "att-0002",
    "name": "vpc-att-02",
    "state": "failed",
    "vpc_id": "vpc-0002",
    "virsubnet_id": "subnet-0002",
}
ROUTE_TABLE = {
    "id": "rt-0001",
    "name": "default-association",
    "state": "available",
    "is_default_association": True,
    "is_default_propagation": False,
    "created_at": "2024-01-01T00:00:00",
}


def hcloud_result(stdout="", stderr="", returncode=0):
    return subprocess.CompletedProcess(
        args=["hcloud"], returncode=returncode, stdout=stdout, stderr=stderr)


class FakeRunner:
    """subprocess.run fake returning canned hcloud outputs per call."""

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
        self.assertFalse(guard_write_intent("list enterprise routers"))
        self.assertFalse(guard_write_intent("show er detail"))
        self.assertFalse(guard_write_intent("ListVpcAttachments"))

    def test_create_blocked(self):
        with self.assertRaises(GuardError):
            guard_write_intent("CreateEnterpriseRouter")

    def test_delete_blocked(self):
        with self.assertRaises(GuardError):
            guard_write_intent("--operation DeleteEnterpriseRouter")

    def test_update_blocked(self):
        with self.assertRaises(GuardError):
            guard_write_intent("UpdateEnterpriseRouter")

    def test_associate_disassociate_blocked(self):
        with self.assertRaises(GuardError):
            guard_write_intent("AssociateRouteTable")
        with self.assertRaises(GuardError):
            guard_write_intent("DisassociateRouteTable")

    def test_enable_disable_blocked(self):
        with self.assertRaises(GuardError):
            guard_write_intent("EnablePropagation")
        with self.assertRaises(GuardError):
            guard_write_intent("DisableFlowLog")

    def test_normalized_separators_blocked(self):
        with self.assertRaises(GuardError):
            guard_write_intent("--create-er")
        with self.assertRaises(GuardError):
            guard_write_intent("delete_enterprise_router")

    def test_resource_value_not_blocked(self):
        self.assertFalse(guard_write_intent(
            guard_text_from_argv(["--resource", "attachment"])))
        self.assertFalse(guard_write_intent(
            guard_text_from_argv(["--resource=route-table"])))

    def test_disallowed_resource_still_blocked(self):
        with self.assertRaises(GuardError):
            guard_write_intent(
                guard_text_from_argv(["--resource", "delete"]))

    def test_local_filter_value_not_blocked(self):
        self.assertFalse(guard_write_intent(
            guard_text_from_argv(["--fuzzy", "delete-test"])))
        self.assertFalse(guard_write_intent(
            guard_text_from_argv(["--name", "create-demo"])))

    def test_state_value_not_blocked(self):
        self.assertFalse(guard_write_intent(
            guard_text_from_argv(["--state", "rejected"])))

    def test_operation_guard_per_resource(self):
        with self.assertRaises(GuardError):
            guard_operation("ListVpcAttachments", allowed="ListEnterpriseRouters")
        self.assertTrue(guard_operation(
            "ListVpcAttachments", allowed="ListVpcAttachments"))
        self.assertTrue(guard_operation(
            "ShowEnterpriseRouter", allowed="ShowEnterpriseRouter"))


class TestBuildCommands(unittest.TestCase):
    def test_er_basic(self):
        argv = build_er_command("cn-north-4")
        self.assertEqual(argv[0], "ER")
        self.assertEqual(argv[1], "ListEnterpriseRouters")
        self.assertIn("--cli-region=cn-north-4", argv)
        self.assertIn("--limit=100", argv)
        self.assertFalse(any(a.startswith("--marker") for a in argv))

    def test_er_array_filters(self):
        argv = build_er_command(
            "cn-south-1", state="available", er_id="er-9",
            enterprise_project_id="0", sort_key="name", sort_dir="desc",
            limit=10)
        self.assertIn("--state.1=available", argv)
        self.assertIn("--id.1=er-9", argv)
        self.assertIn("--enterprise_project_id.1=0", argv)
        self.assertIn("--sort_key.1=name", argv)
        self.assertIn("--sort_dir.1=desc", argv)
        self.assertIn("--limit=10", argv)

    def test_er_owned_by_self_boolean(self):
        self.assertIn("--owned_by_self=true",
                      build_er_command("cn-north-4", owned_by_self=True))
        self.assertIn("--owned_by_self=false",
                      build_er_command("cn-north-4", owned_by_self=False))
        self.assertFalse(any(a.startswith("--owned_by_self")
                             for a in build_er_command("cn-north-4")))

    def test_er_marker(self):
        argv = build_er_command("cn-north-4", marker="tok-2", limit=5)
        self.assertIn("--marker=tok-2", argv)

    def test_attachment_command(self):
        argv = build_attachment_command(
            "cn-north-4", "er-9", state="available", vpc_id="vpc-1",
            limit=10, marker="tok")
        self.assertEqual(argv[1], "ListVpcAttachments")
        self.assertIn("--er_id=er-9", argv)
        self.assertIn("--state.1=available", argv)
        self.assertIn("--vpc_id.1=vpc-1", argv)
        self.assertIn("--marker=tok", argv)

    def test_route_table_command_booleans(self):
        argv = build_route_table_command(
            "cn-north-4", "er-9", is_default_association_table=True,
            is_default_propagation_table=False)
        self.assertEqual(argv[1], "ListRouteTables")
        self.assertIn("--er_id=er-9", argv)
        self.assertIn("--is_default_association_table=true", argv)
        self.assertIn("--is_default_propagation_table=false", argv)

    def test_detail_command(self):
        argv = build_detail_command("cn-north-4", "er-9")
        self.assertEqual(argv[1], "ShowEnterpriseRouter")
        self.assertIn("--er_id=er-9", argv)
        self.assertIn("--cli-region=cn-north-4", argv)

    def test_no_write_flags_ever_added(self):
        for argv in (build_er_command("cn-north-4", state="available"),
                     build_attachment_command("cn-north-4", "er-1"),
                     build_route_table_command("cn-north-4", "er-1"),
                     build_detail_command("cn-north-4", "er-1")):
            for flag in argv:
                low = flag.lower().lstrip("-")
                self.assertFalse(low.startswith(
                    ("create", "delete", "update", "associate", "release")))


class TestExtractAndPaging(unittest.TestCase):
    def test_extract_json_plain_and_noise(self):
        self.assertEqual(extract_json('{"instances": []}'), {"instances": []})
        self.assertEqual(extract_json('noise\n{"a": 1}\n'), {"a": 1})

    def test_extract_json_invalid(self):
        with self.assertRaises(ApiError):
            extract_json("<html>not json</html>")

    def test_extract_items_keys(self):
        self.assertEqual(
            extract_items({"instances": [ER_AVAILABLE]}, ER_ITEM_KEYS),
            [ER_AVAILABLE])
        self.assertEqual(
            extract_items({"vpc_attachments": [ATTACH_AVAILABLE]},
                          ATTACHMENT_ITEM_KEYS),
            [ATTACH_AVAILABLE])
        self.assertEqual(
            extract_items({"route_tables": [ROUTE_TABLE]}, ROUTE_TABLE_ITEM_KEYS),
            [ROUTE_TABLE])
        self.assertEqual(extract_items({"page_info": {}}, ER_ITEM_KEYS), [])
        self.assertEqual(extract_items([ER_AVAILABLE], ER_ITEM_KEYS),
                         [ER_AVAILABLE])

    def test_next_marker(self):
        self.assertEqual(next_marker(
            {"page_info": {"next_marker": "tok"}}), "tok")
        self.assertEqual(next_marker(
            {"pageInfo": {"nextMarker": "tok2"}}), "tok2")
        self.assertIsNone(next_marker({"instances": []}))
        self.assertIsNone(next_marker({"page_info": {"next_marker": None}}))

    def test_payload_error_auth(self):
        payload = {
            "error_code": "common.01010013",
            "error_msg": "User is not authorized to perform er:instances:list",
        }
        with self.assertRaises(AuthError):
            check_payload_error(payload)

    def test_payload_error_not_found(self):
        with self.assertRaises(NotFoundError):
            check_payload_error({
                "error_code": "SYS.0404",
                "error_msg": "The resource could not be found.",
            })

    def test_payload_error_absent(self):
        check_payload_error({"instances": [ER_AVAILABLE]})
        check_payload_error({"page_info": {"next_marker": None}})


class TestClassifyFailure(unittest.TestCase):
    def test_missing_credentials(self):
        err = classify_hcloud_failure(
            "", "ERROR: cli-ak is empty, please run hcloud configure", 1, "ER")
        self.assertIsInstance(err, ConfigError)
        self.assertIn("AK/SK", str(err))

    def test_auth_403(self):
        err = classify_hcloud_failure(
            "", '{"error_code":"ApiGW.0301","error_msg":"403 Forbidden"}',
            1, "ER")
        self.assertIsInstance(err, AuthError)
        self.assertIn("IAM", str(err))

    def test_not_found(self):
        err = classify_hcloud_failure(
            "", "SYS.0404 The resource could not be found", 1, "ER")
        self.assertIsInstance(err, NotFoundError)

    def test_use_error_marker_zero_rc(self):
        err = classify_hcloud_failure(
            "[USE_ERROR]Invalid parameter: state\n\n"
            "Run `hcloud ER ListEnterpriseRouters --help` for details.", "", 0,
            "ListEnterpriseRouters")
        self.assertIsInstance(err, ApiError)
        self.assertIn("参数错误", str(err))

    def test_generic_api_error(self):
        err = classify_hcloud_failure("", "boom", 2, "ER")
        self.assertIsInstance(err, ApiError)

    def test_classify_error_text_not_found(self):
        self.assertIsInstance(
            classify_error_text("The resource does not exist"), NotFoundError)


class TestListCli(unittest.TestCase):
    def test_single_page(self):
        fake = FakeRunner([(
            json.dumps({"instances": [ER_AVAILABLE, ER_FAILED]}), "", 0)])
        with mock.patch("list_er.subprocess.run", fake):
            records = list_ers("cn-north-4")
        self.assertEqual(records, [ER_AVAILABLE, ER_FAILED])
        self.assertEqual(len(fake.calls), 1)

    def test_pagination_via_next_marker(self):
        page1 = {"instances": [ER_AVAILABLE],
                 "page_info": {"next_marker": "tok-2", "current_count": 1}}
        page2 = {"instances": [ER_FAILED],
                 "page_info": {"next_marker": None, "current_count": 1}}
        fake = FakeRunner([(json.dumps(page1), "", 0),
                           (json.dumps(page2), "", 0)])
        with mock.patch("list_er.subprocess.run", fake):
            records = list_ers("cn-north-4", limit=1)
        self.assertEqual(records, [ER_AVAILABLE, ER_FAILED])
        self.assertIn("--marker=tok-2", fake.calls[1])

    def test_empty_region(self):
        fake = FakeRunner([(json.dumps({"instances": []}), "", 0)])
        with mock.patch("list_er.subprocess.run", fake):
            records = list_ers("cn-north-4")
        self.assertEqual(records, [])

    def test_filters_forwarded_to_cli(self):
        fake = FakeRunner([(json.dumps({"instances": [ER_AVAILABLE]}), "", 0)])
        with mock.patch("list_er.subprocess.run", fake):
            list_ers("cn-north-4", state="available", er_id="er-0001",
                     owned_by_self=True, enterprise_project_id="0",
                     sort_key="name", sort_dir="asc")
        call = fake.calls[0]
        for fragment in ("--state.1=available", "--id.1=er-0001",
                         "--owned_by_self=true",
                         "--enterprise_project_id.1=0",
                         "--sort_key.1=name", "--sort_dir.1=asc"):
            self.assertIn(fragment, call)

    def test_error_payload_with_zero_rc_raises_auth(self):
        payload = {"error_code": "common.01010013",
                   "error_msg": "not authorized to perform er:instances:list"}
        fake = FakeRunner([(json.dumps(payload), "", 0)])
        with mock.patch("list_er.subprocess.run", fake):
            with self.assertRaises(AuthError):
                list_ers("cn-north-4")

    def test_nonzero_exit_403(self):
        fake = FakeRunner([("", "403 Forbidden", 1)])
        with mock.patch("list_er.subprocess.run", fake):
            with self.assertRaises(AuthError):
                list_ers("cn-north-4")

    def test_nonzero_exit_credentials(self):
        fake = FakeRunner([("", "ERROR: no AK configured", 1)])
        with mock.patch("list_er.subprocess.run", fake):
            with self.assertRaises(ConfigError):
                list_ers("cn-north-4")

    def test_timeout(self):
        fake = FakeRunner([subprocess.TimeoutExpired(cmd="hcloud", timeout=120)])
        with mock.patch("list_er.subprocess.run", fake):
            with self.assertRaises(ApiError):
                list_ers("cn-north-4")

    def test_sdk_fallback_when_hcloud_missing(self):
        with mock.patch("list_er.subprocess.run",
                        FakeRunner([FileNotFoundError()])), \
                mock.patch("list_er.list_ers_via_sdk",
                           return_value=[ER_AVAILABLE]) as sdk_mock:
            records = list_ers("cn-north-4", state="available",
                               er_id="er-1", owned_by_self=True,
                               project_id="proj-1")
        self.assertEqual(records, [ER_AVAILABLE])
        kwargs = sdk_mock.call_args.kwargs
        self.assertEqual(kwargs.get("state"), "available")
        self.assertEqual(kwargs.get("owned_by_self"), True)
        self.assertEqual(kwargs.get("project_id"), "proj-1")

    def test_attachment_filters_forwarded(self):
        fake = FakeRunner([(
            json.dumps({"vpc_attachments": [ATTACH_AVAILABLE]}), "", 0)])
        with mock.patch("list_er.subprocess.run", fake):
            records = list_attachments("cn-north-4", "er-9",
                                       state="available", vpc_id="vpc-1")
        self.assertEqual(records, [ATTACH_AVAILABLE])
        call = fake.calls[0]
        self.assertIn("--er_id=er-9", call)
        self.assertIn("--vpc_id.1=vpc-1", call)

    def test_route_table_fetch(self):
        fake = FakeRunner([(
            json.dumps({"route_tables": [ROUTE_TABLE]}), "", 0)])
        with mock.patch("list_er.subprocess.run", fake):
            records = list_route_tables(
                "cn-north-4", "er-9", is_default_association_table=True)
        self.assertEqual(records, [ROUTE_TABLE])
        self.assertIn("--is_default_association_table=true", fake.calls[0])

    def test_show_er_success(self):
        fake = FakeRunner([(
            json.dumps({"instance": ER_AVAILABLE}), "", 0)])
        with mock.patch("list_er.subprocess.run", fake):
            instance = show_er("cn-north-4", "er-0001")
        self.assertEqual(instance, ER_AVAILABLE)

    def test_show_er_not_found(self):
        fake = FakeRunner([(
            json.dumps({"error_code": "SYS.0404",
                        "error_msg": "The resource could not be found."}),
            "", 0)])
        with mock.patch("list_er.subprocess.run", fake):
            with self.assertRaises(NotFoundError):
                show_er("cn-north-4", "missing")

    def test_show_er_empty_payload(self):
        fake = FakeRunner([(json.dumps({}), "", 0)])
        with mock.patch("list_er.subprocess.run", fake):
            with self.assertRaises(NotFoundError):
                show_er("cn-north-4", "missing")


class _FakeItem:
    def __init__(self, payload):
        self._payload = payload

    def to_dict(self):
        return self._payload


class _FakeResponse:
    def __init__(self, **kwargs):
        self.page_info = None
        for key, value in kwargs.items():
            setattr(self, key, value)


class _FakeSdkClient:
    def __init__(self, **responses):
        for name, response in responses.items():
            setattr(self, name, mock.Mock(return_value=response))


class TestSdkFallback(unittest.TestCase):
    """Validate the SDK fallback request/response wiring with fake SDK objects."""

    def _fake_client(self, method, **kwargs):
        class _Client:
            pass

        client = _Client()
        setattr(client, method, mock.Mock(return_value=_FakeResponse(**kwargs)))
        return client

    def test_list_ers_via_sdk(self):
        client = self._fake_client(
            "list_enterprise_routers",
            instances=[_FakeItem(ER_AVAILABLE), _FakeItem(ER_FAILED)])
        with mock.patch("list_er._build_sdk_client", return_value=client), \
                mock.patch(
                    "huaweicloudsdker.v3.ListEnterpriseRoutersRequest",
                    lambda **kw: SimpleNamespace(**kw)):
            records = list_ers_via_sdk(
                "cn-north-4", state="available", er_id="er-1",
                owned_by_self=True, enterprise_project_id="0",
                sort_key="name", sort_dir="desc")
        self.assertEqual(records, [ER_AVAILABLE, ER_FAILED])
        request = client.list_enterprise_routers.call_args[0][0]
        self.assertEqual(request.state, ["available"])
        self.assertEqual(request.id, ["er-1"])
        self.assertEqual(request.owned_by_self, True)
        self.assertEqual(request.enterprise_project_id, ["0"])
        self.assertEqual(request.sort_key, ["name"])

    def test_list_attachments_via_sdk(self):
        client = self._fake_client(
            "list_vpc_attachments",
            vpc_attachments=[_FakeItem(ATTACH_AVAILABLE)])
        with mock.patch("list_er._build_sdk_client", return_value=client), \
                mock.patch(
                    "huaweicloudsdker.v3.ListVpcAttachmentsRequest",
                    lambda **kw: SimpleNamespace(**kw)):
            records = list_attachments_via_sdk(
                "cn-north-4", "er-9", state="available", vpc_id="vpc-1")
        self.assertEqual(records, [ATTACH_AVAILABLE])
        request = client.list_vpc_attachments.call_args[0][0]
        self.assertEqual(request.er_id, "er-9")
        self.assertEqual(request.vpc_id, ["vpc-1"])

    def test_list_route_tables_via_sdk(self):
        client = self._fake_client(
            "list_route_tables", route_tables=[_FakeItem(ROUTE_TABLE)])
        with mock.patch("list_er._build_sdk_client", return_value=client), \
                mock.patch(
                    "huaweicloudsdker.v3.ListRouteTablesRequest",
                    lambda **kw: SimpleNamespace(**kw)):
            records = list_route_tables_via_sdk(
                "cn-north-4", "er-9", is_default_association_table=True)
        self.assertEqual(records, [ROUTE_TABLE])
        request = client.list_route_tables.call_args[0][0]
        self.assertEqual(request.er_id, "er-9")
        self.assertEqual(request.is_default_association_table, True)

    def test_show_er_via_sdk(self):
        client = self._fake_client(
            "show_enterprise_router",
            instance=_FakeItem(ER_AVAILABLE))
        with mock.patch("list_er._build_sdk_client", return_value=client), \
                mock.patch(
                    "huaweicloudsdker.v3.ShowEnterpriseRouterRequest",
                    lambda **kw: SimpleNamespace(**kw)):
            instance = show_er_via_sdk("cn-north-4", "er-0001")
        self.assertEqual(instance, ER_AVAILABLE)
        request = client.show_enterprise_router.call_args[0][0]
        self.assertEqual(request.er_id, "er-0001")

    def test_sdk_missing_project_id_raises_config(self):
        env = {name: "" for name in (
            "HW_ACCESS_KEY", "HUAWEI_ACCESS_KEY", "HUAWEICLOUD_SDK_AK",
            "HUAWEI_CLOUD_ACCESS_KEY", "HW_SECRET_KEY", "HUAWEI_SECRET_KEY",
            "HUAWEICLOUD_SDK_SK", "HUAWEI_CLOUD_SECRET_KEY", "HW_PROJECT_ID",
            "HUAWEI_PROJECT_ID", "HUAWEICLOUD_SDK_PROJECT_ID",
            "HUAWEI_CLOUD_PROJECT_ID")}
        env.update(HUAWEI_ACCESS_KEY="ak", HUAWEI_SECRET_KEY="sk")
        with mock.patch.dict(os.environ, env, clear=True):
            with self.assertRaises(ConfigError) as ctx:
                list_ers_via_sdk("cn-north-4")
        self.assertIn("project_id", str(ctx.exception))


class TestRender(unittest.TestCase):
    def test_split_by_state(self):
        available, abnormal = split_by_state([ER_AVAILABLE, ER_FAILED])
        self.assertEqual(available, [ER_AVAILABLE])
        self.assertEqual(abnormal, [ER_FAILED])

    def test_er_table_has_eight_columns(self):
        table = render_fixed_table([ER_AVAILABLE], ER_TABLE_COLUMNS)
        self.assertEqual(len(ER_TABLE_COLUMNS), 8)
        header = table.splitlines()[0]
        for label in ("名称", "ID", "状态", "ASN", "企业项目ID",
                      "可用区", "描述", "创建时间"):
            self.assertIn(label, header)
        self.assertIn("er-0001", table)
        self.assertIn("cn-north-4a,cn-north-4b", table)

    def test_attachment_table_has_six_columns(self):
        table = render_fixed_table([ATTACH_AVAILABLE],
                                   ATTACHMENT_TABLE_COLUMNS)
        self.assertEqual(len(ATTACHMENT_TABLE_COLUMNS), 6)
        self.assertIn("VPC ID", table)
        self.assertIn("subnet-0001", table)

    def test_route_table_table_columns(self):
        self.assertEqual(len(ROUTE_TABLE_COLUMNS), 6)
        table = render_fixed_table([ROUTE_TABLE], ROUTE_TABLE_COLUMNS)
        self.assertIn("True", table)

    def test_render_sections_separates_abnormal(self):
        text = render_sections(
            [ER_AVAILABLE, ER_FAILED], ER_TABLE_COLUMNS,
            "正常（available）企业路由器（%d 个）：",
            "非 available 状态的企业路由器（%d 个，单独列出，请重点关注）：")
        self.assertIn("正常（available）企业路由器（1 个）", text)
        self.assertIn("[!] 非 available 状态的企业路由器（1 个", text)
        self.assertLess(text.index("er-0001"), text.index("[!]"))
        self.assertLess(text.index("[!]"), text.index("er-0002"))

    def test_render_compact_sections_flags_abnormal(self):
        text = render_compact_sections(
            [ER_AVAILABLE, ER_FAILED],
            lambda r, abnormal=False: ("[异常] " if abnormal else "- ")
            + str(r["id"]),
            "正常（available）企业路由器（%d 个）：",
            "非 available 状态的企业路由器（%d 个，单独列出，请重点关注）：")
        self.assertIn("- er-0001", text)
        self.assertIn("[异常] er-0002", text)

    def test_local_filters(self):
        records = [ER_AVAILABLE, ER_FAILED]
        self.assertEqual(apply_local_filters(records, name="er-demo-02"),
                         [ER_FAILED])
        self.assertEqual(apply_local_filters(records, fuzzy="DEMO-01"),
                         [ER_AVAILABLE])
        self.assertEqual(apply_local_filters(records, fuzzy="nomatch"), [])

    def test_render_detail(self):
        detail = render_detail(ER_AVAILABLE, "cn-north-4")
        self.assertIn("企业路由器（ER）详情（Region cn-north-4）", detail)
        self.assertIn("er-0001", detail)
        self.assertIn("默认关联路由表ID: rt-1", detail)


class TestMain(unittest.TestCase):
    def _run(self, argv, results):
        fake = FakeRunner(results)
        with mock.patch("list_er.subprocess.run", fake), \
                mock.patch("sys.stdout") as stdout, \
                mock.patch("sys.stderr") as stderr:
            rc = main(argv)
        out = "".join(c[0][0] for c in stdout.write.call_args_list)
        err = "".join(c[0][0] for c in stderr.write.call_args_list)
        return rc, out, err

    def test_er_compact_output_marks_abnormal(self):
        rc, out, err = self._run(
            ["--region", "cn-north-4"],
            [(json.dumps({"instances": [ER_AVAILABLE, ER_FAILED]}), "", 0)])
        self.assertEqual(rc, 0)
        self.assertIn("企业路由器（ER）列表", out)
        self.assertIn("er-0001", out)
        self.assertIn("[!] 非 available", out)
        self.assertIn("[异常] er-demo-02", out)
        self.assertEqual(err, "")

    def test_er_table_output(self):
        rc, out, _ = self._run(
            ["--table"],
            [(json.dumps({"instances": [ER_AVAILABLE, ER_FAILED]}), "", 0)])
        self.assertEqual(rc, 0)
        for label in ("名称", "ID", "状态", "ASN", "创建时间"):
            self.assertIn(label, out)
        self.assertIn("[!] 非 available", out)

    def test_er_json_output(self):
        rc, out, _ = self._run(
            ["--json"],
            [(json.dumps({"instances": [ER_AVAILABLE]}), "", 0)])
        self.assertEqual(rc, 0)
        self.assertEqual(json.loads(out), [ER_AVAILABLE])

    def test_er_empty_message(self):
        rc, out, _ = self._run(
            ["--region", "cn-south-1"],
            [(json.dumps({"instances": []}), "", 0)])
        self.assertEqual(rc, 0)
        self.assertIn("无企业路由器（ER）", out)
        self.assertIn("cn-south-1", out)

    def test_er_filter_forwarded_and_empty_suffix(self):
        fake = FakeRunner([(json.dumps({"instances": []}), "", 0)])
        with mock.patch("list_er.subprocess.run", fake), \
                mock.patch("sys.stdout") as stdout, \
                mock.patch("sys.stderr"):
            rc = main(["--state", "failed", "--name", "demo"])
        out = "".join(c[0][0] for c in stdout.write.call_args_list)
        self.assertEqual(rc, 0)
        self.assertIn("--state.1=failed", fake.calls[0])
        self.assertIn("state=failed", out)
        self.assertIn("name=demo", out)

    def test_attachment_requires_er_id(self):
        rc, _, err = self._run(["--resource", "attachment"], [])
        self.assertEqual(rc, 1)
        self.assertIn("--er-id", err)

    def test_attachment_table_six_columns(self):
        rc, out, _ = self._run(
            ["--resource", "attachment", "--er-id", "er-9", "--table"],
            [(json.dumps({"vpc_attachments": [ATTACH_AVAILABLE,
                                              ATTACH_FAILED]}), "", 0)])
        self.assertEqual(rc, 0)
        self.assertIn("VPC ID", out)
        self.assertIn("att-0001", out)
        self.assertIn("[!] 非 available", out)

    def test_attachment_empty_message(self):
        rc, out, _ = self._run(
            ["--resource", "attachment", "--er-id", "er-9"],
            [(json.dumps({"vpc_attachments": []}), "", 0)])
        self.assertEqual(rc, 0)
        self.assertIn("无 VPC 连接", out)

    def test_route_table_output(self):
        rc, out, _ = self._run(
            ["--resource", "route-table", "--er-id", "er-9", "--table"],
            [(json.dumps({"route_tables": [ROUTE_TABLE]}), "", 0)])
        self.assertEqual(rc, 0)
        self.assertIn("默认关联", out)
        self.assertIn("rt-0001", out)

    def test_route_table_empty_message(self):
        rc, out, _ = self._run(
            ["--resource", "route-table", "--er-id", "er-9"],
            [(json.dumps({"route_tables": []}), "", 0)])
        self.assertEqual(rc, 0)
        self.assertIn("无路由表", out)

    def test_detail_success(self):
        rc, out, _ = self._run(
            ["--resource", "detail", "--er-id", "er-0001"],
            [(json.dumps({"instance": ER_AVAILABLE}), "", 0)])
        self.assertEqual(rc, 0)
        self.assertIn("企业路由器（ER）详情", out)
        self.assertIn("er-0001", out)

    def test_detail_json(self):
        rc, out, _ = self._run(
            ["--resource", "detail", "--er-id", "er-0001", "--json"],
            [(json.dumps({"instance": ER_AVAILABLE}), "", 0)])
        self.assertEqual(rc, 0)
        self.assertEqual(json.loads(out), ER_AVAILABLE)

    def test_detail_not_found_rc_nonzero(self):
        rc, _, err = self._run(
            ["--resource", "detail", "--er-id", "missing"],
            [(json.dumps({"error_code": "SYS.0404",
                          "error_msg": "The resource could not be found."}),
              "", 0)])
        self.assertEqual(rc, 1)
        self.assertIn("未找到", err)

    def test_detail_requires_er_id(self):
        rc, _, err = self._run(["--resource", "detail"], [])
        self.assertEqual(rc, 1)
        self.assertIn("--er-id", err)

    def test_write_intent_operation_blocked(self):
        rc, _, err = self._run(
            ["--operation", "DeleteEnterpriseRouter"], [])
        self.assertEqual(rc, 1)
        self.assertIn("写操作意图", err)

    def test_write_intent_keyword_blocked(self):
        rc, _, err = self._run(["--er-id", "release-me"], [])
        self.assertEqual(rc, 1)
        self.assertIn("守卫拦截", err)

    def test_auth_error_message(self):
        rc, _, err = self._run([], [("", "403 Forbidden", 1)])
        self.assertEqual(rc, 1)
        self.assertIn("IAM", err)

    def test_missing_ak_sk_message(self):
        rc, _, err = self._run([], [("", "ERROR: cli-ak empty", 1)])
        self.assertEqual(rc, 1)
        self.assertIn("AK/SK", err)

    def test_hcloud_missing_falls_back_to_sdk(self):
        with mock.patch("list_er.list_ers_via_sdk",
                        return_value=[ER_AVAILABLE]):
            rc, out, _ = self._run([], [FileNotFoundError()])
        self.assertEqual(rc, 0)
        self.assertIn("er-0001", out)

    def test_hcloud_missing_sdk_unavailable(self):
        with mock.patch("list_er.list_ers_via_sdk",
                        side_effect=ConfigError("huaweicloudsdker 未安装")):
            rc, _, err = self._run([], [FileNotFoundError()])
        self.assertEqual(rc, 1)
        self.assertIn("未安装", err)

    def test_page_size_out_of_range(self):
        rc, _, err = self._run(["--page-size", "0"], [])
        self.assertEqual(rc, 1)
        self.assertIn("--page-size", err)

    def test_limit_alias(self):
        fake = FakeRunner([(json.dumps({"instances": [ER_AVAILABLE]}), "", 0)])
        with mock.patch("list_er.subprocess.run", fake), \
                mock.patch("sys.stdout"), mock.patch("sys.stderr"):
            rc = main(["--limit", "5"])
        self.assertEqual(rc, 0)
        self.assertIn("--limit=5", fake.calls[0])

    def test_resource_attachment_not_blocked_as_write_intent(self):
        rc, _, _ = self._run(
            ["--resource", "attachment", "--er-id", "er-9"],
            [(json.dumps({"vpc_attachments": []}), "", 0)])
        self.assertEqual(rc, 0)


class TestErrorHierarchy(unittest.TestCase):
    def test_subclasses(self):
        for exc in (GuardError, ConfigError, AuthError, NotFoundError, ApiError):
            self.assertTrue(issubclass(exc, ErListError))


if __name__ == "__main__":
    unittest.main()