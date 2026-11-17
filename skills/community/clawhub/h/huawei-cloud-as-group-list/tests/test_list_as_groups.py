#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Offline unit tests for huawei-cloud-as-group-list.

No credentials and no network are used: the KooCLI subprocess is mocked with a
fake runner (plus one integration case with a real mock executable), and the
SDK fallback is driven by a fake client injected through ``sdk_client``.

Run:
    python3 -m unittest discover -s tests -v
"""

import importlib.util
import io
import json
import os
import pathlib
import stat
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout

HERE = pathlib.Path(__file__).resolve().parent
MOD_PATH = HERE.parent / "scripts" / "list_as_groups.py"

_spec = importlib.util.spec_from_file_location("list_as_groups", MOD_PATH)
as_groups = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(as_groups)


GROUP_A = {
    "scaling_group_id": "grp-aaaa-1111",
    "scaling_group_name": "web-prod",
    "scaling_group_status": "INSERVICE",
    "desire_instance_number": 2,
    "current_instance_number": 2,
    "min_instance_number": 1,
    "max_instance_number": 5,
    "vpc_id": "vpc-1111",
    "networks": [{"id": "subnet-1111"}, {"id": "subnet-2222"}],
    "lbaas_listeners": [{"listener_id": "elb-1111", "pool_id": "pool-1111"}],
    "lb_listener_id": "",
    "create_time": "2025-01-01T00:00:00Z",
}
GROUP_B = {
    "scaling_group_id": "grp-bbbb-2222",
    "scaling_group_name": "web-dev",
    "scaling_group_status": "INSERVICE",
    "desire_instance_number": 3,
    "current_instance_number": 1,
    "min_instance_number": 1,
    "max_instance_number": 5,
    "vpc_id": "vpc-2222",
    "networks": [{"id": "subnet-3333"}],
    "lb_listener_id": "elb-classic-2222",
    "create_time": "2025-01-02T00:00:00Z",
}
GROUP_C = {
    "scaling_group_id": "grp-cccc-3333",
    "scaling_group_name": "batch-worker",
    "scaling_group_status": "ERROR",
    "desire_instance_number": 1,
    "current_instance_number": 1,
    "min_instance_number": 1,
    "max_instance_number": 3,
    "vpc_id": "",
    "networks": [],
    "lbaas_listeners": [],
    "create_time": "2025-01-03T00:00:00Z",
}

INST_A = {
    "instance_id": "inst-1111",
    "instance_name": "web-prod-1",
    "scaling_group_id": GROUP_A["scaling_group_id"],
    "scaling_group_name": GROUP_A["scaling_group_name"],
    "life_cycle_state": "INSERVICE",
    "health_status": "NORMAL",
    "create_time": "2025-01-01T00:01:00Z",
}
INST_B = {
    "instance_id": "inst-2222",
    "instance_name": "web-dev-1",
    "scaling_group_id": GROUP_B["scaling_group_id"],
    "scaling_group_name": GROUP_B["scaling_group_name"],
    "life_cycle_state": "PENDING",
    "health_status": "NORMAL",
    "create_time": "2025-01-02T00:01:00Z",
}
INST_C = {
    "instance_id": "inst-3333",
    "instance_name": "web-prod-2",
    "scaling_group_id": GROUP_A["scaling_group_id"],
    "scaling_group_name": GROUP_A["scaling_group_name"],
    "life_cycle_state": "INSERVICE",
    "health_status": "ERROR",
    "create_time": "2025-01-01T00:02:00Z",
}


def group_page(items, total=None, start=0, limit=100):
    return {
        "total_number": len(items) if total is None else total,
        "start_number": start,
        "limit": limit,
        "scaling_groups": [dict(item) for item in items],
    }


def instance_page(items, total=None, start=0, limit=100):
    return {
        "total_number": len(items) if total is None else total,
        "start_number": start,
        "limit": limit,
        "scaling_group_instances": [dict(item) for item in items],
    }


class FakeHcloud(object):
    """Replacement for ``list_as_groups.run_hcloud``."""

    def __init__(self, pages=None, error=None, fail_op=None):
        self.pages = list(pages or [])
        self.error = error
        self.fail_op = fail_op
        self.calls = []

    def __call__(self, args, timeout=None):
        self.calls.append(list(args))
        operation = args[1] if len(args) > 1 else ""
        if self.error is not None and (self.fail_op is None
                                       or operation == self.fail_op):
            raise self.error
        index = len(self.calls) - 1
        if index < len(self.pages):
            return dict(self.pages[index])
        key = "scaling_group_instances" if operation == "ListScalingInstances" else "scaling_groups"
        return {"total_number": 0, "start_number": 0, "limit": 100, key: []}

    def operations(self):
        return [call[1] for call in self.calls if len(call) > 1]

    def arg(self, call, prefix):
        for item in call:
            if str(item).startswith(prefix):
                return str(item)[len(prefix):]
        return None


class FakeSdkResponse(object):
    def __init__(self, data):
        self._data = data

    def to_dict(self):
        return dict(self._data)


class FakeSdkClient(object):
    def __init__(self, group_pages=None, instance_pages=None):
        self.group_pages = list(group_pages or [])
        self.instance_pages = list(instance_pages or [])
        self.group_requests = []
        self.instance_requests = []

    def list_scaling_groups(self, request):
        self.group_requests.append(request)
        index = len(self.group_requests) - 1
        data = (self.group_pages[index] if index < len(self.group_pages)
                else group_page([]))
        return FakeSdkResponse(data)

    def list_scaling_instances(self, request):
        self.instance_requests.append(request)
        index = len(self.instance_requests) - 1
        data = (self.instance_pages[index] if index < len(self.instance_pages)
                else instance_page([]))
        return FakeSdkResponse(data)


class Base(unittest.TestCase):
    def setUp(self):
        self._env = dict(os.environ)
        for name in as_groups.HCLOUD_BIN_ENV + (
                "HUAWEICLOUD_SDK_AK", "HUAWEICLOUD_SDK_SK",
                "HUAWEICLOUD_SDK_SECURITY_TOKEN",
                "HUAWEI_ACCESS_KEY", "HUAWEI_SECRET_KEY"):
            os.environ.pop(name, None)
        self._run_hcloud = as_groups.run_hcloud
        self._hcloud_binary = as_groups.hcloud_binary
        self._sdk_client = as_groups.sdk_client
        self._sdk_page = as_groups.sdk_page

    def tearDown(self):
        as_groups.run_hcloud = self._run_hcloud
        as_groups.hcloud_binary = self._hcloud_binary
        as_groups.sdk_client = self._sdk_client
        as_groups.sdk_page = self._sdk_page
        os.environ.clear()
        os.environ.update(self._env)

    def install_hcloud(self, fake, binary="/usr/local/bin/hcloud"):
        as_groups.run_hcloud = fake
        as_groups.hcloud_binary = lambda: binary

    def install_sdk(self, fake):
        as_groups.sdk_client = lambda region: fake

    def run_main(self, argv):
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            code = as_groups.main(argv)
        return code, out.getvalue(), err.getvalue()


class TestCommandConstruction(Base):
    def test_group_command_contains_region_limit_and_start(self):
        fake = FakeHcloud([group_page([GROUP_A])])
        self.install_hcloud(fake)
        code, out, _ = self.run_main(["--region", "cn-north-4"])
        self.assertEqual(code, 0)
        call = fake.calls[0]
        self.assertEqual(call[:2], ["AS", "ListScalingGroups"])
        self.assertEqual(fake.arg(call, "--cli-region="), "cn-north-4")
        self.assertEqual(fake.arg(call, "--limit="), "100")
        self.assertEqual(fake.arg(call, "--start_number="), "0")

    def test_name_is_forwarded_server_side(self):
        fake = FakeHcloud([group_page([GROUP_A])])
        self.install_hcloud(fake)
        code, _, _ = self.run_main(["--name", "web-prod"])
        self.assertEqual(code, 0)
        self.assertEqual(fake.arg(fake.calls[0], "--scaling_group_name="),
                         "web-prod")

    def test_group_id_uses_instance_operation(self):
        fake = FakeHcloud([instance_page([INST_A])])
        self.install_hcloud(fake)
        code, _, _ = self.run_main(["--group-id", GROUP_A["scaling_group_id"]])
        self.assertEqual(code, 0)
        self.assertEqual(fake.operations(), ["ListScalingInstances"])
        self.assertEqual(
            fake.arg(fake.calls[0], "--scaling_group_id="),
            GROUP_A["scaling_group_id"])


class TestOutputModes(Base):
    def test_default_compact_group_list(self):
        self.install_hcloud(FakeHcloud(
            [group_page([GROUP_A, GROUP_B, GROUP_C])]))
        code, out, _ = self.run_main(["--region", "cn-north-4"])
        self.assertEqual(code, 0)
        self.assertIn("名称", out)
        self.assertIn("组ID", out)
        self.assertIn("状态", out)
        self.assertNotIn("期望实例数", out)
        self.assertIn("web-prod", out)
        self.assertIn("batch-worker", out)
        self.assertIn("共 3 个伸缩组", out)
        self.assertIn("cn-north-4", out)
        self.assertIn("异常: 2", out)

    def test_group_table_sections_and_markers(self):
        self.install_hcloud(FakeHcloud(
            [group_page([GROUP_A, GROUP_B, GROUP_C])]))
        code, out, _ = self.run_main(["--table"])
        self.assertEqual(code, 0)
        for header in as_groups.GROUP_TABLE_HEADER:
            self.assertIn(header, out)
        self.assertIn("异常伸缩组", out)
        self.assertIn("正常伸缩组", out)
        self.assertIn("⚠ " + GROUP_B["scaling_group_id"], out)
        self.assertIn("⚠ " + GROUP_C["scaling_group_id"], out)
        self.assertNotIn("⚠ " + GROUP_A["scaling_group_id"], out)
        self.assertIn("1-5", out)
        self.assertIn("subnet-1111,subnet-2222", out)
        self.assertIn("elb-1111", out)
        self.assertIn("elb-classic-2222", out)

    def test_group_table_without_abnormal_prints_none(self):
        self.install_hcloud(FakeHcloud([group_page([GROUP_A])]))
        code, out, _ = self.run_main(["--table"])
        self.assertEqual(code, 0)
        self.assertIn("异常伸缩组", out)
        self.assertIn("无", out)
        self.assertIn("正常伸缩组", out)

    def test_instance_default_compact_list(self):
        self.install_hcloud(FakeHcloud(
            [instance_page([INST_A, INST_B, INST_C])]))
        code, out, _ = self.run_main(
            ["--group-id", GROUP_A["scaling_group_id"]])
        self.assertEqual(code, 0)
        self.assertIn("实例ID", out)
        self.assertIn("实例名", out)
        self.assertIn("生命周期状态", out)
        self.assertIn("健康状态", out)
        self.assertIn("inst-1111", out)
        self.assertIn("共 3 个实例", out)
        self.assertIn("异常: 2", out)

    def test_instance_table_sections_and_markers(self):
        self.install_hcloud(FakeHcloud(
            [instance_page([INST_A, INST_B, INST_C])]))
        code, out, _ = self.run_main(
            ["--group-id", GROUP_A["scaling_group_id"], "--table"])
        self.assertEqual(code, 0)
        for header in as_groups.INSTANCE_TABLE_HEADER:
            self.assertIn(header, out)
        self.assertIn("异常实例", out)
        self.assertIn("正常实例", out)
        self.assertIn("⚠ " + INST_B["instance_id"], out)
        self.assertIn("⚠ " + INST_C["instance_id"], out)
        self.assertNotIn("⚠ " + INST_A["instance_id"], out)

    def test_json_group_raw_body(self):
        self.install_hcloud(FakeHcloud(
            [group_page([GROUP_A, GROUP_B], total=2)]))
        code, out, _ = self.run_main(["--json", "--region", "cn-north-4"])
        self.assertEqual(code, 0)
        data = json.loads(out)
        self.assertEqual(data["total_number"], 2)
        self.assertEqual(len(data["scaling_groups"]), 2)
        self.assertEqual(data["region"], "cn-north-4")

    def test_json_instance_raw_body(self):
        self.install_hcloud(FakeHcloud([instance_page([INST_A, INST_B])]))
        code, out, _ = self.run_main(
            ["--json", "--group-id", GROUP_A["scaling_group_id"]])
        self.assertEqual(code, 0)
        data = json.loads(out)
        self.assertEqual(data["total_number"], 2)
        self.assertEqual(len(data["scaling_group_instances"]), 2)

    def test_json_ignores_client_filters(self):
        self.install_hcloud(FakeHcloud([group_page([GROUP_A, GROUP_B])]))
        code, out, _ = self.run_main(["--json", "--name", "does-not-exist"])
        self.assertEqual(code, 0)
        data = json.loads(out)
        self.assertEqual(len(data["scaling_groups"]), 2)


class TestFilters(Base):
    def setUp(self):
        Base.setUp(self)
        self.install_hcloud(FakeHcloud(
            [group_page([GROUP_A, GROUP_B, GROUP_C])]))

    def test_name_exact(self):
        code, out, _ = self.run_main(["--name", "web-prod"])
        self.assertEqual(code, 0)
        self.assertIn("web-prod", out)
        self.assertNotIn("web-dev", out)
        self.assertIn("共 1 个伸缩组", out)

    def test_name_exact_is_not_substring(self):
        code, out, _ = self.run_main(["--name", "web"])
        self.assertEqual(code, 0)
        self.assertIn("未找到匹配的伸缩组", out)

    def test_name_fuzzy(self):
        code, out, _ = self.run_main(["--name", "web", "--fuzzy"])
        self.assertEqual(code, 0)
        self.assertIn("web-prod", out)
        self.assertIn("web-dev", out)
        self.assertNotIn("batch-worker", out)

    def test_status_error(self):
        code, out, _ = self.run_main(["--status", "ERROR"])
        self.assertEqual(code, 0)
        self.assertIn("batch-worker", out)
        self.assertNotIn("web-prod", out)

    def test_status_abnormal_alias(self):
        code, out, _ = self.run_main(["--status", "abnormal"])
        self.assertEqual(code, 0)
        self.assertIn("web-dev", out)
        self.assertIn("batch-worker", out)
        self.assertNotIn("web-prod", out)

    def test_status_inservice_keeps_drift_group(self):
        code, out, _ = self.run_main(["--status", "INSERVICE"])
        self.assertEqual(code, 0)
        self.assertIn("web-prod", out)
        self.assertIn("web-dev", out)
        self.assertNotIn("batch-worker", out)

    def test_invalid_status_rejected(self):
        code, _, err = self.run_main(["--status", "bogus"])
        self.assertEqual(code, 1)
        self.assertIn("--status", err)

    def test_instance_status_filter(self):
        fake = FakeHcloud([instance_page([INST_A, INST_B, INST_C])])
        self.install_hcloud(fake)
        code, out, _ = self.run_main(
            ["--group-id", GROUP_A["scaling_group_id"], "--status", "PENDING"])
        self.assertEqual(code, 0)
        self.assertIn("inst-2222", out)
        self.assertNotIn("inst-1111", out)

    def test_instance_health_status_filter(self):
        fake = FakeHcloud([instance_page([INST_A, INST_B, INST_C])])
        self.install_hcloud(fake)
        code, out, _ = self.run_main(
            ["--group-id", GROUP_A["scaling_group_id"], "--status", "ERROR"])
        self.assertEqual(code, 0)
        self.assertIn("inst-3333", out)
        self.assertNotIn("inst-1111", out)

    def test_instance_abnormal_alias(self):
        fake = FakeHcloud([instance_page([INST_A, INST_B, INST_C])])
        self.install_hcloud(fake)
        code, out, _ = self.run_main(
            ["--group-id", GROUP_A["scaling_group_id"], "--status", "abnormal"])
        self.assertEqual(code, 0)
        self.assertIn("inst-2222", out)
        self.assertIn("inst-3333", out)
        self.assertNotIn("inst-1111", out)


class TestGroupDrillDown(Base):
    def test_empty_instance_list_hint(self):
        self.install_hcloud(FakeHcloud([instance_page([])]))
        code, out, _ = self.run_main(
            ["--group-id", GROUP_A["scaling_group_id"]])
        self.assertEqual(code, 0)
        self.assertIn("内无实例", out)
        self.assertIn("cn-north-4", out)

    def test_status_no_match_hint(self):
        self.install_hcloud(FakeHcloud([instance_page([INST_A])]))
        code, out, _ = self.run_main(
            ["--group-id", GROUP_A["scaling_group_id"], "--status", "REMOVING"])
        self.assertEqual(code, 0)
        self.assertIn("未找到匹配的实例", out)

    def test_invalid_group_id_is_actionable(self):
        self.install_hcloud(FakeHcloud(error=as_groups.AsError(
            "not_found", "伸缩组不存在或不属于当前区域（请确认 --group-id 与 --region）。")))
        code, _, err = self.run_main(["--group-id", "no-such-group"])
        self.assertEqual(code, 1)
        self.assertIn("伸缩组不存在", err)
        self.assertIn("--region", err)


class TestEmptyAndErrors(Base):
    def test_empty_group_list_hint(self):
        self.install_hcloud(FakeHcloud([group_page([])]))
        code, out, _ = self.run_main(["--region", "cn-north-4"])
        self.assertEqual(code, 0)
        self.assertIn("当前区域无伸缩组", out)
        self.assertIn("cn-north-4", out)

    def test_empty_filtered_group_list_hint(self):
        self.install_hcloud(FakeHcloud([group_page([GROUP_A])]))
        code, out, _ = self.run_main(["--name", "nope"])
        self.assertEqual(code, 0)
        self.assertIn("未找到匹配的伸缩组", out)

    def test_forbidden_error_hint(self):
        self.install_hcloud(FakeHcloud(error=as_groups.classify_cli_error(
            '{"error":{"code":"AS.0031","message":"not authorized to perform: '
            'as:scalingGroup:list"}}')))
        code, _, err = self.run_main([])
        self.assertEqual(code, 1)
        self.assertIn("as:scalingGroup:list", err)
        self.assertIn("as:instances:list", err)

    def test_use_error_hint(self):
        self.install_hcloud(FakeHcloud(error=as_groups.AsError(
            "use_error", "KooCLI 参数/用法错误（[USE_ERROR]）")))
        code, _, err = self.run_main([])
        self.assertEqual(code, 1)
        self.assertIn("[USE_ERROR]", err)

    def test_classify_not_found(self):
        exc = as_groups.classify_cli_error(
            "AS.0049 The scaling group does not exist.", 0)
        self.assertEqual(exc.kind, "not_found")
        self.assertIn("伸缩组不存在", exc.message)

    def test_classify_credentials(self):
        exc = as_groups.classify_cli_error(
            "no valid authentication, please configure AK/SK", 1)
        self.assertEqual(exc.kind, "credentials")

    def test_cli_backend_without_hcloud(self):
        self.install_hcloud(FakeHcloud([group_page([GROUP_A])]), binary=None)
        code, _, err = self.run_main(["--backend", "cli"])
        self.assertEqual(code, 1)
        self.assertIn("未找到 hcloud", err)

    def test_auto_falls_back_to_sdk(self):
        self.install_hcloud(FakeHcloud(error=as_groups.AsError(
            "timeout", "timeout")))
        fake_sdk = FakeSdkClient(group_pages=[group_page([GROUP_A])])
        self.install_sdk(fake_sdk)
        code, out, err = self.run_main([])
        self.assertEqual(code, 0)
        self.assertIn("回退 SDK", err)
        self.assertIn("web-prod", out)
        self.assertIn("后端: sdk", out)
        self.assertEqual(len(fake_sdk.group_requests), 1)

    def test_forbidden_does_not_fall_back(self):
        self.install_hcloud(FakeHcloud(error=as_groups.AsError(
            "forbidden", "no permission")))
        fake_sdk = FakeSdkClient(group_pages=[group_page([GROUP_A])])
        self.install_sdk(fake_sdk)
        code, _, err = self.run_main([])
        self.assertEqual(code, 1)
        self.assertIn("no permission", err)
        self.assertEqual(fake_sdk.group_requests, [])

    def test_sdk_backend_request_fields(self):
        fake_sdk = FakeSdkClient(group_pages=[group_page([GROUP_A])])
        self.install_sdk(fake_sdk)
        code, out, _ = self.run_main(["--backend", "sdk", "--name", "web-prod"])
        self.assertEqual(code, 0)
        self.assertIn("web-prod", out)
        request = fake_sdk.group_requests[0]
        self.assertEqual(getattr(request, "scaling_group_name", None), "web-prod")
        self.assertEqual(getattr(request, "limit", None), 100)
        self.assertEqual(getattr(request, "start_number", None), 0)

    def test_sdk_instance_request_fields(self):
        fake_sdk = FakeSdkClient(instance_pages=[instance_page([INST_A])])
        self.install_sdk(fake_sdk)
        code, out, _ = self.run_main(
            ["--backend", "sdk", "--group-id", GROUP_A["scaling_group_id"]])
        self.assertEqual(code, 0)
        self.assertIn("inst-1111", out)
        request = fake_sdk.instance_requests[0]
        self.assertEqual(getattr(request, "scaling_group_id", None),
                         GROUP_A["scaling_group_id"])

    def test_sdk_missing_message(self):
        def missing_client(region):
            raise as_groups.AsError("sdk_missing", "未安装华为云 AS SDK")

        as_groups.sdk_client = missing_client
        code, _, err = self.run_main(["--backend", "sdk"])
        self.assertEqual(code, 1)
        self.assertIn("SDK", err)


class TestPagination(Base):
    def test_follows_total_and_start_number(self):
        fake = FakeHcloud([
            group_page([GROUP_A], total=2, start=0, limit=1),
            group_page([GROUP_B], total=2, start=1, limit=1),
        ])
        self.install_hcloud(fake)
        code, out, _ = self.run_main(["--limit", "1"])
        self.assertEqual(code, 0)
        self.assertIn("共 2 个伸缩组", out)
        self.assertEqual(len(fake.calls), 2)
        self.assertEqual(fake.arg(fake.calls[0], "--start_number="), "0")
        self.assertEqual(fake.arg(fake.calls[1], "--start_number="), "1")

    def test_total_exact_multiple_stops_without_extra_page(self):
        fake = FakeHcloud([
            group_page([GROUP_A], total=2, start=0, limit=1),
            group_page([GROUP_B], total=2, start=1, limit=1),
        ])
        self.install_hcloud(fake)
        code, _, _ = self.run_main(["--limit", "1"])
        self.assertEqual(code, 0)
        self.assertEqual(len(fake.calls), 2)

    def test_short_page_stops_even_if_total_is_larger(self):
        fake = FakeHcloud([
            group_page([GROUP_A], total=10, start=0, limit=100),
        ])
        self.install_hcloud(fake)
        code, out, _ = self.run_main([])
        self.assertEqual(code, 0)
        self.assertEqual(len(fake.calls), 1)
        self.assertIn("共 1 个伸缩组", out)

    def test_empty_first_page_stops(self):
        fake = FakeHcloud([group_page([], total=0, start=0, limit=100)])
        self.install_hcloud(fake)
        code, out, _ = self.run_main([])
        self.assertEqual(code, 0)
        self.assertEqual(len(fake.calls), 1)
        self.assertIn("当前区域无伸缩组", out)

    def test_max_pages_cap(self):
        fake = FakeHcloud([
            group_page([GROUP_A], total=999, start=0, limit=1),
            group_page([GROUP_B], total=999, start=1, limit=1),
            group_page([GROUP_C], total=999, start=2, limit=1),
        ])
        self.install_hcloud(fake)
        code, _, _ = self.run_main(["--limit", "1", "--max-pages", "2"])
        self.assertEqual(code, 0)
        self.assertEqual(len(fake.calls), 2)

    def test_duplicate_items_deduped(self):
        fake = FakeHcloud([
            group_page([GROUP_A, GROUP_B], total=3, start=0, limit=2),
            group_page([GROUP_A, GROUP_C], total=3, start=2, limit=2),
        ])
        self.install_hcloud(fake)
        code, out, _ = self.run_main(["--limit", "2"])
        self.assertEqual(code, 0)
        self.assertEqual(len(fake.calls), 2)
        self.assertIn("共 3 个伸缩组", out)

    def test_instance_pagination(self):
        fake = FakeHcloud([
            instance_page([INST_A], total=2, start=0, limit=1),
            instance_page([INST_B], total=2, start=1, limit=1),
        ])
        self.install_hcloud(fake)
        code, out, _ = self.run_main(
            ["--group-id", GROUP_A["scaling_group_id"], "--limit", "1"])
        self.assertEqual(code, 0)
        self.assertEqual(len(fake.calls), 2)
        self.assertIn("共 2 个实例", out)


class TestWriteGuard(Base):
    def test_action_delete_rejected(self):
        fake = FakeHcloud([group_page([GROUP_A])])
        self.install_hcloud(fake)
        code, _, err = self.run_main(["--action", "delete"])
        self.assertEqual(code, 1)
        self.assertIn("只读", err)
        self.assertEqual(fake.calls, [])

    def test_name_with_create_token_rejected(self):
        fake = FakeHcloud([group_page([GROUP_A])])
        self.install_hcloud(fake)
        code, _, err = self.run_main(["--name", "create-me"])
        self.assertEqual(code, 1)
        self.assertIn("--name", err)
        self.assertEqual(fake.calls, [])

    def test_group_id_with_delete_token_rejected(self):
        fake = FakeHcloud([instance_page([INST_A])])
        self.install_hcloud(fake)
        code, _, err = self.run_main(["--group-id", "delete-1234"])
        self.assertEqual(code, 1)
        self.assertIn("--group-id", err)
        self.assertEqual(fake.calls, [])

    def test_write_flag_rejected(self):
        fake = FakeHcloud([group_page([GROUP_A])])
        self.install_hcloud(fake)
        code, _, err = self.run_main(["--create-group"])
        self.assertEqual(code, 1)
        self.assertIn("写操作参数", err)
        self.assertEqual(fake.calls, [])

    def test_operation_whitelist(self):
        fake = FakeHcloud([group_page([GROUP_A])])
        self.install_hcloud(fake)
        code, _, err = self.run_main(
            ["--operation", "DeleteScalingGroup"])
        self.assertEqual(code, 1)
        self.assertIn("ListScalingGroups", err)
        self.assertEqual(fake.calls, [])

    def test_deleting_status_is_not_blocked(self):
        fake = FakeHcloud([group_page([dict(GROUP_A,
                                            scaling_group_status="DELETING")])])
        self.install_hcloud(fake)
        code, out, _ = self.run_main(["--status", "DELETING"])
        self.assertEqual(code, 0)
        self.assertIn("web-prod", out)
        self.assertTrue(fake.calls)


class TestLimits(Base):
    def test_limit_zero_rejected(self):
        code, _, err = self.run_main(["--limit", "0"])
        self.assertEqual(code, 1)
        self.assertIn("--limit", err)

    def test_limit_too_large_rejected(self):
        code, _, err = self.run_main(["--limit", "101"])
        self.assertEqual(code, 1)
        self.assertIn("--limit", err)

    def test_max_pages_zero_rejected(self):
        code, _, err = self.run_main(["--max-pages", "0"])
        self.assertEqual(code, 1)
        self.assertIn("--max-pages", err)

    def test_timeout_zero_rejected(self):
        code, _, err = self.run_main(["--timeout", "0"])
        self.assertEqual(code, 1)
        self.assertIn("--timeout", err)


class TestNormalization(Base):
    def test_group_fields_and_missing_values(self):
        groups = as_groups.normalize_groups(
            [group_page([GROUP_A, GROUP_C])], "cn-north-4")
        self.assertEqual(groups[0]["subnet_ids"], ["subnet-1111", "subnet-2222"])
        self.assertEqual(groups[0]["elb_ids"], ["elb-1111"])
        self.assertEqual(groups[0]["desire"], 2)
        self.assertEqual(groups[0]["current"], 2)
        self.assertEqual(groups[1]["subnet_ids"], [])
        self.assertEqual(groups[1]["elb_ids"], [])
        self.assertEqual(groups[1]["region"], "cn-north-4")

    def test_group_row_renders_dash_for_missing(self):
        group = as_groups.normalize_groups([group_page([GROUP_C])],
                                           "cn-north-4")[0]
        row = as_groups.group_row(group)
        self.assertEqual(row[6], "-")
        self.assertEqual(row[7], "-")
        self.assertEqual(row[8], "-")

    def test_instance_fields(self):
        instances = as_groups.normalize_instances(
            [instance_page([INST_A])], "cn-north-4",
            GROUP_A["scaling_group_id"])
        self.assertEqual(instances[0]["instance_id"], INST_A["instance_id"])
        self.assertEqual(instances[0]["group_name"], GROUP_A["scaling_group_name"])
        self.assertEqual(instances[0]["life_cycle_state"], "INSERVICE")
        self.assertEqual(instances[0]["health_status"], "NORMAL")

    def test_abnormal_predicates(self):
        self.assertFalse(as_groups.group_is_abnormal(
            {"status": "INSERVICE", "desire": 2, "current": 2}))
        self.assertTrue(as_groups.group_is_abnormal(
            {"status": "INSERVICE", "desire": 2, "current": 1}))
        self.assertTrue(as_groups.group_is_abnormal(
            {"status": "ERROR", "desire": 1, "current": 1}))
        self.assertFalse(as_groups.instance_is_abnormal(
            {"life_cycle_state": "INSERVICE", "health_status": "NORMAL"}))
        self.assertTrue(as_groups.instance_is_abnormal(
            {"life_cycle_state": "PENDING", "health_status": "NORMAL"}))
        self.assertTrue(as_groups.instance_is_abnormal(
            {"life_cycle_state": "INSERVICE", "health_status": "ERROR"}))

    def test_json_parsing_tolerates_diagnostics(self):
        text = ('{"total_number": 0}\n'
                'Failed to get terminal width. The default width will be used.\n')
        data = as_groups.parse_hcloud_json(text)
        self.assertEqual(data, {"total_number": 0})

    def test_json_parsing_tolerates_leading_diagnostics(self):
        text = 'some banner\n{"total_number": 1}\n'
        data = as_groups.parse_hcloud_json(text)
        self.assertEqual(data, {"total_number": 1})

    def test_json_parsing_garbage_returns_none(self):
        self.assertIsNone(as_groups.parse_hcloud_json("not json at all"))


class TestHcloudProcess(Base):
    def write_mock(self, stdout, stderr="", exit_code=0):
        directory = tempfile.mkdtemp()
        path = os.path.join(directory, "mock-hcloud")
        body = "#!/bin/sh\ncat <<'EOF'\n{0}\nEOF\ncat >&2 <<'EOF2'\n{1}\nEOF2\nexit {2}\n".format(
            stdout, stderr, exit_code)
        with open(path, "w") as handle:
            handle.write(body)
        os.chmod(path, os.stat(path).st_mode | stat.S_IEXEC)
        return path

    def test_error_body_with_exit_zero_is_classified(self):
        path = self.write_mock(
            '{"error":{"code":"AS.0031","message":"not authorized to perform: '
            'as:scalingGroup:list"}}',
            "Failed to get terminal width.")
        os.environ["HUAWEI_CLOUD_AS_GROUP_LIST_HCLOUD_BIN"] = path
        with self.assertRaises(as_groups.AsError) as ctx:
            as_groups.run_hcloud(["AS", "ListScalingGroups"])
        self.assertEqual(ctx.exception.kind, "forbidden")
        self.assertIn("as:scalingGroup:list", ctx.exception.message)

    def test_success_with_trailing_diagnostics(self):
        path = self.write_mock(
            '{"total_number":0,"start_number":0,"limit":100,'
            '"scaling_groups":[]}',
            "Failed to get terminal width.")
        os.environ["HUAWEI_CLOUD_AS_GROUP_LIST_HCLOUD_BIN"] = path
        body = as_groups.run_hcloud(["AS", "ListScalingGroups"])
        self.assertEqual(body["total_number"], 0)

    def test_nonzero_exit_with_credential_error(self):
        path = self.write_mock("", "no valid authentication, configure AK/SK",
                               exit_code=1)
        os.environ["HUAWEI_CLOUD_AS_GROUP_LIST_HCLOUD_BIN"] = path
        with self.assertRaises(as_groups.AsError) as ctx:
            as_groups.run_hcloud(["AS", "ListScalingGroups"])
        self.assertEqual(ctx.exception.kind, "credentials")

    def test_use_error_with_exit_zero(self):
        path = self.write_mock("[USE_ERROR]--limit invalid")
        os.environ["HUAWEI_CLOUD_AS_GROUP_LIST_HCLOUD_BIN"] = path
        with self.assertRaises(as_groups.AsError) as ctx:
            as_groups.run_hcloud(["AS", "ListScalingGroups"])
        self.assertEqual(ctx.exception.kind, "use_error")


if __name__ == "__main__":
    unittest.main()