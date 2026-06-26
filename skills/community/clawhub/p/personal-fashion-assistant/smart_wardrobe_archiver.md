---
name: "smart_wardrobe_archiver"
description: 用于处理衣物图片的自动化入库、特征分析、编号生成及本地文件索引管理。

# 【版本与作者】
version: "1.0.0"
author: "Yuna"
---


# 0. Trigger Condition (触发条件)
当满足以下条件时，启动本 Skill (clothing_add)：
1. **安装引导**：在用户处于初始安装流程，被引导并选择进行首次入库时。
2. **冲突检查后**：用户执行完 `clothing_conflict_check` 冲突检查后，明确确认要将该衣物录入衣橱时。
3. **主动触发**：用户上传照片并附带诸如“入库”、“归档”、“纳入衣橱”、“加入衣柜”或“记录”等明确的录入指令。

> 🚨 **全局路由交互规则（针对仅上传照片的场景）**：
> 收到用户上传照片后，Agent **必须等待 10 秒**，看用户是否提出进一步意图。
> 若 10 秒后用户未提出意图，Agent 必须主动询问：“请问您是要进行**冲突检查**还是**入库**？” 根据用户回复触发相应技能。

# 1. Tool Binding (工具绑定)
本Skill依赖于 [wardrobe_tools.py](./TOOLS/wardrobe_tools.py) （位于 `./TOOLS/` 目录下）提供的 `WardrobeManager` 类。AI 在执行各步骤时可调用相应方法：
| 逻辑阶段 | 触发动作 | 调用工具方法 | 输入参数 | 预期输出 |
| :--- | :--- | :--- | :--- | :--- |
| 环境准备 | 首次启动/检测缺失 | `init_environment()` | 无 | 确认目录及文件已就绪 |
| 图像列队入栈 | 接收用户图库 | `receive_image()` | `source_image_path` | 返回含时间戳格式的暂存文件路径 |
| 照片出列检索 | 开始或继续处理循环 | `get_next_temp_processing()` | 无 | 返回时间最早的待处理照片暂存路径 |
| 提取模型特征 | 获取照片和 Prompt 后 | `build_model_payload()` 等 | `prompt_text`, `image_path` | 通过网络抓取含12位提取编码的特征 Markdown 行 |
| 交互预处理 | 拿到生成行准备对审 | `prepare_interaction()` | `temp_path`, `markdown_row` | 判定查重，图像保密改名为 `ID_temp_push` 提供下一步交互锁定基石 |
| 分支流转归档 | 获取判定操作反馈(A/B/C) | `handle_user_decision()` | `action`, `temp_push_path`, `markdown_data` | 基于决策执行丢弃或替换ID复写存档操作，清出已处理临时项 |
| 系统维护 | 暂停整体入库，或列队循环完毕时 | `cleanup_temp()` | 无 | 彻底清空残余的 `temp_upload` 目录 |

# 2. Initialization (初始化步骤)
## 调用 init_environment()。

## Directory Check:
确保根目录 ./smart_wardrobe/ 存在。
建立图片仓库：./smart_wardrobe/wardrobe_data/ (用于持久化存储归档图片)。
建立临时缓存：./smart_wardrobe/temp_upload/ (用于存放用户刚上传、待确认的原始图片)。

## File Check:
检查索引数据库 ./smart_wardrobe/inventory.md。
若不存在：创建该文件并写入如下标准表头及对齐行：
| 分类 | 衣物编号 | 衣物名称 | 主要颜色 | 材质 | 风格 | 适宜的温度 | 推荐季节 | 适合的场景 | 当日日期 | 衣物状态 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
若已存在：跳过创建，准备在末尾追加数据。

# 3. Execution Logic (执行逻辑)

> 🚨 **串行流转处理规则 (Sequential Queue Processing Rule)**：
> 当用户批量上传多张照片时，严禁一次性处理完毕。Agent 必须严格遵循以下单张串行循环逻辑（Step 1 ~ Step 4）：
> 
> **【Step 1】** 全部接收并生成时间戳，存入临时列队。
> **【Step 2】** 按时间先后取出最早第一张，执行多模态大模型特征提取。
> **【Step 3】** 将当前照片重命名为即定 ID 锁定保护，隐藏编号并**停驻等待**用户确认。
> **【Step 4】** 按用户最终指令（确认/放弃/修改）执行入库或删除，随后立即**循环回到 Step 2** 处理下一张，直至列队完全清空。

## Step 1: Image Processing (图像预处理)
调用 `receive_image(image_file)`，接收用户上传的照片。如果是多张照片，依次全部纳入。该环节会自动将文件名命名规则设定为包含接收时间的 `temp_processing_YYYY-MM-DD_HH-mm-ss`，存入 `./smart_wardrobe/temp_upload/`。

## Step 2: Next Image Fetch & Analytics (提取待处理照片与分析)
调用 `get_next_temp_processing()` 获取接收时间最早的待处理照片。如果目录中不存在带有 `temp_processing` 各式的文件，则代表列队执行完毕，跳至收尾工作完毕流程。
获取到照片后，调用 `load_prompt_template()` 以及 `build_model_payload()` 组装 payload，直接请求多模态大模型提取特征，并拿到具有正确格式的 Markdown 表格行输出（其中带有自动生成的 12 位不重复编号）。

## Step 3: Interaction Prep (停驻前预处理与确认) - [CRITICAL BORDER]
在拿到模型的表格反馈后，**立即调用** `prepare_interaction(temp_path, markdown_row)`。
*工具层逻辑*：此时工具提取生成的编号，并在内部二次检查冲突。若通过校验，会将照片改名为 `[12位即定ID]_temp_push.[ext]`，确保数据安全性。若返回 conflict 错误，AI 需立即重新生成编号并再试。
**重点注意：不向用户展示12位衣物编号**。向用户展示特征表格进行确认时，**必须遮蔽或者不显示“衣物编号”这一列的信息**，避免用户轻易修改造成错乱。
*状态标识*：展示完毕后，进入 `WAIT_CONFIRM` 停驻状态。
*必须暂停*：在获得用户确认或修改指令之前，严禁直接执行自动入库！
*指令监听与分支*：
    * **情况 A（用户确认）**：回复“确认”、“没问题”等 ➡ `handle_user_decision(action="confirm")`
    * **情况 B（用户放弃）**：回复“放弃”、“不要入库”等 ➡ `handle_user_decision(action="abandon")`
    * **情况 C（用户修改）**：给出了修改后的新数据（即使包含新ID） ➡ `handle_user_decision(action="modify")`

## Step 4: Archiving based on Decision (基于决断的归档)
调用 `handle_user_decision(action, temp_push_path, markdown_data)`：
* 工具端会自动将修改后的 `markdown_data` 里面对应的编号强行设回最初存入 `temp_push` 对应的那个“最初模型生成的 ID”，不管用户在情况 C 提供的新 markdown 是否改变了ID字段：新markdown的id与原temp_push不一致时，强行按照原temp_push入库并持久保留。
* **对于确认 / 修改分支 (A & C)**：工具会将 `temp_push` 的图片按规则命令保存至持久化目录 `wardrobe_data/` 并更新提取处理后的数据入库 `inventory.md`。
* **对于放弃分支 (B)**：工具直接删除 `temp_upload/` 里不需要的该 `temp_push` 文件。
当本步结束并获取成功信息后，**自动跳回 Step 2 (`get_next_temp_processing()`) 继续处理后续积压照片**，直到所有获取操作返回 `empty` 为止。

# 4. Error Handling (异常处理)
编号冲突：若 ID 在 `prepare_interaction` 时被告知冲突，必须自动重新随机生成合规的 12 位大写英数新 ID 继续请求改名，直到成功。
格式异常：如果有异常必须及时反馈用户并等待下一轮互动。

# 5. Constraint (约束)
由于加入了逐张列队系统，每次操作只有明确等待用户的反馈才可进入下一个文件的处理。
`cleanup_temp()` 触发于暂停整体入库动作时，或已经完成了所有的入库循环（列队清空跳出）后，作为最后的收尾双保险进行大清理。