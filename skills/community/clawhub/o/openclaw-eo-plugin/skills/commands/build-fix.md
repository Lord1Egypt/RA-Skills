# /build-fix - 构建错误修复指令

## 功能
调度对应技术栈的开发专家，自动分析和修复构建错误。

## 参数
```
/build-fix <错误信息或文件> [options]

参数:
  <错误信息>    必填，构建错误信息或日志文件路径
  --lang <语言> 可选，技术栈
                 值: typescript | python | golang | java | rust | cpp
                 默认: 自动检测
  --tool <工具> 可选，构建工具
                 值: npm | maven | gradle | cargo | make | cmake
                 默认: 自动检测
```

## 执行流程

1. **解析错误信息** - 提取错误类型和位置
2. **匹配专家** - 根据语言/工具选择对应的 Build-Resolver
3. **Spawn 子Agent** - 加载错误修复专家
4. **输出修复方案** - 包含原因分析和修复代码

## 输出格式

```markdown
# 🔧 构建错误修复

## 📋 错误摘要
- **错误类型**: Compilation Error
- **文件**: `src/utils/helper.ts`
- **行号**: Line 42

## 🔍 根因分析
`TS2307: Cannot find module './config' or its corresponding type declarations.`

原因：模块路径解析失败，可能是文件扩展名缺失或相对路径错误。

## ✅ 修复方案

### 方案1：添加扩展名
```typescript
// 之前
import { config } from './config'

// 之后
import { config } from './config.ts'
```

### 方案2：检查文件是否存在
```bash
ls -la src/config.ts
```

## 🧪 验证
修复后请运行：
```bash
npm run build
```
确认无错误输出。

## 📚 相关知识
- TypeScript 模块解析文档
- ES2022 模块规范
```

## 示例

```
用户: /build-fix "Error: Cannot find module './utils' in src/index.ts"

我:
1. 检测到 TypeScript 项目
2. 加载 typescript-build-resolver 专家
3. 分析路径问题
4. 输出修复方案
```
