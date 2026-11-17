#!/usr/bin/env python3
"""
Natal chart calculator using Swiss Ephemeris (pyswisseph).
"""

from __future__ import annotations

import argparse
import json
import math
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

import swisseph as swe


ZODIAC_SIGNS = [
    "Aries",
    "Taurus",
    "Gemini",
    "Cancer",
    "Leo",
    "Virgo",
    "Libra",
    "Scorpio",
    "Sagittarius",
    "Capricorn",
    "Aquarius",
    "Pisces",
]


PLANETS = {
    "Sun": swe.SUN,
    "Moon": swe.MOON,
    "Mercury": swe.MERCURY,
    "Venus": swe.VENUS,
    "Mars": swe.MARS,
    "Jupiter": swe.JUPITER,
    "Saturn": swe.SATURN,
    "Uranus": swe.URANUS,
    "Neptune": swe.NEPTUNE,
    "Pluto": swe.PLUTO,
    "TrueNode": swe.TRUE_NODE,
    "Chiron": swe.CHIRON,
}

ASPECTS = {
    "Conjunction": {"angle": 0.0, "orb": 8.0, "abbr": "Conj"},
    "Opposition": {"angle": 180.0, "orb": 8.0, "abbr": "Opp"},
    "Square": {"angle": 90.0, "orb": 6.0, "abbr": "Sqr"},
    "Trine": {"angle": 120.0, "orb": 6.0, "abbr": "Tri"},
    "Sextile": {"angle": 60.0, "orb": 4.0, "abbr": "Sex"},
}

SIDEREAL_MODES = {
    "fagan-bradley": swe.SIDM_FAGAN_BRADLEY,
    "lahiri": swe.SIDM_LAHIRI,
    "deluce": swe.SIDM_DELUCE,
    "raman": swe.SIDM_RAMAN,
    "krishnamurti": swe.SIDM_KRISHNAMURTI,
    "djwhal-khul": swe.SIDM_DJWHAL_KHUL,
    "yukteshwar": swe.SIDM_YUKTESHWAR,
    "jn-bhasin": swe.SIDM_JN_BHASIN,
}


@dataclass
class ChartPoint:
    name: str
    longitude: float
    sign: str
    sign_degree: float
    house: int


@dataclass
class Aspect:
    point_a: str
    point_b: str
    aspect: str
    aspect_abbr: str
    angle: float
    exact_angle: float
    orb: float


def normalize_longitude(value: float) -> float:
    return value % 360.0


def zodiac_from_longitude(longitude: float) -> tuple[str, float]:
    lon = normalize_longitude(longitude)
    sign_index = int(lon // 30)
    sign_degree = lon - sign_index * 30
    return ZODIAC_SIGNS[sign_index], sign_degree


def house_from_longitude(longitude: float, house_cusps: list[float]) -> int:
    lon = normalize_longitude(longitude)
    cusps = [normalize_longitude(c) for c in house_cusps]
    for i in range(12):
        start = cusps[i]
        end = cusps[(i + 1) % 12]
        if start <= end:
            in_house = start <= lon < end
        else:
            in_house = lon >= start or lon < end
        if in_house:
            return i + 1
    return 12


def parse_local_datetime(value: str, tz_name: str) -> datetime:
    naive_dt = datetime.strptime(value, "%Y-%m-%d %H:%M")
    return naive_dt.replace(tzinfo=ZoneInfo(tz_name))


def calculate_equation_of_time_minutes(local_dt: datetime) -> float:
    day_of_year = local_dt.timetuple().tm_yday
    hour_fraction = local_dt.hour + local_dt.minute / 60.0 + local_dt.second / 3600.0
    gamma = 2.0 * math.pi / 365.0 * (day_of_year - 1 + (hour_fraction - 12.0) / 24.0)
    return 229.18 * (
        0.000075
        + 0.001868 * math.cos(gamma)
        - 0.032077 * math.sin(gamma)
        - 0.014615 * math.cos(2.0 * gamma)
        - 0.040849 * math.sin(2.0 * gamma)
    )


def apply_true_solar_time(local_dt: datetime, longitude: float) -> tuple[datetime, float]:
    utc_offset = local_dt.utcoffset()
    if utc_offset is None:
        raise ValueError("Timezone offset is required to compute true solar time.")
    tz_offset_hours = utc_offset.total_seconds() / 3600.0
    eq_time = calculate_equation_of_time_minutes(local_dt)
    delta_minutes = eq_time + 4.0 * longitude - 60.0 * tz_offset_hours
    adjusted = local_dt + timedelta(minutes=delta_minutes)
    return adjusted, delta_minutes


def smallest_angular_distance(a: float, b: float) -> float:
    diff = abs(normalize_longitude(a) - normalize_longitude(b))
    return min(diff, 360.0 - diff)


def calculate_aspects(points: list[ChartPoint]) -> list[Aspect]:
    aspects: list[Aspect] = []
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            pa = points[i]
            pb = points[j]
            exact = smallest_angular_distance(pa.longitude, pb.longitude)
            for aspect_name, cfg in ASPECTS.items():
                orb = abs(exact - cfg["angle"])
                if orb <= cfg["orb"]:
                    aspects.append(
                        Aspect(
                            point_a=pa.name,
                            point_b=pb.name,
                            aspect=aspect_name,
                            aspect_abbr=cfg["abbr"],
                            angle=cfg["angle"],
                            exact_angle=exact,
                            orb=orb,
                        )
                    )
                    break
    return aspects


def to_serializable(result: dict) -> dict:
    serializable = dict(result)
    serializable["points"] = [
        {
            "name": p.name,
            "longitude": p.longitude,
            "sign": p.sign,
            "sign_degree": p.sign_degree,
            "house": p.house,
        }
        for p in result["points"]
    ]
    serializable["aspects"] = [
        {
            "point_a": a.point_a,
            "point_b": a.point_b,
            "aspect": a.aspect,
            "aspect_abbr": a.aspect_abbr,
            "angle": a.angle,
            "exact_angle": a.exact_angle,
            "orb": a.orb,
        }
        for a in result["aspects"]
    ]
    serializable["planets"] = serializable["points"]
    if "schema_version" not in serializable:
        serializable["schema_version"] = "mystilink.horoscope.natal/0.1"
    return serializable


def calculate_chart(
    local_dt: datetime,
    latitude: float,
    longitude: float,
    house_system: str = "P",
    zodiac_mode: str = "tropical",
    sidereal_mode: str = "lahiri",
    use_true_solar_time: bool = False,
    include_aspects: bool = True,
) -> dict:
    effective_local_dt = local_dt
    true_solar_delta_minutes = 0.0
    if use_true_solar_time:
        effective_local_dt, true_solar_delta_minutes = apply_true_solar_time(
            local_dt, longitude
        )

    utc_dt = effective_local_dt.astimezone(timezone.utc)
    jd_ut = swe.julday(
        utc_dt.year,
        utc_dt.month,
        utc_dt.day,
        utc_dt.hour + utc_dt.minute / 60.0 + utc_dt.second / 3600.0,
    )

    zodiac_mode = zodiac_mode.lower()
    sidereal_mode = sidereal_mode.lower()
    if zodiac_mode not in {"tropical", "sidereal"}:
        raise ValueError("zodiac_mode must be 'tropical' or 'sidereal'.")

    sidereal_ayanamsa = 0.0
    if zodiac_mode == "sidereal":
        if sidereal_mode not in SIDEREAL_MODES:
            available_modes = ", ".join(sorted(SIDEREAL_MODES.keys()))
            raise ValueError(
                f"Unsupported sidereal mode '{sidereal_mode}'. Available: {available_modes}"
            )
        swe.set_sid_mode(SIDEREAL_MODES[sidereal_mode], 0, 0)
        sidereal_ayanamsa = swe.get_ayanamsa_ut(jd_ut)

    house_system_code = house_system.upper().encode("ascii")
    houses_result = swe.houses_ex(jd_ut, latitude, longitude, house_system_code)
    house_cusps_tropical = list(houses_result[0][:12])
    ascmc = houses_result[1]
    asc_tropical = normalize_longitude(ascmc[0])
    mc_tropical = normalize_longitude(ascmc[1])

    if zodiac_mode == "sidereal":
        house_cusps = [
            normalize_longitude(cusp - sidereal_ayanamsa) for cusp in house_cusps_tropical
        ]
        asc = normalize_longitude(asc_tropical - sidereal_ayanamsa)
        mc = normalize_longitude(mc_tropical - sidereal_ayanamsa)
    else:
        house_cusps = house_cusps_tropical
        asc = asc_tropical
        mc = mc_tropical

    points: list[ChartPoint] = []
    skipped_points: list[str] = []
    flags = swe.FLG_SWIEPH | swe.FLG_SPEED
    if zodiac_mode == "sidereal":
        flags |= swe.FLG_SIDEREAL

    for name, body in PLANETS.items():
        try:
            position, _retflags = swe.calc_ut(jd_ut, body, flags)
        except swe.Error:
            # Fallback to Moshier if Swiss ephemeris files are unavailable.
            fallback_flags = (flags & ~swe.FLG_SWIEPH) | swe.FLG_MOSEPH
            try:
                position, _retflags = swe.calc_ut(jd_ut, body, fallback_flags)
            except swe.Error:
                skipped_points.append(name)
                continue
        ecl_lon = normalize_longitude(position[0])
        sign, sign_degree = zodiac_from_longitude(ecl_lon)
        house = house_from_longitude(ecl_lon, house_cusps)
        points.append(
            ChartPoint(
                name=name,
                longitude=ecl_lon,
                sign=sign,
                sign_degree=sign_degree,
                house=house,
            )
        )

    aspects = calculate_aspects(points) if include_aspects else []
    asc_sign, asc_degree = zodiac_from_longitude(asc)
    mc_sign, mc_degree = zodiac_from_longitude(mc)

    return {
        "schema_version": "mystilink.horoscope.natal/0.1",
        "local_datetime": local_dt.isoformat(),
        "effective_local_datetime": effective_local_dt.isoformat(),
        "utc_datetime": utc_dt.isoformat(),
        "julian_day_ut": jd_ut,
        "latitude": latitude,
        "longitude": longitude,
        "house_system": house_system.upper(),
        "zodiac_mode": zodiac_mode,
        "sidereal_mode": sidereal_mode if zodiac_mode == "sidereal" else None,
        "ayanamsa": sidereal_ayanamsa if zodiac_mode == "sidereal" else None,
        "true_solar_time_enabled": use_true_solar_time,
        "true_solar_time_delta_minutes": true_solar_delta_minutes,
        "asc": {"longitude": asc, "sign": asc_sign, "sign_degree": asc_degree},
        "mc": {"longitude": mc, "sign": mc_sign, "sign_degree": mc_degree},
        "house_cusps": house_cusps,
        "points": points,
        "aspects": aspects,
        "skipped_points": skipped_points,
    }


def print_chart(result: dict) -> None:
    print("=== Natal Chart ===")
    print(f"Local Time : {result['local_datetime']}")
    print(f"Effective  : {result['effective_local_datetime']}")
    print(f"UTC Time   : {result['utc_datetime']}")
    print(f"Julian Day : {result['julian_day_ut']:.6f}")
    print(f"Lat/Lon    : {result['latitude']}, {result['longitude']}")
    print(f"House Sys  : {result['house_system']}")
    print(f"Zodiac     : {result['zodiac_mode']}")
    if result["zodiac_mode"] == "sidereal":
        print(f"Sidereal   : {result['sidereal_mode']}")
        print(f"Ayanamsa   : {result['ayanamsa']:.6f}")
    print(f"True Solar : {result['true_solar_time_enabled']}")
    if result["true_solar_time_enabled"]:
        print(f"TST Delta  : {result['true_solar_time_delta_minutes']:.2f} minutes")
    print()

    asc = result["asc"]
    mc = result["mc"]
    print(
        f"ASC        : {asc['longitude']:.4f} ({asc['sign']} {asc['sign_degree']:.2f}°)"
    )
    print(f"MC         : {mc['longitude']:.4f} ({mc['sign']} {mc['sign_degree']:.2f}°)")
    print()

    print("House Cusps:")
    for i, cusp in enumerate(result["house_cusps"], start=1):
        sign, deg = zodiac_from_longitude(cusp)
        print(f"  H{i:02d}: {cusp:.4f} ({sign} {deg:.2f}°)")
    print()

    print("Planetary Positions:")
    print(f"{'Body':<10} {'Longitude':>10} {'Sign':>12} {'SignDeg':>10} {'House':>6}")
    for p in result["points"]:
        print(
            f"{p.name:<10} {p.longitude:>10.4f} {p.sign:>12} "
            f"{p.sign_degree:>10.2f} {p.house:>6}"
        )
    print()

    if result["aspects"]:
        print("Aspects:")
        print(
            f"{'Point A':<10} {'Point B':<10} {'Aspect':<12} {'Exact':>8} {'Orb':>8}"
        )
        for a in result["aspects"]:
            print(
                f"{a.point_a:<10} {a.point_b:<10} {a.aspect_abbr:<12} "
                f"{a.exact_angle:>8.2f} {a.orb:>8.2f}"
            )
    if result["skipped_points"]:
        print()
        print("Skipped Points (ephemeris unavailable):")
        for name in result["skipped_points"]:
            print(f"  - {name}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Calculate natal astrology chart using Swiss Ephemeris."
    )
    parser.add_argument(
        "--datetime",
        required=False,
        default=None,
        help='Local datetime in format "YYYY-MM-DD HH:MM"',
    )
    parser.add_argument(
        "--timezone",
        required=False,
        default=None,
        help='IANA timezone, e.g. "Asia/Shanghai"',
    )
    parser.add_argument("--lat", type=float, required=False, default=None, help="Latitude in degrees.")
    parser.add_argument(
        "--lon",
        type=float,
        required=False,
        default=None,
        help="Longitude in degrees (east positive, west negative).",
    )
    parser.add_argument(
        "--house-system",
        default="P",
        help="House system code (default: P for Placidus).",
    )
    parser.add_argument(
        "--zodiac",
        choices=["tropical", "sidereal"],
        default="tropical",
        help="Zodiac mode: tropical or sidereal (default: tropical).",
    )
    parser.add_argument(
        "--sidereal-mode",
        default="lahiri",
        choices=sorted(SIDEREAL_MODES.keys()),
        help="Sidereal ayanamsa mode when --zodiac sidereal (default: lahiri).",
    )
    parser.add_argument(
        "--true-solar-time",
        action="store_true",
        help="Apply true solar time correction to input local time.",
    )
    parser.add_argument(
        "--no-aspects",
        action="store_true",
        help="Disable major aspect calculation.",
    )
    parser.add_argument(
        "--birth-json",
        "--profile-json",
        dest="birth_json",
        default=None,
        help="BirthProfile (mystilink.birth/0.1) or legacy profile.json",
    )
    parser.add_argument(
        "--output",
        choices=["text", "json"],
        default="text",
        help="Output format (default: text).",
    )
    parser.add_argument(
        "--output-file",
        help="Optional output file path. If omitted, print to stdout.",
    )
    return parser


def _load_profile(raw: str) -> dict:
    from pathlib import Path
    import sys

    if raw == "-":
        text = sys.stdin.read()
    else:
        path = Path(raw)
        text = path.read_text(encoding="utf-8") if path.is_file() else raw
    data = json.loads(text)
    if not isinstance(data, dict):
        raise ValueError("profile JSON root must be an object")
    return data


def _resolve_birth(args: argparse.Namespace) -> tuple[str, str, float, float, bool]:
    datetime_str = args.datetime
    timezone_name = args.timezone
    lat = args.lat
    lon = args.lon
    true_solar = bool(args.true_solar_time)

    if args.birth_json:
        data = _load_profile(args.birth_json)
        if data.get("schema_version") == "mystilink.birth/0.1" or (
            isinstance(data.get("birth"), dict) and "datetime" in data["birth"]
        ):
            birth = data["birth"]
            timezone_name = timezone_name or birth["timezone"]
            dt_raw = str(birth["datetime"]).strip().replace("Z", "+00:00")
            instant = datetime.fromisoformat(dt_raw)
            if instant.tzinfo is None:
                raise ValueError("birth.datetime must include a timezone offset")
            datetime_str = (
                f"{instant.year:04d}-{instant.month:02d}-{instant.day:02d} "
                f"{instant.hour:02d}:{instant.minute:02d}"
            )
            if lon is None:
                lon = birth.get("longitude")
            place = data.get("place")
            if isinstance(place, dict):
                if lat is None:
                    lat = place.get("lat")
                if lon is None:
                    lon = place.get("lon")
            if birth.get("true_solar_time"):
                true_solar = True
        else:
            datetime_str = datetime_str or data.get("datetime")
            timezone_name = timezone_name or data.get("timezone")
            if lat is None:
                lat = data.get("lat")
            if lon is None:
                lon = data.get("lon")
            if data.get("true_solar_time"):
                true_solar = True

    if not datetime_str or not timezone_name:
        raise ValueError("datetime and timezone are required")
    if lat is None or lon is None:
        raise ValueError("lat and lon are required")
    return str(datetime_str), str(timezone_name), float(lat), float(lon), true_solar


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    try:
        datetime_str, timezone_name, lat, lon, true_solar = _resolve_birth(args)
        local_dt = parse_local_datetime(datetime_str, timezone_name)
    except ValueError as exc:
        raise SystemExit(f"Invalid input: {exc}") from exc
    except Exception as exc:
        raise SystemExit(f"Failed to resolve birth data: {exc}") from exc

    result = calculate_chart(
        local_dt,
        lat,
        lon,
        args.house_system,
        zodiac_mode=args.zodiac,
        sidereal_mode=args.sidereal_mode,
        use_true_solar_time=true_solar,
        include_aspects=not args.no_aspects,
    )

    if args.output == "json":
        payload = json.dumps(to_serializable(result), ensure_ascii=False, indent=2)
        if args.output_file:
            with open(args.output_file, "w", encoding="utf-8") as f:
                f.write(payload + "\n")
        else:
            print(payload)
    else:
        if args.output_file:
            raise SystemExit("--output-file is currently supported with --output json.")
        print_chart(result)


if __name__ == "__main__":
    main()
