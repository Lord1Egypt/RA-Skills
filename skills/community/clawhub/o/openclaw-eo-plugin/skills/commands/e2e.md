# /e2e - 端到端测试指令

## 功能
调度 QA 专家，使用 Playwright 生成端到端测试用例。

## 参数
```
/e2e <功能描述> [options]

参数:
  <功能描述>   必填，要测试的功能描述
  --browser <浏览器> 可选
                     值: chromium | firefox | webkit
                     默认: chromium
  --format <格式>   可选，输出格式
                     值: playwright | cypress | testcafe
                     默认: playwright
```

## 执行流程

1. **分析功能** → 确定测试页面和用户流程
2. **识别测试点** → 关键操作和预期结果
3. **生成测试代码** → Playwright/Cypress 格式
4. **输出可执行测试** → 包含 Page Object Model

## 输出格式

```markdown
# 🧪 E2E 测试生成 - [功能名称]

## 📋 测试场景

### 场景1: 用户登录流程
**前置条件**: 用户已注册
**步骤**:
1. 访问登录页 `/login`
2. 输入邮箱 `test@example.com`
3. 输入密码 `Test1234`
4. 点击登录按钮
5. 验证跳转到首页

**预期结果**: 
- URL 变为 `/dashboard`
- 显示用户头像

---

## 📝 测试代码 (Playwright)

### Page Object: LoginPage
```typescript
class LoginPage {
  constructor(page: Page) {
    this.page = page
  }

  async navigate() {
    await this.page.goto('/login')
  }

  async login(email: string, password: string) {
    await this.page.fill('[data-testid="email-input"]', email)
    await this.page.fill('[data-testid="password-input"]', password)
    await this.page.click('[data-testid="login-button"]')
  }
}
```

## 对应专家
- QA Engineer
- E2E Tester
