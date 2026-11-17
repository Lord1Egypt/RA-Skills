#!/usr/bin/env python3
"""移动端权限清单校验 —— 提取并校验 AndroidManifest.xml 与 iOS Info.plist 的权限声明。

纯标准库（xml.etree / plistlib / json / argparse），不联网、不修改被检文件，
产出确定可复现。配合 assets/permissions-spec.json（含 _ 注释键，脚本自动跳过）。

检测项：
  E1  Android 组件(activity/service/receiver)在 targetSdk>=31 时缺 android:exported
  E2  Android 权限命中 spec.deny_android_permissions（显式禁止清单）
  E3  iOS 的 NS*UsageDescription 值为空 / 占位符(TODO/xxx/TBD)
  E4  iOS 缺 spec.ios_required_usage_descriptions 中声明的必需用途描述
  W1  Android 危险权限被使用（仅告警，需人工确认是否必要）
  W2  iOS 用途描述过短（<10 字符，可能审核被打回）

用法:
  python3 scripts/check_permissions.py --android AndroidManifest.xml
  python3 scripts/check_permissions.py --ios Info.plist
  python3 scripts/check_permissions.py --android AndroidManifest.xml --ios Info.plist \
      --spec assets/permissions-spec.json
  python3 scripts/check_permissions.py --android AndroidManifest.xml --json
"""
from __future__ import annotations

import argparse
import json
import plistlib
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

ANDROID_NS = "{http://schemas.android.com/apk/res/android}"
COMPONENT_TAGS = {"activity", "activity-alias", "service", "receiver", "provider"}
EXPORTED_REQUIRED_SDK = 31  # Android 12+ 要求显式 exported

# 内置危险权限基线（可被 spec.dangerous_android_permissions 覆盖/追加）
BUILTIN_DANGEROUS = {
    "android.permission.READ_CALENDAR",
    "android.permission.WRITE_CALENDAR",
    "android.permission.CAMERA",
    "android.permission.READ_CONTACTS",
    "android.permission.WRITE_CONTACTS",
    "android.permission.GET_ACCOUNTS",
    "android.permission.ACCESS_FINE_LOCATION",
    "android.permission.ACCESS_COARSE_LOCATION",
    "android.permission.RECORD_AUDIO",
    "android.permission.READ_PHONE_STATE",
    "android.permission.READ_PHONE_NUMBERS",
    "android.permission.CALL_PHONE",
    "android.permission.READ_CALL_LOG",
    "android.permission.WRITE_CALL_LOG",
    "android.permission.ADD_VOICEMAIL",
    "android.permission.USE_SIP",
    "android.permission.PROCESS_OUTGOING_CALLS",
    "android.permission.BODY_SENSORS",
    "android.permission.SEND_SMS",
    "android.permission.RECEIVE_SMS",
    "android.permission.READ_SMS",
    "android.permission.RECEIVE_WAP_PUSH",
    "android.permission.RECEIVE_MMS",
    "android.permission.READ_EXTERNAL_STORAGE",
    "android.permission.WRITE_EXTERNAL_STORAGE",
    "android.permission.READ_MEDIA_IMAGES",
    "android.permission.READ_MEDIA_VIDEO",
    "android.permission.READ_MEDIA_AUDIO",
}

# 内置 iOS 常用用途描述键（可被 spec.ios_required_usage_descriptions 覆盖/追加）
BUILTIN_IOS_REQUIRED = {
    "NSCameraUsageDescription",
    "NSPhotoLibraryUsageDescription",
    "NSLocationWhenInUseUsageDescription",
    "NSMicrophoneUsageDescription",
    "NSContactsUsageDescription",
}

PLACEHOLDER = {"", "todo", "tbd", "xxx", "xxx.", "placeholder", "待补充", "暂无"}


def load_spec(path: str | None) -> dict:
    """读取规范 JSON；以 _ 开头的键是注释，跳过（模板可用性约定）。"""
    if not path:
        return {}
    with open(path, encoding="utf-8") as fh:
        data = json.load(fh)
    return {k: v for k, v in data.items() if not str(k).startswith("_")}


def local(tag: str) -> str:
    return tag.split("}", 1)[-1]


def attr(el, name: str):
    return el.attrib.get(ANDROID_NS + name) or el.attrib.get(name)


def check_android(manifest: Path, spec: dict):
    findings = []
    try:
        tree = ET.parse(manifest)
    except ET.ParseError as e:
        return [{"severity": "error", "check": "XML 解析", "detail": f"无法解析 {manifest}: {e}"}]
    root = tree.getroot()

    # targetSdk 决定 exported 是否必填
    target_sdk = None
    for el in root.iter():
        if local(el.tag) == "uses-sdk":
            v = attr(el, "targetSdkVersion") or attr(el, "minSdkVersion")
            if v and v.isdigit():
                target_sdk = int(v)
    exported_required = target_sdk is not None and target_sdk >= EXPORTED_REQUIRED_SDK

    dangerous = BUILTIN_DANGEROUS | set(spec.get("dangerous_android_permissions", []) or [])
    denied = set(spec.get("deny_android_permissions", []) or [])

    used_perms = []
    for el in root.iter():
        if local(el.tag) == "uses-permission":
            name = attr(el, "name")
            if name:
                used_perms.append(name)

    # E1: 组件缺 exported（targetSdk>=31 必须显式声明）
    if exported_required:
        for el in root.iter():
            if local(el.tag) in COMPONENT_TAGS:
                if attr(el, "exported") is None:
                    findings.append({
                        "severity": "error", "check": "Android exported",
                        "detail": f"<{local(el.tag)}> 缺 android:exported（targetSdk={target_sdk}≥{EXPORTED_REQUIRED_SDK} 必须显式声明）",
                    })

    # E2: 命中禁止权限
    for p in used_perms:
        if p in denied:
            findings.append({
                "severity": "error", "check": "Android 禁止权限",
                "detail": f"权限 {p} 在 deny 清单中，不应申请",
            })
        # W1: 危险权限
        if p in dangerous:
            findings.append({
                "severity": "warn", "check": "Android 危险权限",
                "detail": f"危险权限 {p} 被使用，确认是否必要并在商店说明",
            })

    if not used_perms:
        findings.append({"severity": "warn", "check": "Android 权限", "detail": "未发现任何 uses-permission"})
    return findings


def check_ios(plist: Path, spec: dict):
    findings = []
    try:
        with open(plist, "rb") as fh:
            data = plistlib.load(fh)
    except Exception as e:  # 二进制/XML 解析失败
        return [{"severity": "error", "check": "plist 解析", "detail": f"无法解析 {plist}: {e}"}]
    if not isinstance(data, dict):
        return [{"severity": "error", "check": "plist 结构", "detail": f"{plist} 根不是字典"}]

    required = BUILTIN_IOS_REQUIRED | set(spec.get("ios_required_usage_descriptions", []) or [])
    usage_keys = {k: v for k, v in data.items() if k.endswith("UsageDescription")}

    # E3: 用途描述为空/占位
    for k, v in usage_keys.items():
        val = (v or "").strip().lower() if isinstance(v, str) else ""
        if val in PLACEHOLDER or val == "":
            findings.append({
                "severity": "error", "check": "iOS 用途描述",
                "detail": f"{k} 值为空或占位符，审核必拒",
            })
        elif len((v or "").strip()) < 10:
            findings.append({
                "severity": "warn", "check": "iOS 用途描述",
                "detail": f"{k} 过短（<10 字符），易被审核打回",
            })

    # E4: 缺必需用途描述
    for k in required:
        if k not in usage_keys:
            findings.append({
                "severity": "error", "check": "iOS 必需用途描述缺失",
                "detail": f"规范要求的 {k} 未在 plist 中声明（应用用到该能力却未说明）",
            })
    return findings


def main() -> int:
    ap = argparse.ArgumentParser(
        description="校验 AndroidManifest.xml / Info.plist 权限声明（纯标准库）")
    ap.add_argument("--android", help="AndroidManifest.xml 路径")
    ap.add_argument("--ios", help="Info.plist 路径")
    ap.add_argument("--spec", help="权限规范 JSON（含 _ 注释键，自动跳过）")
    ap.add_argument("--json", action="store_true", help="输出 JSON")
    args = ap.parse_args()

    if not args.android and not args.ios:
        ap.error("至少需要 --android 或 --ios 之一")

    spec = load_spec(args.spec)
    findings = []
    if args.android:
        findings += check_android(Path(args.android), spec)
    if args.ios:
        findings += check_ios(Path(args.ios), spec)

    errors = [f for f in findings if f["severity"] == "error"]
    warns = [f for f in findings if f["severity"] == "warn"]

    if args.json:
        print(json.dumps({"errors": len(errors), "warnings": len(warns),
                          "findings": findings}, ensure_ascii=False, indent=2))
    else:
        for f in findings:
            mark = "✗" if f["severity"] == "error" else "!"
            print(f"  [{mark}] {f['check']}: {f['detail']}")
        print(f"\n结果：{len(errors)} error, {len(warns)} warning")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
