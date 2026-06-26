#!/usr/bin/env python3
"""
EXIF 信息提取脚本
从照片文件中提取拍摄参数元数据，供 photo-guide 技能调用。
"""

import json
import sys

try:
    from PIL import Image
    from PIL.ExifTags import TAGS, GPSTAGS
except ImportError:
    print(json.dumps({
        "has_exif": False,
        "error": "Pillow 未安装，请运行: pip install Pillow"
    }))
    sys.exit(0)


# 需要提取的关键 EXIF 标签
KEY_TAGS = {
    37386: "FocalLength",
    33437: "Aperture",
    33434: "ExposureTime",
    34855: "ISOSpeedRatings",
    37385: "Flash",
    36867: "DateTimeOriginal",
    271: "Make",
    272: "Model",
}


def _format_aperture(value):
    if isinstance(value, tuple) and len(value) == 2 and value[1] != 0:
        return f"f/{value[0] / value[1]:.1f}"
    return f"f/{value}"


def _format_exposure(value):
    if isinstance(value, tuple) and len(value) == 2:
        if value[0] == 0:
            return "0s"
        if value[1] > 0:
            fraction = value[1] / value[0]
            if fraction == int(fraction):
                return f"1/{int(fraction)}s"
            return f"{value[0]}/{value[1]}s"
    return f"{value}s"


def _format_focal(value):
    if isinstance(value, tuple) and len(value) == 2 and value[1] != 0:
        return f"{value[0] / value[1]:.1f}mm"
    return f"{value}mm"


FORMATTERS = {
    "Aperture": _format_aperture,
    "ExposureTime": _format_exposure,
    "FocalLength": _format_focal,
    "ISOSpeedRatings": lambda v: f"ISO {v}",
}


def extract_exif(image_path):
    """从图片文件提取 EXIF 元数据，返回 dict。"""
    try:
        img = Image.open(image_path)
        exif_data = img._getexif()

        if not exif_data:
            return {"has_exif": False}

        params = {}
        for tag_id, tag_name in KEY_TAGS.items():
            if tag_id in exif_data:
                value = exif_data[tag_id]
                formatter = FORMATTERS.get(tag_name)
                params[tag_name] = formatter(value) if formatter else str(value)

        result = {"has_exif": True, "params": params}

        # GPS 信息
        if 34853 in exif_data:
            gps_info = {}
            for key, val in exif_data[34853].items():
                gps_info[GPSTAGS.get(key, key)] = val
            result["gps"] = gps_info

        return result

    except Exception as e:
        return {"has_exif": False, "error": str(e)}


def main():
    if len(sys.argv) != 2:
        print("Usage: python extract_exif.py <image_path>")
        sys.exit(1)

    result = extract_exif(sys.argv[1])
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
