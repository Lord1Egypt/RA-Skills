# Mobile Meeting API Integration Skill

移动会议/云视讯API集成技能，为开发者提供完整的会议管理API集成指导和工具。

## 功能特性

- **会议管理**：创建、查询、更新、取消会议
- **录制管理**：查询录制文件和下载链接
- **会议控制**：会中操作，如邀请、静音、挂断
- **用户管理**：企业通讯录查询
- **可执行脚本**：提供Python脚本快速测试API

## 快速开始

### 1. 获取API凭证

从[云视讯/移动会议开发者中心](https://www.125339.com.cn/developerCenter/ReBar/63/222)获取：
- APP_ID
- APP_KEY
- USER_ID

### 2. 运行脚本示例

```bash
# 获取Token
python scripts/get_token.py

# 创建会议
python scripts/create_meeting.py

# 查询会议
python scripts/search_meetings.py
```

### 3. 使用技能

在支持的环境中，提及“移动会议”、“云视讯”或“会议API”即可激活技能。或者使用user_skill指令手动激活技能mobile-meeting-api

## API文档

完整API文档位于`references/`文件夹，或访问[开发者中心](https://www.125339.com.cn/developerCenter/ReBar/63/197)。

## 项目结构

```
mobile-meeting/
├── SKILL.md              # 技能主文档
├── README.md             # 项目说明
├── requirements.txt      # Python依赖
├── examples/             # 代码示例
│   ├── python_example.py
│   └── javascript_example.js
├── scripts/              # 可执行脚本
│   ├── get_token.py
│   ├── create_meeting.py
│   ├── search_meetings.py
│   └── cancel_meeting.py
└── references/           # API文档
    ├── CreateMeeting.md
    ├── SearchMeetings.md
    └── ...
```

## 贡献

欢迎提交Issue和Pull Request！

## 许可证

MIT License