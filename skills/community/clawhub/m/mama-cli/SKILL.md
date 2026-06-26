---
name: mama-cli
description: 在 BOSS 直聘中筛选候选人、主动打招呼、处理未读消息/接收简历的浏览器自动化技能，触发词：BOSS直聘、招聘、简历、未读消息、打招呼。
---

# BOSS 直聘简历筛选技能

### 触发词示例

**主动打招呼**:
- "在 BOSS 直聘上筛选 Java 工程师，3-5 年经验，本科及以上"
- "帮我找产品经理候选人，5 年以上经验，大厂背景优先"
- "筛选成都地区的前端开发，薪资 15-25k，主动打招呼"

**处理未读消息（含筛选条件）**:
- "处理 BOSS 直聘的未读消息，筛选条件：Java, 3-5年经验, 本科及以上"
- "检查未读消息，筛选产品经理，5年以上，大厂背景"
- "接收臧尔强的简历"
- "处理未读消息，按条件筛选后生成报告导入飞书"

> **核心能力**: 推荐牛人筛选打招呼、沟通页面未读消息处理、简历接收、简历下载、常用语索取简历、查看候选人简历详情。


## 1. 核心配置与规范

### ✅ 浏览器配置 (必须遵守)
所有 `browser` 工具调用必须遵循以下配置：
```yaml
profile: "user"              # 使用用户已登录的浏览器，复用现有 Cookie/登录态
snapshotFormat: "ai"     # 必须使用 AI 快照格式，获取带 [eXX] 数字引用的元素列表
target: "host"           # 本地浏览器
delayMs: 2000-5000       # 操作间隔随机延迟，避免风控
```

**元素定位策略**:
| 场景 | 定位方式 | 示例 |
|------|---------|------|
| **简单元素** (按钮/链接) | `snapshot` + grep "关键字" 获取ref + `click ref`
| **标签页切换** (全部/未读) | `evaluate` + XPath | `//span[contains(text(), '未读')]` |

**通过关键字找到元素标准操作流程**:
1.  **通过grep快照获取元素ref**: 每次操作前，先获取元素Ref，确保元素可见且可点击。
2.  **定位元素 Ref**: 使用 AI 快照返回的 `ref` 进行点击操作。
3.  **处理异常情况**: 若元素操作失败（如超时、元素不可见），根据错误类型调用对应场景（如场景 H：关闭弹窗）。
4. **📸 截图确认操作成功（铁律）**: **每次关键操作后必须截图** (`openclaw browser screenshot`)，确认页面状态符合预期再继续下一步。宁可多截图，不要盲操作。
   - ✅ 页面状态符合预期 → 继续
   - ❌ 状态异常（弹窗未关、跳转错误）→ 先修复再继续
   - ❌ 验证码/滑块 → **立即停止**，通知用户
5. **弹窗处理**: 若操作触发弹窗（如简历、广告）结束后必须关闭，必须使用 [场景 H: 关闭弹窗](scripts/scenario_close_popup.md) 方法处理。

**CLI 常用技巧**:
1.  **定位获取 Ref**:
    ```bash
    # 查找关键字 (如: 推荐牛人、沟通、未读)
    openclaw browser snapshot --target-id <TARGET_ID> --format ai | grep -C 10 "关键字"
    ```
2.  **点击元素 Ref**:
    ```bash
    openclaw browser act --kind click --target-id <TARGET_ID> --ref <REF>
    ```

### 🚫 关键禁令
1.  **禁止新建 Tab**: 必须复用现有的 "BOSS 直聘" Tab。如果未找到，提示用户手动打开。
2.  **禁止隔离模式**: 严禁使用 `profile="openclaw"`。
3.  **禁止高危指令**: 严禁使用 `requests`, `responsebody`, `console`, `cookies`, `storage`。
4.  **禁止 `--labels`**: `snapshot` 时不要使用 `--labels` 参数，会导致 listitem 丢失 ref。
5.  **禁止 非登录态停止**: 若截图确认非登录态，立即停止操作，提示用户登录。
6.  **禁止 中途停止**: 任务必须完整执行到底（导航→列表→遍历所有候选人→报告→飞书），除非遇到无法修复的故障（验证码/登录失效/页面不存在），否则不得在完成一个阶段后停下来。
7.  **禁止 跳过标准流程**: 遇到问题必须先回顾标准流程文档（scripts/scenario_handle_unread_with_filter.md），按排查步骤处理，不得随意跳过步骤或自行发挥。

---

### 🔍 问题排查流程（必须遵守）

**遇到问题时的标准动作**：

```
1. 📸 截图 → 看当前页面状态
2. 📋 回顾标准流程 → 确认当前应该在哪一步
3. 🔄 重试 3 次 → 每次都重新获取 snapshot 和 ref
4. ❓ 仍失败 → 记录错误详情，判断是否属于"允许停止"的 4 种情况
```

**常见问题速查**：
| 问题 | 标准解决 | 参考场景 |
|------|---------|---------|
| 点击候选人无反应 | 用 evaluate + DOM 遍历点击 | scenario_chat_list_click.md |
| 标签页切换失败 | 用 XPath + evaluate 点击 | scenario_tab_switching.md |
| 简历弹窗打不开 | 重新获取姓名 ref，等待 6 秒 | scenario_view_resume_detail.md |
| 弹窗关不掉 | 连续 2 次 Escape，或找关闭按钮 ref | scenario_close_popup.md |
| 返回列表失败 | 确认当前页面，用 Escape 或点击列表项 | scenario_get_unread_list.md |

---

## 2. 核心工作流

### 流程一：推荐牛人筛选与打招呼
**目标页面**: `/web/chat/recommend`

1.  **初始化检查**: 检查浏览器状态 (`status`)，查找并复用 BOSS 直聘 Tab (`tabs`)。
2.  **登录验证**: 截图 (`screenshot`) 确认是否在登录态。
3.  **关闭弹窗**: 若截图确认有弹窗（如"牛人不回应 试试意向沟通"广告），使用 [场景 H: 关闭弹窗](scripts/scenario_close_popup.md) 方法关闭。
    *   **推荐顺序**: Escape 键 → 标准选择器 → 几何位置定位
    *   **注意**: 关闭后可能跳转到个人中心，需导航回原页面
4.  **导航与定位**:
    *   获取页面快照，找到"推荐牛人" ref
    *   点击 "推荐牛人"元素.
    *   **注意**: 内容可能在 iframe 中，需识别并切换 frame。
4.  **筛选操作**:
    *   点击 "职位" 筛选器，选择目标岗位。
    *   点击 "筛选" 按钮，设置学历、经验、薪资条件。
5.  **打招呼循环**:
    *   识别候选人卡片 (`role="listitem"`).
    *   点击 "打招呼" 或 "立即沟通" 按钮。
    *   **风控**: 每次处理 1-2 人，间隔 3-5 秒随机。
6.  **记录与报告**: 记录操作结果，生成 Markdown 报告。


### 流程二：未读消息处理 + 筛选条件 + 飞书报告（⭐ 推荐）
**目标页面**: `/web/chat/index`
**输入**: 筛选条件（职位/经验/学历/薪资/地区）
**输出**: Markdown 筛选报告 → 飞书文档

> **完整12步流程**，涵盖浏览器初始化、候选人遍历、简历判断、条件筛选、报告生成、飞书导入。
> 详见 [场景 J: 处理候选人未读消息（含筛选条件）](scripts/scenario_handle_unread_with_filter.md)

**核心流程概览**:
1. **初始化** (Step 1-3): 检查浏览器 → 启动 → 找 BOSS Tab
2. **导航** (Step 4-6): 沟通 → 全部 → 未读
3. **获取列表** (Step 7): grep "全部 未读" 提取候选人信息（ref/姓名/时间/未读数/职位/消息摘要）
4. **遍历处理** (Step 8): 对每个候选人：
   - 进入聊天 → 读取消息 → 查看简历详情 → 关闭弹窗
   - **条件判断**: 不满足 → 记录原因跳过
   - **简历判断**: 已发送 → 接收+下载 | 未发送 → 常用语索取
5. **报告生成** (Step 10): Markdown 格式，含通过/未通过/统计
6. **飞书导入** (Step 11): 使用 feishu-cli-import 技能
7. **反馈结果** (Step 12): 汇报处理摘要

---

## 3. 常用技巧与场景处理

针对 BOSS 直聘的复杂交互场景，我们提供了详细的解决方案文档。

| 场景 ID | 场景描述 | 解决方案摘要 | 详细文档 |
|---|---|---|---|
| **A** | 要查的元素关键字共享 Ref 的标签页 (如 "全部/未读")，或者是statictext类型 ，或者没有ref的元素 | 使用 `evaluate` + XPath 定位 | [scenario_tab_switching.md](scripts/scenario_tab_switching.md) |
| **B** | 无 Ref 的列表项 (如聊天列表) | 使用 `evaluate` + DOM 查询 | [scenario_chat_list_click.md](scripts/scenario_chat_list_click.md) |
| **C** | 简历预览窗口下载简历 | iframe 内查找下载按钮 | [scenario_resume_download.md](scripts/scenario_resume_download.md) |
| **D** | 使用常用语索取简历 | 自动化发送常用语 | [scenario_request_resume.md](scripts/scenario_request_resume.md) |
| **E** | 定位未读消息页面 | 组合定位 Tab 和筛选器 | [scenario_locate_unread.md](scripts/scenario_locate_unread.md) |
| **F** | 获取未读消息候选人列表 | 定位到未读消息页面后，获取候选人列表 | [scenario_get_unread_list.md](scripts/scenario_get_unread_list.md) |
| **G** | 定位到某个候选人聊天页面 | 有ref直接点击；无ref用evaluate+DOM查询+dispatchEvent（候选人列表通常无ref） | [scenario_locate_candidate.md](scripts/scenario_locate_candidate.md) |
| **H** | 关闭弹窗/模态框 (广告/简历预览/聊天窗口) | Escape 键 → 标准选择器 → 几何位置定位 | [scenario_close_popup.md](scripts/scenario_close_popup.md) |
| **I** | 查看候选人简历详情 | 进入聊天页面后查看候选人简历详情 | [scenario_view_resume_detail.md](scripts/scenario_view_resume_detail.md) |
| **J** | 处理未读消息（含筛选条件）| 完整12步流程：初始化→导航→列表→遍历→筛选→简历判断→报告→飞书导入 | [scenario_handle_unread_with_filter.md](scripts/scenario_handle_unread_with_filter.md) |

### 通用技巧
1.  **AI 快照优先**: 始终使用 `snapshotFormat="ai"` 获取 `eXX` 引用。
2.  **动态 Ref**: 页面刷新后 ref 会变，操作前务必重新获取快照。
3.  **智能等待**: 关键操作（如弹窗、iframe 加载）后增加 `sleep`。
4.  **Escape 键**: 处理弹窗的最稳妥方式。

---

## 4. 风控与合规 (必读)

### 🛡️ 防风控规则
1.  **频率限制**: 主动打招呼 < 30 人/天，< 8 人/小时。
2.  **随机间隔**: 每次操作后必须等待 **2-5 秒随机延迟**。
3.  **单次操作**: 不要批量并发，模拟真人逐个处理。
4.  **停止信号**: 出现验证码、滑块或 "今日沟通已达上限" 时，立即停止。

### ⚠️ 错误处理与重试
*   **Timeout/Not Found**: 重新获取 AI 快照 (`snapshotFormat="ai"`) 后重试，最多 3 次。
*   **元素操作持续失败**: 如果多次尝试操作元素（如点击）仍失败，必须使用截图 (`screenshot`) 检查页面状态，确认是否有非预期的弹窗、蒙层或其他遮挡物，然后调用对应场景（如场景 H：关闭弹窗）进行处理。
*   **浏览器未准备好**: 提示用户先手动打开 BOSS 直聘并登录，确保浏览器处于已登录状态。
*   **登录失效**: 提示用户重新登录。

---

## 5. 输出模板示例

### 推荐牛人筛选报告
```markdown
## BOSS 直聘筛选报告
**时间**: 2026-03-12
**条件**: Java, 3-5年, 本科
**结果**:
| 姓名 | 职位 | 状态 |
|------|------|------|
| 张三 | Java | ✅ 已打招呼 |
| 李四 | Java | ❌ 失败 (原因) |
```

