import json
import sys
import tempfile
import threading
import time
import unittest
import urllib.error
import urllib.request
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import mai  # noqa: E402
import mai_registry  # noqa: E402


class PublicMarketplaceTest(unittest.TestCase):
    def run_cli(self, data_file, *args):
        output = StringIO()
        with redirect_stdout(output):
            mai.main(["--data", str(data_file), *args])
        return output.getvalue()

    def start_registry(self, registry_file, rate_limit_per_minute=60):
        mai_registry.issue_api_key(
            registry_file,
            token="admin-token",
            role="admin",
            subject="ops-admin",
        )
        mai_registry.issue_api_key(
            registry_file,
            token="seller-token",
            role="merchant",
            subject="seller-a",
            merchant_id="seller-a",
        )
        mai_registry.issue_api_key(
            registry_file,
            token="buyer-token",
            role="buyer",
            subject="alice",
            buyer_id="alice",
        )
        server = mai_registry.create_server(
            registry_file,
            host="127.0.0.1",
            port=0,
            rate_limit_per_minute=rate_limit_per_minute,
        )
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        self.addCleanup(server.shutdown)
        self.addCleanup(server.server_close)
        host, port = server.server_address
        base_url = f"http://{host}:{port}"

        for _ in range(20):
            try:
                with urllib.request.urlopen(f"{base_url}/health", timeout=1) as response:
                    payload = json.loads(response.read().decode("utf-8"))
                if payload["ok"]:
                    return base_url
            except OSError:
                time.sleep(0.05)
        self.fail("registry did not become ready")

    def request_json(self, base_url, method, path, token=None, payload=None):
        headers = {"Accept": "application/json"}
        data = None
        if token:
            headers["Authorization"] = f"Bearer {token}"
        if payload is not None:
            headers["Content-Type"] = "application/json"
            data = json.dumps(payload).encode("utf-8")
        request = urllib.request.Request(base_url + path, method=method, headers=headers, data=data)
        with urllib.request.urlopen(request, timeout=2) as response:
            return json.loads(response.read().decode("utf-8"))

    def make_seller_catalog(self, seller_file, sku="tea-a", title="Longjing Gift Box", tags="longjing,gift"):
        self.run_cli(
            seller_file,
            "merchant",
            "create",
            "--id",
            "seller-a",
            "--name",
            "West Lake Tea",
            "--city",
            "Hangzhou",
            "--contact",
            "wechat:westlake",
            "--tags",
            "tea,gift,local",
        )
        self.run_cli(
            seller_file,
            "product",
            "add",
            "--merchant",
            "seller-a",
            "--sku",
            sku,
            "--title",
            title,
            "--price",
            "88",
            "--stock",
            "5",
            "--category",
            "tea",
            "--tags",
            tags,
        )

    def test_authentication_authorization_moderation_and_payment_custody(self):
        with tempfile.TemporaryDirectory() as tmp:
            registry_file = Path(tmp) / "registry.json"
            seller_file = Path(tmp) / "seller.json"
            buyer_file = Path(tmp) / "buyer.json"
            base_url = self.start_registry(registry_file)
            self.make_seller_catalog(seller_file)

            with self.assertRaises(SystemExit):
                self.run_cli(
                    seller_file,
                    "registry",
                    "push",
                    "--url",
                    base_url,
                    "--confirm",
                    "--allow-insecure-localhost",
                )

            self.run_cli(
                seller_file,
                "registry",
                "push",
                "--url",
                base_url,
                "--api-key",
                "seller-token",
                "--confirm",
                "--allow-insecure-localhost",
            )

            with self.assertRaises(SystemExit):
                self.run_cli(
                    buyer_file,
                    "registry",
                    "message",
                    "--url",
                    base_url,
                    "--confirm",
                    "--allow-insecure-localhost",
                    "--buyer",
                    "alice",
                    "--merchant",
                    "seller-a",
                    "--text",
                    "Can this ship today?",
                )

            message = json.loads(
                self.run_cli(
                    buyer_file,
                    "registry",
                    "message",
                    "--url",
                    base_url,
                    "--api-key",
                    "buyer-token",
                    "--confirm",
                    "--allow-insecure-localhost",
                    "--buyer",
                    "alice",
                    "--merchant",
                    "seller-a",
                    "--sku",
                    "tea-a",
                    "--text",
                    "Can this ship today?",
                    "--format",
                    "json",
                )
            )
            self.assertEqual(message["message"]["buyer_id"], "alice")

            order = json.loads(
                self.run_cli(
                    buyer_file,
                    "registry",
                    "order",
                    "--url",
                    base_url,
                    "--api-key",
                    "buyer-token",
                    "--confirm",
                    "--allow-insecure-localhost",
                    "--buyer",
                    "alice",
                    "--merchant",
                    "seller-a",
                    "--sku",
                    "tea-a",
                    "--quantity",
                    "2",
                    "--format",
                    "json",
                )
            )
            self.assertEqual(order["order"]["id"], "ORD-0001")

            payment = json.loads(
                self.run_cli(
                    buyer_file,
                    "registry",
                    "payment-hold",
                    "--url",
                    base_url,
                    "--api-key",
                    "buyer-token",
                    "--confirm",
                    "--allow-insecure-localhost",
                    "--buyer",
                    "alice",
                    "--order",
                    "ORD-0001",
                    "--format",
                    "json",
                )
            )
            self.assertEqual(payment["payment"]["status"], "held_by_psp")
            self.assertEqual(payment["payment"]["provider"], "demo")

            with self.assertRaises(SystemExit):
                self.run_cli(
                    buyer_file,
                    "registry",
                    "payment-release",
                    "--url",
                    base_url,
                    "--api-key",
                    "buyer-token",
                    "--confirm",
                    "--allow-insecure-localhost",
                    "--payment",
                    payment["payment"]["id"],
                )

            released = json.loads(
                self.run_cli(
                    buyer_file,
                    "registry",
                    "payment-release",
                    "--url",
                    base_url,
                    "--api-key",
                    "admin-token",
                    "--confirm",
                    "--allow-insecure-localhost",
                    "--payment",
                    payment["payment"]["id"],
                    "--format",
                    "json",
                )
            )
            self.assertEqual(released["payment"]["status"], "released_to_seller")

            registry_store = json.loads(registry_file.read_text(encoding="utf-8"))
            self.assertEqual(registry_store["payments"]["PAY-0001"]["status"], "released_to_seller")
            self.assertNotIn("buyer-token", registry_file.read_text(encoding="utf-8"))

    def test_rate_limit_and_moderation_queue(self):
        with tempfile.TemporaryDirectory() as tmp:
            registry_file = Path(tmp) / "registry.json"
            seller_file = Path(tmp) / "seller.json"
            base_url = self.start_registry(registry_file, rate_limit_per_minute=3)
            self.make_seller_catalog(
                seller_file,
                sku="bad-a",
                title="Fake ID Kit",
                tags="fake id,document",
            )

            self.run_cli(
                seller_file,
                "registry",
                "push",
                "--url",
                base_url,
                "--api-key",
                "seller-token",
                "--confirm",
                "--allow-insecure-localhost",
            )

            clean_search = json.loads(
                self.run_cli(
                    seller_file,
                    "registry",
                    "search-products",
                    "--url",
                    base_url,
                    "--allow-insecure-localhost",
                    "--query",
                    "fake id",
                    "--format",
                    "json",
                )
            )
            self.assertEqual(clean_search["results"], [])

            queue = self.request_json(base_url, "GET", "/moderation/queue", token="admin-token")
            self.assertEqual(queue["products"][0]["sku"], "bad-a")
            self.assertEqual(queue["products"][0]["moderation_status"], "pending_review")

            approved = self.request_json(
                base_url,
                "POST",
                "/moderation/products/bad-a",
                token="admin-token",
                payload={"action": "approve", "note": "Allowed in test fixture."},
            )
            self.assertEqual(approved["product"]["moderation_status"], "approved")

            visible_search = json.loads(
                self.run_cli(
                    seller_file,
                    "registry",
                    "search-products",
                    "--url",
                    base_url,
                    "--allow-insecure-localhost",
                    "--query",
                    "fake id",
                    "--format",
                    "json",
                )
            )
            self.assertEqual(visible_search["results"][0]["sku"], "bad-a")

            rate_limit_code = None
            for _ in range(4):
                try:
                    self.request_json(base_url, "GET", "/search/products?query=tea")
                except urllib.error.HTTPError as exc:
                    rate_limit_code = exc.code
                    exc.close()
                    break
            self.assertEqual(rate_limit_code, 429)


if __name__ == "__main__":
    unittest.main()
