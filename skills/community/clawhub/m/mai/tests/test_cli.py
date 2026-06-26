import json
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import mai  # noqa: E402


class MaiCliTest(unittest.TestCase):
    def run_cli(self, data_file, *args):
        output = StringIO()
        with redirect_stdout(output):
            mai.main(["--data", str(data_file), *args])
        return output.getvalue()

    def read_store(self, data_file):
        return json.loads(Path(data_file).read_text(encoding="utf-8"))

    def test_full_shopping_match_workflow(self):
        with tempfile.TemporaryDirectory() as tmp:
            data_file = Path(tmp) / "mai.json"

            self.run_cli(
                data_file,
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
                data_file,
                "merchant",
                "create",
                "--id",
                "seller-b",
                "--name",
                "City Tea Market",
                "--city",
                "Shanghai",
                "--contact",
                "phone:10086",
                "--tags",
                "tea,wholesale",
            )
            self.run_cli(
                data_file,
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
                "--description",
                "Fresh spring tea gift box",
                "--shipping",
                "same-city courier",
            )
            self.run_cli(
                data_file,
                "product",
                "add",
                "--merchant",
                "seller-b",
                "--sku",
                "tea-b",
                "--title",
                "Longjing Family Pack",
                "--price",
                "96",
                "--stock",
                "8",
                "--category",
                "tea",
                "--tags",
                "longjing,value",
                "--shipping",
                "express",
            )
            self.run_cli(
                data_file,
                "review",
                "add",
                "--buyer",
                "alice",
                "--merchant",
                "seller-a",
                "--sku",
                "tea-a",
                "--rating",
                "5",
                "--comment",
                "Packaging was clean and delivery was fast.",
            )

            search = json.loads(
                self.run_cli(
                    data_file,
                    "search",
                    "products",
                    "--query",
                    "longjing tea",
                    "--max-price",
                    "100",
                    "--format",
                    "json",
                )
            )
            self.assertEqual([item["sku"] for item in search["results"]], ["tea-a", "tea-b"])
            self.assertEqual(search["results"][0]["merchant"]["id"], "seller-a")
            self.assertIn("in stock", search["results"][0]["reasons"])

            comparison = json.loads(
                self.run_cli(data_file, "compare", "--skus", "tea-a,tea-b", "--format", "json")
            )
            self.assertEqual(comparison["best_value"]["sku"], "tea-a")
            self.assertEqual(comparison["items"][0]["price"], 88.0)
            self.assertEqual(comparison["items"][1]["price_delta"], 8.0)

            self.run_cli(
                data_file,
                "message",
                "add",
                "--buyer",
                "alice",
                "--merchant",
                "seller-a",
                "--sku",
                "tea-a",
                "--text",
                "Can you ship this today?",
            )
            order_output = self.run_cli(
                data_file,
                "order",
                "create",
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
                "--note",
                "Gift order for tomorrow",
            )
            self.assertIn("Order created: ORD-0001", order_output)
            self.run_cli(
                data_file,
                "order",
                "quote",
                "--merchant",
                "seller-a",
                "--order",
                "ORD-0001",
                "--unit-price",
                "86",
                "--payment-url",
                "https://pay.example/orders/ORD-0001",
                "--terms",
                "External payment; seller ships after payment reference is recorded.",
            )
            self.run_cli(
                data_file,
                "order",
                "update",
                "--order",
                "ORD-0001",
                "--status",
                "confirmed",
                "--actor",
                "merchant",
                "--note",
                "Stock reserved.",
            )
            self.run_cli(
                data_file,
                "order",
                "update",
                "--order",
                "ORD-0001",
                "--status",
                "paid_external",
                "--actor",
                "buyer",
                "--payment-reference",
                "wx-20260503-1",
            )
            self.run_cli(
                data_file,
                "order",
                "update",
                "--order",
                "ORD-0001",
                "--status",
                "fulfilled",
                "--actor",
                "merchant",
                "--tracking",
                "SF123",
            )
            self.run_cli(
                data_file,
                "order",
                "update",
                "--order",
                "ORD-0001",
                "--status",
                "completed",
                "--actor",
                "buyer",
            )

            store = self.read_store(data_file)
            self.assertEqual(store["products"]["tea-a"]["stock"], 3)
            self.assertEqual(store["orders"]["ORD-0001"]["status"], "completed")
            self.assertEqual(store["orders"]["ORD-0001"]["payment_reference"], "wx-20260503-1")
            self.assertEqual(store["orders"]["ORD-0001"]["tracking"], "SF123")
            self.assertEqual(len(store["messages"]), 1)
            self.assertEqual(store["reviews"][0]["rating"], 5)
            self.assertEqual(store["sync"]["mode"], "local-first")

    def test_order_confirmation_rejects_insufficient_stock(self):
        with tempfile.TemporaryDirectory() as tmp:
            data_file = Path(tmp) / "mai.json"
            self.run_cli(data_file, "merchant", "create", "--id", "seller", "--name", "Tiny Shop")
            self.run_cli(
                data_file,
                "product",
                "add",
                "--merchant",
                "seller",
                "--sku",
                "one-item",
                "--title",
                "Single Item",
                "--price",
                "10",
                "--stock",
                "1",
            )
            self.run_cli(
                data_file,
                "order",
                "create",
                "--buyer",
                "bob",
                "--merchant",
                "seller",
                "--sku",
                "one-item",
                "--quantity",
                "2",
            )

            with self.assertRaises(SystemExit):
                self.run_cli(
                    data_file,
                    "order",
                    "update",
                    "--order",
                    "ORD-0001",
                    "--status",
                    "confirmed",
                    "--actor",
                    "merchant",
                )

            store = self.read_store(data_file)
            self.assertEqual(store["products"]["one-item"]["stock"], 1)
            self.assertEqual(store["orders"]["ORD-0001"]["status"], "draft")

    def test_invalid_order_transition_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            data_file = Path(tmp) / "mai.json"
            self.run_cli(data_file, "merchant", "create", "--id", "seller", "--name", "Tiny Shop")
            self.run_cli(
                data_file,
                "product",
                "add",
                "--merchant",
                "seller",
                "--sku",
                "item",
                "--title",
                "Item",
                "--price",
                "10",
                "--stock",
                "3",
            )
            self.run_cli(
                data_file,
                "order",
                "create",
                "--buyer",
                "bob",
                "--merchant",
                "seller",
                "--sku",
                "item",
                "--quantity",
                "1",
            )

            with self.assertRaises(SystemExit):
                self.run_cli(
                    data_file,
                    "order",
                    "update",
                    "--order",
                    "ORD-0001",
                    "--status",
                    "completed",
                    "--actor",
                    "buyer",
                )

