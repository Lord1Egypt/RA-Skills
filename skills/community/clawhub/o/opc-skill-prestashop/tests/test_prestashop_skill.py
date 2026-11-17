import unittest
from unittest.mock import MagicMock, patch
import json
import time
import urllib.error

from prestashop_skill.config import PrestaShopConfig
from prestashop_skill.cache import SimpleMemoryCache
from prestashop_skill.client import PrestaShopClient, PrestaShopReadOnlyError, PrestaShopAPIError
from prestashop_skill.tools import PrestaShopSalesTools, clean_html
from prestashop_skill.persona import get_sales_assistant_prompt

class TestPrestaShopConfig(unittest.TestCase):
    def test_config_validation(self):
        config = PrestaShopConfig(shop_url="https://lojadetestes.com", api_key="KEY12345")
        config.validate()
        self.assertEqual(config.shop_url, "https://lojadetestes.com")
        self.assertEqual(config.api_key, "KEY12345")

    def test_invalid_config(self):
        config = PrestaShopConfig(shop_url="", api_key="")
        with self.assertRaises(ValueError):
            config.validate()

    def test_api_key_masking(self):
        config = PrestaShopConfig(shop_url="https://lojadetestes.com", api_key="SECRET_KEY_999")
        log_msg = "Request to https://SECRET_KEY_999@lojadetestes.com/api/products?ws_key=SECRET_KEY_999"
        sanitized = config.sanitize_log_message(log_msg)
        self.assertNotIn("SECRET_KEY_999", sanitized)
        self.assertIn("********", sanitized)


class TestSimpleMemoryCache(unittest.TestCase):
    def test_cache_set_get(self):
        cache = SimpleMemoryCache(default_ttl=5)
        cache.set("key1", {"data": "test"})
        self.assertEqual(cache.get("key1"), {"data": "test"})

    def test_cache_expiration(self):
        cache = SimpleMemoryCache(default_ttl=1)
        cache.set("key1", "val1", ttl=1)
        self.assertEqual(cache.get("key1"), "val1")
        time.sleep(1.1)
        self.assertIsNone(cache.get("key1"))

    def test_cache_delete_clear(self):
        cache = SimpleMemoryCache()
        cache.set("k1", "v1")
        cache.set("k2", "v2")
        cache.delete("k1")
        self.assertIsNone(cache.get("k1"))
        cache.clear()
        self.assertIsNone(cache.get("k2"))


class TestPrestaShopClient(unittest.TestCase):
    def setUp(self):
        self.config = PrestaShopConfig(shop_url="https://lojadetestes.com", api_key="KEY123")
        self.cache = SimpleMemoryCache()
        self.client = PrestaShopClient(self.config, self.cache)

    def test_read_only_enforcement(self):
        """Verifies that non-GET requests are strictly rejected."""
        with self.assertRaises(PrestaShopReadOnlyError):
            self.client.request("products", method="POST")
        with self.assertRaises(PrestaShopReadOnlyError):
            self.client.request("products", method="PUT")
        with self.assertRaises(PrestaShopReadOnlyError):
            self.client.request("products", method="DELETE")

    @patch("urllib.request.urlopen")
    def test_json_response_parsing(self, mock_urlopen):
        mock_response = MagicMock()
        mock_response.headers = {"Content-Type": "application/json"}
        mock_response.read.return_value = json.dumps({
            "products": [
                {"id": 1, "name": "Camiseta", "price": "49.90", "id_category_default": 2}
            ]
        }).encode("utf-8")
        mock_urlopen.return_value.__enter__.return_value = mock_response

        res = self.client.request("products", use_cache=False)
        self.assertIn("products", res)
        self.assertEqual(len(res["products"]), 1)
        self.assertEqual(res["products"][0]["name"], "Camiseta")

    @patch("urllib.request.urlopen")
    def test_xml_fallback_parsing(self, mock_urlopen):
        mock_response = MagicMock()
        mock_response.headers = {"Content-Type": "application/xml"}
        xml_data = """<?xml version="1.0" encoding="UTF-8"?>
        <prestashop>
            <product>
                <id>10</id>
                <name><language id="1">Sapato de Couro</language></name>
                <price>199.90</price>
            </product>
        </prestashop>"""
        mock_response.read.return_value = xml_data.encode("utf-8")
        mock_urlopen.return_value.__enter__.return_value = mock_response

        res = self.client.request("products/10", use_cache=False)
        self.assertIn("product", res)
        self.assertEqual(res["product"]["name"], "Sapato de Couro")
        self.assertEqual(res["product"]["price"], "199.90")

    @patch("urllib.request.urlopen")
    def test_graceful_error_handling(self, mock_urlopen):
        mock_urlopen.side_effect = urllib.error.URLError("Connection refused")
        with self.assertRaises(PrestaShopAPIError) as ctx:
            self.client.request("products", use_cache=False)
        self.assertIn("No momento meu sistema de consultas está atualizando", str(ctx.exception))


class TestPrestaShopSalesTools(unittest.TestCase):
    def setUp(self):
        self.config = PrestaShopConfig(shop_url="https://lojadetestes.com", api_key="KEY123")
        self.client = PrestaShopClient(self.config, SimpleMemoryCache())
        self.tools = PrestaShopSalesTools(self.client)

    @patch.object(PrestaShopClient, "request")
    def test_buscar_produtos(self, mock_request):
        mock_request.return_value = {
            "products": [
                {
                    "id": 1,
                    "name": "Camiseta Polo azul",
                    "price": 79.90,
                    "id_category_default": 5,
                    "description_short": "<p>Camiseta de algodão alta qualidade</p>"
                }
            ]
        }
        res = self.tools.buscar_produtos("Polo")
        self.assertTrue(res["sucesso"])
        self.assertEqual(res["total_encontrados"], 1)
        self.assertEqual(res["produtos"][0]["nome"], "Camiseta Polo azul")
        self.assertEqual(res["produtos"][0]["preco"], 79.90)

    @patch.object(PrestaShopClient, "request")
    def test_consultar_detalhes_produto(self, mock_request):
        mock_request.return_value = {
            "product": {
                "id": 42,
                "name": "Tênis Esportivo",
                "price": 299.90,
                "id_category_default": 10,
                "description": "<p>Tênis ideal para corridas e treinos.</p>",
                "description_short": "Tênis leve e confortável",
                "id_default_image": "105"
            }
        }
        res = self.tools.consultar_detalhes_produto(42)
        self.assertTrue(res["sucesso"])
        prod = res["produto"]
        self.assertEqual(prod["id_produto"], 42)
        self.assertEqual(prod["nome"], "Tênis Esportivo")
        self.assertIn("Tênis ideal para corridas", prod["descricao_completa"])
        self.assertEqual(prod["imagem_url"], "https://lojadetestes.com/api/images/products/42/105")

    @patch.object(PrestaShopClient, "request")
    def test_verificar_disponibilidade_em_estoque(self, mock_request):
        mock_request.return_value = {
            "stock_availables": [
                {"id": 1, "id_product": 10, "quantity": 5}
            ]
        }
        res = self.tools.verificar_disponibilidade(10)
        self.assertTrue(res["sucesso"])
        self.assertTrue(res["em_estoque"])
        self.assertEqual(res["quantidade_disponivel"], 5)

    @patch.object(PrestaShopClient, "request")
    def test_verificar_disponibilidade_esgotado(self, mock_request):
        mock_request.return_value = {
            "stock_availables": [
                {"id": 1, "id_product": 12, "quantity": 0}
            ]
        }
        res = self.tools.verificar_disponibilidade(12)
        self.assertTrue(res["sucesso"])
        self.assertFalse(res["em_estoque"])
        self.assertEqual(res["quantidade_disponivel"], 0)

    @patch.object(PrestaShopClient, "request")
    def test_listar_por_categoria(self, mock_request):
        mock_request.return_value = {
            "products": [
                {"id": 101, "name": "Calça Jeans", "price": 120.00, "description_short": "Calça slim"},
                {"id": 102, "name": "Bermuda Cargo", "price": 90.00, "description_short": "Bermuda de sarja"}
            ]
        }
        res = self.tools.listar_por_categoria(5)
        self.assertTrue(res["sucesso"])
        self.assertEqual(res["total_produtos"], 2)
        self.assertEqual(res["produtos"][0]["id_produto"], 101)


class TestPersonaPrompt(unittest.TestCase):
    def test_prompt_content(self):
        prompt = get_sales_assistant_prompt()
        self.assertIn("Consultor de Vendas Virtual", prompt)
        self.assertIn("VERIFICAÇÃO OBRIGATÓRIA DE ESTOQUE", prompt)
        self.assertIn("RECOMENDAÇÃO PROATIVA", prompt)


if __name__ == "__main__":
    unittest.main()
