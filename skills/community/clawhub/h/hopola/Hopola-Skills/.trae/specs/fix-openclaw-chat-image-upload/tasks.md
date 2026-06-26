# Tasks
- [x] Task 1: 梳理并复现 OpenClaw 对话图片上传失败链路
  - [x] SubTask 1.1: 收集失败样例输入与当前返回链接差异
  - [x] SubTask 1.2: 标注失败发生阶段（解析/上传/校验）
- [x] Task 2: 实现输入归一化与上传结果标准化
  - [x] SubTask 2.1: 增加 OpenClaw 会话图片引用归一化逻辑
  - [x] SubTask 2.2: 增加 URL 标准化与重复斜杠处理逻辑
  - [x] SubTask 2.3: 统一结构化错误返回与提示文案
- [x] Task 3: 完成验证与文档同步
  - [x] SubTask 3.1: 执行单图/会话图/异常 URL 回归验证
  - [x] SubTask 3.2: 更新相关技能文档与配置说明
  - [x] SubTask 3.3: 重新打包并核对产物可用性
- [x] Task 4: 修复带编码字符路径的会话图片解析
  - [x] SubTask 4.1: 保留本地路径中的 `%2F` 字面量，避免误解码
  - [x] SubTask 4.2: 回归验证 markdown 包装的本地缓存路径上传

# Task Dependencies
- Task 2 depends on Task 1
- Task 3 depends on Task 2
- Task 4 depends on Task 3
