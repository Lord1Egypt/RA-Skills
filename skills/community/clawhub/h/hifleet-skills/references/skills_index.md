# 技能清单 / Skills Index

中英双语。

---

## 1. 船位 / Ship Position ✅

| 中文 | 英文 |
|------|------|
| 名称 | 船位 / Ship Position |
| 描述 | 查询船舶实时或历史位置，支持 AIS 报位、锚位、靠泊等。 |
| 触发词 | 船位、位置、报位、在哪、AIS 位置 / ship position, vessel position, location, AIS position, where is |

## 2. 档案 / Archive ✅

| 中文 | 英文 |
|------|------|
| 名称 | 档案 / Archive (Vessel Profile) |
| 描述 | 船舶与公司档案：船籍、船型、建造年份、船东、管理公司等。按 IMO 查询。 |
| 触发词 | 档案、船舶信息、船籍、船型、船东、管理公司 / archive, vessel profile, ship info, flag, ship type, owner, manager |

## 3. 红海/波斯湾海峡通航 / Strait Traffic ✅

| 中文 | 英文 |
|------|------|
| 名称 | 红海/波斯湾海峡通航 / Strait Traffic |
| 描述 | 咽喉航道通航船舶统计：曼德、苏伊士、好望角、霍尔木兹；POST 接口；无 `api_key` 限最近 1 周，有 `api_key` 时间不限。 |
| 触发词 | 红海、波斯湾、海峡通航、曼德、苏伊士、好望角、霍尔木兹 / Red Sea, Persian Gulf, strait traffic, Suez, Cape of Good Hope, Hormuz |

## 4. 区域船舶 / Area Traffic ✅

| 中文 | 英文 |
|------|------|
| 名称 | 区域船舶 / Area Traffic |
| 描述 | 查询指定区域内的当前船舶列表，需 `api_key`；支持 bbox（左下/右上经纬度）、areaId（区域清单 id）或 polygon（WKT 多边形）。用户仅文字描述区域时可先查区域清单（海区/贸易区），按 name/cnName 匹配得到 id 再查询。 |
| 触发词 | 区域船舶、范围内船舶、区域船位、某区域有多少船、红海船舶、北太平洋船位 / area traffic, vessels in area, ships in region |

## 5. PSC 检查 / PSC Inspection ✅

| 中文 | 英文 |
|------|------|
| 名称 | PSC 检查 / PSC Inspection（港口国监督） |
| 描述 | 顺序：**单船 PSC**（按 IMO，船名需先搜船取 IMO）→ **统计异常**（`psc_anomaly_event`，见 [psc_anomaly_api.md](psc_anomaly_api.md)）→ **宏观统计**（区间对比/缺陷 Top/占比对比，见 [psc_openclaw_stats_api.md](psc_openclaw_stats_api.md)）。均需 `api_key`。 |
| 触发词 | **单船**：PSC、港口国监督、港口国检查、滞留、缺陷、检查记录 / port state control, PSC inspection, detention, deficiency, inspection record。**统计异常/宏观统计**：PSC 异常、统计异常、滞留率飙升、缺陷异常、哪国变严、旗国风险、港口风险、缺陷热点、PSC anomaly、detention spike、deficiency spike, PSC statistics |

**统计异常子能力（均需 `api_key`）**

| 子能力 | 说明 |
|--------|------|
| 异常列表 | 分页查询 `openclaw/anomalies`，可选日期、当局、旗国、港口、严重度等 |
| 严重度汇总 | `openclaw/anomalies/summary`，先答 HIGH/MEDIUM/LOW 条数 |
| 单条详情 | `openclaw/anomalies/{id}`，展开描述与 evidence |

脚本：`scripts/get_psc_anomalies.py`（`list` / `summary` / `get <id>`）。接口 URL 使用 `{base}`（默认 `https://api.hifleet.com`，可设 `HIFLEET_API_BASE`）。

**字段语义（OpenClaw 必读）**  
- **`authority`**：上述 PSC 统计相关表中均为 **检查国/检查当局**，**不是**船舶注册国；船旗国为 **`flag`**。  
- **`shipType` / `ship_type`**：在含该维度的表中均为 **检查类型（`type_ins`）**，**不是**船型。  
完整表清单与话术：[psc_stats_field_semantics.md](psc_stats_field_semantics.md)。

**数据稀疏（异常表条数很少或为空）**  
OpenClaw **不得**据此断言「无 PSC 风险」；应说明仅为「异常事件表」在当前条件下无命中或样本极少，并引导：放宽筛选/日期、核对当局与旗国等是否与库内一致、或改用单船 `pscapi/get`。详见 [psc_anomaly_api.md](psc_anomaly_api.md) 专节。

## 6. 港口指南 / Port guide ✅

| 中文 | 英文 |
|------|------|
| 名称 | 港口指南 / Port guide |
| 描述 | **列表**：`GET {base}/portguide/getPort/token`，可选 `portName`、`portCode`。**详情**：`GET {base}/portguide/getPortDetail/token`，`portId` 取列表项 **`piuid`**。需 `api_key`。 |
| 触发词 | 港口、港名、港口代码、泊位、锚地、港口信息、UN/LOCODE / port, port name, port code, berth, anchorage, port info, UN/LOCODE |

**API**：[port_api.md](port_api.md)。**脚本**：`scripts/get_port.py search [--port-name] [--port-code]`、`scripts/get_port.py detail <portId>`（portId 为列表中的 piuid）。

## 7. 性能 / Performance

| 中文 | 英文 |
|------|------|
| 名称 | 性能 / Performance |
| 描述 | 航速、油耗、主机负荷、能效（EEOI）及性能报告。 |
| 触发词 | 性能、油耗、航速、主机、能效、EEOI / performance, fuel consumption, speed, main engine, EEOI, efficiency |

## 8. 航程 / Voyage ✅（部分）

| 中文 | 英文 |
|------|------|
| 名称 | 航程 / Voyage |
| 描述 | OpenClaw 单船航程：**历史轨迹**（`{base}/position/trajectory/token`）、**历史挂靠**（`{base}/position/getcallport/token`）、**历史航次**（`{base}/position/getvoyagelist/token` / `{base}/portofcall/getvoyages`）、**上一港**（`{base}/position/lastdeparture/token`）、**当前停船**（`{base}/position/getstop/token`）。均需 `api_key`；无 MMSI 时先 `shipSearch`。 |
| 触发词 | 历史轨迹、轨迹回放、航行路线、历史挂靠、靠港记录、挂港、历史航次、航次列表、上一港、上次离港、当前停船、停在哪 / track history, trajectory, port call history, voyage history, last departure, current stop, stopped at port |

**API**：[voyage_api.md](voyage_api.md)

## 9. 航线 / Route

| 中文 | 英文 |
|------|------|
| 名称 | 航线 / Route |
| 描述 | 推荐航线、航路点、距离与航时、历史航线对比。 |
| 触发词 | 航线、航路、推荐航线、距离、航时、航路点 / route, shipping route, recommended route, distance, sailing time, waypoint |

## 10. 租船 / Charter ✅

| 中文 | 英文 |
|------|------|
| 名称 | 租船 / Charter |
| 描述 | `hifleet-skills` 内置租船模块（分册 `hifleet-mytonnages/`）：A 邮件船货盘；B 班轮船期；C 预抵船舶。**B/C 列表须全量返回**（`FULL_LIST_POLICY.md`）。邮件需邮箱与记忆；B/C 及 A 补充信息需 `hifleet_api_key` 或 `HIFLEET_API_KEY`。 |
| 触发词 | 租船、船盘、货盘、船期、预抵、即将到港、ETA / charter, open vessel, cargo, schedule, charter party, hire, period, line |

**路由**：A=邮件里；B=班轮船期；C=预抵船舶。详见 `hifleet-mytonnages/ROUTING_AND_WHEN.md`。

## 11. 航运 / Shipping

| 中文 | 英文 |
|------|------|
| 名称 | 航运 / Shipping |
| 描述 | 运价、运力、市场动态、船舶买卖、航运新闻与行业数据。 |
| 触发词 | 航运、运价、运力、市场、买卖、航运新闻 / shipping, freight rate, tonnage, market, sale and purchase, shipping news |

## 12. 气象海况 / Weather & Sea Conditions

| 中文 | 英文 |
|------|------|
| 名称 | 气象海况 / Weather & Sea Conditions |
| 描述 | 风、浪、涌、能见度、台风/气旋路径及航行气象建议。 |
| 触发词 | 气象、海况、风、浪、台风、能见度 / weather, sea conditions, wind, wave, typhoon, visibility |

## 13. 船队 / Fleet

| 中文 | 英文 |
|------|------|
| 名称 | 船队 / Fleet |
| 描述 | 多船监控、船队分布、统计、报警汇总及船队报表。 |
| 触发词 | 船队、多船、船队分布、船队统计、船队报表 / fleet, multi-vessel, fleet distribution, fleet statistics, fleet report |

## 14. AIS

| 中文 | 英文 |
|------|------|
| 名称 | AIS |
| 描述 | AIS 报文、船舶识别、动态/静态数据、轨迹回放与导出（历史轨迹见 **航程 / Voyage**）。 |
| 触发词 | AIS、报文、MMSI、AIS 数据 / AIS, message, MMSI, AIS data |

---

建议实现顺序：船位 → AIS → 档案 → PSC → 港口指南 → 租船 → 航程 → 航线 → 性能 → 气象海况 → 船队 → 航运。
