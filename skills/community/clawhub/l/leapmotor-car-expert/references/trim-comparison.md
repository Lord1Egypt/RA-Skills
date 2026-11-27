# 17 版本配置矩阵

**用法**：只放能追到来源的字段。写“未确认”是“资料未写”，不是“没有”。

**标记**：`†` 间接证据，`*` 媒体口径。带标记的值引用时必须一并说明，逐字段来源、状态与证据等级见 [`fact-records.json`](fact-records.json)。

**冲突**：数值冲突不在本表裁决，见 fact-records.json 的 `conflicts`。

**级别只作用于价格**，电池、芯片等字段各有独立状态，不继承价格级别。

<!-- MATRIX:BEGIN -->
**本区块由 `scripts/facts.py render` 从 [`fact-records.json`](fact-records.json) 生成，请勿手改。**

核对日期：2026-11-11。市场：中国。年款：2027 款。

**读表先看标记**：`†` = 间接证据（未直读原始页面）；`*` = 媒体口径；“未确认” = 资料没写，**不等于没有**；“未决” = 来源冲突未裁决。带标记的值请在引用时一并说明，逐字段来源见 [`fact-records.json`](fact-records.json)。

### C10（4 版）

| 版本键 | 版本 | 能源 | 指导价 | 级别 | CLTC | WLTC | 电池 | 电机 | 快充 | 慢充 | 整备 | 0–100 | 后备箱 |
|---|---|---|---:|---|---:|---:|---:|---|---:|---:|---:|---:|---|
| c10-290-zx | 290 智享版 | 增程 | 12.58 万 | L1 | 290 km | 190 km | 38.7 kWh | 200 kW／360 N·m | 约 16 分钟 | 3.5 h | 1995 kg | 7.38 s | 510–1809 L* |
| c10-290-lidar | 290 激光雷达版 | 增程 | 13.58 万 | L1 | 290 km | 190 km | 38.7 kWh | 200 kW／360 N·m | 约 16 分钟 | 3.5 h | 1995 kg | 7.38 s | 510–1809 L* |
| c10-660-zx | 660 智享版 | 纯电 | 13.28 万 | L1 | 660 km | — | 81.9 kWh | 230 kW／360 N·m | 约 16 分钟 | 7.5 h | 2040 kg | 6.02 s | 510–1809 L* |
| c10-660-lidar | 660 激光雷达版 | 纯电 | 14.28 万 | L1 | 660 km | — | 81.9 kWh | 230 kW／360 N·m | 约 16 分钟 | 7.5 h | 2040 kg | 6.02 s | 510–1809 L* |

### C11（5 版）

| 版本键 | 版本 | 能源 | 指导价 | 级别 | CLTC | 电池 | 电机 | 快充 | 慢充 | 整备 | 0–100 | 后备箱 | 轴距 |
|---|---|---|---:|---|---:|---:|---|---:|---:|---:|---:|---|---:|
| c11-300-lidar | 300 激光雷达版 | 增程 | 14.38 万† | L1* | 300 km† | 41.7 kWh† | 200 kW／320 N·m† | 约 18 分钟† | 4 h† | 2090 kg† | 7.6 s† | 485–1151 L† | 2930 mm |
| c11-300-zun | 300 激光雷达智尊版 | 增程 | 15.38 万† | L1* | 300 km† | 41.7 kWh† | 200 kW／320 N·m† | 约 18 分钟† | 4 h† | 2090 kg† | 7.6 s† | 485–1151 L† | 2930 mm |
| c11-640-zx | 640 智享版 | 纯电 | 14.38 万 | L1 | 640 km† | 81.9 kWh† | 220 kW／360 N·m† | 约 16 分钟† | 7.5 h† | 2110 kg† | 6.1 s† | 未决† | 2930 mm |
| c11-640-lidar | 640 激光雷达版 | 纯电 | 14.98 万 | L1 | 640 km† | 81.9 kWh† | 220 kW／360 N·m† | 约 16 分钟 | 7.5 h† | 2110 kg | 6.1 s | 未决† | 2930 mm |
| c11-640-zun | 640 激光雷达智尊版 | 纯电 | 15.98 万 | L1 | 640 km† | 81.9 kWh† | 220 kW／360 N·m† | 约 16 分钟 | 7.5 h† | 2110 kg | 6.1 s | 未决† | 2930 mm |

### C16（8 版）

| 版本键 | 版本 | 座位 | 能源 | 指导价 | 级别 | CLTC | WLTC | 电池 | 电机 | 快充 | 慢充 | 整备 | 0–100 | 后备箱 |
|---|---|---:|---|---:|---|---:|---:|---:|---|---:|---:|---:|---:|---|
| c16-280-zx-5 | 280 尊享版 | 5 | 增程 | 14.58 万 | L1 | 280 km | 185 km | 38.9 kWh | 200 kW／360 N·m | 约 16 分钟 | 3.5 h | 2120 kg | 8.3 s | 582／放倒 2077 L* |
| c16-280-zx-6 | 280 尊享版 | 6 | 增程 | 14.88 万 | L1 | 280 km | 185 km | 38.9 kWh | 200 kW／360 N·m | 约 16 分钟 | 3.5 h | 2120 kg | 8.3 s | 未决† |
| c16-280-lidar-5 | 280 激光雷达智尊版 | 5 | 增程 | 15.98 万 | L1 | 280 km | 185 km | 38.9 kWh | 200 kW／360 N·m | 约 16 分钟 | 3.5 h | 2120 kg | 8.3 s | 582／放倒 2077 L* |
| c16-280-lidar-6 | 280 激光雷达智尊版 | 6 | 增程 | 16.28 万 | L1 | 280 km | 185 km | 38.9 kWh | 200 kW／360 N·m | 约 16 分钟 | 3.5 h | 2120 kg | 8.3 s | 未决† |
| c16-630-zx-5 | 630 尊享版 | 5 | 纯电 | 15.28 万 | L1 | 630 km | — | 81.9 kWh† | 230 kW／360 N·m | 约 16 分钟 | 未确认 | 2160 kg | 6.8 s | 582／放倒 2077 L* |
| c16-630-zx-6 | 630 尊享版 | 6 | 纯电 | 15.58 万 | L1 | 630 km | — | 81.9 kWh† | 230 kW／360 N·m | 约 16 分钟 | 未确认 | 2160 kg | 6.8 s | 未决† |
| c16-630-lidar-5 | 630 激光雷达智尊版 | 5 | 纯电 | 16.68 万 | L1 | 630 km | — | 81.9 kWh† | 230 kW／360 N·m | 约 16 分钟 | 未确认 | 2160 kg | 6.8 s | 582／放倒 2077 L* |
| c16-630-lidar-6 | 630 激光雷达智尊版 | 6 | 纯电 | 16.98 万 | L1 | 630 km | — | 81.9 kWh† | 230 kW／360 N·m | 约 16 分钟 | 未确认 | 2160 kg | 6.8 s | 未决† |

### 字段证据提示（非直读或非确定）

下表列出主矩阵中**不能当作直读确定值**的字段。同一版本内按“证据/状态 + 来源”合并；完整逐字段来源见 [`fact-records.json`](fact-records.json)。

| 版本键 | 字段 | 状态/证据 | 来源 |
|---|---|---|---|
| c10-290-zx | adas_lidar | media / direct | `yiche-c10-review`、`sina-c10-advisor` |
| c10-290-zx | adas_chip、adas_sensor_count | unknown / indirect | —（无来源，不得作确定值） |
| c10-290-zx | cltc_pure_range、wltc_pure_range、seats、dimensions、motor_power_torque、fast_charge_30_80、curb_weight、accel_0_100 | confirmed / partial | `autohome-c10-config-2027` |
| c10-290-zx | battery_capacity、slow_charge | confirmed / partial | `yiche-c10-config-2027` |
| c10-290-zx | boot_capacity_l | media / partial | `yiche-c10-config-2027` |
| c10-290-lidar | cltc_pure_range、wltc_pure_range、seats、dimensions、motor_power_torque、fast_charge_30_80、curb_weight、accel_0_100 | confirmed / partial | `autohome-c10-config-2027` |
| c10-290-lidar | battery_capacity、slow_charge | confirmed / partial | `yiche-c10-config-2027` |
| c10-290-lidar | boot_capacity_l | media / partial | `yiche-c10-config-2027` |
| c10-660-zx | adas_lidar | media / direct | `yiche-c10-review`、`sina-c10-advisor` |
| c10-660-zx | adas_chip、adas_sensor_count | unknown / indirect | —（无来源，不得作确定值） |
| c10-660-zx | cltc_pure_range、seats、dimensions、motor_power_torque、fast_charge_30_80、curb_weight、accel_0_100 | confirmed / partial | `autohome-c10-config-2027` |
| c10-660-zx | battery_capacity、slow_charge | confirmed / partial | `yiche-c10-config-2027` |
| c10-660-zx | boot_capacity_l | media / partial | `yiche-c10-config-2027` |
| c10-660-lidar | cltc_pure_range、seats、dimensions、motor_power_torque、fast_charge_30_80、curb_weight、accel_0_100 | confirmed / partial | `autohome-c10-config-2027` |
| c10-660-lidar | battery_capacity、slow_charge | confirmed / partial | `yiche-c10-config-2027` |
| c10-660-lidar | boot_capacity_l | media / partial | `yiche-c10-config-2027` |
| c11-300-lidar | adas_lidar | media / direct | `official-c11-page-cn` |
| c11-300-lidar | guidance_price | L1* / indirect | `official-c11-page-cn`、`yiche-c11-config-2027` |
| c11-300-lidar | cltc_pure_range、battery_capacity、seats、dimensions、motor_power_torque、fast_charge_30_80、slow_charge、curb_weight 等 9 项 | confirmed / indirect | `yiche-c11-config-2027` |
| c11-300-lidar | boot_capacity_l | media / indirect | `yiche-c11-config-2027` |
| c11-300-lidar | adas_chip、adas_sensor_count | unknown / indirect | —（无来源，不得作确定值） |
| c11-300-zun | adas_lidar | media / direct | `official-c11-page-cn` |
| c11-300-zun | guidance_price | L1* / indirect | `official-c11-page-cn`、`yiche-c11-config-2027` |
| c11-300-zun | cltc_pure_range、battery_capacity、seats、dimensions、motor_power_torque、fast_charge_30_80、slow_charge、curb_weight 等 9 项 | confirmed / indirect | `yiche-c11-config-2027` |
| c11-300-zun | boot_capacity_l | media / indirect | `yiche-c11-config-2027` |
| c11-300-zun | adas_chip、adas_sensor_count | unknown / indirect | —（无来源，不得作确定值） |
| c11-640-zx | adas_lidar | media / direct | `autohome-c11-guide-2027` |
| c11-640-zx | cltc_pure_range、battery_capacity、seats、dimensions、motor_power_torque、fast_charge_30_80、slow_charge、curb_weight 等 9 项 | confirmed / indirect | `yiche-c11-config-2027` |
| c11-640-zx | boot_capacity_l | conflict / indirect | —（无来源，不得作确定值） |
| c11-640-zx | adas_chip、adas_sensor_count | unknown / indirect | —（无来源，不得作确定值） |
| c11-640-lidar | cltc_pure_range、battery_capacity、motor_power_torque、slow_charge | confirmed / indirect | `yiche-c11-config-2027` |
| c11-640-lidar | boot_capacity_l | conflict / indirect | —（无来源，不得作确定值） |
| c11-640-lidar | seats、dimensions、fast_charge_30_80、curb_weight、accel_0_100、adas_lidar、adas_chip、adas_sensor_count | confirmed / partial | `autohome-c11-config-2027` |
| c11-640-zun | cltc_pure_range、battery_capacity、motor_power_torque、slow_charge | confirmed / indirect | `yiche-c11-config-2027` |
| c11-640-zun | boot_capacity_l | conflict / indirect | —（无来源，不得作确定值） |
| c11-640-zun | seats、dimensions、fast_charge_30_80、curb_weight、accel_0_100、adas_lidar、adas_chip、adas_sensor_count | confirmed / partial | `autohome-c11-config-2027` |
| c16-280-zx-5 | boot_capacity_l | media / direct | `sina-c16-2027` |
| c16-280-zx-5 | wheelbase | confirmed / indirect | `weixin-c16-guide` |
| c16-280-zx-5 | adas_lidar | media / indirect | `weixin-c16-guide` |
| c16-280-zx-5 | adas_chip、adas_sensor_count | unknown / indirect | —（无来源，不得作确定值） |
| c16-280-zx-5 | cltc_pure_range、wltc_pure_range、battery_capacity、seats、dimensions、motor_power_torque、fast_charge_30_80、slow_charge 等 10 项 | confirmed / partial | `autohome-c16-config-2027` |
| c16-280-zx-6 | wheelbase | confirmed / indirect | `weixin-c16-guide` |
| c16-280-zx-6 | boot_capacity_l | conflict / indirect | —（无来源，不得作确定值） |
| c16-280-zx-6 | adas_lidar | media / indirect | `weixin-c16-guide` |
| c16-280-zx-6 | adas_chip、adas_sensor_count | unknown / indirect | —（无来源，不得作确定值） |
| c16-280-zx-6 | cltc_pure_range、wltc_pure_range、battery_capacity、seats、dimensions、motor_power_torque、fast_charge_30_80、slow_charge 等 10 项 | confirmed / partial | `autohome-c16-config-2027` |
| c16-280-lidar-5 | boot_capacity_l | media / direct | `sina-c16-2027` |
| c16-280-lidar-5 | wheelbase | confirmed / indirect | `weixin-c16-guide` |
| c16-280-lidar-5 | adas_lidar、adas_chip | media / indirect | `weixin-c16-guide` |
| c16-280-lidar-5 | adas_sensor_count | unknown / indirect | —（无来源，不得作确定值） |
| c16-280-lidar-5 | cltc_pure_range、wltc_pure_range、battery_capacity、seats、dimensions、motor_power_torque、fast_charge_30_80、slow_charge 等 10 项 | confirmed / partial | `autohome-c16-config-2027` |
| c16-280-lidar-6 | wheelbase | confirmed / indirect | `weixin-c16-guide` |
| c16-280-lidar-6 | boot_capacity_l | conflict / indirect | —（无来源，不得作确定值） |
| c16-280-lidar-6 | adas_lidar、adas_chip | media / indirect | `weixin-c16-guide` |
| c16-280-lidar-6 | adas_sensor_count | unknown / indirect | —（无来源，不得作确定值） |
| c16-280-lidar-6 | cltc_pure_range、wltc_pure_range、battery_capacity、seats、dimensions、motor_power_torque、fast_charge_30_80、slow_charge 等 10 项 | confirmed / partial | `autohome-c16-config-2027` |
| c16-630-zx-5 | boot_capacity_l | media / direct | `sina-c16-2027` |
| c16-630-zx-5 | wheelbase | confirmed / indirect | `weixin-c16-guide` |
| c16-630-zx-5 | battery_capacity、adas_lidar | media / indirect | `weixin-c16-guide` |
| c16-630-zx-5 | slow_charge、adas_chip、adas_sensor_count | unknown / indirect | —（无来源，不得作确定值） |
| c16-630-zx-5 | cltc_pure_range、seats、dimensions、motor_power_torque、fast_charge_30_80、curb_weight、accel_0_100 | confirmed / partial | `autohome-c16-config-2027` |
| c16-630-zx-6 | wheelbase | confirmed / indirect | `weixin-c16-guide` |
| c16-630-zx-6 | boot_capacity_l | conflict / indirect | —（无来源，不得作确定值） |
| c16-630-zx-6 | battery_capacity、adas_lidar | media / indirect | `weixin-c16-guide` |
| c16-630-zx-6 | slow_charge、adas_chip、adas_sensor_count | unknown / indirect | —（无来源，不得作确定值） |
| c16-630-zx-6 | cltc_pure_range、seats、dimensions、motor_power_torque、fast_charge_30_80、curb_weight、accel_0_100 | confirmed / partial | `autohome-c16-config-2027` |
| c16-630-lidar-5 | boot_capacity_l | media / direct | `sina-c16-2027` |
| c16-630-lidar-5 | wheelbase | confirmed / indirect | `weixin-c16-guide` |
| c16-630-lidar-5 | battery_capacity、adas_lidar、adas_chip | media / indirect | `weixin-c16-guide` |
| c16-630-lidar-5 | slow_charge、adas_sensor_count | unknown / indirect | —（无来源，不得作确定值） |
| c16-630-lidar-5 | cltc_pure_range、seats、dimensions、motor_power_torque、fast_charge_30_80、curb_weight、accel_0_100 | confirmed / partial | `autohome-c16-config-2027` |
| c16-630-lidar-6 | wheelbase | confirmed / indirect | `weixin-c16-guide` |
| c16-630-lidar-6 | boot_capacity_l | conflict / indirect | —（无来源，不得作确定值） |
| c16-630-lidar-6 | battery_capacity、adas_lidar、adas_chip | media / indirect | `weixin-c16-guide` |
| c16-630-lidar-6 | slow_charge、adas_sensor_count | unknown / indirect | —（无来源，不得作确定值） |
| c16-630-lidar-6 | cltc_pure_range、seats、dimensions、motor_power_torque、fast_charge_30_80、curb_weight、accel_0_100 | confirmed / partial | `autohome-c16-config-2027` |

### 冲突（未决，不取中值）

| 冲突 | 字段 | 涉及版本 | 各方主张 | 状态 |
|---|---|---|---|---|
| c16-boot-6 | boot_capacity_l | c16-280-zx-6、c16-280-lidar-6、c16-630-zx-6、c16-630-lidar-6 | 275 L／放倒 1066 L（`sina-c16-2027`）；209 L／放倒 1022 L（`youjia-c16-conflict-sample`） | unresolved |
| c11-boot-纯电 | boot_capacity_l | c11-640-zx、c11-640-lidar、c11-640-zun | 537–1203 L（`autohome-c11-config-2027`）；523 L（`modiauto-c11-14799`） | unresolved |
| c10-ar-hud | ar_hud_60in | c10-290-zx、c10-290-lidar、c10-660-zx、c10-660-lidar | 仅激光雷达版增加 60 英寸 AR-HUD（`yoojia-c10-trim-diff`、`zjchewang-c10-discount`）；全系标配 60 英寸 AR-HUD（`sina-c10-2027`）；官方页列于座舱亮点，未限定版本（`official-c10-page`） | unresolved |

### 数据完整性（程序计算）

| 项目 | 结果 |
|---|---|
| 版本数 | 17 |
| 事实记录 | 261 条 |
| 价格级别 | L1 15 个，L1* 2 个 |
| 未确认 | 26 条 |
| 争议未决 | 7 条（3 组冲突） |
| 非直读证据 | 222 条 |

