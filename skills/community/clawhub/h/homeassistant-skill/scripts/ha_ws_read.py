#!/usr/bin/env python3
"""One-shot, allowlisted Home Assistant WebSocket reads; no generic command sender."""

import argparse
import importlib.metadata
import json
import logging
import os
from pathlib import Path
import re
import socket as socket_module
import sys
import threading
from urllib.parse import urlsplit

from ha_read import Client, ENTITY, HAError, MAX_RESPONSE, safe_json, time_window


READS = {
    "config": "get_config", "services": "get_services", "states": "get_states",
    "entities": "config/entity_registry/list", "devices": "config/device_registry/list",
    "areas": "config/area_registry/list", "floors": "config/floor_registry/list",
    "labels": "config/label_registry/list", "assist-pipelines": "assist_pipeline/pipeline/list",
    "assist-agents": "conversation/agent/list", "assist-languages": "assist_pipeline/language/list",
    "energy-preferences": "energy/get_prefs", "energy-info": "energy/info",
    "statistics-metadata": "recorder/list_statistic_ids", "repairs": "repairs/list_issues",
}


def transport():
    try:
        version = importlib.metadata.version("websockets")
        if not 15 <= int(version.split(".")[0]) < 18:
            raise ImportError
        from websockets.sync.client import connect
    except (ImportError, importlib.metadata.PackageNotFoundError, ValueError):
        raise HAError("Optional WebSocket reads need websockets>=15.0.1,<18 in a local Python environment; see requirements-websocket.txt.") from None
    return connect


class WSClient:
    def __init__(self, url, token, timeout=30):
        settings = Client(url, token, timeout)
        self.token = settings.token
        self.timeout = settings.timeout
        origin = urlsplit(settings.url)
        self.uri = origin._replace(scheme="wss" if origin.scheme == "https" else "ws").geturl() + "/api/websocket"

    def _exchange(self, command):
        connect = transport()
        # Keep third-party debug logs from exposing authentication frames.
        logger = logging.Logger("ha-read-websocket")
        logger.disabled = True
        expired = threading.Event()
        try:
            # sync.connect does not follow redirects or reconnect. No credentials
            # are sent in the HTTP handshake; auth follows the trusted HA greeting.
            with connect(self.uri, proxy=None, compression=None, open_timeout=self.timeout,
                         close_timeout=2, ping_interval=None, max_size=MAX_RESPONSE,
                         max_queue=1, logger=logger) as socket:
                # sync.send() has no timeout parameter. Abort the physical socket
                # without taking the library's send lock if the entire exchange
                # expires; this also interrupts a peer that stops reading.
                def abort():
                    expired.set()
                    try:
                        socket.socket.shutdown(socket_module.SHUT_RDWR)
                    except OSError:
                        pass
                    socket.socket.close()

                deadline = threading.Timer(self.timeout, abort)
                deadline.daemon = True
                deadline.start()
                try:
                    hello = self._receive(socket)
                    if hello.get("type") != "auth_required":
                        raise HAError("Expected HA authentication greeting; no credential was sent.")
                    socket.send(json.dumps({"type": "auth", "access_token": self.token}))
                    authenticated = self._receive(socket)
                    if authenticated.get("type") == "auth_invalid":
                        raise HAError("Home Assistant rejected authentication. No retry was sent.")
                    if authenticated.get("type") != "auth_ok":
                        raise HAError("Unexpected authentication reply.")
                    socket.send(json.dumps({"id": 1, **command}))
                    response = self._receive(socket)
                    if response.get("type") != "result" or type(response.get("id")) is not int or response["id"] != 1:
                        raise HAError("Unexpected WebSocket result type or request ID.")
                    if response.get("success") is not True:
                        code = response.get("error", {}).get("code") if isinstance(response.get("error"), dict) else None
                        reasons = {"unknown_command": "Command is unavailable on this installation/version.",
                                   "unauthorized": "This read requires permissions the user does not have.",
                                   "not_found": "Requested entity or configuration is not present.",
                                   "invalid_format": "Parameters were rejected by this version."}
                        raise HAError(reasons.get(code, "Home Assistant rejected the read-only query.") + " No retry was sent.")
                    if expired.is_set():
                        raise HAError("WebSocket exchange deadline exceeded. No retry was sent.")
                    return {"ha_version": authenticated.get("ha_version", hello.get("ha_version")),
                            "result": response.get("result")}
                finally:
                    deadline.cancel()
        except HAError:
            raise
        except Exception:
            # Library exception details may contain frames, URLs or server data.
            if expired.is_set():
                raise HAError("WebSocket exchange deadline exceeded. No retry was sent.") from None
            raise HAError("WebSocket connection/protocol failed or timed out; no redirect or retry was followed.") from None

    def _receive(self, socket):
        raw = socket.recv(timeout=self.timeout)
        if not isinstance(raw, str) or len(raw.encode("utf-8")) > MAX_RESPONSE:
            raise HAError("Expected a bounded text WebSocket message.")
        try:
            data = json.loads(raw)
        except (ValueError, RecursionError):
            raise HAError("Expected a JSON WebSocket message.") from None
        if not isinstance(data, dict):
            raise HAError("Expected a WebSocket message object.")
        return data

    def read(self, name):
        if name not in READS:
            raise HAError("Only named read-only WebSocket queries are allowed.")
        return self._exchange({"type": READS[name]})

    def definition(self, entity):
        if not ENTITY.fullmatch(entity) or entity.split(".", 1)[0] not in {"automation", "script"}:
            raise HAError("Use an exact automation or script entity ID.")
        return self._exchange({"type": entity.split(".", 1)[0] + "/config", "entity_id": entity})

    def validate_config(self, config, legacy_keys=False):
        aliases = {"trigger": "triggers", "triggers": "triggers", "condition": "conditions",
                   "conditions": "conditions", "action": "actions", "actions": "actions"}
        if not isinstance(config, dict) or not config or set(config) - aliases.keys():
            raise HAError("Validation input must contain only triggers, conditions and/or actions sections.")
        normalized = {}
        for key, value in config.items():
            name = aliases[key]
            if name in normalized:
                raise HAError("Do not supply singular and plural forms of the same validation section.")
            normalized[name] = value
        if len(json.dumps(config).encode("utf-8")) > MAX_RESPONSE:
            raise HAError("Validation input exceeds the size limit.")
        # validate_config checks schemas; it does not execute the supplied actions.
        wire = {key[:-1] if legacy_keys else key: value for key, value in normalized.items()}
        result = self._exchange({"type": "validate_config", **wire})
        validation = result.get("result")
        if not isinstance(validation, dict) or set(validation) != set(wire) or any(
                not isinstance(section, dict) or type(section.get("valid")) is not bool for section in validation.values()):
            raise HAError("Server did not validate all requested sections; check this installation's validation API format.")
        return result

    def resolve_target(self, target, expand_groups=False):
        return self._target_query("extract_from_target", target, expand_groups)

    def target_services(self, target, expand_groups=False):
        return self._target_query("get_services_for_target", target, expand_groups)

    def _target_query(self, command, target, expand_groups):
        if not isinstance(target, dict) or not target or set(target) - {"entity_id", "device_id", "area_id", "label_id"}:
            raise HAError("Use explicit entity, device, area or label target IDs.")
        count = 0
        for kind, values in target.items():
            if not isinstance(values, list) or not values or any(not isinstance(value, str) for value in values):
                raise HAError("Target IDs must be nonempty lists of strings.")
            count += len(values)
            for value in values:
                if value == "all" or not (ENTITY.fullmatch(value) if kind == "entity_id" else re.fullmatch(r"[A-Za-z0-9_-]{1,128}", value)):
                    raise HAError("Use exact target IDs; all and wildcard targeting are not allowed.")
        if count > 64:
            raise HAError("Resolve at most 64 explicit target IDs at a time.")
        return self._exchange({"type": command, "target": target, "expand_group": bool(expand_groups)})

    def statistics(self, statistic, start, end, period="day"):
        if not isinstance(statistic, str) or not re.fullmatch(r"[A-Za-z0-9_.:-]{1,200}", statistic) or period not in {"hour", "day"}:
            raise HAError("Use one exact statistic ID and an hour or day period.")
        start, end = time_window(start, end)
        return self._exchange({"type": "recorder/statistics_during_period", "statistic_ids": [statistic],
                               "start_time": start, "end_time": end, "period": period,
                               "types": ["change", "sum", "state", "mean"]})


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--timeout", type=float, default=30)
    commands = parser.add_subparsers(dest="command", required=True)
    read = commands.add_parser("read", help="One named registry, Assist, energy or diagnostic query")
    read.add_argument("name", choices=sorted(READS))
    definition = commands.add_parser("definition", help="Read automation/script definition; requires admin")
    definition.add_argument("entity")
    validate = commands.add_parser("validate-config", help="Validate a local JSON snippet without executing it")
    validate.add_argument("path", type=Path)
    validate.add_argument("--legacy-keys", action="store_true", help="Explicitly use the older singular wire format; never auto-retried")
    for name, help_text in [("resolve-target", "Inspect target expansion without calling an action"),
                            ("target-services", "Discover actions applicable to an explicit target; never execute them")]:
        resolve = commands.add_parser(name, help=help_text)
        for kind in ["entity", "device", "area", "label"]:
            resolve.add_argument("--" + kind, action="append", default=[])
        resolve.add_argument("--expand-groups", action="store_true")
    statistics = commands.add_parser("statistics", help="Query one recorder statistic, maximum 31 days")
    statistics.add_argument("statistic")
    statistics.add_argument("--start", required=True)
    statistics.add_argument("--end", required=True)
    statistics.add_argument("--period", choices=["hour", "day"], default="day")
    args = parser.parse_args(argv)
    try:
        client = WSClient(os.environ.get("HA_URL", ""), os.environ.get("HA_TOKEN", ""), args.timeout)
        if args.command == "read":
            result = client.read(args.name)
        elif args.command == "definition":
            result = client.definition(args.entity)
        elif args.command == "validate-config":
            try:
                with args.path.open("rb") as source:
                    raw = source.read(MAX_RESPONSE + 1)
                if len(raw) > MAX_RESPONSE:
                    raise ValueError
                config = json.loads(raw)
            except (OSError, ValueError, RecursionError):
                raise HAError("Expected a readable, bounded JSON validation file.") from None
            result = client.validate_config(config, args.legacy_keys)
        elif args.command in {"resolve-target", "target-services"}:
            target = {kind + "_id": getattr(args, kind) for kind in ["entity", "device", "area", "label"] if getattr(args, kind)}
            query = client.resolve_target if args.command == "resolve-target" else client.target_services
            result = query(target, args.expand_groups)
        else:
            result = client.statistics(args.statistic, args.start, args.end, args.period)
        print(safe_json(result, client.token))
        return 0
    except HAError as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
