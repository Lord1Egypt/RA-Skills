import base64
import io
import importlib.util
import json
import os
import stat
import tempfile
import threading
import unittest
from urllib import parse, request


MODULE_PATH = os.path.join(os.path.dirname(__file__), "image_forge.py")
SKILL_ROOT = os.path.dirname(os.path.dirname(__file__))
SKILL_MD_PATH = os.path.join(SKILL_ROOT, "SKILL.md")
IMAGE_BRIEF_PATH = os.path.join(SKILL_ROOT, "references", "image-brief.md")


def load_module():
    spec = importlib.util.spec_from_file_location("image_forge", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ConfigTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.cwd = os.path.join(self.tmp.name, "project")
        self.home = os.path.join(self.tmp.name, "home")
        os.makedirs(self.cwd)
        os.makedirs(self.home)
        self.mod = load_module()

    def tearDown(self):
        self.tmp.cleanup()

    def approved_brief(self):
        return "\n".join([
            "Approved Image Brief",
            "Context: user needs a simple test image.",
            "Questions answered:",
            "- Q: What is the image for?",
            "  A: A quick product concept preview.",
            "- Q: Which style should it use?",
            "  A: Clean friendly illustration.",
            "Approaches considered:",
            "- A: Flat illustration, safest for clarity.",
            "- B: Realistic photo, stronger texture but less flexible.",
            "- C: 3D render, more polished but slower to iterate.",
            "Selected direction: flat illustration.",
            "Design confirmations: goal/output, subject, style, composition, text, and constraints were confirmed with the user.",
            "Output: one PNG.",
            "Subject: robot.",
            "Style: clean friendly illustration.",
            "Composition: centered subject with whitespace.",
            "Text: none.",
            "Constraints: no watermark.",
            "Edit scope: not applicable.",
            "Brief self-review: no placeholders, contradictions, missing constraints, or impossible composition.",
            "User approval: yes.",
        ])

    def test_configure_writes_project_config_without_api_key(self):
        result = self.mod.configure_values(
            cwd=self.cwd,
            home=self.home,
            api_url="https://www.nextai-code.com/v1",
            api_key="sk-test-secret",
            default_model="gpt-image-2",
        )

        self.assertTrue(result["projectConfigSaved"])
        project_config_path = os.path.join(self.cwd, ".image-forge", "config.json")
        with open(project_config_path) as handle:
            project_config = json.load(handle)
        self.assertEqual(project_config["apiUrl"], "https://www.nextai-code.com/v1")
        self.assertEqual(project_config["defaultModel"], "gpt-image-2")
        self.assertNotIn("apiKey", project_config)

    def test_configure_writes_user_secret_with_restricted_mode(self):
        result = self.mod.configure_values(
            cwd=self.cwd,
            home=self.home,
            api_url="https://www.nextai-code.com/v1",
            api_key="sk-test-secret",
            default_model="gpt-image-2",
        )

        self.assertTrue(result["secretSaved"])
        secret_path = os.path.join(self.home, ".config", "image-forge", "secrets.json")
        with open(secret_path) as handle:
            secret_config = json.load(handle)
        self.assertEqual(secret_config["apiKey"], "sk-test-secret")
        mode = stat.S_IMODE(os.stat(secret_path).st_mode)
        self.assertEqual(mode, 0o600)

    def test_configure_creates_user_secret_with_restricted_mode_from_start(self):
        secret_path = os.path.join(self.home, ".config", "image-forge", "secrets.json")
        original_dump = self.mod.json.dump
        observed_modes = []

        def recording_dump(data, handle, *args, **kwargs):
            if os.path.abspath(handle.name) == os.path.abspath(secret_path):
                observed_modes.append(stat.S_IMODE(os.stat(secret_path).st_mode))
            return original_dump(data, handle, *args, **kwargs)

        original_umask = os.umask(0)
        self.mod.json.dump = recording_dump
        try:
            result = self.mod.configure_values(
                cwd=self.cwd,
                home=self.home,
                api_key="sk-test-secret",
            )
        finally:
            self.mod.json.dump = original_dump
            os.umask(original_umask)

        self.assertTrue(result["secretSaved"])
        self.assertEqual(observed_modes, [0o600])
        mode = stat.S_IMODE(os.stat(secret_path).st_mode)
        self.assertEqual(mode, 0o600)

    def test_environment_overrides_files(self):
        self.mod.configure_values(
            cwd=self.cwd,
            home=self.home,
            api_url="https://www.nextai-code.com",
            api_key="sk-file-secret",
            default_model="file-model",
        )
        config = self.mod.load_effective_config(
            cwd=self.cwd,
            home=self.home,
            env={
                "IMAGE_FORGE_API_URL": "https://www.nextai-code.com/v1",
                "IMAGE_FORGE_API_KEY": "sk-env-secret",
                "IMAGE_FORGE_MODEL": "env-model",
            },
        )
        self.assertEqual(config["apiUrl"], "https://www.nextai-code.com/v1")
        self.assertEqual(config["apiKey"], "sk-env-secret")
        self.assertEqual(config["model"], "env-model")

    def test_rejects_non_nextai_api_url_from_configure(self):
        with self.assertRaises(self.mod.ImageForgeError) as ctx:
            self.mod.configure_values(
                cwd=self.cwd,
                home=self.home,
                api_url="https://images.example.com/v1",
                api_key="sk-test-secret",
                default_model="gpt-image-2",
            )

        self.assertEqual(ctx.exception.code, "invalid_api_url")
        self.assertIn("https://www.nextai-code.com/v1", str(ctx.exception))

    def test_rejects_non_nextai_api_url_from_environment(self):
        with self.assertRaises(self.mod.ImageForgeError) as ctx:
            self.mod.load_effective_config(
                cwd=self.cwd,
                home=self.home,
                env={"IMAGE_FORGE_API_URL": "https://other.example.com/v1"},
            )

        self.assertEqual(ctx.exception.code, "invalid_api_url")

    def test_default_output_dir_is_project_root(self):
        config = self.mod.load_effective_config(cwd=self.cwd, home=self.home, env={})

        self.assertEqual(config["outputDir"], ".")
        self.assertNotEqual(config["outputDir"], ".image-forge/outputs")
        self.assertNotIn("ImageForge/outputs", config["outputDir"])

    def test_missing_model_is_not_silently_defaulted_before_setup(self):
        self.mod.configure_values(
            cwd=self.cwd,
            home=self.home,
            api_url="https://www.nextai-code.com/v1",
            api_key="sk-file-secret",
        )

        config = self.mod.load_effective_config(cwd=self.cwd, home=self.home, env={})

        self.assertEqual(config["model"], "")
        with self.assertRaises(self.mod.ImageForgeError) as ctx:
            self.mod.preflight(cwd=self.cwd, home=self.home, env={})
        self.assertEqual(ctx.exception.code, "missing_config")
        self.assertIn("model", str(ctx.exception))

    def test_doctor_reports_config_status_without_secret_values(self):
        self.mod.configure_values(
            cwd=self.cwd,
            home=self.home,
            api_url="https://www.nextai-code.com/v1",
            api_key="sk-doctor-secret",
            default_model="gpt-image-2",
        )

        configured = self.mod.doctor(cwd=self.cwd, home=self.home, env={})

        self.assertEqual(configured["configured"], True)
        self.assertEqual(configured["apiHost"], "www.nextai-code.com")
        self.assertEqual(configured["model"], "gpt-image-2")
        self.assertEqual(configured["apiKey"], "configured")
        self.assertNotIn("sk-doctor-secret", json.dumps(configured))

        missing_cwd = os.path.join(self.tmp.name, "missing-project")
        missing_home = os.path.join(self.tmp.name, "missing-home")
        os.makedirs(missing_cwd)
        os.makedirs(missing_home)
        missing = self.mod.doctor(cwd=missing_cwd, home=missing_home, env={})

        self.assertEqual(missing["configured"], False)
        self.assertEqual(missing["apiHost"], "www.nextai-code.com")
        self.assertEqual(missing["model"], "")
        self.assertEqual(missing["apiKey"], "missing")

    def test_preflight_blocks_when_required_config_is_missing(self):
        with self.assertRaises(self.mod.ImageForgeError) as ctx:
            self.mod.preflight(cwd=self.cwd, home=self.home, env={})

        self.assertEqual(ctx.exception.code, "missing_config")
        self.assertIn("API key", str(ctx.exception))
        self.assertIn("model", str(ctx.exception))
        self.assertIn("setup-server", str(ctx.exception))
        self.assertIn("Do not continue", str(ctx.exception))

    def test_preflight_passes_with_api_url_key_and_model_without_leaking_secret(self):
        self.mod.configure_values(
            cwd=self.cwd,
            home=self.home,
            api_url="https://www.nextai-code.com/v1",
            api_key="sk-preflight-secret",
            default_model="custom-image-model",
        )

        result = self.mod.preflight(cwd=self.cwd, home=self.home, env={})

        self.assertEqual(result["ready"], True)
        self.assertEqual(result["apiHost"], "www.nextai-code.com")
        self.assertEqual(result["model"], "custom-image-model")
        self.assertEqual(result["apiKey"], "configured")
        self.assertNotIn("sk-preflight-secret", json.dumps(result))

    def test_setup_interactive_collects_url_key_and_default_model(self):
        answers = iter([
            "",
        ])

        result = self.mod.setup_interactive(
            cwd=self.cwd,
            home=self.home,
            input_func=lambda prompt: next(answers),
            secret_prompt_func=lambda prompt: "sk-setup-secret",
        )

        self.assertEqual(result["ready"], True)
        self.assertEqual(result["apiHost"], "www.nextai-code.com")
        self.assertEqual(result["model"], "gpt-image-2")
        self.assertEqual(result["apiKey"], "configured")
        self.assertNotIn("sk-setup-secret", json.dumps(result))

        with open(os.path.join(self.cwd, ".image-forge", "config.json")) as handle:
            project_config = json.load(handle)
        self.assertEqual(project_config["apiUrl"], "https://www.nextai-code.com/v1")
        self.assertEqual(project_config["defaultModel"], "gpt-image-2")
        self.assertNotIn("apiKey", project_config)

        with open(os.path.join(self.home, ".config", "image-forge", "secrets.json")) as handle:
            secret_config = json.load(handle)
        self.assertEqual(secret_config["apiKey"], "sk-setup-secret")

    def test_setup_interactive_requires_api_key(self):
        answers = iter([
            "custom-image-model",
        ])

        with self.assertRaises(self.mod.ImageForgeError) as ctx:
            self.mod.setup_interactive(
                cwd=self.cwd,
                home=self.home,
                input_func=lambda prompt: next(answers),
                secret_prompt_func=lambda prompt: "",
            )

        self.assertEqual(ctx.exception.code, "missing_config")
        self.assertIn("API key", str(ctx.exception))

    def test_setup_form_html_is_chinese_minimal_and_orders_url_key_model(self):
        self.mod.configure_values(
            cwd=self.cwd,
            home=self.home,
            api_url="https://www.nextai-code.com/v1",
            api_key="sk-existing-secret",
            default_model="gpt-image-2",
        )
        config = self.mod.load_effective_config(cwd=self.cwd, home=self.home, env={})

        html = self.mod.setup_form_html(config=config, token="fixed-token")

        self.assertIn("https://www.nextai-code.com/v1", html)
        self.assertIn("gpt-image-2", html)
        self.assertIn("配置 ImageForge", html)
        self.assertIn("已配置，留空则不修改", html)
        self.assertIn("保存配置", html)
        self.assertIn("https://www.nextai-code.com/v1", html)
        self.assertIn("获取 API Key", html)
        self.assertIn('<label for="api_key">API Key</label>', html)
        self.assertIn('<label for="default_model">默认模型</label>', html)
        self.assertNotIn('name="api_url"', html)
        self.assertNotIn("Configure the OpenAI-compatible image API", html)
        self.assertNotIn("sk-existing-secret", html)
        self.assertLess(html.index('name="api_key"'), html.index('name="default_model"'))

    def test_setup_server_accepts_browser_form_and_shuts_down(self):
        server, setup_url, state = self.mod.create_setup_server(
            cwd=self.cwd,
            home=self.home,
            host="127.0.0.1",
            port=0,
            token="fixed-token",
        )
        thread = threading.Thread(target=server.serve_forever)
        thread.daemon = True
        thread.start()
        try:
            data = parse.urlencode({
                "token": "fixed-token",
                "default_model": "",
                "api_key": "sk-browser-secret",
            }).encode("utf-8")
            req = request.Request(setup_url, data=data, method="POST")

            with request.urlopen(req, timeout=5) as response:
                body = response.read().decode("utf-8")

            thread.join(2)
            self.assertFalse(thread.is_alive())
            self.assertTrue(state["completed"])
            self.assertIn("配置已保存", body)
            self.assertIn("接口地址", body)
            self.assertNotIn("sk-browser-secret", body)
            self.assertNotIn("API Host", body)

            result = self.mod.preflight(cwd=self.cwd, home=self.home, env={})
            self.assertEqual(result["ready"], True)
            self.assertEqual(result["model"], "gpt-image-2")
            self.assertNotIn("sk-browser-secret", json.dumps(result))
        finally:
            server.server_close()

    def test_ensure_ready_returns_preflight_when_configured_without_setup(self):
        self.mod.configure_values(
            cwd=self.cwd,
            home=self.home,
            api_url="https://www.nextai-code.com/v1",
            api_key="sk-ready-secret",
            default_model="gpt-image-2",
        )
        setup_calls = []

        result = self.mod.ensure_ready(
            cwd=self.cwd,
            home=self.home,
            env={},
            setup_func=lambda **kwargs: setup_calls.append(kwargs),
        )

        self.assertEqual(result["ready"], True)
        self.assertEqual(result["apiKey"], "configured")
        self.assertEqual(setup_calls, [])

    def test_ensure_ready_runs_setup_when_config_is_missing(self):
        setup_calls = []

        def fake_setup(**kwargs):
            setup_calls.append(kwargs)
            self.mod.configure_values(
                cwd=self.cwd,
                home=self.home,
                api_url="https://www.nextai-code.com/v1",
                api_key="sk-setup-secret",
                default_model="gpt-image-2",
            )

        result = self.mod.ensure_ready(
            cwd=self.cwd,
            home=self.home,
            env={},
            setup_func=fake_setup,
        )

        self.assertEqual(result["ready"], True)
        self.assertEqual(result["model"], "gpt-image-2")
        self.assertEqual(len(setup_calls), 1)
        self.assertEqual(setup_calls[0]["cwd"], self.cwd)
        self.assertEqual(setup_calls[0]["home"], self.home)

    def test_parse_edit_accepts_multiple_images(self):
        args = self.mod.parse_args([
            "edit",
            "--image", "one.png",
            "--image", "two.png",
            "--prompt", "merge them",
            "--brief", "Approved Brief: merge two provided references into one clean composition",
        ])

        self.assertEqual(args.command, "edit")
        self.assertEqual(args.image, ["one.png", "two.png"])
        self.assertEqual(args.prompt, "merge them")
        self.assertEqual(args.brief, "Approved Brief: merge two provided references into one clean composition")

    def test_parse_generate_accepts_direct_mode(self):
        args = self.mod.parse_args([
            "generate",
            "--prompt", "robot",
            "--direct",
        ])

        self.assertEqual(args.command, "generate")
        self.assertEqual(args.prompt, "robot")
        self.assertTrue(args.direct)

    def test_parse_preflight_command(self):
        args = self.mod.parse_args(["preflight"])

        self.assertEqual(args.command, "preflight")

    def test_parse_setup_command(self):
        args = self.mod.parse_args(["setup"])

        self.assertEqual(args.command, "setup")

    def test_parse_setup_server_command(self):
        args = self.mod.parse_args(["setup-server", "--no-open"])

        self.assertEqual(args.command, "setup-server")
        self.assertTrue(args.no_open)

    def test_parse_ensure_ready_command(self):
        args = self.mod.parse_args(["ensure-ready", "--no-open"])

        self.assertEqual(args.command, "ensure-ready")
        self.assertTrue(args.no_open)

    def test_image_forge_command_wrapper_is_installed_in_skill_bin(self):
        wrapper_path = os.path.join(SKILL_ROOT, "bin", "image-forge")

        self.assertTrue(os.path.exists(wrapper_path))
        self.assertTrue(os.access(wrapper_path, os.X_OK))

    def test_resolve_api_key_for_configure_prompts_when_missing(self):
        self.assertEqual(
            self.mod.resolve_api_key_for_configure("  sk-inline-secret  "),
            "sk-inline-secret",
        )

        prompted = self.mod.resolve_api_key_for_configure(
            None,
            prompt_func=lambda prompt: "  sk-prompt-secret  ",
        )

        self.assertEqual(prompted, "sk-prompt-secret")

    def test_missing_config_returns_setup_guidance(self):
        with self.assertRaises(self.mod.ImageForgeError) as ctx:
            self.mod.require_config({"apiUrl": "", "apiKey": "", "model": ""})
        self.assertEqual(ctx.exception.code, "missing_config")
        self.assertIn("setup-server", str(ctx.exception))
        self.assertNotIn("--api-key '<API key>'", str(ctx.exception))

    def test_redact_hides_sk_tokens_and_api_key_values(self):
        text = 'Authorization: Bearer sk-secret-value and {"api_key": "plain-json-secret"} api_key=plain-equals-secret'
        redacted = self.mod.redact(text)
        self.assertNotIn("sk-secret-value", redacted)
        self.assertNotIn("plain-json-secret", redacted)
        self.assertNotIn("plain-equals-secret", redacted)
        self.assertIn("<REDACTED>", redacted)

    def test_redact_hides_plain_bearer_tokens(self):
        text = "Authorization: Bearer abcdefghijklmnop\nBearer plain-bearer-secret"
        redacted = self.mod.redact(text)
        self.assertNotIn("abcdefghijklmnop", redacted)
        self.assertNotIn("plain-bearer-secret", redacted)
        self.assertIn("<REDACTED>", redacted)

    def test_build_generation_request_uses_openai_endpoint(self):
        config = {
            "apiUrl": "https://www.nextai-code.com/v1",
            "apiKey": "sk-secret",
            "model": "gpt-image-2",
            "outputDir": ".",
        }
        url, headers, body = self.mod.build_generation_request(
            config=config,
            prompt="a brass robot watering a bonsai",
            size="1024x1024",
            quality="high",
            n=1,
        )
        payload = json.loads(body.decode("utf-8"))

        self.assertEqual(url, "https://www.nextai-code.com/v1/images/generations")
        self.assertEqual(headers["Authorization"], "Bearer sk-secret")
        self.assertEqual(payload["model"], "gpt-image-2")
        self.assertEqual(payload["prompt"], "a brass robot watering a bonsai")
        self.assertEqual(payload["size"], "1024x1024")
        self.assertEqual(payload["quality"], "high")
        self.assertEqual(payload["n"], 1)

    def test_build_edit_request_uses_multipart_edit_endpoint(self):
        image_path = os.path.join(self.cwd, "source.png")
        with open(image_path, "wb") as handle:
            handle.write(b"fake-png")
        config = {
            "apiUrl": "https://www.nextai-code.com/v1",
            "apiKey": "sk-secret",
            "model": "gpt-image-2",
            "outputDir": ".",
        }

        url, headers, body = self.mod.build_edit_request(
            config=config,
            image_paths=[image_path],
            prompt="make it neon",
            size="1536x1024",
        )
        body_text = body.decode("latin-1")

        self.assertEqual(url, "https://www.nextai-code.com/v1/images/edits")
        self.assertEqual(headers["Authorization"], "Bearer sk-secret")
        self.assertTrue(headers["Content-Type"].startswith("multipart/form-data; boundary="))
        boundary = headers["Content-Type"].split("boundary=", 1)[1]
        self.assertIn("--" + boundary, body_text)
        self.assertIn('name="model"\r\n\r\ngpt-image-2', body_text)
        self.assertIn('name="prompt"\r\n\r\nmake it neon', body_text)
        self.assertIn('name="size"\r\n\r\n1536x1024', body_text)
        self.assertIn('name="image"; filename="source.png"', body_text)

    def test_build_edit_request_accepts_repeated_image_paths(self):
        image_path = os.path.join(self.cwd, "source.png")
        with open(image_path, "wb") as handle:
            handle.write(b"fake-png")
        config = {
            "apiUrl": "https://www.nextai-code.com/v1",
            "apiKey": "sk-secret",
            "model": "gpt-image-2",
            "outputDir": ".",
        }

        _url, _headers, body = self.mod.build_edit_request(
            config=config,
            image_paths=[image_path, image_path],
            prompt="make it neon",
            size="1024x1024",
        )
        body_text = body.decode("latin-1")

        self.assertEqual(body_text.count('name="image"'), 2)

    def test_write_image_outputs_writes_png_only(self):
        response = {
            "data": [
                {"b64_json": base64.b64encode(b"fake-image").decode("ascii")}
            ]
        }
        paths = self.mod.write_image_outputs(
            response=response,
            output_dir=self.cwd,
            output_name="robot",
        )

        self.assertEqual(len(paths), 1)
        self.assertTrue(paths[0]["imagePath"].endswith(".png"))
        self.assertTrue(os.path.exists(paths[0]["imagePath"]))
        self.assertNotIn("metadataPath", paths[0])
        with open(paths[0]["imagePath"], "rb") as handle:
            self.assertEqual(handle.read(), b"fake-image")
        self.assertFalse(os.path.exists(os.path.join(self.cwd, "robot-01.json")))

    def test_write_image_outputs_does_not_create_sidecar_json_for_multiple_images(self):
        response = {
            "data": [
                {"b64_json": base64.b64encode(b"fake-image-1").decode("ascii")},
                {"b64_json": base64.b64encode(b"fake-image-2").decode("ascii")},
            ]
        }
        paths = self.mod.write_image_outputs(
            response=response,
            output_dir=self.cwd,
            output_name="robot",
        )

        self.assertEqual(len(paths), 2)
        self.assertNotIn("metadataPath", paths[0])
        self.assertFalse(os.path.exists(os.path.join(self.cwd, "robot-01.json")))
        self.assertFalse(os.path.exists(os.path.join(self.cwd, "robot-02.json")))

    def test_generate_image_defaults_to_project_root_without_sidecar_json(self):
        self.mod.configure_values(
            cwd=self.cwd,
            home=self.home,
            api_url="https://www.nextai-code.com/v1",
            api_key="sk-secret",
            default_model="gpt-image-2",
        )
        original_http_json = self.mod.http_json
        self.mod.http_json = lambda _url, _headers, _body: {
            "data": [
                {"b64_json": base64.b64encode(b"fake-image").decode("ascii")}
            ]
        }
        try:
            paths = self.mod.generate_image(
                prompt="robot",
                output_name="robot",
                cwd=self.cwd,
                home=self.home,
                env={},
                brief=self.approved_brief(),
            )
        finally:
            self.mod.http_json = original_http_json

        self.assertEqual(os.path.dirname(paths[0]["imagePath"]), self.cwd)
        self.assertTrue(os.path.exists(os.path.join(self.cwd, "robot-01.png")))
        self.assertFalse(os.path.exists(os.path.join(self.cwd, "robot-01.json")))

    def test_generate_image_requires_brief_before_provider_call(self):
        self.mod.configure_values(
            cwd=self.cwd,
            home=self.home,
            api_url="https://www.nextai-code.com/v1",
            api_key="sk-secret",
            default_model="gpt-image-2",
        )
        calls = []
        original_http_json = self.mod.http_json
        self.mod.http_json = lambda _url, _headers, _body: calls.append("called")
        try:
            with self.assertRaises(self.mod.ImageForgeError) as ctx:
                self.mod.generate_image(
                    prompt="robot",
                    output_name="robot",
                    cwd=self.cwd,
                    home=self.home,
                    env={},
                )
        finally:
            self.mod.http_json = original_http_json

        self.assertEqual(ctx.exception.code, "brief_required")
        self.assertIn("Image Brief Gate", str(ctx.exception))
        self.assertEqual(calls, [])

    def test_generate_image_rejects_unstructured_brief_before_provider_call(self):
        self.mod.configure_values(
            cwd=self.cwd,
            home=self.home,
            api_url="https://www.nextai-code.com/v1",
            api_key="sk-secret",
            default_model="gpt-image-2",
        )
        calls = []
        original_http_json = self.mod.http_json
        self.mod.http_json = lambda _url, _headers, _body: calls.append("called")
        try:
            with self.assertRaises(self.mod.ImageForgeError) as ctx:
                self.mod.generate_image(
                    prompt="robot",
                    output_name="robot",
                    cwd=self.cwd,
                    home=self.home,
                    env={},
                    brief="Approved Brief: robot",
                )
        finally:
            self.mod.http_json = original_http_json

        self.assertEqual(ctx.exception.code, "brief_required")
        self.assertIn("structured Approved Image Brief", str(ctx.exception))
        self.assertEqual(calls, [])

    def test_generate_image_rejects_brief_without_question_answer_evidence_before_provider_call(self):
        self.mod.configure_values(
            cwd=self.cwd,
            home=self.home,
            api_url="https://www.nextai-code.com/v1",
            api_key="sk-secret",
            default_model="gpt-image-2",
        )
        calls = []
        original_http_json = self.mod.http_json
        self.mod.http_json = lambda _url, _headers, _body: calls.append("called")
        weak_brief = self.approved_brief().replace(
            "Questions answered:\n- Q: What is the image for?\n  A: A quick product concept preview.\n- Q: Which style should it use?\n  A: Clean friendly illustration.",
            "Questions answered: purpose, subject, style, output.",
        )
        try:
            with self.assertRaises(self.mod.ImageForgeError) as ctx:
                self.mod.generate_image(
                    prompt="robot",
                    output_name="robot",
                    cwd=self.cwd,
                    home=self.home,
                    env={},
                    brief=weak_brief,
                )
        finally:
            self.mod.http_json = original_http_json

        self.assertEqual(ctx.exception.code, "brief_required")
        self.assertIn("question/answer evidence", str(ctx.exception))
        self.assertEqual(calls, [])

    def test_generate_image_rejects_brief_without_approach_comparison_before_provider_call(self):
        self.mod.configure_values(
            cwd=self.cwd,
            home=self.home,
            api_url="https://www.nextai-code.com/v1",
            api_key="sk-secret",
            default_model="gpt-image-2",
        )
        calls = []
        original_http_json = self.mod.http_json
        self.mod.http_json = lambda _url, _headers, _body: calls.append("called")
        weak_brief = self.approved_brief().replace(
            "Approaches considered:\n- A: Flat illustration, safest for clarity.\n- B: Realistic photo, stronger texture but less flexible.\n- C: 3D render, more polished but slower to iterate.",
            "Approaches considered: flat illustration.",
        )
        try:
            with self.assertRaises(self.mod.ImageForgeError) as ctx:
                self.mod.generate_image(
                    prompt="robot",
                    output_name="robot",
                    cwd=self.cwd,
                    home=self.home,
                    env={},
                    brief=weak_brief,
                )
        finally:
            self.mod.http_json = original_http_json

        self.assertEqual(ctx.exception.code, "brief_required")
        self.assertIn("2-3 approaches", str(ctx.exception))
        self.assertEqual(calls, [])

    def test_generate_image_rejects_empty_brief_fields_before_provider_call(self):
        self.mod.configure_values(
            cwd=self.cwd,
            home=self.home,
            api_url="https://www.nextai-code.com/v1",
            api_key="sk-secret",
            default_model="gpt-image-2",
        )
        calls = []
        original_http_json = self.mod.http_json
        self.mod.http_json = lambda _url, _headers, _body: calls.append("called")
        weak_brief = self.approved_brief().replace(
            "Subject: robot.",
            "Subject:",
        )
        try:
            with self.assertRaises(self.mod.ImageForgeError) as ctx:
                self.mod.generate_image(
                    prompt="robot",
                    output_name="robot",
                    cwd=self.cwd,
                    home=self.home,
                    env={},
                    brief=weak_brief,
                )
        finally:
            self.mod.http_json = original_http_json

        self.assertEqual(ctx.exception.code, "brief_required")
        self.assertIn("empty or placeholder fields", str(ctx.exception))
        self.assertEqual(calls, [])

    def test_generate_image_allows_direct_mode_without_brief(self):
        self.mod.configure_values(
            cwd=self.cwd,
            home=self.home,
            api_url="https://www.nextai-code.com/v1",
            api_key="sk-secret",
            default_model="gpt-image-2",
        )
        original_http_json = self.mod.http_json
        self.mod.http_json = lambda _url, _headers, _body: {
            "data": [
                {"b64_json": base64.b64encode(b"fake-image").decode("ascii")}
            ]
        }
        try:
            paths = self.mod.generate_image(
                prompt="robot",
                output_name="robot-direct",
                cwd=self.cwd,
                home=self.home,
                env={},
                direct=True,
            )
        finally:
            self.mod.http_json = original_http_json

        self.assertTrue(os.path.exists(paths[0]["imagePath"]))

    def test_edit_image_requires_brief_before_provider_call(self):
        source_path = os.path.join(self.cwd, "source.png")
        with open(source_path, "wb") as handle:
            handle.write(b"fake-png")
        self.mod.configure_values(
            cwd=self.cwd,
            home=self.home,
            api_url="https://www.nextai-code.com/v1",
            api_key="sk-secret",
            default_model="gpt-image-2",
        )
        calls = []
        original_http_json = self.mod.http_json
        self.mod.http_json = lambda _url, _headers, _body: calls.append("called")
        try:
            with self.assertRaises(self.mod.ImageForgeError) as ctx:
                self.mod.edit_image(
                    image_paths=[source_path],
                    prompt="make it neon",
                    cwd=self.cwd,
                    home=self.home,
                    env={},
                )
        finally:
            self.mod.http_json = original_http_json

        self.assertEqual(ctx.exception.code, "brief_required")
        self.assertEqual(calls, [])

    def test_version_check_degrades_without_git(self):
        result = self.mod.check_version(
            cwd=self.cwd,
            ttl_hours=24,
            run_git=lambda args, cwd: (_ for _ in ()).throw(OSError("git unavailable")),
        )
        self.assertEqual(result["status"], "unavailable")
        self.assertEqual(result["error"], "version_check_unavailable")

    def test_version_check_reports_update_available(self):
        calls = []

        def fake_git(args, cwd):
            calls.append(list(args))
            if args == ["rev-parse", "HEAD"]:
                return "local-sha\n"
            if args == ["ls-remote", "origin", "HEAD"]:
                return "remote-sha\tHEAD\n"
            raise OSError("unexpected git command")

        result = self.mod.check_version(cwd=self.cwd, ttl_hours=0, run_git=fake_git)
        self.assertEqual(result["status"], "update_available")
        self.assertEqual(result["local"], "local-sha")
        self.assertEqual(result["remote"], "remote-sha")
        self.assertIn("npx skills update image-forge", result["upgradeCommand"])
        self.assertEqual(calls, [
            ["rev-parse", "HEAD"],
            ["ls-remote", "origin", "HEAD"],
        ])

    def test_version_check_never_passes_credentialed_origin_url_to_run_git(self):
        secret_url = "https://ghp_secret_token@example.com/org/repo.git"
        calls = []

        def fake_git(args, cwd):
            calls.append(list(args))
            if any("ghp_secret_token" in arg for arg in args):
                raise AssertionError("credentialed URL leaked into git argv")
            if args == ["rev-parse", "HEAD"]:
                return "local-sha\n"
            if args == ["remote", "get-url", "origin"]:
                return secret_url + "\n"
            if args == ["ls-remote", "origin", "HEAD"]:
                return "remote-sha\tHEAD\n"
            raise OSError("unexpected git command")

        result = self.mod.check_version(cwd=self.cwd, ttl_hours=0, run_git=fake_git)
        self.assertEqual(result["status"], "update_available")
        self.assertEqual(result["remote"], "remote-sha")
        self.assertNotIn("ghp_secret_token", json.dumps(calls))

    def test_version_check_does_not_store_secret_remote_url_on_ls_remote_failure(self):
        def fake_git(args, cwd):
            if args == ["rev-parse", "HEAD"]:
                return "local-sha\n"
            if args == ["ls-remote", "origin", "HEAD"]:
                raise OSError("fatal: could not read from https://ghp_secret_token@example.com/org/repo.git")
            raise OSError("unexpected git command")

        result = self.mod.check_version(cwd=self.cwd, ttl_hours=0, run_git=fake_git)
        state_path = os.path.join(self.cwd, ".image-forge", "version-check.json")
        with open(state_path) as handle:
            stored = handle.read()

        self.assertEqual(result["status"], "unavailable")
        self.assertEqual(result["error"], "version_check_unavailable")
        self.assertNotIn("ghp_secret_token", json.dumps(result))
        self.assertNotIn("ghp_secret_token", stored)

    def test_version_check_sanitizes_cached_unavailable_state(self):
        state_path = os.path.join(self.cwd, ".image-forge", "version-check.json")
        self.mod.write_json(state_path, {
            "status": "unavailable",
            "error": "version_check_unavailable",
            "checkedAt": int(self.mod.time.time()),
            "message": "fatal: could not read from https://ghp_secret_token@example.com/org/repo.git",
        })

        result = self.mod.check_version(
            cwd=self.cwd,
            ttl_hours=24,
            run_git=lambda args, cwd: (_ for _ in ()).throw(AssertionError("git should not run")),
        )
        with open(state_path) as handle:
            stored = handle.read()

        self.assertNotIn("ghp_secret_token", json.dumps(result))
        self.assertEqual(
            result["message"],
            "Version check unavailable; continuing without update status.",
        )
        self.assertNotIn("ghp_secret_token", stored)


class SkillInstructionTests(unittest.TestCase):
    def read_skill(self):
        with io.open(SKILL_MD_PATH, encoding="utf-8") as handle:
            return handle.read()

    def read_image_brief(self):
        with io.open(IMAGE_BRIEF_PATH, encoding="utf-8") as handle:
            return handle.read()

    def test_skill_requires_preflight_as_first_step_for_every_use(self):
        skill = self.read_skill()

        self.assertIn("First Execution Gate", skill)
        self.assertIn("On every ImageForge skill use", skill)
        self.assertIn("run ensure-ready as the first command", skill)
        self.assertIn('python3 "$IMAGE_FORGE_SCRIPT" ensure-ready', skill)

    def test_skill_stops_current_flow_and_runs_setup_when_unconfigured(self):
        skill = self.read_skill()

        self.assertIn("ensure-ready runs preflight", skill)
        self.assertIn("If configuration is missing, it stops the current flow", skill)
        self.assertIn("setup-server", skill)
        self.assertIn("Do not do any other work until preflight passes", skill)
        self.assertNotIn("Before any AI image generation or editing work, run ImageForge `preflight`.", skill)
        self.assertNotIn("brand questions", skill)
        self.assertNotIn("style questions", skill)
        self.assertNotIn("brand, product, copy, style, layout", skill)

    def test_skill_resolves_workspace_and_home_install_paths_before_commands(self):
        skill = self.read_skill()

        self.assertIn("IMAGE_FORGE_SCRIPT", skill)
        self.assertIn('$PWD/.agents/skills/image-forge/scripts/image_forge.py', skill)
        self.assertIn('$HOME/.agents/skills/image-forge/scripts/image_forge.py', skill)
        self.assertIn('python3 "$IMAGE_FORGE_SCRIPT" ensure-ready', skill)
        self.assertNotIn("python3 ~/.agents/skills/image-forge/scripts/image_forge.py preflight", skill)

    def test_skill_defaults_outputs_to_project_root_without_sidecar_json(self):
        skill = self.read_skill()

        self.assertIn("Default output directory is the project root", skill)
        self.assertIn("do not create output sidecar `.json` files", skill)
        self.assertNotIn("ImageForge/outputs/YYYY-MM-DD", skill)
        self.assertNotIn("metadata path", skill)

    def test_skill_requires_image_brief_gate_before_generate_or_edit(self):
        skill = self.read_skill()

        self.assertIn("Image Brief Gate", skill)
        self.assertIn("Read `references/image-brief.md`", skill)
        self.assertIn("Do not run `generate` or `edit` until", skill)
        self.assertIn("user approves the brief", skill)
        self.assertIn("Ask one question at a time", skill)
        self.assertIn("MUST complete the Image Brief Brainstorming Workflow", skill)
        self.assertIn("Do not compress the workflow into one brief", skill)
        self.assertIn("Direct mode", skill)
        self.assertIn("Generate: after the Image Brief Gate", skill)
        self.assertIn("Edit: after the Image Brief Gate", skill)
        self.assertIn("--brief '<approved brief>'", skill)
        self.assertIn("--direct", skill)

    def test_image_brief_reference_covers_quality_inputs_and_confirmation(self):
        brief = self.read_image_brief()

        self.assertIn("Purpose", brief)
        self.assertIn("Audience", brief)
        self.assertIn("Deliverable", brief)
        self.assertIn("Subject", brief)
        self.assertIn("Style", brief)
        self.assertIn("Composition", brief)
        self.assertIn("Text", brief)
        self.assertIn("Constraints", brief)
        self.assertIn("Edit-Specific", brief)
        self.assertIn("Approved Brief", brief)
        self.assertIn("one question at a time", brief)
        self.assertIn("Direct mode", brief)
        self.assertIn("Image Brief Brainstorming Workflow", brief)
        self.assertIn("MUST complete these steps in order", brief)
        self.assertIn("Explore context", brief)
        self.assertIn("Offer visual companion", brief)
        self.assertIn("Ask clarifying questions", brief)
        self.assertIn("Propose 2-3 approaches", brief)
        self.assertIn("Present design sections", brief)
        self.assertIn("User approves", brief)
        self.assertIn("Brief self-review", brief)
        self.assertIn("Do not compress this into one message", brief)
        self.assertIn("Approved Image Brief", brief)
        self.assertIn("Questions answered", brief)
        self.assertIn("Approaches considered", brief)
        self.assertIn("Selected direction", brief)
        self.assertIn("visible checklist", brief)
        self.assertIn("Do NOT answer with an Approved Image Brief in the first response", brief)
        self.assertIn("stop after the first question", brief)
        self.assertIn("Design confirmations", brief)
        self.assertIn("question/answer evidence", brief)
        self.assertIn("2-3 approaches", brief)

    def test_docs_do_not_show_generate_or_edit_without_brief_gate(self):
        docs = []
        for path in [
            os.path.join(SKILL_ROOT, "SKILL.md"),
            os.path.join(SKILL_ROOT, "references", "installation.md"),
            os.path.join(SKILL_ROOT, "references", "openai-compatible-images.md"),
            os.path.join(SKILL_ROOT, "references", "troubleshooting.md"),
        ]:
            with io.open(path, encoding="utf-8") as handle:
                docs.append(handle.read())
        combined = "\n".join(docs)

        self.assertNotIn("generate --prompt '<prompt>'", combined)
        self.assertNotIn("edit --image '<path>' --prompt '<instruction>'", combined)
        self.assertIn("generate --brief '<approved brief>'", combined)
        self.assertIn("edit --brief '<approved brief>'", combined)


if __name__ == "__main__":
    unittest.main()
