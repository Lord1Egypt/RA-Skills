#!/usr/bin/env python3
"""Bibliotalk API client for GuruTalk skills.

This script always reads runtime configuration from the current skill directory's
`.env` file. When copied into a generated figure skill, it keeps working with the
same relative layout:

- <skill_dir>/.env
- <skill_dir>/scripts/bibliotalk_client.py
"""

from __future__ import annotations

import argparse
import http.client
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from getpass import getpass
from pathlib import Path
from typing import Any

try:
	from dotenv import dotenv_values, load_dotenv
except ImportError as exc:
	raise SystemExit(
		"Missing dependency python-dotenv. Install it with `python -m pip install -r requirements.txt`."
	) from exc


DEFAULT_BIBLIOTALK_API_URL = "https://api.bibliotalk.space"
DEFAULT_BIBLIOTALK_WEB_URL = "https://bibliotalk.space"
USER_AGENT = "GuruTalk-BibliotalkClient/1.0 (+https://github.com/gurutalk)"


@dataclass(frozen=True)
class RuntimeConfig:
	skill_dir: Path
	env_path: Path
	api_url: str
	api_key: str


def resolve_skill_dir(script_path: str | Path | None = None) -> Path:
	script_file = Path(script_path or __file__).resolve()
	return script_file.parent.parent


def load_runtime_config(
	skill_dir: str | Path | None = None,
	*,
	require_api_key: bool = False,
) -> RuntimeConfig:
	resolved_skill_dir = Path(skill_dir).expanduser().resolve() if skill_dir else resolve_skill_dir()
	env_path = resolved_skill_dir / ".env"

	env_values: dict[str, str | None] = {}
	if env_path.exists():
		load_dotenv(dotenv_path=env_path, override=False)
		env_values = dotenv_values(env_path)

	api_url = str(
		env_values.get("BIBLIOTALK_API_URL")
		or os.environ.get("BIBLIOTALK_API_URL")
		or DEFAULT_BIBLIOTALK_API_URL
	).strip().rstrip("/")
	api_key = str(
		env_values.get("BIBLIOTALK_API_KEY")
		or os.environ.get("BIBLIOTALK_API_KEY")
		or ""
	).strip()

	if require_api_key and not env_path.exists():
		raise RuntimeError(
			f"Missing runtime env file: {env_path}. Run `python scripts/bibliotalk_client.py configure` in this skill directory and retry."
		)
	if require_api_key and not api_key:
		raise RuntimeError(
			f"Missing BIBLIOTALK_API_KEY in {env_path}. Run `python scripts/bibliotalk_client.py configure` in this skill directory and retry."
		)

	return RuntimeConfig(
		skill_dir=resolved_skill_dir,
		env_path=env_path,
		api_url=api_url,
		api_key=api_key,
	)


def _request_json(
	path: str,
	*,
	skill_dir: str | Path | None = None,
	method: str = "GET",
	body: dict[str, Any] | None = None,
) -> Any:
	config = load_runtime_config(skill_dir=skill_dir, require_api_key=True)
	url = f"{config.api_url}{path}"
	data = None if body is None else json.dumps(body).encode("utf-8")

	headers = {
		"Accept": "application/json",
		"User-Agent": USER_AGENT,
		"x-api-key": config.api_key,
	}
	if body is not None:
		headers["Content-Type"] = "application/json"

	last_error: Exception | None = None
	for attempt in range(3):
		req = urllib.request.Request(url, headers=headers, data=data, method=method)
		try:
			with urllib.request.urlopen(req, timeout=20) as resp:
				raw = resp.read().decode("utf-8")
				return json.loads(raw)
		except http.client.IncompleteRead as exc:
			last_error = exc
			if attempt == 2:
				break
		except urllib.error.HTTPError as exc:
			err_body = ""
			try:
				err_body = exc.read().decode("utf-8")
			except Exception:
				err_body = ""
			raise RuntimeError(f"HTTP {exc.code} fetching {url}: {err_body or exc.reason}") from exc
		except urllib.error.URLError as exc:
			last_error = exc
			if attempt == 2:
				break
	if last_error is None:
		raise RuntimeError(f"Unknown error fetching {url}")
	if isinstance(last_error, urllib.error.URLError):
		raise RuntimeError(f"Network error fetching {url}: {last_error.reason}") from last_error
	raise RuntimeError(f"Incomplete response fetching {url}: {last_error}") from last_error


def send_magiclink(email: str) -> dict[str, Any]:
	quoted_email = urllib.parse.quote(email, safe="")
	url = f"{DEFAULT_BIBLIOTALK_WEB_URL}/login/magiclink?email={quoted_email}"
	req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT}, method="GET")
	try:
		with urllib.request.urlopen(req, timeout=20) as resp:
			resp.read()
			status = getattr(resp, "status", resp.getcode())
	except urllib.error.HTTPError as exc:
		err_body = ""
		try:
			err_body = exc.read().decode("utf-8")
		except Exception:
			err_body = ""
		raise RuntimeError(f"HTTP {exc.code} requesting magic link: {err_body or exc.reason}") from exc
	except urllib.error.URLError as exc:
		raise RuntimeError(f"Network error requesting magic link: {exc.reason}") from exc

	return {
		"ok": True,
		"email": email,
		"status": status,
		"login_url": url,
	}


def _write_env_value(env_path: Path, key: str, value: str) -> None:
	if "\n" in value or "\r" in value:
		raise RuntimeError(f"Invalid value for {key}: newlines are not allowed")

	existing_lines = env_path.read_text(encoding="utf-8").splitlines() if env_path.exists() else []
	updated_lines: list[str] = []
	replaced = False

	for line in existing_lines:
		if line.strip().startswith(f"{key}="):
			if not replaced:
				updated_lines.append(f"{key}={value}")
				replaced = True
			continue
		updated_lines.append(line)

	if not replaced:
		updated_lines.append(f"{key}={value}")

	env_path.parent.mkdir(parents=True, exist_ok=True)
	env_path.write_text("\n".join(updated_lines).rstrip("\n") + "\n", encoding="utf-8")


def configure_runtime(skill_dir: str | Path | None = None) -> dict[str, Any]:
	config = load_runtime_config(skill_dir=skill_dir, require_api_key=False)

	try:
		api_key = getpass("Enter Bibliotalk API Key: ").strip()
	except (EOFError, KeyboardInterrupt) as exc:
		raise RuntimeError("Cancelled API key input") from exc

	if not api_key:
		raise RuntimeError("Empty API key; nothing was saved")

	_write_env_value(config.env_path, "BIBLIOTALK_API_KEY", api_key)

	return {
		"ok": True,
		"skill_dir": str(config.skill_dir),
		"env_path": str(config.env_path),
		"api_url": config.api_url,
		"configured": ["BIBLIOTALK_API_KEY"],
	}


def fetch_figures_index(skill_dir: str | Path | None = None) -> list[dict[str, Any]]:
	data = _request_json("/v1/figures", skill_dir=skill_dir)
	return data if isinstance(data, list) else []


def fetch_figure_detail(slug: str, skill_dir: str | Path | None = None) -> dict[str, Any]:
	quoted_slug = urllib.parse.quote(slug, safe="")
	data = _request_json(f"/v1/figure/{quoted_slug}", skill_dir=skill_dir)
	return data if isinstance(data, dict) else {}


def query_figure(
	figure: str,
	query: str,
	*,
	limit: int | None = None,
	skill_dir: str | Path | None = None,
) -> dict[str, Any]:
	body: dict[str, Any] = {
		"figure": figure,
		"query": query,
	}
	if limit is not None:
		body["limit"] = limit
	data = _request_json("/v1/query", method="POST", body=body, skill_dir=skill_dir)
	return data if isinstance(data, dict) else {}


def fetch_quote(quote_id: str, skill_dir: str | Path | None = None) -> dict[str, Any]:
	quoted_quote_id = urllib.parse.quote(quote_id, safe="")
	data = _request_json(f"/v1/quote/{quoted_quote_id}", skill_dir=skill_dir)
	return data if isinstance(data, dict) else {}


def _print_json(data: Any) -> None:
	json.dump(data, sys.stdout, ensure_ascii=False, indent=2)
	sys.stdout.write("\n")


def main() -> None:
	parser = argparse.ArgumentParser(description="Bibliotalk client for GuruTalk skills")
	parser.add_argument(
		"--skill-dir",
		default=None,
		help="技能目录（默认取当前脚本所在技能目录）",
	)
	subparsers = parser.add_subparsers(dest="command", required=True)

	subparsers.add_parser("configure", help="交互式写入当前技能目录的 API key")

	magiclink_parser = subparsers.add_parser("magiclink", help="请求 Bibliotalk magic link")
	magiclink_parser.add_argument("--email", required=True, help="登录邮箱")

	subparsers.add_parser("figures", help="获取云端人物目录")

	figure_parser = subparsers.add_parser("figure", help="获取单个人物 profile")
	figure_parser.add_argument("--slug", required=True, help="人物 slug")

	query_parser = subparsers.add_parser("query", help="查询人物记忆库")
	query_parser.add_argument("--figure", required=True, help="人物 slug")
	query_parser.add_argument("--query", required=True, help="用户问题")
	query_parser.add_argument("--limit", type=int, default=None, help="返回结果数量")

	quote_parser = subparsers.add_parser("quote", help="获取引用详情")
	quote_parser.add_argument("--quote-id", required=True, help="引用 ID")

	args = parser.parse_args()

	try:
		if args.command == "configure":
			_print_json(configure_runtime(skill_dir=args.skill_dir))
			return
		if args.command == "magiclink":
			_print_json(send_magiclink(args.email))
			return
		if args.command == "figures":
			_print_json(fetch_figures_index(skill_dir=args.skill_dir))
			return
		if args.command == "figure":
			_print_json(fetch_figure_detail(args.slug, skill_dir=args.skill_dir))
			return
		if args.command == "query":
			_print_json(
				query_figure(
					args.figure,
					args.query,
					limit=args.limit,
					skill_dir=args.skill_dir,
				)
			)
			return
		if args.command == "quote":
			_print_json(fetch_quote(args.quote_id, skill_dir=args.skill_dir))
			return
	except Exception as exc:
		print(f"错误：{exc}", file=sys.stderr)
		sys.exit(1)

	print(f"错误：未知 command={args.command}", file=sys.stderr)
	sys.exit(1)


if __name__ == "__main__":
	main()
