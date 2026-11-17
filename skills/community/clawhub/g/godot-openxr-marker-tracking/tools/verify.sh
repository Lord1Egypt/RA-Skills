#!/usr/bin/env bash
# ---------------------------------------------------------------------------
# verify.sh —— Godot OpenXR 标记追踪：一键验证
#
# 把 SKILL.md「七、验证清单」里的三件事串起来跑：
#   1. API 回归：把「三、API 纠错对照表」逐条断言（正确名字必须存在、
#      文档里的错误写法必须不存在）。Godot 改 API 时第一时间暴露。
#   2. 编译校验：扫项目里所有 .gd，用 load() + can_instantiate() 分类。
#      在 --xr-mode off 下调用 OpenXR 单例的脚本必然落到 can_instantiate()
#      == false，这类归为 NEED_XR（环境限制），不算失败。
#   3. Python 自测：验证 tilt_deg() 的倾斜角算法（用 projectPoints 正向造
#      精确倾斜的像点，solvePnP 反解比对），以及 cv2.imwrite 在非 ASCII
#      路径下静默失败的问题。
#
# 用法
#   bash tools/verify.sh --project /d/my/godot/project
#   bash tools/verify.sh                  # 在当前目录找 project.godot
#   bash tools/verify.sh --skip-godot     # 只跑 Python 自测
#
# 退出码
#   0  全部通过（跳过项不算失败）
#   1  有失败项
#   2  一项都没跑成（缺 Godot 也缺 Python）
# ---------------------------------------------------------------------------
set -uo pipefail

PROJ=""
GODOT_BIN="${GODOT:-}"
PYTHON_BIN="${PYTHON:-}"
RUN_GODOT=1
RUN_PY=1
VERBOSE=0
TIMEOUT_SEC=300

usage() {
    sed -n '3,23p' "$0" | sed 's/^# \{0,1\}//'
    exit 0
}

while [ $# -gt 0 ]; do
    case "$1" in
        --project)    PROJ="${2:-}"; shift 2 ;;
        --godot)      GODOT_BIN="${2:-}"; shift 2 ;;
        --python)     PYTHON_BIN="${2:-}"; shift 2 ;;
        --skip-godot) RUN_GODOT=0; shift ;;
        --skip-python) RUN_PY=0; shift ;;
        --timeout)    TIMEOUT_SEC="${2:-300}"; shift 2 ;;
        -v|--verbose) VERBOSE=1; shift ;;
        -h|--help)    usage ;;
        *) echo "未知参数：$1（用 --help 看用法）" >&2; exit 2 ;;
    esac
done

# ---------- 输出 ----------
if [ -t 1 ]; then
    C_R=$'\033[31m'; C_G=$'\033[32m'; C_Y=$'\033[33m'; C_B=$'\033[36m'; C_0=$'\033[0m'
else
    C_R=""; C_G=""; C_Y=""; C_B=""; C_0=""
fi
PASS_N=0; FAIL_N=0; SKIP_N=0
pass() { PASS_N=$((PASS_N+1)); printf '  %sPASS%s  %s\n' "$C_G" "$C_0" "$1"; }
fail() { FAIL_N=$((FAIL_N+1)); printf '  %sFAIL%s  %s\n' "$C_R" "$C_0" "$1"; [ -n "${2:-}" ] && printf '        %s\n' "$2"; }
skip() { SKIP_N=$((SKIP_N+1)); printf '  %sSKIP%s  %s\n' "$C_Y" "$C_0" "$1"; }
head1() { printf '\n%s── %s %s\n' "$C_B" "$1" "$C_0"; }

TMPD="$(mktemp -d 2>/dev/null || echo "/tmp/verify.$$")"
# Git Bash 下 mktemp 会返回 "C:\Users\...\Temp/tmp.x" 这种盘符与正斜杠混写的路径，
# 少数环境的 rm 包装器（如 safe-delete）会直接拒绝。统一转成 POSIX 形式再删。
_posix() {
    if command -v cygpath >/dev/null 2>&1; then
        cygpath -u "$1" 2>/dev/null || printf '%s' "$1"
    else
        printf '%s' "$1"
    fi
}
TMPD="$(_posix "$TMPD")"
mkdir -p "$TMPD"
cleanup() {
    [ -n "${TMPD:-}" ] && rm -rf "$TMPD" >/dev/null 2>&1
    if [ -n "${PROBE_GD:-}" ] && [ -f "${PROBE_GD:-}" ]; then
        rm -f "$(_posix "$PROBE_GD")" >/dev/null 2>&1
        if [ -f "$PROBE_GD" ]; then
            printf '  注意：临时探针脚本没能自动删除，请手动移除 %s\n' "$PROBE_GD" >&2
        fi
    fi
    return 0
}
trap cleanup EXIT

# ---------- 环境探测 ----------
if [ -z "$PROJ" ]; then PROJ="$PWD"; fi
PROJ="${PROJ%/}"
PROJ_MARK="$PROJ/project.godot"

if [ -z "$GODOT_BIN" ]; then
    for cand in "$(command -v godot 2>/dev/null)" \
                "$(command -v godot4 2>/dev/null)" \
                "$(command -v Godot 2>/dev/null)"; do
        if [ -n "$cand" ] && [ -x "$cand" ]; then GODOT_BIN="$cand"; break; fi
    done
fi

if [ -z "$PYTHON_BIN" ]; then
    for cand in "$HOME/.workbuddy/binaries/python/envs/default/Scripts/python.exe" \
                "$(command -v python3 2>/dev/null)" \
                "$(command -v python 2>/dev/null)"; do
        if [ -n "$cand" ] && [ -x "$cand" ]; then
            if "$cand" -c "import cv2" >/dev/null 2>&1; then PYTHON_BIN="$cand"; break; fi
        fi
    done
    # 没有 cv2 的 python 也留作兜底，后面会 SKIP
    if [ -z "$PYTHON_BIN" ]; then
        for cand in "$(command -v python3 2>/dev/null)" "$(command -v python 2>/dev/null)"; do
            if [ -n "$cand" ] && [ -x "$cand" ]; then PYTHON_BIN="$cand"; break; fi
        done
    fi
fi

printf '%sGodot OpenXR 标记追踪 · 验证%s\n' "$C_B" "$C_0"
printf '  项目     : %s\n' "$PROJ"
printf '  Godot    : %s\n' "${GODOT_BIN:-<未找到>}"
printf '  Python   : %s\n' "${PYTHON_BIN:-<未找到>}"

# ===========================================================================
# 1. API 回归
# ===========================================================================
if [ "$RUN_GODOT" -eq 1 ]; then
    head1 "1/2 API 回归（对照表逐条断言）"

    if [ -z "$GODOT_BIN" ]; then
        skip "未找到 Godot 可执行文件（用 --godot 指定，或设 \$GODOT）"
    elif [ ! -f "$PROJ_MARK" ]; then
        skip "项目里没有 project.godot：$PROJ（用 --project 指定）"
    else
        PROBE_GD="$PROJ/verify_probe.gd"
        cat > "$PROBE_GD" <<'GDEOF'
extends SceneTree

# [类, 成员, 类型, 期望存在]
const CASES := [
    # 文档/直觉写法 vs 实际 API：正确的必须存在，错误的必须不存在
    ["OpenXRSpatialEntityExtension", "is_aruco_supported",       "method", true],
    ["OpenXRSpatialEntityExtension", "aruco_is_supported",       "method", false],
    ["OpenXRSpatialEntityExtension", "discover_spatial_entities","method", true],
    ["OpenXRSpatialEntityExtension", "start_entity_discovery",   "method", false],
    ["OpenXRSpatialEntityExtension", "free_spatial_snapshot",    "method", true],
    ["OpenXRSpatialEntityExtension", "cancel_discovery",         "method", false],
    ["OpenXRSpatialEntityExtension", "query_snapshot",           "method", true],
    ["OpenXRSpatialEntityExtension", "free_spatial_context",     "method", true],
    ["OpenXRSpatialEntityExtension", "COMPONENT_TYPE_MARKER",    "const",  true],
    ["OpenXRFutureResult", "get_result_value", "method", true],
    ["OpenXRFutureResult", "get_result",       "method", false],
    ["OpenXRFutureResult", "RESULT_FINISHED",  "const",  true],
    ["OpenXRFutureResult", "RESULT_SUCCESS",   "const",  false],
    ["OpenXRSpatialComponentBounded2DList", "get_center_pose", "method", true],
    ["OpenXRSpatialComponentBounded2DList", "get_size",        "method", true],
    ["OpenXRSpatialComponentBounded2DList", "get_bounded_2d",  "method", false],
    ["OpenXRSpatialComponentMarkerList", "MARKER_TYPE_ARUCO",  "const",  true],
    ["OpenXRSpatialComponentMarkerList", "get_marker_id",      "method", true],
    ["OpenXRSpatialQueryResultData", "get_capacity",           "method", true],
    ["XRServer", "add_tracker",    "method", true],
    ["XRServer", "remove_tracker", "method", true],
    ["OpenXRSpatialSnapshotResult", "", "class", false],
]

func _has_prop(cls: String, prop: String) -> bool:
    # second arg = no_inheritance；必须传 false 否则漏掉父类字段
    for p in ClassDB.class_get_property_list(cls, false):
        if String(p.get("name", "")) == prop:
            return true
    return false

func _check(cls: String, member: String, kind: String) -> Variant:
    if not ClassDB.class_exists(cls):
        return null                      # 本构建里没这个类，无法判定
    match kind:
        "method": return ClassDB.class_has_method(cls, member)
        "const":  return ClassDB.class_has_integer_constant(cls, member)
        "prop":   return _has_prop(cls, member)
        "class":  return true
    return null

func _scan_gd(dir_path: String, acc: Array) -> void:
    var d := DirAccess.open(dir_path)
    if d == null:
        return
    d.list_dir_begin()
    var f := d.get_next()
    while f != "":
        if f.begins_with("."):
            f = d.get_next()
            continue
        var p := dir_path.path_join(f)
        if d.current_is_dir():
            _scan_gd(p, acc)
        elif f.ends_with(".gd"):
            acc.append(p)
        f = d.get_next()
    d.list_dir_end()

func _initialize() -> void:
    # ---- API 回归 ----
    for c in CASES:
        var cls: String = c[0]
        var member: String = c[1]
        var kind: String = c[2]
        var expect: bool = c[3]
        if kind == "class":
            var exists := ClassDB.class_exists(cls)
            if exists != expect:
                print("VERIFY|API|FAIL|%s|class %s, expected %s" % [cls, "exists" if exists else "absent", "exists" if expect else "absent"])
            else:
                print("VERIFY|API|PASS|class %s %s" % [cls, "absent" if expect == false else "exists"])
            continue
        var got = _check(cls, member, kind)
        if got == null:
            print("VERIFY|API|SKIP|%s.%s|class not in this build" % [cls, member])
        elif bool(got) == expect:
            print("VERIFY|API|PASS|%s.%s %s" % [cls, member, "exists" if expect else "absent"])
        else:
            print("VERIFY|API|FAIL|%s.%s|expected %s, got %s" % [cls, member, "exist" if expect else "absent", "exists" if got else "absent"])

    # ---- 属性类断言（含继承）----
    for pair in [["OpenXRMarkerTracker", "name", true],
                 ["OpenXRMarkerTracker", "tracker_name", false],
                 ["OpenXRMarkerTracker", "register_with_xr_server", false],
                 ["OpenXRMarkerTracker", "bounds_size", true]]:
        var cls: String = pair[0]
        var prop: String = pair[1]
        var expect: bool = pair[2]
        if not ClassDB.class_exists(cls):
            print("VERIFY|API|SKIP|%s.%s|class not in this build" % [cls, prop])
            continue
        var has := _has_prop(cls, prop)
        if has == expect:
            print("VERIFY|API|PASS|%s.%s %s" % [cls, prop, "exists" if expect else "absent"])
        else:
            print("VERIFY|API|FAIL|%s.%s|expected %s, got %s" % [cls, prop, "exist" if expect else "absent", "exists" if has else "absent"])

    # ---- 编译校验 ----
    var files: Array = []
    _scan_gd("res://", files)
    for p in files:
        if p.get_file() == "verify_probe.gd":
            continue
        var res_path := p
        var s = load(res_path)
        if s == null:
            print("VERIFY|BUILD|FAIL|%s|cannot load (硬失败，源码读不出)" % res_path)
            continue
        if s.can_instantiate():
            print("VERIFY|BUILD|PASS|%s" % res_path)
            continue
        # can_instantiate false：要么真有解析错误，要么是 --xr-mode off 下
        # 调用 OpenXR 单例导致的必然结果，按源码是否涉及 OpenXR 分流
        var txt := FileAccess.get_file_as_string(res_path)
        if txt.find("OpenXR") != -1:
            print("VERIFY|BUILD|NEED_XR|%s|含 OpenXR 单例调用，需在启用 XR 的环境复核" % res_path)
        else:
            print("VERIFY|BUILD|FAIL|%s|can_instantiate() == false（疑似解析错误）" % res_path)

    print("VERIFY|DONE|1")
    quit(0)
GDEOF

        LOG="$TMPD/godot.log"
        RUNNER=""
        if command -v timeout >/dev/null 2>&1; then RUNNER="timeout $TIMEOUT_SEC"; fi

        # 关键：必须带 --xr-mode off，否则无 XR 运行时会在初始化无限阻塞
        $RUNNER "$GODOT_BIN" --headless --xr-mode off --path "$PROJ" \
            --script "res://verify_probe.gd" > "$LOG" 2>&1
        RC=$?

        if grep -q '^VERIFY|DONE' "$LOG"; then
            while IFS='|' read -r _lvl section verdict detail extra; do
                case "$section:$verdict" in
                    API:PASS)   pass "${detail:-$extra}" ;;
                    API:FAIL)   fail "${detail:-$extra}" "${extra:-}" ;;
                    API:SKIP)   skip "${detail:-$extra}" ;;
                    BUILD:PASS) pass "编译 $detail" ;;
                    BUILD:FAIL) fail "编译 $detail" "$extra" ;;
                    BUILD:NEED_XR) skip "需 XR 环境：$detail" ;;
                esac
            done < <(grep '^VERIFY|' "$LOG")
        else
            fail "Godot 验证脚本没能跑完（退出码 $RC）" \
                 "常见原因：未加 --xr-mode off 导致阻塞；或 project.godot 首次导入尚未完成。日志尾部：$(tail -3 "$LOG" 2>/dev/null | tr '\n' ' ')"
            [ "$VERBOSE" -eq 1 ] && cat "$LOG"
        fi
    fi
else
    head1 "1/2 API 回归"
    skip "已按 --skip-godot 关闭"
fi

# ===========================================================================
# 2. Python 自测
# ===========================================================================
if [ "$RUN_PY" -eq 1 ]; then
    head1 "2/2 Python 自测（倾斜角算法 + 非 ASCII 路径写图）"

    if [ -z "$PYTHON_BIN" ]; then
        skip "未找到 Python"
    elif ! "$PYTHON_BIN" -c "import cv2, numpy" >/dev/null 2>&1; then
        skip "当前 Python 缺 opencv / numpy：$PYTHON_BIN"
    else
        PY_TEST="$TMPD/test_pose.py"
        cat > "$PY_TEST" <<'PYEOF'
# -*- coding: utf-8 -*-
"""验证 SKILL.md 第六节的两条结论。失败即说明实现退化。"""
import math
import sys
import tempfile
from pathlib import Path

import numpy as np
import cv2

MARK = 0.042                      # 标记边长 42mm
HALF = MARK / 2.0
OBJ = np.array([[-HALF, -HALF, 0.0], [HALF, -HALF, 0.0],
                [HALF, HALF, 0.0], [-HALF, HALF, 0.0]], dtype=np.float64)
K = np.array([[800.0, 0, 320.0], [0, 800.0, 240.0], [0, 0, 1.0]])
DIST = np.zeros((5, 1))


def tilt_deg(rvec, tvec):
    """0° = 正对镜头，90° = 完全侧对。"""
    R, _ = cv2.Rodrigues(np.asarray(rvec).reshape(3, 1))
    normal = R[:, 2].ravel()
    t = np.asarray(tvec).ravel()
    n = float(np.linalg.norm(t))
    if n < 1e-9:
        return 0.0
    los = -t / n
    cos_a = abs(float(np.dot(normal, los)))
    return math.degrees(math.acos(max(0.0, min(1.0, cos_a))))


def naive_angle(rvec):
    """错误做法：直接把旋转向量的模长当倾斜角。"""
    return float(np.linalg.norm(rvec)) * 180.0 / math.pi


def pose_for(tilt):
    """构造「正对时法线朝相机」的标准解，再绕 x 轴倾斜 tilt 度。"""
    th = math.radians(tilt)
    Rx = np.array([[1, 0, 0],
                   [0, math.cos(th), -math.sin(th)],
                   [0, math.sin(th), math.cos(th)]], dtype=np.float64)
    R0 = np.diag([1.0, -1.0, -1.0])       # 正对镜头：法线 = (0,0,-1)
    R = Rx @ R0
    rvec, _ = cv2.Rodrigues(R)
    tvec = np.array([[0.0], [0.0], [0.35]])   # 35cm 处
    return rvec, tvec


fails = 0


def check(name, ok, detail=""):
    global fails
    if ok:
        print("VERIFY|PY|PASS|%s" % name)
    else:
        fails += 1
        print("VERIFY|PY|FAIL|%s|%s" % (name, detail))


# ---- 1. tilt_deg 在 0/15/30/45/60 度上的反解误差 ----
worst = 0.0
for deg in (0, 15, 30, 45, 60):
    rvec_t, tvec_t = pose_for(deg)
    img_pts, _ = cv2.projectPoints(OBJ, rvec_t, tvec_t, K, DIST)
    ok, rvec, tvec = cv2.solvePnP(OBJ, img_pts, K, DIST)
    if not ok:
        check("solvePnP(%d°)" % deg, False, "解算失败")
        continue
    got = tilt_deg(rvec, tvec)
    err = abs(got - deg)
    worst = max(worst, err)
    check("tilt_deg @ %2d° → %.2f°（误差 %.2f°）" % (deg, got, err), err < 0.5,
          "误差超阈值 0.5°")

print("VERIFY|PY|INFO|tilt_deg 最大误差 %.3f°" % worst)

# ---- 2. 反证：错误做法确实会把「正对」算成 180° ----
rvec_front, tvec_front = pose_for(0)
img_pts, _ = cv2.projectPoints(OBJ, rvec_front, tvec_front, K, DIST)
ok, rvec, tvec = cv2.solvePnP(OBJ, img_pts, K, DIST)
naive = naive_angle(rvec)
check("反证 ‖rvec‖ 在正对时 ≈180°（实测 %.1f°）" % naive, naive > 170.0,
      "该陷阱不成立或 solvePnP 行为已变，需复核正文")

# ---- 3. cv2.imwrite 非 ASCII 路径：必须用 imencode + write_bytes ----
with tempfile.TemporaryDirectory() as td:
    img = np.zeros((32, 32, 3), dtype=np.uint8)
    img[:, :] = (0, 200, 120)

    naive_path = Path(td) / "非ASCII路径_naive.png"
    naive_ok = cv2.imwrite(str(naive_path), img)

    def save_png(image, path):
        ok2, buf = cv2.imencode(".png", image)
        if not ok2:
            raise RuntimeError("PNG 编码失败: %s" % path)
        Path(path).write_bytes(buf.tobytes())

    safe_path = Path(td) / "非ASCII路径_safe.png"
    save_png(img, safe_path)
    check("save_png 在非 ASCII 路径下真的写出文件",
          safe_path.exists() and safe_path.stat().st_size > 0,
          "文件未生成")
    # 说明性信息：naive 的行为随平台而异（Windows 上常静默失败），不作断言
    print("VERIFY|PY|INFO|cv2.imwrite 非 ASCII 路径直接返回 %s（平台相关，仅记录）" % naive_ok)

print("VERIFY|PY|DONE|%d" % fails)
PYEOF

        PY_OUT="$TMPD/py.log"
        "$PYTHON_BIN" "$PY_TEST" > "$PY_OUT" 2>&1
        PY_RC=$?

        if grep -q '^VERIFY|PY|DONE' "$PY_OUT"; then
            while IFS='|' read -r _l section verdict detail extra; do
                case "$verdict" in
                    PASS) pass "$detail" ;;
                    FAIL) fail "$detail" "${extra:-}" ;;
                    INFO) printf '  %sINFO%s  %s\n' "$C_Y" "$C_0" "$detail" ;;
                esac
            done < <(grep '^VERIFY|PY|' "$PY_OUT")
        else
            fail "Python 自测脚本异常退出（退出码 $PY_RC）" "$(tail -3 "$PY_OUT" | tr '\n' ' ')"
            [ "$VERBOSE" -eq 1 ] && cat "$PY_OUT"
        fi
    fi
else
    head1 "2/2 Python 自测"
    skip "已按 --skip-python 关闭"
fi

# ===========================================================================
# 汇总
# ===========================================================================
TOTAL=$((PASS_N + FAIL_N + SKIP_N))
printf '\n%s── 汇总 %s\n' "$C_B" "$C_0"
printf '  通过 %d · 失败 %d · 跳过 %d（共 %d 项）\n' "$PASS_N" "$FAIL_N" "$SKIP_N" "$TOTAL"

if [ "$TOTAL" -eq 0 ]; then
    printf '  %s没有可执行的检查项。%s请安装 Godot，或用 --project 指定含 project.godot 的目录。\n' "$C_R" "$C_0"
    exit 2
fi

if [ "$FAIL_N" -gt 0 ]; then
    printf '  %s结论：不通过%s——上面 FAIL 项需逐个处理；SKIP 的需在具备条件的环境补跑。\n' "$C_R" "$C_0"
    exit 1
fi

if [ "$PASS_N" -eq 0 ]; then
    printf '  %s结论：未验证%s——全部跳过，环境不具备，不能当作通过。\n' "$C_Y" "$C_0"
    exit 2
fi

printf '  %s结论：通过%s（%d 项跳过，注意补跑）\n' "$C_G" "$C_0" "$SKIP_N"
exit 0
