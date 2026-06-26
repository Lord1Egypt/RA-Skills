#!/usr/bin/env python3
"""Helper CLI API-first para Mercado Público (capa read-only).

Requiere ticket en variable de entorno MERCADO_PUBLICO_API_TICKET.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

API_BASE = "https://api.mercadopublico.cl/servicios/v1"
DEFAULT_TIMEOUT = 15
DEFAULT_MAX_RETRIES = 2
DEFAULT_BACKOFF_SECONDS = 1.0
DEFAULT_CACHE_TTL = 0
TICKET_ENV = "MERCADO_PUBLICO_API_TICKET"
DEFAULT_CACHE_DIR = Path(__file__).resolve().parents[1] / "run" / "api-cache"
SUMMARY_VERSION = "1"


class ApiError(Exception):
    pass


def _extract_10500(payload: Any) -> bool:
    if isinstance(payload, dict):
        code = payload.get("Codigo")
        msg = str(payload.get("Mensaje", "")).lower()
        if code == 10500 or "peticiones simult" in msg:
            return True
    return False


def _do_request(url: str, timeout: int) -> Any:
    req = urllib.request.Request(url, headers={"Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as response:
        raw = response.read().decode("utf-8", errors="replace")
    try:
        return json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ApiError(f"Respuesta no es JSON válido: {exc}") from exc


def fetch_with_retry(url: str, timeout: int, max_retries: int, backoff_seconds: float) -> Any:
    attempt = 0
    while True:
        try:
            payload = _do_request(url, timeout=timeout)
            if _extract_10500(payload):
                if attempt >= max_retries:
                    raise ApiError(
                        "API respondió Codigo 10500 (peticiones simultáneas). "
                        "Reintentos agotados; prueba más tarde o serializa aún más las llamadas."
                    )
                time.sleep(backoff_seconds * (attempt + 1))
                attempt += 1
                continue
            return payload
        except urllib.error.HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace") if exc.fp else ""
            if exc.code >= 500 and attempt < max_retries:
                time.sleep(backoff_seconds * (attempt + 1))
                attempt += 1
                continue
            raise ApiError(f"HTTP {exc.code}: {body[:500]}") from exc
        except urllib.error.URLError as exc:
            if attempt < max_retries:
                time.sleep(backoff_seconds * (attempt + 1))
                attempt += 1
                continue
            raise ApiError(f"Error de red/timeout: {exc}") from exc


def build_url(path: str, ticket: str, params: dict[str, Any]) -> str:
    clean = {k: str(v) for k, v in params.items() if v is not None and str(v) != ""}
    clean["ticket"] = ticket
    query = urllib.parse.urlencode(clean)
    return f"{API_BASE}{path}?{query}"


def _normalize_url_for_cache(url: str) -> str:
    parsed = urllib.parse.urlparse(url)
    query_pairs = urllib.parse.parse_qsl(parsed.query, keep_blank_values=False)
    query_pairs.sort(key=lambda pair: pair[0])
    normalized_query = urllib.parse.urlencode(query_pairs)
    return urllib.parse.urlunparse((parsed.scheme, parsed.netloc, parsed.path, "", normalized_query, ""))


def _cache_file_path(cache_dir: Path, url: str) -> Path:
    normalized = _normalize_url_for_cache(url)
    digest = hashlib.sha256(normalized.encode("utf-8")).hexdigest()
    return cache_dir / f"{digest}.json"


def _read_cache(cache_path: Path) -> dict[str, Any] | None:
    try:
        raw = cache_path.read_text(encoding="utf-8")
        data = json.loads(raw)
        if not isinstance(data, dict):
            return None
        if "payload" not in data or "fetched_at" not in data:
            return None
        return data
    except (OSError, json.JSONDecodeError):
        return None


def _write_cache(cache_path: Path, url: str, payload: Any) -> None:
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    data = {
        "url": _normalize_url_for_cache(url),
        "fetched_at": int(time.time()),
        "payload": payload,
    }
    tmp_path = cache_path.with_suffix(".tmp")
    tmp_path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    tmp_path.replace(cache_path)


def fetch_with_optional_cache(
    url: str,
    timeout: int,
    max_retries: int,
    backoff_seconds: float,
    cache_ttl: int,
    cache_dir: Path,
) -> tuple[Any, dict[str, Any]]:
    if cache_ttl <= 0:
        payload = fetch_with_retry(url, timeout, max_retries, backoff_seconds)
        return payload, {"source": "api", "cache_enabled": False}

    cache_path = _cache_file_path(cache_dir, url)
    cached = _read_cache(cache_path)
    now = int(time.time())
    if cached is not None:
        age = max(0, now - int(cached.get("fetched_at", now)))
        if age <= cache_ttl:
            return cached["payload"], {
                "source": "cache",
                "cache_enabled": True,
                "cache_age_seconds": age,
                "cache_ttl_seconds": cache_ttl,
            }

    payload = fetch_with_retry(url, timeout, max_retries, backoff_seconds)
    _write_cache(cache_path, url, payload)
    return payload, {
        "source": "api",
        "cache_enabled": True,
        "cache_age_seconds": 0,
        "cache_ttl_seconds": cache_ttl,
    }


def _items_from_payload(payload: Any) -> list[Any] | None:
    if isinstance(payload, list):
        return payload
    if not isinstance(payload, dict):
        return None
    for key in (
        "Listado",
        "Lista",
        "ListaCompradores",
        "ListaEmpresas",
        "Licitaciones",
        "OrdenesDeCompra",
        "Items",
    ):
        value = payload.get(key)
        if isinstance(value, list):
            return value
    for value in payload.values():
        if isinstance(value, list):
            return value
    return None


def _contains_filter(value: Any, needle: str) -> bool:
    if isinstance(value, dict):
        return any(_contains_filter(v, needle) for v in value.values())
    if isinstance(value, list):
        return any(_contains_filter(v, needle) for v in value)
    return needle in str(value).lower()


def maybe_filter_payload(payload: Any, text_filter: str | None) -> Any:
    if not text_filter:
        return payload
    items = _items_from_payload(payload)
    if items is None:
        return payload
    needle = text_filter.lower()
    filtered = [item for item in items if _contains_filter(item, needle)]
    if isinstance(payload, list):
        return filtered
    clone = dict(payload)
    for key, value in payload.items():
        if isinstance(value, list):
            clone[key] = filtered
            break
    clone["_meta_filter"] = {
        "filter": text_filter,
        "original_count": len(items),
        "filtered_count": len(filtered),
    }
    return clone


def _as_item_list(payload: Any) -> list[dict[str, Any]]:
    items = _items_from_payload(payload)
    if items is not None:
        return [item for item in items if isinstance(item, dict)]
    if isinstance(payload, dict):
        return [payload]
    return []


def _sanitize_value(value: Any) -> str:
    if value is None:
        return "-"
    text = str(value).strip()
    if not text:
        return "-"
    return " ".join(text.split())


def _pick(item: dict[str, Any], *candidates: str) -> str:
    for key in candidates:
        if key in item and item.get(key) not in (None, ""):
            return _sanitize_value(item.get(key))
    return "-"


def _emit_summary(lines: list[tuple[str, Any]]) -> None:
    for key, value in lines:
        print(f"{key}={_sanitize_value(value)}")


def print_summary(command: str, args: argparse.Namespace, payload: Any, meta: dict[str, Any]) -> None:
    items = _as_item_list(payload)
    first = items[0] if items else {}

    lines: list[tuple[str, Any]] = [
        ("summary_version", SUMMARY_VERSION),
        ("command", command),
        ("source", meta.get("source", "api")),
        ("count", len(items)),
    ]

    if meta.get("cache_enabled"):
        lines.append(("cache_ttl_seconds", meta.get("cache_ttl_seconds", "-")))
        lines.append(("cache_age_seconds", meta.get("cache_age_seconds", "-")))

    if command == "buscar-proveedor":
        lines.extend(
            [
                ("query_rut", args.rut),
                ("first_rut", _pick(first, "RutEmpresa", "Rut", "RutProveedor")),
                ("first_nombre", _pick(first, "NombreEmpresa", "Nombre", "RazonSocial")),
                ("first_codigo", _pick(first, "CodigoEmpresa", "Codigo", "CodigoProveedor")),
            ]
        )
    elif command == "buscar-comprador":
        lines.extend(
            [
                ("query_filter", args.filter or "-"),
                (
                    "filter_count",
                    payload.get("_meta_filter", {}).get("filtered_count", "-") if isinstance(payload, dict) else "-",
                ),
                ("first_codigo_organismo", _pick(first, "CodigoOrganismo", "Codigo")),
                ("first_nombre", _pick(first, "NombreOrganismo", "Nombre", "RazonSocial")),
            ]
        )
    elif command == "licitaciones":
        mode = "codigo" if args.codigo else "fecha"
        lines.extend(
            [
                ("query_mode", mode),
                ("query_codigo", args.codigo or "-"),
                ("query_fecha", args.fecha or "-"),
                ("query_estado", args.estado or "-"),
                ("query_codigo_organismo", args.codigo_organismo or "-"),
                ("query_codigo_proveedor", args.codigo_proveedor or "-"),
                ("first_codigo", _pick(first, "CodigoExterno", "Codigo")),
                ("first_estado", _pick(first, "Estado", "CodigoEstado")),
                ("first_nombre", _pick(first, "Nombre")),
            ]
        )
    elif command == "ordenes":
        mode = "codigo" if args.codigo else "fecha"
        lines.extend(
            [
                ("query_mode", mode),
                ("query_codigo", args.codigo or "-"),
                ("query_fecha", args.fecha or "-"),
                ("query_estado", args.estado or "-"),
                ("query_codigo_organismo", args.codigo_organismo or "-"),
                ("query_codigo_proveedor", args.codigo_proveedor or "-"),
                ("first_codigo", _pick(first, "Codigo")),
                ("first_estado", _pick(first, "EstadoProveedor", "CodigoEstado", "Estado")),
                ("first_codigo_licitacion", _pick(first, "CodigoLicitacion")),
                ("first_total", _pick(first, "Total")),
            ]
        )
    else:
        lines.append(("detail", "summary_not_defined_for_command"))

    _emit_summary(lines)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Helper API pública Mercado Público (read-only)")
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT, help="Timeout por request (segundos)")
    parser.add_argument("--max-retries", type=int, default=DEFAULT_MAX_RETRIES, help="Reintentos suaves")
    parser.add_argument("--backoff", type=float, default=DEFAULT_BACKOFF_SECONDS, help="Backoff base (segundos)")
    parser.add_argument("--summary", action="store_true", help="Mostrar resumen estable (clave=valor) en vez de JSON")
    parser.add_argument(
        "--cache-ttl",
        type=int,
        default=DEFAULT_CACHE_TTL,
        help="TTL de caché local (segundos). 0 desactiva caché",
    )
    parser.add_argument(
        "--cache-dir",
        help=f"Directorio de caché (default: {DEFAULT_CACHE_DIR})",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    p_prov = subparsers.add_parser("buscar-proveedor", help="Empresas/BuscarProveedor por RUT")
    p_prov.add_argument("--rut", required=True, help="RUT proveedor")

    p_comp = subparsers.add_parser("buscar-comprador", help="Empresas/BuscarComprador")
    p_comp.add_argument("--filter", help="Filtro textual local sobre la respuesta")

    p_lic = subparsers.add_parser("licitaciones", help="Consultar licitaciones por código o fecha")
    group_lic = p_lic.add_mutually_exclusive_group(required=True)
    group_lic.add_argument("--codigo", help="Código de licitación, ej: 1509-5-L114")
    group_lic.add_argument("--fecha", help="Fecha DDMMAAAA")
    p_lic.add_argument("--estado", help="Estado textual o numérico")
    p_lic.add_argument("--codigo-organismo", type=int, dest="codigo_organismo")
    p_lic.add_argument("--codigo-proveedor", type=int, dest="codigo_proveedor")

    p_oc = subparsers.add_parser("ordenes", help="Consultar órdenes de compra por código o fecha")
    group_oc = p_oc.add_mutually_exclusive_group(required=True)
    group_oc.add_argument("--codigo", help="Código de OC, ej: 2097-241-SE14")
    group_oc.add_argument("--fecha", help="Fecha DDMMAAAA")
    p_oc.add_argument("--estado", help="Estado textual o numérico")
    p_oc.add_argument("--codigo-organismo", type=int, dest="codigo_organismo")
    p_oc.add_argument("--codigo-proveedor", type=int, dest="codigo_proveedor")

    return parser


def command_to_request(args: argparse.Namespace, ticket: str) -> tuple[str, str]:
    if args.command == "buscar-proveedor":
        url = build_url(
            "/Publico/Empresas/BuscarProveedor",
            ticket,
            {"rutempresaproveedor": args.rut},
        )
        return args.command, url

    if args.command == "buscar-comprador":
        url = build_url("/Publico/Empresas/BuscarComprador", ticket, {})
        return args.command, url

    if args.command == "licitaciones":
        url = build_url(
            "/publico/licitaciones.json",
            ticket,
            {
                "codigo": args.codigo,
                "fecha": args.fecha,
                "estado": args.estado,
                "CodigoOrganismo": args.codigo_organismo,
                "CodigoProveedor": args.codigo_proveedor,
            },
        )
        return args.command, url

    if args.command == "ordenes":
        url = build_url(
            "/publico/ordenesdecompra.json",
            ticket,
            {
                "codigo": args.codigo,
                "fecha": args.fecha,
                "estado": args.estado,
                "CodigoOrganismo": args.codigo_organismo,
                "CodigoProveedor": args.codigo_proveedor,
            },
        )
        return args.command, url

    raise ApiError(f"Comando no soportado: {args.command}")


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    ticket = os.getenv(TICKET_ENV)
    if not ticket:
        print(
            f"Falta ticket API. Exporta {TICKET_ENV} antes de usar este helper.\n"
            f"Ejemplo: export {TICKET_ENV}='TU_TICKET'",
            file=sys.stderr,
        )
        return 2

    cache_dir = Path(args.cache_dir).expanduser() if args.cache_dir else DEFAULT_CACHE_DIR

    try:
        command, url = command_to_request(args, ticket)
        payload, fetch_meta = fetch_with_optional_cache(
            url=url,
            timeout=args.timeout,
            max_retries=args.max_retries,
            backoff_seconds=args.backoff,
            cache_ttl=args.cache_ttl,
            cache_dir=cache_dir,
        )

        if command == "buscar-comprador":
            payload = maybe_filter_payload(payload, args.filter)

        if args.summary:
            print_summary(command, args, payload, fetch_meta)
        else:
            print(json.dumps(payload, indent=2, ensure_ascii=False))
        return 0
    except ApiError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
