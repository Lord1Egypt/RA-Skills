"""Convert structured decimal, DMS, or UTM coordinates to WGS84 lon/lat."""

import argparse
import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from utils import dms_to_decimal, validate_coordinates, write_json_stdout


def _utm_footpoint(northing, hemisphere):
    semi_major = 6378137.0
    eccentricity_squared = 0.00669438
    scale = 0.9996
    eccentricity_prime = eccentricity_squared / (1 - eccentricity_squared)
    e1 = (
        (1 - math.sqrt(1 - eccentricity_squared))
        / (1 + math.sqrt(1 - eccentricity_squared))
    )

    y = northing - (10000000.0 if hemisphere == "S" else 0.0)
    meridional_arc = y / scale
    mu = meridional_arc / (
        semi_major
        * (
            1
            - eccentricity_squared / 4
            - 3 * eccentricity_squared**2 / 64
            - 5 * eccentricity_squared**3 / 256
        )
    )

    phi1 = (
        mu
        + (3 * e1 / 2 - 27 * e1**3 / 32) * math.sin(2 * mu)
        + (21 * e1**2 / 16 - 55 * e1**4 / 32) * math.sin(4 * mu)
        + (151 * e1**3 / 96) * math.sin(6 * mu)
        + (1097 * e1**4 / 512) * math.sin(8 * mu)
    )
    return semi_major, eccentricity_squared, scale, eccentricity_prime, phi1


def _utm_project(easting, zone, constants):
    semi_major, eccentricity_squared, scale, eccentricity_prime, phi1 = constants
    x = easting - 500000.0
    sin_phi = math.sin(phi1)
    cos_phi = math.cos(phi1)
    tan_phi = math.tan(phi1)
    n1 = semi_major / math.sqrt(1 - eccentricity_squared * sin_phi**2)
    t1 = tan_phi**2
    c1 = eccentricity_prime * cos_phi**2
    r1 = (
        semi_major
        * (1 - eccentricity_squared)
        / (1 - eccentricity_squared * sin_phi**2) ** 1.5
    )
    d = x / (n1 * scale)

    latitude = phi1 - (n1 * tan_phi / r1) * (
        d**2 / 2
        - (5 + 3 * t1 + 10 * c1 - 4 * c1**2 - 9 * eccentricity_prime)
        * d**4
        / 24
        + (
            61
            + 90 * t1
            + 298 * c1
            + 45 * t1**2
            - 252 * eccentricity_prime
            - 3 * c1**2
        )
        * d**6
        / 720
    )
    longitude_delta = (
        d
        - (1 + 2 * t1 + c1) * d**3 / 6
        + (
            5
            - 2 * c1
            + 28 * t1
            - 3 * c1**2
            + 8 * eccentricity_prime
            + 24 * t1**2
        )
        * d**5
        / 120
    ) / cos_phi
    central_meridian = (zone - 1) * 6 - 180 + 3
    return [
        central_meridian + math.degrees(longitude_delta),
        math.degrees(latitude),
    ]


def utm_to_wgs84(easting, northing, zone, hemisphere):
    easting = float(easting)
    northing = float(northing)
    zone = int(zone)
    hemisphere = str(hemisphere).strip().upper()
    if not 1 <= zone <= 60:
        raise ValueError("UTM zone must be between 1 and 60")
    if hemisphere not in {"N", "S"}:
        raise ValueError("UTM hemisphere must be N or S")
    if not 100000 <= easting <= 1000000 or not 0 <= northing <= 10000000:
        raise ValueError("UTM easting or northing is outside the supported range")
    return _utm_project(
        easting,
        zone,
        _utm_footpoint(northing, hemisphere),
    )


def convert(data):
    coordinate_format = str(data.get("format", "decimal")).lower()
    coordinates = data.get("coordinates", [])
    result = []

    if coordinate_format == "decimal":
        order = str(data.get("order", "lonlat")).lower()
        if order not in {"lonlat", "latlon"}:
            raise ValueError("Decimal order must be lonlat or latlon")
        for first, second in coordinates:
            result.append(
                [float(first), float(second)]
                if order == "lonlat"
                else [float(second), float(first)]
            )
    elif coordinate_format == "dms":
        for first, second in coordinates:
            first_value = dms_to_decimal(first)
            second_value = dms_to_decimal(second)
            first_axis = str(first).strip()[-1:].upper()
            second_axis = str(second).strip()[-1:].upper()
            if first_axis in {"E", "W"} and second_axis in {"N", "S"}:
                result.append([first_value, second_value])
            elif first_axis in {"N", "S"} and second_axis in {"E", "W"}:
                result.append([second_value, first_value])
            else:
                raise ValueError("DMS pairs must include latitude and longitude hemispheres")
    elif coordinate_format == "utm":
        zone = data.get("zone")
        hemisphere = data.get("hemisphere")
        result = [
            utm_to_wgs84(easting, northing, zone, hemisphere)
            for easting, northing in coordinates
        ]
    else:
        raise ValueError("format must be decimal, dms, or utm")

    errors = validate_coordinates(result)
    if errors:
        raise ValueError("; ".join(errors))
    return {"vertices": result, "source_format": coordinate_format, "errors": []}


def main():
    parser = argparse.ArgumentParser(
        description="Convert JSON coordinates from stdin to WGS84 lon/lat"
    )
    parser.parse_args()
    try:
        write_json_stdout(convert(json.load(sys.stdin)))
    except (KeyError, TypeError, ValueError) as exc:
        write_json_stdout({"error": str(exc)})
        raise SystemExit(2)


if __name__ == "__main__":
    main()
