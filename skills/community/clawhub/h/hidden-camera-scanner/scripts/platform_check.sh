#!/usr/bin/env bash
#
# hidden-camera-scanner · platform_check.sh
# 环境体检：识别平台、检查各阶段依赖，输出能力矩阵与缺失项的安装/替代指引。
# 用途：会话开始时先跑一次，向用户如实说明本机哪些阶段能跑、哪些不能、替代方案是什么。
#
# 用法：bash platform_check.sh [--install]
#   --install : 安装缺失的依赖（netaddr / nmap / bleak）。⚠️ 必须先向操作者确认、获得同意后
#               才能带此参数运行——本脚本只负责执行，征询同意是 Agent 的职责。
# 退出码：0 = 至少 Wi-Fi 或报告可用；1 = 平台完全不可运行（如 iOS）

set -uo pipefail

DO_INSTALL=0
while [[ $# -gt 0 ]]; do
  case "$1" in
    --install) DO_INSTALL=1;;
    -h|--help) grep -E '^#' "$0" | sed 's/^# \{0,1\}//'; exit 0;;
    *) echo "未知参数: $1" >&2; exit 1;;
  esac
  shift
done

RAW_OS="$(uname -s)"
IS_DARWIN=0; IS_WIN=0; IS_TERMUX=0; PLAT=""

case "$RAW_OS" in
  Darwin)  IS_DARWIN=1; PLAT="macOS";;
  MINGW*|MSYS*|CYGWIN*) IS_WIN=1; PLAT="Windows (Git Bash)";;
  Linux)
    if [[ -n "${TERMUX_VERSION:-}" ]]; then IS_TERMUX=1; PLAT="Android (Termux)"
    else PLAT="Linux"; fi;;
  *)
    # iOS / 未知平台
    echo "平台: $RAW_OS"
    echo ""
    echo "能力: ①Wi-Fi ❌  ②蓝牙 ❌  ③MVT ❌  ④人工排查 ✅  ⑤报告 ❌"
    echo ""
    echo "该平台无终端/不允许任意网络探测，脚本均不可运行。替代方案："
    echo "  1. 追踪器检测：iOS「查找」App 追踪器检测 / AirGuard / 系统「未知追踪器警报」"
    echo "  2. 局域网设备：Fing 等网络扫描 App"
    echo "  3. 人工排查：照技能 manual_checklist.md 清单执行（手电镜面测试等）"
    echo "  4. 如需汇总报告，把发现结果带到 Mac / Windows 上用 generate_report.py 生成"
    exit 1;;
esac

echo "平台: $PLAT"
echo ""

have() { command -v "$1" >/dev/null 2>&1; }

# ---- 依赖检测 ----
PY=""
if have python3; then PY="python3"; elif have python; then PY="python"; fi
PY_VER=""; BLEAK="no"; NETADDR="no"
if [[ -n "$PY" ]]; then
  PY_VER="$($PY -c 'import sys;print(".".join(map(str,sys.version_info[:2])))' 2>/dev/null)"
  $PY -c "import bleak" >/dev/null 2>&1 && BLEAK="yes"
  $PY -c "import netaddr" >/dev/null 2>&1 && NETADDR="yes"
fi
NMAP="no"; have nmap && NMAP="yes"

# ---- 平台相关安装提示 ----
NMAP_HINT=""; BLEAK_HINT=""
case "$PLAT" in
  macOS)
    NMAP_HINT="brew install nmap"
    BLEAK_HINT="pip install bleak（首次运行需在 系统设置→隐私与安全性→蓝牙 授权终端）";;
  "Windows (Git Bash)")
    NMAP_HINT="winget install Insecure.Nmap（安装时勾选 Npcap）；注意 WSL2 不可用于 Wi-Fi 扫描"
    BLEAK_HINT="pip install bleak（需 Windows 10 16299+）";;
  "Android (Termux)")
    NMAP_HINT="pkg install nmap"
    BLEAK_HINT="（不可用）bleak 仅支持打包成 App 的 Python，Termux 无 Java 桥";;
  *)
    NMAP_HINT="sudo apt install nmap 或 dnf install nmap"
    BLEAK_HINT="pip install bleak（需 BlueZ >= 5.43）";;
esac

# ---- 能力判定 ----
WIFI="✅"; BLE="✅"; REPORT="✅"
if [[ "$IS_TERMUX" -eq 1 ]]; then BLE="❌"; fi
[[ -z "$PY" ]] && REPORT="❌"

echo "能力: ①Wi-Fi $WIFI  ②蓝牙 $BLE  ③MVT ⚠️需授权+取证知识  ④人工排查 ✅  ⑤报告 $REPORT"
echo ""
# 阶段①主用 scripts/wifi_scan.py（纯 Python，免 nmap）；nmap 仅为可选增强（效率更高）
if [[ "$NMAP" == "yes" ]]; then NMAP_NOTE="可选增强已装（wifi_scan.py 为主，nmap 效率更高）"
else NMAP_NOTE="未装（不影响：wifi_scan.py 纯 Python 扫描，无需 nmap）"; fi

# ---- 缺失依赖安装（--install，需 Agent 事先征得操作者同意）----
install_missing() {
  if [[ "$NETADDR" == "no" && "$WIFI" == "✅" && -n "$PY" ]]; then
    echo "▶ 安装 netaddr（阶段①厂商识别，纯 Python 包）..."
    if "$PY" -m pip install -q netaddr 2>/dev/null; then NETADDR="yes"
    elif "$PY" -m pip install -q --user netaddr 2>/dev/null; then NETADDR="yes"
    else
      echo "  ✗ pip 安装失败（可能为 externally-managed 环境）。建议用 venv："
      echo "    $PY -m venv ~/.venvs/hcs && ~/.venvs/hcs/bin/pip install netaddr"
    fi
  fi
  if [[ "$NMAP" == "no" && "$WIFI" == "✅" ]]; then
    echo "▶ 安装 nmap（可选增强，不装不影响功能）..."
    case "$PLAT" in
      macOS)
        if have brew; then brew install nmap && NMAP="yes" || echo "  ✗ brew 安装失败，请手动执行: brew install nmap"
        else echo "  ✗ 未找到 Homebrew，请先安装 brew 或到 nmap.org 手动安装"; fi;;
      "Windows (Git Bash)")
        if have winget; then winget install --id Insecure.Nmap -e --accept-source-agreements --accept-package-agreements && NMAP="yes" || echo "  ✗ winget 安装失败，请到 nmap.org 下载安装包（勾选 Npcap）"
        else echo "  ✗ 未找到 winget，请到 nmap.org 下载安装包（勾选 Npcap）"; fi;;
      "Android (Termux)")
        pkg install -y nmap && NMAP="yes" || echo "  ✗ pkg 安装失败，请手动执行: pkg install nmap";;
      *)
        if have apt-get; then sudo apt-get install -y nmap && NMAP="yes" || echo "  ✗ apt 安装失败，请手动执行: sudo apt install nmap"
        elif have dnf; then sudo dnf install -y nmap && NMAP="yes" || echo "  ✗ dnf 安装失败，请手动执行: sudo dnf install nmap"
        else echo "  ✗ 未识别的包管理器，请手动安装 nmap"; fi;;
    esac
  fi
  if [[ "$BLEAK" == "no" && "$BLE" == "✅" && -n "$PY" ]]; then
    echo "▶ 安装 bleak ..."
    if "$PY" -m pip install -q bleak 2>/dev/null; then BLEAK="yes"
    elif "$PY" -m pip install -q --user bleak 2>/dev/null; then BLEAK="yes"
    else
      echo "  ✗ pip 安装失败（可能为 externally-managed 环境）。建议用 venv："
      echo "    $PY -m venv ~/.venvs/hcs && ~/.venvs/hcs/bin/pip install bleak"
      echo "    之后用 ~/.venvs/hcs/bin/python 运行 bt_scan.py"
    fi
  fi
}

if [[ "$DO_INSTALL" -eq 1 ]]; then
  echo "▶ 已获操作者同意，安装缺失依赖..."
  echo ""
  install_missing
  # 复检
  NMAP="no"; have nmap && NMAP="yes"
  NETADDR="no"; BLEAK="no"
  [[ -n "$PY" ]] && "$PY" -c "import netaddr" >/dev/null 2>&1 && NETADDR="yes"
  [[ -n "$PY" ]] && "$PY" -c "import bleak" >/dev/null 2>&1 && BLEAK="yes"
  if [[ "$NMAP" == "yes" ]]; then NMAP_NOTE="可选增强已装"; else NMAP_NOTE="未装（不影响 wifi_scan.py）"; fi
  echo ""
  echo "▶ 复检结果:"
fi

echo "依赖状态:"
echo "  python:  ${PY:-未安装} ${PY_VER:+($PY_VER)}"
echo "  netaddr: $NETADDR （阶段①厂商识别，纯 Python 包；缺失时厂商显示为未知）"
echo "  nmap:    $NMAP  （${NMAP_NOTE}）"
echo "  bleak:   $BLEAK （阶段②蓝牙扫描依赖）"
echo ""
if [[ "$NETADDR" == "no" && "$WIFI" == "✅" && -n "$PY" ]]; then echo "建议安装: $PY -m pip install netaddr"; fi
if [[ "$NMAP" == "no" && "$WIFI" == "✅" ]]; then echo "可选安装（增强，非必需）: $NMAP_HINT"; fi
if [[ "$BLEAK" == "no" && "$BLE" == "✅" ]]; then echo "建议安装: $BLEAK_HINT"; fi
if [[ "$DO_INSTALL" -eq 0 && ( "$NETADDR" == "no" || "$BLEAK" == "no" ) ]]; then
  echo ""
  echo "确认安装后可执行: bash $0 --install"
fi
if [[ "$IS_TERMUX" -eq 1 ]]; then
  echo ""
  echo "⚠️ 本平台不支持蓝牙扫描（阶段②）。替代方案："
  echo "  1. 装 AirGuard / 用系统「未知追踪器警报」"
  echo "  2. 把 bt_scan.py 放到 Mac / Windows 上跑"
  echo "  3. 人工排查照 manual_checklist.md 清单执行"
fi
if [[ "$IS_WIN" -eq 1 ]]; then
  echo ""
  echo "⚠️ Windows 注意：必须用 Git Bash 运行 .sh；不要用 WSL2（默认 NAT 看不到物理局域网）。"
fi
if [[ "$REPORT" == "❌" ]]; then
  echo ""
  echo "⚠️ 本平台无 Python，报告（阶段⑤）不可用。替代：把扫描/人工排查结果带到 Mac / Windows 汇总。"
fi

[[ "$WIFI" == "✅" || "$REPORT" == "✅" ]] && exit 0 || exit 1
