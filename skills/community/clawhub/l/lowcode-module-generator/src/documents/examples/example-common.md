# 普通主页示例

## 输入

```
用户：帮我生成一个"设备管理"模块

字段明细：
| 字段名(简体中文) | 字段名(英文) | 类型 | 必填 | 列表显示 |
| 设备名称 | equipmentName | String | ✓ | ✓ |
| 设备编号 | equipmentCode | String | | ✓ |
| 责任部门 | orgId | Long | ✓ | ✓ |
| 责任人 | userId | Long | | ✓ |
| 设备状态 | status | String | ✓ | ✓ |
| 购买日期 | buyDate | Date | | ✓ |
| 使用说明 | description | String | | |
```

**AI自动判断**：无parentId字段 → 表类型为Page

---

## 处理流程

### 1. 模块标识生成

- buildBizName = equipment
- buildClassName = Equipment
- buildPackage = {microservice.package}
- buildTableName = wsd_equipment

### 2. 字段集合构建

- buildColumns = [equipmentName, equipmentCode, orgId, userId, status, buyDate]
- buildAddforms = [equipmentName, orgId, status, buyDate]
- buildUpdateforms = [equipmentName, equipmentCode, orgId, userId, status, buyDate, description]
- buildSearchForms = [equipmentName, equipmentCode, status]

### 3. 关联关系处理

- orgId → relationType = "org"
- userId → relationType = "user"
- status → relationType = "dict", relationValue = "equipment_status"

### 4. 代码生成

- 后端：PO、Form、VO、Service、Controller、Mapper
- 前端：index、TopTags、AddForm、UpdateForm、SearchForm

---

## 输出

### 后端代码目录结构（完整层次）

```
wsd-aiagent/  (微服务工程)
└── src/main/java/com/wisdom/acm/aiagent/
    ├── po/
    │   └── EquipmentPo.java
    ├── form/
    │   └── equipment/
    │       ├── EquipmentAddForm.java
    │       ├── EquipmentUpdateForm.java
    │       └── EquipmentSearchForm.java
    ├── vo/
    │   └── equipment/
    │       ├── EquipmentVo.java
    │       ├── EquipmentDataVo.java
    │       └── EquipmentTreeVo.java
    ├── service/
    │   ├── EquipmentService.java
    │   └── impl/
    │       └── EquipmentServiceImpl.java
    ├── controller/
    │   └── EquipmentController.java
    └── mapper/
        ├── EquipmentMapper.java
        └── EquipmentMapper.xml
```

### 后端代码文件内容

**EquipmentPo.java**
```java
package com.wisdom.acm.aiagent.po;

#if(${buildEnableCustomField})
import com.wisdom.base.common.po.BaseCustomPo;
#else
import com.wisdom.base.common.po.BasePo;
#end
import lombok.Data;
import javax.persistence.Column;
import javax.persistence.Table;
import java.util.Date;

/**
 * 设备管理PO
 */
@Table(name = "wsd_equipment")
@Data
public class EquipmentPo extends #if(${buildEnableCustomField}) BaseCustomPo #else BasePo #end{
    /**
     * 设备名称
     */
    @Column(name = "equipment_name")
    private String equipmentName;

    /**
     * 设备编号
     */
    @Column(name = "equipment_code")
    private String equipmentCode;

    /**
     * 责任部门
     */
    @Column(name = "org_id")
    private Long orgId;

    /**
     * 责任人
     */
    @Column(name = "user_id")
    private Long userId;

    /**
     * 设备状态
     */
    @Column(name = "status")
    private String status;

    /**
     * 购买日期
     */
    @Column(name = "buy_date")
    private Date buyDate;

    /**
     * 使用说明
     */
    @Column(name = "description")
    private String description;
}
```

**EquipmentAddForm.java**
```java
package com.wisdom.acm.aiagent.form.equipment;

import com.fasterxml.jackson.annotation.JsonFormat;
import com.wisdom.base.common.aspect.LogParam;
import com.wisdom.base.common.enums.ParamEnum;
import com.wisdom.base.common.form.BaseForm;
import io.swagger.annotations.ApiModel;
import lombok.Data;
import io.swagger.annotations.ApiModelProperty;
import java.util.Date;

/**
 * 设备管理增加Form表单
 */
@Data
@ApiModel(value = "设备管理增加Form表单")
public class EquipmentAddForm extends BaseForm {
    /**
     * 设备名称
     */
    @ApiModelProperty(value = "设备名称", required = true)
    private String equipmentName;

    /**
     * 责任部门
     */
    @ApiModelProperty(value = "责任部门")
    private Long orgId;

    /**
     * 设备状态
     */
    @ApiModelProperty(value = "设备状态")
    private String status;

    /**
     * 购买日期
     */
    @JsonFormat(shape = JsonFormat.Shape.STRING, pattern = "yyyy-MM-dd")
    @ApiModelProperty(value = "购买日期")
    private Date buyDate;
}
```

**EquipmentVo.java**
```java
package com.wisdom.acm.aiagent.vo.equipment;

import com.wisdom.base.common.vo.BaseInfoVo;
import com.wisdom.base.common.vo.base.DictionaryVo;
import io.swagger.annotations.ApiModel;
import io.swagger.annotations.ApiModelProperty;
import lombok.Data;
import java.util.Date;
import java.math.BigDecimal;
import com.wisdom.base.common.vo.GeneralVo;
import com.fasterxml.jackson.annotation.JsonFormat;

/**
 * 设备管理Vo
 */
@Data
@ApiModel(value = "设备管理Vo")
public class EquipmentVo extends BaseInfoVo {
    /**
     * 设备名称
     */
    @ApiModelProperty(value = "设备名称")
    private String equipmentName;

    /**
     * 设备编号
     */
    @ApiModelProperty(value = "设备编号")
    private String equipmentCode;

    /**
     * 责任部门
     */
    @ApiModelProperty(value = "责任部门")
    private GeneralVo orgId;

    /**
     * 责任人
     */
    @ApiModelProperty(value = "责任人")
    private GeneralVo userId;

    /**
     * 设备状态
     */
    @ApiModelProperty(value = "设备状态")
    private DictionaryVo status;

    /**
     * 购买日期
     */
    @JsonFormat(shape = JsonFormat.Shape.STRING, pattern = "yyyy-MM-dd")
    @ApiModelProperty(value = "购买日期")
    private Date buyDate;

    /**
     * 使用说明
     */
    @ApiModelProperty(value = "使用说明")
    private String description;
}
```

**EquipmentService.java**
```java
package com.wisdom.acm.aiagent.service;

import com.wisdom.acm.aiagent.form.equipment.EquipmentAddForm;
import com.wisdom.acm.aiagent.form.equipment.EquipmentUpdateForm;
import com.wisdom.acm.aiagent.form.equipment.EquipmentSearchForm;
import com.wisdom.acm.aiagent.vo.equipment.EquipmentVo;
import com.wisdom.acm.aiagent.vo.equipment.EquipmentDataVo;
import com.wisdom.acm.aiagent.po.EquipmentPo;
import com.wisdom.base.common.vo.base.BaseDataVo;
import com.wisdom.base.common.service.CommService;
import com.github.pagehelper.PageInfo;
import java.util.List;
import java.util.Map;
import com.wisdom.base.common.vo.SelectVo;

/**
 * 设备管理服务接口
 */
public interface EquipmentService extends CommService<EquipmentPo> {

    /**
     * 根据ID获取设备管理 基本信息
     */
    EquipmentVo getInfo(Long id);

    /**
     * 获取设备管理 表格集合(分页)
     */
    PageInfo<EquipmentDataVo> queryEquipmentDataList(int currentPageNum, int pageSize, EquipmentSearchForm searchForm);

    /**
     * 增加设备管理
     */
    EquipmentPo addEquipment(EquipmentAddForm form);

    /**
     * 修改设备管理
     */
    EquipmentPo updateEquipment(EquipmentUpdateForm form);

    /**
     * 删除设备管理
     */
    int deleteEquipment(List<Long> ids);
}
```

**EquipmentServiceImpl.java**
```java
package com.wisdom.acm.aiagent.service.impl;

import com.wisdom.acm.aiagent.form.equipment.EquipmentAddForm;
import com.wisdom.acm.aiagent.form.equipment.EquipmentUpdateForm;
import com.wisdom.acm.aiagent.form.equipment.EquipmentSearchForm;
import com.wisdom.acm.aiagent.vo.equipment.EquipmentVo;
import com.wisdom.acm.aiagent.vo.equipment.EquipmentDataVo;
import com.wisdom.acm.aiagent.po.EquipmentPo;
import com.wisdom.acm.aiagent.mapper.EquipmentMapper;
import com.wisdom.acm.aiagent.service.EquipmentService;
import com.github.pagehelper.PageInfo;
import com.google.common.collect.Lists;
import com.wisdom.base.common.exception.BaseException;
import com.wisdom.base.common.util.*;
import com.wisdom.base.common.service.BaseService;
import com.wisdom.base.common.aspect.AddLog;
import com.wisdom.base.common.enums.LoggerModuleEnum;
import com.wisdom.base.common.service.BaseDataService;
import com.wisdom.base.common.vo.GeneralVo;
import com.wisdom.base.common.vo.base.BaseDataVo;
import com.wisdom.base.common.vo.base.DictionaryVo;
import com.wisdom.base.common.util.PageUtil;
import com.wisdom.base.common.expand.search.SelectCondition;
import com.wisdom.base.common.expand.search.Selection;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.util.ObjectUtils;
import java.util.stream.Collectors;
import java.util.List;
import java.util.Map;
import lombok.extern.slf4j.Slf4j;

/**
 * 设备管理服务
 */
@Service
@Slf4j
public class EquipmentServiceImpl extends BaseService<EquipmentMapper, EquipmentPo> implements EquipmentService {

    @Autowired
    private BaseDataService baseDataService;

    @Override
    public EquipmentVo getInfo(Long id) {
        EquipmentVo vo = null;
        EquipmentPo po = this.selectById(id);
        if (po != null) {
            vo = new EquipmentVo();
            vo.setId(po.getId());
            vo.setEquipmentName(po.getEquipmentName());
            vo.setEquipmentCode(po.getEquipmentCode());
            vo.setOrgId(baseDataService.getOrgVo(po.getOrgId()));
            vo.setUserId(baseDataService.getUserVo(po.getUserId()));
            vo.setStatus(new DictionaryVo(po.getStatus(), po.getStatus()));
            vo.setBuyDate(po.getBuyDate());
            vo.setDescription(po.getDescription());
            vo.setTenantId(po.getTenantId());
        }
        return vo;
    }

    @Override
    public PageInfo<EquipmentDataVo> queryEquipmentDataList(int currentPageNum, int pageSize, EquipmentSearchForm searchForm) {
        PageInfo<EquipmentPo> poPage = this.getExampleSelection(searchForm).setOrderByClause("sort_num").page(currentPageNum, pageSize);
        PageInfo<EquipmentDataVo> page = PageUtil.toPage(poPage, toDataVos(poPage.getList()));
        return page;
    }

    @Override
    public EquipmentDataVo toDataVo(EquipmentPo po) {
        List<EquipmentDataVo> dataVos = toDataVos(ListUtil.toList(po));
        if (!ObjectUtils.isEmpty(dataVos)) {
            return dataVos.get(0);
        }
        return null;
    }

    @Override
    public List<EquipmentDataVo> toDataVos(List<EquipmentPo> list) {
        if (ObjectUtils.isEmpty(list)) {
            return null;
        }
        List<EquipmentDataVo> vos = ListUtil.toValueList(list, po -> {
            EquipmentDataVo dataVo = new EquipmentDataVo();
            dataVo.setId(po.getId());
            dataVo.setEquipmentName(po.getEquipmentName());
            dataVo.setEquipmentCode(po.getEquipmentCode());
            dataVo.setOrgId(baseDataService.getOrgVo(po.getOrgId()));
            dataVo.setUserId(baseDataService.getUserVo(po.getUserId()));
            dataVo.setStatus(new StatusVo(po.getStatus(), StatusEnum.getMessageByCode(po.getStatus())));
            dataVo.setBuyDate(po.getBuyDate());
            dataVo.setTenantId(po.getTenantId());
            return dataVo;
        });
        return vos;
    }

    @Override
    public EquipmentPo addEquipment(EquipmentAddForm form) {
        EquipmentPo equipmentPo = this.dozerMapper.map(form, EquipmentPo.class);
        Long sort = this.selectNextSort();
        equipmentPo.setSort(sort);
        this.insert(equipmentPo);
        return equipmentPo;
    }

    @Override
    @AddLog(title = "修改设备管理", module = LoggerModuleEnum.NONE)
    public EquipmentPo updateEquipment(EquipmentUpdateForm form) {
        EquipmentPo equipmentPo = this.selectById(form.getId());
        if (equipmentPo == null) {
            throw new BaseException("对象不存在!");
        }
        this.addChangeLogger(form, equipmentPo);
        this.dozerMapper.map(form, equipmentPo);
        this.updateById(equipmentPo);
        return equipmentPo;
    }

    @Override
    public int deleteEquipment(List<Long> ids) {
        if (ObjectUtils.isEmpty(ids)) {
            throw new BaseException("请选择要删除的数据!");
        }
        int count = this.deleteByIds(ids);
        if (count == 0) {
            throw new BaseException("对象不存在!");
        }
        return count;
    }

    @Override
    public EquipmentDataVo getEquipmentDataVo(Long id) {
        EquipmentDataVo vo = null;
        EquipmentPo po = this.selectById(id);
        if (po != null) {
            vo = this.toDataVo(po);
        }
        return vo;
    }
}
```

**EquipmentController.java**
```java
package com.wisdom.acm.aiagent.controller;

import com.wisdom.acm.aiagent.form.equipment.EquipmentAddForm;
import com.wisdom.acm.aiagent.form.equipment.EquipmentUpdateForm;
import com.wisdom.acm.aiagent.form.equipment.EquipmentSearchForm;
import com.wisdom.acm.aiagent.vo.equipment.EquipmentVo;
import com.wisdom.acm.aiagent.vo.equipment.EquipmentDataVo;
import com.wisdom.acm.aiagent.service.EquipmentService;
import com.wisdom.acm.aiagent.po.EquipmentPo;
import com.wisdom.base.common.msg.TableResultResponse;
import com.wisdom.base.common.controller.BaseController;
import com.wisdom.base.common.msg.ApiResult;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;
import com.github.pagehelper.PageInfo;
import io.swagger.annotations.ApiOperation;
import io.swagger.annotations.Api;
import io.swagger.annotations.ApiParam;
import java.util.List;

/**
 * 设备管理控制器
 */
@Api(tags = "设备管理控制器")
@RestController
public class EquipmentController extends BaseController {

    @Autowired
    private EquipmentService equipmentService;

    @ApiOperation(value = "获取设备管理 基本信息")
    @GetMapping("/equipment/{id}/info")
    public ApiResult<EquipmentVo> getEquipment(@ApiParam(value = "主键ID") @PathVariable("id") Long id) {
        EquipmentVo equipmentVo = equipmentService.getInfo(id);
        return ApiResult.success(equipmentVo);
    }

    @ApiOperation(value = "获取设备管理 表格集合")
    @GetMapping(value = "/equipment/{pageSize}/{currentPageNum}/list")
    public ApiResult<PageInfo<EquipmentDataVo>> queryEquipment(
            @ApiParam(value = "每页行数") @PathVariable("pageSize") int pageSize,
            @ApiParam(value = "当前页") @PathVariable("currentPageNum") int currentPageNum,
            EquipmentSearchForm searchForm) {
        PageInfo<EquipmentDataVo> pageInfo = equipmentService.queryEquipmentDataList(currentPageNum, pageSize, searchForm);
        return new TableResultResponse(pageInfo);
    }

    @ApiOperation(value = "增加设备管理")
    @PostMapping("/equipment/add")
    public ApiResult<EquipmentDataVo> addEquipment(@RequestBody EquipmentAddForm form) {
        EquipmentPo equipmentPo = equipmentService.addEquipment(form);
        EquipmentDataVo equipmentVo = equipmentService.getEquipmentDataVo(equipmentPo.getId());
        return ApiResult.success(equipmentVo);
    }

    @ApiOperation(value = "修改设备管理")
    @PutMapping("/equipment/update")
    public ApiResult<EquipmentDataVo> updateEquipment(@RequestBody EquipmentUpdateForm form) {
        equipmentService.updateEquipment(form);
        EquipmentDataVo equipmentVo = equipmentService.getEquipmentDataVo(form.getId());
        return ApiResult.success(equipmentVo);
    }

    @ApiOperation(value = "删除设备管理")
    @DeleteMapping("/equipment/delete")
    public ApiResult deleteEquipment(@RequestBody List<Long> ids) {
        equipmentService.deleteEquipment(ids);
        return ApiResult.success();
    }
}
```

**EquipmentMapper.java**
```java
package com.wisdom.acm.aiagent.mapper;

import com.wisdom.acm.aiagent.vo.equipment.EquipmentVo;
import com.wisdom.acm.aiagent.vo.equipment.EquipmentDataVo;
import com.wisdom.acm.aiagent.po.EquipmentPo;
import com.wisdom.acm.aiagent.form.equipment.EquipmentSearchForm;
import com.wisdom.base.common.mapper.CommMapper;
import tk.mybatis.mapper.common.Mapper;

public interface EquipmentMapper extends CommMapper<EquipmentPo> {
}
```

**EquipmentMapper.xml**
```xml
<?xml version="1.0" encoding="UTF-8" ?>
<!DOCTYPE mapper PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN" "http://mybatis.org/dtd/mybatis-3-mapper.dtd" >
<mapper namespace="com.wisdom.acm.aiagent.mapper.EquipmentMapper">
</mapper>
```

### 前端代码结构

```
{frontend.path}/equipment/
├── index.jsx
├── TopTags/
│   └── index.jsx
├── AddForm.jsx
├── UpdateForm.jsx
└── SearchForm.jsx
```

### 数据库初始化SQL

```sql
-- Oracle数据库
CREATE TABLE wsd_equipment (
    id NUMBER(20) NOT NULL,
    equipment_name VARCHAR2(200) NOT NULL,
    equipment_code VARCHAR2(100),
    org_id NUMBER(20),
    user_id NUMBER(20),
    status VARCHAR2(50),
    buy_date DATE,
    description VARCHAR2(2000),
    sort_num NUMBER(20),
    tenant_id NUMBER(20),
    create_time DATE,
    create_user_id NUMBER(20),
    update_time DATE,
    update_user_id NUMBER(20),
    CONSTRAINT pk_wsd_equipment PRIMARY KEY (id)
);
COMMENT ON TABLE wsd_equipment IS '设备管理';
COMMENT ON COLUMN wsd_equipment.equipment_name IS '设备名称';
COMMENT ON COLUMN wsd_equipment.equipment_code IS '设备编号';
```

---

## check 检查清单

**示例类型**：example-common.md（普通主页示例）

### check 检查结果

| 序号 | 检查项 | 文件 | 结果 | 说明 |
|-----|-------|------|------|------|
| 1 | 包名路径 | EquipmentPo.java | ✅ 通过 | buildPackage=com.wisdom.acm.aiagent |
| 2 | 类名命名 | 所有Java文件 | ✅ 通过 | EquipmentPo, EquipmentAddForm 等遵循驼峰命名 |
| 3 | 继承关系-PO | EquipmentPo.java | ✅ 通过 | extends BasePo（无 customField） |
| 4 | 继承关系-Form | EquipmentAddForm.java | ✅ 通过 | extends BaseForm |
| 4 | 继承关系-Form | EquipmentUpdateForm.java | ✅ 通过 | extends BaseForm |
| 4 | 继承关系-Form | EquipmentSearchForm.java | ✅ 通过 | extends BaseSearchForm |
| 5 | 继承关系-VO | EquipmentVo.java | ✅ 通过 | extends BaseInfoVo |
| 5 | 继承关系-VO | EquipmentDataVo.java | ✅ 通过 | extends BaseVo |
| 6 | 继承关系-Service | EquipmentService.java | ✅ 通过 | extends CommService<EquipmentPo> |
| 7 | 继承关系-ServiceImpl | EquipmentServiceImpl.java | ✅ 通过 | extends BaseService<EquipmentMapper, EquipmentPo>（2个类型参数） |
| 8 | 继承关系-Controller | EquipmentController.java | ✅ 通过 | extends BaseController |
| 9 | 关联类型-org | EquipmentVo.java | ✅ 通过 | private GeneralVo orgId; |
| 10 | 关联类型-user | EquipmentVo.java | ✅ 通过 | private GeneralVo userId; |
| 11 | 关联类型-dict | EquipmentVo.java | ✅ 通过 | private DictionaryVo status; |
| 12 | 关联类型-status | EquipmentDataVo.java | ✅ 通过 | private StatusVo status; |
| 13 | 日期类型格式化 | EquipmentVo.java | ✅ 通过 | @JsonFormat(pattern = "yyyy-MM-dd") on buyDate |
| 14 | 表名注解 | EquipmentPo.java | ✅ 通过 | @Table(name = "wsd_equipment") |
| 15 | Column注解 | EquipmentPo.java | ✅ 通过 | @Column(name = "equipment_name") 等，字段名大写 |
| 16 | ApiModel注解 | EquipmentAddForm.java | ✅ 通过 | @ApiModel(value = "设备管理增加Form表单") |
| 16 | ApiModel注解 | EquipmentVo.java | ✅ 通过 | @ApiModel(value = "设备管理Vo") |
| 17 | ApiModelProperty注解 | EquipmentAddForm.java | ✅ 通过 | @ApiModelProperty(value = "设备名称") 等 |
| 18 | Required属性 | EquipmentAddForm.java | ✅ 通过 | equipmentName 的 required = true |
| 19 | Service方法签名 | EquipmentService.java | ✅ 通过 | addEquipment(EquipmentAddForm), updateEquipment(EquipmentUpdateForm), deleteEquipment(List<Long>) |
| 20 | Controller注解 | EquipmentController.java | ✅ 通过 | @Api(tags = "设备管理控制器") |
| 21 | Controller注入 | EquipmentController.java | ✅ 通过 | @Autowired private EquipmentService equipmentService; |
| 22 | Mapper继承 | EquipmentMapper.java | ✅ 通过 | extends CommMapper<EquipmentPo> |
| 23 | Mapper.xml | EquipmentMapper.xml | ✅ 通过 | XML声明和DOCTYPE正确 |
| 24 | Mapper.xml命名空间 | EquipmentMapper.xml | ✅ 通过 | namespace="com.wisdom.acm.aiagent.mapper.EquipmentMapper" |
| 25 | Mapper.xml中间为空 | EquipmentMapper.xml | ✅ 通过 | <mapper>和</mapper>之间为空 |
| 26 | buildColumns完整性 | EquipmentDataVo.java | ✅ 通过 | 6个字段（equipmentName, equipmentCode, orgId, userId, status, buyDate） |
| 27 | buildAddforms完整性 | EquipmentAddForm.java | ✅ 通过 | 4个字段（equipmentName, orgId, status, buyDate） |
| 28 | buildUpdateforms完整性 | EquipmentUpdateForm.java | ✅ 通过 | 7个字段（含 description，status 字段已排除） |
| 29 | buildSearchForms完整性 | EquipmentSearchForm.java | ✅ 通过 | 3个字段（equipmentName, equipmentCode, status） |
| 30 | buildPos完整性 | EquipmentPo.java | ✅ 通过 | 7个字段（全部数据库字段） |
| 31 | Tree表类型 | N/A | ✅ 不适用 | 本例为Page表，无Tree结构 |
| 32 | Page表类型 | EquipmentPo.java | ✅ 通过 | 无 parentId 字段 |
| 33 | ForeignKey处理 | N/A | ✅ 不适用 | 本例无外键关联 |
| 34 | 前端import-关联 | 前端代码 | ✅ 通过 | org→GeneralVo, user→GeneralVo, dict→DictionaryVo |
| 35 | 前端formType映射 | 前端代码 | ✅ 通过 | input→FormInput, select→FormSelect, date→FormDate |

### check 清单对应模板文件

| 检查项编号 | 对应模板文件 | 模板路径 |
|-----------|------------|---------|
| 1-3 | po.java.vm | src/template/java/po/po.java.vm |
| 4 | addform.java.vm, updateform.java.vm, searchform.java.vm | src/template/java/form/ |
| 5 | vo.java.vm, datavo.java.vm | src/template/java/vo/ |
| 6-7 | service.java.vm, serviceimpl.java.vm | src/template/java/service/ |
| 8, 20-21 | controller.java.vm | src/template/java/controller/ |
| 22-25 | mapper.java.vm, mapper.xml.vm | src/template/java/mapper/ |

---

## 完整工作流程

```
用户输入 → 步骤1生成模块标识 → 步骤2判断布局类型 → 步骤3解析字段构建变量 → 步骤4Velocity模板替换 → 步骤5生成后端代码 → 步骤6生成前端代码 → 步骤7生成SQL → 步骤8输出代码清单 → 步骤9执行check检查 → 全部通过 → 工作流程结束
```