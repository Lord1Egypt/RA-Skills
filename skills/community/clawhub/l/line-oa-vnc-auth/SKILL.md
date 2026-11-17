---
name: line-oa-vnc-auth
description: Use when LINE Official Account access requires a user-operated temporary VNC/noVNC login, MFA/QR completion, session verification, and secure teardown.
version: 1.0.3
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [line-oa, line, vnc, novnc, cloudflared, login, messaging]
    related_skills: [secure-remote-browser-access, line-oa]
---

# LINE OA：透過暫時 VNC 驗證登入

## Overview

此流程讓使用者在隔離的圖形化 Chromium 中自行完成 LINE Business ID 登入與 MFA，再由代理人於 LINE Official Account Manager 確認收件人、傳送指定訊息、驗證外發泡泡，最後關閉所有遠端存取服務。

**帳密、MFA、QR 內容、Cookie 絕不可在聊天、命令列、截圖或日誌中要求、轉貼或保存。** 使用者只能在 VNC 畫面的 LINE 網頁內輸入敏感資訊。

## When to Use

- 使用者要求從 LINE Official Account Manager 發送訊息，但遠端瀏覽器尚未登入。
- 使用者要求透過 VNC/noVNC 自行執行 LINE 登入或二次驗證。
- 需要在登入後，確認正確 LINE 對話與外發訊息結果。

不要用於一般個人 LINE 帳號自動化、未獲授權的帳號登入，或可由既有已登入瀏覽器安全完成的工作。

## Required Components

Linux 範例套件（Debian/Ubuntu）：

```bash
sudo apt-get update
sudo apt-get install -y chromium xvfb x11vnc novnc websockify cloudflared x11-apps xdotool openssl curl
```

確認：

```bash
command -v chromium Xvfb x11vnc websockify cloudflared xwd xdotool
```

若系統套件庫沒有 `cloudflared`，從 Cloudflare 官方 release 下載目前架構的 `.deb`，以 `dpkg-deb -x` 解壓到受限目錄，勿把未驗證的第三方安裝腳本直接 pipe 到 shell。若無 root 權限，也可將 `.deb` 解壓至專用目錄，並設定 `LD_LIBRARY_PATH` 指向其私有函式庫；每個二進位啟動前先以 `ldd` 檢查缺少的 shared libraries。

## Secure Session Setup

1. **讀取 LINE OA chat URL。** 從受限設定檔取得 `chatUrl`（例如 `https://chat.line.biz/U...`）；不要把權杖或 Cookie 寫入設定。完成條件：只取得聊天管理網址。
2. **建立隔離工作區與瀏覽器 profile。**

   ```bash
   BASE="$HOME/.line-oa-remote"
   install -d -m 700 "$BASE/profile" "$BASE/tmp"
   ```

   完成條件：profile 不與系統或代理人既有 Chrome profile 共用。
3. **啟動本機虛擬桌面與隔離 Chromium。**

   ```bash
   Xvfb :99 -screen 0 1280x900x24 -nolisten tcp &
   DISPLAY=:99 chromium --no-sandbox --disable-dev-shm-usage \
     --user-data-dir="$BASE/profile" --window-size=1280,900 "$CHAT_URL" &
   ```

   完成條件：X server 只供本機使用，Chromium 使用指定隔離 profile。
4. **產生短效 VNC 密碼。** 傳統 VNC 通常只支援前 8 個字元；產生 8 個高熵、可輸入的字元，檔案權限設為 `600`，並以 `x11vnc -storepasswd` 建立雜湊檔。只把一次性明文密碼私下傳給指定使用者；不得在日誌印出。
5. **只綁定 loopback 的 VNC 與 noVNC。**

   ```bash
   x11vnc -display :99 -localhost -rfbauth "$BASE/vnc-passwd" \
     -forever -shared -rfbport 5901 &
   websockify --web /usr/share/novnc 127.0.0.1:6080 127.0.0.1:5901 &
   curl -fsS http://127.0.0.1:6080/vnc.html >/dev/null
   ```

   完成條件：VNC 僅監聽 `127.0.0.1:5901`，noVNC 僅監聽 `127.0.0.1:6080`，本機 `vnc.html` 回傳 200。
6. **最後才建立 Cloudflare Quick Tunnel。**

   ```bash
   cloudflared tunnel --url http://127.0.0.1:6080 --no-autoupdate
   ```

   從輸出擷取唯一 `https://*.trycloudflare.com` 網址，驗證 `https://…/vnc.html` 回傳 200。Quick Tunnel 是公開網址，**不是**存取控制；VNC 一次性密碼仍為必要保護。
7. **給使用者最小指示。** 傳送 noVNC 網址及短效 VNC 密碼，請他直接在遠端瀏覽器完成 LINE 登入。明確說明：不要在聊天中傳送 LINE 密碼、MFA、QR 或恢復碼。完成條件：使用者回覆已登入，或畫面可見聊天管理頁。

## Login Verification and Sending

1. **獨立驗證登入。** 確認頁面是 `chat.line.biz` 聊天管理介面，而非 `account.line.biz` 登入頁；確認目前 OA 帳號顯示正確。不可只依使用者口頭稱已登入。
2. **確認對話目標。** 在聊天列表找到使用者指定名稱，打開對話，並在 UI 看到正確名稱才可輸入。名稱模糊、重複或不存在時，停止並請使用者選擇。
3. **只發送已核准的精確文字。** 點選輸入框，輸入指定內容，再按 Send/Enter。不要夾帶簽名、測試文字或自動回覆。
4. **驗證結果。** 截取當前 X display 或檢查 DOM，確認正確對話中的最新外發泡泡內容完全一致。只回報 UI 顯示的狀態；外發泡泡表示已送出，不能推論「已送達」或「已讀」。

### X11 Screenshot Fallback

當一般瀏覽器自動化無法連上該隔離 Chromium 時，可擷取 virtual display：

```bash
DISPLAY=:99 xwd -root -silent > "$BASE/line-oa.xwd"
```

將 XWD 轉成 PNG 後用視覺工具確認登入狀態、收件人與外發泡泡。轉換後的截圖可能包含私人聊天內容；只供本次驗證使用，完成後刪除。

可用 `xdotool` 互動，但每次點擊前都必須從最新截圖重新確認座標與對話名稱。避免依舊截圖或猜測座標。

## Teardown (Required)

除非使用者**明確要求**保留本機已登入 session 以便緊接的後續工作，完成傳送與驗證後立即：

1. 先停止 `cloudflared`，並驗證原 public noVNC URL 已無法使用（非 200／連線失敗）。
2. 停止 websockify/noVNC、x11vnc、Chromium 與 Xvfb。
3. 安全刪除 VNC 明文、雜湊密碼檔、暫存 QR、XWD/PNG 截圖與任何 temporary access artifacts。
4. 若使用者明確要求保留登入，才可保留隔離 browser profile 與存活的本機 Chromium/Xvfb；仍必須關閉 tunnel、noVNC、VNC，刪除一次性 VNC 密碼，並說明 session 無法保證跨重啟持續。

## Common Pitfalls

1. **VNC 密碼被拒絕。** 多數 RFB 實作有效密碼僅 8 字元；更換為新的隨機 8 字元密碼並重啟 x11vnc。不要重用或請使用者貼回密碼。
2. **一次性 VNC 密碼誤貼到公開／群組聊天。** 立刻停止 x11vnc、作廢並刪除舊密碼檔，產生新的 8 字元高熵密碼後才可重啟；舊 tunnel URL 或舊密碼一律視為失效。不要在後續訊息引用外洩的密碼。
3. **把 Quick Tunnel 當作安全機制。** Quick Tunnel 是公開的；必須加上高熵短效 VNC 密碼，並在完成後關閉。
3. **browser tool 與 VNC browser 是不同 session。** 以 X11 screenshot/實際 UI 驗證隔離 browser 的狀態，不要假設一方登入代表另一方登入。
4. **容器缺少 x11vnc 依賴。** 用 `ldd <binary> | grep 'not found'` 找出缺少 library；安裝或解壓正確相依套件後再啟動，勿把警告一概當作登入失敗。
5. **誤稱已送達或已讀。** 除非 LINE UI 明確顯示，僅能說「已看到外發訊息泡泡」。
6. **未清理遠端桌面。** 沒有使用者明確保留要求時，這是安全缺陷；必須關閉 tunnel 並刪除短效憑證。

## Verification Checklist

- [ ] 使用隔離 Chromium profile 與專用 Xvfb display
- [ ] x11vnc/noVNC 均只綁定 loopback
- [ ] 使用者自行在畫面內處理 LINE 帳密與 MFA
- [ ] public noVNC URL 與 VNC 一次性密碼已測試可用
- [ ] 已在 UI 確認正確 OA 帳號、對話名稱與訊息內容
- [ ] 已看到對應最新外發泡泡，且報告未超過 UI 證據
- [ ] tunnel、noVNC、VNC、browser、Xvfb 已停止（或獲明確允許保留 browser session）
- [ ] VNC 密碼、登入畫面與聊天截圖等暫存檔已清除
