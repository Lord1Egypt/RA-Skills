# Filesystem Blueprint - my-study-pal

用这个文件创建概念解释系统的最小可运行骨架。

## 1. 创建基础目录结构

创建：

```text
mystudy/
  study-detail/
```

创建基础文件：
- `mystudy/study-summary.md`
- `mystudy/user-profile.md`
- `mystudy/runtime-profile.md`

可选参考内置模板资源：
- `assets/mystudy-template/study-summary.md`
- `assets/mystudy-template/user-profile.md`
- `assets/mystudy-template/runtime-profile.md`
- `assets/mystudy-template/study-detail/study-detail-template.md`

## 2. 补齐基础文件

### `study-summary.md`

至少包含：
- 标题
- 时间 / 学习主题 / 回答方式 / 是否完成 的表头

### `user-profile.md`

至少包含：
- 用户工作 / 专业 / 业务领域
- 用户爱好领域
- 用户最近的 5 个学习知识点
- 用户教学偏好 > 讲解式
  - 展开程度
  - 术语密度
  - 例子来源
  - 追问偏好
- 用户教学偏好 > 引导式
  - 互动强度
  - 问题形式
  - 引导切入方式
  - 术语密度
  - 例子来源
- 用户教学偏好 > 辨析式
  - 展开程度
  - 术语密度
  - 对照形式
  - 例子来源
  - 追问偏好
- 用户教学偏好 > 场景应用式
  - 应用深度
  - 步骤粒度
  - 例子来源
  - 风险提示强度
- 用户教学偏好 > 记忆巩固式
  - 记忆强度
  - 测试方式
  - 复习提示
  - 例子来源
- 语言风格偏好

### `runtime-profile.md`

至少包含：
- 回答方式默认策略
- 用户语境摘要
- 直答模式生效配置
- 讲解式生效配置
- 引导式生效配置
- 语言风格生效配置

规则：
- `user-profile.md` 是源头，`runtime-profile.md` 是派生缓存
- 用户长期偏好变化后，先更新 `user-profile.md`，再刷新 `runtime-profile.md`
- 不要只改 `runtime-profile.md` 来保存长期偏好

### `study-detail/` 模板

至少包含：
- 学习主题
- 日期
- 回答方式
- 对话记录

## 3. 定义可运行状态

概念解释系统只有在以下条件都满足时才算可运行：

- `mystudy/` 目录存在
- `study-detail/` 目录存在
- `study-summary.md` 存在
- `user-profile.md` 存在
- `runtime-profile.md` 存在
- `user-profile.md` 中至少存在讲解式默认配置

## 4. 检查首次运行安全性

首次使用时必须保证：
- 不覆盖已有文件
- 模板字段完整
- 没有遗留旧的 `config.md` 依赖
- 后续记录路径明确可用
- 内置模板与 references 中描述的字段口径一致
