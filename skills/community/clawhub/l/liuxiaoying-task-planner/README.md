# task-planner - OpenClaw 任务管理助手

个人任务与行程管理助手，支持微信语音输入、定时提醒、重复任务、日历导出。

## 功能特性

- ✅ 自然语言添加/修改/删除任务
- ✅ 截止时间 + 提醒（可设置提前提醒）
- ✅ 重复任务（每日/每周/每月/每年）
- ✅ 自动发送提醒到微信
- ✅ 导出日历为 Markdown 表格
- ✅ 微信语音转文字（需 OpenAI API Key）

## 安装方法

```bash
mkdir -p ~/.openclaw/skills/task-planner
cp -r * ~/.openclaw/skills/task-planner/
openclaw gateway restart
pip3 install openai
MIT
# openclaw-task-planner
