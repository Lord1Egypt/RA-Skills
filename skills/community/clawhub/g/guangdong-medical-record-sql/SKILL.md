# 广东省病案统计管理系统 SQL 查询大师

> 本技能基于《广东省医疗机构病案统计管理系统(2012版)》数据库表结构文档构建，精通该系统所有表的SQL查询。

---

## 一、系统概览

**系统**: 广东省医疗机构病案统计管理系统（2012版）  
**数据库类型**: 通常为 SQL Server 或 Oracle  
**核心模块**: 标准编码 / 门诊日志 / 住院病案 / 报表统计 / 医技 / 妇婴

---

## 二、核心表清单

### 2.1 标准编码表

| 表名 | 中文名 | 主键 |
|------|--------|------|
| `tStandardMain` | 标准编码主表 | `FStdMainCode` |
| `tStandardMx` | 标准编码从表 | `FStdMxCode` |
| `tICD` | ICD编码库 | `FICDCode` |
| `tJBFLB` | 疾病分类表 | `FCode` |
| `tCHDISEASE` | 中医码字典库 | `FCHDICode` |
| `tSDISEASE` | 单病种表 | `FCode` |
| `tSDISEASERemark` | 单病种提示表 | `FID` |
| `tOperate` | 手术码表 | `FOperaCode` |
| `tOperateFlb` | 手术分类表 | `FCode` |
| `tBurnICD` | 中度烧伤ICD | `FICDCode` |
| `tJBFLFSB` | 疾病分类方式表 | `FCode` |

### 2.2 系统字典表

| 表名 | 中文名 | 主键 |
|------|--------|------|
| `tWorkroom` | 科室词典表 | `FCode` |
| `tSpecialRoom` | 专科科室表 | `FzkCode` |
| `tdoctor` | 医生表 | `FGh` (工号) |
| `tdoctorWorkRoom` | 医生科室表 | `FID` |
| `tParam` | 系统参数表 | `FParaCode` |
| `TSYSUSER` | 系统用户表 | `FUserCode` |
| `TRight` | 系统权限表 | `FRightCode` |
| `TMenu` | 系统菜单表 | `FMenuCode` |
| `TRightMenu` | 权限菜单设置表 | `FID` |
| `TGroup` | 用户组表 | `FCode` |
| `TGroupRight` | 用户组权限设置表 | `FID` |
| `TWinpy` | 汉字拼音对照表 | `FID` |

### 2.3 门诊工作日志表

| 表名 | 中文名 | 主键 |
|------|--------|------|
| `tWorklogNoDoctor` | 科室门诊工作日志 | `FDate`, `FTkh` |
| `tWorklog` | 医生门诊工作日志 | `FDate`, `FTKh`, `FGh` |
| `tEmergeLogNoKs` | 急诊工作日志（不分科） | `FDate` |
| `tEmergeLog` | 急诊工作日志（分科） | `FDate`, `FTKh` |
| `tObservelogNoKs` | 观察室工作日志（不分科） | `FDate` |
| `tObservelog` | 观察室工作日志（分科） | `FDate`, `FTKh` |
| `tSpecialLog` | 专科门诊病人数 | `FDate`, `FTzkCode` |
| `tMedicalTechLog` | 医技科室 | `FDate`, `FTKh` |
| `tMedicalTechPlog` | 医技科室（自定义） | `FID` |
| `tMzOperateRoom` | 门诊手术室表 | `FOpBh` |

### 2.4 住院病案核心表

| 表名 | 中文名 | 主键 |
|------|--------|------|
| `tPatientVisit` | 病人住院信息 | `FPatientID` / `FBaNo` |
| `tDiagnose` | 病人诊断信息 | `FPatientID`, `FType` |
| `tDiagnoseAdd` | 诊断码附加编码 | `FID` |
| `tOperation` | 病人手术信息 | `FPatientID`, `FSeq` |
| `tSwitchKs` | 病人转科情况 | `FPatientID` |
| `tBabyCard` | 妇婴卡 | `FPatientID` |
| `TPATIENT` | 病人最新信息 | `FPatientID` |

### 2.5 住院工作日志表

| 表名 | 中文名 | 主键 |
|------|--------|------|
| `TZyWardWorklog` | 病房工作动态日志 | `FDate`, `FWardCode` |
| `TZyWardWorkDayReport` | 病房工作动态日报 | `FDate`, `FWardCode` |
| `TZyHomeBedLog` | 家庭病床工作日志 | `FDate` |
| `TZyjz` | 住院记帐信息表 | `FPatientID` |

### 2.6 报表主表

| 表名 | 中文名 | 关键字段 |
|------|--------|---------|
| `TMzReportMain` | 门诊报表（主表） | `FReportCode`, `FReportDateStr` |
| `TMzMjzWorkReport` | 门（急）诊工作报表 | 同上 |
| `TZyReportMain` | 住院报表（主表） | 同上 |
| `TZyHospitalWorkReport` | 医院工作报表（住院部分） | 同上 |
| `TMzHospitalWorkReport` | 医院工作报表（门诊部分） | 同上 |
| `TReport` | 报表记录表 | `FCode` |

### 2.7 病案质量与核查

| 表名 | 中文名 | 主键 |
|------|--------|------|
| `TBasyValidation` | 病案首页验证规则表 | `FIndexID` |
| `TCheckSet` | 病案首页核查设置表 | `FIndexID` |
| `TBasyBalance` | 首页核查结果表 | `FPatientID` |
| `tbaLend` | 病案借阅登记表 | `FBarCode` |
| `tbaSubmit` | 病案上交登记表 | `FBarCode` |
| `tBaLog` | 病案日志表 | `FBarCode`, `FDate` |

### 2.8 综合查询（自定义）

| 表名 | 中文名 |
|------|--------|
| `TQuerySelfShow` | 综合查询自定义显示（字段） |
| `TQuerySelfShowTemplate` | 综合查询自定义显示（模板） |
| `TQuerySelfShowTemplateField` | 模板字段对照关系 |
| `TQuerySelfCondition` | 综合查询自定义条件 |

---

## 三、常用SQL查询示例

### 3.1 门诊统计

**【门诊日志】按科室按日统计诊疗人次**
```sql
SELECT 
    CONVERT(VARCHAR(10), wl.FDate, 120) AS 统计日期,
    w.FName AS 科室名称,
    SUM(wl.FZsrs) AS 医生人数,
    SUM(wl.FZzlrc) AS 诊疗人次,
    SUM(wl.FZzlygrc) AS 主诊疗人次,
    SUM(wl.FZlzrc) AS 留诊人次
FROM tWorklogNoDoctor wl
JOIN tWorkroom w ON wl.FTKh = w.FTKh
WHERE wl.FDate BETWEEN '2024-01-01' AND '2024-01-31'
GROUP BY wl.FDate, w.FName
ORDER BY wl.FDate, w.FName;
```

**【门诊医生工作量】按医生统计月工作量**
```sql
SELECT 
    w.FName AS 科室,
    d.FName AS 医生姓名,
    d.FZhicheng AS 职称,
    SUM(l.FZzlrc) AS 总诊疗人次,
    SUM(l.FZlzrc) AS 留诊人次,
    SUM(l.FSsusrc) AS 手术人次,
    COUNT(DISTINCT CONVERT(VARCHAR(7), l.FDate, 120)) AS 出诊天数
FROM tWorklog l
JOIN tdoctor d ON l.FGh = d.FGh
JOIN tWorkroom w ON l.FTKh = w.FTKh
WHERE l.FDate BETWEEN '2024-01-01' AND '2024-01-31'
GROUP BY w.FName, d.FName, d.FZhicheng
ORDER BY SUM(l.FZzlrc) DESC;
```

**【急诊日志】按日统计急诊情况**
```sql
SELECT 
    CONVERT(VARCHAR(10), el.FDate, 120) AS 日期,
    SUM(el.FJzsrc) AS 急诊人次,
    SUM(el.FQzysrc) AS 抢救人次,
    SUM(el.FQzcgysrc) AS 抢救成功人次,
    CASE WHEN SUM(el.FJzsrc) > 0 
         THEN ROUND(SUM(el.FQzcgysrc) * 100.0 / SUM(el.FJzsrc), 2) 
         ELSE 0 END AS 抢救成功率Pct
FROM tEmergeLogNoKs el
WHERE el.FDate BETWEEN '2024-01-01' AND '2024-01-31'
GROUP BY el.FDate
ORDER BY el.FDate;
```

**【观察室日志】**
```sql
SELECT 
    CONVERT(VARCHAR(10), ol.FDate, 120) AS 日期,
    SUM(ol.FGcsbeds) AS 观察室床位数,
    SUM(ol.FYbrs) AS 现有病人数,
    SUM(ol.FCsbrs) AS 出室病人数,
    SUM(ol.FCssmws) AS 出室病人死亡,
    SUM(ol.FQzbingsrc) AS 抢救病人数,
    SUM(ol.FCzbrs) AS 出室病人占床日数
FROM tObservelogNoKs ol
WHERE ol.FDate BETWEEN '2024-01-01' AND '2024-01-31'
GROUP BY ol.FDate
ORDER BY ol.FDate;
```

---

### 3.2 住院病案查询

**【病案首页】查询指定时间段出院病人**
```sql
SELECT 
    pv.FBaNo AS 病案号,
    pv.FFromHos AS 出院科室,
    CONVERT(VARCHAR(10), pv.FOutDate, 120) AS 出院日期,
    pv.FInDays AS 住院天数,
    d.FDiagName AS 主要诊断,
    d.FICDCode AS 主要诊断ICD,
    o.FOperaName AS 手术名称,
    o.FOperaDate AS 手术日期,
    o.FMZDoctorName AS 麻醉医生,
    pv.FCureRate AS 治疗效果
FROM tPatientVisit pv
LEFT JOIN (
    SELECT FPatientID, FDiagName, FICDCode
    FROM tDiagnose WHERE FType = 1  -- 主诊断
) d ON pv.FPatientID = d.FPatientID
LEFT JOIN (
    SELECT FPatientID, FOperaName, FOperaDate, FMZDoctorName
    FROM tOperation WHERE FSeq = 1  -- 主手术
) o ON pv.FPatientID = o.FPatientID
WHERE pv.FOutDate BETWEEN '2024-01-01' AND '2024-01-31'
  AND pv.FStatus = '已出院'
ORDER BY pv.FOutDate DESC;
```

**【诊断查询】按ICD编码统计疾病**
```sql
SELECT 
    diag.FICDCode AS ICD编码,
    icd.FICDName AS 疾病名称,
    COUNT(*) AS 病例数,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 2) AS 构成比Pct
FROM tDiagnose diag
JOIN tICD icd ON diag.FICDCode = icd.FICDCode
WHERE diag.FType = 1  -- 主诊断
  AND diag.FDiagDate BETWEEN '2024-01-01' AND '2024-01-31'
GROUP BY diag.FICDCode, icd.FICDName
HAVING COUNT(*) >= 5  -- 过滤小于5例
ORDER BY COUNT(*) DESC;
```

**【手术查询】按手术医生统计**
```sql
SELECT 
    o.FOperaDoctorName AS 手术医生,
    d.FZhicheng AS 职称,
    COUNT(*) AS 手术总例数,
    SUM(CASE WHEN o.FQzxSzbh = 'I' THEN 1 ELSE 0 END) AS 一类切口,
    SUM(CASE WHEN o.FQzxSzbh = 'II' THEN 1 ELSE 0 END) AS 二类切口,
    SUM(CASE WHEN o.FQzxSzbh = 'III' THEN 1 ELSE 0 END) AS 三类切口,
    SUM(CASE WHEN o.FYhyhdj = '甲' THEN 1 ELSE 0 END) AS 甲级愈合
FROM tOperation o
JOIN tdoctor d ON o.FOperaDoctorCode = d.FGh
WHERE o.FOperaDate BETWEEN '2024-01-01' AND '2024-01-31'
GROUP BY o.FOperaDoctorName, d.FZhicheng
ORDER BY COUNT(*) DESC;
```

**【转科查询】住院期间转科记录**
```sql
SELECT 
    pv.FBaNo AS 病案号,
    pv.FName AS 姓名,
    sk.FInDate AS 转入日期,
    w1.FName AS 转出科室,
    w2.FName AS 转入科室
FROM tSwitchKs sk
JOIN tPatientVisit pv ON sk.FPatientID = pv.FPatientID
JOIN tWorkroom w1 ON sk.FFromDept = w1.FTKh
JOIN tWorkroom w2 ON sk.FToDept = w2.FTKh
WHERE sk.FInDate BETWEEN '2024-01-01' AND '2024-01-31'
ORDER BY pv.FBaNo, sk.FInDate;
```

**【科室病床占用情况】**
```sql
SELECT 
    CONVERT(VARCHAR(10), wl.FDate, 120) AS 日期,
    w.FName AS 科室,
    wl.FCyrys AS 出院人数,
    wl.FZyrs AS 在院人数,
    wl.FBeds AS 病床数,
    ROUND(wl.FBedsOccRate, 2) AS 病床占用率
FROM TZyWardWorklog wl
JOIN tWorkroom w ON wl.FWardCode = w.FTKh
WHERE wl.FDate BETWEEN '2024-01-01' AND '2024-01-31'
ORDER BY wl.FDate, w.FName;
```

---

### 3.3 ICD编码与疾病分类

**【ICD查询】精确查找ICD编码**
```sql
-- ICD-10诊断编码精确查询
SELECT 
    FICDCode AS 编码,
    FICDName AS 名称,
    FStdClass AS 分类
FROM tICD
WHERE FICDCode = 'I10' 
   OR FICDName LIKE '%高血压%';

-- 按章节统计ICD使用频次
SELECT 
    LEFT(diag.FICDCode, 3) AS 章节码,
    COUNT(*) AS 使用次数
FROM tDiagnose diag
WHERE diag.FDiagDate BETWEEN '2024-01-01' AND '2024-01-31'
GROUP BY LEFT(diag.FICDCode, 3)
ORDER BY COUNT(*) DESC;
```

**【单病种查询】**
```sql
SELECT 
    sd.FCode AS 病种码,
    sd.FName AS 病种名称,
    sd.FPjhjs AS 平均住院日,
    sd.FZyyhls AS 治愈好转率,
    sd.FZdqds AS 平均确诊天数
FROM tSDISEASE sd
WHERE sd.FIsMainOnly = 1  -- 只统计主诊断
ORDER BY sd.FCode;
```

**【手术编码查询】**
```sql
SELECT 
    FOperaCode AS 手术编码,
    FOperaName AS 手术名称,
    FFlName AS 手术分类
FROM tOperate
WHERE FOperaName LIKE '%子宫切除%'
   OR FOperaCode LIKE '68%';
```

---

### 3.4 报表统计

**【住院报表主表】按月汇总**
```sql
SELECT 
    rm.FReportDateStr AS 报表月份,
    rm.FReportType AS 报表类型,
    rm.FStartDate AS 开始日期,
    rm.FEndDate AS 结束日期,
    rm.FStatus AS 报表状态,
    u.FUserName AS 汇总人
FROM TZyReportMain rm
LEFT JOIN TSYSUSER u ON rm.FHzUserCode = u.FUserCode
WHERE rm.FReportDateStr LIKE '2024-01%'
ORDER BY rm.FReportDateStr;
```

**【十种疾病术后十日内死亡统计】**
```sql
SELECT 
    r.FReportDateStr AS 报表月份,
    jf.FName AS 疾病类别,
    op.FName AS 手术类别,
    r.FFromHosNum AS 出院人数,
    r.FOptNum AS 手术人数,
    r.FDead10Num AS 术后10日内死亡人数,
    CASE WHEN r.FOptNum > 0 
         THEN ROUND(r.FDead10Num * 100.0 / r.FOptNum, 2) 
         ELSE 0 END AS 死亡率Pct
FROM TZy20ICDDeadInTenReport r
JOIN tJBFLB jf ON r.FJbflCode = jf.FCode
JOIN tOperateFlb op ON r.FOptCode = op.FCode
WHERE r.FReportDateStr LIKE '2024-01%'
ORDER BY r.FDead10Num DESC;
```

**【经济收入报表】**
```sql
SELECT 
    r.FReportDateStr AS 月份,
    r.FYwSrTotal AS 业务收入合计,
    r.FMzSrTotal AS 门诊收入合计,
    r.FZySrTotal AS 住院收入合计,
    r.FYwZcTotal AS 业务支出合计,
    ROUND((r.FYwSrTotal - r.FYwZcTotal) * 1.0 / r.FYwSrTotal * 100, 2) AS 收支结余率,
    r.FPjZcyDays AS 出院者平均住院日,
    r.FPjZyF AS 出院者平均费用
FROM TZyHosEcInOutReport r
WHERE r.FReportDateStr BETWEEN '2024-01' AND '2024-12'
ORDER BY r.FReportDateStr;
```

---

### 3.5 病案质量核查

**【首页核查】查询未通过核查的病案**
```sql
SELECT 
    pv.FBaNo AS 病案号,
    pv.FFromHos AS 科室,
    b.FFieldName AS 核查字段,
    b.FErrorMsg AS 错误信息,
    b.FChkDate AS 核查日期
FROM TBasyBalance b
JOIN tPatientVisit pv ON b.FPatientID = pv.FPatientID
WHERE b.FResult = 0  -- 未通过
  AND b.FChkDate BETWEEN '2024-01-01' AND '2024-01-31'
ORDER BY pv.FFromHos, b.FChkDate;
```

**【病案借阅查询】**
```sql
SELECT 
    lv.FBarCode AS 病案条码,
    pv.FName AS 病人姓名,
    lv.FOutDate AS 借出日期,
    lv.FPlanReturnDate AS 应还日期,
    CASE WHEN lv.FIsReturn = 1 THEN '已还' ELSE '未还' END AS 状态,
    lv.FReaderDept AS 借阅科室,
    lv.FReaderName AS 借阅人
FROM tbaLend lv
JOIN tPatientVisit pv ON lv.FPatientID = pv.FPatientID
WHERE lv.FOutDate BETWEEN '2024-01-01' AND '2024-01-31'
ORDER BY lv.FIsReturn, lv.FOutDate;
```

---

### 3.6 医技与特殊报表

**【医技工作量报表】**
```sql
SELECT 
    r.FReportDateStr AS 月份,
    r.FGcsrc AS 观察室人次,
    r.FYjksrc AS 医技科室人次,
    r.FZzrc AS 诊察人次,
    r.FJcxsrc AS 检查想人次,
    r.FZlxsrc AS 治疗想人次
FROM tMedicalTechLog r
WHERE r.FReportDateStr LIKE '2024-01%';
```

**【家庭病床报表】**
```sql
SELECT 
    r.FReportDateStr AS 月份,
    r.FCcbrs AS 撤床病人数,
    r.FCcbrzrc AS 撤床病人诊疗人次,
    r.FTnskbs AS 期内开设总病床数,
    r.FZcbrzrs AS 期内总撤床病日数
FROM TZyHomeBedReport r
WHERE r.FReportDateStr BETWEEN '2024-01' AND '2024-12';
```

---

## 四、字段命名规则（字段前缀对照）

| 前缀 | 含义 | 示例 |
|------|------|------|
| `F` | 字段 | `FName`, `FDate` |
| `FCode` | 编码 | 科室代码、报表代码 |
| `FName` | 名称 | `FName` |
| `FID` | 内部ID | 主键 |
| `FTKh` | 统一科号 | `FTKh` = 统一科号 |
| `FGh` | 工号 | 医生工号 |
| `FDate` | 日期 | 日期 |
| `FDateStr` | 日期字符串 | `YYYY-MM-DD` |
| `FSrc` | 人数/人次 | `FJzsSrc` 急诊人次 |
| `FNum` | 数量 | `FOptNum` 手术数量 |
| `FFee` | 费用 | `FFyTotal` 总费用 |
| `FRate` | 比率/率 | `FSsccRate` 成功率 |
| `FPct` | 百分比 | 占比 |
| `FSum` | 合计 | `FFySum` 费用合计 |

---

## 五、常用条件与过滤

### 日期范围
```sql
-- 日期字段通常是 FDate 或 FOutDate (出院日期)
WHERE FDate >= '2024-01-01' AND FDate < '2024-02-01'
-- 或字符串格式
WHERE FReportDateStr BETWEEN '2024-01' AND '2024-12'
```

### 主诊断/主手术
```sql
-- 诊断类型: FType = 1 为主诊断, 2+ 为其他诊断
WHERE FType = 1
-- 手术 FSeq = 1 为主手术
WHERE FSeq = 1
```

### 报表状态
```sql
-- 0=日报, 1=月报, 2=季度报, 3=年度报
WHERE FReportType = 1
-- 报表状态: 草稿/已提交/已审核
WHERE FStatus IN ('已提交', '已审核')
```

### 切口愈合等级
```sql
-- 甲级愈合 / 乙级愈合 / 丙级愈合
WHERE FYhyhdj = '甲'
```

### 治疗效果
```sql
-- 治愈 / 好转 / 未愈 / 死亡 / 其他
WHERE FCureRate = '治愈'
```

---

## 六、查询技巧

### 6.1 关联HIS系统数据
```sql
-- 对应HIS_MZLOG1等HIS接口表
SELECT * FROM HIS_MZLOG1 
WHERE FReportDate = '2024-01-15';
```

### 6.2 拼音码查询
```sql
-- 医生/科室拼音查询（通过TWinpy表关联）
SELECT d.FGh, d.FName, wp.FFirstLetter AS 拼音首字母
FROM tdoctor d
LEFT JOIN TWinpy wp ON d.FName = wp.FHz
WHERE wp.FFirstLetter LIKE 'ZXK%';
```

### 6.3 分页查询（大数据量）
```sql
SELECT * FROM (
    SELECT ROW_NUMBER() OVER (ORDER BY FOutDate DESC) AS RowNum,
           pv.*
    FROM tPatientVisit pv
    WHERE pv.FOutDate >= '2024-01-01'
) t
WHERE t.RowNum BETWEEN 1 AND 50;
```

### 6.4 医保病案上传状态
```sql
SELECT * FROM UPLOADZYBA 
WHERE FMedInsCode = '贵阳市医保'
  AND FUploadDate IS NOT NULL;
```

---

## 七、注意事项

1. **日期字段**: 不同表日期字段不同，注意 `FDate`(日志) vs `FOutDate`(出院) vs `FInDate`(入院)
2. **编码对应**: 使用 `FTKh`(统一科号) 而非科室名称进行关联
3. **报表月份**: 报表常用字符串格式如 `YYYY-MM`，需用 `LIKE '2024-01%'`
4. **空值处理**: 出院病人若无手术，`tOperation` 联合查询时用 `LEFT JOIN`
5. **HIS接口**: HIS系统传入数据存储在 `HIS_*` 前缀表中，可用于数据核对

---

> 💡 **使用提示**: 提问时尽量说明"查什么"、"时间段"、"按什么维度汇总"，我可生成更精准的SQL语句。
