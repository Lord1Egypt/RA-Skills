import json
import sys
import tempfile
import threading
import time
import unittest
import urllib.request
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import mai  # noqa: E402
import mai_registry  # noqa: E402


class MaiRegistryTest(unittest.TestCase):
    def run_cli(self, data_file, *args):
        output = StringIO()
        with redirect_stdout(output):
            mai.main(["--data", str(data_file), *args])
        return output.getvalue()

    def start_registry(self, registry_file):
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
        server = mai_registry.create_server(registry_file, host="127.0.0.1", port=0)
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

    def test_registry_enables_cross_agent_discovery_and_orders(self):
        with tempfile.TemporaryDirectory() as tmp:
            registry_file = Path(tmp) / "registry.json"
            seller_file = Path(tmp) / "seller.json"
            buyer_file = Path(tmp) / "buyer.json"
            base_url = self.start_registry(registry_file)

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
                "tea-a",
                "--title",
                "Longjing Gift Box",
                "--price",
                "88",
                "--stock",
                "5",
                "--category",
                "tea",
                "--tags",
                "longjing,gift",
                "--shipping",
                "same-city courier",
            )

            push = json.loads(
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
                    "--format",
                    "json",
                )
            )
            self.assertEqual(push["pushed"]["merchants"], 1)
            self.assertEqual(push["pushed"]["products"], 1)

            search = json.loads(
                self.run_cli(
                    buyer_file,
                    "registry",
                    "search-products",
                    "--url",
                    base_url,
                    "--allow-insecure-localhost",
                    "--query",
                    "longjing tea",
                    "--max-price",
                    "100",
                    "--format",
                    "json",
                )
            )
            self.assertEqual(search["results"][0]["sku"], "tea-a")
            self.assertEqual(search["results"][0]["merchant"]["id"], "seller-a")

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
            self.assertEqual(message["message"]["merchant_id"], "seller-a")

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
                    "--offer-price",
                    "86",
                    "--format",
                    "json",
                )
            )
            self.assertEqual(order["order"]["status"], "draft")
            self.assertEqual(order["order"]["merchant_id"], "seller-a")

            pull = json.loads(
                self.run_cli(
                    seller_file,
                    "registry",
                    "pull",
                    "--url",
                    base_url,
                    "--api-key",
                    "seller-token",
                    "--confirm",
                    "--allow-insecure-localhost",
                    "--merchant",
                    "seller-a",
                    "--format",
                    "json",
                )
            )
            self.assertEqual(pull["pulled"]["messages"], 1)
            self.assertEqual(pull["pulled"]["orders"], 1)

            seller_store = json.loads(seller_file.read_text(encoding="utf-8"))
            self.assertEqual(seller_store["messages"][0]["text"], "Can this ship today?")
            self.assertEqual(seller_store["orders"]["ORD-0001"]["buyer_id"], "alice")
            self.assertEqual(seller_store["sync"]["remote_marketplace_url"], base_url)

            registry_store = json.loads(registry_file.read_text(encoding="utf-8"))
            self.assertIn("seller-a", registry_store["merchants"])
            self.assertIn("tea-a", registry_store["products"])
            self.assertEqual(len(registry_store["messages"]), 1)
            self.assertIn("ORD-0001", registry_store["orders"])


if __name__ == "__main__":
    unittest.main()
