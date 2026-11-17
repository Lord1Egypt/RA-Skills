---
name: oo-sf-express
description: "SF Express (open.sf-express.com). Use this skill for ANY SF Express request — reading, creating, updating, and deleting data. Whenever a task involves SF Express, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "SF Express"
  author: "OOMOL"
  version: "1.0.5"
  services: ["sf_express"]
  icon: "https://static.oomol.com/logo/third-party/sf_express.png"
---

# SF Express

Operate **SF Express** through your OOMOL-connected account. This skill calls the `sf_express` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected SF Express. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "sf_express" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "sf_express" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `check_pickup_time` — Check whether an SF Express pickup at an address can be served at a planned time, optionally returning the service window.
- `coldchain_cancel_order` — Cancel an SF Cold Chain transport order that has not been accepted yet. [destructive]
- `coldchain_check_transport_flow` — Check whether SF Cold Chain can serve a given origin-destination flow with a product, returning the serving points' business hours and the available temperature levels.
- `coldchain_create_order` — Create an SF Cold Chain transport order (陆运运输). The monthly account is required for monthly-settlement payment (PR_ACCOUNT). [write]
- `coldchain_estimate_delivery_time` — Estimate the SF Cold Chain delivery time for a flow and one or more products, including pickup and delivery transit times.
- `coldchain_estimate_transport_fee` — Estimate the SF Cold Chain transport fee for a flow and one or more products, returning the per-product fee breakdown.
- `coldchain_query_order_info` — Query the full details of an SF Cold Chain order, including parties, weights, goods lines, value-added services, and the sign-back receipt.
- `coldchain_query_route` — Query SF Cold Chain route events by waybill number, SF order number, or client order number, combined with the order source code.
- `coldchain_query_waybill_no` — Query the waybill numbers (master waybill, sign-back receipt number, child waybills) generated for an SF Cold Chain order.
- `create_order` — Create a real SF Express shipment order (下订单) and allocate waybill numbers; charges may apply. Mainland China and Hong Kong/Macao/Taiwan lanes are supported. The response includes the screening result (filterResult) and the allocated waybill numbers. Use pre_order to validate an order without creating it. [write]
- `delete_print_template` — Delete a merchant custom print template (ISV 删除自定义模板); SF caps the number of templates per account, so delete unused ones before adding new. [destructive]
- `estimate_delivery_time` — Query the promised delivery time for an SF Express waybill, verified by the sender or recipient phone number or by the monthly card that paid the waybill.
- `filter_order` — Check whether origin and destination addresses are within SF Express pickup and delivery coverage (筛单), before placing an order.
- `freight_append_install_service` — Append an install service to an existing SF waybill. The append is only confirmed once the waybill is picked up; the final result arrives via the install status push. This endpoint requires SF sales onboarding (联系客户经理). [write]
- `freight_append_ltl_sub_waybill` — Append sub waybill numbers to an SF Freight LTL order, for shippers who finalize the package count after packing. Only own orders before pickup; at most 1200 sub waybills per order. Reprint the waybills afterwards if they were already printed. [write]
- `freight_audit_value_added_service` — Audit a value-added service request (审核增值服务), for example the JZ17 好评返现 service. [write]
- `freight_bid_report_add_fee_result` — Report the master's decision on a bidding install order's add-fee request (增加费用结果回传). [write]
- `freight_bid_report_complaint_result` — Report the complaint handling result for a bidding install order (接收投诉结果). [write]
- `freight_bid_report_operation_node` — Report an operation node for a bidding install order (供应商自主报价操作节点回传). operate_data's required keys depend on operate_code: OP000006 needs installMaster+installConcat, OP000004 needs appTime, OP000008/OP000001/OP000010 need imgUrl, OP000013 needs closeReason. [write]
- `freight_bid_report_refund_result` — Report the master's decision on a bidding install order's refund request (退款结果回传). [write]
- `freight_bid_send_evidence_notice` — Ask the customer for supplementary evidence while handling a complaint (通知用户补充举证). The deadline defaults to 12 hours after the notice time. [write]
- `freight_bid_submit_master_evidence` — Submit the master's evidence for a complaint on a bidding install order (师傅举证回传). [write]
- `freight_bid_submit_quote` — Submit a supplier master's quote for a bidding install order (回传报价). [write]
- `freight_cancel_install_order` — Cancel an appended install service; the waybill must not be picked up yet. [destructive]
- `freight_cancel_ltl_order` — Cancel an SF Freight LTL order. Only orders not yet picked up can be cancelled. [destructive]
- `freight_cancel_recovery_order` — Cancel an SF recovery order; not possible once the master has arrived. [destructive]
- `freight_cancel_tl_order` — Cancel an SF Freight truckload order. Cancellation only succeeds while the order is in a cancellable state; otherwise the error message explains why. [destructive]
- `freight_check_address_reachable` — Check whether an address is within SF Freight pickup or delivery coverage (订单筛单).
- `freight_city_calc_fee` — Calculate the freight fee for an SF Freight city-delivery shipment before ordering.
- `freight_city_cancel_order` — Cancel an SF Freight city-delivery order. [destructive]
- `freight_city_confirm_order` — Place an SF Freight city-delivery (城市配送货运) order. send_start_time must be at least 2 hours in the future. [write]
- `freight_city_get_order_detail` — Get the details of an SF Freight city-delivery order by order number or client order number.
- `freight_city_list_appointment_times` — Get the pickup appointment time window available for a city in SF Freight city delivery.
- `freight_city_list_available_vas` — List the value-added services available for a city and vehicle model in SF Freight city delivery.
- `freight_city_list_cities` — List the cities where SF Freight city delivery is available.
- `freight_city_list_orders` — List SF Freight city-delivery orders for an ordering phone number, with optional time and pagination filters.
- `freight_city_list_vehicles` — List the vehicle models available for a city and business scenario in SF Freight city delivery.
- `freight_create_install_order` — Create an SF install order (安装单下单): install-only, pickup-and-install, or repair. [write]
- `freight_create_ltl_order` — Place an SF Freight (快运) LTL order for bulky or heavy shipments. This is for 大件 special scenarios only; for regular parcels use sf_express.create_order. When waybill_no is provided, the order uses that reserved master waybill number instead of generating one. [write]
- `freight_create_recovery_order` — Create an SF recovery order (回收单下单) for door-to-door goods recycling. The pickup date must be within 3 days, the window whole hours between 08:00 and 21:00. [write]
- `freight_create_tl_order` — Create an SF Freight truckload (整车直达) order. Set generate_waybill_no to have SF assign a waybill number, or pass your own waybill_no. A monthly card (monthly_card) is required when pay_method is 1 (寄付月结) or 2 (寄付转第三方). [write]
- `freight_create_vehicle_track_url` — Create the vehicle track playback page URL for an SF Freight waybill. Requires the monthly card that paid the waybill. [write]
- `freight_crossborder_cancel_order` — Cancel one or more SF cross-border bulky orders by waybill number. [destructive]
- `freight_crossborder_confirm_delivery_window` — Confirm and update a new delivery window option for an FBA shipment as the carrier agent. [write]
- `freight_crossborder_get_delivery_window` — Query the current delivery window of an FBA shipment as the carrier agent.
- `freight_crossborder_get_pod_info` — Query the proof-of-delivery information for an SF cross-border bulky waybill.
- `freight_crossborder_get_print_batch` — Start an SF cross-border bulky waybill print download and get the print batch number. [write]
- `freight_crossborder_place_order` — Place an SF cross-border bulky (大件跨境) order and receive the master and sub waybill numbers. A monthly card (monthly_card) is required when settlement_type is 2 (寄付月结). [write]
- `freight_crossborder_query_delivery_window_options` — Query the selectable delivery window options for an FBA shipment as the carrier agent.
- `freight_crossborder_query_postcode_address` — Check whether a destination postal code is served for SF cross-border bulky shipments, returning the address info and remote-area flag.
- `freight_crossborder_query_print_result` — Get the waybill print file download URLs for a print batch created by freight_crossborder_get_print_batch.
- `freight_crossborder_report_trace` — Report logistics traces for an SF cross-border bulky shipment, as the carrier agent. Routes are stored newest first; milestone values make the corresponding nodes visible to end customers. [write]
- `freight_crossborder_upload_pod_files` — Upload proof-of-delivery files for an SF cross-border bulky waybill, as publicly accessible file URLs. [write]
- `freight_forward_apply_add_fee` — Apply for an additional last-mile fee on an SF Freight forwarding waybill; currently only 入仓垫付 (warehouse entry advance, type 50) is supported. [write]
- `freight_forward_apply_monthly_payment` — Bind the payment of an SF Freight forwarding waybill to a monthly settlement card (月结卡号) so the fee is charged to it. Requires a monthly card. [write]
- `freight_forward_place_return_order` — Place a return-receipt order (标快到付) for one or more SF Freight forwarding waybills. [write]
- `freight_forward_report_exception` — Report an exception for an SF Freight forwarding waybill, for example damage, miscount, delay, or a reweigh appeal. delay_days is required for codes SIGN_03/SIGN_05/SIGN_15/TRANSITING_15; weight and sub_items are required for the reweigh codes HANDOVER_06/TRANSITING_17. [write]
- `freight_forward_start_pay` — Get the payment QR code for an unpaid SF Freight forwarding waybill. [write]
- `freight_forward_update_order_status` — Upload a real-time order status update for an SF Freight forwarding shipment. [write]
- `freight_forward_upload_driver` — Upload the pickup driver information for an SF Freight forwarding order once the carrier assigns the driver. [write]
- `freight_forward_upload_receipt` — Upload the sign-back receipt number for an SF Freight forwarding waybill. [write]
- `freight_forward_upload_return_route` — Upload route events for an SF Freight forwarding return receipt. Upload incrementally, newest first; cover all loading, unloading, out-for-delivery, and signed nodes. [write]
- `freight_forward_upload_route` — Upload route events for an SF Freight forwarding waybill. Upload incrementally, newest first; cover all loading, unloading, and out-for-delivery nodes (use freight_forward_upload_sign_image for the signed node). [write]
- `freight_forward_upload_sign_image` — Upload the recipient's signature or other proof-of-delivery images for an SF Freight forwarding waybill; SF reviews them and then marks the waybill signed. Image URLs must be publicly accessible. [write]
- `freight_forward_upload_track` — Upload one vehicle track point for an SF Freight forwarding waybill. [write]
- `freight_forward_upload_track_batch` — Upload multiple vehicle track points for one SF Freight forwarding waybill in a single call. All track points must belong to the same waybill number. [write]
- `freight_forward_upload_waybill_remark` — Upload a remark for an SF Freight forwarding waybill. [write]
- `freight_get_ltl_order_result` — Get the latest dispatch result of an SF Freight LTL order placed with courier call (下call), including the assigned waybill numbers.
- `freight_list_crossborder_transfer_nos` — List the transfer waybill numbers (转单号) of an SF cross-border bulky mother waybill.
- `freight_notify_install_arrival` — Mark an install order's goods as arrived (到货通知), optionally completing the pickup address. Only the not-arrived to arrived transition is supported. [write]
- `freight_query_crossborder_route` — Query the route of an SF cross-border bulky (大件跨境) waybill. For transfer waybill numbers (转单号), use freight_query_crossborder_transfer_routes.
- `freight_query_crossborder_transfer_routes` — Query the route events of a transfer waybill number (转单号) for an SF cross-border bulky shipment.
- `freight_query_delivery_rules` — Query the home-delivery service rules (宅配规则) bound to one or more SF monthly cards.
- `freight_query_install_order` — Query an SF install order's status and fee breakdown by client order number.
- `freight_query_recovery_products` — Query the full SF recovery product catalog (回收品类). The list is large and returned in full; cache it instead of calling repeatedly.
- `freight_query_standard_price` — Query the standard base freight price for an SF Freight product between two addresses. At least one of weight, size, or declare_value is required for pricing.
- `freight_query_tl_order` — Query an SF Freight truckload order by client order number; pass waybill_no as well when you have it.
- `freight_register_ltl_picture_push` — Register an SF Freight waybill for waybill picture push. The picture push callback must be configured in the SF console before pushes arrive. [write]
- `freight_reply_work_order` — Reply to an SF Freight work order, identified by work_order_id or report_source_no (at least one). [write]
- `freight_report_work_order` — Report a work order (工单) about an SF Freight shipment to SF customer service. [write]
- `freight_supplier_apply_add_fee` — Apply for an add-fee on a bidding install order as the supplier (供应商侧发起增加费用). [write]
- `freight_supplier_query_add_fee_result` — Query the result of a supplier add-fee application (增加费用结果查询); the fallback when the result push or report fails.
- `freight_supplier_query_appointment_times` — Query the appointment times a supplier's master may offer for an install task (送装协同可预约时间).
- `freight_supplier_report_operation_node` — Report an install-task operation node to SF as the supplier (操作节点回传): assign master, pickup, appointment, arrival check, completion, review, fault detection, and more. Required fields depend on operate_code; images are required for codes 3, 17, 20, 21. [write]
- `freight_update_install_order` — Update an install order's customer info, non-SF logistics info, or cargo images. Customer and logistics info can only change before a master is assigned; cargo images can change until the waybill is signed. [write]
- `get_sub_waybill_nos` — Allocate additional child waybill numbers (子单号) for an existing SF Express order, at most 20 per call.
- `intercept_order` — Intercept, redirect, return, or adjust an in-transit SF Express waybill (截单转寄退回), for example redirecting it to a new address or returning it to the sender. Only for waybills already picked up; cancel an unshipped order with update_order instead. [destructive]
- `list_print_templates` — List a merchant's published custom print templates with their placeholder fields (ISV 自定义模板列表).
- `pre_order` — Validate whether an SF Express order would be accepted (预下单) — checks cargo, monthly card, address reachability, and number controls — without creating it, and returns the available service time windows.
- `print_waybill_cainiao_template` — Convert waybills into Cainiao print template URLs (云打印面单转菜鸟模板) for systems already integrated with the Cainiao print component.
- `print_waybill_command` — Convert waybills into printer command sets (云打印面单转指令, cpcl or zpl), returned inline as text or as downloadable files.
- `print_waybill_html` — Generate waybill HTML print files from a cloud print template (云打印面单转HTML). Returns download URLs that need the returned token in the X-Auth-token header (valid 24h). [write]
- `print_waybill_pdf` — Generate waybill PDF print files from a cloud print template (云打印面单转PDF). Returns download URLs that need the returned token in the X-Auth-token header (valid 24h). [write]
- `query_citywide_print_status` — Query the status and generated PDF files of a 大同城 citywide print batch.
- `query_delivery_time_price` — Query the SF Express delivery time standards for an origin and destination, optionally with freight prices per product.
- `query_order_result` — Query the processing result of a previously placed SF Express order, for example when the create_order response never arrived.
- `query_service_points` — List nearby SF Express service points (自营服务点, 合作商家店, 顺丰站, 丰巢柜, and more) around an address or a coordinate.
- `query_waybill_fee` — Query the freight fee breakdown (清单运费) of an SF Express shipment by order number (only orders placed under your partnerID) or by waybill number (the waybill's monthly card must be bound to your partnerID).
- `recommend_product` — Recommend SF Express products with prices and promised delivery times for a shipment.
- `recommend_vas` — Recommend value-added services (保鲜, 保价, 定时派送, and more) with prices for a shipment on a chosen product.
- `register_route_push` — Register an SF Express order or waybill for route (tracking) push. Prerequisite: the route push callback must already be configured in the SF console (控制台 → 开发者对接 → 查看API → 路由注册接口 → 配置信息); after registration, SF pushes route updates to that address. [write]
- `register_waybill_picture_push` — Register a waybill for waybill picture push (回单 receipt, 清单 manifest, 拍照回传 photo proof, etc.). SF pushes the AES-encrypted picture to the configured callback once generated; register after the shipment is signed for, because pictures are produced late. The decryption key comes from the SF console (控制台 → 开发者对接 → 查看API → 图片注册及推送接口). [write]
- `save_print_template` — Save a merchant custom print template (ISV 保存自定义模板); same name means a new version of the same template. The content follows the SF markup language spec. [write]
- `search_routes` — Query logistics routes (tracking events) for up to 10 SF Express shipments. Waybill-only queries return routes only for shipments paid with a monthly card bound to your partnerID; for any other shipment, pass the sender or recipient phone's last 4 digits in check_phone_nos. Only shipments from the last 3 months have routes.
- `send_delivery_notice` — Send a delivery or return notification for an SF Express waybill (派件通知), used in pre-sale scenarios where the goods were stocked in an SF warehouse in advance. [write]
- `station_add_brand_inspection_images` — Submit brand-inspection images for a station task (品牌巡检相册新增); resubmitting the same task_id updates its images. [write]
- `station_add_store_images` — Attach business-license, filing, or album image file names to an external station (外部驿站上传营业执照、末端备案、相册). [write]
- `station_batch_inventory` — Batch-upload the 600 route (滞留件盘点) for waybills held at a partner station. [write]
- `station_check_delivery_operation` — Check whether an operator on a channel may handle a waybill at a store (渠道可派件交接管控).
- `station_check_waybill` — Check whether a waybill is valid for external-station operations (外部驿站运单校验); an SF waybill without a recipient phone cannot receive station SMS.
- `station_courier_pickup_in_store` — Register that an SF courier picked up the consigned parcels from a store (顺丰小哥到店收件). [write]
- `station_customer_pickup_in_store` — Register that a customer picked up their parcel at a store (顾客到店取件). When receiver_payment is 1 (到付), weight, pack_fee, insurance_money, insurance_fee and successfully_payed_fee are required. [write]
- `station_customer_receive_pack` — Check out a waybill at an external station when the customer picks it up (外部驿站派件出库, route 658). [write]
- `station_customer_send_in_store` — Register a customer drop-off at a store (顾客到店寄件). When receiver_payment is 0 (寄付), weight, pack_fee, insurance_money and insurance_fee are required. [write]
- `station_get_oss_token` — Get an OSS token for direct image upload (获取OSSToken信息). The oss_client_name and path_id values come from your SF Express contact.
- `station_handle_exception_return` — Report an exception return for a waybill at an external station (驿站异常件退件处理). [write]
- `station_handover_pack` — Check in a delivery waybill at an external station (外部驿站派件入库, route 657). [write]
- `station_notify_recipient` — Send a pickup notification SMS to the recipient of a waybill held at a station. [write]
- `station_pre_handover_pack` — Pre-check-in a delivery waybill at an external station (外部驿站派件预入库) before the physical handover. [write]
- `station_query_centralization` — Query whether a waybill is a centralized (集收/集派) shipment through the station general query API.
- `station_query_grid_schedule` — Query the grid/bin assignment for a courier's shift at a station (星管家排班信息查询).
- `station_query_store_info` — Query a station's information. One of virtual_addr or store_code is required. The returned field names vary by api_version.
- `station_query_waybill_info` — Query a waybill's contact, payer and fee details (通用运单查询). Phone and address fields in the response are encrypted by SF Express.
- `station_query_waybill_route` — Query the route events of a waybill for the station channel.
- `station_save_store` — Create or update an external station (新增/修改外部驿站). Omit virtual_addr to create; pass it to update an existing station. [write]
- `station_save_village_store` — Create or update a township agent station (乡镇代理基本信息新增). [write]
- `station_save_xgj_store` — Create or update a 星管家 station's base information (星管家基本信息新增). [write]
- `station_send_sms` — Send a pickup-code SMS for a waybill from an external station (外部驿站发送短信). [write]
- `station_send_waybill_sms` — Send a fixed-template notification SMS for a waybill to its recipient or sender. [write]
- `station_store_batch_inventory` — Batch-upload the 600 route (滞留件盘点) for waybills held at a convenience store. [write]
- `station_store_handle_exception_return` — Report an exception return for a waybill at a store (门店异常件退件处理). [write]
- `station_store_receive_delivery` — Register that a store received parcels handed over by an SF courier (门店接收小哥派件). [write]
- `station_submit_fc_resource` — Submit or update a Hive Box service station's information (丰巢服务站信息接收或更新). [write]
- `station_submit_receipt_info` — Submit a waybill's receipt information with its fee, service, mark and addition lists (回单信息). [write]
- `station_temp_store` — Report a temporary station hold for a waybill (驿站暂存): bill_type 1 = 收端暂存 (route 410), 2 = 派端暂存 (route 210). [write]
- `station_update_outsource_info` — Submit or update the regional outsourcing information (区域外包信息变更) for outsourced station areas. [write]
- `station_update_xgj_insurance_fee` — Update a 星管家 station's monthly insurance fee (星管家保险费更新). [write]
- `station_update_xgj_waybill_fee` — Update a 星管家 waybill's dispatch and review-fee information (星管家运单及好评费更新). [write]
- `station_upload_fc_images` — Upload storefront and interior images for a Hive Box service station (丰巢服务站相册新增). [write]
- `station_upload_picture` — Upload one base64 image for a station (图片上传); the image must be at most 200 KB. [write]
- `station_upload_store_album` — Upload album images for a station (驿站相册新增), such as exterior, license, poster and signage photos. [write]
- `station_upload_village_store_images` — Upload the exterior and interior images for a township agent station (乡镇代理图片上传). [write]
- `station_upload_xgj_images` — Upload identity, face and property images for a 星管家 station (星管家相册新增); identity_file_names must contain exactly 2 images. [write]
- `station_upsert_cage_cabinet` — Create or update a cage cabinet (笼车柜); the sn field is the upsert key. [write]
- `station_upsert_fc_outsource_store` — Create or update a Hive Box regional-outsource store (丰巢区域外包门店新增及更新). [write]
- `station_upsert_robot_channel` — Create or update a robot/smart-cabinet channel station (渠道新增/修改). Omit virtual_addr when creating; pass it when updating. [write]
- `station_upsert_store_info` — Create or update a city station's base information (驿站基本信息新增/更新). When outsource_flag is 1, outsource_info is saved and required for 驿收发/丰巢 stores. [write]
- `station_upsert_ysf_outsource_store` — Create or update a 驿收发 regional-outsource store (驿收发区域外包门店新增及更新). [write]
- `station_validate_delivery_password` — Validate a customer's pickup password for a waybill at a partner station (验证取件密码).
- `station_verify_delivery_permission` — Check whether a channel and courier may deliver a waybill (派件管控). The channel code is allocated by SF (联系868850).
- `station_verify_fc_settlement` — Check whether a Hive Box (丰巢) cabinet drop-off fee settles monthly (丰巢订单结算校验, 订单类型 1 派件投柜). The rental and reservation order types carry different payloads and are not covered.
- `station_verify_waybill_number` — Check whether a waybill number is an SF Express waybill number, for the station channel.
- `submit_citywide_print` — Submit waybill print content for 大同城 citywide freight orders. Asynchronous by default: returns a print batch number to poll with sf_express.query_citywide_print_status; sync mode (max 20 documents) returns the files directly. [write]
- `update_order` — Confirm (deal_type confirm) or cancel (deal_type cancel) an SF Express order before shipment, optionally updating weight, volume, or the recipient address. Confirming requires the waybill numbers. A cancelled order number cannot be reused. [destructive]
- `validate_waybill_no` — Check whether a waybill number is a valid SF Express waybill number.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change SF Express state — confirm the exact payload and effect with the user before running.**
- **Actions tagged `[destructive]` remove or overwrite data — always confirm the target and get explicit approval first.**

## First-time setup

These are **one-time** steps — do not repeat them on every call. Run a step only when a command fails for the matching reason.

- **`oo: command not found`** — install the oo CLI (other platforms: <https://cli.oomol.com/install-guide.md>):

  ```bash
  curl -fsSL https://cli.oomol.com/install.sh | bash    # macOS / Linux
  ```

  ```powershell
  irm https://cli.oomol.com/install.ps1 | iex           # Windows PowerShell
  ```

- **Not signed in / authentication error** — sign in to your OOMOL account once:

  ```bash
  oo auth login
  ```

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — SF Express is not connected, or the connection expired or lacks a scope. Connect once (auth type: custom credential) at:

  ```text
  https://console.oomol.com/connections/sf_express
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- SF Express homepage: https://open.sf-express.com
