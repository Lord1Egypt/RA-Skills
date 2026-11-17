#!/usr/bin/env python3
"""Unit tests for mopng_api.py"""

import io
import os
import sys
import unittest
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

# Add repo root and scripts to path: entry points resolve their sibling helpers
# (`_http`) on the scripts dir, tests patch third-party modules (urllib) as loaded.
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))
import mopng_api as api


class TestImageValidation(unittest.TestCase):
    """Test image validation functions"""
    
    def test_detect_png(self):
        """Test PNG format detection"""
        png_header = b"\x89PNG\r\n\x1a\n"
        self.assertEqual(api._detect_image_format(png_header), "png")
    
    def test_detect_jpeg(self):
        """Test JPEG format detection"""
        jpeg_header = b"\xff\xd8\xff\xe0\x00\x10JFIF"
        self.assertEqual(api._detect_image_format(jpeg_header), "jpeg")
    
    def test_detect_webp(self):
        """Test WEBP format detection"""
        webp_header = b"RIFF\x00\x00\x00\x00WEBPVP8 "
        self.assertEqual(api._detect_image_format(webp_header), "webp")
    
    def test_detect_unknown(self):
        """Test unknown format detection"""
        self.assertIsNone(api._detect_image_format(b"NOTANIMAGE"))


class TestPrepareOutputPath(unittest.TestCase):
    """Test _prepare_output_path relative / workspace rules"""

    def test_relative_file_goes_under_safe_root(self):
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp).resolve()
            safe = workspace / "outputs" / "mopng-api"
            safe.mkdir(parents=True)
            out = api._prepare_output_path("./cat.jpg", workspace, safe)
            self.assertEqual(out, safe / "cat.jpg")

    def test_outputs_prefix_from_workspace(self):
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp).resolve()
            safe = workspace / "outputs" / "mopng-api"
            safe.mkdir(parents=True)
            out = api._prepare_output_path(
                "outputs/mopng-api/nested.png", workspace, safe
            )
            self.assertEqual(out, safe / "nested.png")

    def test_absolute_under_safe_ok(self):
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp).resolve()
            safe = workspace / "outputs" / "mopng-api"
            safe.mkdir(parents=True)
            out = api._prepare_output_path(str(safe / "abs.png"), workspace, safe)
            self.assertEqual(out, safe / "abs.png")


class TestUrlValidation(unittest.TestCase):
    """User-supplied image URLs and result download URL checks"""

    def test_user_url_accepts_mopng_https(self):
        api._validate_user_image_url("https://cdn.mopng.cn/foo/bar.png")

    def test_user_url_rejects_non_https(self):
        with self.assertRaises(ValueError):
            api._validate_user_image_url("http://img.mopng.cn/x.png")

    def test_user_url_rejects_unknown_host(self):
        with self.assertRaises(ValueError):
            api._validate_user_image_url("https://evil.example/x.png")

    def test_user_url_rejects_credentials(self):
        with self.assertRaises(ValueError):
            api._validate_user_image_url("https://user:pass@img.mopng.cn/x.png")

    def test_download_rejects_private_ip(self):
        with self.assertRaises(ValueError):
            api._validate_result_download_url("https://127.0.0.1/s.png")

    def test_download_accepts_public_https(self):
        api._validate_result_download_url("https://cdn.example.com/out.png")


class TestWorkspaceUtils(unittest.TestCase):
    """Test workspace utilities"""
    
    def test_ensure_within_valid(self):
        """Test path within workspace"""
        root = Path("/workspace")
        path = Path("/workspace/subdir/file.txt")
        # Should not raise
        api._ensure_within(path, root, "test path")
    
    def test_ensure_within_invalid(self):
        """Test path outside workspace"""
        root = Path("/workspace")
        path = Path("/other/file.txt")
        with self.assertRaises(ValueError):
            api._ensure_within(path, root, "test path")

    def test_ensure_within_rejects_dotdot_escape(self):
        """A literal path under the root must not escape it via '..'."""
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp).resolve() / "ws"
            (root / "sub").mkdir(parents=True)
            escape = root / "sub" / ".." / ".." / "outside.txt"
            self.assertTrue(str(escape).startswith(str(root)))
            with self.assertRaises(ValueError):
                api._ensure_within(escape, root, "output path")

    def test_ensure_within_rejects_symlink_escape(self):
        """A path whose literal form is under root but resolves outside must fail."""
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp).resolve()
            root = base / "ws"
            root.mkdir()
            outside = base / "elsewhere"
            outside.mkdir()
            link = root / "link.png"
            link.symlink_to(outside / "evil.png")
            with self.assertRaises(ValueError):
                api._ensure_within(link, root, "output path")

    def test_ensure_within_accepts_normalized_path(self):
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp).resolve()
            (root / "sub").mkdir()
            api._ensure_within(root / "sub" / ".." / "ok.png", root, "output path")

    def test_workspace_root_uses_env(self):
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            with patch.dict(os.environ, {"OPENCLAW_WORKSPACE": tmp}):
                self.assertEqual(api._workspace_root(), Path(tmp).resolve())

    def test_workspace_root_defaults_to_checkout_not_cwd(self):
        """Without the env var the boundary must not follow the process CWD."""
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            old_cwd = os.getcwd()
            try:
                os.chdir(tmp)
                with patch.dict(os.environ, {}, clear=False):
                    os.environ.pop("OPENCLAW_WORKSPACE", None)
                    root = api._workspace_root()
                self.assertNotEqual(root, Path(tmp).resolve())
                self.assertEqual(root, Path(api.__file__).resolve().parent.parent)
            finally:
                os.chdir(old_cwd)


class TestApiBaseUrlConfig(unittest.TestCase):
    """BASE_URL / UPSCALE_URL have a single configurable default."""

    def _reload(self, **env):
        import importlib

        with patch.dict(os.environ, env, clear=False):
            for key in ("MOPNG_API_BASE_URL", "MOPNG_UPSCALE_BASE_URL"):
                if key not in env:
                    os.environ.pop(key, None)
            return importlib.reload(api)

    def tearDown(self):
        self._reload()

    def test_defaults_are_identical_and_trimmed(self):
        mod = self._reload()
        self.assertEqual(mod.BASE_URL, "https://mo-api.mopng.cn")
        self.assertEqual(mod.UPSCALE_URL, mod.BASE_URL)

    def test_env_overrides_base_url(self):
        mod = self._reload(MOPNG_API_BASE_URL="https://staging.example/")
        self.assertEqual(mod.BASE_URL, "https://staging.example")
        self.assertEqual(mod.UPSCALE_URL, "https://staging.example")

    def test_upscale_can_override_independently(self):
        mod = self._reload(
            MOPNG_API_BASE_URL="https://api.example",
            MOPNG_UPSCALE_BASE_URL="https://upscale.example/",
        )
        self.assertEqual(mod.BASE_URL, "https://api.example")
        self.assertEqual(mod.UPSCALE_URL, "https://upscale.example")


class TestAPIRequest(unittest.TestCase):
    """Test API request functionality"""
    
    @patch('mopng_api.request.urlopen')
    def test_api_request_success(self, mock_urlopen):
        """Test successful API request"""
        mock_response = MagicMock()
        mock_response.read.return_value = b'{"code": 0, "data": {"result": "ok"}}'
        mock_urlopen.return_value.__enter__.return_value = mock_response
        
        result = api._api_request("GET", "/test", "test_key")
        self.assertEqual(result["code"], 0)
    
    @patch('mopng_api.request.urlopen')
    def test_api_request_error(self, mock_urlopen):
        """Test API request error"""
        from urllib.error import HTTPError
        mock_urlopen.side_effect = HTTPError(
            "https://example.com", 400, "Bad Request", {}, None
        )
        
        with self.assertRaises(RuntimeError):
            api._api_request("GET", "/test", "test_key")

    @patch('mopng_api.request.urlopen')
    def test_api_request_network_error_is_runtime_error(self, mock_urlopen):
        """Network failures must surface as RuntimeError, not leak URLError."""
        from urllib.error import URLError
        mock_urlopen.side_effect = URLError("timed out")

        with self.assertRaises(RuntimeError) as ctx:
            api._api_request("GET", "/test", "test_key")
        self.assertIn("unavailable", str(ctx.exception))

    @patch('mopng_api.request.urlopen')
    def test_api_request_http_error_message_from_json(self, mock_urlopen):
        from urllib.error import HTTPError
        mock_urlopen.side_effect = HTTPError(
            "https://example.com", 400, "Bad Request", {},
            io.BytesIO(b'{"message": "invalid key"}'),
        )

        with self.assertRaises(RuntimeError) as ctx:
            api._api_request("GET", "/test", "test_key")
        self.assertEqual(str(ctx.exception), "MoPNG API API error: invalid key")

    @patch('mopng_api.request.urlopen')
    def test_api_request_http_error_non_json_body(self, mock_urlopen):
        from urllib.error import HTTPError
        mock_urlopen.side_effect = HTTPError(
            "https://example.com", 503, "Unavailable", {}, io.BytesIO(b"boom")
        )

        with self.assertRaises(RuntimeError) as ctx:
            api._api_request("GET", "/test", "test_key")
        self.assertEqual(str(ctx.exception), "MoPNG API HTTP 503: boom")

    @patch('mopng_api.request.urlopen')
    def test_api_request_non_json_success_body(self, mock_urlopen):
        mock_response = MagicMock()
        mock_response.read.return_value = b"<html>"
        mock_urlopen.return_value.__enter__.return_value = mock_response

        with self.assertRaises(RuntimeError) as ctx:
            api._api_request("GET", "/test", "test_key")
        self.assertIn("non-JSON", str(ctx.exception))

    @patch('mopng_api.request.urlopen')
    def test_api_request_sends_bearer_auth_to_given_base_url(self, mock_urlopen):
        mock_response = MagicMock()
        mock_response.read.return_value = b'{"code": 0}'
        mock_urlopen.return_value.__enter__.return_value = mock_response

        api._api_request("GET", "/test", "secret", base_url="https://alt.example")

        req = mock_urlopen.call_args.args[0]
        self.assertEqual(req.full_url, "https://alt.example/test")
        self.assertEqual(req.get_header("Authorization"), "Bearer secret")

    @patch('mopng_api.request.urlopen')
    def test_api_request_uploads_multipart_file(self, mock_urlopen):
        import tempfile

        mock_response = MagicMock()
        mock_response.read.return_value = b'{"code": 0}'
        mock_urlopen.return_value.__enter__.return_value = mock_response

        with tempfile.TemporaryDirectory() as tmp:
            image = Path(tmp) / "pic.png"
            image.write_bytes(b"PNGDATA")
            api._api_request("POST", "/upload", "k", files={"file": (image, b"PNGDATA")})

        req = mock_urlopen.call_args.args[0]
        self.assertTrue(req.get_header("Content-type").startswith("multipart/form-data"))
        self.assertIn(b'filename="pic.png"', req.data)


class TestPollTask(unittest.TestCase):
    """Test task polling functionality"""
    
    @patch('mopng_api._api_request')
    def test_poll_task_completed(self, mock_request):
        """Test polling until completed"""
        mock_request.return_value = {
            "data": {"status": "completed", "result": {"imageUrl": "https://example.com/img.png"}}
        }
        
        result = api._poll_task("/tasks", "task-123", "test_key", max_retries=1)
        self.assertEqual(result["status"], "completed")
    
    @patch('mopng_api._api_request')
    def test_poll_task_failed(self, mock_request):
        """Test polling task failed"""
        mock_request.return_value = {
            "data": {"status": "failed", "message": "Processing error"}
        }
        
        with self.assertRaises(RuntimeError) as ctx:
            api._poll_task("/tasks", "task-123", "test_key", max_retries=1, interval=0)
        self.assertIn("failed", str(ctx.exception))


class TestDownloadImage(unittest.TestCase):
    """Test image download functionality"""
    
    @patch('mopng_api.request.urlopen')
    def test_download_image(self, mock_urlopen):
        """Test image download"""
        mock_response = MagicMock()
        mock_response.read.return_value = b"fake_image_data"
        mock_urlopen.return_value.__enter__.return_value = mock_response
        
        import tempfile
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "test.png"
            api._download_image("https://example.com/img.png", output_path)
            self.assertTrue(output_path.exists())
            self.assertEqual(output_path.read_bytes(), b"fake_image_data")


class TestCommandArguments(unittest.TestCase):
    """Test command argument parsing"""
    
    def test_remove_bg_args(self):
        """Test remove-bg argument parsing"""
        import argparse
        parser = argparse.ArgumentParser()
        sub = parser.add_subparsers(dest="command")
        cmd = sub.add_parser("remove-bg")
        cmd.add_argument("--input", "-i", required=True)
        cmd.add_argument("--output", "-o", required=True)
        cmd.add_argument("--output-format", default="png")
        cmd.add_argument("--async-mode", action="store_true")
        cmd.add_argument("--return-mask", action="store_true")
        cmd.add_argument("--only-mask", action="store_true")
        
        args = parser.parse_args(["remove-bg", "-i", "test.jpg", "-o", "out.png"])
        self.assertEqual(args.input, "test.jpg")
        self.assertEqual(args.output, "out.png")
        self.assertEqual(args.output_format, "png")
    
    def test_upscale_args(self):
        """Test upscale argument parsing"""
        import argparse
        parser = argparse.ArgumentParser()
        sub = parser.add_subparsers(dest="command")
        cmd = sub.add_parser("upscale")
        cmd.add_argument("--input", "-i", required=True)
        cmd.add_argument("--output", "-o", required=True)
        cmd.add_argument("--scale", type=int, default=2)
        
        args = parser.parse_args(["upscale", "-i", "test.jpg", "-o", "out.png", "--scale", "4"])
        self.assertEqual(args.scale, 4)
    
    def test_text_to_image_args(self):
        """Test text-to-image argument parsing"""
        import argparse
        parser = argparse.ArgumentParser()
        sub = parser.add_subparsers(dest="command")
        cmd = sub.add_parser("text-to-image")
        cmd.add_argument("--prompt", "-p", required=True)
        cmd.add_argument("--output", "-o", required=True)
        cmd.add_argument("--model", default="wanx-v2.5")
        
        args = parser.parse_args([
            "text-to-image", 
            "-p", "a cat", 
            "-o", "out.png",
            "--model", "wanx-v2"
        ])
        self.assertEqual(args.prompt, "a cat")
        self.assertEqual(args.model, "wanx-v2")


class TestEnvironment(unittest.TestCase):
    """Test environment setup"""
    
    def test_api_key_required(self):
        """Test that API key is required"""
        # Save original env
        original_key = os.environ.get("MOPNG_API_KEY")
        
        try:
            # Remove API key
            if "MOPNG_API_KEY" in os.environ:
                del os.environ["MOPNG_API_KEY"]
            
            # Import should work, but main should fail
            import subprocess
            result = subprocess.run(
                [sys.executable, "-m", "scripts.mopng_api", "list-models"],
                capture_output=True,
                text=True,
                cwd=str(Path(__file__).parent.parent)
            )
            self.assertEqual(result.returncode, 2)
            self.assertIn("MOPNG_API_KEY", result.stderr)
        finally:
            # Restore original env
            if original_key:
                os.environ["MOPNG_API_KEY"] = original_key


if __name__ == "__main__":
    unittest.main(verbosity=2)
