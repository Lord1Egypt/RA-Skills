// Service 接口模板 — 使用时替换以下占位符：
// {Name}   → 类名（PascalCase，如 KbDocument）
// {name}   → 变量名（camelCase，如 kbDocument）
// {module} → 模块名（如 aiAssistant）
// {domain} → 业务域名（如 knowledge）

package com.link.{module}.{domain}.{name}.service;

import com.link.core.service.BasicService;
import com.link.{module}.{domain}.{name}.model.{Name};

import java.util.List;

/**
 * {Name} Service 接口
 *
 * @author link-dev
 */
public interface {Name}Service extends BasicService<{Name}> {

    /**
     * 分页查询
     *
     * @param entity   查询条件
     * @param page     页码（从1开始）
     * @param pageSize 每页条数
     * @return 查询结果列表
     */
    List<{Name}> queryByExamplePage({Name} entity, int page, int pageSize);

    /**
     * 查询总数
     *
     * @param entity 查询条件
     * @return 总记录数
     */
    int queryCount({Name} entity);

    /**
     * 根据ID查询
     *
     * @param id 主键ID
     * @return 查询结果
     */
    {Name} queryById(Long id);

    /**
     * 新增
     *
     * @param entity 实体对象
     * @return 影响行数
     */
    int insert({Name} entity);

    /**
     * 更新（乐观锁）
     *
     * @param entity 实体对象（含 objectVersionNumber）
     * @return 影响行数
     */
    int update({Name} entity);

    /**
     * 根据ID删除
     *
     * @param id 主键ID
     * @return 影响行数
     */
    int deleteById(Long id);
}
