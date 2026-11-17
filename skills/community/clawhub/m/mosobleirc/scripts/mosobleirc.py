#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import sqlite3
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from mosobleirc_core import (
    DEFAULT_DATA_ROOT,
    MosOblEIRCError, RelayNetworkError, ReferenceStore, RelayClient, StateStore,
    load_inventory, assess_consumption, provider_submission_verified)


def _runtime_config(data_root: Path) -> dict:
    explicit = os.environ.get("MOSOBLEIRC_RUNTIME_CONFIG", "").strip()
    path = Path(explicit).expanduser() if explicit else Path(data_root) / "config" / "runtime.json"
    if not path.exists():
        return {}
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise MosOblEIRCError("runtime config is unreadable or invalid JSON") from exc
    if not isinstance(value, dict):
        raise MosOblEIRCError("runtime config must be a JSON object")
    return value

def _resolve_runtime_args(args) -> None:
    cfg = _runtime_config(args.data_root)
    args.transport = getattr(args, "transport", None) or os.environ.get("MOSOBLEIRC_TRANSPORT") or cfg.get("transport", "yandex-relay")
    if args.transport not in {"direct", "yandex-relay"}:
        raise MosOblEIRCError("unknown transport")
    args.provider_token_file = getattr(args, "provider_token_file", None) or os.environ.get("MOSOBLEIRC_PROVIDER_TOKEN_FILE") or cfg.get("provider_token_path")
    args.provider_base_url = getattr(args, "provider_base_url", None) or os.environ.get("MOSOBLEIRC_PROVIDER_BASE_URL") or cfg.get("provider_base_url", "https://lkk.mosobleirc.ru")
    if args.inventory is None:
        raw = os.environ.get("MOSOBLEIRC_INVENTORY", "").strip() or str(cfg.get("inventory_path") or "")
        args.inventory = Path(raw).expanduser() if raw else Path(args.data_root) / "config" / "inventory.json"
    if not args.function_url:
        args.function_url = os.environ.get("MOSOBLEIRC_FUNCTION_URL", "").strip() or str(cfg.get("function_url") or "").strip() or None
    if args.api_key is None:
        raw = os.environ.get("MOSOBLEIRC_API_KEY_FILE", "").strip() or str(cfg.get("api_key_path") or "")
        if raw:
            args.api_key = Path(raw).expanduser()
DEFAULT_SOURCE_ROOTS = []


def _emit(payload: dict) -> None:
    print(json.dumps(payload, ensure_ascii=False, separators=(",", ":")))


def _state(args) -> tuple[StateStore, list[dict]]:
    inventory = load_inventory(args.inventory)
    store = StateStore(args.data_root)
    store.initialize(inventory)
    return store, inventory

def _source_roots() -> list[Path]:
    raw = os.environ.get("MOSOBLEIRC_ALLOWED_SOURCE_ROOTS", "").strip()
    if raw:
        return [Path(x) for x in raw.split(os.pathsep) if x.strip()]
    return DEFAULT_SOURCE_ROOTS


def _relay(args):
    if getattr(args, "transport", "yandex-relay") == "direct":
        from direct_transport import DirectClient
        if not args.provider_token_file:
            raise MosOblEIRCError("provider token file is not configured")
        return DirectClient(Path(args.provider_token_file).expanduser(), args.inventory, args.provider_base_url)
    if not args.function_url:
        raise MosOblEIRCError("relay function URL is not configured")
    key_path = Path(args.api_key or (Path(args.data_root) / "secrets" / "yandex_api_key")).expanduser()
    return RelayClient(args.function_url, key_path)


def cmd_setup(args):
    from setup_runtime import setup
    setup(args.data_root, args.transport)
    _emit({"ok": True, "provider_contacted": False})
    return 0


def cmd_init(args) -> int:
    store, _ = _state(args)
    meters = store.list_meters()
    pending = store.pending_references()
    _emit({"ok": True, "provider_contacted": False, "meters": len(meters), "pending_references": len(pending)})
    return 0


def cmd_status(args) -> int:
    store, inventory = _state(args)
    meters = store.list_meters()
    pending = store.pending_references()
    _emit({
        "ok": True,
        "provider_contacted": False,
        "inventory_items": len(inventory),
        "meters": len(meters),
        "pending_references": len(pending),
        "automatic_writes_enabled": False,
        "write_path_requires_explicit_confirmation": True,
    })
    return 0

def cmd_reference_pending(args) -> int:
    store, _ = _state(args)
    refs = ReferenceStore(store, args.data_root, allowed_source_roots=_source_roots())
    pending = refs.pending()
    _emit({"ok": True, "provider_contacted": False, "count": len(pending), "meters": pending})
    return 0


def cmd_reference_add(args) -> int:
    store, _ = _state(args)
    if args.observed_serial:
        matched = store.identify_meter_by_serial(args.observed_serial)
        if matched is None or int(matched["meter_id"]) != int(args.meter_id):
            _emit({"ok": False, "provider_contacted": False, "error": "REFERENCE_SERIAL_MISMATCH"})
            return 2
    elif not args.confirmed_by_user:
        _emit({"ok": False, "provider_contacted": False, "error": "REFERENCE_BINDING_CONFIRMATION_REQUIRED"})
        return 2
    refs = ReferenceStore(store, args.data_root, allowed_source_roots=_source_roots())
    profile = refs.add(args.meter_id, args.image)
    _emit({
        "ok": True,
        "provider_contacted": False,
        "meter_id": profile["meter_id"],
        "reference_path": profile["reference_path"],
    })
    return 0


def cmd_relay(args) -> int:
    action = {"submit-check": "write-status"}.get(args.action, args.action)
    payload = {}
    result = _relay(args).call(action, **payload)
    _emit(result)
    return 0 if result.get("ok") else 1


def cmd_live(args) -> int:
    payload = {}
    if args.action == "meters":
        payload["item_id"] = args.item_id
    result = _relay(args).call(args.action, **payload)
    _emit(result)
    return 0 if result.get("ok") else 1


def cmd_local(args) -> int:
    store,_=_state(args)
    if args.local_action == "identify":
        meter = store.identify_meter_by_serial(args.serial)
        if meter is None:
            _emit({"ok":False,"provider_contacted":False,"status":"REVIEW","meter_id":None,"serial":args.serial})
            return 2
        _emit({"ok":True,"provider_contacted":False,"status":"MATCHED","meter_id":meter["meter_id"],
               "item_id":meter["item_id"],"apartment":meter["apartment"],"address":meter["address"],
               "meter_type":meter["meter_type"],"physical_serial":meter.get("physical_serial"),"provider_serial":meter["serial"]})
        return 0
    if args.local_action == "analyze":
        meter=store.get_meter(args.meter_id)
        consumption=assess_consumption(store,args.meter_id,args.value,args.observed_at)
        _emit({"ok":True,"provider_contacted":False,"meter_id":args.meter_id,
               "apartment":meter["apartment"],"address":meter["address"],"meter_type":meter["meter_type"],
               "physical_serial":meter.get("physical_serial"),"provider_serial":meter["serial"],
               "previous_provider_value":meter.get("last_provider_value"),"previous_provider_date":meter.get("last_provider_date"),
               "current_value":args.value,"consumption":consumption})
        return 0
    if args.local_action == "record-photo":
        _emit({"ok":False,"provider_contacted":False,"error":"PERSIST_BEFORE_VERIFICATION_FORBIDDEN"})
        return 2
    if args.local_action == "history":
        meter=store.get_meter(args.meter_id)
        _emit({"ok":True,"provider_contacted":False,"meter":meter,
               "photo_history":store.photo_history(args.meter_id),"provider_history":store.provider_history(args.meter_id)})
        return 0
    raise MosOblEIRCError("unknown local action")


def _provider_snapshot(selected: dict) -> tuple[float | None, str | None]:
    meter=selected.get("meter") or {}; last=meter.get("lastValue") or {}; total=last.get("total") or {}
    value=total.get("value")
    return (None if value is None else float(value), last.get("receivedDate"))


def _parse_reading_specs(raw_values) -> list[dict]:
    readings = []
    seen = set()
    for raw in raw_values or []:
        parts = str(raw).split(":")
        if len(parts) != 3:
            raise MosOblEIRCError("reading must be meter_id:whole_value:full_photo_value")
        try:
            meter_id = int(parts[0])
            value = int(parts[1])
            photo_value = float(parts[2])
        except ValueError as exc:
            raise MosOblEIRCError("invalid reading value") from exc
        if meter_id <= 0 or value < 0 or photo_value < 0:
            raise MosOblEIRCError("invalid reading value")
        if meter_id in seen:
            raise MosOblEIRCError("duplicate meter_id in readings")
        seen.add(meter_id)
        readings.append({"meter_id": meter_id, "value": value, "photo_value": photo_value})
    if not readings:
        raise MosOblEIRCError("at least one reading required")
    return readings


def _provider_entry(entries: list, meter_id: int) -> dict | None:
    return next(
        (
            x
            for x in entries
            if isinstance(x, dict)
            and int((x.get("meter") or {}).get("id") or -1) == int(meter_id)
        ),
        None,
    )


def _normalize_submit_status(submit: dict) -> str:
    raw = str(submit.get("status") or "").strip()
    if raw in {"VERIFIED", "VERIFIED_AFTER_UNCERTAIN_RESPONSE"}:
        return raw
    if raw in {"UNCERTAIN_NO_RETRY", "ACCEPTED_NOT_YET_VERIFIED", "UNKNOWN"}:
        return "UNCERTAIN_NO_RETRY"
    if not submit.get("ok"):
        error = str(submit.get("error") or raw or "FAILED")
        if error == "AUTH_REQUIRED":
            return "AUTH_REQUIRED"
        return "FAILED"
    return "UNCERTAIN_NO_RETRY"


def _send_readings(args, store: StateStore) -> int:
    readings = _parse_reading_specs(args.reading)
    with store.exclusive_meter_locks([x["meter_id"] for x in readings]):
        return _send_readings_locked(args, store, readings)


def _send_readings_locked(args, store: StateStore, readings: list[dict]) -> int:
    relay = _relay(args)
    provider_by_item = {}
    results = []

    for reading in readings:
        meter_id = reading["meter_id"]
        value = reading["value"]
        photo_value = reading["photo_value"]
        meter = store.get_meter(meter_id)
        item_id = int(meter["item_id"])

        if item_id not in provider_by_item:
            try:
                live = relay.call("meters", item_id=item_id)
            except RelayNetworkError:
                results.append({
                    "meter_id": meter_id,
                    "value": value,
                    "photo_value": photo_value,
                    "status": "PREFLIGHT_NETWORK_ERROR",
                    "post_attempted": False,
                })
                _emit({
                    "ok": False,
                    "provider_contacted": True,
                    "action": "readings",
                    "results": results,
                })
                return 1
            if not live.get("ok"):
                results.append({
                    "meter_id": meter_id,
                    "value": value,
                    "photo_value": photo_value,
                    "status": str(live.get("error") or "PROVIDER_ERROR"),
                    "post_attempted": False,
                })
                _emit({
                    "ok": False,
                    "provider_contacted": True,
                    "action": "readings",
                    "results": results,
                })
                return 1
            provider_by_item[item_id] = live.get("data") or []

        selected = _provider_entry(provider_by_item[item_id], meter_id)
        if selected is None:
            raise MosOblEIRCError("meter missing from provider response")

        previous, previous_date = _provider_snapshot(selected)
        info = selected.get("valueSendInfo") or {}
        sent_now = info.get("isValueSentForCurrentPeriod") is True
        inflight = store.find_open_submit(
            meter_id,
            None,
            statuses=("EXECUTING", "UNCERTAIN_NO_RETRY", "ACCEPTED_NOT_YET_VERIFIED"),
        )

        if inflight is not None:
            details = inflight.get("details") or {}
            old_payload = details.get("payload") or {}
            try:
                old_value = int(old_payload.get("value"))
            except (TypeError, ValueError):
                old_value = None
            old_observed_at = old_payload.get("observed_at")
            if old_value is not None and provider_submission_verified(
                selected, old_value, old_observed_at
            ):
                stamp = previous_date or old_observed_at or args.observed_at
                recovery = {
                    "ok": True,
                    "status": "VERIFIED",
                    "post_attempted": False,
                    "reconciled": True,
                }
                store.commit_verified_submission(
                    inflight["operation_id"],
                    selected,
                    fetched_at=stamp,
                    final_status="VERIFIED",
                    result=recovery,
                    updated_at=stamp,
                )
                inflight = None
            else:
                results.append({
                    "meter_id": meter_id,
                    "value": value,
                    "photo_value": photo_value,
                    "status": "RECONCILE_REQUIRED",
                    "existing_operation_id": inflight["operation_id"],
                    "post_attempted": False,
                })
                continue

        if provider_submission_verified(selected, value, args.observed_at):
            stamp = previous_date or args.observed_at
            store.sync_provider_meter(selected, fetched_at=stamp)
            results.append({
                "meter_id": meter_id,
                "value": value,
                "photo_value": photo_value,
                "status": "ALREADY_SENT",
                "provider_value": previous,
                "post_attempted": False,
            })
            continue

        blockers = []
        if info.get("isAbleToSendMeterValues") is False:
            blockers.append("provider_disallows_send")
        if info.get("isInAllowedPeriod") is False:
            blockers.append("submission_window_closed")
        if sent_now:
            blockers.append("already_sent_different_value")
        if previous is not None and int(value) < float(previous):
            blockers.append("reading_decreased")

        consumption = assess_consumption(
            store,
            meter_id,
            value,
            args.observed_at,
            previous_value=previous,
            previous_date=previous_date,
        )
        warnings = []
        if consumption.get("status") in {"WATCH", "ANOMALY"}:
            warnings.append("consumption_" + consumption["status"].lower())
        if blockers:
            results.append({
                "meter_id": meter_id,
                "value": value,
                "photo_value": photo_value,
                "status": "BLOCKED",
                "blockers": blockers,
                "warnings": warnings,
                "provider_value": previous,
                "post_attempted": False,
            })
            continue

        old_prepared = store.find_open_submit(
            meter_id,
            None,
            statuses=("PREPARED",),
        )
        if old_prepared is not None:
            store.update_operation(
                old_prepared["operation_id"],
                "SUPERSEDED",
                updated_at=args.observed_at,
            )

        operation_id = str(uuid.uuid4())
        snapshot = {
            "provider_value": previous,
            "provider_date": previous_date,
            "is_able_to_send": info.get("isAbleToSendMeterValues"),
            "is_in_allowed_period": info.get("isInAllowedPeriod"),
            "is_value_sent_for_current_period": info.get("isValueSentForCurrentPeriod"),
            "meter_indication_date": info.get("meterIndicationDate"),
        }
        store.prepare_operation(
            operation_id,
            meter_id=meter_id,
            value=value,
            observed_at=args.observed_at,
            provider_snapshot=snapshot,
            consumption=consumption,
            ready=True,
            created_at=args.observed_at,
            photo_value=photo_value,
        )
        store.update_operation(
            operation_id,
            "EXECUTING",
            updated_at=args.observed_at,
        )

        try:
            submit = dict(relay.call(
                "submit",
                operation_id=operation_id,
                item_id=item_id,
                meter_id=meter_id,
                value=value,
            ))
        except RelayNetworkError:
            submit = {
                "ok": False,
                "provider_contacted": True,
                "operation_id": operation_id,
                "status": "UNCERTAIN_NO_RETRY",
                "error": "RELAY_NETWORK_ERROR",
            }

        final_status = _normalize_submit_status(submit)
        verified = bool(submit.get("ok")) and final_status in {
            "VERIFIED",
            "VERIFIED_AFTER_UNCERTAIN_RESPONSE",
        }
        readback = submit.get("readback_meter")

        if verified and isinstance(readback, dict):
            try:
                store.commit_verified_submission(
                    operation_id,
                    readback,
                    fetched_at=args.observed_at,
                    final_status=final_status,
                    result=submit,
                    updated_at=args.observed_at,
                )
            except sqlite3.Error:
                results.append({
                    "meter_id": meter_id,
                    "value": value,
                    "photo_value": photo_value,
                    "status": "UNCERTAIN_NO_RETRY",
                    "warnings": warnings,
                    "post_attempted": True,
                    "error": "LOCAL_COMMIT_FAILED",
                })
                break
            results.append({
                "meter_id": meter_id,
                "value": value,
                "photo_value": photo_value,
                "status": final_status,
                "warnings": warnings,
                "post_attempted": True,
            })
            continue

        if verified:
            final_status = "UNCERTAIN_NO_RETRY"
        store.update_operation(
            operation_id,
            final_status,
            result=submit,
            updated_at=args.observed_at,
        )
        results.append({
            "meter_id": meter_id,
            "value": value,
            "photo_value": photo_value,
            "status": final_status,
            "warnings": warnings,
            "post_attempted": True,
        })
        if final_status in {"UNCERTAIN_NO_RETRY", "AUTH_REQUIRED", "FAILED"}:
            break

    ok = bool(results) and all(
        x.get("status") in {"VERIFIED", "VERIFIED_AFTER_UNCERTAIN_RESPONSE", "ALREADY_SENT"}
        for x in results
    )
    _emit({
        "ok": ok,
        "provider_contacted": True,
        "action": "readings",
        "results": results,
    })
    return 0 if ok else 1


def _prepare_operation(args, store: StateStore) -> int:
    with store.exclusive_meter_locks([args.meter_id]):
        if store.get_operation(args.operation_id) is not None:
            _emit({"ok":False,"provider_contacted":False,"error":"OPERATION_ID_ALREADY_EXISTS",
                   "operation_id":args.operation_id})
            return 4
        existing=store.find_open_submit(
            args.meter_id,None,
            statuses=("PREPARED","EXECUTING","UNCERTAIN_NO_RETRY","ACCEPTED_NOT_YET_VERIFIED"),
        )
        if existing is not None:
            status=str(existing.get("status") or "")
            error="PREPARE_EXISTS" if status=="PREPARED" else "RECONCILE_REQUIRED"
            _emit({"ok":False,"provider_contacted":False,"error":error,
                   "existing_operation_id":existing["operation_id"],
                   "meter_id":args.meter_id,"value":args.value})
            return 4
        meter=store.get_meter(args.meter_id)
        result=_relay(args).call("meters",item_id=meter["item_id"])
        if not result.get("ok"):
            _emit(result)
            return 1
        entries=result.get("data") or []
        selected=next((x for x in entries if isinstance(x,dict)
                       and int((x.get("meter") or {}).get("id") or -1)==args.meter_id),None)
        if selected is None:
            raise MosOblEIRCError("meter missing from provider response")
        previous,previous_date=_provider_snapshot(selected)
        consumption=assess_consumption(store,args.meter_id,args.value,args.observed_at,
            previous_value=previous,previous_date=previous_date)
        info=selected.get("valueSendInfo") or {}
        blockers=[]
        if info.get("isAbleToSendMeterValues") is False:
            blockers.append("provider_disallows_send")
        if info.get("isInAllowedPeriod") is False:
            blockers.append("submission_window_closed")
        if info.get("isValueSentForCurrentPeriod") is True:
            blockers.append("already_sent_current_period")
        if previous is not None and int(args.value) < previous:
            blockers.append("reading_decreased")
        warnings = []
        if consumption.get("status") in {"WATCH", "ANOMALY"}:
            warnings.append("consumption_" + consumption["status"].lower())
        ready=not blockers
        fetched_at=args.fetched_at or args.observed_at
        snapshot={"provider_value":previous,"provider_date":previous_date,
                  "is_able_to_send":info.get("isAbleToSendMeterValues"),
                  "is_in_allowed_period":info.get("isInAllowedPeriod"),
                  "is_value_sent_for_current_period":info.get("isValueSentForCurrentPeriod"),
                  "meter_indication_date":info.get("meterIndicationDate")}
        op=store.prepare_operation(args.operation_id,meter_id=args.meter_id,value=args.value,
            observed_at=args.observed_at,provider_snapshot=snapshot,consumption=consumption,
            ready=ready,created_at=fetched_at,photo_value=args.photo_value)
        _emit({"ok":ready,"provider_contacted":True,"action":"prepare",
               "operation_id":args.operation_id,"ready_to_send":ready,"blockers":blockers,
               "warnings":warnings,
               "meter_id":args.meter_id,"provider_value":previous,"provider_date":previous_date,
               "candidate_value":args.value,"consumption":consumption,"operation_status":op["status"]})
        return 0 if ready else 3


def _reconcile_operation(args, store: StateStore) -> int:
    initial=store.get_operation(args.operation_id)
    initial_details=(initial or {}).get("details") or {}
    initial_payload=initial_details.get("payload") or {}
    try:
        meter_id=int(initial_payload.get("meter_id"))
    except (TypeError,ValueError):
        _emit({"ok":False,"provider_contacted":False,"error":"EXECUTING_OPERATION_REQUIRED",
               "operation_id":args.operation_id})
        return 2
    with store.exclusive_meter_locks([meter_id]):
        op=store.get_operation(args.operation_id)
        details=(op or {}).get("details") or {}
        payload=details.get("payload") or {}
        if op is None or op.get("action")!="submit" or op.get("status") not in {
            "EXECUTING","UNCERTAIN_NO_RETRY","ACCEPTED_NOT_YET_VERIFIED"
        }:
            _emit({"ok":False,"provider_contacted":False,"error":"EXECUTING_OPERATION_REQUIRED",
                   "operation_id":args.operation_id})
            return 2
        value=int(payload.get("value") if payload.get("value") is not None else -1)
        meter=store.get_meter(meter_id)
        result=_relay(args).call("meters",item_id=meter["item_id"])
        if not result.get("ok"):
            _emit(result)
            return 1
        entries=result.get("data") or []
        selected=next((x for x in entries if isinstance(x,dict)
                       and int((x.get("meter") or {}).get("id") or -1)==meter_id),None)
        if selected is None:
            raise MosOblEIRCError("meter missing from provider response")
        provider_value,provider_date=_provider_snapshot(selected)
        applied=provider_submission_verified(selected,value,payload.get("observed_at"))
        stamp=provider_date or payload.get("observed_at") or ""
        if applied:
            out={"ok":True,"provider_contacted":True,"action":"reconcile",
                 "operation_id":args.operation_id,"status":"VERIFIED","meter_id":meter_id,
                 "value":value,"provider_value":provider_value,"provider_date":provider_date,
                 "post_attempted":False}
            store.commit_verified_submission(args.operation_id,selected,fetched_at=stamp,
                final_status="VERIFIED",result=out,updated_at=stamp)
            _emit(out)
            return 0
        out={"ok":False,"provider_contacted":True,"action":"reconcile",
             "operation_id":args.operation_id,"status":"UNCERTAIN_NO_RETRY","meter_id":meter_id,
             "value":value,"provider_value":provider_value,"provider_date":provider_date,
             "post_attempted":False}
        store.update_operation(args.operation_id,"UNCERTAIN_NO_RETRY",result=out,updated_at=stamp)
        _emit(out)
        return 5


def _resolve_not_applied_operation(args, store: StateStore) -> int:
    if not args.confirmed_not_applied_by_user:
        _emit({"ok":False,"provider_contacted":False,"error":"RESOLUTION_CONFIRMATION_REQUIRED",
               "operation_id":args.operation_id})
        return 2

    initial=store.get_operation(args.operation_id)
    initial_details=(initial or {}).get("details") or {}
    initial_payload=initial_details.get("payload") or {}
    try:
        meter_id=int(initial_payload.get("meter_id"))
    except (TypeError,ValueError):
        _emit({"ok":False,"provider_contacted":False,"error":"UNCERTAIN_OPERATION_REQUIRED",
               "operation_id":args.operation_id})
        return 2

    with store.exclusive_meter_locks([meter_id]):
        op=store.get_operation(args.operation_id)
        details=(op or {}).get("details") or {}
        payload=details.get("payload") or {}
        if op is None or op.get("action")!="submit" or op.get("status") not in {
            "EXECUTING","UNCERTAIN_NO_RETRY","ACCEPTED_NOT_YET_VERIFIED"
        }:
            _emit({"ok":False,"provider_contacted":False,"error":"UNCERTAIN_OPERATION_REQUIRED",
                   "operation_id":args.operation_id})
            return 2

        value=int(payload.get("value") if payload.get("value") is not None else -1)
        meter=store.get_meter(meter_id)
        relay=_relay(args)
        try:
            fresh=relay.call("meters",item_id=meter["item_id"])
        except RelayNetworkError:
            _emit({"ok":False,"provider_contacted":True,"error":"RESOLUTION_PREFLIGHT_NETWORK_ERROR",
                   "operation_id":args.operation_id,"post_attempted":False})
            return 1
        if not fresh.get("ok"):
            out=dict(fresh)
            out.setdefault("operation_id",args.operation_id)
            out["post_attempted"]=False
            _emit(out)
            return 1

        entries=fresh.get("data") or []
        selected=_provider_entry(entries,meter_id)
        if selected is None:
            raise MosOblEIRCError("meter missing from provider response")

        provider_value,provider_date=_provider_snapshot(selected)
        if provider_submission_verified(selected,value,payload.get("observed_at")):
            stamp=provider_date or payload.get("observed_at") or ""
            out={"ok":True,"provider_contacted":True,"action":"resolve-not-applied",
                 "operation_id":args.operation_id,"status":"VERIFIED","meter_id":meter_id,
                 "value":value,"provider_value":provider_value,"provider_date":provider_date,
                 "post_attempted":False,"manual_resolution":False,
                 "resolution_basis":"provider_positive_proof"}
            store.commit_verified_submission(args.operation_id,selected,fetched_at=stamp,
                final_status="VERIFIED",result=out,updated_at=stamp)
            _emit(out)
            return 0

        meter_payload=selected.get("meter") or {}
        raw_last=meter_payload.get("lastValue") if "lastValue" in meter_payload else None
        info=selected.get("valueSendInfo") or {}
        current_period_flag=info.get("isValueSentForCurrentPeriod")

        no_history = raw_last is None
        last = raw_last if isinstance(raw_last, dict) else {}
        provider_status=str(last.get("status") or "").upper()
        stable_historical = (
            isinstance(raw_last, dict)
            and bool(raw_last)
            and provider_status=="PROCESSED"
            and provider_value is not None
        )
        stable_negative = current_period_flag is False and (no_history or stable_historical)
        provider_state_kind = "NO_HISTORY" if no_history else ("HISTORICAL_PROCESSED" if stable_historical else "AMBIGUOUS")

        # Manual negative resolution is forbidden while provider state is ambiguous/pending.
        # A truly new meter may legitimately have no lastValue at all; explicit current-period=False
        # plus separate user confirmation is the negative proof path for that case.
        if not stable_negative:
            out={"ok":False,"provider_contacted":True,"action":"resolve-not-applied",
                 "operation_id":args.operation_id,"status":"UNCERTAIN_NO_RETRY",
                 "error":"PROVIDER_STATE_AMBIGUOUS","meter_id":meter_id,"value":value,
                 "provider_value":provider_value,"provider_date":provider_date,
                 "provider_status":provider_status or None,
                 "provider_state_kind":provider_state_kind,
                 "is_value_sent_for_current_period":current_period_flag,
                 "post_attempted":False}
            store.update_operation(args.operation_id,"UNCERTAIN_NO_RETRY",result=out,
                                   updated_at=provider_date or payload.get("observed_at") or "")
            _emit(out)
            return 5

        resolved_at=datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00","Z")
        out={"ok":True,"provider_contacted":True,"action":"resolve-not-applied",
             "operation_id":args.operation_id,"status":"NOT_APPLIED","meter_id":meter_id,
             "value":value,"provider_value":provider_value,"provider_date":provider_date,
             "provider_status":provider_status or None,
             "provider_state_kind":provider_state_kind,
             "is_value_sent_for_current_period":current_period_flag,
             "post_attempted":False,"manual_resolution":True,
             "user_confirmed_provider_absence":True,
             "resolution_basis":"fresh_provider_negative_plus_user_confirmation",
             "resolved_at":resolved_at}
        store.update_operation(args.operation_id,"NOT_APPLIED",result=out,updated_at=resolved_at)
        _emit(out)
        return 0


def _execute_operation(args, store: StateStore) -> int:
    with store.exclusive_meter_locks([args.meter_id]):
        op=store.get_operation(args.operation_id)
        details=(op or {}).get("details") or {}
        payload=details.get("payload") or {}
        if (op is None or op.get("action")!="submit" or op.get("status")!="PREPARED"
                or int(payload.get("meter_id") or -1)!=int(args.meter_id)
                or int(payload.get("value") if payload.get("value") is not None else -1)!=int(args.value)):
            _emit({"ok":False,"provider_contacted":False,"error":"PREPARE_REQUIRED",
                   "operation_id":args.operation_id})
            return 2

        other=store.find_open_submit(
            args.meter_id,None,
            statuses=("EXECUTING","UNCERTAIN_NO_RETRY","ACCEPTED_NOT_YET_VERIFIED"),
        )
        if other is not None and other["operation_id"] != args.operation_id:
            _emit({"ok":False,"provider_contacted":False,"error":"RECONCILE_REQUIRED",
                   "existing_operation_id":other["operation_id"],"operation_id":args.operation_id})
            return 4

        meter=store.get_meter(args.meter_id)
        relay=_relay(args)
        try:
            fresh=relay.call("meters",item_id=meter["item_id"])
        except RelayNetworkError:
            _emit({"ok":False,"provider_contacted":True,"error":"PREFLIGHT_NETWORK_ERROR",
                   "operation_id":args.operation_id,"post_attempted":False})
            return 1
        if not fresh.get("ok"):
            _emit(fresh)
            return 1
        entries=fresh.get("data") or []
        selected=_provider_entry(entries,args.meter_id)
        if selected is None:
            raise MosOblEIRCError("meter missing from provider response")

        previous,_previous_date=_provider_snapshot(selected)
        info=selected.get("valueSendInfo") or {}
        if provider_submission_verified(selected,args.value,payload.get("observed_at")):
            stamp=args.executed_at or payload.get("observed_at") or ""
            result={"ok":True,"provider_contacted":True,"operation_id":args.operation_id,
                    "status":"VERIFIED","value":args.value,"readback_meter":selected,
                    "post_attempted":False,"reconciled":True}
            store.commit_verified_submission(args.operation_id,selected,fetched_at=stamp,
                final_status="VERIFIED",result=result,updated_at=stamp)
            result["local_sync_ok"]=True
            result["operation_local_status"]="VERIFIED"
            _emit(result)
            return 0

        blockers=[]
        if info.get("isAbleToSendMeterValues") is False:
            blockers.append("provider_disallows_send")
        if info.get("isInAllowedPeriod") is False:
            blockers.append("submission_window_closed")
        if info.get("isValueSentForCurrentPeriod") is True:
            blockers.append("already_sent_current_period")
        if previous is not None and int(args.value) < float(previous):
            blockers.append("reading_decreased")
        if blockers:
            result={"ok":False,"provider_contacted":True,"operation_id":args.operation_id,
                    "status":"BLOCKED","blockers":blockers,"post_attempted":False}
            store.update_operation(args.operation_id,"BLOCKED",result=result,
                                   updated_at=args.executed_at or payload.get("observed_at") or "")
            _emit(result)
            return 3

        stamp=args.executed_at or payload.get("observed_at") or ""
        store.update_operation(args.operation_id,"EXECUTING",updated_at=stamp)
        try:
            result=dict(relay.call("submit",operation_id=args.operation_id,
                        item_id=meter["item_id"],meter_id=args.meter_id,value=args.value))
        except RelayNetworkError:
            result={"ok":False,"provider_contacted":True,"operation_id":args.operation_id,
                    "status":"UNCERTAIN_NO_RETRY","error":"RELAY_NETWORK_ERROR"}

        final_status=_normalize_submit_status(result)
        verified=result.get("ok") and final_status in {"VERIFIED","VERIFIED_AFTER_UNCERTAIN_RESPONSE"}
        if verified:
            readback=result.get("readback_meter")
            if isinstance(readback,dict):
                try:
                    store.commit_verified_submission(args.operation_id,readback,fetched_at=stamp,
                        final_status=final_status,result=result,updated_at=stamp)
                    result["local_sync_ok"]=True
                except sqlite3.Error:
                    result["local_sync_ok"]=False
                    result["status"]="UNCERTAIN_NO_RETRY"
                    result["error"]="LOCAL_COMMIT_FAILED"
                    result["operation_local_status"]="EXECUTING"
                    _emit(result)
                    return 1
            else:
                result["local_sync_ok"]=False
                final_status="UNCERTAIN_NO_RETRY"
        if not (verified and result.get("local_sync_ok") is True):
            store.update_operation(args.operation_id,final_status,result=result,updated_at=stamp)
        result["operation_local_status"]=final_status
        _emit(result)
        return 0 if verified and result.get("local_sync_ok") is True else 1


def cmd_send(args) -> int:
    store,_=_state(args)
    if args.send_action in {"readings","prepare","execute"} and not args.confirmed_by_user:
        _emit({"ok":False,"provider_contacted":False,"error":"CONFIRMATION_REQUIRED"}); return 2
    if args.send_action == "readings":
        return _send_readings(args,store)
    if args.send_action == "prepare":
        return _prepare_operation(args,store)
    if args.send_action == "reconcile":
        return _reconcile_operation(args,store)
    if args.send_action == "resolve-not-applied":
        return _resolve_not_applied_operation(args,store)
    if args.send_action == "execute":
        return _execute_operation(args,store)
    raise MosOblEIRCError("unknown send action")

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="mosobleirc")
    parser.add_argument("--data-root", type=Path, default=DEFAULT_DATA_ROOT)
    parser.add_argument("--inventory", type=Path)
    parser.add_argument("--function-url")
    parser.add_argument("--api-key", type=Path)
    parser.add_argument("--transport", choices=("direct", "yandex-relay"))
    parser.add_argument("--provider-token-file", type=Path)
    parser.add_argument("--provider-base-url")
    sub = parser.add_subparsers(dest="command", required=True)

    p_setup = sub.add_parser("setup")
    p_setup.set_defaults(func=cmd_setup)

    p_init = sub.add_parser("init")
    p_init.set_defaults(func=cmd_init)

    p_status = sub.add_parser("status")
    p_status.set_defaults(func=cmd_status)

    p_ref = sub.add_parser("reference")
    ref_sub = p_ref.add_subparsers(dest="reference_command", required=True)
    p_pending = ref_sub.add_parser("pending")
    p_pending.set_defaults(func=cmd_reference_pending)
    p_add = ref_sub.add_parser("add")
    p_add.add_argument("meter_id", type=int)
    p_add.add_argument("image", type=Path)
    p_add.add_argument("--observed-serial")
    p_add.add_argument("--confirmed-by-user", action="store_true")
    p_add.set_defaults(func=cmd_reference_add)

    p_relay = sub.add_parser("relay")
    p_relay.add_argument("action", choices=("ping", "inventory", "submit-check"))
    p_relay.set_defaults(func=cmd_relay)

    p_live = sub.add_parser("live")
    p_live.add_argument("action", choices=("accounts", "items", "meters"))
    p_live.add_argument("--item-id", type=int)
    p_live.set_defaults(func=cmd_live)

    p_local = sub.add_parser("local")
    local_sub = p_local.add_subparsers(dest="local_action", required=True)
    p_id = local_sub.add_parser("identify")
    p_id.add_argument("--serial", required=True)
    p_id.set_defaults(func=cmd_local)
    p_an = local_sub.add_parser("analyze")
    p_an.add_argument("--meter-id", type=int, required=True)
    p_an.add_argument("--value", type=float, required=True)
    p_an.add_argument("--observed-at", required=True)
    p_an.set_defaults(func=cmd_local)
    p_rec = local_sub.add_parser("record-photo")
    p_rec.add_argument("--meter-id", type=int, required=True)
    p_rec.add_argument("--value", type=float, required=True)
    p_rec.add_argument("--observed-at", required=True)
    p_rec.add_argument("--status", default="UNVERIFIED")
    p_rec.add_argument("--image-sha256")
    p_rec.set_defaults(func=cmd_local)
    p_hist = local_sub.add_parser("history")
    p_hist.add_argument("--meter-id", type=int, required=True)
    p_hist.set_defaults(func=cmd_local)

    p_send = sub.add_parser("send")
    send_sub = p_send.add_subparsers(dest="send_action", required=True)
    p_readings = send_sub.add_parser("readings")
    p_readings.add_argument("--reading", action="append", required=True,
                            help="meter_id:whole_value:full_photo_value")
    p_readings.add_argument("--observed-at", required=True)
    p_readings.add_argument("--confirmed-by-user", action="store_true")
    p_readings.set_defaults(func=cmd_send)
    p_prep = send_sub.add_parser("prepare")
    p_prep.add_argument("--meter-id", type=int, required=True)
    p_prep.add_argument("--value", type=int, required=True)
    p_prep.add_argument("--photo-value", type=float)
    p_prep.add_argument("--observed-at", required=True)
    p_prep.add_argument("--fetched-at")
    p_prep.add_argument("--operation-id", required=True)
    p_prep.add_argument("--confirmed-by-user", action="store_true")
    p_prep.set_defaults(func=cmd_send)
    p_recon = send_sub.add_parser("reconcile")
    p_recon.add_argument("--operation-id", required=True)
    p_recon.set_defaults(func=cmd_send)
    p_resolve = send_sub.add_parser("resolve-not-applied")
    p_resolve.add_argument("--operation-id", required=True)
    p_resolve.add_argument("--confirmed-not-applied-by-user", action="store_true",
                           help="user checked provider UI and explicitly confirmed the reading is absent")
    p_resolve.set_defaults(func=cmd_send)
    p_exec = send_sub.add_parser("execute")
    p_exec.add_argument("--meter-id", type=int, required=True)
    p_exec.add_argument("--value", type=int, required=True)
    p_exec.add_argument("--operation-id", required=True)
    p_exec.add_argument("--executed-at")
    p_exec.add_argument("--confirmed-by-user", action="store_true")
    p_exec.set_defaults(func=cmd_send)
    return parser

def main(argv=None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command == "live" and args.action == "meters" and args.item_id is None:
        parser.error("live meters requires --item-id")
    try:
        if args.command != "setup":
            _resolve_runtime_args(args)
        return int(args.func(args))
    except MosOblEIRCError as exc:
        _emit({"ok": False, "error": type(exc).__name__, "message": str(exc)[:300]})
        return 1
    except sqlite3.Error:
        _emit({"ok": False, "provider_contacted": False, "error": "DATABASE_ERROR"})
        return 1
    except KeyboardInterrupt:
        _emit({"ok": False, "error": "INTERRUPTED"})
        return 130


if __name__ == "__main__":
    raise SystemExit(main())
