# READONLY_GATEWAY_BOUNDARIES

## 一句話定位
read-only gateway 是 **跨節點查 Arthur-OS 的安全只讀通道**。
它用來查，不用來寫，也不是遠端控制 Obsidian 的 API。

## 先記住這 6 條
1. Mac Studio 本機打：`http://127.0.0.1:27133`
2. 其他節點（5090 / 5092 / 5094 / Mac mini）打：`http://10.0.1.10:27133`
3. **不要** 在其他節點打自己的 `127.0.0.1:27133`
4. gateway health 要打：`/health`
5. gateway 根路徑 `/` 回 `not_found` 屬正常，**不代表沒有 OB**
6. `27133` 與 `27124` 是兩層不同鑑權，**token 不要混用**

## Canonical 鏈路
### Mac Studio 本機
- gateway：`http://127.0.0.1:27133`
- health：`GET /health`
- upstream：`https://127.0.0.1:27124`
- upstream 來源：Obsidian app 的 `obsidian-local-rest-api` plugin

### 其他節點
- gateway：`http://10.0.1.10:27133`
- health：`http://10.0.1.10:27133/health`
- 不要打自己 `127.0.0.1`

補充：
- 舊入口 `19092` 不再是 canonical
- 若 `27133` 活著但搜尋炸掉，優先懷疑 `27124` upstream 沒起來
- `27124` 是否存在，取決於 Obsidian app 已啟動且 plugin 正常掛起

## 什麼時候可以用
- 其他節點需要 **查** Arthur-OS
  - 找筆記名稱
  - 搜筆記內容
  - 讀單篇筆記
- 主控端暫時不方便跑互動式工具，但需要做 LAN 只讀查詢

## 什麼時候不要用
- 任何寫入：create / append / patch / rename / move / delete
- 任何遠端控制：command execute / plugin command / command palette
- 任何「查到就直接動檔」的捷徑

## Token 邊界（高頻坑）
- `27133` gateway bearer：`arthur-obsidian-readonly-20260312`
- `27124` plugin bearer / apiKey：`b9cf98bc7b7e074996691b54243a3154ca7b59e136c780388add760c25c5eeff`
- 不要把 gateway token 拿去打 `27124`
- 也不要把 `27124` 的 plugin token 拿去打 `27133`

## 最小排障順序
### 在 Mac Studio 本機
1. 先測 `http://127.0.0.1:27133/health`
2. 若 health 正常但 search/content 失敗，再查 `127.0.0.1:27124`
3. 若 `27124` refused，先確認 Obsidian app 是否已啟動

### 在其他節點
1. 先測 `http://10.0.1.10:27133/health`
2. 不要先測自己的 `127.0.0.1:27133`
3. 若遠端 health 失敗，再回頭檢查 Mac Studio 的 `27133 / 27124`

## 不在這裡處理
- 部署、launchd/systemd、TLS、反向代理、port 暴露
- OpenAPI、SDK、MCP 封裝

這些應留在 OpenClaw / Server 類文件，不放在這個治理 skill 裡。
