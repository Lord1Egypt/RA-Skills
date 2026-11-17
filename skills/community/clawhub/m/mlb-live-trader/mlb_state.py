"""Fail-closed live trade state persistence for the MLB skill."""

from __future__ import annotations

import errno
import fcntl
import hashlib
import json
import math
import os
import tempfile
from collections.abc import Callable
from contextlib import AbstractContextManager, nullcontext
from dataclasses import asdict, dataclass, field
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from types import TracebackType
from typing import Any


class TradeStateError(RuntimeError):
    """Base exception for unsafe live trade state operations."""


class InvalidTradeStateError(TradeStateError):
    """Raised when persisted live state is corrupt or structurally invalid."""


class UninitializedTradeStateError(InvalidTradeStateError):
    """Raised when live execution has no reconciled durable ledger."""


class TradeStateAccessError(TradeStateError):
    """Raised when live state cannot be read or durably written."""


class ConcurrentLiveRunError(TradeStateError):
    """Raised when another process already owns the live execution lock."""


class UtcDateProvider:
    """Provide the current UTC date to stateful orchestration."""

    def today(self) -> str:
        """Return the current UTC date in ISO format.

        Returns:
            Current UTC date as ``YYYY-MM-DD``.
        """
        return datetime.now(timezone.utc).strftime("%Y-%m-%d")


_UTC_DATE_PROVIDER = UtcDateProvider()


class UtcClock:
    """Provide the current aware UTC timestamp to reservation logic."""

    def now(self) -> datetime:
        """Return the current aware UTC timestamp.

        Returns:
            Current UTC timestamp.
        """
        return datetime.now(timezone.utc)


_UTC_CLOCK = UtcClock()


def utc_date() -> str:
    """Return the current UTC date in ISO format.

    Returns:
        Current UTC date as ``YYYY-MM-DD``.
    """
    return _UTC_DATE_PROVIDER.today()


def utc_now() -> datetime:
    """Return the current aware UTC timestamp.

    Returns:
        Current UTC timestamp.
    """
    return _UTC_CLOCK.now()


class UtcTimestampCodec:
    """Validate and normalize persisted UTC timestamps."""

    @staticmethod
    def parse(value: object, field_name: str) -> datetime:
        """Parse one aware timestamp and normalize it to UTC.

        Args:
            value: Timestamp boundary value.
            field_name: Stable field name for an actionable error.

        Returns:
            Aware UTC timestamp.

        Raises:
            InvalidTradeStateError: If the value is not an aware ISO timestamp.
        """
        if not isinstance(value, str) or not value:
            raise InvalidTradeStateError(
                f"Live trade reservation {field_name} must be an ISO timestamp."
            )
        try:
            parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError as exc:
            raise InvalidTradeStateError(
                f"Live trade reservation {field_name} must be an ISO timestamp."
            ) from exc
        if parsed.tzinfo is None:
            raise InvalidTradeStateError(
                f"Live trade reservation {field_name} must include a timezone."
            )
        return parsed.astimezone(timezone.utc)

    @staticmethod
    def format(value: datetime) -> str:
        """Format one aware timestamp as canonical UTC ISO text.

        Args:
            value: Aware timestamp.

        Returns:
            Canonical timestamp ending in ``Z``.

        Raises:
            InvalidTradeStateError: If the value has no timezone.
        """
        if value.tzinfo is None:
            raise InvalidTradeStateError(
                "Live trade reservation timestamp must include a timezone."
            )
        return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


class ReservationTimingPolicy:
    """Bound duplicate locks to a conservative MLB settlement window."""

    _DEFAULT_TTL = timedelta(hours=48)
    _SETTLEMENT_GRACE = timedelta(hours=36)
    _LEGACY_TTL = timedelta(hours=72)
    _MAX_TTL = timedelta(hours=96)

    def expiry_for(
        self,
        *,
        reserved_at: datetime,
        game_resolves_at: str | None,
    ) -> datetime:
        """Calculate a bounded reservation expiry.

        Args:
            reserved_at: Submission-reservation timestamp.
            game_resolves_at: Market resolution timestamp when available.

        Returns:
            Conservative expiry after the game settlement window.

        Raises:
            InvalidTradeStateError: If the supplied window is unsafe.
        """
        expiry = reserved_at + self._DEFAULT_TTL
        if game_resolves_at is not None:
            resolution = UtcTimestampCodec.parse(
                game_resolves_at,
                "game_resolves_at",
            )
            expiry = resolution + self._SETTLEMENT_GRACE
        self.validate_window(reserved_at=reserved_at, expires_at=expiry)
        return expiry

    def legacy_window(self, persisted_day: str) -> tuple[datetime, datetime]:
        """Create a bounded conservative window for one legacy identifier set.

        Args:
            persisted_day: Legacy daily-counter date.

        Returns:
            Synthetic reservation and expiry timestamps.
        """
        parsed_day = date.fromisoformat(persisted_day)
        reserved_at = datetime(
            parsed_day.year,
            parsed_day.month,
            parsed_day.day,
            tzinfo=timezone.utc,
        )
        return reserved_at, reserved_at + self._LEGACY_TTL

    def validate_window(
        self,
        *,
        reserved_at: datetime,
        expires_at: datetime,
    ) -> None:
        """Reject non-positive or effectively permanent reservation windows.

        Args:
            reserved_at: Reservation creation timestamp.
            expires_at: Reservation expiry timestamp.

        Raises:
            InvalidTradeStateError: If the window is outside safe bounds.
        """
        lifetime = expires_at - reserved_at
        if lifetime <= timedelta(0) or lifetime > self._MAX_TTL:
            raise InvalidTradeStateError(
                "Live trade reservation expiry must be within 96 hours."
            )


@dataclass(frozen=True)
class LegacyImportProvenance:
    """Identify the exact legacy ledger imported into central state."""

    content_sha256: str

    @classmethod
    def from_content(cls, content: bytes) -> LegacyImportProvenance:
        """Fingerprint exact legacy file bytes for later reconciliation.

        Args:
            content: Raw legacy state file bytes.

        Returns:
            Stable SHA-256 migration provenance.
        """
        return cls(content_sha256=hashlib.sha256(content).hexdigest())

    @classmethod
    def from_dict(cls, raw: object) -> LegacyImportProvenance:
        """Validate persisted migration provenance.

        Args:
            raw: Serialized provenance boundary value.

        Returns:
            Valid migration provenance.

        Raises:
            InvalidTradeStateError: If the provenance is malformed.
        """
        if not isinstance(raw, dict) or set(raw) != {"content_sha256"}:
            raise InvalidTradeStateError(
                "Live trade state legacy_import must contain content_sha256."
            )
        content_sha256 = raw["content_sha256"]
        if (
            not isinstance(content_sha256, str)
            or len(content_sha256) != 64
            or any(character not in "0123456789abcdef" for character in content_sha256)
        ):
            raise InvalidTradeStateError(
                "Live trade state legacy_import content_sha256 must be lowercase "
                "SHA-256 text."
            )
        return cls(content_sha256=content_sha256)

    def to_dict(self) -> dict[str, str]:
        """Serialize migration provenance.

        Returns:
            JSON-compatible provenance mapping.
        """
        return {"content_sha256": self.content_sha256}


@dataclass(frozen=True)
class TradeReservation:
    """Durable duplicate lock for one attempted live market and game."""

    market_id: str | None
    game_id: str | None
    amount_usd: float
    counted_on: str
    reserved_at: str
    expires_at: str

    @classmethod
    def from_dict(
        cls,
        raw: dict[str, Any],
        timing_policy: ReservationTimingPolicy,
    ) -> TradeReservation:
        """Validate and restore a persisted reservation.

        Args:
            raw: Serialized reservation object.
            timing_policy: Bounded expiry policy.

        Returns:
            Valid normalized reservation.

        Raises:
            InvalidTradeStateError: If any reservation field is unsafe.
        """
        required_fields = {
            "market_id",
            "game_id",
            "amount_usd",
            "counted_on",
            "reserved_at",
            "expires_at",
        }
        missing_fields = sorted(required_fields.difference(raw))
        if missing_fields:
            missing = ", ".join(missing_fields)
            raise InvalidTradeStateError(
                f"Live trade reservation is missing required fields: {missing}."
            )
        market_id = cls._validate_optional_id(raw["market_id"], "market_id")
        game_id = cls._validate_optional_id(raw["game_id"], "game_id")
        if market_id is None and game_id is None:
            raise InvalidTradeStateError(
                "Live trade reservation must lock a market or game identifier."
            )
        amount_usd = DailyTradeState._validate_spent_usd(raw["amount_usd"])
        counted_on = raw["counted_on"]
        DailyTradeState._validate_date(counted_on)
        reserved_at = UtcTimestampCodec.parse(raw["reserved_at"], "reserved_at")
        expires_at = UtcTimestampCodec.parse(raw["expires_at"], "expires_at")
        timing_policy.validate_window(
            reserved_at=reserved_at,
            expires_at=expires_at,
        )
        return cls(
            market_id=market_id,
            game_id=game_id,
            amount_usd=amount_usd,
            counted_on=counted_on,
            reserved_at=UtcTimestampCodec.format(reserved_at),
            expires_at=UtcTimestampCodec.format(expires_at),
        )

    def to_dict(self) -> dict[str, Any]:
        """Serialize the reservation to its stable JSON object.

        Returns:
            JSON-compatible reservation mapping.
        """
        return asdict(self)

    def is_active(self, now: datetime) -> bool:
        """Return whether this duplicate lock has not expired.

        Args:
            now: Current aware UTC timestamp.

        Returns:
            Whether the reservation must still block submission.
        """
        return UtcTimestampCodec.parse(self.expires_at, "expires_at") > now

    @staticmethod
    def _validate_optional_id(value: object, field_name: str) -> str | None:
        if value is None:
            return None
        if not isinstance(value, str) or not value:
            raise InvalidTradeStateError(
                f"Live trade reservation {field_name} must be a non-empty string."
            )
        return value


@dataclass
class DailyTradeState:
    """Daily risk counters plus independently expiring duplicate locks."""

    date: str
    spent_usd: float = 0.0
    trades: int = 0
    reservations: list[TradeReservation] = field(default_factory=list)
    legacy_import: LegacyImportProvenance | None = None

    @property
    def market_ids(self) -> list[str]:
        """Return unique market identifiers with active persisted locks."""
        return list(
            dict.fromkeys(
                reservation.market_id
                for reservation in self.reservations
                if reservation.market_id is not None
            )
        )

    @property
    def game_ids(self) -> list[str]:
        """Return unique game identifiers with active persisted locks."""
        return list(
            dict.fromkeys(
                reservation.game_id
                for reservation in self.reservations
                if reservation.game_id is not None
            )
        )

    @classmethod
    def fresh(cls, today: str | None = None) -> DailyTradeState:
        """Create empty limits for one UTC day.

        Args:
            today: Explicit ISO date, or the current UTC date when omitted.

        Returns:
            Empty daily state.

        Raises:
            InvalidTradeStateError: If the supplied date is invalid.
        """
        current_day = today or utc_date()
        cls._validate_date(current_day)
        return cls(date=current_day)

    @classmethod
    def from_dict(
        cls,
        raw: dict[str, Any],
        today: str,
        *,
        now: datetime | None = None,
        timing_policy: ReservationTimingPolicy | None = None,
    ) -> DailyTradeState:
        """Validate, migrate, and restore persisted live state.

        Daily spend counters reset at the UTC boundary. Duplicate locks are
        retained independently until their bounded expiry, including across
        midnight, so an accepted or ambiguous submission cannot be repeated.

        Args:
            raw: Decoded JSON object.
            today: UTC date used for the daily risk boundary.
            now: Optional timestamp used to prune expired reservations.
            timing_policy: Reservation expiry validator and migration policy.

        Returns:
            Valid current-day counters and active duplicate locks.

        Raises:
            InvalidTradeStateError: If any required field is missing or invalid.
        """
        cls._validate_date(today)
        policy = timing_policy or ReservationTimingPolicy()
        required_fields = {
            "date",
            "spent_usd",
            "trades",
            "market_ids",
            "game_ids",
        }
        missing_fields = sorted(required_fields.difference(raw))
        if missing_fields:
            missing = ", ".join(missing_fields)
            raise InvalidTradeStateError(
                f"Live trade state is missing required fields: {missing}."
            )

        persisted_date = raw["date"]
        cls._validate_date(persisted_date)
        if date.fromisoformat(persisted_date) > date.fromisoformat(today):
            raise InvalidTradeStateError(
                "Live trade state date cannot be later than the current UTC date."
            )
        spent_usd = cls._validate_spent_usd(raw["spent_usd"])
        trades = cls._validate_trades(raw["trades"])
        market_ids = cls._validate_ids(raw["market_ids"], "market_ids")
        game_ids = cls._validate_ids(raw["game_ids"], "game_ids")
        reservations = cls._restore_reservations(
            raw,
            persisted_date=persisted_date,
            market_ids=market_ids,
            game_ids=game_ids,
            timing_policy=policy,
        )
        legacy_import = cls._restore_legacy_import(raw)
        cls._validate_reservation_counters(
            persisted_date=persisted_date,
            spent_usd=spent_usd,
            trades=trades,
            reservations=reservations,
        )
        if now is not None:
            cls._validate_aware_now(now)
            reservations = [
                reservation
                for reservation in reservations
                if reservation.is_active(now.astimezone(timezone.utc))
            ]

        if persisted_date != today:
            spent_usd = 0.0
            trades = 0
        return cls(
            date=today,
            spent_usd=spent_usd,
            trades=trades,
            reservations=reservations,
            legacy_import=legacy_import,
        )

    def to_dict(self) -> dict[str, Any]:
        """Serialize counters and duplicate locks using schema version 2.

        Returns:
            JSON-compatible state mapping retaining legacy identifier indexes.
        """
        serialized_state: dict[str, Any] = {
            "schema_version": 2,
            "date": self.date,
            "spent_usd": self.spent_usd,
            "trades": self.trades,
            "market_ids": self.market_ids,
            "game_ids": self.game_ids,
            "reservations": [
                reservation.to_dict() for reservation in self.reservations
            ],
        }
        if self.legacy_import is not None:
            serialized_state["legacy_import"] = self.legacy_import.to_dict()
        return serialized_state

    @staticmethod
    def _restore_legacy_import(
        raw: dict[str, Any],
    ) -> LegacyImportProvenance | None:
        if "legacy_import" not in raw:
            return None
        if raw.get("schema_version") != 2:
            raise InvalidTradeStateError(
                "Live trade state legacy_import requires schema_version 2."
            )
        return LegacyImportProvenance.from_dict(raw["legacy_import"])

    @classmethod
    def _restore_reservations(
        cls,
        raw: dict[str, Any],
        *,
        persisted_date: str,
        market_ids: list[str],
        game_ids: list[str],
        timing_policy: ReservationTimingPolicy,
    ) -> list[TradeReservation]:
        schema_version = raw.get("schema_version")
        if schema_version is None:
            if "reservations" in raw:
                raise InvalidTradeStateError(
                    "Live trade state reservations require schema_version 2."
                )
            return cls._migrate_legacy_reservations(
                persisted_date=persisted_date,
                market_ids=market_ids,
                game_ids=game_ids,
                timing_policy=timing_policy,
            )
        if isinstance(schema_version, bool) or schema_version != 2:
            raise InvalidTradeStateError("Live trade state schema_version must be 2.")
        raw_reservations = raw.get("reservations")
        if not isinstance(raw_reservations, list) or not all(
            isinstance(item, dict) for item in raw_reservations
        ):
            raise InvalidTradeStateError(
                "Live trade state reservations must be a list of objects."
            )
        reservations = [
            TradeReservation.from_dict(item, timing_policy) for item in raw_reservations
        ]
        restored = cls(
            date=persisted_date,
            reservations=reservations,
        )
        if restored.market_ids != market_ids or restored.game_ids != game_ids:
            raise InvalidTradeStateError(
                "Live trade state identifier indexes do not match reservations."
            )
        return reservations

    @staticmethod
    def _validate_reservation_counters(
        *,
        persisted_date: str,
        spent_usd: float,
        trades: int,
        reservations: list[TradeReservation],
    ) -> None:
        counted_reservations = []
        for reservation in reservations:
            if reservation.counted_on > persisted_date:
                raise InvalidTradeStateError(
                    "Live trade reservation cannot be counted on a future day."
                )
            if reservation.counted_on == persisted_date and reservation.amount_usd > 0:
                counted_reservations.append(reservation)
        reserved_amount = sum(
            reservation.amount_usd for reservation in counted_reservations
        )
        if trades < len(counted_reservations) or spent_usd + 1e-8 < reserved_amount:
            raise InvalidTradeStateError(
                "Live trade daily counters understate persisted reservations."
            )

    @classmethod
    def _migrate_legacy_reservations(
        cls,
        *,
        persisted_date: str,
        market_ids: list[str],
        game_ids: list[str],
        timing_policy: ReservationTimingPolicy,
    ) -> list[TradeReservation]:
        reserved_at, expires_at = timing_policy.legacy_window(persisted_date)
        reservations: list[TradeReservation] = []
        for index in range(max(len(market_ids), len(game_ids))):
            reservations.append(
                TradeReservation(
                    market_id=(market_ids[index] if index < len(market_ids) else None),
                    game_id=(game_ids[index] if index < len(game_ids) else None),
                    amount_usd=0.0,
                    counted_on=persisted_date,
                    reserved_at=UtcTimestampCodec.format(reserved_at),
                    expires_at=UtcTimestampCodec.format(expires_at),
                )
            )
        return reservations

    @staticmethod
    def _validate_date(value: object) -> None:
        if not isinstance(value, str):
            raise InvalidTradeStateError("Live trade state date must be a string.")
        try:
            parsed = date.fromisoformat(value)
        except ValueError as exc:
            raise InvalidTradeStateError(
                "Live trade state date must use YYYY-MM-DD format."
            ) from exc
        if parsed.isoformat() != value:
            raise InvalidTradeStateError(
                "Live trade state date must use YYYY-MM-DD format."
            )

    @staticmethod
    def _validate_spent_usd(value: object) -> float:
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise InvalidTradeStateError(
                "Live trade state spent_usd must be a finite non-negative number."
            )
        normalized = float(value)
        if not math.isfinite(normalized) or normalized < 0:
            raise InvalidTradeStateError(
                "Live trade state spent_usd must be a finite non-negative number."
            )
        return normalized

    @staticmethod
    def _validate_trades(value: object) -> int:
        if isinstance(value, bool) or not isinstance(value, int) or value < 0:
            raise InvalidTradeStateError(
                "Live trade state trades must be a non-negative integer."
            )
        return value

    @staticmethod
    def _validate_ids(value: object, field_name: str) -> list[str]:
        if not isinstance(value, list) or not all(
            isinstance(item, str) and item for item in value
        ):
            raise InvalidTradeStateError(
                f"Live trade state {field_name} must be a list of non-empty strings."
            )
        return list(value)

    @staticmethod
    def _validate_aware_now(value: datetime) -> None:
        if value.tzinfo is None:
            raise InvalidTradeStateError(
                "Live trade state clock must provide an aware timestamp."
            )


class ExclusiveLiveRunLock(AbstractContextManager[None]):
    """Non-blocking advisory file lock for one live strategy run."""

    def __init__(self, path: Path) -> None:
        """Initialize a lock for a deterministic filesystem path.

        Args:
            path: Lock file path shared by competing live processes.
        """
        self._path = path
        self._file_descriptor: int | None = None

    def __enter__(self) -> None:
        """Acquire the live execution lock without waiting.

        Raises:
            ConcurrentLiveRunError: If another live run owns the lock.
            TradeStateAccessError: If the lock file cannot be opened or secured.
        """
        flags = os.O_RDWR | os.O_CREAT
        flags |= getattr(os, "O_CLOEXEC", 0)
        flags |= getattr(os, "O_NOFOLLOW", 0)
        descriptor: int | None = None
        try:
            self._path.parent.mkdir(parents=True, exist_ok=True)
            descriptor = os.open(self._path, flags, 0o600)
            os.fchmod(descriptor, 0o600)
        except OSError as exc:
            if descriptor is not None:
                os.close(descriptor)
            raise TradeStateAccessError(
                f"Cannot open live execution lock at {self._path}."
            ) from exc

        if descriptor is None:
            raise TradeStateAccessError(
                f"Cannot open live execution lock at {self._path}."
            )
        try:
            fcntl.flock(descriptor, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError as exc:
            os.close(descriptor)
            if exc.errno in {errno.EACCES, errno.EAGAIN}:
                raise ConcurrentLiveRunError(
                    "Another live MLB trader run is already active."
                ) from exc
            raise TradeStateAccessError(
                f"Cannot acquire live execution lock at {self._path}."
            ) from exc
        self._file_descriptor = descriptor

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        """Release the process lock while preserving body exceptions.

        Args:
            exc_type: Exception type raised inside the context, if any.
            exc_value: Exception raised inside the context, if any.
            traceback: Traceback for the body exception, if any.
        """
        del exc_type, exc_value, traceback
        descriptor = self._file_descriptor
        if descriptor is None:
            return
        self._file_descriptor = None
        try:
            fcntl.flock(descriptor, fcntl.LOCK_UN)
        finally:
            os.close(descriptor)


LockFactory = Callable[[Path], AbstractContextManager[None]]
ReplaceFile = Callable[[Path, Path], None]
DateProvider = Callable[[], str]
TimestampProvider = Callable[[], datetime]


class TradeStateStore:
    """Persist live risk state atomically and coordinate live processes."""

    _CENTRAL_MARKER_CONTENT = b'{"format":"mlb-live-trader-central-state-v1"}\n'

    def __init__(
        self,
        path: Path,
        *,
        legacy_path: Path | None = None,
        date_provider: DateProvider | None = None,
        clock: TimestampProvider | None = None,
        reservation_timing: ReservationTimingPolicy | None = None,
        lock_factory: LockFactory = ExclusiveLiveRunLock,
        replace_file: ReplaceFile = os.replace,
    ) -> None:
        """Initialize the state adapter and its deterministic seams.

        Args:
            path: JSON state file path.
            legacy_path: Optional pre-v2.2 state file imported when path is absent.
            date_provider: Injectable UTC date source.
            clock: Injectable aware UTC timestamp source.
            reservation_timing: Injectable bounded reservation timing policy.
            lock_factory: Injectable non-blocking live lock factory.
            replace_file: Injectable atomic filesystem replacement operation.
        """
        self.path = path
        self._central_marker_path = self.path.with_name(f"{self.path.name}.initialized")
        self._legacy_path = legacy_path if legacy_path != path else None
        self._legacy_archive_path = (
            self._legacy_path.with_name(f"{self._legacy_path.name}.migrated")
            if self._legacy_path is not None
            else None
        )
        self._date_provider = date_provider if date_provider is not None else utc_date
        self._clock = clock if clock is not None else utc_now
        self._reservation_timing = reservation_timing or ReservationTimingPolicy()
        self._lock_factory = lock_factory
        self._replace_file = replace_file

    def execution_lock(self, *, live: bool) -> AbstractContextManager[None]:
        """Return a whole-run execution lock for the selected mode.

        The returned context manager is a no-op in paper mode. Live callers
        must hold it around the complete load, scan, trade, and save lifecycle.

        Args:
            live: Whether the enclosing run can submit live trades.

        Returns:
            Non-blocking live lock or a paper-mode no-op context manager.
        """
        if not live:
            return nullcontext()
        return self._lock_factory(self.path.with_suffix(self.path.suffix + ".lock"))

    def load(self, *, live: bool, today: str | None = None) -> DailyTradeState:
        """Load validated live state or isolated paper state.

        Args:
            live: Whether persisted live state should be read.
            today: Explicit UTC date for deterministic callers.

        Returns:
            Valid daily trade state.

        Raises:
            InvalidTradeStateError: If live state is corrupt or invalid.
            TradeStateAccessError: If an existing live state file is unreadable.
        """
        current_day = today or self._date_provider()
        if not live:
            return DailyTradeState.fresh(current_day)
        central_content = self._read_optional_state(
            self.path,
            description="live trade state",
        )
        central_marker_content = self._read_optional_state(
            self._central_marker_path,
            description="live trade state initialization marker",
        )
        if central_marker_content is not None:
            self._validate_central_marker(central_marker_content)
        if central_content is None and central_marker_content is not None:
            raise InvalidTradeStateError(
                "A live-state initialization marker exists but central state is "
                "missing; restore or reconcile the central ledger before live "
                "trading."
            )
        legacy_content = (
            self._read_optional_state(
                self._legacy_path,
                description="legacy live trade state",
            )
            if self._legacy_path is not None
            else None
        )
        legacy_archive_content = (
            self._read_optional_state(
                self._legacy_archive_path,
                description="migrated legacy live trade state",
            )
            if self._legacy_archive_path is not None
            else None
        )
        if legacy_content is not None and legacy_archive_content is not None:
            raise InvalidTradeStateError(
                "An active legacy live trade state reappeared after it was migrated; "
                "stop old writers and reconcile both files before live trading."
            )
        if central_content is None and legacy_archive_content is not None:
            raise InvalidTradeStateError(
                "A migrated legacy live trade state exists but central state is "
                "missing; restore or reconcile the central ledger before live "
                "trading."
            )
        if central_content is not None:
            source_path = self.path
            content = central_content
        elif legacy_content is not None and self._legacy_path is not None:
            source_path = self._legacy_path
            content = legacy_content
        else:
            raise UninitializedTradeStateError(
                "Live trade state is not initialized; stop prior schedulers and run "
                "--initialize-live-state before live trading."
            )

        try:
            serialized = content.decode("utf-8")
            raw = json.loads(serialized)
        except (json.JSONDecodeError, UnicodeError) as exc:
            raise InvalidTradeStateError(
                f"Live trade state at {source_path} contains invalid JSON."
            ) from exc
        if not isinstance(raw, dict):
            raise InvalidTradeStateError(
                f"Live trade state at {source_path} must be a JSON object."
            )
        state = DailyTradeState.from_dict(
            raw,
            current_day,
            now=self._clock(),
            timing_policy=self._reservation_timing,
        )
        migration_content = legacy_content or legacy_archive_content
        if source_path == self.path:
            if migration_content is not None:
                expected_import = LegacyImportProvenance.from_content(migration_content)
                if state.legacy_import != expected_import:
                    raise InvalidTradeStateError(
                        "Central and legacy live trade state do not share the "
                        "recorded migration provenance; reconcile both ledgers "
                        "before live trading."
                    )
            self._ensure_central_marker()
            if legacy_content is not None:
                self._archive_legacy_state()
        else:
            state.legacy_import = LegacyImportProvenance.from_content(content)
            self.save(state, live=True)
            self._archive_legacy_state()
        return state

    def initialize_empty(self, *, today: str | None = None) -> DailyTradeState:
        """Create the first empty live ledger after external reconciliation.

        Callers must hold :meth:`execution_lock` and must first prove through a
        read-only account audit that no prior exposure or recent receipt can be
        lost. Existing central or legacy content is never overwritten.

        Args:
            today: Explicit UTC date for deterministic callers.

        Returns:
            Newly persisted empty live state.

        Raises:
            InvalidTradeStateError: If central or legacy state already exists.
            TradeStateAccessError: If state cannot be read or durably created.
        """
        if (
            self._read_optional_state(
                self.path,
                description="live trade state",
            )
            is not None
        ):
            raise InvalidTradeStateError(
                "Live trade state already exists; load and reconcile it instead."
            )
        central_marker_content = self._read_optional_state(
            self._central_marker_path,
            description="live trade state initialization marker",
        )
        if central_marker_content is not None:
            self._validate_central_marker(central_marker_content)
            raise InvalidTradeStateError(
                "A live-state initialization marker exists but central state is "
                "missing; restore or reconcile it instead."
            )
        if self._legacy_path is not None and (
            self._read_optional_state(
                self._legacy_path,
                description="legacy live trade state",
            )
            is not None
        ):
            raise InvalidTradeStateError(
                "A legacy live trade state exists; import and reconcile it instead."
            )
        if self._legacy_archive_path is not None and (
            self._read_optional_state(
                self._legacy_archive_path,
                description="migrated legacy live trade state",
            )
            is not None
        ):
            raise InvalidTradeStateError(
                "A migrated legacy live trade state exists; restore or reconcile "
                "the central ledger instead."
            )
        state = DailyTradeState.fresh(today or self._date_provider())
        self.save(state, live=True)
        return state

    def _archive_legacy_state(self) -> None:
        """Move one consumed legacy ledger to a durable owner-only marker."""
        if self._legacy_path is None or self._legacy_archive_path is None:
            raise InvalidTradeStateError(
                "Legacy migration paths are unavailable for archival."
            )
        try:
            self._replace_file(self._legacy_path, self._legacy_archive_path)
            self._legacy_archive_path.chmod(0o600)
            self._sync_parent_directory(self._legacy_archive_path.parent)
        except OSError as exc:
            raise TradeStateAccessError(
                "Cannot archive the imported legacy live trade state; live trading "
                "remains blocked until migration can be retried."
            ) from exc

    @classmethod
    def _validate_central_marker(cls, content: bytes) -> None:
        """Reject a corrupt or foreign central-state generation marker."""
        if content != cls._CENTRAL_MARKER_CONTENT:
            raise InvalidTradeStateError(
                "Live trade state initialization marker is invalid; reconcile the "
                "central ledger before live trading."
            )

    def _ensure_central_marker(self) -> None:
        """Create or validate the durable central-state generation marker."""
        existing = self._read_optional_state(
            self._central_marker_path,
            description="live trade state initialization marker",
        )
        if existing is not None:
            self._validate_central_marker(existing)
            return

        descriptor: int | None = None
        flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
        flags |= getattr(os, "O_CLOEXEC", 0)
        flags |= getattr(os, "O_NOFOLLOW", 0)
        try:
            self._central_marker_path.parent.mkdir(parents=True, exist_ok=True)
            descriptor = os.open(self._central_marker_path, flags, 0o600)
            os.fchmod(descriptor, 0o600)
            with os.fdopen(descriptor, "wb") as marker_file:
                descriptor = None
                marker_file.write(self._CENTRAL_MARKER_CONTENT)
                marker_file.flush()
                os.fsync(marker_file.fileno())
            self._sync_parent_directory(self._central_marker_path.parent)
        except FileExistsError as exc:
            concurrent_content = self._read_optional_state(
                self._central_marker_path,
                description="live trade state initialization marker",
            )
            if concurrent_content is None:
                raise TradeStateAccessError(
                    "Live trade state initialization marker disappeared during "
                    "creation."
                ) from exc
            self._validate_central_marker(concurrent_content)
        except OSError as exc:
            raise TradeStateAccessError(
                "Cannot durably create the live trade state initialization marker."
            ) from exc
        finally:
            if descriptor is not None:
                os.close(descriptor)

    @staticmethod
    def _read_optional_state(
        path: Path,
        *,
        description: str,
    ) -> bytes | None:
        """Read an optional state file without treating absence as corruption.

        Args:
            path: State file path.
            description: Stable wording for an actionable access error.

        Returns:
            Exact file bytes, or ``None`` when the file does not exist.

        Raises:
            TradeStateAccessError: If an existing state file cannot be read.
        """
        try:
            return path.read_bytes()
        except FileNotFoundError:
            return None
        except OSError as exc:
            raise TradeStateAccessError(
                f"Cannot read {description} at {path}."
            ) from exc

    def save(self, state: DailyTradeState, *, live: bool) -> None:
        """Atomically save validated live state with owner-only permissions.

        Args:
            state: Daily risk counters to persist.
            live: Whether persistence is authorized for this run.

        Raises:
            InvalidTradeStateError: If the in-memory state is invalid.
            TradeStateAccessError: If the atomic save cannot complete.
        """
        if not live:
            return
        serialized_state = state.to_dict()
        DailyTradeState.from_dict(
            serialized_state,
            state.date,
            timing_policy=self._reservation_timing,
        )
        try:
            payload = (
                json.dumps(
                    serialized_state,
                    indent=2,
                    allow_nan=False,
                )
                + "\n"
            )
        except (TypeError, ValueError) as exc:
            raise InvalidTradeStateError(
                "Live trade state cannot be serialized safely."
            ) from exc

        self._ensure_central_marker()

        temporary_path: Path | None = None
        temporary_descriptor: int | None = None
        try:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            temporary_descriptor, temporary_name = tempfile.mkstemp(
                dir=self.path.parent,
                prefix=f".{self.path.name}.",
                suffix=".tmp",
            )
            temporary_path = Path(temporary_name)
            os.fchmod(temporary_descriptor, 0o600)
            with os.fdopen(
                temporary_descriptor, "w", encoding="utf-8"
            ) as temporary_file:
                temporary_descriptor = None
                temporary_file.write(payload)
                temporary_file.flush()
                os.fsync(temporary_file.fileno())
            self._replace_file(temporary_path, self.path)
            temporary_path = None
            self.path.chmod(0o600)
            self._sync_parent_directory()
        except OSError as exc:
            raise TradeStateAccessError(
                f"Cannot atomically save live trade state at {self.path}."
            ) from exc
        finally:
            if temporary_descriptor is not None:
                os.close(temporary_descriptor)
            if temporary_path is not None and temporary_path.exists():
                try:
                    temporary_path.unlink()
                except OSError as exc:
                    raise TradeStateAccessError(
                        f"Cannot remove temporary live state at {temporary_path}."
                    ) from exc

    def reserve_trade(
        self,
        state: DailyTradeState,
        *,
        live: bool,
        market_id: str,
        game_id: str,
        amount_usd: float,
        game_resolves_at: str | None = None,
    ) -> DailyTradeState:
        """Durably reserve daily capacity before a live order submission.

        Args:
            state: Current daily counters.
            live: Whether the caller can submit a live trade.
            market_id: Runtime-discovered market identifier.
            game_id: Matched MLB game identifier.
            amount_usd: Amount about to be submitted in US dollars.
            game_resolves_at: Market resolution timestamp used for lock expiry.

        Returns:
            Updated state. Paper state is returned unchanged.

        Raises:
            InvalidTradeStateError: If the state or reservation is invalid.
            TradeStateAccessError: If the reservation cannot be persisted.
        """
        if not live:
            return state
        return self._add_trade(
            state,
            market_id=market_id,
            game_id=game_id,
            amount_usd=amount_usd,
            game_resolves_at=game_resolves_at,
        )

    def refresh(
        self,
        state: DailyTradeState,
        *,
        live: bool,
    ) -> DailyTradeState:
        """Refresh live counters at the UTC boundary before risk checks.

        Args:
            state: Current daily counters.
            live: Whether persisted live state is active.

        Returns:
            Valid current-day state. Paper state is returned unchanged.

        Raises:
            InvalidTradeStateError: If the state or current date is invalid.
            TradeStateAccessError: If a day rollover cannot be persisted.
        """
        if not live:
            return state
        previous_state = state.to_dict()
        self._refresh_current_state(state)
        if state.to_dict() != previous_state:
            self.save(state, live=True)
        return state

    def release_trade(
        self,
        state: DailyTradeState,
        *,
        live: bool,
        market_id: str,
        game_id: str,
        amount_usd: float,
    ) -> DailyTradeState:
        """Release a reservation after a confirmed live-order rejection.

        Callers must retain the reservation when submission status is
        ambiguous. Removing capacity is safe only after the execution adapter
        proves that no order was accepted.

        Args:
            state: State containing the persisted reservation.
            live: Whether the rejected submission was a live attempt.
            market_id: Reserved market identifier.
            game_id: Reserved MLB game identifier.
            amount_usd: Reserved amount in US dollars.

        Returns:
            Updated state. Paper state is returned unchanged.

        Raises:
            InvalidTradeStateError: If no exact reservation can be released.
            TradeStateAccessError: If the release cannot be persisted.
        """
        if not live:
            return state
        self._validate_trade_details(market_id, game_id, amount_usd)
        self._refresh_current_state(state)
        reservation_index = next(
            (
                index
                for index, reservation in enumerate(state.reservations)
                if reservation.market_id == market_id
                and reservation.game_id == game_id
                and math.isclose(
                    reservation.amount_usd,
                    amount_usd,
                    rel_tol=0.0,
                    abs_tol=1e-8,
                )
            ),
            None,
        )
        if reservation_index is None:
            raise InvalidTradeStateError(
                "Cannot release a live trade reservation that is not recorded."
            )
        reservation = state.reservations[reservation_index]
        if reservation.counted_on == state.date:
            if state.trades < 1 or amount_usd > state.spent_usd:
                raise InvalidTradeStateError(
                    "Cannot release more than the recorded daily live capacity."
                )
            state.trades -= 1
            state.spent_usd = round(state.spent_usd - amount_usd, 8)
        state.reservations.pop(reservation_index)
        self.save(state, live=True)
        return state

    def record_trade(
        self,
        state: DailyTradeState,
        *,
        live: bool,
        market_id: str,
        game_id: str,
        amount_usd: float,
        game_resolves_at: str | None = None,
    ) -> DailyTradeState:
        """Record and persist one confirmed live trade.

        Args:
            state: Current daily counters.
            live: Whether the trade occurred in live mode.
            market_id: Runtime-discovered market identifier.
            game_id: Matched MLB game identifier.
            amount_usd: Confirmed trade amount in US dollars.
            game_resolves_at: Market resolution timestamp used for lock expiry.

        Returns:
            Updated state. Paper state is returned unchanged.
        """
        if not live:
            return state
        return self._add_trade(
            state,
            market_id=market_id,
            game_id=game_id,
            amount_usd=amount_usd,
            game_resolves_at=game_resolves_at,
        )

    def _add_trade(
        self,
        state: DailyTradeState,
        *,
        market_id: str,
        game_id: str,
        amount_usd: float,
        game_resolves_at: str | None,
    ) -> DailyTradeState:
        """Rotate the UTC boundary, add capacity usage, and persist it."""
        self._validate_trade_details(market_id, game_id, amount_usd)
        current_time = self._clock()
        DailyTradeState._validate_aware_now(current_time)
        current_time = current_time.astimezone(timezone.utc)
        current_day = current_time.strftime("%Y-%m-%d")
        self._refresh_current_state(
            state,
            current_time=current_time,
        )
        expires_at = self._reservation_timing.expiry_for(
            reserved_at=current_time,
            game_resolves_at=game_resolves_at,
        )
        state.reservations.append(
            TradeReservation(
                market_id=market_id,
                game_id=game_id,
                amount_usd=float(amount_usd),
                counted_on=current_day,
                reserved_at=UtcTimestampCodec.format(current_time),
                expires_at=UtcTimestampCodec.format(expires_at),
            )
        )
        state.spent_usd = round(state.spent_usd + amount_usd, 8)
        state.trades += 1
        self.save(state, live=True)
        return state

    def _refresh_current_state(
        self,
        state: DailyTradeState,
        *,
        current_day: str | None = None,
        current_time: datetime | None = None,
    ) -> None:
        """Validate, rotate daily counters, and prune expired duplicate locks."""
        resolved_time = current_time if current_time is not None else self._clock()
        DailyTradeState._validate_aware_now(resolved_time)
        resolved_time = resolved_time.astimezone(timezone.utc)
        resolved_day = current_day or resolved_time.strftime("%Y-%m-%d")
        current_state = DailyTradeState.from_dict(
            state.to_dict(),
            resolved_day,
            now=resolved_time,
            timing_policy=self._reservation_timing,
        )
        state.date = current_state.date
        state.spent_usd = current_state.spent_usd
        state.trades = current_state.trades
        state.reservations = current_state.reservations

    @staticmethod
    def _validate_state(state: DailyTradeState) -> None:
        """Reject an invalid in-memory state before mutating it."""
        DailyTradeState.from_dict(state.to_dict(), state.date)

    @staticmethod
    def _validate_trade_details(
        market_id: str,
        game_id: str,
        amount_usd: float,
    ) -> None:
        """Validate one reservation boundary without exposing identifiers."""
        if (
            not isinstance(market_id, str)
            or not market_id
            or not isinstance(game_id, str)
            or not game_id
        ):
            raise InvalidTradeStateError(
                "Live trade market and game identifiers must be non-empty."
            )
        if (
            isinstance(amount_usd, bool)
            or not isinstance(amount_usd, (int, float))
            or not math.isfinite(float(amount_usd))
            or amount_usd <= 0
        ):
            raise InvalidTradeStateError(
                "Live trade amount must be a finite positive number."
            )

    def _sync_parent_directory(self, directory: Path | None = None) -> None:
        """Durably commit an atomic replacement in one parent directory."""
        target_directory = directory or self.path.parent
        flags = os.O_RDONLY
        flags |= getattr(os, "O_CLOEXEC", 0)
        flags |= getattr(os, "O_DIRECTORY", 0)
        descriptor = os.open(target_directory, flags)
        try:
            os.fsync(descriptor)
        finally:
            os.close(descriptor)
