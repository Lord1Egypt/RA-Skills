# LINE OA VNC Auth

安全地透過 **LINE Official Account Manager** 完成登入與 session 驗證：當遠端瀏覽器尚未登入時，提供使用者一個暫時、受密碼保護的 VNC/noVNC 畫面，讓使用者自行完成 LINE Business ID 登入與 MFA；登入後驗證 OA session，並可在使用者已核准時協助執行單次訊息操作。

> **安全界線：** 使用者只能在遠端瀏覽器中輸入帳密、MFA、QR 或恢復碼。請勿在聊天、終端機命令、截圖或日誌中要求、貼上或保存這些敏感資訊。

## 功能

- 隔離 Chromium profile，避免共用代理人或系統瀏覽器的 Cookie。
- `Xvfb` 虛擬桌面 + `x11vnc` + `noVNC`，提供可視化登入。
- Cloudflare Quick Tunnel 讓使用者暫時連入 noVNC；VNC 本身仍以一次性密碼保護。
- 在 UI 中確認正確 LINE OA 帳號、收件人與訊息內容。
- 驗證最新外發泡泡，且不把「已送出」誇大成「已送達」或「已讀」。
- 任務結束後自動關閉 tunnel、VNC/noVNC、browser、virtual display，並清除短效憑證與暫存截圖。

## 適用情境

- 需要透過 LINE Official Account Manager 傳送客服或 OA 訊息。
- 尚未登入 LINE OA，且使用者希望親自在視覺化瀏覽器完成登入或 MFA。
- 需要在代理人執行外部訊息動作前後，有可檢查的 UI 證據。

不適用於一般個人 LINE 帳號自動化、未獲授權帳號，或不需要登入的既有工作流程。

## 安裝需求

Linux（Debian/Ubuntu）範例：

```bash
sudo apt-get update
sudo apt-get install -y chromium xvfb x11vnc novnc websockify cloudflared x11-apps xdotool openssl curl
```

確認工具：

```bash
command -v chromium Xvfb x11vnc websockify cloudflared xwd xdotool
```

若無 root 權限，可把需要的 `.deb` 解壓到私有目錄後執行；使用 `ldd <binary> | grep 'not found'` 檢查缺失 shared libraries。請只從發行者官方來源取得套件或 release，不要直接執行不明安裝腳本。

## 工作流程摘要

1. 從受限設定讀取 LINE OA 的 `chatUrl`。
2. 建立專用的 Chromium profile 與 `Xvfb` display。
3. 啟動 Chromium、僅綁定 loopback 的 x11vnc/noVNC，以及一次性 VNC 密碼。
4. 確認本機 `http://127.0.0.1:6080/vnc.html` 可用後，才建立 Cloudflare Quick Tunnel。
5. 將 noVNC URL 與一次性 VNC 密碼提供給指定使用者；使用者只在瀏覽器內完成 LINE 登入。
6. 獨立確認已回到 `chat.line.biz` 聊天管理頁，並檢查當前 OA 帳號。
7. 打開名稱明確的收件人對話，發送使用者已核准的精確訊息文字。
8. 在 UI 中確認最新外發泡泡；只陳述 UI 顯示的狀態。
9. 除非使用者明確要求保留本機 session，立即關閉與刪除所有暫時遠端存取資源。

完整、可執行的步驟與例外處理請見 [`SKILL.md`](SKILL.md)。

## 搭配的 Skill

本 Skill **不取代**日常的 LINE OA 管理能力；它負責「尚未登入或 session 已失效時」的受控登入、MFA／QR 驗證與 session bootstrap。

請搭配使用 Hermes 內建的 `line-oa` Skill：

| 情境 | 應使用的 Skill |
| --- | --- |
| 已有可用的 LINE OA 登入 session；列出未讀、查看對話、回覆、管理 Notes／Tags 或切換 OA 帳號 | `line-oa` |
| 需要使用者親自在隔離瀏覽器完成 LINE Business ID、MFA 或 QR 登入，再傳送經核准的訊息 | `line-oa-vnc-auth` |

典型順序是先使用 `line-oa-vnc-auth` 建立並驗證登入 session；在需要較完整的日常對話管理時，改由 `line-oa` 執行。兩者都必須從設定取得 OA chat URL，並在實際 UI 中確認目前 OA 帳號與收件人。

## 安全注意事項

- Cloudflare Quick Tunnel 是公開網址，**不是**安全控制；必須使用高熵、短效 VNC 密碼。
- 傳統 VNC 常僅支援前 8 個密碼字元。使用新的隨機 8 字元密碼，並在連線失敗時重新產生；不要要求使用者回貼密碼。
- VNC 與 noVNC 必須各自只綁定 `127.0.0.1`。
- 不可依使用者口頭稱「已登入」就傳送；必須檢查實際 UI。
- 對話名稱有歧義、重複或找不到時，停止並要求使用者選擇，不要猜測。
- 完成後先關閉 Cloudflare tunnel，再關閉 noVNC、VNC、Chromium、Xvfb，最後清除 VNC 密碼與任何含私人內容的截圖。

## 授權

MIT
