🌐 IP 归属地查询技能 - 使用指南

📁 文件夹结构:
├── SKILL.md              # 技能核心文件
├── scripts/
│   └── ip-lookup.sh      # IP 查询脚本
├── references/
│   └── fields.md         # API 字段参考
└── assets/               # 资源文件（空）

🚀 快速开始:

1️⃣  查询当前公网 IP
   ./scripts/ip-lookup.sh

2️⃣  查询指定 IP
   ./scripts/ip-lookup.sh 8.8.8.8

3️⃣  批量查询
   ./scripts/ip-lookup.sh 8.8.8.8 1.1.1.1 208.67.222.222

4️⃣  查看帮助
   ./scripts/ip-lookup.sh --help

📋 输出示例:

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🌐 IP 地址：8.8.8.8
📍 位置：美国 US · California · Mountain View 94035
🌍 坐标：纬度 37.386, 经度 -122.0838
🕐 时区：America/Los_Angeles
🌐 运营商：Google LLC
🏢 组织：Public DNS
🔗 AS 号：AS15169 Google LLC
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚠️ 注意事项:

- 免费版限制：60 次/分钟，4500 次/天
- 内网 IP（192.168.x.x）无法定位
- 位置是估算值，非精确位置
- 商业用途需购买付费版

🔗 相关链接:

- API 文档：https://ip-api.com/docs/
- 付费版：https://ip-api.com/

祝你使用愉快！🦾
