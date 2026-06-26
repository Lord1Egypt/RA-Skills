"""
Flask API server that proxies to the unified provider services.
"""
from __future__ import annotations

import logging
from typing import Any, Dict

from flask import Flask, jsonify, request

from app.core.logger import setup_logging
from app.services import user_service
from app.services.provider_factory import canonical_name

setup_logging()
logger = logging.getLogger(__name__)
app = Flask(__name__)


def success(payload: Dict[str, Any], status: int = 200):
    return jsonify({"success": True, "data": payload}), status


def failure(message: str, status: int = 400, extra: Dict[str, Any] | None = None):
    body = {"success": False, "message": message}
    if extra:
        body.update(extra)
    return jsonify(body), status


def normalize_provider(name: str) -> str:
    try:
        return canonical_name(name)
    except ValueError as exc:
        raise ValueError(str(exc))


@app.route("/health", methods=["GET"])
def health():
    return success({"status": "ok"})


@app.route("/api/<provider>/init", methods=["POST"])
def init_provider(provider: str):
    provider = normalize_provider(provider)
    metadata = user_service.init_provider(provider)
    products = user_service.list_products(provider)
    return success({"metadata": metadata, "products": products})


@app.route("/api/<provider>/products", methods=["GET"])
def list_products(provider: str):
    provider = normalize_provider(provider)
    cached = user_service.get_cached_state(provider)
    products = cached.get("products")
    if not products:
        products = user_service.list_products(provider)
    return success({"products": products})


@app.route("/api/<provider>/users", methods=["POST"])
def create_user(provider: str):
    provider = normalize_provider(provider)
    payload = request.get_json(force=True) or {}
    identifier = payload.get("identifier")
    if not identifier:
        return failure("Missing identifier", 400)
    product = payload.get("product")
    options = payload.get("options") or {}
    result = user_service.create_user(provider, identifier, product=product, **options)
    return success(result, 201)


@app.route("/api/<provider>/users/<identifier>/assign", methods=["POST"])
def assign_product(provider: str, identifier: str):
    provider = normalize_provider(provider)
    payload = request.get_json(force=True) or {}
    product = payload.get("product")
    if not product:
        return failure("Missing product", 400)
    result = user_service.assign_product(provider, identifier, product)
    return success(result)


@app.route("/api/<provider>/users/<identifier>/password", methods=["POST"])
def reset_password(provider: str, identifier: str):
    provider = normalize_provider(provider)
    payload = request.get_json(force=True) or {}
    result = user_service.reset_password(
        provider,
        identifier,
        new_password=payload.get("new_password"),
        force_change_password=payload.get("force_change_password", True),
    )
    return success(result)


@app.route("/api/<provider>/users/<identifier>", methods=["DELETE"])
def delete_user(provider: str, identifier: str):
    provider = normalize_provider(provider)
    result = user_service.delete_user(provider, identifier)
    return success(result)


@app.route("/api/<provider>/users/<identifier>", methods=["GET"])
def describe_user(provider: str, identifier: str):
    provider = normalize_provider(provider)
    result = user_service.describe_user(provider, identifier)
    return success(result)


@app.errorhandler(Exception)
def handle_exception(exc: Exception):
    logger.exception("API 请求异常: %s", exc)
    status = getattr(exc, "status_code", 500)
    message = str(exc)
    return failure(message, status=status)


if __name__ == "__main__":
    import os

    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", "9999"))
    app.run(host=host, port=port)
