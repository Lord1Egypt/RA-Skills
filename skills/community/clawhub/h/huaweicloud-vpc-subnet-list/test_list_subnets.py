import json
import os
import sys
import tempfile
import unittest
import urllib.error
from unittest import mock

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from list_subnets import (  # noqa: E402
    ApiError,
    AuthError,
    ConfigError,
    DEFAULT_REGION,
    SubnetListError,
    _extract_next_marker,
    list_subnets,
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
        url = "https://vpc.cn-north-4.myhuaweicloud.com/v1/p1/subnets?vpc_id=vpc-1&limit=1000"
        headers = {
            "content-type": "application/json",
            "host": "vpc.cn-north-4.myhuaweicloud.com",
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
        url = "https://vpc.cn-north-4.myhuaweicloud.com/v1/p1/subnets?vpc_id=vpc-1"
        headers = {
            "content-type": "application/json",
            "host": "vpc.cn-north-4.myhuaweicloud.com",
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
        url = "https://vpc.cn-north-4.myhuaweicloud.com/v1/p1/subnets"
        headers = {
            "content-type": "application/json",
            "host": "vpc.cn-north-4.myhuaweicloud.com",
            "x-sdk-date": "20240101T000000Z",
        }
        empty_payload_hash = _hashlib.sha256(b"").hexdigest()
        canonical_request = (
            "GET\n"
            "/v1/p1/subnets/\n"
            "\n"
            "content-type:application/json\n"
            "host:vpc.cn-north-4.myhuaweicloud.com\n"
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

    def test_sign_request_structure_with_vpc_id_query(self):
        """验证带 vpc_id 查询参数时签名结构正确（签名算法黄金向量已在 vpc-list 验证）。"""
        ak, sk = "AKIDEXAMPLE", "SKIDEXAMPLE"
        url = "https://vpc.cn-north-4.myhuaweicloud.com/v1/p1/subnets?vpc_id=vpc-1&limit=1000"
        headers = {
            "content-type": "application/json",
            "host": "vpc.cn-north-4.myhuaweicloud.com",
            "x-sdk-date": "20240101T000000Z",
        }
        auth = sign_request(ak, sk, "GET", url, headers)
        self.assertTrue(auth.startswith("SDK-HMAC-SHA256 Access=AKIDEXAMPLE,"))
        self.assertIn("SignedHeaders=content-type;host;x-sdk-date", auth)
        self.assertIn("Signature=", auth)
        # 同一 URL 两次签名一致（确定性）
        self.assertEqual(auth, sign_request(ak, sk, "GET", url, headers))

    def test_sign_request_canonical_headers_sorted(self):
        url = "https://vpc.cn-north-4.myhuaweicloud.com/v1/p1/subnets"
        headers = {
            "x-sdk-date": "20240101T000000Z",
            "host": "vpc.cn-north-4.myhuaweicloud.com",
            "content-type": "application/json",
        }
        a = sign_request("ak1", "sk1", "GET", url, headers)
        self.assertIn(
            "SignedHeaders=content-type;host;x-sdk-date", a
        )


class TestResolveProjectId(unittest.TestCase):
    def test_use_provided_project_id(self):
        with mock.patch("list_subnets._http_request") as m:
            pid = resolve_project_id("ak", "sk", "cn-north-4", "proj-1")
            self.assertEqual(pid, "proj-1")
            m.assert_not_called()

    def test_resolve_via_iam(self):
        fake = FakeUrlopen(
            {"iam.myhuaweicloud.com": {"projects": [{"id": "proj-iam"}]}}
        )
        with mock.patch("list_subnets.urllib.request.urlopen", fake):
            pid = resolve_project_id("ak", "sk", "cn-north-4")
            self.assertEqual(pid, "proj-iam")
        self.assertTrue(any("iam.myhuaweicloud.com" in c for c in fake.calls))
        self.assertTrue(any("name=cn-north-4" in c for c in fake.calls))

    def test_resolve_via_iam_no_project(self):
        fake = FakeUrlopen({"iam.myhuaweicloud.com": {"projects": []}})
        with mock.patch("list_subnets.urllib.request.urlopen", fake):
            with self.assertRaises(ApiError):
                resolve_project_id("ak", "sk", "cn-north-4")


class TestExtractNextMarker(unittest.TestCase):
    def test_extract_from_next_link(self):
        data = {
            "subnets_links": [
                {
                    "rel": "self",
                    "href": "https://vpc.cn-north-4.myhuaweicloud.com/v1/p1/subnets?vpc_id=vpc-1&limit=1000",
                },
                {
                    "rel": "next",
                    "href": "https://vpc.cn-north-4.myhuaweicloud.com/v1/p1/subnets?vpc_id=vpc-1&limit=1000&marker=sub-9",
                },
            ]
        }
        self.assertEqual(_extract_next_marker(data), "sub-9")

    def test_extract_none_when_no_next(self):
        self.assertIsNone(_extract_next_marker({}))
        self.assertIsNone(_extract_next_marker({"subnets_links": []}))
        self.assertIsNone(
            _extract_next_marker(
                {
                    "subnets_links": [
                        {
                            "rel": "self",
                            "href": "https://vpc.cn-north-4.myhuaweicloud.com/v1/p1/subnets",
                        }
                    ]
                }
            )
        )
        self.assertIsNone(
            _extract_next_marker(
                {
                    "subnets_links": [
                        {
                            "rel": "next",
                            "href": "https://vpc.cn-north-4.myhuaweicloud.com/v1/p1/subnets?limit=1000",
                        }
                    ]
                }
            )
        )


class TestListSubnets(unittest.TestCase):
    def test_list_subnets_success_with_pagination(self):
        """分页走 subnets_links（真实 API 响应格式）翻页，直到无 next 链接。"""

        def paged(request, *args, **kwargs):
            if "marker=sub-2" in request.full_url:
                return make_response(
                    {
                        "subnets": [
                            {"id": "sub-3", "name": "my-subnet-03", "vpc_id": "vpc-1"}
                        ],
                        "subnets_links": [
                            {
                                "rel": "self",
                                "href": "https://vpc.cn-north-4.myhuaweicloud.com"
                                "/v1/proj-1/subnets?vpc_id=vpc-1&limit=1000&marker=sub-2",
                            }
                        ],
                    }
                )
            return make_response(
                {
                    "subnets": [
                        {"id": "sub-1", "name": "my-subnet-01", "vpc_id": "vpc-1"},
                        {"id": "sub-2", "name": "my-subnet-02", "vpc_id": "vpc-1"},
                    ],
                    "subnets_links": [
                        {
                            "rel": "next",
                            "href": "https://vpc.cn-north-4.myhuaweicloud.com"
                            "/v1/proj-1/subnets?vpc_id=vpc-1&limit=1000&marker=sub-2",
                        }
                    ],
                }
            )

        with mock.patch("list_subnets.urllib.request.urlopen", paged):
            result = list_subnets("ak", "sk", "cn-north-4", "vpc-1", "proj-1")
        self.assertEqual(
            result,
            [
                {"name": "my-subnet-01", "id": "sub-1"},
                {"name": "my-subnet-02", "id": "sub-2"},
                {"name": "my-subnet-03", "id": "sub-3"},
            ],
        )

    def test_list_subnets_stops_without_next_link(self):
        """仅返回 self 链接（rel 不为 next）时停止翻页。"""
        fake = FakeUrlopen(
            {
                "vpc.cn-north-4.myhuaweicloud.com/v1/proj-1/subnets": {
                    "subnets": [{"id": "sub-1", "name": "my-subnet-01"}],
                    "subnets_links": [
                        {
                            "rel": "self",
                            "href": "https://vpc.cn-north-4.myhuaweicloud.com"
                            "/v1/proj-1/subnets?vpc_id=vpc-1&limit=1000",
                        }
                    ],
                }
            }
        )
        with mock.patch("list_subnets.urllib.request.urlopen", fake):
            result = list_subnets("ak", "sk", "cn-north-4", "vpc-1", "proj-1")
        self.assertEqual(result, [{"name": "my-subnet-01", "id": "sub-1"}])

    def test_list_subnets_empty(self):
        fake = FakeUrlopen(
            {"vpc.cn-north-4.myhuaweicloud.com/v1/proj-1/subnets": {"subnets": []}}
        )
        with mock.patch("list_subnets.urllib.request.urlopen", fake):
            result = list_subnets("ak", "sk", "cn-north-4", "vpc-1", "proj-1")
        self.assertEqual(result, [])

    def test_list_subnets_skips_missing_id(self):
        fake = FakeUrlopen(
            {
                "vpc.cn-north-4.myhuaweicloud.com/v1/proj-1/subnets": {
                    "subnets": [
                        {"id": "sub-1", "name": "ok"},
                        {"name": "no-id"},
                    ]
                }
            }
        )
        with mock.patch("list_subnets.urllib.request.urlopen", fake):
            result = list_subnets("ak", "sk", "cn-north-4", "vpc-1", "proj-1")
        self.assertEqual(result, [{"name": "ok", "id": "sub-1"}])

    def test_list_subnets_passes_vpc_id_param(self):
        """验证请求 URL 中包含 vpc_id 查询参数。"""
        fake = FakeUrlopen(
            {
                "vpc.cn-north-4.myhuaweicloud.com/v1/proj-1/subnets": {
                    "subnets": [{"id": "sub-1", "name": "my-subnet"}]
                }
            }
        )
        with mock.patch("list_subnets.urllib.request.urlopen", fake):
            list_subnets("ak", "sk", "cn-north-4", "vpc-target", "proj-1")
        self.assertTrue(
            any("vpc_id=vpc-target" in c for c in fake.calls),
            f"vpc_id 参数未出现在请求 URL: {fake.calls}",
        )

    def test_list_subnets_missing_vpc_id(self):
        with self.assertRaises(ConfigError):
            list_subnets("ak", "sk", "cn-north-4", "", "proj-1")

    def test_list_subnets_auth_error(self):
        def raiser(request, *args, **kwargs):
            raise urllib.error.HTTPError(
                url=request.full_url,
                code=401,
                msg="Unauthorized",
                hdrs={},
                fp=None,
            )

        with mock.patch("list_subnets.urllib.request.urlopen", raiser):
            with self.assertRaises(AuthError):
                list_subnets("ak", "sk", "cn-north-4", "vpc-1", "proj-1")

    def test_list_subnets_api_error(self):
        def raiser(request, *args, **kwargs):
            raise urllib.error.HTTPError(
                url=request.full_url,
                code=500,
                msg="Server Error",
                hdrs={},
                fp=None,
            )

        with mock.patch("list_subnets.urllib.request.urlopen", raiser):
            with self.assertRaises(ApiError):
                list_subnets("ak", "sk", "cn-north-4", "vpc-1", "proj-1")

    def test_list_subnets_network_error(self):
        def raiser(request, *args, **kwargs):
            raise urllib.error.URLError("connection refused")

        with mock.patch("list_subnets.urllib.request.urlopen", raiser):
            with self.assertRaises(ApiError):
                list_subnets("ak", "sk", "cn-north-4", "vpc-1", "proj-1")

    def test_list_subnets_non_json_response(self):
        def not_json(request, *args, **kwargs):
            body = "<html>Internal Server Error</html>".encode("utf-8")
            response = mock.Mock()
            response.read.return_value = body
            response.__enter__ = mock.Mock(return_value=response)
            response.__exit__ = mock.Mock(return_value=False)
            return response

        with mock.patch("list_subnets.urllib.request.urlopen", not_json):
            with self.assertRaises(ApiError):
                list_subnets("ak", "sk", "cn-north-4", "vpc-1", "proj-1")

    def test_list_subnets_resolves_project_id(self):
        fake = FakeUrlopen(
            {
                "iam.myhuaweicloud.com": {
                    "projects": [{"id": "proj-iam"}]
                },
                "vpc.cn-north-4.myhuaweicloud.com/v1/proj-iam/subnets": {
                    "subnets": [{"id": "sub-1", "name": "my-subnet"}]
                },
            }
        )
        with mock.patch("list_subnets.urllib.request.urlopen", fake):
            result = list_subnets("ak", "sk", "cn-north-4", "vpc-1")
        self.assertEqual(result, [{"name": "my-subnet", "id": "sub-1"}])


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
                "vpc.cn-north-4.myhuaweicloud.com/v1/proj-1/subnets": {
                    "subnets": [{"id": "sub-1", "name": "my-subnet-01"}]
                },
            }
        )
        with mock.patch("list_subnets.urllib.request.urlopen", fake):
            with mock.patch(
                "sys.stdout"
            ) as stdout, mock.patch(
                "sys.stderr"
            ) as stderr:
                rc = main(["-c", self.config.name, "-v", "vpc-1"])
        self.assertEqual(rc, 0)
        out = stdout.write.call_args_list
        joined = "".join(c[0][0] for c in out)
        self.assertIn("my-subnet-01", joined)
        self.assertIn("sub-1", joined)
        self.assertIn("vpc-1", joined)
        stderr.write.assert_not_called()

    def test_main_empty(self):
        fake = FakeUrlopen(
            {
                "iam.myhuaweicloud.com": {"projects": [{"id": "proj-1"}]},
                "vpc.cn-north-4.myhuaweicloud.com/v1/proj-1/subnets": {
                    "subnets": []
                },
            }
        )
        with mock.patch("list_subnets.urllib.request.urlopen", fake):
            with mock.patch("sys.stdout") as stdout:
                rc = main(["-c", self.config.name, "-v", "vpc-1"])
        self.assertEqual(rc, 0)
        joined = "".join(c[0][0] for c in stdout.write.call_args_list)
        self.assertIn("暂无子网", joined)

    def test_main_missing_vpc_id(self):
        with mock.patch("sys.stderr") as stderr:
            rc = main(["-c", self.config.name])
        self.assertEqual(rc, 1)
        joined = "".join(c[0][0] for c in stderr.write.call_args_list)
        self.assertIn("VPC ID", joined)

    def test_main_config_missing(self):
        with mock.patch("sys.stderr") as stderr:
            rc = main(["-c", "/no/such/config.json", "-v", "vpc-1"])
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

        with mock.patch("list_subnets.urllib.request.urlopen", raiser):
            with mock.patch("sys.stderr") as stderr:
                rc = main(["-c", self.config.name, "-v", "vpc-1"])
        self.assertEqual(rc, 1)
        joined = "".join(c[0][0] for c in stderr.write.call_args_list)
        self.assertIn("认证失败", joined)

    def test_main_region_override(self):
        fake = FakeUrlopen(
            {
                "iam.myhuaweicloud.com": {
                    "projects": [{"id": "proj-south"}]
                },
                "vpc.cn-south-1.myhuaweicloud.com/v1/proj-south/subnets": {
                    "subnets": [{"id": "sub-s", "name": "south-subnet"}]
                },
            }
        )
        with mock.patch("list_subnets.urllib.request.urlopen", fake):
            with mock.patch("sys.stdout") as stdout:
                rc = main(["-c", self.config.name, "-v", "vpc-1", "-r", "cn-south-1"])
        self.assertEqual(rc, 0)
        joined = "".join(c[0][0] for c in stdout.write.call_args_list)
        self.assertIn("cn-south-1", joined)
        self.assertIn("south-subnet", joined)


if __name__ == "__main__":
    unittest.main()
