import json
import os
import sys
import tempfile
import unittest
import urllib.error
from unittest import mock

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from list_ecs import (  # noqa: E402
    ApiError,
    AuthError,
    ConfigError,
    DEFAULT_REGION,
    EcsListError,
    PAGE_LIMIT,
    _has_more,
    list_ecs,
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
        url = "https://ecs.cn-north-4.myhuaweicloud.com/v1/p1/cloudservers/detail?limit=1000&offset=1"
        headers = {
            "content-type": "application/json",
            "host": "ecs.cn-north-4.myhuaweicloud.com",
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
        url = "https://ecs.cn-north-4.myhuaweicloud.com/v1/p1/cloudservers/detail?limit=1000&offset=1"
        headers = {
            "content-type": "application/json",
            "host": "ecs.cn-north-4.myhuaweicloud.com",
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
        url = "https://ecs.cn-north-4.myhuaweicloud.com/v1/p1/cloudservers/detail"
        headers = {
            "content-type": "application/json",
            "host": "ecs.cn-north-4.myhuaweicloud.com",
            "x-sdk-date": "20240101T000000Z",
        }
        empty_payload_hash = _hashlib.sha256(b"").hexdigest()
        canonical_request = (
            "GET\n"
            "/v1/p1/cloudservers/detail/\n"
            "\n"
            "content-type:application/json\n"
            "host:ecs.cn-north-4.myhuaweicloud.com\n"
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
        """黄金向量：与官方 huaweicloudsdkcore Signer 算法一致（IAM 向量与 vpc-list 交叉验证一致）。"""
        ak, sk = "AKIDEXAMPLE", "SKIDEXAMPLE"
        cases = [
            (
                "https://ecs.cn-north-4.myhuaweicloud.com/v1/p1/cloudservers/detail?limit=1000&offset=1",
                "ecs.cn-north-4.myhuaweicloud.com",
                "SDK-HMAC-SHA256 Access=AKIDEXAMPLE, "
                "SignedHeaders=content-type;host;x-sdk-date, "
                "Signature=dc19a921e6150d37d736fc8a81472e058be72391565ed9003a74a3e99a560fc5",
            ),
            (
                "https://ecs.cn-north-4.myhuaweicloud.com/v1/p1/cloudservers/detail?limit=1000&offset=2",
                "ecs.cn-north-4.myhuaweicloud.com",
                "SDK-HMAC-SHA256 Access=AKIDEXAMPLE, "
                "SignedHeaders=content-type;host;x-sdk-date, "
                "Signature=e7aeef5e7cbb2d40f79c95fdd0be8b7410ef97bda0d1185da637669de94e4ced",
            ),
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
        url = "https://ecs.cn-north-4.myhuaweicloud.com/v1/p1/cloudservers/detail"
        headers = {
            "x-sdk-date": "20240101T000000Z",
            "host": "ecs.cn-north-4.myhuaweicloud.com",
            "content-type": "application/json",
        }
        a = sign_request("ak1", "sk1", "GET", url, headers)
        self.assertIn(
            "SignedHeaders=content-type;host;x-sdk-date", a
        )


class TestResolveProjectId(unittest.TestCase):
    def test_use_provided_project_id(self):
        with mock.patch("list_ecs._http_request") as m:
            pid = resolve_project_id("ak", "sk", "cn-north-4", "proj-1")
            self.assertEqual(pid, "proj-1")
            m.assert_not_called()

    def test_resolve_via_iam(self):
        fake = FakeUrlopen(
            {"iam.myhuaweicloud.com": {"projects": [{"id": "proj-iam"}]}}
        )
        with mock.patch("list_ecs.urllib.request.urlopen", fake):
            pid = resolve_project_id("ak", "sk", "cn-north-4")
            self.assertEqual(pid, "proj-iam")
        self.assertTrue(any("iam.myhuaweicloud.com" in c for c in fake.calls))
        self.assertTrue(any("name=cn-north-4" in c for c in fake.calls))

    def test_resolve_via_iam_no_project(self):
        fake = FakeUrlopen({"iam.myhuaweicloud.com": {"projects": []}})
        with mock.patch("list_ecs.urllib.request.urlopen", fake):
            with self.assertRaises(ApiError):
                resolve_project_id("ak", "sk", "cn-north-4")


class TestHasMore(unittest.TestCase):
    def test_has_more_when_below_total(self):
        self.assertTrue(_has_more(10, 0, 2))

    def test_no_more_when_reached_total(self):
        self.assertFalse(_has_more(3, 3, 3))

    def test_no_more_when_empty_batch(self):
        self.assertFalse(_has_more(10, 0, 0))

    def test_no_more_when_total_zero(self):
        self.assertFalse(_has_more(0, 0, int(PAGE_LIMIT)))

    def test_has_more_when_collected_below_total_with_partial_page(self):
        """count 权威：已收集未达 count 即便本页非满页也继续翻页。"""
        self.assertTrue(_has_more(10, 3, 3))


class TestListEcs(unittest.TestCase):
    def test_list_ecs_success_with_pagination(self):
        """offset 分页：第一页满页且有 count，第二页收尾不满，停止翻页。"""

        def paged(request, *args, **kwargs):
            if "offset=2" in request.full_url:
                return make_response(
                    {
                        "count": 3,
                        "servers": [
                            {"id": "ecs-3", "name": "my-ecs-03"}
                        ],
                    }
                )
            return make_response(
                {
                    "count": 3,
                    "servers": [
                        {"id": "ecs-1", "name": "my-ecs-01"},
                        {"id": "ecs-2", "name": "my-ecs-02"},
                    ],
                }
            )

        with mock.patch("list_ecs.urllib.request.urlopen", paged):
            result = list_ecs("ak", "sk", "cn-north-4", "proj-1")
        self.assertEqual(
            result,
            [
                {"name": "my-ecs-01", "id": "ecs-1"},
                {"name": "my-ecs-02", "id": "ecs-2"},
                {"name": "my-ecs-03", "id": "ecs-3"},
            ],
        )

    def test_list_ecs_stops_when_count_reached(self):
        """第一页就收集到 count 总数时停止翻页（不再请求 offset=2）。"""
        fake = FakeUrlopen(
            {
                "ecs.cn-north-4.myhuaweicloud.com/v1/proj-1/cloudservers/detail": {
                    "count": 2,
                    "servers": [
                        {"id": "ecs-1", "name": "my-ecs-01"},
                        {"id": "ecs-2", "name": "my-ecs-02"},
                    ],
                }
            }
        )
        with mock.patch("list_ecs.urllib.request.urlopen", fake):
            result = list_ecs("ak", "sk", "cn-north-4", "proj-1")
        self.assertEqual(
            result,
            [
                {"name": "my-ecs-01", "id": "ecs-1"},
                {"name": "my-ecs-02", "id": "ecs-2"},
            ],
        )
        self.assertFalse(any("offset=2" in c for c in fake.calls))

    def test_list_ecs_empty(self):
        fake = FakeUrlopen(
            {"ecs.cn-north-4.myhuaweicloud.com/v1/proj-1/cloudservers/detail": {"count": 0, "servers": []}}
        )
        with mock.patch("list_ecs.urllib.request.urlopen", fake):
            result = list_ecs("ak", "sk", "cn-north-4", "proj-1")
        self.assertEqual(result, [])

    def test_list_ecs_skips_missing_id(self):
        fake = FakeUrlopen(
            {
                "ecs.cn-north-4.myhuaweicloud.com/v1/proj-1/cloudservers/detail": {
                    "count": 1,
                    "servers": [
                        {"id": "ecs-1", "name": "ok"},
                        {"name": "no-id"},
                    ],
                }
            }
        )
        with mock.patch("list_ecs.urllib.request.urlopen", fake):
            result = list_ecs("ak", "sk", "cn-north-4", "proj-1")
        self.assertEqual(result, [{"name": "ok", "id": "ecs-1"}])

    def test_list_ecs_passes_offset_param(self):
        """验证请求 URL 中包含 limit 与 offset 查询参数。"""
        fake = FakeUrlopen(
            {
                "ecs.cn-north-4.myhuaweicloud.com/v1/proj-1/cloudservers/detail": {
                    "count": 1,
                    "servers": [{"id": "ecs-1", "name": "my-ecs"}]
                }
            }
        )
        with mock.patch("list_ecs.urllib.request.urlopen", fake):
            list_ecs("ak", "sk", "cn-north-4", "proj-1")
        self.assertTrue(
            any("offset=1" in c and "limit=1000" in c for c in fake.calls),
            f"offset/limit 参数未出现在请求 URL: {fake.calls}",
        )

    def test_list_ecs_auth_error(self):
        def raiser(request, *args, **kwargs):
            raise urllib.error.HTTPError(
                url=request.full_url,
                code=401,
                msg="Unauthorized",
                hdrs={},
                fp=None,
            )

        with mock.patch("list_ecs.urllib.request.urlopen", raiser):
            with self.assertRaises(AuthError):
                list_ecs("ak", "sk", "cn-north-4", "proj-1")

    def test_list_ecs_api_error(self):
        def raiser(request, *args, **kwargs):
            raise urllib.error.HTTPError(
                url=request.full_url,
                code=500,
                msg="Server Error",
                hdrs={},
                fp=None,
            )

        with mock.patch("list_ecs.urllib.request.urlopen", raiser):
            with self.assertRaises(ApiError):
                list_ecs("ak", "sk", "cn-north-4", "proj-1")

    def test_list_ecs_network_error(self):
        def raiser(request, *args, **kwargs):
            raise urllib.error.URLError("connection refused")

        with mock.patch("list_ecs.urllib.request.urlopen", raiser):
            with self.assertRaises(ApiError):
                list_ecs("ak", "sk", "cn-north-4", "proj-1")

    def test_list_ecs_non_json_response(self):
        def not_json(request, *args, **kwargs):
            body = "<html>Internal Server Error</html>".encode("utf-8")
            response = mock.Mock()
            response.read.return_value = body
            response.__enter__ = mock.Mock(return_value=response)
            response.__exit__ = mock.Mock(return_value=False)
            return response

        with mock.patch("list_ecs.urllib.request.urlopen", not_json):
            with self.assertRaises(ApiError):
                list_ecs("ak", "sk", "cn-north-4", "proj-1")

    def test_list_ecs_resolves_project_id(self):
        fake = FakeUrlopen(
            {
                "iam.myhuaweicloud.com": {
                    "projects": [{"id": "proj-iam"}]
                },
                "ecs.cn-north-4.myhuaweicloud.com/v1/proj-iam/cloudservers/detail": {
                    "count": 1,
                    "servers": [{"id": "ecs-1", "name": "my-ecs"}]
                },
            }
        )
        with mock.patch("list_ecs.urllib.request.urlopen", fake):
            result = list_ecs("ak", "sk", "cn-north-4")
        self.assertEqual(result, [{"name": "my-ecs", "id": "ecs-1"}])


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
                "ecs.cn-north-4.myhuaweicloud.com/v1/proj-1/cloudservers/detail": {
                    "count": 1,
                    "servers": [{"id": "ecs-1", "name": "my-ecs-01"}]
                },
            }
        )
        with mock.patch("list_ecs.urllib.request.urlopen", fake):
            with mock.patch(
                "sys.stdout"
            ) as stdout, mock.patch(
                "sys.stderr"
            ) as stderr:
                rc = main(["-c", self.config.name])
        self.assertEqual(rc, 0)
        out = stdout.write.call_args_list
        joined = "".join(c[0][0] for c in out)
        self.assertIn("my-ecs-01", joined)
        self.assertIn("ecs-1", joined)
        stderr.write.assert_not_called()

    def test_main_empty(self):
        fake = FakeUrlopen(
            {
                "iam.myhuaweicloud.com": {"projects": [{"id": "proj-1"}]},
                "ecs.cn-north-4.myhuaweicloud.com/v1/proj-1/cloudservers/detail": {
                    "count": 0,
                    "servers": []
                },
            }
        )
        with mock.patch("list_ecs.urllib.request.urlopen", fake):
            with mock.patch("sys.stdout") as stdout:
                rc = main(["-c", self.config.name])
        self.assertEqual(rc, 0)
        joined = "".join(c[0][0] for c in stdout.write.call_args_list)
        self.assertIn("暂无 ECS 实例", joined)

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

        with mock.patch("list_ecs.urllib.request.urlopen", raiser):
            with mock.patch("sys.stderr") as stderr:
                rc = main(["-c", self.config.name])
        self.assertEqual(rc, 1)
        joined = "".join(c[0][0] for c in stderr.write.call_args_list)
        self.assertIn("认证失败", joined)

    def test_main_region_override(self):
        fake = FakeUrlopen(
            {
                "iam.myhuaweicloud.com": {
                    "projects": [{"id": "proj-south"}]
                },
                "ecs.cn-south-1.myhuaweicloud.com/v1/proj-south/cloudservers/detail": {
                    "count": 1,
                    "servers": [{"id": "ecs-s", "name": "south-ecs"}]
                },
            }
        )
        with mock.patch("list_ecs.urllib.request.urlopen", fake):
            with mock.patch("sys.stdout") as stdout:
                rc = main(["-c", self.config.name, "-r", "cn-south-1"])
        self.assertEqual(rc, 0)
        joined = "".join(c[0][0] for c in stdout.write.call_args_list)
        self.assertIn("cn-south-1", joined)
        self.assertIn("south-ecs", joined)


if __name__ == "__main__":
    unittest.main()
