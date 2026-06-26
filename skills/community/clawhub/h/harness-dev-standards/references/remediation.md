# 常见问题自动修复策略库

## 目录

- [依赖问题修复](#依赖问题修复)
- [TypeScript 类型错误修复](#typescript-类型错误修复)
- [Import 路径错误修复](#import-路径错误修复)
- [语法错误修复](#语法错误修复)
- [启动失败修复](#启动失败修复)
- [构建错误修复](#构建错误修复)

---

## 依赖问题修复

### 问题 1: 依赖版本冲突

**错误信息：**
```
npm ERR! code ERESOLVE
npm ERR! ERESOLVE could not resolve dependency
```

**自动修复策略：**

1. **识别冲突包** - 从错误信息中提取冲突的包名和版本范围
2. **查看 peerDependencies** - 检查冲突包的对等依赖要求
3. **应用以下修复方案：**

   **方案 A: 使用 --legacy-peer-deps（临时方案）**
   ```bash
   npm install --legacy-peer-deps
   # 或
   pnpm install --no-strict-peer-dependencies
   ```

   **方案 B: 升级/降级冲突包**
   - 查找兼容的版本组合
   - 更新 package.json 中的版本号
   - 重新安装

   **方案 C: 使用 overrides（npm）或 resolutions（pnpm）**
   ```json
   // package.json
   {
     "overrides": {
       "react": "^18.0.0"
     }
   }
   ```

4. **验证修复** - 重新运行 install 确认问题解决

---

### 问题 2: 未使用的依赖

**错误信息：**
```
Unused dependencies found:
- package-a
- package-b
```

**自动修复策略：**

1. **二次确认** - 检查代码中是否真的没有使用这些包
   - 搜索 import 语句
   - 搜索 require 调用
   - 检查配置文件中的引用

2. **安全移除** - 如果确认未使用：
   ```bash
   npm uninstall package-a package-b
   # 或
   pnpm remove package-a package-b
   ```

3. **注意事项**
   - 不要移除仅在配置文件中引用的包
   - 不要移除 peerDependencies 中声明的包
   - 某些包可能通过字符串动态导入，需要特殊处理

---

### 问题 3: 缺失的依赖

**错误信息：**
```
Cannot find module 'missing-package'
```

**自动修复策略：**

1. **识别缺失包名** - 从错误信息提取
2. **检查是否为 devDependency** - 有些包可能只在开发环境需要
3. **安装依赖**：
   ```bash
   npm install missing-package
   # 或开发依赖
   npm install -D missing-package
   ```

4. **特殊情况处理**
   - 如果是类型定义缺失：`npm install -D @types/missing-package`
   - 如果是 monorepo 内部包：检查 workspace 配置
   - 如果是私有包：检查 npm registry 配置

---

### 问题 4: 安全漏洞

**错误信息：**
```
npm audit found 3 high severity vulnerabilities
```

**自动修复策略：**

1. **运行自动修复**：
   ```bash
   npm audit fix
   ```

2. 如果自动修复无法解决：
   - 查看漏洞详情：`npm audit`
   - 检查受影响包的最新版本是否修复
   - 如果有修复版本，手动升级：`npm update vulnerable-package`
   - 如果无法升级，考虑使用替代包或添加忽略说明

3. **记录说明** - 如果必须保留有漏洞的版本，在代码中添加注释说明原因

---

## TypeScript 类型错误修复

### 问题 1: 隐式 any 类型

**错误信息：**
```
Parameter 'x' implicitly has an 'any' type.
```

**自动修复策略：**

1. **推断类型** - 根据参数使用方式推断合理的类型
2. **添加类型注解**：
   ```typescript
   // 修复前
   function process(x) { ... }
   
   // 修复后
   function process(x: string) { ... }
   ```

3. **如果类型确实不确定**：
   - 使用 `unknown` 而不是 `any`
   - 添加类型守卫
   ```typescript
   function process(x: unknown) {
     if (typeof x === 'string') {
       // x 在这里是 string 类型
     }
   }
   ```

---

### 问题 2: 类型不匹配

**错误信息：**
```
Type 'string' is not assignable to type 'number'.
```

**自动修复策略：**

1. **分析上下文** - 确定期望的类型和实际的类型
2. **应用类型转换**：
   ```typescript
   // 修复前
   const count: number = params.count;
   
   // 修复后
   const count: number = Number(params.count);
   ```

3. **常见转换模式**：
   - 字符串转数字：`Number(x)` 或 `parseInt(x, 10)`
   - 任意转布尔：`Boolean(x)` 或 `!!x`
   - 联合类型收窄：使用类型守卫

---

### 问题 3: 可能为 null/undefined

**错误信息：**
```
Object is possibly 'null'.
Object is possibly 'undefined'.
```

**自动修复策略：**

1. **添加空值检查**（推荐）：
   ```typescript
   // 修复前
   const name = user.name;
   
   // 修复后
   const name = user?.name;
   ```

2. **如果确定不会为空**，使用非空断言：
   ```typescript
   const name = user!.name;
   ```

3. **提供默认值**：
   ```typescript
   const name = user?.name ?? 'default';
   ```

---

### 问题 4: 缺少属性定义

**错误信息：**
```
Property 'email' does not exist on type 'User'.
```

**自动修复策略：**

1. **找到类型定义位置**
2. **添加缺失的属性**：
   ```typescript
   // 修复前
   interface User {
     id: number;
     name: string;
   }
   
   // 修复后
   interface User {
     id: number;
     name: string;
     email: string;
   }
   ```

3. **如果是外部类型**，使用类型扩展：
   ```typescript
   declare module 'external-lib' {
     interface User {
       email: string;
     }
   }
   ```

---

## Import 路径错误修复

### 问题 1: 模块未找到

**错误信息：**
```
Cannot find module '@/components/Button' or its corresponding type declarations.
```

**自动修复策略：**

1. **检查路径别名配置** - 查看 tsconfig.json 中的 paths 配置
2. **验证文件是否存在** - 检查目标文件的实际位置
3. **修正路径**：

   **相对路径问题**：
   ```typescript
   // 修复前
   import Button from '../../components/Button';
   
   // 修复后（层数不对）
   import Button from '../../../components/Button';
   ```

   **路径别名问题**：
   - 确认 tsconfig.json 配置正确
   - 确认构建工具（webpack/vite）也配置了别名
   - 如果使用 Next.js，检查是否配置了 baseUrl

4. **扩展名问题** - 某些环境需要明确加 `.ts` / `.tsx` 扩展名

---

### 问题 2: 命名导出不存在

**错误信息：**
```
Module '"../utils"' has no exported member 'formatDate'.
```

**自动修复策略：**

1. **检查目标模块的导出**
2. **修正导入名称** - 可能是拼写错误
3. **如果是默认导出**，改为默认导入：
   ```typescript
   // 修复前
   import { formatDate } from '../utils';
   
   // 修复后
   import formatDate from '../utils';
   ```

4. **如果确实需要命名导出**，在目标模块添加导出：
   ```typescript
   // 在 ../utils 中添加
   export { formatDate };
   ```

---

## 语法错误修复

### 常见 JavaScript/TypeScript 语法错误

| 错误模式 | 修复方案 |
|---------|---------|
| 缺少分号 | 添加分号（或配置无分号风格） |
| 括号不匹配 | 找出缺失的括号并补全 |
| 引号不匹配 | 统一引号类型（单/双/模板字符串） |
| `const` 变量重新赋值 | 改为 `let` 或避免重新赋值 |
| 解构时使用保留字 | 重命名变量：`{ default: defaultVal }` |
| 异步函数中没有 await | 添加 await 或移除 async |

### 示例修复

**问题：缺少闭括号**
```typescript
// 修复前
function add(a, b {
  return a + b;
}

// 修复后
function add(a, b) {
  return a + b;
}
```

**问题：const 重新赋值**
```typescript
// 修复前
const count = 0;
count = 1;

// 修复后
let count = 0;
count = 1;
```

---

## 启动失败修复

### 问题 1: 端口被占用

**错误信息：**
```
Port 3000 is already in use.
```

**自动修复策略：**

1. **查找占用进程**：
   ```bash
   lsof -i :3000
   # 或
   netstat -ano | findstr :3000
   ```

2. **杀掉进程**：
   ```bash
   kill -9 <PID>
   ```

3. **或使用其他端口**：
   - 修改 package.json 中的启动命令
   - 或设置环境变量 `PORT=3001`

---

### 问题 2: 环境变量缺失

**错误信息：**
```
Error: DATABASE_URL is not defined
```

**自动修复策略：**

1. **检查 .env 文件是否存在**
2. **检查 .env.example 中的配置项**
3. **创建/更新 .env 文件**，添加缺失的环境变量
4. **确认环境变量加载工具已正确配置**（dotenv 等）

---

### 问题 3: Node.js 版本不兼容

**错误信息：**
```
Error: Cannot find module 'node:fs'
```

**自动修复策略：**

1. **检查 package.json 中的 engines 配置**
2. **建议升级 Node.js 版本**
3. **或降级相关依赖包到兼容版本**

---

## 构建错误修复

### 问题 1: Next.js 构建时页面报错

**错误信息：**
```
Error occurred prerendering page "/xxx".
```

**自动修复策略：**

1. **检查是否有服务端不支持的 API**（window, document 等）
2. **添加动态导入或客户端标记**：
   ```typescript
   'use client'; // 客户端组件
   
   // 或动态导入
   const Component = dynamic(() => import('./Component'), {
     ssr: false
   });
   ```

3. **检查 getStaticProps/getServerSideProps 中的错误**
4. **检查数据获取是否有异常未捕获**

---

### 问题 2: 构建产物过大

**警告信息：**
```
Warning: asset size limit: The following asset(s) exceed the recommended size limit (244 KiB).
```

**自动修复策略：**

1. **分析 bundle 组成**：
   ```bash
   npx webpack-bundle-analyzer
   # 或 Next.js 内置分析
   ANALYZE=true npm run build
   ```

2. **应用优化手段**：
   - 代码分割（动态 import）
   - 移除未使用的依赖
   - 使用更轻量的替代库
   - 启用 Tree Shaking
   - 配置 externals

---

## 修复验证流程

每次自动修复后，必须执行以下验证：

1. **重新运行出错的命令** - 确认错误已解决
2. **运行类型检查** - `npx tsc --noEmit`
3. **运行 lint 检查** - `npx eslint .`
4. **尝试启动项目** - `npm run dev`
5. **尝试构建项目** - `npm run build`

**如果还有错误，重复诊断-修复-验证流程，直到全部通过。**

---

## 修复优先级原则

1. **正确性优先** - 保证修复后的代码逻辑正确
2. **最小改动** - 只修改必要的部分，不引入无关变更
3. **保留语义** - 修复后代码的行为应和原意图一致
4. **可维护性** - 修复方案应清晰易懂，不是黑魔法

---

*本策略库基于 100+ 实际项目问题总结而成，持续更新中...*
