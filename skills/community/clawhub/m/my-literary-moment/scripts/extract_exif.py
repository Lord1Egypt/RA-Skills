import sys
import json
import os
import subprocess
import platform

try:
    from PIL import Image
    from PIL.ExifTags import TAGS, GPSTAGS
except Exception:
    Image = None
    TAGS = {}
    GPSTAGS = {}

_IS_MACOS: bool = platform.system() == "Darwin"
_heif_registered = False
_ensure_cache: dict | None = None


def ensure_pillow(auto_install: bool) -> dict:
    global Image, TAGS, GPSTAGS, _heif_registered, _ensure_cache

    if _ensure_cache is not None:
        return _ensure_cache

    def _try_register_heif(auto: bool) -> str | None:
        global _heif_registered
        if _heif_registered:
            return None
        try:
            from pillow_heif import register_heif_opener
            register_heif_opener()
            _heif_registered = True
            return None
        except ImportError:
            if not auto:
                return "pillow-heif not installed; HEIC/HEIF unsupported"
            try:
                subprocess.check_call(
                    [sys.executable, "-m", "pip", "install", "--quiet", "pillow-heif"]
                )
                from pillow_heif import register_heif_opener
                register_heif_opener()
                _heif_registered = True
                return None
            except Exception as e:
                return f"pillow-heif auto-install failed: {e}"

    if Image is not None:
        warn = _try_register_heif(auto_install)
        result: dict = {"ok": True}
        if warn:
            result["heic_warning"] = warn
        _ensure_cache = result
        return result

    if not auto_install:
        return {
            "ok": False,
            "error": "Pillow not installed",
            "hint": "Run: pip install -r requirements.txt",
        }

    try:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "--quiet",
             "pillow>=10.0.0", "pillow-heif"]
        )
        from PIL import Image as PILImage
        from PIL.ExifTags import TAGS as PILTAGS, GPSTAGS as PILGPSTAGS
        from pillow_heif import register_heif_opener

        Image = PILImage
        TAGS = PILTAGS
        GPSTAGS = PILGPSTAGS
        register_heif_opener()
        _heif_registered = True

        result = {"ok": True, "auto_installed": True}
        _ensure_cache = result
        return result

    except Exception as e:
        return {
            "ok": False,
            "error": "Auto install failed",
            "details": str(e),
            "hint": "Run: pip install -r requirements.txt",
        }


def ratio_to_float(v) -> float | None:
    try:
        if isinstance(v, tuple) and len(v) == 2 and v[1]:
            return float(v[0]) / float(v[1])
        if hasattr(v, "numerator") and hasattr(v, "denominator") and v.denominator:
            return float(v.numerator) / float(v.denominator)
        return float(v)
    except Exception:
        return None


def is_macos() -> bool:
    return _IS_MACOS


def extract_exif_macos(image_path: str) -> dict | None:
    if not _IS_MACOS:
        return None

    try:
        proc_result = subprocess.run(
            ["mdls", image_path],
            capture_output=True,
            text=True,
            timeout=10,
        )
        if proc_result.returncode != 0:
            return None

        metadata: dict = {}
        gps_data: dict = {}

        for line in proc_result.stdout.strip().split("\n"):
            if " = " not in line:
                continue
            key_raw, value_raw = line.split(" = ", 1)
            key = key_raw.replace("kMDItem", "").strip()
            value = value_raw.strip()

            if not value or value in ("(null)", '""'):
                continue

            if key in ("Latitude", "Longitude", "Altitude"):
                try:
                    gps_data[key] = float(value)
                except ValueError:
                    pass
            else:
                if value.startswith('"') and value.endswith('"'):
                    value = value[1:-1]
                metadata[key] = value

        if not metadata and not gps_data:
            return None

        output: dict = {}

        date_time = metadata.get("ContentCreationDate") or metadata.get("FSCreationDate")
        if date_time:
            output["DateTime"] = date_time
            output["DateTimeOriginal"] = date_time

        make = metadata.get("AcquisitionMake") or metadata.get("Make")
        if make:
            output["Make"] = make

        model = metadata.get("AcquisitionModel") or metadata.get("Model")
        if model:
            output["Model"] = model

        if metadata.get("Creator"):
            output["Software"] = metadata["Creator"]

        if "Latitude" in gps_data and "Longitude" in gps_data:
            output["GPSParsed"] = {
                "latitude": gps_data["Latitude"],
                "longitude": gps_data["Longitude"],
                "altitude_m": gps_data.get("Altitude"),
                "raw": None,
            }
            output["GPSInfo"] = gps_data

        for field in (
            "ISOSpeed", "FNumber", "FocalLength", "FocalLength35mm",
            "ExposureTimeSeconds", "FlashOnOff", "WhiteBalance",
            "ExposureMode", "ExposureProgram", "MeteringMode",
            "Aperture", "ImageDirection", "PixelWidth", "PixelHeight",
            "ColorSpace", "ProfileName", "PixelCount", "BitsPerSample",
            "ResolutionWidthDPI", "ResolutionHeightDPI", "ContentType",
            "Timestamp", "GPSDateStamp", "GPSDestBearing", "RedEyeOnOff",
            "HasAlphaChannel",
        ):
            if field in metadata:
                output[field] = metadata[field]

        if not output:
            return None

        output["_source"] = "mdls"
        return output

    except Exception:
        return None


def dms_to_decimal(dms, ref) -> float | None:
    try:
        d = ratio_to_float(dms[0])
        m = ratio_to_float(dms[1])
        s = ratio_to_float(dms[2])
        if d is None or m is None or s is None:
            return None
        value = d + (m / 60.0) + (s / 3600.0)
        if str(ref).upper() in ("S", "W"):
            value = -value
        return round(value, 6)
    except Exception:
        return None


def parse_gps(gps_info: dict) -> dict | None:
    if not gps_info:
        return None

    parsed = {GPSTAGS.get(k, str(k)): v for k, v in gps_info.items()}

    lat = dms_to_decimal(parsed.get("GPSLatitude"), parsed.get("GPSLatitudeRef"))
    lon = dms_to_decimal(parsed.get("GPSLongitude"), parsed.get("GPSLongitudeRef"))

    altitude = None
    alt = parsed.get("GPSAltitude")
    if alt is not None:
        v = ratio_to_float(alt)
        if v is not None:
            altitude = round(v, 1)

    location_text = {}
    for key in ("GPSAreaInformation", "GPSMapDatum", "GPSProcessingMethod"):
        val = parsed.get(key)
        if val is not None:
            if isinstance(val, bytes):
                val = val.decode(errors="ignore")
            location_text[key] = str(val)

    return {
        "latitude": lat,
        "longitude": lon,
        "altitude_m": altitude,
        "raw": location_text or None,
    }


def extract_exif(image_path: str, auto_install: bool = False) -> dict:
    if _IS_MACOS:
        macos_result = extract_exif_macos(image_path)
        if macos_result is not None:
            return macos_result

    ensure = ensure_pillow(auto_install=auto_install)
    if not ensure.get("ok"):
        return ensure

    try:
        with Image.open(image_path) as image:
            exifdata = image.getexif()

        exif_dict: dict = {}
        for tag_id in exifdata:
            tag = TAGS.get(tag_id, tag_id)
            data = exifdata.get(tag_id)
            if isinstance(data, bytes):
                try:
                    data = data.decode()
                except Exception:
                    data = str(data)
            exif_dict[tag] = data

        output: dict = {}

        for field in ("DateTime", "DateTimeOriginal", "Make", "Model", "Software",
                      "ImageDescription", "XPTitle", "XPComment", "UserComment"):
            if exif_dict.get(field):
                output[field] = exif_dict[field]

        gps_info = exif_dict.get("GPSInfo")
        if gps_info:
            output["GPSInfo"] = gps_info
            gps_parsed = parse_gps(gps_info)
            if gps_parsed:
                output["GPSParsed"] = gps_parsed

        output["_source"] = "pillow"

        if len(output) == 1:
            result = {"_source": "pillow", "error": "No EXIF data found"}
        else:
            result = output

        if ensure.get("auto_installed"):
            result["AutoInstall"] = "Pillow auto-installed successfully"
        if ensure.get("heic_warning"):
            result["heic_warning"] = ensure["heic_warning"]

        return result

    except Exception as e:
        return {"error": str(e)}


_SORT_TAIL = "\xff" * 20


def batch_extract(paths: list[str], auto_install: bool = False) -> dict:
    ensure_pillow(auto_install)

    results = []
    for p in paths:
        info = extract_exif(p, auto_install=auto_install)
        info["_path"] = p
        results.append(info)

    def sort_key(item: dict) -> str:
        return item.get("DateTimeOriginal") or item.get("DateTime") or _SORT_TAIL

    sorted_items = sorted(results, key=sort_key)
    sorted_paths = [item["_path"] for item in sorted_items]
    input_paths = [item["_path"] for item in results]

    note = None
    if input_paths != sorted_paths:
        note = (
            "检测到输入顺序与拍摄时间顺序不一致，已按拍摄时间重新排序。"
            "请留意：EXIF 时间可能有时区偏差或相机未校准，建议对照确认。"
        )

    output_items = [
        {k: v for k, v in item.items() if not k.startswith("_")}
        for item in sorted_items
    ]

    return {
        "images": output_items,
        "sorted_summary": {
            "images_count": len(paths),
            "shooting_sequence": sorted_paths,
            "note": note,
        },
    }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"error": "No image path provided"}))
        sys.exit(1)

    auto_install_flag = os.getenv("MY_PROSE_POEM_AUTO_INSTALL", "0") == "1"
    clean_args = []

    for arg in sys.argv[1:]:
        if arg == "--auto-install":
            auto_install_flag = True
        else:
            clean_args.append(arg)

    if not clean_args:
        print(json.dumps({"error": "No image path provided"}))
        sys.exit(1)

    result = batch_extract(clean_args, auto_install=auto_install_flag)
    print(json.dumps(result, indent=2, ensure_ascii=False))
