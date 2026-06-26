---
name: jimeng-video
description: 在 Jimeng（即梦）里稳定执行“视频生成→等待完成→下载本地”流程。用于需要生成视频、查找最新视频、下载 mp4 的场景。内置前置健康检查、状态机执行、长等待轮询与防抖规则，降低卡住和误操作概率。
---

# Jimeng Video

用于 **Jimeng 视频任务**，目标是稳定完成：
- 打开视频页
- 提交生成
- 等待完成
- 下载本地文件

浏览器必须走 OpenClaw 托管链路：
```bash
openclaw browser --browser-profile <profile> <subcommand>
```

---

## 0) 强制执行约束（提高成功率）

### A. 前置健康检查固定化（每次必做）
按顺序固定执行，不跳步：
1. `status`
2. 如 `running:false` 则 `start`
3. `open` 视频页
4. `snapshot`

只有上一步成功，才进入下一步。

### B. 状态机执行（禁止自由发挥）
只允许按以下状态前进：
- `PRECHECK`
- `MODE_GUARD`
- `SUBMIT`
- `POLL`
- `DOWNLOAD`
- `VERIFY`
- `DONE` / `FAILED`

每个状态都有：
- 成功条件
- 最大重试次数
- 失败后的去向

### C. 轮询策略固定
- 轮询间隔：**20–30 秒**
- 最大总等待：**12 分钟**
- 到上限仍未完成：标记 `FAILED(timeout)`，不要无限等

### D. 防抖与去风暴
- 页面未跳转时，禁止重复 `open`
- 非 ref 失效场景，禁止连续 `snapshot`
- 同一状态下 `snapshot` 连续失败 2 次，先回 `PRECHECK`

---

## 1) 适用场景

当用户要：
- 生成 Jimeng 视频
- 找到最新一条已生成视频
- 下载视频到本地

不适用于：
- 纯文本问答（不需要浏览器）
- 图片生成（请用 `jimeng-image`）

---

## 2) 入口与 profile

视频入口：
```text
https://jimeng.jianying.com/ai-tool/home/?workspace=0&type=video
```

profile 选择优先级：
1. 当前 agent 专用 profile
2. 用户指定 profile
3. 默认 profile
4. `openclaw`（兜底）

---

## 3) 状态机定义（含成功条件和重试上限）

### PRECHECK
动作：
1. `status`
2. 如未启动则 `start`
3. `open` 视频页
4. `snapshot`

成功条件：
- snapshot 能拿到可交互页面结构

重试上限：
- 整体最多 2 轮

失败去向：
- 超过上限 -> `FAILED(precheck)`

---

### MODE_GUARD
动作：
- 检查当前模式是否 `首尾帧`
- 若是且没有上传首尾帧图片：切换到 `全能参考`
- 切换后重新 snapshot 确认

成功条件：
- 当前模式可用于无参考图生成（通常为 `全能参考`）

重试上限：
- 2 次

失败去向：
- 回 `PRECHECK` 1 次
- 再失败 -> `FAILED(mode_guard)`

---

### SUBMIT
动作：
- 填写提示词
- 按需设置模型/时长/比例
- 点击生成
- snapshot 确认任务已提交

模型/时长规则（必须校验）：
- 若用户指定 `Seedance 2.0 Fast`，可选时长 `4s`~`15s`
- 用户指定不支持组合时：停止并告知，不要擅自改参数

成功条件：
- 页面出现“提交成功/排队中/生成中/可追踪任务”任一信号

重试上限：
- 2 次

失败去向：
- 回 `MODE_GUARD` 1 次
- 再失败 -> `FAILED(submit)`

---

### POLL
动作：
- 每 20–30 秒检查一次
- 每轮只做一次 snapshot + 一次状态判断
- 判断是否出现：`下载` / `去查看` / 已完成卡片

成功条件：
- 找到可下载入口（直接下载按钮或可进入详情页）

重试上限：
- 最多 24 轮（约 12 分钟）

失败去向：
- 超时 -> `FAILED(timeout)`

---

### DOWNLOAD
动作：
- 优先在当前页下载
- 若当前页无下载入口，走资产页兜底：
  - 打开 `https://jimeng.jianying.com/ai-tool/asset`
  - 查找最新生成视频
  - 进入详情下载

成功条件：
- 下载命令返回本地路径

重试上限：
- 2 次

失败去向：
- 回 `POLL` 1 次再找入口
- 再失败 -> `FAILED(download)`

---

### VERIFY
动作：
- 校验文件存在
- 校验大小 > 0
- 扩展名为 mp4（或页面声明的视频格式）

成功条件：
- 文件可用且路径可回报

重试上限：
- 1 次重新下载

失败去向：
- `FAILED(verify)`

---

## 4) 标准执行模板（最小可靠版）

1. `PRECHECK`
2. `MODE_GUARD`
3. `SUBMIT`
4. `POLL`（20–30 秒间隔，最长 12 分钟）
5. `DOWNLOAD`
6. `VERIFY`
7. 输出路径并 `DONE`

---

## 5) 故障处理

### Gateway / 浏览器链路异常
- 先回 `PRECHECK`
- 不要在中间状态无限重试

### Ref 失效
- 只允许“重新 snapshot 一次”
- 仍失败则回退上一个状态

### 下载入口消失
- 直接走资产页兜底，不在当前页盲点

---

## 6) 反模式（禁止）

- 连续重复 `open` 同一页面
- 高频 snapshot（无状态变化还不断抓）
- 忘记 `running:false` 就直接点页面
- 轮询无上限，导致看起来“卡死”
- 下载后不校验文件是否真实落地

---

## 7) 成功标准

任务完成必须回报：
1. 本地绝对路径
2. 文件校验结果（存在/大小/格式）
3. 失败时给出明确失败状态（如 `FAILED(timeout)`）
