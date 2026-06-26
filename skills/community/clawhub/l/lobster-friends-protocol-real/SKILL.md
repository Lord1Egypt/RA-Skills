---
name: lobster-friends-protocol
description: "龙虾好友协议技能：基于P2P加密通讯的社交好友管理系统，提供好友发现、关系管理、安全通信和社交图谱功能。"
author: "柏然 (通过小龙虾实现)"
version: "1.0.0"
created: "2026-03-12"
license: "MIT"
metadata:
  openclaw:
    emoji: "🦞🤝"
    requires:
      bins: ["bash", "jq", "openssl", "sqlite3"]
    dependencies:
      - "secure-p2p-messenger"
    install:
      - id: "scripts"
        kind: "shell"
        command: "./install.sh"
        label: "安装龙虾好友协议技能"
    examples:
      - input: "发现附近的小龙虾好友"
        output: "扫描网络发现可用的好友节点"
      - input: "添加新好友"
        output: "交换公钥，建立加密通信通道"
      - input: "查看好友列表"
        output: "显示所有好友的信任等级和状态"
      - input: "给好友发送加密消息"
        output: "使用好友公钥加密并发送消息"
      - input: "管理好友分组"
        output: "创建、编辑好友分组（家人、同事、朋友）"
---

# 龙虾好友协议技能

## 技能描述
这是一个基于P2P加密通讯的社交好友管理系统，专为小龙虾生态设计。它建立在`secure-p2p-messenger`基础上，提供完整的好友发现、关系管理、安全通信和社交图谱功能。

## 核心特性

### 🔍 **智能好友发现**
- **网络扫描**：自动发现同一网络中的小龙虾节点
- **公钥交换**：安全交换加密身份信息
- **指纹验证**：可视化指纹验证防止中间人攻击
- **离线发现**：支持蓝牙、WiFi Direct等离线发现方式

### 👥 **好友关系管理**
- **信任等级系统**：1-5级信任评级（陌生人 → 亲密好友）
- **好友分组**：自定义分组管理（家人、同事、兴趣小组）
- **关系图谱**：可视化社交关系网络
- **活动状态**：实时显示好友在线/离线状态

### 🔐 **安全通信层**
- **继承自secure-p2p-messenger**：完整的端到端加密
- **专属通信通道**：每个好友关系有独立的加密通道
- **消息历史**：本地加密存储所有通信记录
- **文件共享**：安全的好友间文件传输

### 📊 **社交智能**
- **互动频率分析**：自动分析好友互动模式
- **兴趣匹配**：基于通信内容的兴趣发现
- **关系建议**：智能推荐可能认识的人
- **社交健康度**：评估社交关系的活跃度和质量

## 协议架构

### **1. 好友发现协议**
```
发现阶段：
1. 广播发现信号（加密的"hello"消息）
2. 接收响应，交换公钥
3. 验证指纹，确认身份
4. 建立临时加密通道
5. 完成好友添加流程
```

### **2. 好友关系协议**
```
关系状态机：
陌生人 → 已发现 → 待验证 → 已验证 → 好友 → 亲密好友
      ↓         ↓         ↓         ↓         ↓
   可发现    可添加    需验证    可通信    高信任
```

### **3. 社交图谱协议**
```
图谱结构：
节点：小龙虾身份（公钥 + 元数据）
边：好友关系（信任等级 + 互动数据）
属性：分组、标签、互动历史
```

## 文件结构

```
lobster-friends-protocol/
├── SKILL.md (本文件)
├── lobster-friends.sh          # 主管理脚本
├── friend-discovery.sh         # 好友发现脚本
├── friend-manager.sh           # 好友管理脚本
├── social-graph.sh             # 社交图谱脚本
├── install.sh                  # 安装脚本
├── config/
│   ├── friends-db.schema       # 好友数据库架构
│   ├── discovery-config.json   # 发现配置
│   └── trust-rules.json        # 信任规则
├── lib/
│   ├── protocol-core.sh        # 协议核心
│   ├── discovery-engine.sh     # 发现引擎
│   ├── trust-manager.sh        # 信任管理器
│   ├── graph-builder.sh        # 图谱构建器
│   └── crypto-wrapper.sh       # 加密包装器
├── data/
│   ├── friends.db              # SQLite好友数据库
│   ├── social-graph.json       # 社交图谱数据
│   └── messages/               # 加密消息存储
└── ui/
    ├── friend-list.sh          # 好友列表界面
    ├── discovery-ui.sh         # 发现界面
    └── graph-visualizer.sh     # 图谱可视化
```

## 与secure-p2p-messenger的集成

### **继承关系**
```
secure-p2p-messenger (基础)
    ├── 加密核心 (RSA + AES)
    ├── 身份系统 (公钥基础设施)
    └── 消息协议 (加密信封)
    
lobster-friends-protocol (扩展)
    ├── 好友发现层
    ├── 关系管理层
    ├── 社交图谱层
    └── 信任系统层
```

### **数据流**
```
用户操作 → 好友协议层 → 加密通讯层 → 网络传输
                                  ↓
接收消息 ← 解密验证层 ← 网络接收 ← 加密传输
```

## 使用场景

### **场景1：建立新的好友关系**
```bash
# 1. 启动好友发现
lobster-friends.sh discover

# 2. 查看发现的好友
lobster-friends.sh list-discovered

# 3. 添加好友
lobster-friends.sh add-friend <friend-id>

# 4. 验证指纹
lobster-friends.sh verify-fingerprint <friend-id>

# 5. 发送欢迎消息
lobster-friends.sh send-message <friend-id> "你好！"
```

### **场景2：管理好友关系**
```bash
# 查看好友列表
lobster-friends.sh list-friends

# 设置信任等级
lobster-friends.sh set-trust <friend-id> 4

# 添加到分组
lobster-friends.sh add-to-group <friend-id> "同事"

# 查看社交图谱
lobster-friends.sh show-graph
```

### **场景3：好友间协作**
```bash
# 创建协作组
lobster-friends.sh create-group "项目团队"

# 添加多个好友到组
lobster-friends.sh add-members-to-group "项目团队" friend1 friend2 friend3

# 发送组消息
lobster-friends.sh send-group-message "项目团队" "明天开会"

# 共享文件给组
lobster-friends.sh share-file "项目团队" /path/to/document.pdf
```

## 安全与隐私

### **隐私保护**
- **选择性披露**：只分享必要的信息给好友
- **关系隐私**：好友关系本地存储，不上传
- **通信加密**：所有消息端到端加密
- **元数据保护**：最小化暴露通信模式

### **安全机制**
- **双重验证**：公钥 + 指纹验证
- **信任渐进**：逐步建立信任关系
- **异常检测**：检测可疑的好友行为
- **关系审计**：定期审查好友关系

### **数据控制**
- **本地优先**：所有数据存储在本地
- **用户主权**：用户完全控制好友关系
- **可导出**：支持好友关系导出备份
- **可删除**：彻底删除好友关系和所有数据

## 安装与配置

### **1. 安装依赖**
```bash
# 安装必需工具
sudo apt-get install sqlite3 jq openssl

# 安装基础技能
cd ~/.openclaw/workspace/skills/secure-p2p-messenger
./install.sh
```

### **2. 安装本技能**
```bash
cd ~/.openclaw/workspace/skills/lobster-friends-protocol
./install.sh
```

### **3. 初始化**
```bash
# 初始化好友系统
lobster-friends.sh init

# 生成加密身份（如果还没有）
lobster-friends.sh generate-identity

# 配置发现设置
lobster-friends.sh config discovery.mode "hybrid"
```

## 高级功能

### **1. 智能好友推荐**
基于以下因素推荐好友：
- 共同好友数量
- 地理位置接近度
- 兴趣标签匹配度
- 社交圈重叠度

### **2. 关系健康度监控**
监控指标：
- 通信频率变化
- 消息响应时间
- 互动质量评分
- 关系活跃度趋势

### **3. 社交图谱分析**
分析功能：
- 中心性分析（谁是最重要的好友）
- 社区检测（发现社交子群）
- 关系路径查找（通过谁认识谁）
- 影响力评估

### **4. 跨平台好友同步**
支持：
- 多设备好友同步（通过加密通道）
- 好友关系备份和恢复
- 好友列表导出/导入
- 跨网络好友发现

## 故障排除

### **常见问题**
1. **无法发现好友**
   ```
   原因：网络配置问题或防火墙阻止
   解决：检查网络设置，确保端口开放
   ```

2. **指纹验证失败**
   ```
   原因：中间人攻击或密钥错误
   解决：通过安全渠道验证指纹
   ```

3. **好友状态不同步**
   ```
   原因：设备间同步延迟
   解决：手动触发同步或检查网络
   ```

### **调试模式**
```bash
# 启用详细日志
export LOBSTER_FRIENDS_DEBUG=1
lobster-friends.sh discover --verbose

# 查看数据库状态
lobster-friends.sh db-status

# 检查协议版本
lobster-friends.sh protocol-version
```

## 路线图

### **v1.0 (基础版)**
- [x] 好友发现和添加
- [x] 基本好友管理
- [x] 加密通信集成
- [x] 本地社交图谱

### **v1.1 (增强版)**
- [ ] 智能好友推荐
- [ ] 关系健康度分析
- [ ] 跨设备同步
- [ ] 高级分组管理

### **v1.2 (社交版)**
- [ ] 兴趣匹配系统
- [ ] 社交活动协调
- [ ] 好友间资源共享
- [ ] 社交游戏化元素

### **v2.0 (生态版)**
- [ ] 跨技能好友集成
- [ ] 去中心化社交网络
- [ ] 区块链身份验证
- [ ] AI社交助手

## 社区与贡献

### **加入龙虾社交网络**
```
1. 安装技能并初始化
2. 发现附近的小龙虾用户
3. 建立第一个好友关系
4. 参与社区协作
```

### **贡献指南**
欢迎贡献：
1. 新的发现协议实现
2. 社交算法改进
3. 用户界面优化
4. 安全增强功能

### **反馈与支持**
- **问题报告**：GitHub Issues
- **功能建议**：社区讨论
- **安全漏洞**：安全邮件报告
- **使用帮助**：文档和示例

---

**版本**: 1.0.0  
**协议**: 龙虾好友协议 v1  
**兼容**: secure-p2p-messenger v1.0+  
**状态**: 开发中  

🦞 *"真正的连接始于安全的握手，成长于持续的信任"* 🦞