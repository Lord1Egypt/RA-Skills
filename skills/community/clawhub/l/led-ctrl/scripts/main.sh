#!/bin/bash
# 第一行稱為 Shebang，指定使用 /bin/bash 來執行此腳本
# 專案名稱或功能描述：Pi GPIO 技能控制 - OpenClaw 專案
# 使用範例範例：./main.sh gpio_on 17 (這會開啟第 17 號引腳)
# ---------- 變數讀取 ----------
# $1 代表執行指令時的第一個參數 (例如: gpio_on)
ACTION="$1"
# $2 代表執行指令時的第二個參數 (例如: 17)
PIN="$2"
# ---------- 參數檢查 ----------
# 檢查 ACTION 或 PIN 是否為空字串 (-z 代表 zero，意即字串長度為 0)
if [[ -z "$ACTION" || -z "$PIN" ]]; then
# 如果參數不足，顯示正確的用法提示並退出程式
echo "Usage: gpio_on <pin> | gpio_off <pin>"
# exit 1 代表程式異常終止（回傳非 0 值）
exit 1
fi
# ---------- 伺服器資訊 ----------
# 設定樹莓派控制伺服器的 IP 地址
# 請確保執行此腳本的電腦與樹莓派在同一個區域網路 (LAN) 下
PI_IP="192.168.0.14"
# ---------- 發送請求 ----------
# 使用 curl 工具發送 HTTP POST 請求
# -s (silent): 靜音模式，不顯示進度條或錯誤訊息
# http://$PI_IP:9000/run: 目標 API 地址
curl -s http://$PI_IP:9000/run \
-H "Content-Type: application/json" \
-d "{\"action\": \"$ACTION\", \"pin\": $PIN}"
# 參數說明：
# -H: 設定 HTTP Header，告知伺服器我們發送的是 JSON 格式
# -d: 實際發送的 Data (JSON 格式)，這裡會自動帶入變數 $ACTION 與 $PIN