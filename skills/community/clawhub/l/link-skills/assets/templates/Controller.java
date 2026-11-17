// Controller 模板 — 使用时替换以下占位符：
// {Name}      → 类名（PascalCase，如 KbDocument）
// {name}      → 变量名（camelCase，如 kbDocument）
// {module}    → 模块名（如 aiAssistant）
// {domain}    → 业务域名（如 knowledge）
// {table}     → 表名（如 LNK_KB_DOCUMENT）
// {desc}      → 接口描述（如 知识库文档）

package com.link.{module}.{domain}.{name}.controller;

import com.link.core.annotation.JsonParam;
import com.link.core.controller.BasicController;
import com.link.core.exception.BasicServiceException;
import com.link.{module}.{domain}.{name}.model.{Name};
import com.link.{module}.{domain}.{name}.service.{Name}Service;
import io.swagger.annotations.Api;
import io.swagger.annotations.ApiOperation;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseBody;

import javax.annotation.Resource;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * {desc}接口
 *
 * @author link-dev
 */
@Api(tags = {"{desc}接口"})
@Controller
@RequestMapping("/link/{module}/{name}")
@Slf4j
public class {Name}Controller extends BasicController<{Name}> {

    @Resource
    private {Name}Service {name}Service;

    /**
     * 分页查询
     */
    @ApiOperation("分页查询")
    @RequestMapping({"/queryByExamplePage"})
    @ResponseBody
    public Map<String, Object> queryByExamplePage(
            @JsonParam {Name} entity,
            @RequestParam(defaultValue = "1") int page,
            @RequestParam(defaultValue = "10") int pageSize) {
        Map<String, Object> result = new HashMap<>(8);
        try {
            List<{Name}> rows = {name}Service.queryByExamplePage(entity, page, pageSize);
            int total = {name}Service.queryCount(entity);
            result.put("success", true);
            result.put("code", "200");
            result.put("rows", rows);
            result.put("total", total);
        } catch (BasicServiceException var8) {
            result.put("success", false);
            result.put("code", var8.getCode());
            result.put("detailMessage", var8.getDetailMessage());
        } catch (Exception var9) {
            log.error("分页查询{desc}失败", var9);
            result.put("success", false);
            result.put("code", "500");
            result.put("detailMessage", "系统错误");
        }
        return result;
    }

    /**
     * 根据ID查询
     */
    @ApiOperation("根据ID查询")
    @RequestMapping({"/queryById"})
    @ResponseBody
    public Map<String, Object> queryById(@RequestParam("id") Long id) {
        Map<String, Object> result = new HashMap<>(8);
        try {
            {Name} entity = {name}Service.queryById(id);
            result.put("success", true);
            result.put("code", "200");
            result.put("result", entity);
        } catch (BasicServiceException var8) {
            result.put("success", false);
            result.put("code", var8.getCode());
            result.put("detailMessage", var8.getDetailMessage());
        } catch (Exception var9) {
            log.error("根据ID查询{desc}失败", var9);
            result.put("success", false);
            result.put("code", "500");
            result.put("detailMessage", "系统错误");
        }
        return result;
    }

    /**
     * 新增
     */
    @ApiOperation("新增")
    @RequestMapping({"/insert"})
    @ResponseBody
    public Map<String, Object> insert(@JsonParam {Name} entity) {
        Map<String, Object> result = new HashMap<>(8);
        try {
            int count = {name}Service.insert(entity);
            result.put("success", true);
            result.put("code", "200");
            result.put("result", count);
        } catch (BasicServiceException var8) {
            result.put("success", false);
            result.put("code", var8.getCode());
            result.put("detailMessage", var8.getDetailMessage());
        } catch (Exception var9) {
            log.error("新增{desc}失败", var9);
            result.put("success", false);
            result.put("code", "500");
            result.put("detailMessage", "系统错误");
        }
        return result;
    }

    /**
     * 更新（乐观锁）
     */
    @ApiOperation("更新")
    @RequestMapping({"/update"})
    @ResponseBody
    public Map<String, Object> update(@JsonParam {Name} entity) {
        Map<String, Object> result = new HashMap<>(8);
        try {
            int count = {name}Service.update(entity);
            result.put("success", true);
            result.put("code", "200");
            result.put("result", count);
        } catch (BasicServiceException var8) {
            result.put("success", false);
            result.put("code", var8.getCode());
            result.put("detailMessage", var8.getDetailMessage());
        } catch (Exception var9) {
            log.error("更新{desc}失败", var9);
            result.put("success", false);
            result.put("code", "500");
            result.put("detailMessage", "系统错误");
        }
        return result;
    }

    /**
     * 根据ID删除
     */
    @ApiOperation("根据ID删除")
    @RequestMapping({"/deleteById"})
    @ResponseBody
    public Map<String, Object> deleteById(@RequestParam("id") Long id) {
        Map<String, Object> result = new HashMap<>(8);
        try {
            int count = {name}Service.deleteById(id);
            result.put("success", true);
            result.put("code", "200");
            result.put("result", count);
        } catch (BasicServiceException var8) {
            result.put("success", false);
            result.put("code", var8.getCode());
            result.put("detailMessage", var8.getDetailMessage());
        } catch (Exception var9) {
            log.error("删除{desc}失败", var9);
            result.put("success", false);
            result.put("code", "500");
            result.put("detailMessage", "系统错误");
        }
        return result;
    }
}
