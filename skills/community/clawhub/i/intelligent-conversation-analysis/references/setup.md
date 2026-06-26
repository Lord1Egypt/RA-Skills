# CCAI AIO 应用配置指南

> 来源：[阿里云百炼 - 获取 APP ID 和 Workspace ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id)

---

## 步骤一：开通 CCAI AIO 服务

1. 登录 [阿里云百炼控制台](https://bailian.console.aliyun.com/)
2. 在应用广场中找到「通义晓蜜 CCAI-对话分析 AIO」
3. 点击开通服务（需要实名认证）

---

## 步骤二：创建应用

1. 进入 [应用中心](https://bailian.console.aliyun.com/#/app-center)
2. 点击「创建应用」，选择「通义晓蜜 CCAI-对话分析 AIO」
3. 填写应用名称，完成创建

---

## 步骤三：获取 APP ID

1. 在应用列表中找到刚创建的应用
2. 复制该应用的 **APP ID**（格式类似 `a070a49c681f4a95a0f0...`）

```bash
export CCAI_APP_ID="你的APP_ID"
```

---

## 步骤四：获取 Workspace ID ⚠️ 必填

**`CCAI_WORKSPACE_ID` 是必填参数**，无论应用在默认业务空间还是子业务空间都必须配置，否则 API 调用会返回 404。

1. 登录百炼控制台
2. 点击左下角图标 → 业务空间详情
3. 在弹窗中复制 **业务空间 ID**（格式类似 `llm-ik...RVYCKzt`）

或者：进入 [业务空间管理](https://bailian.console.aliyun.com/?admin=1#/efm/business_management) 页面，在列表的 Workspace ID 列中复制。

```bash
export CCAI_WORKSPACE_ID="你的Workspace_ID"   # 必填，不可省略
```

---

## 引导话术

当用户询问如何配置时：

- "您是否已在百炼控制台开通了 CCAI AIO 服务？"
  - 未开通 → 引导完成步骤一和步骤二
  - 已开通 → 引导获取 APP ID（步骤三）和 Workspace ID（步骤四）

- `CCAI_APP_ID` 和 `CCAI_WORKSPACE_ID` **两个都是必填的**，缺少任何一个都无法正常调用 API。
