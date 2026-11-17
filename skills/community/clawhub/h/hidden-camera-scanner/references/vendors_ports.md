# 监控厂商 / 可疑端口 / 蓝牙追踪器签名与判定规则

本文件供 skill 在解读扫描结果、给结论时引用。所有签名均来自公开资料，已在各条目标注来源。

## 1. 监控设备厂商关键字（用于匹配 nmap 的 MAC 厂商字段）

局域网扫描中，nmap 会给出设备的 MAC 厂商名。下列关键字命中即标记 `vendor_suspect=true`（仍需结合端口与场景判断，不等于偷拍）。

| 关键字（不区分大小写） | 厂商 | 备注 |
|---|---|---|
| Hikvision / 海康威视 / Hangzhou Hikvision | 海康威视 | 最常见监控厂商 |
| Dahua / 大华 | 浙江大华 | 私有协议端口 34567/37777 |
| Reolink | Reolink | 消费级 PoE/WiFi 摄像头 |
| Axis | Axis Communications | 企业级网络摄像头 |
| EZVIZ / 萤石 | 海康旗下消费品牌 | |
| IMOU / 乐橙 | 大华旗下消费品牌 | |
| Uniview / 宇视 / UNV | 宇视科技 | |
| TP-LINK | 普联（含安防系列） | 也做路由器，需结合端口 |
| Xiaomi / 小米 / Mi Home | 小米（含摄像头） | |
| D-Link | 友讯 | |
| Foscam | 福斯康姆 | |
| Yi / 小蚁 | 小蚁 | |
| Amcrest | Amcrest | |
| Wyze | Wyze | |
| Lorex / Swann / Tend / Wansview / Tenvis | 各消费监控品牌 | |
| GeoVision / 奇偶、Vivotek / 台达、Mobotix、Hanwha / 三星安防、Bosch、Panasonic、Sony、Netatmo、Nest | 各类监控/安防厂商 | |

> 注：仅列常见项，非穷举。无 nmap（靠 MAC OUI 回退）时，厂商识别能力弱，应明确提示「建议安装 nmap 以获得准确厂商识别」。

## 2. 可疑端口表（用于端口扫描标记）

| 端口 | 协议 | 服务 | 与监控的关联 |
|---|---|---|---|
| 554 | TCP | RTSP | 实时视频流，监控摄像头**最常见**开放端口 |
| 8554 | TCP | RTSP 备用 | RTSP 备选端口 |
| 3702 | UDP | ONVIF WS-Discovery | 监控设备发现协议，开放即高度疑似监控设备 |
| 80 / 8080 | TCP | HTTP Web 管理 | 摄像头/ NVR 管理界面 |
| 443 | TCP | HTTPS | 管理界面/视频 |
| 8000 | TCP | 海康威视 ISAPI/SDK | 海康设备特征端口 |
| 34567 / 37777 | TCP | 大华私有协议 | 大华设备特征端口 |
| 8899 | TCP | 大华/通用 | 部分摄像头 |
| 23 | TCP | Telnet | 老旧摄像头常暴露，高危 |
| 21 | TCP | FTP | 录像文件传输 |
| 1900 | UDP | UPnP/SSDP | 设备发现 |
| 9999 / 49152 | TCP | 各厂商私有 | 部分 NVR/摄像头 |

**判定**：开放 `554/8554/3702/8000/34567/37777` 中任一即高可疑；同时厂商命中监控关键字则更高危。

## 3. 蓝牙追踪器广播签名（已核实来源）

来源汇总：Apple AirTag 逆向 (adamcatley.com)、AirTag 检测项目 (Itheras/AirFlag, nitekry/airtag-recon)、Bluetooth SIG 分配号、Network Survey 文档、VIGIL 论文 (KaraZajac)。

| 追踪器 | 判定签名 | 注意事项 |
|---|---|---|
| Apple AirTag / Find My | 厂商数据 `company_id=0x004C` 且 payload 首字节 `0x12`（Find My 网络广播；未注册态为 `0x07`） | **不能**仅凭 `0x004C` 判定——iPhone/Mac 也用 `0x004C` 做 Handoff 等。必须要求 `0x12` 类型。MAC 由公钥派生，约每天轮换、分离态约每 15 分钟轮换。 |
| Samsung SmartTag / SmartTag2 | 服务 UUID `0000fd5a-...`（SmartTag 服务） | 厂商 `0x0075`(Samsung) 出现在所有三星设备，**非标签独有**，故以服务 UUID `0xFD5A` 为锚。 |
| Tile | 服务数据 UUID `0000feed`(已激活)/`0000feec`(未激活)/`0000fe84`(旧版)，或厂商 `0x02E5`(Tile)；设备名含 "tile" | Tile MAC **永不轮换**，最易跨轮关联；无「分离态」信标。 |
| Google FMDN / Find Hub | 服务 UUID `0000feaa`(Eddystone)，service-data 首字节 `0x40`(正常)/`0x41`(分离/防追踪) | 厂商 `0x00E0`(Google)。 |
| Chipolo（原生模式） | 厂商 `0x0133`(Chipolo d.o.o.) | 若配对接入 Apple/Google 网络，则表现为对应网络签名。 |
| DULT（统一防追踪，新兴） | 服务 UUID `0000fcb2` | 前向兼容，解析 near-owner 位。 |

**地址轮换分析**：同一广播签名（厂商数据/服务 UUID 组合的稳定片段）在多次扫描中换用不同 MAC 出现 → 标记为 `rotating_address_suspect`（高度疑似追踪器，因其刻意隐藏物理地址）。iPhone 等正常设备也可能轮换，但一般不同时满足「无设备名 + 固定 Find My/追踪器签名」。

## 4. 风险分级规则（generate_report.py 使用）

- **高危**：开放 RTSP/ONVIF/厂商私有端口 且 厂商命中监控关键字；或蓝牙发现稳定的 Find My/SmartTag/Tile 签名且地址轮换。
- **中危**：厂商命中监控关键字但无监控端口；或开放单一 Web 管理端口无可疑厂商；或蓝牙发现追踪器签名但 RSSI 极弱/仅单次。
- **低危/提示**：仅发现本机与网关（疑似客户端隔离）；或发现未知厂商设备但有合理用途（手机/笔记本/电视）。
- **未检出**：本轮扫描未发现可疑设备——但必须附「扫描局限」说明（蜂窝/其他 Wi-Fi/纯本地存储摄像头不可见）。
