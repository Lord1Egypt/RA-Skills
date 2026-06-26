"""Generic GTFS loader and cache manager.

System-agnostic: works for LIRR, Metro-North, Subway, or any GTFS feed.
Each GtfsSystem instance manages its own cache directory and feed URLs.
"""

import csv
import io
import re
import sys
import zipfile
from datetime import datetime
from pathlib import Path
from urllib.request import urlopen
from zoneinfo import ZoneInfo

from google.transit import gtfs_realtime_pb2

MTA_TZ = ZoneInfo("America/New_York")


CACHE_MAX_AGE_HOURS = 24
DOWNLOAD_TIMEOUT_SEC = 60


# --- Standalone utility functions (used across modules) ---

def parse_gtfs_time(t):
    """Parse GTFS time (HH:MM:SS, may be >24h for next-day service). Returns total minutes."""
    parts = t.split(":")
    return int(parts[0]) * 60 + int(parts[1])


def format_time(minutes):
    """Format minutes since midnight as HH:MM AM/PM."""
    h = minutes // 60
    m = minutes % 60
    if h >= 24:
        h -= 24
    period = "AM" if h < 12 else "PM"
    display_h = h % 12
    if display_h == 0:
        display_h = 12
    return f"{display_h}:{m:02d} {period}"


def apply_realtime(entry, rt_stops, origin_id, dest_id, sched_dep_min):
    """Overlay realtime arrival/departure data onto a train entry in-place.

    Updates depart/depart_str/delay_min/status and arrive/arrive_str/duration
    when realtime data is present. Guards against midnight wrap in the delay
    calculation (clamped to ±12h).
    """
    rt_dep = rt_stops.get(origin_id, {}).get("dep")
    rt_arr = rt_stops.get(dest_id, {}).get("arr")

    if rt_dep:
        rt_dep_dt = datetime.fromtimestamp(rt_dep, tz=MTA_TZ)
        rt_dep_min = rt_dep_dt.hour * 60 + rt_dep_dt.minute
        delay = rt_dep_min - (sched_dep_min % (24 * 60))
        if delay > 12 * 60:
            delay -= 24 * 60
        elif delay < -12 * 60:
            delay += 24 * 60
        entry["depart"] = rt_dep_min
        entry["depart_str"] = format_time(rt_dep_min)
        entry["delay_min"] = delay
        if delay > 0:
            entry["status"] = f"{delay}min late"
        elif delay < 0:
            entry["status"] = f"{abs(delay)}min early"
        else:
            entry["status"] = "On time"

    if rt_arr:
        rt_arr_dt = datetime.fromtimestamp(rt_arr, tz=MTA_TZ)
        rt_arr_min = rt_arr_dt.hour * 60 + rt_arr_dt.minute
        # If arrival wrapped past midnight, bump into "next day" minute space
        # so duration stays positive.
        if rt_arr_min < entry["depart"]:
            rt_arr_min += 24 * 60
        entry["arrive"] = rt_arr_min
        entry["arrive_str"] = format_time(rt_arr_min)
        entry["duration"] = rt_arr_min - entry["depart"]


def fuzzy_match_station(query, stops):
    """Find stations matching a query string. Returns list of (stop_id, stop_name, score)."""
    query_lower = query.lower().strip()
    matches = []
    for sid, s in stops.items():
        name = s["stop_name"].lower()
        code = s.get("stop_code", "").lower()
        if query_lower == code:
            matches.append((sid, s["stop_name"], 100))
        elif query_lower == name:
            matches.append((sid, s["stop_name"], 95))
        elif name.startswith(query_lower):
            matches.append((sid, s["stop_name"], 80))
        elif query_lower in name:
            matches.append((sid, s["stop_name"], 60))
        else:
            q_words = set(query_lower.split())
            n_words = set(name.split())
            overlap = q_words & n_words
            if overlap and len(overlap) >= len(q_words) * 0.5:
                matches.append((sid, s["stop_name"], 40 + len(overlap) * 10))
    matches.sort(key=lambda x: -x[2])
    return matches


class GtfsSystem:
    """A single GTFS transit system with caching and real-time support."""

    def __init__(self, key, name, short_name, gtfs_url, cache_dir,
                 gtfs_rt_url=None, alerts_url=None, alerts_agency_id=None):
        self.key = key
        self.name = name
        self.short_name = short_name
        self.gtfs_url = gtfs_url
        self.gtfs_rt_url = gtfs_rt_url
        self.alerts_url = alerts_url
        self.alerts_agency_id = alerts_agency_id
        self.cache_dir = Path(cache_dir)
        self.cache_zip = self.cache_dir / f"gtfs_{key}.zip"

    @classmethod
    def from_config(cls, key, config, data_dir):
        """Create a GtfsSystem from a feeds.json config entry."""
        return cls(
            key=key,
            name=config["name"],
            short_name=config["short_name"],
            gtfs_url=config["gtfs_url"],
            cache_dir=Path(data_dir) / config["cache_dir"],
            gtfs_rt_url=config.get("gtfs_rt_url"),
            alerts_url=config.get("alerts_url"),
            alerts_agency_id=config.get("alerts_agency_id"),
        )

    def ensure_cache(self):
        """Download GTFS data if missing or stale."""
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        if self.cache_zip.exists():
            age = datetime.now().timestamp() - self.cache_zip.stat().st_mtime
            if age < CACHE_MAX_AGE_HOURS * 3600:
                return
        print(f"Downloading {self.name} GTFS data...", file=sys.stderr)
        tmp_path = self.cache_zip.with_suffix(self.cache_zip.suffix + ".part")
        try:
            with urlopen(self.gtfs_url, timeout=DOWNLOAD_TIMEOUT_SEC) as resp, \
                 open(tmp_path, "wb") as out:
                while True:
                    chunk = resp.read(65536)
                    if not chunk:
                        break
                    out.write(chunk)
            tmp_path.replace(self.cache_zip)
        except Exception:
            if tmp_path.exists():
                tmp_path.unlink()
            raise
        for f in self.cache_dir.glob("*.txt"):
            f.unlink()

    def _read_file(self, filename):
        """Read a CSV file from the cached GTFS zip."""
        cached_txt = self.cache_dir / filename
        if cached_txt.exists():
            with open(cached_txt, "r", encoding="utf-8-sig") as f:
                return list(csv.DictReader(f))
        with zipfile.ZipFile(self.cache_zip, "r") as zf:
            with zf.open(filename) as f:
                text = f.read().decode("utf-8-sig")
                cached_txt.write_text(text)
                return list(csv.DictReader(io.StringIO(text)))

    def load_stops(self):
        """Load station data. Returns dict keyed by stop_id."""
        rows = self._read_file("stops.txt")
        return {r["stop_id"]: r for r in rows}

    def load_routes(self):
        """Load route data. Returns dict keyed by route_id."""
        rows = self._read_file("routes.txt")
        return {r["route_id"]: r for r in rows}

    def load_trips(self):
        """Load trip data. Returns dict keyed by trip_id."""
        rows = self._read_file("trips.txt")
        return {r["trip_id"]: r for r in rows}

    def load_stop_times(self):
        """Load stop_times. Returns list of dicts."""
        return self._read_file("stop_times.txt")

    def load_active_services(self, date_str):
        """Get set of service_ids active on a given date (YYYY-MM-DD).

        Supports both calendar_dates.txt (LIRR/MNR) and calendar.txt (Subway).
        """
        target = date_str.replace("-", "")
        active = set()
        removed = set()

        # calendar_dates.txt — exceptions
        try:
            rows = self._read_file("calendar_dates.txt")
            for r in rows:
                if r["date"] == target:
                    if r["exception_type"] == "1":
                        active.add(r["service_id"])
                    elif r["exception_type"] == "2":
                        removed.add(r["service_id"])
        except (KeyError, FileNotFoundError):
            pass

        # calendar.txt — regular weekly schedules
        try:
            cal_rows = self._read_file("calendar.txt")
            dow = datetime.strptime(date_str, "%Y-%m-%d").weekday()
            day_names = ["monday", "tuesday", "wednesday", "thursday",
                         "friday", "saturday", "sunday"]
            day_col = day_names[dow]
            for r in cal_rows:
                start = r.get("start_date", "")
                end = r.get("end_date", "")
                if start <= target <= end and r.get(day_col) == "1":
                    active.add(r["service_id"])
        except (KeyError, FileNotFoundError):
            pass

        return active - removed

    def fetch_realtime(self):
        """Fetch GTFS-RT trip updates.

        Returns dict of trip_id -> {stop_id -> {arr, dep}} with unix timestamps.
        Returns empty dict if no RT URL configured or on network error.
        """
        if not self.gtfs_rt_url:
            return {}

        try:
            data = urlopen(self.gtfs_rt_url, timeout=10).read()
        except Exception as e:
            print(f"Warning: could not fetch {self.short_name} real-time data: {e}",
                  file=sys.stderr)
            return {}

        feed = gtfs_realtime_pb2.FeedMessage()
        feed.ParseFromString(data)

        rt = {}
        for entity in feed.entity:
            if not entity.HasField("trip_update"):
                continue
            tu = entity.trip_update
            tid = tu.trip.trip_id
            stops = {}
            for stu in tu.stop_time_update:
                stops[stu.stop_id] = {
                    "arr": stu.arrival.time if stu.arrival.time else None,
                    "dep": stu.departure.time if stu.departure.time else None,
                }
            rt[tid] = stops
        return rt

    def fetch_alerts(self):
        """Fetch service alerts for this system.

        Filters the shared MTA alerts feed by this system's agency_id.
        Returns list of {"header": str, "description": str}.
        """
        if not self.alerts_url or not self.alerts_agency_id:
            return []

        try:
            data = urlopen(self.alerts_url, timeout=10).read()
        except Exception as e:
            print(f"Warning: could not fetch {self.short_name} alerts: {e}",
                  file=sys.stderr)
            return []

        feed = gtfs_realtime_pb2.FeedMessage()
        feed.ParseFromString(data)

        agency_id = self.alerts_agency_id
        alerts = []
        seen_headers = set()
        for entity in feed.entity:
            if not entity.HasField("alert"):
                continue
            alert = entity.alert
            is_match = False
            for ie in alert.informed_entity:
                if ie.agency_id == agency_id or (
                    ie.route_id and ie.route_id.startswith(agency_id)
                ):
                    is_match = True
                    break
            if not is_match:
                continue

            header = ""
            for t in alert.header_text.translation:
                if t.language in ("en", ""):
                    header = t.text
                    break
            if not header:
                continue

            desc = ""
            for t in alert.description_text.translation:
                if t.language in ("en", ""):
                    desc = t.text
                    break

            header = re.sub(r"<[^>]+>", "", header).strip()
            desc = re.sub(r"<[^>]+>", "", desc).strip()

            if header in seen_headers:
                continue
            seen_headers.add(header)

            alerts.append({"header": header, "description": desc})
        return alerts

    def find_trains(self, origin_id, dest_id, date_str, time_str=None,
                    count=5, realtime=None):
        """Find trains from origin to destination on a given date.

        Returns list of dicts sorted by departure time.
        """
        active_services = self.load_active_services(date_str)
        if not active_services:
            return []

        trips = self.load_trips()
        routes = self.load_routes()
        stops = self.load_stops()
        stop_times = self.load_stop_times()

        trip_stops = {}
        for st in stop_times:
            tid = st["trip_id"]
            if tid not in trip_stops:
                trip_stops[tid] = []
            trip_stops[tid].append({
                "stop_id": st["stop_id"],
                "departure": st["departure_time"],
                "arrival": st["arrival_time"],
                "sequence": int(st["stop_sequence"]),
            })

        results = []
        for tid, tstops in trip_stops.items():
            trip = trips.get(tid)
            if not trip:
                continue
            if trip["service_id"] not in active_services:
                continue

            origin_stop = None
            dest_stop = None
            for ts in tstops:
                if ts["stop_id"] == origin_id:
                    origin_stop = ts
                if ts["stop_id"] == dest_id:
                    dest_stop = ts

            if origin_stop and dest_stop and origin_stop["sequence"] < dest_stop["sequence"]:
                dep_min = parse_gtfs_time(origin_stop["departure"])
                arr_min = parse_gtfs_time(dest_stop["arrival"])
                route = routes.get(trip.get("route_id", ""), {})

                entry = {
                    "trip_id": tid,
                    "system": self.key,
                    "route": route.get("route_long_name",
                                       route.get("route_short_name", "?")),
                    "headsign": trip.get("trip_headsign", ""),
                    "depart": dep_min,
                    "depart_str": format_time(dep_min),
                    "arrive": arr_min,
                    "arrive_str": format_time(arr_min),
                    "duration": arr_min - dep_min,
                    "origin": stops[origin_id]["stop_name"],
                    "destination": stops[dest_id]["stop_name"],
                    "status": "Scheduled",
                    "delay_min": 0,
                }

                if realtime and tid in realtime:
                    apply_realtime(entry, realtime[tid], origin_id, dest_id, dep_min)

                results.append(entry)

        results.sort(key=lambda x: x["depart"])

        if time_str:
            parts = time_str.split(":")
            target_min = int(parts[0]) * 60 + int(parts[1])
            results = [r for r in results if r["depart"] >= target_min]

        return results[:count]
