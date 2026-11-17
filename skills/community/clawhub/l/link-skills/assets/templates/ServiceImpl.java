// Service 实现模板 — 使用时替换以下占位符：
// {Name}   → 类名（PascalCase，如 KbDocument）
// {name}   → 变量名（camelCase，如 kbDocument）
// {module} → 模块名（如 aiAssistant）
// {domain} → 业务域名（如 knowledge）

package com.link.{module}.{domain}.{name}.service.impl;

import com.link.core.service.impl.BasicServiceImpl;
import com.link.{module}.{domain}.{name}.dao.mybatis.mapper.{Name}Mapper;
import com.link.{module}.{domain}.{name}.model.{Name};
import com.link.{module}.{domain}.{name}.service.{Name}Service;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

import javax.annotation.Resource;
import java.util.List;

/**
 * {Name} Service 实现
 *
 * @author link-dev
 */
@Service
@Slf4j
public class {Name}ServiceImpl extends BasicServiceImpl<{Name}> implements {Name}Service {

    @Resource
    private {Name}Mapper {name}Mapper;

    @Override
    public List<{Name}> queryByExamplePage({Name} entity, int page, int pageSize) {
        int offset = (page - 1) * pageSize;
        return {name}Mapper.queryByExamplePage(entity, offset, pageSize);
    }

    @Override
    public int queryCount({Name} entity) {
        return {name}Mapper.queryCount(entity);
    }

    @Override
    public {Name} queryById(Long id) {
        return {name}Mapper.queryById(id);
    }

    @Override
    public int insert({Name} entity) {
        return {name}Mapper.insert(entity);
    }

    @Override
    public int update({Name} entity) {
        return {name}Mapper.update(entity);
    }

    @Override
    public int deleteById(Long id) {
        return {name}Mapper.deleteById(id);
    }
}
