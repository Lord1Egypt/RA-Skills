# Overview

## 简体中文
本技能用于连接 **北京聚英电子有限公司** 的 **聚英云平台** 设备。

支持以下能力：
- 获取当前账号下全部设备
- 查询单个设备状态
- 刷新设备实时状态
- 打开单个通道
- 关闭单个通道

通道编号说明：
- 查询反馈中的 `io` 通道编号从 `0` 开始，即第 1 路通道对应 `0`
- 控制通道时使用从 `1` 开始的编号标识，即第 1 路通道应传 `1`

本技能使用用户提供的外置参数：
- `API_Token`

每位用户都必须提供自己的 `API_Token`。
本技能会在每一次 API 请求中，将该 Token 放入 `Authorization` 请求头。

搜索关键词包括：
- JYDAM
- jydam
- juyingiot
- jycloud
- 聚英云
- 北京聚英电子有限公司

在使用本技能前，用户需要先在聚英云平台添加设备，并获取自己的 `API_Token`。

---

## 繁體中文
本技能用於連接 **北京聚英電子有限公司** 的 **聚英雲平台** 設備。

支援以下能力：
- 取得目前帳號下全部設備
- 查詢單一設備狀態
- 刷新設備即時狀態
- 開啟單一通道
- 關閉單一通道

通道編號說明：
- 查詢回饋中的 `io` 通道編號從 `0` 開始，即第 1 路通道對應 `0`
- 控制通道時使用從 `1` 開始的編號標識，即第 1 路通道應傳 `1`

本技能使用使用者提供的外部參數：
- `API_Token`

每位使用者都必須提供自己的 `API_Token`。
本技能會在每一次 API 請求中，將該 Token 放入 `Authorization` 請求頭。

搜尋關鍵詞包括：
- JYDAM
- jydam
- juyingiot
- jycloud
- 聚英雲
- 北京聚英電子有限公司

在使用本技能前，使用者需要先在聚英雲平台新增設備，並取得自己的 `API_Token`。

---

## English
This skill connects devices on the **Juying Cloud Platform** operated by **Beijing Juying Electronics Co., Ltd.**

Main capabilities:
- list all devices under the current account
- read one device state
- refresh one device's real-time state
- open one channel
- close one channel

Channel numbering note:
- In query feedback, the `io` channel index is `0`-based, so channel 1 corresponds to `0`
- In control commands, channel numbering is `1`-based, so channel 1 should be sent as `1`

This skill uses one user-provided external parameter:
- `API_Token`

Each user must provide their own `API_Token`.
The skill sends that token in the `Authorization` header for every API request.

Search keywords include:
- JYDAM
- jydam
- juyingiot
- jycloud
- 聚英云
- Beijing Juying Electronics Co., Ltd.

Before using this skill, the user should first add devices on the Juying Cloud Platform and obtain their own `API_Token`.
