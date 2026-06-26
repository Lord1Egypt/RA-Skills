# 示例对话

## 项目初始化

```
用户: /init

助手: [1/4] 探测项目类型... ✓ react (置信度: 95%)
      [2/4] 分析项目结构... ✓
      [3/4] 解析配置文件... ✓
      [4/4] 生成项目文档... ✓ .claude/project.md
```

## 智能问答

```
用户: 登录功能是怎么实现的？

助手: ## 登录实现

      通过 `AuthService` + `JwtUtil` 实现：
      1. 前端提交 → `LoginApi.login()`
      2. 后端验证 → `AuthService.authenticate()`
      3. Token生成 → `JwtUtil.createToken()`

      相关代码：
      - `src/pages/Login.tsx:45-78`
      - `src/api/auth.ts:23-56`

      📝 已生成文档: .claude/docs/qa/feature/xxx.md
```

## 影响分析

```
用户: 修改 login 函数会影响什么？

助手: ## 影响分析: login

      ### 直接调用者
      - `src/pages/Login.tsx:45` - handleLogin
      - `src/pages/Signup.tsx:78` - autoLogin

      ### 测试覆盖
      - `src/tests/auth.test.ts` - 3 个测试用例
```

## 飞书集成

```
用户: /feishu-status

助手: 📋 文档同步状态

      状态: 🟡 建议更新
      变更文件: 5
      高优先级: 2 项

      建议执行 /feishu-report 查看详情
```

## 配置管理

```
用户: /show-config

助手: 当前配置：
      - workdir: /home/user/project
      - build_command: make all
      - feishu.doc_token: doccnxxx
```