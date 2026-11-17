// Model 实体模板 — 使用时替换以下占位符：
// {Name}   → 类名（PascalCase，如 KbDocument）
// {name}   → 变量名（camelCase，如 kbDocument）
// {module} → 模块名（如 aiAssistant）
// {domain} → 业务域名（如 knowledge）
// 字段部分请根据实际表结构调整

package com.link.{module}.{domain}.{name}.model;

import com.link.core.model.BasicModel;
import io.swagger.annotations.ApiModelProperty;
import lombok.Data;

import java.util.Date;

/**
 * {Name} 实体模型
 *
 * @author link-dev
 */
@Data
public class {Name} extends BasicModel {

    @ApiModelProperty("主键ID")
    private Long id;

    @ApiModelProperty("名称")
    private String name;

    @ApiModelProperty("描述")
    private String description;

    @ApiModelProperty("状态: 0-禁用, 1-启用")
    private Integer status;

    @ApiModelProperty("创建人")
    private String createdBy;

    @ApiModelProperty("创建时间")
    private Date creationDate;

    @ApiModelProperty("最后更新人")
    private String lastUpdatedBy;

    @ApiModelProperty("最后更新时间")
    private Date lastUpdateDate;

    @ApiModelProperty("乐观锁版本号")
    private Long objectVersionNumber;
}
