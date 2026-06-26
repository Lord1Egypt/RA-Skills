# 设备 MIoT 属性映射 / Device MIoT Property Catalog (中文/English)

> 通过 `python -m mijiaAPI --get_device_info <model>` 可获取完整属性列表
> Full property list via `python -m mijiaAPI --get_device_info <model>`

## 米家智能插座3 / Mijia Smart Plug 3 (cuco.plug.v3)

| 属性 / Property | siid | piid | 值说明 / Values |
|---|---|---|---|
| 开关 / Power | 2 | 1 | 0=关/off, 1=开/on |
| 功率 / Power (W) | 2 | 2 | 只读 / read-only |
| LED 开关 / LED | 6 | 1 | 0=关/off, 1=开/on |

## 小爱音箱Art / Mi Smart Speaker Art II (xiaomi.wifispeaker.l09b)

| 属性 / Property | siid | piid | 值说明 / Values |
|---|---|---|---|
| 电源 / Power | 2 | 1 | 0=关/off, 1=开/on |

## Redmi小爱触屏音箱8 / Redmi Smart Display 8inch (xiaomi.wifispeaker.x08c)

| 属性 / Property | siid | piid | 值说明 / Values |
|---|---|---|---|
| 电源 / Power | 2 | 1 | 0=关/off, 1=开/on |

## 小米智能摄像机4 / Xiaomi Smart Camera 4 (chuangmi.camera.079ac1)

| 属性 / Property | siid | piid | 值说明 / Values |
|---|---|---|---|
| 电源 / Power | 2 | 1 | 0=关/off, 1=开/on |

## 温湿度计 / Temp & Humidity Monitor (Mijia Smart Temp & Humidity Monitor 3)

| 属性 / Property | siid | piid | 值说明 / Values |
|---|---|---|---|
| 温度 / Temperature | 3 | 1 | 只读(°C) / read-only |
| 湿度 / Humidity | 3 | 2 | 只读(%) / read-only |
| 电池 / Battery | 3 | 3 | 只读(%) / read-only |
