---
name: openclaw-offer-radar
description: 把 Gmail 招聘邮件转成中文 Apple Reminders。用户提到“检查邮件里的面试/笔试/测评/授权”“把招聘邮件转成提醒事项”“别漏掉面试时间”“同步到 iPhone 提醒”等需求时触发。优先识别 ATS 邮件和面试信息更新，忽略投递成功回执。
---

# OpenClaw Offer Radar

## 适用场景

- 用户想把 Gmail 里的招聘邮件转成 Apple Reminders
- 邮件里包含面试、笔试、测评、授权等需要行动的时间信息
- 用户明确要求不要漏掉“面试信息更新”
- 用户希望提醒同步到 iPhone / Mac / iPad

## 当前依赖

- `gog` 负责搜索 Gmail 候选邮件
- Apple Mail 负责补抓邮件正文
- Apple Reminders 负责把事件落到原生提醒事项

## 默认流程

1. 运行扫描脚本：

```bash
python3 scripts/recruiting_sync.py --account your@gmail.com --mail-account 谷歌
```

2. 扫描脚本默认先看最近 2 天、最多 60 条候选线程。

3. 默认忽略：
   - 投递成功
   - 收到申请
   - 感谢投递
   - 简历完善
   - 反馈问卷

4. 对以下邮件提高召回：
   - `ibeisen`
   - `mokahr`
   - `nowcoder`
   - `腾讯校招`

5. 识别时优先提取：
   - 公司名
   - 岗位
   - 面试 / 笔试 / 测评时间
   - 截止时间
   - 主入口链接

6. 同一事件的“邀请”和“更新”必须归并为一个提醒，优先保留最新时间。

7. 一个事件只保留一条主提醒，不生成额外追提醒。

8. 当前实现依赖 Apple Mail 补抓邮件正文，所以要求：
   - Apple Mail 已登录同一个 Gmail 账号
   - 运行环境已放行 Mail / Reminders 权限

9. 如果用户要求真正同步到系统提醒事项，再执行：

```bash
python3 scripts/recruiting_sync.py --account your@gmail.com --mail-account 谷歌 --sync-reminders
```

## 标题和备注规范

- 标题必须是中文
- 标题只写事件本身，不写“11点提醒”之类调度信息
- 备注只保留：
  - 真实时间或截止时间
  - 岗位
  - 主入口链接
  - 必要时的一句说明
- 不写：
  - Gmail ID
  - 发件人元数据
  - 长摘要
  - 与事件无关的信息

## 输出要求

- 先说明识别出多少个招聘事件
- 若同步成功，回执：
  - 事件标题
  - due 时间
  - 使用的列表
- 若没有新事件，明确说明“本轮无新的高置信度招聘提醒”
