---
name: "junit-test-generator"
description: "Generates JUnit 5 test classes from JSON test case files. Invoke when user wants to generate Spring Boot JUnit 5 tests from JSON test cases."
---

# JUnit 5 Test Generator

LLM驱动的JUnit 5测试代码生成系统。读取由"Test Case Generator"生成的JSON格式测试用例，自动生成符合Spring Boot最佳实践和JUnit 5规范的测试类和测试方法。

## 核心功能

1. **JSON解析** - 解析测试用例JSON文件，提取测试数据、预期结果和元数据
2. **测试类生成** - 基于测试套件生成完整的JUnit 5测试类
3. **测试方法生成** - 为每个测试用例生成对应的@Test方法
4. **批量导入** - 支持批量处理多个测试用例文件
5. **多场景支持** - 支持API接口测试、服务层测试等多种测试类型
6. **SQL自动执行** - 自动执行setup/teardown中的MySQL SQL语句

## 工作流程

```
┌─────────────────────────────────────────────────────────────┐
│                      LLM 智能层                             │
│  ┌─────────────────┐    ┌─────────────────────────────┐ │
│  │ 解析JSON测试用例  │ -> │ 分析测试类型和结构           │ │
│  └─────────────────┘    └─────────────────────────────┘ │
│  ┌─────────────────┐    ┌─────────────────────────────┐ │
│  │ 生成测试类模板    │ -> │ 生成测试方法实现             │ │
│  └─────────────────┘    └─────────────────────────────┘ │
│  ┌─────────────────────────────────────────────────────┐ │
│  │ 生成完整的JUnit 5测试代码                              │ │
│  └─────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                       Python 执行层                          │
│  ┌──────────────────────┐    ┌──────────────────────────┐ │
│  │ run_generator.py      │    │ testcase_parser.py        │ │
│  │ 入口脚本(一键执行)     │    │ 测试用例JSON解析器        │ │
│  └──────────────────────┘    └──────────────────────────┘ │
│  ┌──────────────────────┐    ┌──────────────────────────┐ │
│  │ jtest_generator.py    │    │                          │ │
│  │ JUnit 5测试代码生成器   │    │                          │ │
│  └──────────────────────┘    └──────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```
## 何时被调用
- 当已经有"TestCase Generator"这个skill生成的JSON格式测试用例文件时，调用此skill生成对应的JUnit 5测试类。
- "TestCase Generator"这个skill主动调用此skill，生成对应的JUnit 5测试类。


## 输入JSON格式

```json
{
  "test_suite": "ControllerName_MethodName",
  "description": "接口功能描述",
  "interface_info": {
    "endpoint": "/api/path",
    "method": "POST",
    "content_type": "application/json",
    "function": "接口功能说明"
  },
  "request_dto": {
    "field1": "类型 - 字段说明"
  },
  "test_cases": [
    {
      "id": "TC_001",
      "name": "测试场景描述",
      "endpoint": "/api/path",
      "method": "POST",
      "headers": {"Content-Type": "application/json"},
      "body": {"field1": "value1"},
      "setup": {"mysql": [], "redis": {}},
      "expected": {"status": 200, "body": {"key": "value"}},
      "teardown": {"mysql": [], "redis": []}
    }
  ]
}
```

## 生成的测试类结构

```java
package generated.tests.controller;

import com.fasterxml.jackson.databind.ObjectMapper;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.MvcResult;
import org.springframework.jdbc.core.JdbcTemplate;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.HashMap;
import java.util.Map;

import static org.junit.jupiter.api.Assertions.*;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@SpringBootTest
@AutoConfigureMockMvc
class ControllerNameMethodNameTest {

    private static final Logger logger = LoggerFactory.getLogger(ControllerNameMethodNameTest.class);

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private ObjectMapper objectMapper;

    @Autowired
    private JdbcTemplate jdbcTemplate;

    @Test
    void testMethodName_TC_001() throws Exception {
        logger.info("Executing test: TC_001 - 测试场景描述");

        // Setup - 准备测试数据
        // jdbcTemplate.execute("INSERT INTO ...");

        // Given - 构建请求
        Map<String, Object> requestBody = new HashMap<>();
        requestBody.put("field1", "value1");

        // When & Then - 执行请求并验证
        mockMvc.perform(post("/api/path")
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(requestBody)))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.key").value("value"))
            .andDo(print());

        // Teardown - 清理测试数据
        // jdbcTemplate.execute("DELETE FROM ...");
    }
}
```

## 测试类型支持

| 测试类型 | 注解 | 说明 |
|---------|------|------|
| API接口测试 | `@SpringBootTest @AutoConfigureMockMvc` | Controller层测试 |
| 服务层测试 | `@SpringBootTest` | Service层测试 |
| 单元测试 | `@ExtendWith(MockitoExtension.class)` | 纯单元测试 |
| 集成测试 | `@SpringBootTest` | 完整集成测试 |

## 使用方法

### 方式一: 使用入口脚本（推荐）

```bash
# 进入skill目录
cd .trae/skills/junit-test-generator/scripts

# 一键生成测试类
python run_generator.py <test_cases.json> [output_dir]

# 示例
python run_generator.py test_cases.json
python run_generator.py test_cases.json src/test/java
```

### 方式二: Python API调用

```python
from jtest_generator import JUnitTestGenerator

generator = JUnitTestGenerator(package_name="your.package.name")
java_code = generator.generate(test_suite)
```

## 完整测试执行流程

```
┌─────────────────────────────────────────────────────────────┐
│                    完整测试执行流程                            │
├─────────────────────────────────────────────────────────────┤
│  1. testcase-generator: 生成测试用例JSON                     │
│             ↓                                                │
│  2. 本skill: 解析JSON并生成JUnit 5测试类                     │
│             ↓                                                │
│  3. 写入 src/test/java 目录                                 │
│             ↓                                                │
│  4. mvn test [-Dtest=ClassName] 执行测试                    │
│             ↓                                                │
│  5. 查看 target/surefire-reports/ 测试结果                  │
└─────────────────────────────────────────────────────────────┘
```

## Maven测试命令

| 命令 | 说明 |
|------|------|
| `mvn test` | 执行所有测试 |
| `mvn test -Dtest=ClassName` | 执行指定测试类 |
| `mvn test -Dtest=ClassName#methodName` | 执行指定测试方法 |
| `mvn test -Dspring.profiles.active=test` | 使用test配置执行 |
| `mvn test verify` | 执行测试并验证 |

## 测试结果查看

- `target/surefire-reports/` - 测试执行报告 (XML/TXT)
- 控制台直接输出测试结果

## 生成的代码规范

- **包名**: 可配置，默认 `generated.tests.controller`
- **类名**: PascalCase + "Test"后缀，**自动移除中文字符和非ASCII字符**
- **方法名**: `test` + 操作描述 + 场景描述
- **断言**: 使用`assertEquals`, `assertTrue`, `jsonPath`等
- **注释**: 包含测试用例ID和描述
- **Endpoint**: 自动清理context-path（如果路径段数>2）

## LLM提示词模板

### 测试代码生成提示词

```
你是一个测试工程师。请根据以下JSON测试用例，生成符合JUnit 5规范的Spring Boot测试代码。

## 测试套件信息
- 测试套件名: {test_suite_name}
- 描述: {description}
- 接口路径: {endpoint}
- HTTP方法: {method}

## 测试用例数据
{test_cases_json}

## 生成要求
1. 使用JUnit 5注解 (@Test, @BeforeEach, @AfterEach)
2. 使用@SpringBootTest和@AutoConfigureMockMvc进行API测试
3. 使用MockMvc进行HTTP请求模拟
4. 使用jsonPath进行响应断言
5. 在测试方法注释中包含测试用例ID和描述
6. 遵循Spring Boot最佳实践

请生成完整的Java测试类代码。
```

## 质量标准

- ✅ 生成的测试类符合JUnit 5规范
- ✅ 支持Spring Boot `@SpringBootTest` 集成测试
- ✅ 支持`@WebMvcTest` Controller单元测试
- ✅ 正确处理HTTP请求和响应断言
- ✅ 测试方法命名清晰描述测试意图
- ✅ 包含必要的setup/teardown逻辑
- ✅ **自动执行setup中的MySQL SQL语句（测试数据准备）**
- ✅ **自动执行teardown中的MySQL SQL语句（测试数据清理）**
- ✅ 使用JdbcTemplate执行原生SQL语句
- ✅ 使用SLF4J Logger记录测试执行日志
- ✅ 自动移除endpoint中的context-path
- ✅ 类名自动移除中文字符

## 版本信息

- 版本: 2.1.0
- 创建日期: 2026-03-20
- 更新日期: 2026-03-25
- 设计理念: 从JSON到JUnit 5测试代码的自动化转换，支持完整的测试数据setup/teardown，通用化设计适用于任何Spring Boot项目
