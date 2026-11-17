import json
import os
import sys
import tempfile
import unittest
import urllib.error
from unittest import mock

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from list_rds import (  # noqa: E402
    ApiError,
    AuthError,
    ConfigError,
    DEFAULT_REGION,
    PAGE_LIMIT,
    RdsListError,
    _extract_instance,
    _has_more,
    list_rds,
    load_config,
    main,
    resolve_project_id,
    sign_request,
)


def make_response(payload, status=200, url=None):
    body = json.dumps(payload).encode("utf-8")
    response = mock.Mock()
    response.read.return_value = body
    response.status = status
    response.url = url or "http://example.com"
    response.__enter__ = mock.Mock(return_value=response)
    response.__exit__ = mock.Mock(return_value=False)
    return response


class FakeUrlopen:
    """按 URL 分发响应的 urlopen 假实现。"""

    def __init__(self, routes):
        self.routes = routes
        self.calls = []

    def __call__(self, request, *args, **kwargs):
        self.calls.append(request.full_url)
        for key, payload in self.routes.items():
            if key in request.full_url:
                return make_response(payload)
        raise AssertionError(f"unexpected url: {request.full_url}")


class TestLoadConfig(unittest.TestCase):
    def test_load_config_ok(self):
        with tempfile.NamedTemporaryFile(
            "w", suffix=".json", delete=False
        ) as fh:
            json.dump(
                {"ak": "ak1", "sk": "sk1", "region": "cn-south-1"}, fh
            )
            path = fh.name
        try:
            cfg = load_config(path)
            self.assertEqual(cfg["ak"], "ak1")
            self.assertEqual(cfg["sk"], "sk1")
            self.assertEqual(cfg["region"], "cn-south-1")
            self.assertIsNone(cfg["project_id"])
        finally:
            os.unlink(path)

    def test_load_config_default_region(self):
        with tempfile.NamedTemporaryFile(
            "w", suffix=".json", delete=False
        ) as fh:
            json.dump({"ak": "ak1", "sk": "sk1"}, fh)
            path = fh.name
        try:
            cfg = load_config(path)
            self.assertEqual(cfg["region"], DEFAULT_REGION)
        finally:
            os.unlink(path)

    def test_load_config_missing_file(self):
        with self.assertRaises(ConfigError):
            load_config("/no/such/config.json")

    def test_load_config_missing_ak_sk(self):
        with tempfile.NamedTemporaryFile(
            "w", suffix=".json", delete=False
        ) as fh:
            json.dump({"ak": "", "sk": ""}, fh)
            path = fh.name
        try:
            with self.assertRaises(ConfigError):
                load_config(path)
        finally:
            os.unlink(path)

    def test_load_config_bad_json(self):
        with tempfile.NamedTemporaryFile(
            "w", suffix=".json", delete=False
        ) as fh:
            fh.write("{not json")
            path = fh.name
        try:
            with self.assertRaises(ConfigError):
                load_config(path)
        finally:
            os.unlink(path)


class TestSignRequest(unittest.TestCase):
    def test_sign_request_deterministic(self):
        url = "https://rds.cn-north-4.myhuaweicloud.com/v3/p1/instances?limit=100&offset=0"
        headers = {
            "content-type": "application/json",
            "host": "rds.cn-north-4.myhuaweicloud.com",
            "x-sdk-date": "20240101T000000Z",
        }
        a1 = sign_request("ak1", "sk1", "GET", url, headers)
        a2 = sign_request("ak1", "sk1", "GET", url, headers)
        self.assertEqual(a1, a2)
        self.assertTrue(a1.startswith("SDK-HMAC-SHA256 Access=ak1, SignedHeaders="))
        self.assertIn("content-type", a1)
        self.assertIn("host", a1)
        self.assertIn("x-sdk-date", a1)
        self.assertIn("Signature=", a1)

    def test_sign_request_differs_by_sk(self):
        url = "https://rds.cn-north-4.myhuaweicloud.com/v3/p1/instances?limit=100&offset=0"
        headers = {
            "content-type": "application/json",
            "host": "rds.cn-north-4.myhuaweicloud.com",
            "x-sdk-date": "20240101T000000Z",
        }
        a1 = sign_request("ak1", "sk1", "GET", url, headers)
        a2 = sign_request("ak1", "sk2", "GET", url, headers)
        self.assertNotEqual(a1, a2)

    def test_sign_request_matches_manual_spec(self):
        """独立按华为云 SDK-HMAC-SHA256 规范（含 payload hash、URI 以 / 结尾）手工计算签名。"""
        import hashlib as _hashlib
        import hmac as _hmac

        ak, sk = "ak1", "sk1"
        url = "https://rds.cn-north-4.myhuaweicloud.com/v3/p1/instances"
        headers = {
            "content-type": "application/json",
            "host": "rds.cn-north-4.myhuaweicloud.com",
            "x-sdk-date": "20240101T000000Z",
        }
        empty_payload_hash = _hashlib.sha256(b"").hexdigest()
        canonical_request = (
            "GET\n"
            "/v3/p1/instances/\n"
            "\n"
            "content-type:application/json\n"
            "host:rds.cn-north-4.myhuaweicloud.com\n"
            "x-sdk-date:20240101T000000Z\n"
            "\n"
            "content-type;host;x-sdk-date\n"
            + empty_payload_hash
        )
        string_to_sign = (
            "SDK-HMAC-SHA256\n"
            "20240101T000000Z\n"
            + _hashlib.sha256(canonical_request.encode()).hexdigest()
        )
        expected = _hmac.new(
            b"sk1", string_to_sign.encode(), _hashlib.sha256
        ).hexdigest()
        auth = sign_request(ak, sk, "GET", url, headers)
        self.assertIn(f"Signature={expected}", auth)

    def test_sign_request_golden_vector_official_sdk(self):
        """黄金向量：签名代码与 huaweicloud-vpc-list 完全一致（后者已由官方
        huaweicloudsdkcore 3.1.210 Signer 校验）。IAM URL 签名与 vpc-list
        黄金向量完全相同，证明签名实现一致；RDS URL 为同算法在新端点上的向量。"""
        ak, sk = "AKIDEXAMPLE", "SKIDEXAMPLE"
        cases = [
            (
                "https://rds.cn-north-4.myhuaweicloud.com/v3/p1/instances?limit=100&offset=0",
                "rds.cn-north-4.myhuaweicloud.com",
                "SDK-HMAC-SHA256 Access=AKIDEXAMPLE, "
                "SignedHeaders=content-type;host;x-sdk-date, "
                "Signature=bd12ae6642e218656f5b07e1ac6ea2832018f23bf4903c8943eb4ec6d11635be",
            ),
            (
                "https://rds.cn-north-4.myhuaweicloud.com/v3/p1/instances?limit=100&offset=100",
                "rds.cn-north-4.myhuaweicloud.com",
                "SDK-HMAC-SHA256 Access=AKIDEXAMPLE, "
                "SignedHeaders=content-type;host;x-sdk-date, "
                "Signature=24c521500f73bc9c95a2f4013eb7f17ba7977f765475730a7a7049ac92a69feb",
            ),
            # IAM URL 黄金向量 —— 与 huaweicloud-vpc-list 官方 SDK 向量完全一致
            (
                "https://iam.myhuaweicloud.com/v3/projects?name=cn-north-4",
                "iam.myhuaweicloud.com",
                "SDK-HMAC-SHA256 Access=AKIDEXAMPLE, "
                "SignedHeaders=content-type;host;x-sdk-date, "
                "Signature=082a751eb6d1962783e5ba968ffdeeaea9fd9f9d286a989ae66b40dd731a1b37",
            ),
        ]
        for url, host, expected in cases:
            headers = {
                "content-type": "application/json",
                "host": host,
                "x-sdk-date": "20240101T000000Z",
            }
            self.assertEqual(sign_request(ak, sk, "GET", url, headers), expected)

    def test_sign_request_canonical_headers_sorted(self):
        url = "https://rds.cn-north-4.myhuaweicloud.com/v3/p1/instances"
        headers = {
            "x-sdk-date": "20240101T000000Z",
            "host": "rds.cn-north-4.myhuaweicloud.com",
            "content-type": "application/json",
        }
        a = sign_request("ak1", "sk1", "GET", url, headers)
        self.assertIn("SignedHeaders=content-type;host;x-sdk-date", a)


class TestResolveProjectId(unittest.TestCase):
    def test_use_provided_project_id(self):
        with mock.patch("list_rds._http_request") as m:
            pid = resolve_project_id("ak", "sk", "cn-north-4", "proj-1")
            self.assertEqual(pid, "proj-1")
            m.assert_not_called()

    def test_resolve_via_iam(self):
        fake = FakeUrlopen(
            {"iam.myhuaweicloud.com": {"projects": [{"id": "proj-iam"}]}}
        )
        with mock.patch("list_rds.urllib.request.urlopen", fake):
            pid = resolve_project_id("ak", "sk", "cn-north-4")
            self.assertEqual(pid, "proj-iam")
        self.assertTrue(any("iam.myhuaweicloud.com" in c for c in fake.calls))
        self.assertTrue(any("name=cn-north-4" in c for c in fake.calls))

    def test_resolve_via_iam_no_project(self):
        fake = FakeUrlopen({"iam.myhuaweicloud.com": {"projects": []}})
        with mock.patch("list_rds.urllib.request.urlopen", fake):
            with self.assertRaises(ApiError):
                resolve_project_id("ak", "sk", "cn-north-4")


class TestHasMore(unittest.TestCase):
    def test_has_more_when_collected_below_total(self):
        self.assertTrue(_has_more(10, 5, 5))

    def test_no_more_when_collected_reaches_total(self):
        self.assertFalse(_has_more(10, 10, 10))

    def test_no_more_when_total_zero(self):
        self.assertFalse(_has_more(0, 0, 0))

    def test_no_more_when_empty_batch(self):
        self.assertFalse(_has_more(10, 5, 0))


class TestExtractInstance(unittest.TestCase):
    def test_extract_full_fields(self):
        inst = {
            "id": "rds-1",
            "name": "my-rds",
            "status": "ACTIVE",
            "datastore": {"type": "MySQL", "version": "8.0"},
            "flavor_ref": "rds.mysql.c2.large.4",
        }
        result = _extract_instance(inst)
        self.assertEqual(result["name"], "my-rds")
        self.assertEqual(result["id"], "rds-1")
        self.assertEqual(result["status"], "ACTIVE")
        self.assertEqual(result["engine"], "MySQL")
        self.assertEqual(result["spec"], "rds.mysql.c2.large.4")

    def test_extract_missing_datastore(self):
        inst = {"id": "rds-1", "name": "my-rds", "status": "BUILD"}
        result = _extract_instance(inst)
        self.assertEqual(result["engine"], "")
        self.assertEqual(result["spec"], "")

    def test_extract_empty_instance(self):
        result = _extract_instance({})
        self.assertEqual(result["name"], "")
        self.assertEqual(result["id"], "")
        self.assertEqual(result["status"], "")
        self.assertEqual(result["engine"], "")
        self.assertEqual(result["spec"], "")


class TestListRds(unittest.TestCase):
    def test_list_rds_success_with_pagination(self):
        """分页走 offset（0 开始，按 limit=100 步进），直到收集到 total_count。"""

        def paged(request, *args, **kwargs):
            if "offset=100" in request.full_url:
                return make_response(
                    {
                        "instances": [
                            {
                                "id": "rds-3",
                                "name": "my-rds-03",
                                "status": "ACTIVE",
                                "datastore": {"type": "PostgreSQL", "version": "12"},
                                "flavor_ref": "rds.pg.c2.large.4",
                            }
                        ],
                        "total_count": 3,
                    }
                )
            return make_response(
                {
                    "instances": [
                        {
                            "id": "rds-1",
                            "name": "my-rds-01",
                            "status": "ACTIVE",
                            "datastore": {"type": "MySQL", "version": "8.0"},
                            "flavor_ref": "rds.mysql.c2.large.4",
                        },
                        {
                            "id": "rds-2",
                            "name": "my-rds-02",
                            "status": "BUILD",
                            "datastore": {"type": "MySQL", "version": "8.0"},
                            "flavor_ref": "rds.mysql.c2.large.2",
                        },
                    ],
                    "total_count": 3,
                }
            )

        with mock.patch("list_rds.urllib.request.urlopen", paged):
            result = list_rds("ak", "sk", "cn-north-4", "proj-1")
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0]["name"], "my-rds-01")
        self.assertEqual(result[0]["engine"], "MySQL")
        self.assertEqual(result[0]["spec"], "rds.mysql.c2.large.4")
        self.assertEqual(result[2]["name"], "my-rds-03")
        self.assertEqual(result[2]["engine"], "PostgreSQL")

    def test_list_rds_stops_when_collected_reaches_total(self):
        """本页即收集到 total_count 时停止翻页，不再发第二次请求。"""
        fake = FakeUrlopen(
            {
                "rds.cn-north-4.myhuaweicloud.com/v3/proj-1/instances": {
                    "instances": [
                        {
                            "id": "rds-1",
                            "name": "my-rds-01",
                            "status": "ACTIVE",
                            "datastore": {"type": "MySQL"},
                            "flavor_ref": "rds.mysql.c2.large.4",
                        }
                    ],
                    "total_count": 1,
                }
            }
        )
        with mock.patch("list_rds.urllib.request.urlopen", fake):
            result = list_rds("ak", "sk", "cn-north-4", "proj-1")
        self.assertEqual(len(result), 1)
        self.assertEqual(len(fake.calls), 1)

    def test_list_rds_empty(self):
        fake = FakeUrlopen(
            {"rds.cn-north-4.myhuaweicloud.com/v3/proj-1/instances": {"instances": [], "total_count": 0}}
        )
        with mock.patch("list_rds.urllib.request.urlopen", fake):
            result = list_rds("ak", "sk", "cn-north-4", "proj-1")
        self.assertEqual(result, [])

    def test_list_rds_skips_missing_id(self):
        fake = FakeUrlopen(
            {
                "rds.cn-north-4.myhuaweicloud.com/v3/proj-1/instances": {
                    "instances": [
                        {"id": "rds-1", "name": "ok", "status": "ACTIVE", "datastore": {"type": "MySQL"}},
                        {"name": "no-id"},
                    ],
                    "total_count": 1,
                }
            }
        )
        with mock.patch("list_rds.urllib.request.urlopen", fake):
            result = list_rds("ak", "sk", "cn-north-4", "proj-1")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["name"], "ok")

    def test_list_rds_auth_error(self):
        def raiser(request, *args, **kwargs):
            raise urllib.error.HTTPError(
                url=request.full_url,
                code=401,
                msg="Unauthorized",
                hdrs={},
                fp=None,
            )

        with mock.patch("list_rds.urllib.request.urlopen", raiser):
            with self.assertRaises(AuthError):
                list_rds("ak", "sk", "cn-north-4", "proj-1")

    def test_list_rds_api_error(self):
        def raiser(request, *args, **kwargs):
            raise urllib.error.HTTPError(
                url=request.full_url,
                code=500,
                msg="Server Error",
                hdrs={},
                fp=None,
            )

        with mock.patch("list_rds.urllib.request.urlopen", raiser):
            with self.assertRaises(ApiError):
                list_rds("ak", "sk", "cn-north-4", "proj-1")

    def test_list_rds_network_error(self):
        def raiser(request, *args, **kwargs):
            raise urllib.error.URLError("connection refused")

        with mock.patch("list_rds.urllib.request.urlopen", raiser):
            with self.assertRaises(ApiError):
                list_rds("ak", "sk", "cn-north-4", "proj-1")

    def test_list_rds_non_json_response(self):
        def not_json(request, *args, **kwargs):
            body = "<html>Internal Server Error</html>".encode("utf-8")
            response = mock.Mock()
            response.read.return_value = body
            response.__enter__ = mock.Mock(return_value=response)
            response.__exit__ = mock.Mock(return_value=False)
            return response

        with mock.patch("list_rds.urllib.request.urlopen", not_json):
            with self.assertRaises(ApiError):
                list_rds("ak", "sk", "cn-north-4", "proj-1")

    def test_list_rds_resolves_project_id(self):
        fake = FakeUrlopen(
            {
                "iam.myhuaweicloud.com": {"projects": [{"id": "proj-iam"}]},
                "rds.cn-north-4.myhuaweicloud.com/v3/proj-iam/instances": {
                    "instances": [
                        {"id": "rds-1", "name": "my-rds", "status": "ACTIVE", "datastore": {"type": "MySQL"}}
                    ],
                    "total_count": 1,
                },
            }
        )
        with mock.patch("list_rds.urllib.request.urlopen", fake):
            result = list_rds("ak", "sk", "cn-north-4")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["name"], "my-rds")


class TestMain(unittest.TestCase):
    def setUp(self):
        self.config = tempfile.NamedTemporaryFile(
            "w", suffix=".json", delete=False
        )
        json.dump({"ak": "ak1", "sk": "sk1"}, self.config)
        self.config.close()

    def tearDown(self):
        os.unlink(self.config.name)

    def test_main_success(self):
        fake = FakeUrlopen(
            {
                "iam.myhuaweicloud.com": {"projects": [{"id": "proj-1"}]},
                "rds.cn-north-4.myhuaweicloud.com/v3/proj-1/instances": {
                    "instances": [
                        {
                            "id": "rds-1",
                            "name": "my-rds-01",
                            "status": "ACTIVE",
                            "datastore": {"type": "MySQL"},
                            "flavor_ref": "rds.mysql.c2.large.4",
                        }
                    ],
                    "total_count": 1,
                },
            }
        )
        with mock.patch("list_rds.urllib.request.urlopen", fake):
            with mock.patch("sys.stdout") as stdout, mock.patch("sys.stderr") as stderr:
                rc = main(["-c", self.config.name])
        self.assertEqual(rc, 0)
        out = stdout.write.call_args_list
        joined = "".join(c[0][0] for c in out)
        self.assertIn("my-rds-01", joined)
        self.assertIn("rds-1", joined)
        self.assertIn("ACTIVE", joined)
        self.assertIn("MySQL", joined)
        self.assertIn("rds.mysql.c2.large.4", joined)
        stderr.write.assert_not_called()

    def test_main_empty(self):
        fake = FakeUrlopen(
            {
                "iam.myhuaweicloud.com": {"projects": [{"id": "proj-1"}]},
                "rds.cn-north-4.myhuaweicloud.com/v3/proj-1/instances": {
                    "instances": [],
                    "total_count": 0,
                },
            }
        )
        with mock.patch("list_rds.urllib.request.urlopen", fake):
            with mock.patch("sys.stdout") as stdout:
                rc = main(["-c", self.config.name])
        self.assertEqual(rc, 0)
        joined = "".join(c[0][0] for c in stdout.write.call_args_list)
        self.assertIn("暂无 RDS 实例", joined)

    def test_main_config_missing(self):
        with mock.patch("sys.stderr") as stderr:
            rc = main(["-c", "/no/such/config.json"])
        self.assertEqual(rc, 1)
        stderr.write.assert_called()

    def test_main_auth_error(self):
        def raiser(request, *args, **kwargs):
            raise urllib.error.HTTPError(
                url=request.full_url,
                code=403,
                msg="Forbidden",
                hdrs={},
                fp=None,
            )

        with mock.patch("list_rds.urllib.request.urlopen", raiser):
            with mock.patch("sys.stderr") as stderr:
                rc = main(["-c", self.config.name])
        self.assertEqual(rc, 1)
        joined = "".join(c[0][0] for c in stderr.write.call_args_list)
        self.assertIn("认证失败", joined)

    def test_main_region_override(self):
        fake = FakeUrlopen(
            {
                "iam.myhuaweicloud.com": {"projects": [{"id": "proj-south"}]},
                "rds.cn-south-1.myhuaweicloud.com/v3/proj-south/instances": {
                    "instances": [
                        {
                            "id": "rds-s",
                            "name": "south-rds",
                            "status": "ACTIVE",
                            "datastore": {"type": "PostgreSQL"},
                            "flavor_ref": "rds.pg.c2.large.4",
                        }
                    ],
                    "total_count": 1,
                },
            }
        )
        with mock.patch("list_rds.urllib.request.urlopen", fake):
            with mock.patch("sys.stdout") as stdout:
                rc = main(["-c", self.config.name, "-r", "cn-south-1"])
        self.assertEqual(rc, 0)
        joined = "".join(c[0][0] for c in stdout.write.call_args_list)
        self.assertIn("cn-south-1", joined)
        self.assertIn("south-rds", joined)


if __name__ == "__main__":
    unittest.main()
