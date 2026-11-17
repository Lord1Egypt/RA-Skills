from __future__ import annotations

import json
import hashlib
import os
import socket
import sqlite3
import stat
import urllib.error
import urllib.request
from contextlib import contextmanager
from pathlib import Path
from typing import Callable
from urllib.parse import urlparse


class MosOblEIRCError(Exception):
    pass


class SecretPermissionError(MosOblEIRCError):
    pass


class RelayNetworkError(MosOblEIRCError):
    pass


class RelayAuthError(MosOblEIRCError):
    pass


class RelayResponseError(MosOblEIRCError):
    pass


DEFAULT_DATA_ROOT = Path(
    os.environ.get("MOSOBLEIRC_DATA_ROOT", str(Path.home() / ".local" / "share" / "mosobleirc"))
).expanduser()


def _positive_inventory_id(value, label: str) -> int:
    if isinstance(value, bool):
        raise MosOblEIRCError(f"{label} must be a positive integer")
    try:
        result = int(value)
    except (TypeError, ValueError) as exc:
        raise MosOblEIRCError(f"{label} must be a positive integer") from exc
    if result <= 0:
        raise MosOblEIRCError(f"{label} must be a positive integer")
    return result


def load_inventory(path: str | Path) -> list[dict]:
    data = json.loads(Path(path).read_text(encoding="utf-8-sig"))
    if not isinstance(data, list):
        raise MosOblEIRCError("inventory must be a list")
    seen_items: set[int] = set()
    seen_meters: set[int] = set()
    for item in data:
        if not isinstance(item, dict) or not isinstance(item.get("meters"), list):
            raise MosOblEIRCError("invalid inventory item")
        item_id = _positive_inventory_id(item.get("item_id"), "item_id")
        if item_id in seen_items:
            raise MosOblEIRCError(f"duplicate item_id in inventory: {item_id}")
        seen_items.add(item_id)
        for meter in item["meters"]:
            if not isinstance(meter, dict):
                raise MosOblEIRCError("invalid inventory meter")
            meter_id = _positive_inventory_id(meter.get("meter_id"), "meter_id")
            if meter_id in seen_meters:
                raise MosOblEIRCError(f"duplicate meter_id in inventory: {meter_id}")
            seen_meters.add(meter_id)
    return data


def provider_submission_verified(provider_payload: dict, requested_value: int, observed_at: str | None = None,
                                 *, require_current_period: bool = False) -> bool:
    if not isinstance(provider_payload, dict):
        return False
    meter = provider_payload.get("meter")
    if not isinstance(meter, dict):
        return False
    last = meter.get("lastValue") or {}
    total = last.get("total") or {}
    try:
        same_value = int(float(total.get("value"))) == int(requested_value)
    except (TypeError, ValueError):
        return False
    if not same_value or str(last.get("status") or "").upper() != "PROCESSED":
        return False
    info = provider_payload.get("valueSendInfo") or {}
    if info.get("isValueSentForCurrentPeriod") is True:
        return True
    if require_current_period:
        return False
    if not observed_at:
        return False
    try:
        year = int(str(observed_at)[:4])
        month = int(str(observed_at)[5:7])
    except (TypeError, ValueError):
        return False
    settlement = last.get("settlementPeriod") or {}
    try:
        return int(settlement.get("year")) == year and int(settlement.get("month")) == month
    except (TypeError, ValueError):
        return False


def _json_body(raw: bytes) -> dict:
    try:
        value = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise RelayResponseError("relay returned invalid JSON") from exc
    if not isinstance(value, dict):
        raise RelayResponseError("relay returned non-object JSON")
    return value


class RelayClient:
    def __init__(
        self,
        function_url: str,
        api_key_path: str | Path,
        *,
        opener: Callable = urllib.request.urlopen,
        timeout: int = 15,
        user_agent: str = "OpenClaw-MosOblEIRC/1.0",
    ) -> None:
        self.function_url = str(function_url).strip()
        parsed = urlparse(self.function_url)
        if parsed.scheme.lower() != "https" or not parsed.hostname or parsed.username or parsed.password:
            raise MosOblEIRCError("relay function URL must be an HTTPS URL without embedded credentials")
        self.api_key_path = Path(api_key_path)
        self.opener = opener
        self.timeout = int(timeout)
        self.user_agent = user_agent

    def _api_key(self) -> str:
        try:
            mode = stat.S_IMODE(self.api_key_path.stat().st_mode)
        except OSError as exc:
            raise MosOblEIRCError("Yandex API key file is unavailable") from exc
        if mode & 0o077:
            raise SecretPermissionError("Yandex API key file permissions must be 0600 or stricter")
        try:
            secret = self.api_key_path.read_text(encoding="utf-8").strip()
        except OSError as exc:
            raise MosOblEIRCError("Yandex API key file is unreadable") from exc
        if not secret:
            raise MosOblEIRCError("Yandex API key is empty")
        return secret

    def call(self, action: str, **payload) -> dict:
        secret = self._api_key()
        body_obj = {"action": str(action), **payload}
        body = json.dumps(body_obj, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
        req = urllib.request.Request(
            self.function_url,
            data=body,
            method="POST",
            headers={
                "Authorization": f"Api-Key {secret}",
                "Content-Type": "application/json; charset=utf-8",
                "Accept": "application/json",
                "User-Agent": self.user_agent,
            },
        )
        try:
            with self.opener(req, timeout=self.timeout) as response:
                result = _json_body(response.read())
        except urllib.error.HTTPError as exc:
            raw = exc.read()
            try:
                result = _json_body(raw)
            except RelayResponseError:
                result = {"ok": False, "error": "HTTP_ERROR", "http_status": int(exc.code)}
            if exc.code in (401, 403) and result.get("error") != "WRITES_DISABLED":
                raise RelayAuthError(f"relay authorization failed with HTTP {exc.code}") from None
            result.setdefault("http_status", int(exc.code))
        except (urllib.error.URLError, TimeoutError, socket.timeout, OSError) as exc:
            raise RelayNetworkError("relay network error") from None
        return result


class StateStore:
    def __init__(self, root: str | Path) -> None:
        self.root = Path(root)
        self.db_path = self.root / "meter.db"

    def _ensure_root(self) -> None:
        self.root.mkdir(parents=True, exist_ok=True)
        try:
            os.chmod(self.root, 0o700)
        except PermissionError:
            pass

    @contextmanager
    def _connect(self):
        self._ensure_root()
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            if self.db_path.exists():
                os.chmod(self.db_path, 0o600)
            with conn:
                yield conn
        finally:
            conn.close()

    @contextmanager
    def exclusive_meter_locks(self, meter_ids):
        try:
            import fcntl
        except ImportError as exc:
            raise MosOblEIRCError("inter-process meter locking is unavailable on this platform") from exc
        self._ensure_root()
        lock_dir = self.root / "locks"
        lock_dir.mkdir(parents=True, exist_ok=True)
        os.chmod(lock_dir, 0o700)
        handles = []
        try:
            for meter_id in sorted({int(x) for x in meter_ids}):
                path = lock_dir / f"meter-{meter_id}.lock"
                handle = path.open("a+", encoding="utf-8")
                os.chmod(path, 0o600)
                try:
                    fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
                except BlockingIOError as exc:
                    handle.close()
                    raise MosOblEIRCError(f"another submit is active for meter {meter_id}") from exc
                handles.append(handle)
            yield
        finally:
            for handle in reversed(handles):
                try:
                    fcntl.flock(handle.fileno(), fcntl.LOCK_UN)
                finally:
                    handle.close()

    def initialize(self, inventory: list[dict]) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS meters (
                    meter_id INTEGER PRIMARY KEY,
                    item_id INTEGER NOT NULL,
                    apartment TEXT NOT NULL DEFAULT '',
                    address TEXT NOT NULL DEFAULT '',
                    serial TEXT NOT NULL,
                    meter_type TEXT NOT NULL,
                    last_provider_value REAL,
                    last_provider_date TEXT,
                    verification_deadline TEXT,
                    physical_serial TEXT,
                    location_zone TEXT,
                    provider_updated_at TEXT
                )
                """
            )
            cols={row[1] for row in conn.execute("PRAGMA table_info(meters)")}
            for name, sqltype in (("physical_serial","TEXT"),("location_zone","TEXT"),("provider_updated_at","TEXT")):
                if name not in cols:
                    conn.execute(f"ALTER TABLE meters ADD COLUMN {name} {sqltype}")
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS provider_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT, meter_id INTEGER NOT NULL,
                    provider_value_id INTEGER, value REAL NOT NULL, consumption REAL, received_date TEXT,
                    settlement_year INTEGER, settlement_month INTEGER, status TEXT, is_average INTEGER NOT NULL DEFAULT 0,
                    fetched_at TEXT NOT NULL, UNIQUE(meter_id, provider_value_id)
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS reference_profiles (
                    meter_id INTEGER PRIMARY KEY REFERENCES meters(meter_id),
                    reference_path TEXT,
                    model_hint TEXT,
                    display_bbox TEXT,
                    digit_layout TEXT,
                    integer_digits INTEGER,
                    decimal_digits INTEGER,
                    visual_notes TEXT,
                    updated_at TEXT
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS readings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    operation_id TEXT UNIQUE,
                    meter_id INTEGER NOT NULL REFERENCES meters(meter_id),
                    value REAL NOT NULL,
                    observed_at TEXT NOT NULL,
                    validation_status TEXT NOT NULL,
                    payload_json TEXT NOT NULL DEFAULT '{}'
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS operations (
                    operation_id TEXT PRIMARY KEY,
                    action TEXT NOT NULL,
                    status TEXT NOT NULL,
                    payload_hash TEXT,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    provider_result_json TEXT
                )
                """
            )
            for item in inventory:
                item_id = int(item["item_id"])
                apartment = str(item.get("name") or "")
                address = str(item.get("address") or "")
                for meter in item.get("meters") or []:
                    meter_id = int(meter["meter_id"])
                    conn.execute(
                        """
                        INSERT INTO meters (
                            meter_id, item_id, apartment, address, serial, meter_type,
                            last_provider_value, last_provider_date, verification_deadline
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                        ON CONFLICT(meter_id) DO UPDATE SET
                            item_id=excluded.item_id,
                            apartment=excluded.apartment,
                            address=excluded.address,
                            serial=excluded.serial,
                            meter_type=excluded.meter_type,
                            last_provider_value=CASE WHEN meters.provider_updated_at IS NULL THEN excluded.last_provider_value ELSE meters.last_provider_value END,
                            last_provider_date=CASE WHEN meters.provider_updated_at IS NULL THEN excluded.last_provider_date ELSE meters.last_provider_date END,
                            verification_deadline=excluded.verification_deadline
                        """,
                        (
                            meter_id,
                            item_id,
                            apartment,
                            address,
                            str(meter.get("number") or ""),
                            str(meter.get("type") or ""),
                            meter.get("last_value"),
                            meter.get("last_value_date"),
                            meter.get("verification_deadline"),
                        ),
                    )
                    conn.execute(
                        "INSERT OR IGNORE INTO reference_profiles (meter_id) VALUES (?)",
                        (meter_id,),
                    )
        os.chmod(self.db_path, 0o600)

    def list_meters(self) -> list[dict]:
        with self._connect() as conn:
            rows = conn.execute("SELECT * FROM meters ORDER BY item_id, meter_id").fetchall()
        return [dict(row) for row in rows]

    @staticmethod
    def _serial_key(value) -> str:
        return "".join(ch for ch in str(value or "").lower() if ch.isalnum())

    def identify_meter_by_serial(self, serial: str) -> dict | None:
        key = self._serial_key(serial)
        if not key:
            return None
        matches = []
        for meter in self.list_meters():
            ids = {self._serial_key(meter.get("serial")), self._serial_key(meter.get("physical_serial"))}
            ids.discard("")
            if key in ids:
                matches.append(meter)
        return matches[0] if len(matches) == 1 else None

    def pending_references(self) -> list[dict]:
        with self._connect() as conn:
            rows = conn.execute(
                """
                SELECT m.*, r.reference_path
                FROM meters AS m
                JOIN reference_profiles AS r ON r.meter_id=m.meter_id
                WHERE r.reference_path IS NULL OR r.reference_path=''
                ORDER BY m.item_id, m.meter_id
                """
            ).fetchall()
        return [dict(row) for row in rows]

    def set_reference(self, meter_id: int, reference_path: str) -> None:
        with self._connect() as conn:
            exists = conn.execute("SELECT 1 FROM meters WHERE meter_id=?", (int(meter_id),)).fetchone()
            if not exists:
                raise MosOblEIRCError("unknown meter_id")
            conn.execute(
                """
                INSERT INTO reference_profiles (meter_id, reference_path)
                VALUES (?, ?)
                ON CONFLICT(meter_id) DO UPDATE SET reference_path=excluded.reference_path
                """,
                (int(meter_id), str(reference_path)),
            )

    def get_reference(self, meter_id: int) -> dict:
        with self._connect() as conn:
            row = conn.execute(
                """
                SELECT m.*, r.reference_path, r.model_hint, r.display_bbox, r.digit_layout,
                       r.integer_digits, r.decimal_digits, r.visual_notes, r.updated_at
                FROM meters AS m
                JOIN reference_profiles AS r ON r.meter_id=m.meter_id
                WHERE m.meter_id=?
                """,
                (int(meter_id),),
            ).fetchone()
        if row is None:
            raise MosOblEIRCError("unknown meter_id")
        return dict(row)


    def get_meter(self, meter_id: int) -> dict:
        with self._connect() as conn:
            row=conn.execute("SELECT * FROM meters WHERE meter_id=?",(int(meter_id),)).fetchone()
        if row is None:
            raise MosOblEIRCError("unknown meter_id")
        return dict(row)

    def set_meter_identity(self, meter_id: int, *, physical_serial: str | None = None, location_zone: str | None = None) -> dict:
        self.get_meter(meter_id)
        with self._connect() as conn:
            conn.execute("UPDATE meters SET physical_serial=COALESCE(?,physical_serial), location_zone=COALESCE(?,location_zone) WHERE meter_id=?",
                         (physical_serial, location_zone, int(meter_id)))
        return self.get_meter(meter_id)

    def add_provider_history(self, meter_id: int, *, provider_value_id, value, consumption=None, received_date=None,
                             settlement_year=None, settlement_month=None, status=None, is_average=False, fetched_at: str) -> None:
        self.get_meter(meter_id)
        with self._connect() as conn:
            conn.execute("""INSERT INTO provider_history
                (meter_id,provider_value_id,value,consumption,received_date,settlement_year,settlement_month,status,is_average,fetched_at)
                VALUES (?,?,?,?,?,?,?,?,?,?)
                ON CONFLICT(meter_id,provider_value_id) DO UPDATE SET
                value=excluded.value,consumption=excluded.consumption,received_date=excluded.received_date,
                settlement_year=excluded.settlement_year,settlement_month=excluded.settlement_month,status=excluded.status,
                is_average=excluded.is_average,fetched_at=excluded.fetched_at""",
                (int(meter_id),provider_value_id,float(value),None if consumption is None else float(consumption),received_date,
                 settlement_year,settlement_month,status,1 if is_average else 0,fetched_at))

    def sync_provider_meter(self, payload: dict, *, fetched_at: str) -> dict:
        meter=payload.get("meter") if isinstance(payload,dict) else None
        if not isinstance(meter,dict) or meter.get("id") is None:
            raise MosOblEIRCError("invalid provider meter payload")
        meter_id=int(meter["id"]); self.get_meter(meter_id)
        last=meter.get("lastValue") or {}; total=last.get("total") or {}
        value=total.get("value"); received=last.get("receivedDate")
        if value is not None:
            settlement=last.get("settlementPeriod") or {}
            self.add_provider_history(meter_id,provider_value_id=last.get("id"),value=value,
                consumption=total.get("consumptionValue"),received_date=received,
                settlement_year=settlement.get("year"),settlement_month=settlement.get("month"),
                status=last.get("status"),is_average=bool(last.get("isAverageValue")),fetched_at=fetched_at)
            with self._connect() as conn:
                conn.execute("UPDATE meters SET last_provider_value=?,last_provider_date=?,provider_updated_at=? WHERE meter_id=?",
                             (float(value),received,fetched_at,meter_id))
        return self.get_meter(meter_id)

    def provider_history(self, meter_id: int) -> list[dict]:
        with self._connect() as conn:
            rows=conn.execute("SELECT * FROM provider_history WHERE meter_id=? ORDER BY COALESCE(received_date,''),id",(int(meter_id),)).fetchall()
        return [dict(r) for r in rows]

    def record_photo_reading(self, meter_id: int, value, observed_at: str, *, image_sha256: str | None = None,
                             validation_status: str = "UNVERIFIED", payload: dict | None = None) -> int:
        self.get_meter(meter_id)
        body=dict(payload or {})
        if image_sha256: body["image_sha256"]=str(image_sha256)
        with self._connect() as conn:
            cur=conn.execute("INSERT INTO readings (operation_id,meter_id,value,observed_at,validation_status,payload_json) VALUES (NULL,?,?,?,?,?)",
                             (int(meter_id),float(value),observed_at,str(validation_status),json.dumps(body,ensure_ascii=False,separators=(",",":"))))
            return int(cur.lastrowid)

    def photo_history(self, meter_id: int) -> list[dict]:
        with self._connect() as conn:
            rows=conn.execute("SELECT id,meter_id,value,observed_at,validation_status,payload_json FROM readings WHERE meter_id=? ORDER BY observed_at,id",(int(meter_id),)).fetchall()
        result=[]
        for row in rows:
            item=dict(row)
            try: item["payload"]=json.loads(item.pop("payload_json"))
            except json.JSONDecodeError: item["payload"]={}
            result.append(item)
        return result


    def prepare_operation(self, operation_id: str, *, meter_id: int, value: int, observed_at: str,
                          provider_snapshot: dict, consumption: dict, ready: bool, created_at: str,
                          photo_value: float | None = None) -> dict:
        operation_id=str(operation_id).strip()
        if not operation_id:
            raise MosOblEIRCError("operation_id required")
        payload={"meter_id":int(meter_id),"value":int(value),"observed_at":str(observed_at),
                 "photo_value":float(photo_value) if photo_value is not None else float(value)}
        canonical=json.dumps(payload,ensure_ascii=False,sort_keys=True,separators=(",",":"))
        digest=hashlib.sha256(canonical.encode("utf-8")).hexdigest()
        body={"payload":payload,"provider_snapshot":provider_snapshot,"consumption":consumption}
        with self._connect() as conn:
            old=conn.execute("SELECT operation_id FROM operations WHERE operation_id=?",(operation_id,)).fetchone()
            if old is not None:
                raise MosOblEIRCError("operation_id already exists")
            status="PREPARED" if ready else "BLOCKED"
            conn.execute("""INSERT INTO operations(operation_id,action,status,payload_hash,created_at,updated_at,provider_result_json)
                VALUES (?,?,?,?,?,?,?)""",
                (operation_id,"submit",status,digest,created_at,created_at,json.dumps(body,ensure_ascii=False,separators=(",",":"))))
        return self.get_operation(operation_id)

    def set_reference_layout(self, meter_id: int, *, integer_digits: int, decimal_digits: int, display_bbox: str | None = None) -> dict:
        self.get_meter(meter_id)
        if int(integer_digits) <= 0 or int(decimal_digits) < 0:
            raise MosOblEIRCError("invalid display layout")
        with self._connect() as conn:
            conn.execute("UPDATE reference_profiles SET integer_digits=?,decimal_digits=?,display_bbox=COALESCE(?,display_bbox) WHERE meter_id=?",
                         (int(integer_digits),int(decimal_digits),display_bbox,int(meter_id)))
        return self.get_reference(meter_id)

    def commit_verified_submission(self, operation_id: str, provider_payload: dict, *, fetched_at: str,
                                   final_status: str | None = None, result: dict | None = None,
                                   updated_at: str | None = None) -> dict:
        op=self.get_operation(operation_id)
        if op is None or op.get('action')!='submit':
            raise MosOblEIRCError('unknown submit operation')
        details=op.get('details') or {}; requested=details.get('payload') or {}
        meter=provider_payload.get('meter') if isinstance(provider_payload,dict) else None
        if not isinstance(meter,dict) or int(meter.get('id') or -1)!=int(requested.get('meter_id') or -2):
            raise MosOblEIRCError('readback meter mismatch')
        if not provider_submission_verified(provider_payload, int(requested.get('value')), requested.get('observed_at')):
            raise MosOblEIRCError('readback value not verified')
        last=meter.get('lastValue') or {}; total=last.get('total') or {}; value=total.get('value')
        settlement=last.get('settlementPeriod') or {}; meter_id=int(meter['id'])
        photo_value=float(requested.get('photo_value',requested['value'])); observed_at=str(requested.get('observed_at') or fetched_at)
        submitted_value=int(requested['value'])
        manual_override=int(photo_value)!=submitted_value
        body=json.dumps({'source':'verified_submit_readback','provider_value_id':last.get('id'),
                         'submitted_value':submitted_value,'photo_value':photo_value,
                         'manual_override':manual_override},ensure_ascii=False,separators=(',',':'))
        with self._connect() as conn:
            conn.execute("""INSERT INTO provider_history
                (meter_id,provider_value_id,value,consumption,received_date,settlement_year,settlement_month,status,is_average,fetched_at)
                VALUES (?,?,?,?,?,?,?,?,?,?) ON CONFLICT(meter_id,provider_value_id) DO UPDATE SET
                value=excluded.value,consumption=excluded.consumption,received_date=excluded.received_date,
                settlement_year=excluded.settlement_year,settlement_month=excluded.settlement_month,status=excluded.status,
                is_average=excluded.is_average,fetched_at=excluded.fetched_at""",
                (meter_id,last.get('id'),float(value),None if total.get('consumptionValue') is None else float(total.get('consumptionValue')),
                 last.get('receivedDate'),settlement.get('year'),settlement.get('month'),last.get('status'),
                 1 if last.get('isAverageValue') else 0,fetched_at))
            conn.execute("UPDATE meters SET last_provider_value=?,last_provider_date=?,provider_updated_at=? WHERE meter_id=?",
                         (float(value),last.get('receivedDate'),fetched_at,meter_id))
            conn.execute("""INSERT INTO readings(operation_id,meter_id,value,observed_at,validation_status,payload_json)
                VALUES (?,?,?,?,?,?) ON CONFLICT(operation_id) DO NOTHING""",
                (str(operation_id),meter_id,photo_value,observed_at,'VERIFIED',body))
            if final_status is not None:
                merged=dict(details)
                if result is not None:
                    merged["execute_result"]=result
                conn.execute("UPDATE operations SET status=?,updated_at=?,provider_result_json=? WHERE operation_id=?",
                    (str(final_status),str(updated_at or fetched_at),
                     json.dumps(merged,ensure_ascii=False,separators=(',',':')),str(operation_id)))
        return self.get_meter(meter_id)

    def find_open_submit(self, meter_id: int, value: int | None = None, *, statuses=("EXECUTING",)) -> dict | None:
        wanted={str(x) for x in statuses}
        with self._connect() as conn:
            rows=conn.execute("SELECT * FROM operations WHERE action='submit' ORDER BY rowid DESC").fetchall()
        for row in rows:
            item=dict(row)
            if str(item.get("status")) not in wanted:
                continue
            try:
                details=json.loads(item.get("provider_result_json") or "{}")
            except json.JSONDecodeError:
                continue
            payload=details.get("payload") or {}
            try:
                same_meter=int(payload.get("meter_id"))==int(meter_id)
                same_value=value is None or int(payload.get("value"))==int(value)
                same=same_meter and same_value
            except (TypeError,ValueError):
                same=False
            if same:
                item["details"]=details
                return item
        return None


    def get_operation(self, operation_id: str) -> dict | None:
        with self._connect() as conn:
            row=conn.execute("SELECT * FROM operations WHERE operation_id=?",(str(operation_id),)).fetchone()
        if row is None:
            return None
        item=dict(row)
        try: item["details"]=json.loads(item.get("provider_result_json") or "{}")
        except json.JSONDecodeError: item["details"]={}
        return item

    def update_operation(self, operation_id: str, status: str, *, result: dict | None = None, updated_at: str) -> dict:
        if self.get_operation(operation_id) is None:
            raise MosOblEIRCError("unknown operation_id")
        with self._connect() as conn:
            if result is None:
                conn.execute("UPDATE operations SET status=?,updated_at=? WHERE operation_id=?",(str(status),updated_at,str(operation_id)))
            else:
                old=self.get_operation(operation_id) or {}; details=dict(old.get("details") or {})
                details["execute_result"]=result
                conn.execute("UPDATE operations SET status=?,updated_at=?,provider_result_json=? WHERE operation_id=?",
                    (str(status),updated_at,json.dumps(details,ensure_ascii=False,separators=(",",":")),str(operation_id)))
        return self.get_operation(operation_id)

from dataclasses import dataclass
from datetime import date, datetime


@dataclass(frozen=True)
class ValidationResult:
    status: str
    reasons: list[str]
    integer_value: int | None
    requires_confirmation: bool = True

    def as_dict(self) -> dict:
        return {
            "status": self.status,
            "reasons": list(self.reasons),
            "integer_value": self.integer_value,
            "requires_confirmation": self.requires_confirmation,
        }


def _as_date(value) -> date | None:
    if value is None or value == "":
        return None
    if isinstance(value, date) and not isinstance(value, datetime):
        return value
    text = str(value).strip()
    try:
        return date.fromisoformat(text[:10])
    except ValueError:
        return None


def _meter_type_key(value) -> str:
    text = "".join(ch for ch in str(value or "").lower() if ch.isalnum())
    aliases = {
        "coldwater": "coldwater",
        "хвс": "coldwater",
        "hotwater": "hotwater",
        "гвс": "hotwater",
    }
    return aliases.get(text, text)


def _append_once(target: list[str], reason: str) -> None:
    if reason not in target:
        target.append(reason)


def validate_reading(
    profile: dict,
    observation: dict,
    previous_value,
    previous_date,
    today,
    *,
    unusual_monthly_consumption: float = 25.0,
    extreme_monthly_consumption: float = 60.0,
) -> ValidationResult:
    red: list[str] = []
    yellow: list[str] = []
    current_date = _as_date(today)
    if current_date is None:
        raise MosOblEIRCError("invalid current date")

    if observation.get("same_meter") is not True:
        _append_once(red, "meter_identity_uncertain")
    if observation.get("ambiguous") is True:
        _append_once(red, "ambiguous_reading")
    if observation.get("passes_agree") is False:
        _append_once(red, "pass_disagreement")
    elif observation.get("passes_agree") is not True:
        _append_once(yellow, "second_pass_not_confirmed")

    expected_type = _meter_type_key(profile.get("meter_type"))
    observed_type = _meter_type_key(observation.get("meter_type"))
    if expected_type and observed_type and expected_type != observed_type:
        _append_once(red, "meter_type_mismatch")

    serial_visible = observation.get("serial_visible") is True
    if serial_visible:
        expected_serial = str(profile.get("serial") or "").strip().lower()
        observed_serial = str(observation.get("serial") or "").strip().lower()
        if expected_serial and observed_serial and expected_serial != observed_serial:
            _append_once(red, "serial_mismatch")
        elif expected_serial and not observed_serial:
            _append_once(yellow, "serial_unreadable")
    else:
        _append_once(yellow, "serial_not_visible")

    raw_integer = observation.get("integer_part")
    integer_value: int | None
    try:
        if isinstance(raw_integer, bool) or raw_integer is None:
            raise ValueError
        integer_value = int(raw_integer)
        if float(raw_integer) != float(integer_value) or integer_value < 0:
            raise ValueError
    except (TypeError, ValueError, OverflowError):
        integer_value = None
        _append_once(red, "invalid_integer_reading")

    deadline = _as_date(profile.get("verification_deadline"))
    if deadline is not None and current_date > deadline:
        _append_once(red, "verification_expired")

    if observation.get("glare") is True:
        _append_once(yellow, "glare")
    if observation.get("blur") is True:
        _append_once(yellow, "blur")
    quality = str(observation.get("image_quality") or "").strip().lower()
    if quality and quality != "good":
        _append_once(yellow, "image_quality_not_good")
    if not quality:
        _append_once(yellow, "image_quality_unknown")

    confidences = observation.get("digit_confidence")
    if isinstance(confidences, list) and confidences:
        try:
            min_conf = min(float(x) for x in confidences)
        except (TypeError, ValueError):
            min_conf = 0.0
        if min_conf < 0.65:
            _append_once(red, "digit_confidence_critical")
        elif min_conf < 0.90:
            _append_once(yellow, "digit_confidence_low")
    else:
        _append_once(yellow, "digit_confidence_missing")

    if not (13 <= current_date.day <= 23):
        _append_once(yellow, "submission_window_closed")

    if integer_value is not None and previous_value is not None:
        try:
            previous = float(previous_value)
        except (TypeError, ValueError):
            previous = None
        if previous is not None:
            if float(integer_value) < previous:
                _append_once(red, "reading_decreased")
            else:
                delta = float(integer_value) - previous
                prior_date = _as_date(previous_date)
                if prior_date is not None:
                    months = max(1, (current_date.year - prior_date.year) * 12 + current_date.month - prior_date.month)
                    monthly = delta / months
                    if monthly > extreme_monthly_consumption:
                        _append_once(red, "extreme_consumption")
                    elif monthly > unusual_monthly_consumption:
                        _append_once(yellow, "unusual_consumption")

    if red:
        return ValidationResult("RED", red + yellow, integer_value, True)
    if yellow:
        return ValidationResult("YELLOW", yellow, integer_value, True)
    return ValidationResult("GREEN", [], integer_value, True)


def assess_consumption(store: StateStore, meter_id: int, current_value, current_date, *, previous_value=None, previous_date=None) -> dict:
    meter_id=int(meter_id)
    if previous_value is None or previous_date is None:
        meter=store.get_meter(meter_id)
        previous_value=meter.get("last_provider_value") if previous_value is None else previous_value
        previous_date=meter.get("last_provider_date") if previous_date is None else previous_date
    now=_as_date(current_date); before=_as_date(previous_date)
    if now is None or before is None or previous_value is None:
        raise MosOblEIRCError("previous provider reading is unavailable")
    delta=float(current_value)-float(previous_value)
    if delta < 0:
        return {"meter_id":meter_id,"status":"ANOMALY","reason":"reading_decreased","delta":delta}
    days=max(1,(now-before).days)
    monthly=delta*30.4375/days
    hist=[float(x["consumption"]) for x in store.provider_history(meter_id)
          if x.get("consumption") is not None and not x.get("is_average") and str(x.get("status") or "").upper() in {"","PROCESSED"}]
    hist=[x for x in hist if x >= 0][-12:]
    result={"meter_id":meter_id,"status":"INSUFFICIENT_HISTORY","delta":delta,"period_days":days,
            "monthly_equivalent":round(monthly,3),"history_periods":len(hist),"historical_median":None,
            "ratio_to_median":None,"robust_deviation":None}
    if len(hist)<3:
        return result
    from statistics import median
    med=float(median(hist)); mad=float(median([abs(x-med) for x in hist]))
    scale=max(0.5,1.4826*mad,med*0.20)
    deviation=abs(monthly-med)/scale
    ratio=None if med<=0 else monthly/med
    status="NORMAL"
    if deviation>=4.0 or (ratio is not None and ratio>=3.0): status="ANOMALY"
    elif deviation>=2.0 or (ratio is not None and ratio>=2.0): status="WATCH"
    result.update(status=status,historical_median=round(med,3),ratio_to_median=None if ratio is None else round(ratio,3),
                  robust_deviation=round(deviation,3))
    return result

import tempfile
from PIL import Image, ImageOps, UnidentifiedImageError


class ReferenceStore:
    def __init__(
        self,
        state_store: StateStore,
        data_root: str | Path,
        *,
        allowed_source_roots: list[str | Path] | None = None,
    ) -> None:
        self.state_store = state_store
        self.data_root = Path(data_root)
        self.reference_dir = self.data_root / "reference-images"
        if allowed_source_roots is None:
            raw = os.environ.get("MOSOBLEIRC_ALLOWED_SOURCE_ROOTS", "").strip()
            allowed_source_roots = [x for x in raw.split(os.pathsep) if x.strip()] if raw else []
        self.allowed_source_roots = [Path(x).expanduser().resolve() for x in allowed_source_roots]

    def _prepare_dirs(self) -> None:
        self.data_root.mkdir(parents=True, exist_ok=True)
        self.reference_dir.mkdir(parents=True, exist_ok=True)
        for directory in (self.data_root, self.reference_dir):
            try:
                os.chmod(directory, 0o700)
            except PermissionError:
                pass

    def _checked_source(self, image_path: str | Path) -> Path:
        source = Path(image_path).expanduser().resolve()
        if not source.is_file():
            raise MosOblEIRCError("reference source is not a file")
        if self.allowed_source_roots:
            allowed = any(source == root or root in source.parents for root in self.allowed_source_roots)
            if not allowed:
                raise MosOblEIRCError("reference source is outside allowed roots")
        return source

    def add(self, meter_id: int, image_path: str | Path) -> dict:
        meter_id = int(meter_id)
        self.state_store.get_reference(meter_id)
        source = self._checked_source(image_path)
        self._prepare_dirs()
        destination = self.reference_dir / f"{meter_id}.png"
        fd, tmp_name = tempfile.mkstemp(prefix=f".{meter_id}.", suffix=".tmp", dir=self.reference_dir)
        os.close(fd)
        try:
            try:
                with Image.open(source) as raw:
                    normalized = ImageOps.exif_transpose(raw).convert("RGB")
                    normalized.info.clear()
                    normalized.save(tmp_name, format="PNG", optimize=False)
            except (UnidentifiedImageError, OSError) as exc:
                raise MosOblEIRCError("reference image is unreadable or unsupported") from exc
            os.chmod(tmp_name, 0o600)
            os.replace(tmp_name, destination)
            os.chmod(destination, 0o600)
        finally:
            try:
                os.unlink(tmp_name)
            except FileNotFoundError:
                pass
        relative = f"reference-images/{meter_id}.png"
        self.state_store.set_reference(meter_id, relative)
        return self.state_store.get_reference(meter_id)

    def pending(self) -> list[dict]:
        return self.state_store.pending_references()
