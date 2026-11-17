# FDA UDI 实施实务

> 原创整理，依据公开官方法规：FDA《UDI 最终规则》（2013）、21 CFR Part 830（标签）、801.20（UDI 呈现）、GUDID。**合规日期以 FDA 官方当前发布为准。**

## 0. 官方原文直达
- FDA UDI 系统官方专题页（UDI Basics）：https://www.fda.gov/medical-devices/unique-device-identification-system-udi-system/udi-basics
- 21 CFR Part 830（UDI 规则，eCFR）：https://www.ecfr.gov/current/title-21/chapter-I/subchapter-H/part-830
- 21 CFR 801.20（UDI 在标签上的呈现要求，eCFR）：https://www.ecfr.gov/current/title-21/chapter-I/subchapter-H/part-801
- GUDID 数据库（AccessGUDID 查询）：https://gudid.fda.gov/gudid/
- UDI 最终规则（Federal Register 2013-23059）：https://www.govinfo.gov/app/details/FR-2013-09-24/2013-23059

## 1. 是什么
FDA 于 2013 年发布最终规则建立 UDI 系统，是全球最早法制化的器械唯一标识体系。输美医疗器械须符合。UDI 由两部分组成：
- **DI（Device Identifier，器械识别码）**：固定部分，标识标签者（通常为制造商）与具体型号/版本；由 FDA 认可的发码机构分配，须上传 GUDID。
- **PI（Production Identifier，生产识别码）**：可变部分，含批号、序列号、生产日期、有效期、软件版本等。

## 2. 发码机构（FDA 认可，认可期 3 年、可续、FDA 有权撤销）
- **GS1**（主流，GTIN 14 位格式）
- **HIBCC**（Health Industry Business Communications Council，6-23 位字母数字）
- **ICCBBA**（血液/细胞/组织专用，10-16 位）
- FDA 在极端或必要情形下保留自任发码机构的可能。

## 3. GUDID
Global UDI Database，制造商上传产品数据（DI 层），公众可免费查询、下载。Labeler 对 UDI 承担完整责任：确保 UDI 由认可机构分配、出现在标签与包装上、向 GUDID 提交 DI 数据。**GUDID 账号须开在 labeler（标签上署名方）名下**，即便标签设计外包，FDA 也不会把账号开给非 labeler。

## 4. 合规日期（按器械类别）
| 类别 | 标签 + GUDID | 直接标记 |
|---|---|---|
| Class III（高风险） | 2014-09-24 | 2016-09-24 |
| 植入/生命支持/生命维持（I/LS/LS） | 2015-09-24 | 2015-09-24（同步） |
| Class II（中风险） | 2016-09-24 | 2018-09-24 |
| Class I 与未分类 | 2022-12-08（enforcement 延至该日） | 2020-09-24 |

注：Class I 标签/GUDID 原定 2020-09-24，FDA 行使 enforcement discretion 延至 2022-12-08。到 2024 年后几乎所有在美上市器械应满足 UDI 标签 + GUDID 提交。

## 5. 编码与条码
- DI 结构因机构而异：GS1 为 GTIN 14 位（公司前缀+项目参考+校验位）；HIBCC/ICCBBA 字母数字。
- 条码格式：GS1-128（1D）、GS1 DataMatrix（2D，小器械/DPM 主流）。标签须同时具备人读明文与 AIDC 机器可读。

## 6. 实操检查清单
- [ ] 确认 labeler 身份（制造商 or 美国品牌方），开设 GUDID 账号
- [ ] 选定发码机构（多数国际厂选 GS1，兼顾 FDA/EU MDR）
- [ ] 分配 DI、登记基础 UDI-DI，按类落实 PI 要素
- [ ] 按合规日期完成标签改造与 GUDID 数据提交
- [ ] 复用/再处理器械须直接标记

## 7. 分步实操：GUDID 提交全流程（手把手）

> 从 0 到 GUDID 数据上线的实操顺序，每步给动作 + 系统入口 + 交付物。

**① 开通 GUDID 账号**
- 动作：在 FDA 设备注册与列名系统以 **labeler（标签署名方）** 身份注册 GUDID 账号。
- 坑：FDA 不开账号给非 labeler——即便标签设计外包，账号也必须在 labeler（制造商/美国品牌方）名下。

**② 选发码机构 + 申请厂商前缀**
- 动作：选 FDA 认可发码机构（GS1 / HIBCC / ICCBBA）；向机构申请厂商识别段。
- 多数国际厂选 **GS1**：申请 GCP（厂商识别码）→ 得 GTIN-14 结构（公司前缀 + 项目参考 + 校验位）。血液/细胞/组织专用选 ICCBBA。

**③ 编制 UDI-DI**
- 动作：按机构编码规则为具体型号/版本生成 DI；在 EU 侧对应概念为"基础 UDI-DI"，FDA 侧即 DI 层。
- 交付物：每个型号一个唯一 DI。

**④ 确定 PI 要素**
- 动作：按器械类别确定须承载的生产识别码（PI）：批号 / 序列号 / 生产日期 / 有效期 / 软件版本（有源/SaMD 常含软件版本）。
- 坑：类别不同 PI 要求不同，照搬别家模板会缺项。

**⑤ 标签与直接标记**
- 动作：标签印 DI+PI，**同时具备人读明文 + AIDC 机器可读**（GS1-128 一维 / GS1 DataMatrix 二维，小器械与 DPM 主流）。
- 坑：复用/再处理器械除标签外须**直接标记于器械本身**（合规日期见第 4 节）。

**⑥ 提交 GUDID**
- 动作：在 GUDID 上传 DI 层数据（设备描述、标识符、联系方、生产信息、使用信息等），按第 4 节合规日期完成提交。
- 入口：FDA GUDID（accessgudid.fda.gov）。
- 坑：设计/标签变更须及时更新 GUDID，否则数据库与实物不符。

**⑦ 维护**
- 动作：建立 UDI 变更触发机制——任何影响 DI/PI/标识的变更，同步更新 GUDID 与标签，留痕。

> 一句话：labeler 开账号 → 选 GS1 拿前缀 → 编 DI → 定 PI → 改标签 → 提 GUDID → 持续维护。多市场（EU MDR 同样强制 UDI）可共用 GS1 发码，减少重复工作。
