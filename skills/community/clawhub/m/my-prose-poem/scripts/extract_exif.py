import sys
import json
import os
import subprocess

try:
    from PIL import Image
    from PIL.ExifTags import TAGS, GPSTAGS
except Exception:
    Image = None
    TAGS = {}
    GPSTAGS = {}


def ensure_pillow(auto_install):
    global Image, TAGS, GPSTAGS
    if Image is not None:
        return {"ok": True}
    if not auto_install:
        return {
            "ok": False,
            "error": "Pillow not installed",
            "hint": "Run: pip install -r requirements.txt"
        }
    try:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "--quiet", "pillow>=10.0.0"]
        )
        from PIL import Image as PILImage
        from PIL.ExifTags import TAGS as PILTAGS, GPSTAGS as PILGPSTAGS
        Image = PILImage
        TAGS = PILTAGS
        GPSTAGS = PILGPSTAGS
        return {"ok": True, "auto_installed": True}
    except Exception as e:
        return {
            "ok": False,
            "error": "Auto install failed",
            "details": str(e),
            "hint": "Run: pip install -r requirements.txt"
        }


def ratio_to_float(v):
    if isinstance(v, tuple) and len(v) == 2 and v[1]:
        return float(v[0]) / float(v[1])
    if hasattr(v, "numerator") and hasattr(v, "denominator") and v.denominator:
        return float(v.numerator) / float(v.denominator)
    return float(v)


def dms_to_decimal(dms, ref):
    try:
        d = ratio_to_float(dms[0])
        m = ratio_to_float(dms[1])
        s = ratio_to_float(dms[2])
        value = d + (m / 60.0) + (s / 3600.0)
        if str(ref).upper() in ["S", "W"]:
            value = -value
        return round(value, 6)
    except Exception:
        return None


def parse_gps(gps_info):
    if not gps_info:
        return None
    parsed = {}
    for k, v in gps_info.items():
        parsed[GPSTAGS.get(k, str(k))] = v
    lat = dms_to_decimal(parsed.get("GPSLatitude"), parsed.get("GPSLatitudeRef"))
    lon = dms_to_decimal(parsed.get("GPSLongitude"), parsed.get("GPSLongitudeRef"))
    alt = parsed.get("GPSAltitude")
    altitude = None
    if alt is not None:
        try:
            altitude = round(ratio_to_float(alt), 1)
        except Exception:
            altitude = None
    location_text = {}
    for key in ["GPSAreaInformation", "GPSMapDatum", "GPSProcessingMethod"]:
        if parsed.get(key) is not None:
            value = parsed.get(key)
            if isinstance(value, bytes):
                try:
                    value = value.decode(errors="ignore")
                except Exception:
                    value = str(value)
            location_text[key] = str(value)
    result = {
        "latitude": lat,
        "longitude": lon,
        "altitude_m": altitude,
        "raw": location_text if location_text else None
    }
    return result


def extract_exif(image_path, auto_install=False):
    ensure = ensure_pillow(auto_install=auto_install)
    if not ensure.get("ok"):
        return ensure
    try:
        image = Image.open(image_path)
        exifdata = image.getexif()

        exif_dict = {}
        for tag_id in exifdata:
            tag = TAGS.get(tag_id, tag_id)
            data = exifdata.get(tag_id)

            if isinstance(data, bytes):
                try:
                    data = data.decode()
                except Exception:
                    data = str(data)

            exif_dict[tag] = data

        gps_parsed = parse_gps(exif_dict.get("GPSInfo"))
        text_candidates = {
            "ImageDescription": exif_dict.get("ImageDescription"),
            "XPTitle": exif_dict.get("XPTitle"),
            "XPComment": exif_dict.get("XPComment"),
            "UserComment": exif_dict.get("UserComment")
        }
        result = {
            "DateTime": exif_dict.get("DateTime"),
            "DateTimeOriginal": exif_dict.get("DateTimeOriginal"),
            "Make": exif_dict.get("Make"),
            "Model": exif_dict.get("Model"),
            "Software": exif_dict.get("Software"),
            "GPSInfo": exif_dict.get("GPSInfo"),
            "GPSParsed": gps_parsed,
            "LocationTextCandidates": text_candidates,
            "AddressInExif": "EXIF 通常不包含可直接使用的完整地址，常见的是经纬度或无地址信息。"
        }
        if ensure.get("auto_installed"):
            result["AutoInstall"] = "Pillow auto-installed successfully"

        return result
    except Exception as e:
        return {"error": str(e)}


def batch_extract(paths, auto_install=False):
    results = []
    for p in paths:
        info = extract_exif(p, auto_install=auto_install)
        info["_path"] = p
        results.append(info)

    sortable = []
    for item in results:
        dt = item.get("DateTimeOriginal") or item.get("DateTime")
        sortable.append((dt or "", item))

    sorted_items = [item for _, item in sorted(sortable, key=lambda x: x[0])]

    sorted_paths = [item["_path"] for item in sorted_items]
    input_paths = [item["_path"] for item in results]

    sorted_summary = {
        "images_count": len(paths),
        "shooting_sequence": sorted_paths,
        "note": None
    }
    if input_paths != sorted_paths and sorted_paths:
        sorted_summary["note"] = (
            "检测到输入顺序与拍摄时间顺序不一致，已按拍摄时间重新排序。"
            "请留意：EXIF 时间可能有时区偏差或相机未校准，建议对照确认。"
        )

    output_items = []
    for item in sorted_items:
        cleaned = {k: v for k, v in item.items() if not k.startswith("_")}
        output_items.append(cleaned)

    return {"images": output_items, "sorted_summary": sorted_summary}


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

    paths = clean_args
    if len(paths) == 0:
        print(json.dumps({"error": "No image path provided"}))
        sys.exit(1)

    result = batch_extract(paths, auto_install=auto_install_flag)
    print(json.dumps(result, indent=2, ensure_ascii=False))
