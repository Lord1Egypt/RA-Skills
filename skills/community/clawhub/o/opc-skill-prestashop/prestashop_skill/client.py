import json
import base64
import urllib.request
import urllib.parse
import urllib.error
import xml.etree.ElementTree as ET
from typing import Dict, Any, Optional, Union
from .config import PrestaShopConfig
from .cache import SimpleMemoryCache

class PrestaShopAPIError(Exception):
    """Base exception for PrestaShop API errors."""
    pass

class PrestaShopReadOnlyError(PermissionError):
    """Exception raised when a non-GET operation is attempted."""
    pass

class PrestaShopClient:
    """
    Read-Only REST Client for PrestaShop Web Services API.
    Enforces security, masks credentials, parses JSON/XML responses,
    and integrates with an in-memory TTL cache.
    """

    ALLOWED_METHODS = {"GET"}

    def __init__(self, config: PrestaShopConfig, cache: Optional[SimpleMemoryCache] = None):
        self.config = config
        self.config.validate()
        self.cache = cache or SimpleMemoryCache(default_ttl=config.cache_ttl_seconds)

    def _get_auth_header(self) -> Dict[str, str]:
        """Generates Basic Auth header using the API key."""
        auth_str = f"{self.config.api_key}:"
        b64_auth = base64.b64encode(auth_str.encode("utf-8")).decode("utf-8")
        return {"Authorization": f"Basic {b64_auth}"}

    def request(self, endpoint: str, params: Optional[Dict[str, Any]] = None, method: str = "GET", use_cache: bool = True) -> Dict[str, Any]:
        """
        Executes a RESTful request against PrestaShop Web Services.
        STRICTLY ENFORCES READ-ONLY (GET ONLY) ACCESS.
        """
        method_upper = method.upper()
        if method_upper not in self.ALLOWED_METHODS:
            raise PrestaShopReadOnlyError(
                f"Operação não permitida: '{method_upper}'. "
                "Esta skill tem permissão apenas de LEITURA (GET) no PrestaShop Web Services."
            )

        endpoint_clean = endpoint.lstrip("/")
        base_url = f"{self.config.shop_url}/api/{endpoint_clean}"
        
        # Prepare query parameters
        queryParams = params.copy() if params else {}
        if "output_format" not in queryParams:
            queryParams["output_format"] = "JSON"

        query_string = urllib.parse.urlencode(queryParams, doseq=True)
        full_url = f"{base_url}?{query_string}" if query_string else base_url

        # Check Cache for GET requests
        cache_key = f"{method_upper}:{full_url}"
        if use_cache:
            cached_data = self.cache.get(cache_key)
            if cached_data is not None:
                return cached_data

        # Prepare HTTP Headers
        headers = self._get_auth_header()
        headers["Output-Format"] = "JSON"
        headers["Accept"] = "application/json, application/xml, text/xml"
        headers["User-Agent"] = "OpenClaw-VirtualSalesAssistant/1.0"

        req = urllib.request.Request(full_url, headers=headers, method=method_upper)

        try:
            with urllib.request.urlopen(req, timeout=self.config.timeout) as response:
                content_type = response.headers.get("Content-Type", "").lower()
                raw_bytes = response.read()
                data = self._parse_response(raw_bytes, content_type)
                
                # Cache response
                if use_cache:
                    self.cache.set(cache_key, data)
                
                return data

        except urllib.error.HTTPError as e:
            error_body = ""
            try:
                error_body = e.read().decode("utf-8", errors="replace")
            except Exception:
                pass
            
            masked_msg = self.config.sanitize_log_message(
                f"Erro na requisição ao PrestaShop (HTTP {e.code}): {e.reason}. Detalhes: {error_body[:200]}"
            )
            if e.code == 404:
                return {}
            raise PrestaShopAPIError("No momento meu sistema de consultas está atualizando, pode aguardar um instante?") from e

        except (urllib.error.URLError, TimeoutError, OSError) as e:
            masked_err = self.config.sanitize_log_message(str(e))
            raise PrestaShopAPIError("No momento meu sistema de consultas está atualizando, pode aguardar um instante?") from e

    def _parse_response(self, raw_bytes: bytes, content_type: str) -> Dict[str, Any]:
        """Parses response as JSON with XML fallback."""
        text = raw_bytes.decode("utf-8", errors="replace").strip()
        if not text:
            return {}

        # Attempt JSON parsing
        if "json" in content_type or text.startswith("{") or text.startswith("["):
            try:
                return json.loads(text)
            except json.JSONDecodeError:
                pass

        # Attempt XML parsing fallback
        try:
            root = ET.fromstring(text)
            return self._xml_element_to_dict(root)
        except ET.ParseError as pe:
            raise PrestaShopAPIError("Resposta do PrestaShop em formato inválido ou corrompido.") from pe

    def _xml_element_to_dict(self, element: ET.Element) -> Union[Dict[str, Any], str]:
        """Converts XML ElementTree structure to python dictionary."""
        # Handle PrestaShop multi-language nodes like <name><language id="1">Text</language></name>
        children = list(element)
        if not children:
            return element.text or ""

        # Check if children are language nodes
        if all(child.tag == "language" for child in children):
            # Prefer first language text
            return children[0].text or ""

        result = {}
        for child in children:
            child_data = self._xml_element_to_dict(child)
            if child.tag in result:
                if isinstance(result[child.tag], list):
                    result[child.tag].append(child_data)
                else:
                    result[child.tag] = [result[child.tag], child_data]
            else:
                result[child.tag] = child_data
        return result
