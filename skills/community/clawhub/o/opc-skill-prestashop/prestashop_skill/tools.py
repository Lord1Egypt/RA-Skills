import re
from typing import Dict, Any, List, Optional
from .client import PrestaShopClient, PrestaShopAPIError

def clean_html(raw_html: str) -> str:
    """Removes HTML tags and normalizes whitespace in text strings."""
    if not raw_html or not isinstance(raw_html, str):
        return ""
    clean = re.sub(r'<br\s*/?>', '\n', raw_html, flags=re.IGNORECASE)
    clean = re.sub(r'</p>', '\n', clean, flags=re.IGNORECASE)
    clean = re.sub(r'<[^>]+>', '', clean)
    clean = re.sub(r'\n\s*\n', '\n\n', clean)
    return clean.strip()

class PrestaShopSalesTools:
    """
    OpenClaw Skill Tools layer for PrestaShop Virtual Sales Assistant.
    Exposes 4 key tools:
    - buscar_produtos
    - consultar_detalhes_produto
    - verificar_disponibilidade
    - listar_por_categoria
    """

    def __init__(self, client: PrestaShopClient):
        self.client = client

    def buscar_produtos(self, termo_de_busca: str) -> Dict[str, Any]:
        """
        Consulta a API do PrestaShop para encontrar produtos que correspondam à intenção ou termo de busca do usuário.
        
        Args:
            termo_de_busca (str): Nome ou palavra-chave do produto desejado.

        Returns:
            Dict[str, Any]: Lista de produtos encontrados com IDs, nomes, preços e categorias.
        """
        try:
            # Query products with full display or filtered by name
            params = {
                "display": "full",
                "filter[name]": f"%{termo_de_busca}%"
            }
            res = self.client.request("products", params=params)

            products_raw = res.get("products", [])
            if isinstance(products_raw, dict) and "product" in products_raw:
                products_raw = products_raw["product"]
            if isinstance(products_raw, dict):
                products_raw = [products_raw]

            # If filter returned nothing, fetch full list and search in name/description locally
            if not products_raw:
                full_res = self.client.request("products", params={"display": "full"})
                all_prods = full_res.get("products", [])
                if isinstance(all_prods, dict) and "product" in all_prods:
                    all_prods = all_prods["product"]
                if isinstance(all_prods, dict):
                    all_prods = [all_prods]

                termo_lower = termo_de_busca.lower()
                products_raw = []
                for p in all_prods:
                    name = str(p.get("name", "")).lower()
                    desc = str(p.get("description_short", "")).lower()
                    if termo_lower in name or termo_lower in desc:
                        products_raw.append(p)

            results = []
            for p in products_raw[:10]: # Limit to 10 top matches
                prod_id = int(p.get("id", 0))
                name = p.get("name", "Produto Sem Nome")
                price = float(p.get("price", 0.0))
                cat_id = int(p.get("id_category_default", 0))
                short_desc = clean_html(str(p.get("description_short", "")))

                results.append({
                    "id_produto": prod_id,
                    "nome": name,
                    "preco": round(price, 2),
                    "id_categoria": cat_id,
                    "resumo": short_desc[:150] + ("..." if len(short_desc) > 150 else "")
                })

            return {
                "sucesso": True,
                "termo_buscado": termo_de_busca,
                "total_encontrados": len(results),
                "produtos": results
            }

        except PrestaShopAPIError as e:
            return {"sucesso": False, "mensagem": str(e), "produtos": []}

    def consultar_detalhes_produto(self, id_produto: int) -> Dict[str, Any]:
        """
        Retorna o preço atualizado, descrição completa, variações e link da imagem de um produto específico.
        
        Args:
            id_produto (int): ID único do produto no PrestaShop.

        Returns:
            Dict[str, Any]: Detalhes completos do produto.
        """
        try:
            res = self.client.request(f"products/{id_produto}", params={"display": "full"})
            
            product_data = res.get("product") or res.get("products")
            if isinstance(product_data, list) and product_data:
                product_data = product_data[0]

            if not product_data or not isinstance(product_data, dict):
                return {
                    "sucesso": False,
                    "mensagem": f"Produto ID {id_produto} não foi encontrado no catálogo.",
                    "produto": None
                }

            name = product_data.get("name", "Produto")
            price = float(product_data.get("price", 0.0))
            cat_id = int(product_data.get("id_category_default", 0))
            full_desc = clean_html(str(product_data.get("description", "")))
            short_desc = clean_html(str(product_data.get("description_short", "")))
            image_id = product_data.get("id_default_image", "")

            image_url = ""
            if image_id:
                image_url = f"{self.client.config.shop_url}/api/images/products/{id_produto}/{image_id}"

            # Variations/Combinations if present
            associations = product_data.get("associations", {})
            combinations = []
            if isinstance(associations, dict) and "combinations" in associations:
                comb_list = associations["combinations"]
                if isinstance(comb_list, dict) and "combination" in comb_list:
                    comb_list = comb_list["combination"]
                if isinstance(comb_list, list):
                    combinations = [c.get("id") for c in comb_list if isinstance(c, dict) and "id" in c]

            return {
                "sucesso": True,
                "produto": {
                    "id_produto": int(id_produto),
                    "nome": name,
                    "preco": round(price, 2),
                    "id_categoria_padrao": cat_id,
                    "descricao_curta": short_desc,
                    "descricao_completa": full_desc or short_desc,
                    "imagem_url": image_url,
                    "possui_variacoes": len(combinations) > 0,
                    "total_variacoes": len(combinations)
                }
            }

        except PrestaShopAPIError as e:
            return {"sucesso": False, "mensagem": str(e), "produto": None}

    def verificar_disponibilidade(self, id_produto: int) -> Dict[str, Any]:
        """
        Checa no Web Service do PrestaShop se o item está em estoque e qual a quantidade real disponível.
        
        Args:
            id_produto (int): ID único do produto a ser verificado.

        Returns:
            Dict[str, Any]: Status de disponibilidade e quantidade disponível.
        """
        try:
            params = {
                "display": "full",
                "filter[id_product]": str(id_produto)
            }
            res = self.client.request("stock_availables", params=params)

            stocks_raw = res.get("stock_availables", [])
            if isinstance(stocks_raw, dict) and "stock_available" in stocks_raw:
                stocks_raw = stocks_raw["stock_available"]
            if isinstance(stocks_raw, dict):
                stocks_raw = [stocks_raw]

            total_qty = 0
            for stock in stocks_raw:
                qty = int(stock.get("quantity", 0))
                total_qty += qty

            em_estoque = total_qty > 0

            return {
                "sucesso": True,
                "id_produto": int(id_produto),
                "em_estoque": em_estoque,
                "quantidade_disponivel": total_qty,
                "mensagem": f"Item em estoque ({total_qty} unidades disponíveis)." if em_estoque else "Item esgotado no momento."
            }

        except PrestaShopAPIError as e:
            return {
                "sucesso": False,
                "id_produto": int(id_produto),
                "em_estoque": False,
                "quantidade_disponivel": 0,
                "mensagem": str(e)
            }

    def listar_por_categoria(self, id_categoria: int) -> Dict[str, Any]:
        """
        Busca opções de produtos dentro de uma categoria/departamento específico para oferecer alternativas ao cliente.
        
        Args:
            id_categoria (int): ID da categoria no PrestaShop.

        Returns:
            Dict[str, Any]: Lista de produtos pertencentes à categoria especificada.
        """
        try:
            params = {
                "display": "full",
                "filter[id_category_default]": str(id_categoria)
            }
            res = self.client.request("products", params=params)

            products_raw = res.get("products", [])
            if isinstance(products_raw, dict) and "product" in products_raw:
                products_raw = products_raw["product"]
            if isinstance(products_raw, dict):
                products_raw = [products_raw]

            alternativas = []
            for p in products_raw:
                p_id = int(p.get("id", 0))
                name = p.get("name", "Produto")
                price = float(p.get("price", 0.0))
                short_desc = clean_html(str(p.get("description_short", "")))

                alternativas.append({
                    "id_produto": p_id,
                    "nome": name,
                    "preco": round(price, 2),
                    "id_categoria": int(id_categoria),
                    "resumo": short_desc[:120] + ("..." if len(short_desc) > 120 else "")
                })

            return {
                "sucesso": True,
                "id_categoria": int(id_categoria),
                "total_produtos": len(alternativas),
                "produtos": alternativas
            }

        except PrestaShopAPIError as e:
            return {
                "sucesso": False,
                "id_categoria": int(id_categoria),
                "mensagem": str(e),
                "produtos": []
            }
