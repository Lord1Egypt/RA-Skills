# PlantUML / mxGraph 图标索引

> Agent 画云架构/网络拓扑/BPMN/工业流程图时，按 namespace 查找精确图标名。
> 总计 9574 个图标，61 个 namespace 文件。

## 使用方法

在 PlantUML 代码中引用图标：
```
!include <namespace/icon_name>
```
例如：`!include <aws4/lambda>` 或 `!include <kubernetes/deploy>`

在 draw.io XML 中引用 mxGraph stencil：
```
style="shape=mxgraph.namespace.icon_name"
```

---

## AWS4 (1035 icons) ⭐ 最常用

**分类**：Compute / Database / Storage / Networking / Security / Analytics / ML / IoT / Management / Migration / Containers / Serverless

**常用图标（Top 30）**：
lambda, ec2, s3, rds, dynamodb, cloudfront, api_gateway, ecs, eks, sqs, sns, kinesis, redshift, elasticache, route_53, vpc, elastic_load_balancing, cloudwatch, step_functions, sagemaker, fargate, eventbridge, cognito, aurora, efs_standard, elastic_block_store, cloudformation, codepipeline, secrets_manager, bedrock

**Compute**: ec2, lambda, fargate, elastic_beanstalk, batch, outposts, lightsail, app_runner
**Database**: rds, dynamodb, aurora, elasticache, neptune, redshift, documentdb_with_mongodb_compatibility, memorydb_for_redis, keyspaces
**Storage**: s3, elastic_block_store, elastic_file_system, glacier, fsx, backup, s3_object_lambda
**Networking**: vpc, cloudfront, route_53, elastic_load_balancing, api_gateway, direct_connect, transit_gateway, global_accelerator, vpn_gateway, network_firewall
**Containers**: ecs, eks, ecr, fargate, app_mesh, ecs_anywhere
**ML/AI**: sagemaker, bedrock, rekognition, comprehend, textract, polly, lex, personalize, forecast, kendra
**Security**: identity_and_access_management, cognito, guardduty, inspector, waf, shield, secrets_manager, certificate_manager, security_hub
**Serverless**: lambda, step_functions, eventbridge, sqs, sns, api_gateway, dynamodb, s3

---

## AWS (legacy, 100 icons)

旧版AWS图标，建议优先用 aws4。
**常用**：compute.ec2, compute.lambda, database.rds, database.dynamodb, storage.s3, content_delivery.cloudfront, messaging.sqs, messaging.sns

---

## GCP2 (323 icons)

**分类**：AI & ML / Compute / Data Analytics / Databases / Networking / Security / Storage / Serverless

**常用图标**：
cloud_run, cloud_functions, compute_engine, gke, bigquery, cloud_storage, cloud_sql, pubsub, cloud_cdn, cloud_load_balancing, cloud_armor, vertex_ai, cloud_spanner, firestore, memorystore, cloud_nat, cloud_dns, artifact_registry, cloud_build, secret_manager

---

## Azure (90 icons)

**常用**：azure_active_directory, azure_load_balancer, azure_cache, azure_instance, automation, autoscale, azure_website, backup_service, cloud, certificate

---

## Kubernetes (42 icons)

**常用**：deploy, pod, svc, ing, cm, ns, pv, pvc, ds, sts, job, cronjob, hpa, sc, sa, role, c_role, crb, ep, etcd, k_proxy, kubelet, c_c_m, c_m, node, frame, group

---

## Cisco (297 icons)

**分类**：Buildings / Computers / Controllers / Hubs / Misc / Modems / People / Phones / Routers / Security / Servers / Storage / Switches / Wireless

**常用**：routers.router, switches.workgroup_switch, servers.standard_server, wireless.access_point, security.firewall, security.vpn_concentrator, controllers.wireless_lan_controller, storage.storage_server

---

## Cisco SAFE (486 icons)

专业安全架构图标，覆盖 Capability / Composit / Design / Threat / Policy / Icon

---

## Rack (488 icons)

机架图标，按厂商分：APC / Cisco / Dell / HP / IBM / Oracle
**常用**：cisco.cisco_2901_integrated_services_router, hp.hp_proliant_dl360, dell.dell_poweredge_t630, ibm.ibm_bladecenter_t_chassis

---

## Electrical (643 icons)

**分类**：Abstract / Capacitors / Diodes / Inductors / Instrument / Logic Gates / Opamps / Resistors / Signal Sources / Switches / Transistors / Transmission / Waveforms

**常用**：resistors.resistor, capacitors.capacitor, diodes.diode, transistors.nmos, transistors.pmos, logic_gates.and, logic_gates.or, logic_gates.not, signal_sources.vdc, signal_sources.ac_source

---

## BPMN (184 icons)

**分类**：Tasks / Events / Gateways / Data / Conversations / Choreography

**常用**：business_rule_task, user_task, service_task, send_task, receive_task, script_task, exclusive_gateway, parallel_gateway, inclusive_gateway, event_based_gateway, timer_intermediate, message_start, message_end, error_end, signal_intermediate

---

## PID (480 icons) — 工艺流程图

**分类**：Agitators / Centrifuges / Compressors / Dryers / Engines / Fans / Filters / Heat_Exchangers / Instruments / Mixers / Piping / Pumps / Separators / Tanks / Valves / Vessels

**常用**：valves.gate_valve, valves.globe_valve, valves.check_valve, pumps.centrifugal_pump, instruments.flow_indicator, instruments.temperature_indicator, heat_exchangers.shell_and_tube, tanks.tank, vessels.pressure_vessel

---

## Office (450 icons) — Microsoft 365

**分类**：Clouds / Communications / Concepts / Databases / Devices / Security / Servers / Services / Sites / Users

**常用**：clouds.office_365, clouds.azure, servers.application_server, servers.database_server, servers.web_server, security.lock_with_key, users.user, communications.chat_room, databases.database

---

## Veeam (334 icons) + Veeam2 (248 icons)

备份和容灾架构图标。
**常用 2D**：agent, backup_repository, backup_from_storage_snapshots, cloud, datastore, endpoint, proxy, tape, vm, wan_accelerator
**常用 3D**：1u_server, agent, backup_browser, cloud, monitor, nas, proxy, server, tape_library, vm_linux, vm_windows

---

## Signs (370 icons)

**分类**：Animals / Food / Healthcare / Nature / People / Safety / Science / Sports / Tech / Transportation / Travel

通用标识图标，适合非技术性图表装饰。

---

## Salesforce (97 icons)

**分类**：Analytics / Apps / Automation / Bots / Commerce / Communications / Data / Education / Marketing / Platform / Service

---

## Alibaba Cloud (311 icons)

阿里云架构图标，覆盖 Compute / Storage / Network / Database / Security / Analytics

---

## 其他 Namespace（按需使用）

| Namespace | 图标数 | 适用场景 |
|-----------|--------|---------|
| `mscae` | 369 | Microsoft Azure Enterprise 架构 |
| `fluid_power` | 247 | 液压/气动系统图 |
| `cisco19` | 234 | Cisco 新版图标 |
| `weblogos` | 179 | 品牌/公司 Logo |
| `webicons` | 177 | Web UI 图标 |
| `floorplan` | 76 | 平面布局/办公室 |
| `android` | 50 | Android UI 元素 |
| `archimate` | 11 | ArchiMate 企业架构 |
| `lean_mapping` | ~30 | 精益价值流图 |
| `dfd` | 6 | 数据流图 |
| `sitemap` | ~30 | 站点地图 |
| `mockup` | ~60 | UI 线框原型 |
| `vvd` | ~20 | VMware VVD |

---

## 查找技巧

1. **不确定图标名**时：按分类缩小范围，再用关键词猜测（图标名通常是 `下划线分隔的英文描述`）
2. **AWS 优先用 aws4**（最新最全），旧版 aws/aws2/aws3 仅在特殊情况使用
3. **云架构图**：aws4 + gcp2 + azure 三选一或混用
4. **企业内部架构**：office + cisco + rack 组合
5. **工业/制造**：pid + electrical + fluid_power
