# UDI全球标识枢纽

> 医疗器械注册工程师资料枢纽 · 由 WorkBuddy 生成，链接均指向官方源，点击可直达。

---

# UDI 全球标识枢纽

  每个出厂产品都要贴 UDI。本枢纽汇总中国 / 美国 / 欧盟 / 日本 四套体系的编码规则、数据库录入入口、DI/PI 模板与实施时间表，所有官方入口均可点击直达。适用于注册、质量、供应链全岗位。

## 四体系总览对照

    同一把器械，四套 UDI 体系并行。核心差异在发码机构、数据库、责任方与强制节奏。

    
| 维度 | 中国 | 美国 | 欧盟 | 日本 |
| --- | --- | --- | --- | --- |
| 法规依据 | 2019年第66号公告《UDI系统规则》 | 21 CFR 830 + UDI 最终规则 | MDR 2017/745 第27条 | 药机法2019改正 + UDI実施要項 |
| 发码机构 | GS1 / MA（码上放心）/ 阿里健康等 | GS1 / HIBCC / ICCBBA | GS1（配合 EMDN  nomenclature） | GS1（国内流通统一） |
| 官方数据库 | 国家药监局 UDI 数据库 | GUDID | EUDAMED | KikiDB |
| 责任方 | 注册人 / 备案人 | Labeler（标签方） | 制造商 | MAH / DMAH |
| 强制范围 | III类全覆盖，逐步扩至全部 | 按风险分阶段（III→II→I） | 所有器械（含 I 类） | 几乎全分类（I~IV） |

    关键提示：GS1 是全球最通用的发码体系，四地均可采用 GS1 编码（GTIN），可大幅降低多市场赋码成本。日本虽接受 HIBCC/ICCBBA，但国内流通强制转为 GS1。

  

  
    ## 中国 NMPA UDI

    国家药监局统筹建立 UDI 数据库，注册人/备案人负责上传与维护。

    
| 项目 | 说明 / 入口 |
| --- | --- |
| UDI 数据库（公众查询/企业填报） | [udi.nmpa.gov.cn](https://udi.nmpa.gov.cn) — 数据查询、下载、对接入口 |
| 产品标识申报（政务服务门户） | [国家药监局政务服务门户 · 医疗器械产品标识申报](https://zwfw.nmpa.gov.cn/web/taskview/11100000MB0341032Y100207209800001) |
| 操作手册 / 数据导入模板 | [udi.nmpa.gov.cn/toOperationManual.html](https://udi.nmpa.gov.cn/toOperationManual.html)（含 v3 数据模板） |
| 常见问题 | [udi.nmpa.gov.cn/showListFAQ.html](https://udi.nmpa.gov.cn/showListFAQ.html) |
| 填报方式 | 网页填报 / 批量导入（Excel 模板）/ 接口对接 三种 |
| 发码机构及规则 | 数据库内“发码机构及规则”栏目公开，企业需先向发码机构申请厂商识别码（DI 前缀） |

    I 类II 类III 类 第三类已全覆盖；第二批实施公告（2021年第114号）扩展至部分 II 类。填报依据 YY/T 1752-2020《UDI 数据库填报指南》。

  

  
    ## 美国 FDA GUDID

    Labeler 须在 device 上市前将 DI 信息提交至 GUDID；PI 不存入 GUDID（仅存 PI 标识位）。

    
| 项目 | 说明 / 入口 |
| --- | --- |
| GUDID 总览页（含指南） | [fda.gov/.../global-unique-device-identification-database-gudid](https://www.fda.gov/medical-devices/unique-device-identification-system-udi-system/global-unique-device-identification-database-gudid) |
| AccessGUDID（公众查询） | [accessgudid.nlm.nih.gov](https://accessgudid.nlm.nih.gov)（官方公众查询，无需登录） |
| GUDID 企业登录填报 | [gudid.fda.gov/gudid/](https://gudid.fda.gov/gudid/)（需 LDE 权限；批量 SPL 经 FDA ESG 网关 [ESG](https://www.fda.gov/industry/electronic-submissions-gateway-esg)）；账号申请 [request-gudid-account](https://www.fda.gov/medical-devices/global-unique-device-identification-database-gudid/request-gudid-account) |
| 法规 | 21 CFR 830（UDI 规则）；21 CFR 801.20（标签要求） |
| 赋码阶段 | III 类及生命支持类 2015-09-24；II 类 2016-09-24；I 类及未分类 2018-09-24 |

    注意：GUDID 仅含 DI（设备标识符），不含 PI 数据；PI 印在标签上但不进库。批量提交须经 FDA ESG（Electronic Submissions Gateway）以 HL7 SPL 格式。

  

  
    ## 欧盟 EUDAMED

    MDR/IVDR 要求制造商在 EUDAMED 提交 UDI/器械信息；UDI/Devices 模块自 2026-05-28 起强制使用。

    
| 项目 | 说明 / 入口 |
| --- | --- |
| UDI/器械注册模块 | [ec.europa.eu/health/md_eudamed/udi_devices_registration_en](https://ec.europa.eu/health/md_eudamed/udi_devices_registration_en) |
| EUDAMED 公共网站 | [ec.europa.eu/tools/eudamed](https://ec.europa.eu/tools/eudamed) |
| EUDAMED 登录（受限） | [webgate.ec.europa.eu/eudamed](https://webgate.ec.europa.eu/eudamed)（EU Login 账户） |
| nomenclature（EMDN） | 欧盟医疗器械命名系统，注册时必须使用；完全版在 EUDAMED 公共站 |
| Basic UDI-DI vs UDI-DI | Basic UDI-DI 为“型号族”级标识（用于证书/技术文档关联），UDI-DI 为具体型号；两者均须赋值 |

    I 类IIaIIbIII 类 所有类别均需 Basic UDI-DI + UDI-DI。2026-05-28 起前四个模块（Actor、UDI/Devices、NB & Certificates、Market Surveillance）强制。

  

  
    ## 日本 KikiDB / GS1

    基于 2019 年药机法改正的 UDI 制度，2022-12-01 实施；包装须印 GS1 条码，信息入 KikiDB。

    
| 项目 | 说明 / 入口 |
| --- | --- |
| UDI 実施要項（MHLW 原案） | [mhlw.go.jp UDI実施要項 PDF](https://www.mhlw.go.jp/content/11124500/000681371.pdf) |
| GS1 Japan UDI 条码表示指南 | [gs1jp.org UDI対応バーコード表示ガイド](https://www.gs1jp.org/assets/img/pdf/UDI_guide.pdf) |
| KikiDB（官方数据库） | [kikidb.jp](https://www.kikidb.jp/) — 医療機器データベース |
| 编码体系 | GS1-128（一维）/ GS1 DataMatrix（二维）；国内流通统一 GS1 |
| 责任方 | MAH（製造販売業者）/ DMAH；海外厂须及时准确向 MAH 提供数据 |

    I 类II 类III 类IV 类 日本近乎全分类强制，与医保结算（特别指定材料）直接挂钩，注册错误将影响医院报销。

  

  
    ## GS1 通用发码体系

    跨国企业首选 GS1，一套 GTIN 可复用于中/美/欧/日，显著降低赋码成本。

    
| 资源 | 入口 |
| --- | --- |
| GS1 国际官网 | [gs1.org](https://www.gs1.org/) |
| GTIN / 条码申请 | 各国 GS1 成员组织（中国物品编码中心、GS1 US、GS1 Japan 等） |
| 关键概念 | GTIN（贸易项目编码=DI）、AI（应用标识符，如 (01) 商品、(10) 批号、(21) 序列号、(11) 生产日期、(17) 失效日期） |

  

  
    ## 实施时间表（赋码强制节点）

    
| 市场 | 关键节点 | 备注 |
| --- | --- | --- |
| 美国 | III类 2015-09-24 / II类 2016-09-24 / I类 2018-09-24 | 按风险分阶段，直接标记（direct mark）对 III 类更高要求 |
| 中国 | III类已全覆盖；II类部分（2021第114号）逐步实施 | 生产/进口 III 类最先，其余按品种推进 |
| 欧盟 | UDI/Devices 模块 2026-05-28 强制 | 前四模块强制；legacy device 亦须登记 |
| 日本 | 2022-12-01 实施，2025 前后基本替换legacy库存 | 与 e-IFU（电子说明书）扫码联动 |

  

  
    ## DI / PI 模板要素

    UDI = DI（固定，标识“哪款器械”）+ PI（可变，标识“哪一批/哪一件”）。

    
| 组成 | 内容 | 示例（GS1 AI） |
| --- | --- | --- |
| DI 设备标识符 | 厂商识别码 + 商品项目码 + 校验位（GTIN-14） | (01) 07612345123457 |
| PI 生产标识符（可选组合） | 批号 / 序列号 / 生产日期 / 失效日期 | (10) LOT2026 / (21) SN0088 / (11) 260101 / (17) 301231 |
| 数据库必填 | 企业信息、注册证号、产品名称、规格、DI、PI 属性标识 | 各国表单字段不同，详见各库操作手册 |

    实操建议：立项时即向发码机构申请厂商码；DI 一旦分配给某型号即不可复用/不得变更；包装层级（个装/中箱/外箱）可分别赋 DI。美国 GUDID 仅收 DI，PI 只标不存。

  

UDI 全球标识枢纽 · 注册工程师资料系列 · 链接核实于 2026-08 · 官方页面可能更新，以各数据库最新发布为准


---

*本枢纽由「注册老炮」原创整理，供医疗器械注册合规参考。*
