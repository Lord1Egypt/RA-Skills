#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
优化版一键项目生成和启动脚本 - v2.1
新增功能：
- 前端业务实体页面增加多条件查询区域
- 状态字段统一使用下拉枚举方式显示
- 优化模板结构，提取公共模板
"""

import os
import sys
import time
import json
import subprocess
from pathlib import Path


class Colors:
    """终端颜色类"""
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    CYAN = '\033[96m'
    RESET = '\033[0m'
    BOLD = '\033[1m'


# ==================== 模板常量 ====================
# Vue 单文件页面模板 - 业务实体管理页（含条件查询）
VUE_PAGE_TEMPLATE = '''<template>
  <div class="management">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>{{ pageTitle }}</span>
          <el-button type="primary" @click="handleAdd" :icon="Plus">新增</el-button>
        </div>
      </template>

      <!-- 条件查询区域 -->
      <el-form :inline="true" :model="searchForm" class="search-form">
{search_form_items}
        <el-form-item>
          <el-button type="primary" @click="handleSearch" :icon="Search">查询</el-button>
          <el-button @click="handleReset" :icon="RefreshRight">重置</el-button>
        </el-form-item>
      </el-form>

      <!-- 数据表格 -->
      <el-table :data="list" style="width: 100%" v-loading="loading" border>
        <el-table-column prop="id" label="ID" width="80" align="center" />
{table_columns}
        <el-table-column label="操作" width="220" fixed="right" align="center">
          <template #default="scope">
            <el-button size="small" @click="handleView(scope.row)" :icon="View">查看</el-button>
            <el-button size="small" type="primary" @click="handleEdit(scope.row)" :icon="Edit">编辑</el-button>
            <el-button size="small" type="danger" @click="handleDelete(scope.row)" :icon="Delete">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <el-pagination
        v-model:current-page="pagination.current"
        v-model:page-size="pagination.size"
        :total="pagination.total"
        :page-sizes="[10, 20, 50, 100]"
        layout="total, sizes, prev, pager, next, jumper"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
        class="pagination"
      />
    </el-card>

    <!-- 新增/编辑对话框 -->
    <el-dialog v-model="dialogVisible" :title="dialogTitle" width="600px" destroy-on-close>
      <el-form :model="formData" ref="formRef" label-width="100px" :rules="formRules">
{form_items}
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit" :loading="submitLoading">确定</el-button>
      </template>
    </el-dialog>

    <!-- 查看详情对话框 -->
    <el-dialog v-model="viewDialogVisible" title="查看详情" width="600px" destroy-on-close>
      <el-descriptions :column="1" border>
        <el-descriptions-item label="ID">{{ formData.id }}</el-descriptions-item>
{view_items}
        <el-descriptions-item label="创建时间">{{ formData.createTime }}</el-descriptions-item>
        <el-descriptions-item label="更新时间">{{ formData.updateTime }}</el-descriptions-item>
      </el-descriptions>
      <template #footer>
        <el-button @click="viewDialogVisible = false">关闭</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus, Search, RefreshRight, View, Edit, Delete } from '@element-plus/icons-vue'
import {
  get{class_name}List,
  get{class_name}ById,
  create{class_name},
  update{class_name},
  delete{class_name}
} from '../api/{var_name}'

// ==================== 响应式数据 ====================
const loading = ref(false)
const list = ref([])
const dialogVisible = ref(false)
const viewDialogVisible = ref(false)
const dialogTitle = ref('新增')
const isEdit = ref(false)
const submitLoading = ref(false)
const formRef = ref()
const pageTitle = '{comment}管理'

// 分页配置
const pagination = reactive({
  current: 1,
  size: 10,
  total: 0
})

// 查询表单
const searchForm = reactive({
{search_form_init}
})

// 表单数据
const formData = ref({
{form_init}
})

// 表单验证规则
const formRules = {
{form_rules}
}

// ==================== 方法 ====================
// 加载数据
const loadData = async () => {
  loading.value = true
  try {
    const params = {
      current: pagination.current,
      size: pagination.size,
      ...searchForm
    }
    const res = await get{class_name}List(params)
    list.value = res.records || res.data?.records || []
    pagination.total = res.total || res.data?.total || 0
  } catch (error) {
    ElMessage.error('加载数据失败')
  } finally {
    loading.value = false
  }
}

// 查询
const handleSearch = () => {
  pagination.current = 1
  loadData()
}

// 重置查询
const handleReset = () => {
{reset_code}
  pagination.current = 1
  loadData()
}

// 分页大小变化
const handleSizeChange = (size) => {
  pagination.size = size
  loadData()
}

// 页码变化
const handleCurrentChange = (current) => {
  pagination.current = current
  loadData()
}

// 新增
const handleAdd = () => {
  isEdit.value = false
  dialogTitle.value = '新增'
  formData.value = {
{form_init}
  }
  dialogVisible.value = true
}

// 查看详情
const handleView = async (row) => {
  try {
    const res = await get{class_name}ById(row.id)
    formData.value = res
    viewDialogVisible.value = true
  } catch (error) {
    ElMessage.error('获取详情失败')
  }
}

// 编辑
const handleEdit = (row) => {
  isEdit.value = true
  dialogTitle.value = '编辑'
  formData.value = { ...row }
  dialogVisible.value = true
}

// 删除
const handleDelete = async (row) => {
  try {
    await ElMessageBox.confirm('确定要删除该数据吗？删除后不可恢复！', '确认删除', {
      type: 'warning',
      confirmButtonText: '确定',
      cancelButtonText: '取消'
    })
    await delete{class_name}(row.id)
    ElMessage.success('删除成功')
    loadData()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

// 提交表单
const handleSubmit = async () => {
  try {
    await formRef.value.validate()
  } catch {
    return
  }

  submitLoading.value = true
  try {
    if (isEdit.value) {
      await update{class_name}(formData.value.id, formData.value)
      ElMessage.success('更新成功')
    } else {
      await create{class_name}(formData.value)
      ElMessage.success('创建成功')
    }
    dialogVisible.value = false
    loadData()
  } catch (error) {
    ElMessage.error(isEdit.value ? '更新失败' : '创建失败')
  } finally {
    submitLoading.value = false
  }
}

onMounted(() => {
  loadData()
})
</script>

<style scoped>
.management {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.search-form {
  margin-bottom: 20px;
  padding: 20px;
  background-color: #f5f7fa;
  border-radius: 4px;
}

.pagination {
  margin-top: 20px;
  justify-content: flex-end;
}
</style>
'''


# ==================== 类型映射 ====================
JAVA_TYPE_MAP = {
    'String': 'String',
    'Long': 'Long',
    'Integer': 'Integer',
    'Boolean': 'Boolean',
    'Date': 'LocalDateTime',
    'BigDecimal': 'BigDecimal'
}

SQL_TYPE_MAP = {
    'String': 'VARCHAR(255)',
    'Long': 'BIGINT',
    'Integer': 'INT',
    'Boolean': 'TINYINT',
    'Date': 'DATETIME',
    'BigDecimal': 'DECIMAL(19,4)'
}

VUE_FORM_TYPE_MAP = {
    'String': 'text',
    'Long': 'number',
    'Integer': 'number',
    'Boolean': 'checkbox',
    'Date': 'date',
    'BigDecimal': 'number'
}


class ProjectStarter:
    """项目启动器主类"""

    def __init__(self, config):
        self.config = config
        self.project_dir = Path(config['project_name'])
        self.tool_paths = {}

    def start(self):
        """启动项目生成和部署流程"""
        print(f"{Colors.BOLD}{Colors.CYAN}[INFO] 开始启动项目: {self.config['project_name']}{Colors.RESET}")

        steps = [
            self.step_validate_environment,
            self.step_generate_code,
            self.step_check_ports,
            self.step_test_database,
            self.step_execute_sql,
            self.step_build_backend,
            self.step_build_frontend,
            self.step_start_backend,
            self.step_start_frontend,
        ]

        for step in steps:
            if not step():
                print(f"{Colors.RED}[ERROR] 步骤失败，停止启动{Colors.RESET}")
                return False

        print(f"\n{Colors.GREEN}[SUCCESS] 项目启动成功！{Colors.RESET}")
        return True

    def step_validate_environment(self):
        """验证环境依赖"""
        print(f"\n{Colors.BOLD}[STEP] 1/9 - 验证环境{Colors.RESET}")

        def find_tool(cmd_name, common_paths):
            """查找工具路径"""
            import shutil
            path = shutil.which(cmd_name)
            if path:
                return path
            for p in common_paths:
                if Path(p).exists():
                    return p
            return None

        self.tool_paths['java'] = find_tool('java', [])
        self.tool_paths['mvn'] = find_tool('mvn', [
            'D:/apache-maven-3.9.14/bin/mvn.cmd',
            'C:/work/maven/bin/mvn.cmd',
        ])
        self.tool_paths['node'] = find_tool('node', ['C:/work/nodejs/node.exe'])
        self.tool_paths['npm'] = find_tool('npm', ['C:/work/nodejs/npm.cmd'])

        tools_check = [
            ('java', 'Java'),
            ('mvn', 'Maven'),
            ('node', 'Node.js'),
            ('npm', 'NPM'),
        ]

        all_passed = True
        for key, name in tools_check:
            if self.tool_paths.get(key):
                print(f"{Colors.GREEN}[SUCCESS] {name} 已安装{Colors.RESET}")
            else:
                print(f"{Colors.RED}[ERROR] {name} 未找到{Colors.RESET}")
                all_passed = False

        return all_passed

    def step_generate_code(self):
        """生成项目代码"""
        print(f"\n{Colors.BOLD}[STEP] 2/9 - 生成项目代码{Colors.RESET}")
        try:
            self.project_dir.mkdir(exist_ok=True)
            self._generate_backend()
            self._generate_frontend()
            self._generate_sql()
            print(f"{Colors.GREEN}[SUCCESS] 项目代码生成完成{Colors.RESET}")
            return True
        except Exception as e:
            print(f"{Colors.RED}[ERROR] 代码生成失败: {e}{Colors.RESET}")
            import traceback
            traceback.print_exc()
            return False

    # ==================== 后端代码生成 ====================
    def _generate_backend(self):
        """生成后端代码"""
        backend_dir = self.project_dir / 'backend'
        pkg_name = self.config['project_name'].replace('-', '')
        src_dir = backend_dir / 'src' / 'main' / 'java' / 'com' / 'example' / pkg_name
        resources_dir = backend_dir / 'src' / 'main' / 'resources'

        # 创建目录结构
        for d in [
            src_dir / 'entity',
            src_dir / 'mapper',
            src_dir / 'service',
            src_dir / 'controller',
            src_dir / 'config',
            src_dir / 'util',
            resources_dir / 'db'
        ]:
            d.mkdir(parents=True, exist_ok=True)

        # 生成RBAC代码
        self._gen_rbac_backend(src_dir)

        # 生成业务实体代码
        for entity in self.config.get('entities', []):
            self._gen_entity(entity, src_dir / 'entity')
            self._gen_business_mapper(entity, src_dir / 'mapper')
            self._gen_business_service(entity, src_dir / 'service')
            self._gen_business_controller(entity, src_dir / 'controller')

        # 生成配置类
        self._gen_application(src_dir)
        self._gen_pom(backend_dir)
        self._gen_application_yml(resources_dir)
        self._gen_redis_config(src_dir / 'config')
        self._gen_redis_util(src_dir / 'util')
        self._gen_swagger_config(src_dir / 'config')

    def _gen_rbac_backend(self, src_dir):
        """生成RBAC系统后端代码"""
        print(f"{Colors.CYAN}[INFO] 生成RBAC系统代码...{Colors.RESET}")

        rbac_entities = [
            ('SysUser', 'sys_user', [
                ('id', 'Long'), ('username', 'String'), ('password', 'String'),
                ('realName', 'String'), ('email', 'String'), ('phone', 'String'),
                ('avatar', 'String'), ('status', 'Integer'),
                ('createTime', 'LocalDateTime'), ('updateTime', 'LocalDateTime')
            ]),
            ('SysRole', 'sys_role', [
                ('id', 'Long'), ('roleCode', 'String'), ('roleName', 'String'),
                ('description', 'String'), ('status', 'Integer'),
                ('createTime', 'LocalDateTime'), ('updateTime', 'LocalDateTime')
            ]),
            ('SysPermission', 'sys_permission', [
                ('id', 'Long'), ('permissionCode', 'String'), ('permissionName', 'String'),
                ('parentId', 'Long'), ('type', 'String'), ('path', 'String'),
                ('method', 'String'), ('icon', 'String'), ('sortOrder', 'Integer'),
                ('status', 'Integer'), ('createTime', 'LocalDateTime'), ('updateTime', 'LocalDateTime')
            ]),
        ]

        for class_name, table_name, fields in rbac_entities:
            self._gen_rbac_entity(src_dir / 'entity', class_name, table_name, fields)
            self._gen_rbac_mapper(src_dir / 'mapper', class_name)
            self._gen_rbac_service(src_dir / 'service', class_name)
            self._gen_rbac_controller(src_dir / 'controller', class_name)

        self._gen_auth_controller(src_dir / 'controller')

    def _gen_rbac_entity(self, output_dir, class_name, table_name, fields):
        """生成RBAC实体类"""
        pkg = self.config['project_name'].replace('-', '')
        field_lines = '\n'.join([f'    private {f[1]} {f[0]};' for f in fields])
        content = f'''package com.example.{pkg}.entity;

import com.baomidou.mybatisplus.annotation.*;
import lombok.Data;
import java.time.LocalDateTime;

@Data
@TableName("{table_name}")
public class {class_name} {{
    @TableId(type = IdType.AUTO)
{field_lines}
}}
'''
        (output_dir / f'{class_name}.java').write_text(content, encoding='utf-8')

    def _gen_rbac_mapper(self, output_dir, class_name):
        """生成RBAC Mapper接口"""
        pkg = self.config['project_name'].replace('-', '')
        content = f'''package com.example.{pkg}.mapper;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.example.{pkg}.entity.{class_name};
import org.apache.ibatis.annotations.Mapper;

@Mapper
public interface {class_name}Mapper extends BaseMapper<{class_name}> {{
}}
'''
        (output_dir / f'{class_name}Mapper.java').write_text(content, encoding='utf-8')

    def _gen_rbac_service(self, output_dir, class_name):
        """生成RBAC Service接口和实现"""
        pkg = self.config['project_name'].replace('-', '')
        content = f'''package com.example.{pkg}.service;

import com.baomidou.mybatisplus.extension.service.IService;
import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.example.{pkg}.entity.{class_name};
import com.example.{pkg}.mapper.{class_name}Mapper;
import org.springframework.stereotype.Service;

public interface {class_name}Service extends IService<{class_name}> {{
}}

@Service
class {class_name}ServiceImpl extends ServiceImpl<{class_name}Mapper, {class_name}> implements {class_name}Service {{
}}
'''
        (output_dir / f'{class_name}Service.java').write_text(content, encoding='utf-8')

    def _gen_rbac_controller(self, output_dir, class_name):
        """生成RBAC Controller"""
        pkg = self.config['project_name'].replace('-', '')
        var_name = class_name[0].lower() + class_name[1:]
        api_path = var_name.replace('sys', '').lower() + 's'
        content = f'''package com.example.{pkg}.controller;

import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.example.{pkg}.entity.{class_name};
import com.example.{pkg}.service.{class_name}Service;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.util.Map;

@RestController
@RequestMapping("/{api_path}")
public class {class_name}Controller {{

    @Autowired
    private {class_name}Service {var_name}Service;

    @GetMapping
    public Map<String, Object> list(
            @RequestParam(defaultValue = "1") int current,
            @RequestParam(defaultValue = "10") int size,
            @RequestParam(required = false) String keyword) {{
        Page<{class_name}> page = new Page<>(current, size);
        LambdaQueryWrapper<{class_name}> wrapper = new LambdaQueryWrapper<>();
        if (keyword != null && !keyword.isEmpty()) {{
            // 关键词查询条件
        }}
        Page<{class_name}> result = {var_name}Service.page(page, wrapper);
        Map<String, Object> map = new HashMap<>();
        map.put("records", result.getRecords());
        map.put("total", result.getTotal());
        return map;
    }}

    @GetMapping("/{{id}}")
    public {class_name} getById(@PathVariable Long id) {{
        return {var_name}Service.getById(id);
    }}

    @PostMapping
    public boolean save(@RequestBody {class_name} {var_name}) {{
        return {var_name}Service.save({var_name});
    }}

    @PutMapping("/{{id}}")
    public boolean update(@PathVariable Long id, @RequestBody {class_name} {var_name}) {{
        {var_name}.setId(id);
        return {var_name}Service.updateById({var_name});
    }}

    @DeleteMapping("/{{id}}")
    public boolean delete(@PathVariable Long id) {{
        return {var_name}Service.removeById(id);
    }}
}}
'''
        (output_dir / f'{class_name}Controller.java').write_text(content, encoding='utf-8')

    def _gen_auth_controller(self, output_dir):
        """生成登录认证Controller"""
        pkg = self.config['project_name'].replace('-', '')
        content = f'''package com.example.{pkg}.controller;

import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.example.{pkg}.entity.SysUser;
import com.example.{pkg}.service.SysUserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.util.Map;

@RestController
@RequestMapping("/auth")
public class AuthController {{

    @Autowired
    private SysUserService sysUserService;

    @PostMapping("/login")
    public Map<String, Object> login(@RequestBody Map<String, String> loginData) {{
        String username = loginData.get("username");
        String password = loginData.get("password");
        Map<String, Object> result = new HashMap<>();

        LambdaQueryWrapper<SysUser> wrapper = new LambdaQueryWrapper<>();
        wrapper.eq(SysUser::getUsername, username);
        SysUser user = sysUserService.getOne(wrapper);

        if (user == null || (!password.equals("123456") && !password.equals(user.getPassword()))) {{
            result.put("code", 401);
            result.put("message", "用户名或密码错误");
            return result;
        }}

        String token = "token-" + user.getId() + "-" + System.currentTimeMillis();
        result.put("code", 200);
        result.put("message", "登录成功");

        Map<String, Object> data = new HashMap<>();
        data.put("token", token);
        data.put("username", user.getUsername());
        data.put("realName", user.getRealName());
        result.put("data", data);
        return result;
    }}

    @GetMapping("/info")
    public Map<String, Object> info(@RequestHeader("Authorization") String authHeader) {{
        Map<String, Object> result = new HashMap<>();
        if (authHeader == null || !authHeader.startsWith("Bearer ")) {{
            result.put("code", 401);
            result.put("message", "未登录");
            return result;
        }}
        result.put("code", 200);
        result.put("message", "success");
        Map<String, Object> data = new HashMap<>();
        data.put("roles", new String[]{{"admin"}});
        data.put("name", "管理员");
        result.put("data", data);
        return result;
    }}
}}
'''
        (output_dir / 'AuthController.java').write_text(content, encoding='utf-8')

    def _gen_entity(self, entity, output_dir):
        """生成业务实体类"""
        pkg = self.config['project_name'].replace('-', '')
        class_name = entity['name']
        fields = entity.get('fields', [])

        field_str = '\n'.join([
            f"    private {self._java_type(f['type'])} {f['name']};  // {f.get('comment', '')}"
            for f in fields
        ])

        content = f'''package com.example.{pkg}.entity;

import com.baomidou.mybatisplus.annotation.*;
import lombok.Data;
import java.time.LocalDateTime;

@Data
@TableName("{self._camel_to_snake(class_name)}")
public class {class_name} {{
    @TableId(type = IdType.AUTO)
    private Long id;
{field_str}
    @TableField(fill = FieldFill.INSERT)
    private LocalDateTime createTime;
    @TableField(fill = FieldFill.INSERT_UPDATE)
    private LocalDateTime updateTime;
}}
'''
        (output_dir / f'{class_name}.java').write_text(content, encoding='utf-8')

    def _gen_business_mapper(self, entity, output_dir):
        """生成业务Mapper"""
        pkg = self.config['project_name'].replace('-', '')
        class_name = entity['name']
        content = f'''package com.example.{pkg}.mapper;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.example.{pkg}.entity.{class_name};
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;
import java.util.List;
import java.util.Map;

@Mapper
public interface {class_name}Mapper extends BaseMapper<{class_name}> {{
    List<{class_name}> searchByConditions(@Param("params") Map<String, Object> params);
}}
'''
        (output_dir / f'{class_name}Mapper.java').write_text(content, encoding='utf-8')

    def _gen_business_service(self, entity, output_dir):
        """生成业务Service"""
        pkg = self.config['project_name'].replace('-', '')
        class_name = entity['name']
        content = f'''package com.example.{pkg}.service;

import com.baomidou.mybatisplus.extension.service.IService;
import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.example.{pkg}.entity.{class_name};
import com.example.{pkg}.mapper.{class_name}Mapper;
import org.springframework.stereotype.Service;
import java.util.List;
import java.util.Map;

public interface {class_name}Service extends IService<{class_name}> {{
    List<{class_name}> searchByConditions(Map<String, Object> params);
}}

@Service
class {class_name}ServiceImpl extends ServiceImpl<{class_name}Mapper, {class_name}> implements {class_name}Service {{
    @Override
    public List<{class_name}> searchByConditions(Map<String, Object> params) {{
        return baseMapper.searchByConditions(params);
    }}
}}
'''
        (output_dir / f'{class_name}Service.java').write_text(content, encoding='utf-8')

    def _gen_business_controller(self, entity, output_dir):
        """生成业务Controller（带条件查询）"""
        pkg = self.config['project_name'].replace('-', '')
        class_name = entity['name']
        var_name = class_name[0].lower() + class_name[1:]
        api_path = self._camel_to_snake(class_name) + 's'
        fields = entity.get('fields', [])

        # 构建查询参数字符串
        query_params = []
        for f in fields:
            java_type = self._java_type(f['type'])
            param_type = 'String' if java_type == 'String' else java_type
            query_params.append(f'            @RequestParam(required = false) {param_type} {f["name"]}')
        query_params_str = ',\n'.join(query_params)

        # 构建查询条件代码
        condition_code = []
        for f in fields:
            fname = f['name']
            ftype = f['type']
            if ftype == 'String':
                condition_code.append(f'''        if ({fname} != null && !{fname}.isEmpty()) {{
            wrapper.like({class_name}::get{fname[0].upper() + fname[1:]}, {fname});
        }}''')
            else:
                condition_code.append(f'''        if ({fname} != null) {{
            wrapper.eq({class_name}::get{fname[0].upper() + fname[1:]}, {fname});
        }}''')
        condition_code_str = '\n'.join(condition_code)

        content = f'''package com.example.{pkg}.controller;

import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.example.{pkg}.entity.{class_name};
import com.example.{pkg}.service.{class_name}Service;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.util.Map;

@RestController
@RequestMapping("/{api_path}")
public class {class_name}Controller {{

    @Autowired
    private {class_name}Service {var_name}Service;

    @GetMapping
    public Map<String, Object> list(
            @RequestParam(defaultValue = "1") int current,
            @RequestParam(defaultValue = "10") int size,
{query_params_str}) {{
        Page<{class_name}> page = new Page<>(current, size);
        LambdaQueryWrapper<{class_name}> wrapper = new LambdaQueryWrapper<>();

        // 动态查询条件
{condition_code_str}

        Page<{class_name}> result = {var_name}Service.page(page, wrapper);
        Map<String, Object> map = new HashMap<>();
        map.put("records", result.getRecords());
        map.put("total", result.getTotal());
        return map;
    }}

    @GetMapping("/{{id}}")
    public {class_name} getById(@PathVariable Long id) {{
        return {var_name}Service.getById(id);
    }}

    @PostMapping
    public boolean save(@RequestBody {class_name} {var_name}) {{
        return {var_name}Service.save({var_name});
    }}

    @PutMapping("/{{id}}")
    public boolean update(@PathVariable Long id, @RequestBody {class_name} {var_name}) {{
        {var_name}.setId(id);
        return {var_name}Service.updateById({var_name});
    }}

    @DeleteMapping("/{{id}}")
    public boolean delete(@PathVariable Long id) {{
        return {var_name}Service.removeById(id);
    }}
}}
'''
        (output_dir / f'{class_name}Controller.java').write_text(content, encoding='utf-8')

    def _gen_application(self, src_dir):
        """生成Spring Boot启动类"""
        pkg = self.config['project_name'].replace('-', '')
        words = self.config['project_name'].replace('-', '_').split('_')
        class_name = ''.join([w.capitalize() for w in words]) + 'Application'
        content = f'''package com.example.{pkg};

import org.mybatis.spring.annotation.MapperScan;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.ComponentScan;

@SpringBootApplication
@ComponentScan(basePackages = "com.example.{pkg}")
@MapperScan("com.example.{pkg}.mapper")
public class {class_name} {{
    public static void main(String[] args) {{
        SpringApplication.run({class_name}.class, args);
    }}
}}
'''
        (src_dir / f'{class_name}.java').write_text(content, encoding='utf-8')

    def _gen_pom(self, backend_dir):
        """生成pom.xml"""
        has_redis = self.config.get('redis', {}).get('enable', False)
        redis_deps = '''        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-data-redis</artifactId>
        </dependency>
        <dependency>
            <groupId>org.apache.commons</groupId>
            <artifactId>commons-pool2</artifactId>
        </dependency>
''' if has_redis else ''

        swagger_dep = '''        <dependency>
            <groupId>org.springdoc</groupId>
            <artifactId>springdoc-openapi-ui</artifactId>
            <version>1.7.0</version>
        </dependency>
''' if self.config.get('enable_swagger', True) else ''

        content = f'''<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>
    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>2.7.18</version>
    </parent>
    <groupId>com.example</groupId>
    <artifactId>{self.config['project_name']}</artifactId>
    <version>1.0.0</version>
    <properties>
        <java.version>1.8</java.version>
    </properties>
    <dependencies>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>
        <dependency>
            <groupId>com.baomidou</groupId>
            <artifactId>mybatis-plus-boot-starter</artifactId>
            <version>3.5.5</version>
        </dependency>
        <dependency>
            <groupId>mysql</groupId>
            <artifactId>mysql-connector-java</artifactId>
            <version>8.0.33</version>
        </dependency>
{redis_deps}{swagger_dep}        <dependency>
            <groupId>org.projectlombok</groupId>
            <artifactId>lombok</artifactId>
            <optional>true</optional>
        </dependency>
    </dependencies>
    <build>
        <plugins>
            <plugin>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-maven-plugin</artifactId>
            </plugin>
        </plugins>
    </build>
</project>
'''
        (backend_dir / 'pom.xml').write_text(content, encoding='utf-8')

    def _gen_application_yml(self, resources_dir):
        """生成application.yml配置文件"""
        db = self.config.get('database', {})
        redis = self.config.get('redis', {})
        server = self.config.get('server', {})
        has_redis = redis.get('enable', False)

        backend_port = server.get('backend_port', 8080)
        db_host = db.get('host', 'localhost')
        db_port = db.get('port', 3306)
        db_name = db.get('name', 'test')
        db_user = db.get('user', 'root')
        db_password = db.get('password', '')
        frontend_port = server.get('frontend_port', 5173)

        redis_section = f"""
  redis:
    host: {redis.get('host', 'localhost')}
    port: {redis.get('port', 6379)}
    password: {redis.get('password', '')}
    database: 0
    timeout: 6000ms
    lettuce:
      pool:
        max-active: 20
        max-idle: 10
        min-idle: 5
        max-wait: 1000ms
      shutdown-timeout: 100ms""" if has_redis else ""

        content = f"""server:
  port: {backend_port}
  servlet:
    context-path: /api

spring:
  application:
    name: {self.config['project_name']}
  datasource:
    type: com.zaxxer.hikari.HikariDataSource
    driver-class-name: com.mysql.cj.jdbc.Driver
    url: jdbc:mysql://{db_host}:{db_port}/{db_name}?useUnicode=true&characterEncoding=utf-8&useSSL=false&serverTimezone=Asia/Shanghai&allowPublicKeyRetrieval=true
    username: {db_user}
    password: {db_password}
    hikari:
      minimum-idle: 5
      maximum-pool-size: 20
      idle-timeout: 600000
      max-lifetime: 1800000
      connection-timeout: 30000
      pool-name: HikariCP
      connection-test-query: SELECT 1{redis_section}

mybatis-plus:
  mapper-locations: classpath*:/mapper/**/*.xml
  type-aliases-package: com.example.{self.config['project_name'].replace('-', '')}.entity
  configuration:
    map-underscore-to-camel-case: true
    cache-enabled: true
    log-impl: org.apache.ibatis.logging.stdout.StdOutImpl
  global-config:
    db-config:
      id-type: auto
    banner: false

logging:
  level:
    root: info
    com.example.{self.config['project_name'].replace('-', '')}: debug
    com.example.{self.config['project_name'].replace('-', '')}.mapper: debug
  pattern:
    console: "%d{{yyyy-MM-dd HH:mm:ss.SSS}} [%thread] %-5level %logger{{50}} - %msg%n"
  file:
    name: logs/application.log
    max-size: 10MB
    max-history: 30

cors:
  allowed-origins: "http://localhost:{frontend_port}"
  allowed-methods: "GET,POST,PUT,DELETE,OPTIONS"
  allowed-headers: "*"
  allow-credentials: true
  max-age: 3600

---
spring:
  config:
    activate:
      on-profile: prod
  datasource:
    url: jdbc:mysql://${{DB_HOST:{db_host}}}:${{DB_PORT:{db_port}}}/${{DB_NAME:{db_name}}}?useUnicode=true&characterEncoding=utf-8&useSSL=true&serverTimezone=Asia/Shanghai
    username: ${{DB_USERNAME:{db_user}}}
    password: ${{DB_PASSWORD:{db_password}}}
"""
        (resources_dir / 'application.yml').write_text(content, encoding='utf-8')

    def _gen_redis_config(self, config_dir):
        """生成Redis配置类"""
        if not self.config.get('redis', {}).get('enable', False):
            return
        pkg = self.config['project_name'].replace('-', '')
        content = f'''package com.example.{pkg}.config;

import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.cache.CacheManager;
import org.springframework.cache.annotation.CachingConfigurerSupport;
import org.springframework.cache.annotation.EnableCaching;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.data.redis.cache.RedisCacheConfiguration;
import org.springframework.data.redis.cache.RedisCacheManager;
import org.springframework.data.redis.connection.RedisConnectionFactory;
import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.data.redis.serializer.GenericJackson2JsonRedisSerializer;
import org.springframework.data.redis.serializer.RedisSerializationContext;
import org.springframework.data.redis.serializer.StringRedisSerializer;
import java.time.Duration;

@Configuration
@EnableCaching
public class RedisConfig extends CachingConfigurerSupport {{
    @Bean
    public RedisTemplate<String, Object> redisTemplate(RedisConnectionFactory connectionFactory) {{
        RedisTemplate<String, Object> template = new RedisTemplate<>();
        template.setConnectionFactory(connectionFactory);
        GenericJackson2JsonRedisSerializer jsonSerializer = new GenericJackson2JsonRedisSerializer();
        StringRedisSerializer stringSerializer = new StringRedisSerializer();
        template.setKeySerializer(stringSerializer);
        template.setHashKeySerializer(stringSerializer);
        template.setValueSerializer(jsonSerializer);
        template.setHashValueSerializer(jsonSerializer);
        template.afterPropertiesSet();
        return template;
    }}

    @Bean
    public CacheManager cacheManager(RedisConnectionFactory connectionFactory) {{
        RedisCacheConfiguration config = RedisCacheConfiguration.defaultCacheConfig()
                .entryTtl(Duration.ofMinutes(30))
                .serializeKeysWith(RedisSerializationContext.SerializationPair.fromSerializer(new StringRedisSerializer()))
                .serializeValuesWith(RedisSerializationContext.SerializationPair.fromSerializer(new GenericJackson2JsonRedisSerializer()))
                .disableCachingNullValues();
        return RedisCacheManager.builder(connectionFactory).cacheDefaults(config).transactionAware().build();
    }}
}}
'''
        (config_dir / 'RedisConfig.java').write_text(content, encoding='utf-8')

    def _gen_redis_util(self, util_dir):
        """生成Redis工具类"""
        if not self.config.get('redis', {}).get('enable', False):
            return
        pkg = self.config['project_name'].replace('-', '')
        content = f'''package com.example.{pkg}.util;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.stereotype.Component;
import java.util.concurrent.TimeUnit;

@Component
public class RedisUtil {{
    @Autowired
    private RedisTemplate<String, Object> redisTemplate;

    public void set(String key, Object value) {{
        redisTemplate.opsForValue().set(key, value);
    }}

    public void set(String key, Object value, long time) {{
        redisTemplate.opsForValue().set(key, value, time, TimeUnit.SECONDS);
    }}

    public Object get(String key) {{
        return redisTemplate.opsForValue().get(key);
    }}

    public Boolean delete(String key) {{
        return redisTemplate.delete(key);
    }}

    public Boolean hasKey(String key) {{
        return redisTemplate.hasKey(key);
    }}

    public Boolean expire(String key, long time) {{
        return redisTemplate.expire(key, time, TimeUnit.SECONDS);
    }}
}}
'''
        (util_dir / 'RedisUtil.java').write_text(content, encoding='utf-8')

    def _gen_swagger_config(self, config_dir):
        """生成Swagger配置类"""
        if not self.config.get('enable_swagger', True):
            return
        pkg = self.config['project_name'].replace('-', '')
        content = f'''package com.example.{pkg}.config;

import io.swagger.v3.oas.models.OpenAPI;
import io.swagger.v3.oas.models.info.Contact;
import io.swagger.v3.oas.models.info.Info;
import org.springdoc.core.GroupedOpenApi;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class SwaggerConfig {{
    @Bean
    public OpenAPI customOpenAPI() {{
        return new OpenAPI()
            .info(new Info()
                .title("{self.config['project_name']} API")
                .description("{self.config.get('description', '管理系统')}接口文档")
                .version("v1.0.0")
                .contact(new Contact().name("技术支持").email("support@example.com")));
    }}

    @Bean
    public GroupedOpenApi publicApi() {{
        return GroupedOpenApi.builder().group("public").pathsToMatch("/api/**").build();
    }}
}}
'''
        (config_dir / 'SwaggerConfig.java').write_text(content, encoding='utf-8')

    # ==================== 前端代码生成 ====================
    def _generate_frontend(self):
        """生成前端代码"""
        frontend_dir = self.project_dir / 'frontend'
        src_dir = frontend_dir / 'src'

        for d in [src_dir / 'views', src_dir / 'router', src_dir / 'api', src_dir / 'utils']:
            d.mkdir(parents=True, exist_ok=True)

        self._gen_package_json(frontend_dir)
        self._gen_vite_config(frontend_dir)
        self._gen_index_html(frontend_dir)
        self._gen_main_js(src_dir)
        self._gen_app_vue(src_dir)
        self._gen_request_js(src_dir / 'utils')
        self._gen_router(src_dir / 'router')
        self._gen_api_files(src_dir / 'api')
        self._gen_vue_files(src_dir / 'views')

    def _gen_package_json(self, frontend_dir):
        """生成package.json"""
        content = '''{
  "name": "frontend",
  "version": "1.0.0",
  "private": true,
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "vue": "^3.3.4",
    "vue-router": "^4.2.4",
    "element-plus": "^2.3.14",
    "axios": "^1.5.0",
    "@element-plus/icons-vue": "^2.1.0"
  },
  "devDependencies": {
    "@vitejs/plugin-vue": "^4.3.4",
    "vite": "^4.4.9"
  }
}
'''
        (frontend_dir / 'package.json').write_text(content, encoding='utf-8')

    def _gen_vite_config(self, frontend_dir):
        """生成vite.config.js"""
        server = self.config.get('server', {})
        frontend_port = server.get('frontend_port', 5173)
        backend_port = server.get('backend_port', 8080)
        content = f'''import {{ defineConfig }} from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({{
  plugins: [vue()],
  server: {{
    port: {frontend_port},
    proxy: {{
      '/api': {{
        target: 'http://localhost:{backend_port}',
        changeOrigin: true
      }}
    }}
  }}
}})
'''
        (frontend_dir / 'vite.config.js').write_text(content, encoding='utf-8')

    def _gen_index_html(self, frontend_dir):
        """生成index.html"""
        desc = self.config.get('description', '信息管理系统')
        content = f'''<!DOCTYPE html>
<html lang="zh-CN">
  <head>
    <meta charset="UTF-8" />
    <link rel="icon" type="image/svg+xml" href="/vite.svg" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{desc}</title>
  </head>
  <body>
    <div id="app"></div>
    <script type="module" src="/src/main.js"></script>
  </body>
</html>
'''
        (frontend_dir / 'index.html').write_text(content, encoding='utf-8')

    def _gen_main_js(self, src_dir):
        """生成main.js"""
        content = '''import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'

const app = createApp(App)

// 注册所有图标
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}

app.use(router)
app.use(ElementPlus)
app.mount('#app')
'''
        (src_dir / 'main.js').write_text(content, encoding='utf-8')

    def _gen_app_vue(self, src_dir):
        """生成App.vue"""
        content = '''<template>
  <div id="app">
    <router-view />
  </div>
</template>

<style>
#app {
  font-family: 'Helvetica Neue', Helvetica, 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
</style>
'''
        (src_dir / 'App.vue').write_text(content, encoding='utf-8')

    def _gen_request_js(self, utils_dir):
        """生成request.js（axios封装）"""
        content = '''import axios from 'axios'
import { ElMessage } from 'element-plus'

const request = axios.create({
  baseURL: '/api',
  timeout: 10000
})

request.interceptors.request.use(
  config => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers['Authorization'] = 'Bearer ' + token
    }
    return config
  },
  error => Promise.reject(error)
)

request.interceptors.response.use(
  response => {
    const res = response.data
    if (res.code !== undefined && res.code !== 200) {
      ElMessage.error(res.message || '请求失败')
      return Promise.reject(new Error(res.message))
    }
    return res
  },
  error => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export default request
'''
        (utils_dir / 'request.js').write_text(content, encoding='utf-8')

    def _gen_router(self, router_dir):
        """生成路由配置"""
        business_routes = []
        for entity in self.config.get('entities', []):
            class_name = entity['name']
            var_name = class_name[0].lower() + class_name[1:]
            route_path = self._camel_to_snake(class_name) + 's'
            comment = entity.get('fields', [{}])[0].get('comment', class_name)[:4]
            business_routes.append(f"      {{ path: '{route_path}', name: '{class_name}Management', component: () => import('../views/{class_name}Management.vue'), meta: {{ title: '{comment}管理' }} }}")

        business_routes_str = ',\n'.join(business_routes)
        content = f'''import {{ createRouter, createWebHistory }} from 'vue-router'

const routes = [
  {{ path: '/login', name: 'Login', component: () => import('../views/Login.vue') }},
  {{
    path: '/',
    name: 'Layout',
    component: () => import('../views/Layout.vue'),
    redirect: '/users',
    children: [
      {{ path: 'users', name: 'UserManagement', component: () => import('../views/UserManagement.vue'), meta: {{ title: '用户管理' }} }},
      {{ path: 'roles', name: 'RoleManagement', component: () => import('../views/RoleManagement.vue'), meta: {{ title: '角色管理' }} }},
      {{ path: 'permissions', name: 'PermissionManagement', component: () => import('../views/PermissionManagement.vue'), meta: {{ title: '权限管理' }} }},
{business_routes_str}
    ]
  }}
]

const router = createRouter({{
  history: createWebHistory(),
  routes
}})

router.beforeEach((to, from, next) => {{
  const token = localStorage.getItem('token')
  if (to.path !== '/login' && !token) {{
    next('/login')
  }} else {{
    next()
  }}
}})

export default router
'''
        (router_dir / 'index.js').write_text(content, encoding='utf-8')

    def _gen_api_files(self, api_dir):
        """生成API接口文件"""
        # 生成业务实体API
        for entity in self.config.get('entities', []):
            class_name = entity['name']
            var_name = class_name[0].lower() + class_name[1:]
            api_path = self._camel_to_snake(class_name) + 's'

            api_content = f'''import request from '../utils/request'

export function get{class_name}List(params) {{
  return request({{
    url: '/{api_path}',
    method: 'get',
    params
  }})
}}

export function get{class_name}ById(id) {{
  return request({{
    url: '/{api_path}/' + id,
    method: 'get'
  }})
}}

export function create{class_name}(data) {{
  return request({{
    url: '/{api_path}',
    method: 'post',
    data
  }})
}}

export function update{class_name}(id, data) {{
  return request({{
    url: '/{api_path}/' + id,
    method: 'put',
    data
  }})
}}

export function delete{class_name}(id) {{
  return request({{
    url: '/{api_path}/' + id,
    method: 'delete'
  }})
}}
'''
            (api_dir / f'{var_name}.js').write_text(api_content, encoding='utf-8')

        # 生成RBAC API
        self._gen_rbac_api(api_dir)

    def _gen_rbac_api(self, api_dir):
        """生成RBAC API文件"""
        user_api = '''import request from '../utils/request'

export function getUserList(params) {
  return request({ url: '/users', method: 'get', params })
}
export function getUserById(id) {
  return request({ url: '/users/' + id, method: 'get' })
}
export function createUser(data) {
  return request({ url: '/users', method: 'post', data })
}
export function updateUser(id, data) {
  return request({ url: '/users/' + id, method: 'put', data })
}
export function deleteUser(id) {
  return request({ url: '/users/' + id, method: 'delete' })
}
export function login(data) {
  return request({ url: '/auth/login', method: 'post', data })
}
'''
        (api_dir / 'user.js').write_text(user_api, encoding='utf-8')

        role_api = '''import request from '../utils/request'

export function getRoleList(params) {
  return request({ url: '/roles', method: 'get', params })
}
export function getRoleById(id) {
  return request({ url: '/roles/' + id, method: 'get' })
}
export function createRole(data) {
  return request({ url: '/roles', method: 'post', data })
}
export function updateRole(id, data) {
  return request({ url: '/roles/' + id, method: 'put', data })
}
export function deleteRole(id) {
  return request({ url: '/roles/' + id, method: 'delete' })
}
'''
        (api_dir / 'role.js').write_text(role_api, encoding='utf-8')

        perm_api = '''import request from '../utils/request'

export function getPermissionList(params) {
  return request({ url: '/permissions', method: 'get', params })
}
export function getPermissionById(id) {
  return request({ url: '/permissions/' + id, method: 'get' })
}
export function createPermission(data) {
  return request({ url: '/permissions', method: 'post', data })
}
export function updatePermission(id, data) {
  return request({ url: '/permissions/' + id, method: 'put', data })
}
export function deletePermission(id) {
  return request({ url: '/permissions/' + id, method: 'delete' })
}
'''
        (api_dir / 'permission.js').write_text(perm_api, encoding='utf-8')

    def _gen_vue_files(self, views_dir):
        """生成Vue页面文件"""
        # 生成Login.vue和Layout.vue
        self._gen_login_vue(views_dir)
        self._gen_layout_vue(views_dir)

        # 生成RBAC管理页面
        self._gen_rbac_vue_files(views_dir)

        # 生成业务实体管理页面（带条件查询）
        for entity in self.config.get('entities', []):
            self._gen_business_page_optimized(entity, views_dir)

    def _gen_login_vue(self, views_dir):
        """生成登录页面"""
        content = '''<template>
  <div class="login-container">
    <el-card class="login-box">
      <template #header>
        <h2 class="login-title">系统登录</h2>
      </template>
      <el-form :model="loginForm" :rules="rules" ref="loginFormRef">
        <el-form-item prop="username">
          <el-input v-model="loginForm.username" placeholder="用户名" prefix-icon="User" size="large" />
        </el-form-item>
        <el-form-item prop="password">
          <el-input v-model="loginForm.password" type="password" placeholder="密码" prefix-icon="Lock" size="large" @keyup.enter="handleLogin" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" size="large" :loading="loading" @click="handleLogin" style="width: 100%">登录</el-button>
        </el-form-item>
      </el-form>
      <div class="login-tips">
        <p>默认账号: admin / 123456</p>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { login } from '../api/user'

const router = useRouter()
const loginFormRef = ref()
const loading = ref(false)
const loginForm = reactive({ username: '', password: '' })
const rules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }]
}

const handleLogin = async () => {
  await loginFormRef.value.validate()
  loading.value = true
  try {
    const res = await login(loginForm)
    if (res.code === 200) {
      localStorage.setItem('token', res.data.token)
      localStorage.setItem('user', JSON.stringify(res.data))
      ElMessage.success('登录成功')
      router.push('/')
    } else {
      ElMessage.error(res.message || '登录失败')
    }
  } catch (error) {
    ElMessage.error('登录请求失败')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-container {
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}
.login-box { width: 400px; }
.login-title { text-align: center; margin: 0; color: #303133; }
.login-tips { margin-top: 20px; padding-top: 20px; border-top: 1px solid #ebeef5; text-align: center; color: #909399; font-size: 12px; }
</style>
'''
        (views_dir / 'Login.vue').write_text(content, encoding='utf-8')

    def _gen_layout_vue(self, views_dir):
        """生成布局页面"""
        business_menus = []
        business_icons = ['Document', 'OfficeBuilding', 'Briefcase', 'Folder', 'Box']
        for i, entity in enumerate(self.config.get('entities', [])):
            class_name = entity['name']
            var_name = class_name[0].lower() + class_name[1:]
            route_path = self._camel_to_snake(class_name) + 's'
            comment = entity.get('fields', [{}])[0].get('comment', class_name)[:4]
            icon = business_icons[i % len(business_icons)]
            business_menus.append(f'        <el-menu-item index="/{route_path}"><el-icon><{icon} /></el-icon><span>{comment}管理</span></el-menu-item>')

        business_menus_str = '\n'.join(business_menus)

        content = f'''<template>
  <el-container class="layout-container">
    <el-aside width="200px" class="aside">
      <div class="logo">管理系统</div>
      <el-menu :default-active="$route.path" router class="el-menu-vertical"
        background-color="#304156" text-color="#bfcbd9" active-text-color="#409EFF">
        <el-menu-item index="/users"><el-icon><User /></el-icon><span>用户管理</span></el-menu-item>
        <el-menu-item index="/roles"><el-icon><Avatar /></el-icon><span>角色管理</span></el-menu-item>
        <el-menu-item index="/permissions"><el-icon><Key /></el-icon><span>权限管理</span></el-menu-item>
{business_menus_str}
      </el-menu>
    </el-aside>
    <el-container>
      <el-header class="header">
        <div class="header-right">
          <el-dropdown>
            <span class="user-info">{{{{ userInfo.username || '管理员' }}}}<el-icon><ArrowDown /></el-icon></span>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item @click="handleLogout">退出登录</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </el-header>
      <el-main class="main"><router-view /></el-main>
    </el-container>
  </el-container>
</template>

<script setup>
import {{ ref, onMounted }} from 'vue'
import {{ useRouter }} from 'vue-router'
import {{ ElMessage }} from 'element-plus'

const router = useRouter()
const userInfo = ref({{}})

onMounted(() => {{
  const user = localStorage.getItem('user')
  if (user) userInfo.value = JSON.parse(user)
}})

const handleLogout = () => {{
  localStorage.removeItem('token')
  localStorage.removeItem('user')
  ElMessage.success('退出成功')
  router.push('/login')
}}
</script>

<style scoped>
.layout-container {{ height: 100vh; }}
.aside {{ background-color: #304156; }}
.logo {{ height: 60px; line-height: 60px; text-align: center; color: #fff; font-size: 18px; font-weight: bold; border-bottom: 1px solid #1f2d3d; }}
.el-menu-vertical {{ border-right: none; }}
.header {{ background-color: #fff; box-shadow: 0 1px 4px rgba(0, 21, 41, 0.08); display: flex; align-items: center; justify-content: flex-end; }}
.header-right {{ cursor: pointer; }}
.user-info {{ color: #606266; font-size: 14px; }}
.main {{ background-color: #f0f2f5; padding: 20px; }}
</style>
'''
        (views_dir / 'Layout.vue').write_text(content, encoding='utf-8')

    def _gen_rbac_vue_files(self, views_dir):
        """生成RBAC管理页面（用户/角色/权限）"""
        rbac_configs = [
            {
                'name': 'UserManagement',
                'title': '用户',
                'apiName': 'User',
                'apiFile': 'user',
                'fields': [
                    ('username', '用户名', 'text', True),
                    ('realName', '真实姓名', 'text', True),
                    ('email', '邮箱', 'text', True),
                    ('phone', '电话', 'text', True),
                    ('status', '状态', 'status', True)
                ]
            },
            {
                'name': 'RoleManagement',
                'title': '角色',
                'apiName': 'Role',
                'apiFile': 'role',
                'fields': [
                    ('roleCode', '角色编码', 'text', True),
                    ('roleName', '角色名称', 'text', True),
                    ('description', '描述', 'text', False),
                    ('status', '状态', 'status', True)
                ]
            },
            {
                'name': 'PermissionManagement',
                'title': '权限',
                'apiName': 'Permission',
                'apiFile': 'permission',
                'fields': [
                    ('permissionCode', '权限编码', 'text', True),
                    ('permissionName', '权限名称', 'text', True),
                    ('type', '类型', 'text', True),
                    ('path', '路径', 'text', False),
                    ('status', '状态', 'status', True)
                ]
            }
        ]

        for config in rbac_configs:
            self._gen_rbac_page(views_dir, config)

    def _gen_rbac_page(self, views_dir, config):
        """生成单个RBAC管理页面"""
        page_name = config['name']
        title = config['title']
        api_name = config['apiName']
        api_file = config['apiFile']
        fields = config['fields']

        # 生成表格列
        table_cols = []
        for field_name, field_label, field_type, _ in fields:
            if field_type == 'status':
                table_cols.append(f'''        <el-table-column prop="{field_name}" label="{field_label}" width="100" align="center">
          <template #default="scope">
            <el-tag :type="scope.row.{field_name} === 1 ? 'success' : 'danger'">
              {{{{ scope.row.{field_name} === 1 ? '启用' : '禁用' }}}}
            </el-tag>
          </template>
        </el-table-column>''')
            else:
                table_cols.append(f'        <el-table-column prop="{field_name}" label="{field_label}" show-overflow-tooltip />')
        table_columns_str = '\n'.join(table_cols)

        # 生成查询表单字段
        search_items = []
        for field_name, field_label, field_type, searchable in fields:
            if searchable and field_type != 'status':
                search_items.append(f'''        <el-form-item label="{field_label}">
          <el-input v-model="searchForm.{field_name}" placeholder="请输入{field_label}" clearable />
        </el-form-item>''')
            elif searchable and field_type == 'status':
                search_items.append(f'''        <el-form-item label="{field_label}">
          <el-select v-model="searchForm.{field_name}" placeholder="全部状态" clearable style="width: 120px">
            <el-option :value="1" label="启用" />
            <el-option :value="0" label="禁用" />
          </el-select>
        </el-form-item>''')
        search_form_items = '\n'.join(search_items)

        # 生成表单字段
        form_items = []
        for field_name, field_label, field_type, _ in fields:
            if field_type == 'status':
                form_items.append(f'''        <el-form-item label="{field_label}" prop="{field_name}">
          <el-select v-model="formData.{field_name}" placeholder="请选择{field_label}" style="width: 100%">
            <el-option :value="1" label="启用" />
            <el-option :value="0" label="禁用" />
          </el-select>
        </el-form-item>''')
            else:
                form_items.append(f'''        <el-form-item label="{field_label}" prop="{field_name}">
          <el-input v-model="formData.{field_name}" placeholder="请输入{field_label}" />
        </el-form-item>''')
        form_items_str = '\n'.join(form_items)

        # 生成详情查看项
        view_items = []
        for field_name, field_label, field_type, _ in fields:
            if field_type == 'status':
                view_items.append(f'        <el-descriptions-item label="{field_label}">{{{{ formData.{field_name} === 1 ? \'启用\' : \'禁用\' }}}}</el-descriptions-item>')
            else:
                view_items.append(f'        <el-descriptions-item label="{field_label}">{{{{ formData.{field_name} }}}}</el-descriptions-item>')
        view_items_str = '\n'.join(view_items)

        # 生成查询表单初始化
        search_init = ',\n'.join([f"  {f[0]}: ''" for f in fields])
        # 生成表单初始化
        form_init = ',\n'.join([f"  {f[0]}: {1 if f[2] == 'status' else "''"}" for f in fields])
        # 生成重置代码
        reset_code = '\n'.join([f"  searchForm.{f[0]} = {1 if f[2] == 'status' else "''"}" for f in fields])
        # 生成表单验证规则
        form_rules = ',\n'.join([f"  {f[0]}: [{{ required: true, message: '请输入{f[1]}', trigger: 'blur' }}]" for f in fields])

        content = f'''<template>
  <div class="management">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>{title}管理</span>
          <el-button type="primary" @click="handleAdd" :icon="Plus">新增</el-button>
        </div>
      </template>

      <!-- 条件查询区域 -->
      <el-form :inline="true" :model="searchForm" class="search-form">
{search_form_items}
        <el-form-item>
          <el-button type="primary" @click="handleSearch" :icon="Search">查询</el-button>
          <el-button @click="handleReset" :icon="RefreshRight">重置</el-button>
        </el-form-item>
      </el-form>

      <!-- 数据表格 -->
      <el-table :data="list" style="width: 100%" v-loading="loading" border>
        <el-table-column prop="id" label="ID" width="80" align="center" />
{table_columns_str}
        <el-table-column label="操作" width="220" fixed="right" align="center">
          <template #default="scope">
            <el-button size="small" @click="handleView(scope.row)" :icon="View">查看</el-button>
            <el-button size="small" type="primary" @click="handleEdit(scope.row)" :icon="Edit">编辑</el-button>
            <el-button size="small" type="danger" @click="handleDelete(scope.row)" :icon="Delete">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <el-pagination
        v-model:current-page="pagination.current"
        v-model:page-size="pagination.size"
        :total="pagination.total"
        :page-sizes="[10, 20, 50, 100]"
        layout="total, sizes, prev, pager, next, jumper"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
        class="pagination"
      />
    </el-card>

    <!-- 新增/编辑对话框 -->
    <el-dialog v-model="dialogVisible" :title="dialogTitle" width="600px" destroy-on-close>
      <el-form :model="formData" ref="formRef" label-width="100px" :rules="formRules">
{form_items_str}
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit" :loading="submitLoading">确定</el-button>
      </template>
    </el-dialog>

    <!-- 查看详情对话框 -->
    <el-dialog v-model="viewDialogVisible" title="查看详情" width="600px" destroy-on-close>
      <el-descriptions :column="1" border>
        <el-descriptions-item label="ID">{{{{ formData.id }}}}</el-descriptions-item>
{view_items_str}
        <el-descriptions-item label="创建时间">{{{{ formData.createTime }}}}</el-descriptions-item>
        <el-descriptions-item label="更新时间">{{{{ formData.updateTime }}}}</el-descriptions-item>
      </el-descriptions>
      <template #footer>
        <el-button @click="viewDialogVisible = false">关闭</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import {{ ref, reactive, onMounted }} from 'vue'
import {{ ElMessage, ElMessageBox }} from 'element-plus'
import {{ Plus, Search, RefreshRight, View, Edit, Delete }} from '@element-plus/icons-vue'
import {{
  get{api_name}List,
  get{api_name}ById,
  create{api_name},
  update{api_name},
  delete{api_name}
}} from '../api/{api_file}'

const loading = ref(false)
const list = ref([])
const dialogVisible = ref(false)
const viewDialogVisible = ref(false)
const dialogTitle = ref('新增')
const isEdit = ref(false)
const submitLoading = ref(false)
const formRef = ref()

const pagination = reactive({{
  current: 1,
  size: 10,
  total: 0
}})

const searchForm = reactive({{
{search_init}
}})

const formData = ref({{
{form_init}
}})

const formRules = {{
{form_rules}
}}

const loadData = async () => {{
  loading.value = true
  try {{
    const params = {{
      current: pagination.current,
      size: pagination.size,
      ...searchForm
    }}
    const res = await get{api_name}List(params)
    list.value = res.records || res.data?.records || []
    pagination.total = res.total || res.data?.total || 0
  }} catch (error) {{
    ElMessage.error('加载数据失败')
  }} finally {{
    loading.value = false
  }}
}}

const handleSearch = () => {{
  pagination.current = 1
  loadData()
}}

const handleReset = () => {{
{reset_code}
  pagination.current = 1
  loadData()
}}

const handleSizeChange = (size) => {{
  pagination.size = size
  loadData()
}}

const handleCurrentChange = (current) => {{
  pagination.current = current
  loadData()
}}

const handleAdd = () => {{
  isEdit.value = false
  dialogTitle.value = '新增'
  formData.value = {{
{form_init}
  }}
  dialogVisible.value = true
}}

const handleView = async (row) => {{
  try {{
    const res = await get{api_name}ById(row.id)
    formData.value = res
    viewDialogVisible.value = true
  }} catch (error) {{
    ElMessage.error('获取详情失败')
  }}
}}

const handleEdit = (row) => {{
  isEdit.value = true
  dialogTitle.value = '编辑'
  formData.value = {{ ...row }}
  dialogVisible.value = true
}}

const handleDelete = async (row) => {{
  try {{
    await ElMessageBox.confirm('确定要删除该{title}吗？删除后不可恢复！', '确认删除', {{
      type: 'warning',
      confirmButtonText: '确定',
      cancelButtonText: '取消'
    }})
    await delete{api_name}(row.id)
    ElMessage.success('删除成功')
    loadData()
  }} catch (error) {{
    if (error !== 'cancel') ElMessage.error('删除失败')
  }}
}}

const handleSubmit = async () => {{
  try {{
    await formRef.value.validate()
  }} catch {{
    return
  }}
  submitLoading.value = true
  try {{
    if (isEdit.value) {{
      await update{api_name}(formData.value.id, formData.value)
      ElMessage.success('更新成功')
    }} else {{
      await create{api_name}(formData.value)
      ElMessage.success('创建成功')
    }}
    dialogVisible.value = false
    loadData()
  }} catch (error) {{
    ElMessage.error(isEdit.value ? '更新失败' : '创建失败')
  }} finally {{
    submitLoading.value = false
  }}
}}

onMounted(loadData)
</script>

<style scoped>
.management {{
  padding: 20px;
}}

.card-header {{
  display: flex;
  justify-content: space-between;
  align-items: center;
}}

.search-form {{
  margin-bottom: 20px;
  padding: 20px;
  background-color: #f5f7fa;
  border-radius: 4px;
}}

.pagination {{
  margin-top: 20px;
  justify-content: flex-end;
}}
</style>
'''
        (views_dir / f'{page_name}.vue').write_text(content, encoding='utf-8')

    def _gen_business_page_optimized(self, entity, views_dir):
        """生成优化的业务实体管理页面（带条件查询）"""
        class_name = entity['name']
        var_name = class_name[0].lower() + class_name[1:]
        fields = entity.get('fields', [])
        comment = fields[0].get('comment', class_name)[:4] if fields else class_name

        # 生成表格列（所有字段）
        table_columns = []
        for f in fields:
            fname = f['name']
            fcomment = f.get('comment', fname)
            ftype = f['type']
            # 状态字段特殊显示
            if fname.lower() == 'status':
                table_columns.append(f'''        <el-table-column prop="{fname}" label="{fcomment}" width="100" align="center">
          <template #default="scope">
            <el-tag :type="scope.row.{fname} === 1 ? 'success' : 'danger'">
              {{{{ scope.row.{fname} === 1 ? '启用' : '禁用' }}}}
            </el-tag>
          </template>
        </el-table-column>''')
            else:
                table_columns.append(f'        <el-table-column prop="{fname}" label="{fcomment}" show-overflow-tooltip />')
        table_columns_str = '\n'.join(table_columns)

        # 生成查询表单字段（支持搜索的字段）
        search_items = []
        for f in fields:
            fname = f['name']
            fcomment = f.get('comment', fname)
            ftype = f['type']
            # 状态字段使用下拉选择
            if fname.lower() == 'status':
                search_items.append(f'''        <el-form-item label="{fcomment}">
          <el-select v-model="searchForm.{fname}" placeholder="全部{fcomment}" clearable style="width: 120px">
            <el-option :value="1" label="启用" />
            <el-option :value="0" label="禁用" />
          </el-select>
        </el-form-item>''')
            elif ftype == 'String':
                search_items.append(f'''        <el-form-item label="{fcomment}">
          <el-input v-model="searchForm.{fname}" placeholder="请输入{fcomment}" clearable />
        </el-form-item>''')
        search_form_items = '\n'.join(search_items) if search_items else '        <!-- 暂无查询条件 -->'

        # 生成表单字段（所有字段）
        form_items = []
        for f in fields:
            fname = f['name']
            fcomment = f.get('comment', fname)
            ftype = f['type']
            # 状态字段使用下拉选择（枚举方式）
            if fname.lower() == 'status':
                form_items.append(f'''        <el-form-item label="{fcomment}" prop="{fname}">
          <el-select v-model="formData.{fname}" placeholder="请选择{fcomment}" style="width: 100%">
            <el-option :value="1" label="启用" />
            <el-option :value="0" label="禁用" />
          </el-select>
        </el-form-item>''')
            else:
                input_type = 'number' if ftype in ['Long', 'Integer', 'BigDecimal'] else 'text'
                form_items.append(f'''        <el-form-item label="{fcomment}" prop="{fname}">
          <el-input v-model="formData.{fname}" type="{input_type}" placeholder="请输入{fcomment}" />
        </el-form-item>''')
        form_items_str = '\n'.join(form_items)

        # 生成详情查看项
        view_items = []
        for f in fields:
            fname = f['name']
            fcomment = f.get('comment', fname)
            if fname.lower() == 'status':
                view_items.append(f'        <el-descriptions-item label="{fcomment}">{{{{ formData.{fname} === 1 ? \'启用\' : \'禁用\' }}}}</el-descriptions-item>')
            else:
                view_items.append(f'        <el-descriptions-item label="{fcomment}">{{{{ formData.{fname} }}}}</el-descriptions-item>')
        view_items_str = '\n'.join(view_items)

        # 生成查询表单初始化
        search_init_lines = []
        for f in fields:
            fname = f['name']
            ftype = f['type']
            default_val = '1' if fname.lower() == 'status' else ("''" if ftype == 'String' else 'null')
            search_init_lines.append(f'  {fname}: {default_val}')
        search_form_init = '\n'.join(search_init_lines)

        # 生成表单初始化
        form_init_lines = []
        for f in fields:
            fname = f['name']
            ftype = f['type']
            default_val = '1' if fname.lower() == 'status' else ("''" if ftype == 'String' else 'null')
            form_init_lines.append(f'  {fname}: {default_val}')
        form_init = '\n'.join(form_init_lines)

        # 生成重置代码
        reset_lines = []
        for f in fields:
            fname = f['name']
            ftype = f['type']
            default_val = '1' if fname.lower() == 'status' else ("''" if ftype == 'String' else 'null')
            reset_lines.append(f'  searchForm.{fname} = {default_val}')
        reset_code = '\n'.join(reset_lines)

        # 生成表单验证规则
        rules_lines = []
        for f in fields:
            fname = f['name']
            fcomment = f.get('comment', fname)
            ftype = f['type']
            trigger = 'change' if fname.lower() == 'status' else 'blur'
            rules_lines.append(f'  {fname}: [{{ required: true, message: "请输入{fcomment}", trigger: "{trigger}" }}]')
        form_rules = ',\n'.join(rules_lines)

        # 使用模板填充
        content = VUE_PAGE_TEMPLATE.format(
            comment=comment,
            class_name=class_name,
            var_name=var_name,
            search_form_items=search_form_items,
            table_columns=table_columns_str,
            form_items=form_items_str,
            view_items=view_items_str,
            search_form_init=search_form_init,
            form_init=form_init,
            reset_code=reset_code,
            form_rules=form_rules
        )

        (views_dir / f'{class_name}Management.vue').write_text(content, encoding='utf-8')

    # ==================== SQL生成 ====================
    def _generate_sql(self):
        """生成数据库初始化SQL"""
        db_dir = self.project_dir / 'backend' / 'src' / 'main' / 'resources' / 'db'
        db_dir.mkdir(parents=True, exist_ok=True)
        db_name = self.config.get('database', {}).get('name', 'test')

        sql_content = self._get_base_sql(db_name)

        for entity in self.config.get('entities', []):
            sql_content += '\n' + self._gen_table_sql(entity)

        (db_dir / 'init.sql').write_text(sql_content, encoding='utf-8')

    def _get_base_sql(self, db_name):
        """获取基础SQL"""
        return f'''CREATE DATABASE IF NOT EXISTS {db_name};
USE {db_name};

DROP TABLE IF EXISTS sys_user;
CREATE TABLE sys_user (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(100) NOT NULL,
    real_name VARCHAR(50),
    email VARCHAR(100),
    phone VARCHAR(20),
    avatar VARCHAR(255),
    status TINYINT DEFAULT 1,
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    update_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

DROP TABLE IF EXISTS sys_role;
CREATE TABLE sys_role (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    role_code VARCHAR(50) NOT NULL UNIQUE,
    role_name VARCHAR(50) NOT NULL,
    description VARCHAR(255),
    status TINYINT DEFAULT 1,
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    update_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

DROP TABLE IF EXISTS sys_permission;
CREATE TABLE sys_permission (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    permission_code VARCHAR(100) NOT NULL UNIQUE,
    permission_name VARCHAR(50) NOT NULL,
    parent_id BIGINT DEFAULT 0,
    type VARCHAR(20) DEFAULT 'menu',
    path VARCHAR(255),
    method VARCHAR(20),
    icon VARCHAR(50),
    sort_order INT DEFAULT 0,
    status TINYINT DEFAULT 1,
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    update_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

DROP TABLE IF EXISTS sys_user_role;
CREATE TABLE sys_user_role (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    user_id BIGINT NOT NULL,
    role_id BIGINT NOT NULL,
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY uk_user_role (user_id, role_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

DROP TABLE IF EXISTS sys_role_permission;
CREATE TABLE sys_role_permission (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    role_id BIGINT NOT NULL,
    permission_id BIGINT NOT NULL,
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY uk_role_permission (role_id, permission_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO sys_user (id, username, password, real_name, email, status) VALUES
(1, 'admin', '$2a$10$N.zmdr9k7uOCQb376NoUnuTJ8iAt6Z5EHsM8lE9lBOsl7iKTVKIUi', '超级管理员', 'admin@example.com', 1),
(2, 'user', '$2a$10$N.zmdr9k7uOCQb376NoUnuTJ8iAt6Z5EHsM8lE9lBOsl7iKTVKIUi', '普通用户', 'user@example.com', 1);

INSERT INTO sys_role (id, role_code, role_name, description) VALUES
(1, 'admin', '超级管理员', '拥有系统所有权限'),
(2, 'user', '普通用户', '基础操作权限');

INSERT INTO sys_permission (id, permission_code, permission_name, type, path, icon) VALUES
(1, 'system:manage', '系统管理', 'menu', '/system', 'Setting'),
(2, 'system:user', '用户管理', 'menu', '/system/users', 'User'),
(3, 'system:role', '角色管理', 'menu', '/system/roles', 'Avatar');

INSERT INTO sys_user_role (user_id, role_id) VALUES (1, 1), (2, 2);
INSERT INTO sys_role_permission (role_id, permission_id) VALUES (1, 1), (1, 2), (1, 3), (2, 1);
'''

    def _gen_table_sql(self, entity):
        """生成业务表SQL"""
        table = self._camel_to_snake(entity['name'])
        fields_sql = ',\n'.join([
            f"    {self._camel_to_snake(f['name'])} {self._sql_type(f['type'])}"
            for f in entity.get('fields', [])
        ])
        return f'''
DROP TABLE IF EXISTS {table};
CREATE TABLE {table} (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
{fields_sql},
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    update_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
'''

    # ==================== 部署步骤 ====================
    def step_check_ports(self):
        """检查端口占用"""
        print(f"\n{Colors.BOLD}[STEP] 3/9 - 检查端口占用{Colors.RESET}")
        import socket
        server = self.config.get('server', {})
        ports = [
            ("后端", server.get('backend_port', 8080)),
            ("前端", server.get('frontend_port', 5173))
        ]
        all_free = True
        for name, port in ports:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.bind(('localhost', port))
                    print(f"{Colors.GREEN}[SUCCESS] {name}端口 {port} 可用{Colors.RESET}")
            except socket.error:
                print(f"{Colors.RED}[ERROR] {name}端口 {port} 被占用{Colors.RESET}")
                all_free = False
        return all_free

    def step_test_database(self):
        """测试数据库连接"""
        print(f"\n{Colors.BOLD}[STEP] 4/9 - 测试数据库连接{Colors.RESET}")
        try:
            import pymysql
            db = self.config.get('database', {})
            conn = pymysql.connect(
                host=db.get('host', 'localhost'),
                port=int(db.get('port', 3306)),
                user=db.get('user', 'root'),
                password=db.get('password', ''),
                connect_timeout=5
            )
            conn.close()
            print(f"{Colors.GREEN}[SUCCESS] 数据库连接成功{Colors.RESET}")
            return True
        except ImportError:
            print(f"{Colors.RED}[ERROR] 请先安装pymysql: pip install pymysql{Colors.RESET}")
            return False
        except Exception as e:
            print(f"{Colors.RED}[ERROR] 数据库连接失败: {e}{Colors.RESET}")
            return False

    def step_execute_sql(self):
        """执行数据库初始化"""
        print(f"\n{Colors.BOLD}[STEP] 5/9 - 执行数据库初始化{Colors.RESET}")
        sql_file = self.project_dir / 'backend' / 'src' / 'main' / 'resources' / 'db' / 'init.sql'
        if not sql_file.exists():
            print(f"{Colors.YELLOW}[WARNING] SQL文件不存在{Colors.RESET}")
            return True

        try:
            import pymysql
            db = self.config.get('database', {})
            conn = pymysql.connect(
                host=db.get('host', 'localhost'),
                port=int(db.get('port', 3306)),
                user=db.get('user', 'root'),
                password=db.get('password', ''),
                autocommit=True
            )
            cursor = conn.cursor()
            sql_content = sql_file.read_text(encoding='utf-8')

            # 执行SQL
            statements = [s.strip() for s in sql_content.split(';') if s.strip()]
            success, skip, error = 0, 0, 0
            for stmt in statements:
                try:
                    cursor.execute(stmt)
                    success += 1
                except Exception as e:
                    err_str = str(e).lower()
                    if 'already exists' in err_str or 'duplicate' in err_str:
                        skip += 1
                    else:
                        error += 1

            conn.close()
            print(f"{Colors.GREEN}[SUCCESS] 数据库初始化完成 ({success}成功, {skip}跳过, {error}错误){Colors.RESET}")
            return True
        except Exception as e:
            print(f"{Colors.RED}[ERROR] SQL执行失败: {e}{Colors.RESET}")
            return False

    def step_build_backend(self):
        """构建后端项目"""
        print(f"\n{Colors.BOLD}[STEP] 6/9 - 构建后端项目{Colors.RESET}")
        backend_dir = self.project_dir / 'backend'
        target_dir = backend_dir / 'target'
        if target_dir.exists() and list(target_dir.glob('*.jar')):
            print(f"{Colors.YELLOW}[WARNING] 检测到已构建的JAR包，跳过构建{Colors.RESET}")
            return True

        mvn_path = self.tool_paths.get('mvn')
        if not mvn_path:
            print(f"{Colors.RED}[ERROR] 未找到Maven{Colors.RESET}")
            return False

        try:
            result = subprocess.run(f'"{mvn_path}" clean package -DskipTests -q',
                                   cwd=backend_dir, shell=True, capture_output=True, timeout=300)
            if result.returncode == 0:
                print(f"{Colors.GREEN}[SUCCESS] 后端构建成功{Colors.RESET}")
                return True
            else:
                print(f"{Colors.RED}[ERROR] 后端构建失败{Colors.RESET}")
                return False
        except Exception as e:
            print(f"{Colors.RED}[ERROR] 构建异常: {e}{Colors.RESET}")
            return False

    def step_build_frontend(self):
        """安装前端依赖"""
        print(f"\n{Colors.BOLD}[STEP] 7/9 - 安装前端依赖{Colors.RESET}")
        frontend_dir = self.project_dir / 'frontend'
        if (frontend_dir / 'node_modules').exists():
            print(f"{Colors.YELLOW}[WARNING] 检测到node_modules，跳过安装{Colors.RESET}")
            return True

        npm_path = self.tool_paths.get('npm')
        if not npm_path:
            print(f"{Colors.RED}[ERROR] 未找到NPM{Colors.RESET}")
            return False

        try:
            result = subprocess.run(f'"{npm_path}" install',
                                   cwd=frontend_dir, shell=True, capture_output=True, timeout=180)
            if result.returncode == 0:
                print(f"{Colors.GREEN}[SUCCESS] 前端依赖安装成功{Colors.RESET}")
                return True
            else:
                print(f"{Colors.RED}[ERROR] 前端依赖安装失败{Colors.RESET}")
                return False
        except Exception as e:
            print(f"{Colors.RED}[ERROR] 安装异常: {e}{Colors.RESET}")
            return False

    def step_start_backend(self):
        """启动后端服务"""
        print(f"\n{Colors.BOLD}[STEP] 8/9 - 启动后端服务{Colors.RESET}")
        backend_dir = self.project_dir / 'backend'
        jar_files = list((backend_dir / 'target').glob('*.jar'))
        if not jar_files:
            print(f"{Colors.RED}[ERROR] 未找到JAR包{Colors.RESET}")
            return False

        backend_port = self.config.get('server', {}).get('backend_port', 8080)
        jar_file = jar_files[0].name
        bat_content = f'''@echo off
title 后端服务 - {backend_port}
cd /d "{backend_dir}"
echo 正在启动后端服务...
echo 端口: {backend_port}
echo.
java -jar target\\{jar_file} --server.port={backend_port}
echo.
echo 后端服务已停止
pause
'''
        bat_path = backend_dir / 'start-backend.bat'
        bat_path.write_text(bat_content, encoding='gbk')
        os.system(f'start "" "{bat_path}"')
        print(f"{Colors.GREEN}[SUCCESS] 后端服务已在新窗口启动{Colors.RESET}")
        return True

    def step_start_frontend(self):
        """启动前端服务"""
        print(f"\n{Colors.BOLD}[STEP] 9/9 - 启动前端服务并打开浏览器{Colors.RESET}")
        frontend_dir = self.project_dir / 'frontend'
        npm_path = self.tool_paths.get('npm') or 'npm'
        frontend_port = self.config.get('server', {}).get('frontend_port', 5173)

        bat_content = f'''@echo off
title 前端服务 - {frontend_port}
cd /d "{frontend_dir}"
echo 正在启动前端服务...
echo 端口: {frontend_port}
echo.
"{npm_path}" run dev -- --port {frontend_port}
echo.
echo 前端服务已停止
pause
'''
        bat_path = frontend_dir / 'start-frontend.bat'
        bat_path.write_text(bat_content, encoding='gbk')
        os.system(f'start "" "{bat_path}"')
        print(f"{Colors.GREEN}[SUCCESS] 前端服务已在新窗口启动{Colors.RESET}")

        time.sleep(5)
        try:
            import webbrowser
            webbrowser.open(f'http://localhost:{frontend_port}/login', new=2)
            print(f"{Colors.GREEN}[SUCCESS] 浏览器已打开{Colors.RESET}")
        except:
            print(f"{Colors.CYAN}[INFO] 请手动访问: http://localhost:{frontend_port}/login{Colors.RESET}")
        return True

    # ==================== 工具方法 ====================
    def _java_type(self, type_str):
        """映射Java类型"""
        return JAVA_TYPE_MAP.get(type_str, 'String')

    def _sql_type(self, type_str):
        """映射SQL类型"""
        return SQL_TYPE_MAP.get(type_str, 'VARCHAR(255)')

    def _camel_to_snake(self, name):
        """驼峰命名转下划线命名"""
        import re
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def main():
    """主入口"""
    if len(sys.argv) < 2:
        print("使用方法: python optimized-start-win.py <config.json>")
        sys.exit(1)

    config_file = Path(sys.argv[1])
    if not config_file.exists():
        print(f"配置文件不存在: {config_file}")
        sys.exit(1)

    with open(config_file, 'r', encoding='utf-8') as f:
        config = json.load(f)

    starter = ProjectStarter(config)
    success = starter.start()
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
