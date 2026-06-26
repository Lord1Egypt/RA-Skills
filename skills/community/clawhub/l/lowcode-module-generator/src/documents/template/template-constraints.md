# 模板约束规则

## 概述

`src/template/` 目录下的所有 `.vm` 模板文件**禁止修改**。

---

## ⚠️ 铁律：生成代码前必须先读取模板文件

> 参考：[Velocity模板变量详解](./velocity-variables.md)

**所有代码生成任务必须遵循以下强制规则：**

| 规则 | 说明 |
|-----|------|
| **必须读取模板** | 生成任何代码之前，**必须先读取对应的 `.vm 模板文件**，读取全部内容 |
| **禁止想当然** | 禁止根据"经验"或"常识"生成代码，必须严格按模板结构填充变量 |
| **类型参数一致** | `BaseService<Mapper, Po>` 的类型参数数量和顺序必须与模板完全一致 |
| **继承关系一致** | 生成的类继承父类、实现接口必须与模板一致 |
| **注入方式一致** | `@Autowired` 注入的类必须与模板一致 |

**⚠️ 绝对禁止：凭记忆生成代码**

| 禁止行为 | 后果 | 正确做法 |
|---------|------|---------|
| 凭记忆写import | import路径写错，编译失败 | 复制模板中的import语句 |
| 凭经验猜变量类型 | 类型不匹配，运行时异常 | 查看模板中的变量定义 |
| 凭直觉写代码逻辑 | 逻辑遗漏，功能缺失 | 按照模板的Velocity语法填充 |
| 跳过模板直接写 | 代码风格不一致，难以维护 | 必须先读取模板再生成 |

**错误示例**：
```java
// ❌ 错误：凭记忆写import，导致路径错误
import com.wisdom.base.common.vo.base.GeneralVo;

// ✅ 正确：从模板复制，路径正确
import com.wisdom.base.common.vo.GeneralVo;
```

**正确流程**：
```
1. 确定要生成的文件类型（如 ServiceImpl）
2. 找到对应的 .vm 模板文件（如 serviceimpl.java.vm）
3. 读取模板全部内容，理解 Velocity 变量含义
4. 将模板内容作为基础，替换 ${变量} 为实际值
5. 输出生成的代码
```

---

## 约束说明

1. **模板文件只读**：所有 `.vm` 模板文件是原始模板，不可修改、删除、替换
2. **槽位填充原则**：代码生成仅做变量槽位替换，不改变模板格式内容
3. **空模板设计**：某些模板（如 mapper.xml.vm）内容为空是 低代码平台的Velocity模板 原始设计，用于槽位填充
4. **模板来源**：模板来源于 `wsd-adp/src/main/resources/codebuilder/`，与 ADP 保持同步

---

## ⚠️ 常见错误：BaseService 类型参数

> 参考：[Velocity模板变量详解 - 一、后端核心变量](./velocity-variables/velocity-variables.md)

**模板中 BaseService 的定义**：
```java
public class XxxServiceImpl extends BaseService<XxxMapper, XxxPo> implements XxxService {
```
- 类型参数只有 **2个**：`Mapper` 和 `Po`
- **不是 5个**（Po、Vo、AddForm、UpdateForm、SearchForm）

**错误示例（禁止）**：
```java
// ❌ 错误：类型参数数量与模板不一致
public class OntologyActionServiceImpl extends BaseService<OntologyActionPo, OntologyActionVo, OntologyActionAddForm, OntologyActionUpdateForm, OntologyActionSearchForm>
```

**正确示例（必须）**：
```java
// ✅ 正确：严格按模板，只有2个类型参数
public class OntologyActionServiceImpl extends BaseService<OntologyActionMapper, OntologyActionPo>
```

---

## 槽位填充要求

| 要求 | 说明 |
|-----|------|
| 不改格式 | 仅替换 `${变量}` 槽位，保持模板原有缩进、换行 |
| 不删内容 | 模板中已有内容（如 import、注解）不可删除，**禁止减少** |
| 不减内容 | 生成的代码不能比模板内容少，保持模板完整结构 |
| 空模板保留 | 空内容的模板（如 mapper.xml）保留空结构 |
| 变量为空时 | 使用空字符串填充，不得删除槽位所在行 |

---

## mapper.xml 模板约束

**核心原则**：执行 Velocity 引擎生成纯代码，`<mapper></mapper>` 标签内部保持为空。

**处理流程**：
1. 调用 Velocity 引擎处理 `.vm` 模板
2. 替换 `${变量}` → 实际值
3. 执行 `#if`/`#else`/`#end` → 条件判断
4. 执行 `#set` → 变量赋值
5. 输出**纯代码**（无 Velocity 指令）
6. **特殊约束**：`<mapper>` 和 `</mapper>` 之间保持为空

**模板**：
```xml
#if(${buildTableType} == 'Tree')
#set($vmTableVoClassName = "${buildClassName}TreeVo")
#set($vmSelectVo = "TreeVo")
#else
#set($vmTableVoClassName = "${buildClassName}DataVo")
#set($vmSelectVo = "DataVo")
#end
<?xml version="1.0" encoding="UTF-8" ?>
<!DOCTYPE mapper PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN" "http://mybatis.org/dtd/mybatis-3-mapper.dtd" >
<mapper namespace="${buildPackage}.mapper.${buildClassName}Mapper">

</mapper>
```

**生成结果**（假设 buildTableType=Page，buildPackage={microservice.package}，buildClassName=ValueType）：
```xml
<?xml version="1.0" encoding="UTF-8" ?>
<!DOCTYPE mapper PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN" "http://mybatis.org/dtd/mybatis-3-mapper.dtd" >
<mapper namespace="{microservice.package}.mapper.ValueTypeMapper">

</mapper>
```

**处理说明**：
| 步骤 | 操作 | 示例 |
|-----|------|-----|
| 1 | 执行 `#if` 条件 | `buildTableType == 'Page'`，执行 `#else` 分支 |
| 2 | 执行 `#set` 赋值 | `$vmTableVoClassName = "ValueTypeDataVo"` |
| 3 | 替换 `${变量}` | `${buildPackage}` → `{microservice.package}` |
| 4 | 保持中间为空 | `<mapper>` 和 `</mapper>` 之间无内容 |

---

## 违反约束的处理

如需调整功能，请：
1. 在 SKILL 文档中说明，而非修改模板
2. 通过变量配置实现差异化（如 buildEnableCustomField）
3. 确需修改时，新建模板副本（如 `po-ext.java.vm`）
